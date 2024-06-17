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
import os, sys, time
import Logger as log
import traceback
from robot.libraries.BuiltIn import BuiltIn
import CRobot
from datetime import datetime
curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curDir, '../commonlib'))
sys.path.append(os.path.join(curDir, '../../crobot'))
sys.path.append(os.path.join(curDir, '../../crobot/legacy'))
import CommonKeywords
import CommonLib
workDir = CRobot.getWorkDir()
sys.path.append(workDir)

try:
  from common.sdk.InitFrameworkLib import *
  from Const import *
  from Device import Device
  import DeviceMgr
except Exception as err:
  log.cprint(str(err))
  log.cprint(traceback.format_exc())

###################################################################################
# Common Wrapper Library Functions
###################################################################################
def Log_Info(msg):
    dLibObj = getSdkLibObj()
    dLibObj.wpl_log_info(msg)

def ssh_login_bmc():
    dLibObj = getSdkLibObj()
    dLibObj.ssh_login_bmc()


def ssh_disconnect():
    dLibObj = getSdkLibObj()
    dLibObj.ssh_disconnect()


def Log_Debug(msg):
    dLibObj = getSdkLibObj()
    dLibObj.wpl_log_debug(msg)


def Switch_To_Centos():
    return CommonLib.switch_to_centos()


def Switch_To_Openbmc():
    return CommonLib.switch_to_openbmc()


def reboot_bmc():
    Log_Debug("Entering procedure reboot_bmc.\n")
    return CommonLib.reboot("openbmc")


def reboot_centos():
    Log_Debug("Entering procedure reboot_centos.\n")
    return CommonLib.reboot("centos")


def Check_IP_Address():
    Log_Debug("Entering procedure Check_IP_Address.\n")
    dLibObj = getSdkLibObj()

    var_interface = eth_int_params['interface']
    var_mode = 'centos'

    return CommonLib.check_ip_address(Const.DUT, var_interface, var_mode)


def Ping_IP_Address(ip, mode):
    Log_Debug("Entering procedure Ping_IP_Address.\n")
    dLibObj = getSdkLibObj()

    var_ipAddr = ip
    var_mode = 'centos'
    var_count = 5

    return CommonLib.exec_ping(Const.DUT, var_ipAddr, var_count, var_mode)


def change_dir_to_sdk_path():
    Log_Debug("Entering procedure change_dir_to_sdk_path.\n")

    var_path = SDK_PATH
    var_mode = centos_mode
    return CommonLib.change_dir(var_path, var_mode)


def change_dir_to_default():
    Log_Debug("Entering procedure change_dir_to_default.\n")

    return CommonLib.change_dir()


def load_sdk_port_mode_dd_8x50g_qsfp_4x50g():
    Log_Debug("Entering procedure load_sdk_port_mode_dd_8x50g_qsfp_4x50g. \n")
    dLibObj = getSdkLibObj()

    var_portMode = 'dd_8x50g_qsfp_4x50g'
    var_expectedPortDict = portStatusDD_8X50G_QSFP_4X50G
    var_expectedResult = ok_keyword
    var_devicePhase = DUT_PHASE

    return dLibObj.load_sdk_init_with_portcheck(var_portMode, var_expectedPortDict, var_expectedResult, var_devicePhase)

def load_sdk_port_mode_dd_8x50g_qsfp_4x25g():
    Log_Debug("Entering procedure load_sdk_port_mode_dd_8x50g_qsfp_4x25g. \n")
    dLibObj = getSdkLibObj()

    var_portMode = 'dd_8x50g_qsfp_4x25g'
    var_expectedPortDict = portStatusDD_8X50G_QSFP_4X25G
    var_expectedResult = ok_keyword
    var_devicePhase = DUT_PHASE

    return dLibObj.load_sdk_init_with_portcheck(var_portMode, var_expectedPortDict, var_expectedResult, var_devicePhase)

def check_sdk_version():
    Log_Debug("Entering procedure check_sdk_version.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.verify_sdk_version(sdk_version_dict)

def run_port_loopback_test(portmode, loopback_type, full_log=True):
    Log_Debug("Entering procedure run_port_loopback_test.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.run_port_loopback_test(portmode, loopback_type, full_log=full_log)

def check_port_loopback_status(loopback_type):
    log.debug('Entering procedure check_port_loopback_status.\n ')
    dLibObj = getSdkLibObj()
    dLibObj.check_port_loopback_status(loopback_type)

def run_port_linkup_test(portmode):
    Log_Debug("Entering procedure run_port_linkup_test.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.run_port_linkup_test(portmode)

def run_default_port_info_test(portmode):
    Log_Debug("Entering procedure run_default_port_info_test.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.run_default_port_info_test(portmode)

def check_default_port_info_status(portmode):
    Log_Debug("Entering procedure check_default_port_info_status.\n")
    dLibObj = getSdkLibObj()
    try:
        dLibObj.check_default_port_info_status(portmode)
    except:
        raise Exception(traceback.format_exc())


def check_temperature():
    Log_Debug("Entering procedure check_temperature.\n")
    dLibObj = getSdkLibObj()

    var_expectedResult = r'-do_sensor_test.*TEST.*?PASS'

    return dLibObj.check_temperature(var_expectedResult)


def check_max_power():
    Log_Debug("Entering procedure check_max_power.\n")
    dLibObj = getSdkLibObj()

    var_expectedResult = ok_keyword
    var_devicePhase = DUT_PHASE

    return dLibObj.check_max_power(var_expectedResult, var_devicePhase)


def check_voltage():
    Log_Debug("Entering procedure check_voltage.\n")
    dLibObj = getSdkLibObj()

    var_expectedResult = ok_keyword

    return dLibObj.check_voltage(var_expectedResult)


def check_Memory_BIST():
    Log_Debug("Entering procedure check_Memory_BIST.\n")
    dLibObj = getSdkLibObj()

    var_expectedResult = 'OK'

    return dLibObj.check_memory_bist(var_expectedResult)


def run_test_L2_traffic(portmode):
    Log_Debug("Entering procedure test_L2_traffic.\n")
    dLibObj = getSdkLibObj()
    var_runningTime = 300
    test_level = 'L2'

    return dLibObj.test_traffic(portmode, var_runningTime, test_level)

def run_test_L3_traffic(portmode):
    Log_Debug("Entering procedure test_L3_traffic.\n")
    dLibObj = getSdkLibObj()
    var_runningTime = 300
    test_level = 'L3'

    return dLibObj.test_traffic(portmode, var_runningTime, test_level)

def check_L2_traffic_status(portmode):
    Log_Debug("Entering procedure check_L2_traffic_status.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.check_traffic_status(portmode)

def check_L3_traffic_status(portmode):
    Log_Debug("Entering procedure check_L3_traffic_status.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.check_traffic_status(portmode)

def step(StepNumber, name, *args):
    log.debug('Entering procedure step[%s]\n '%(str(locals())))
    return BuiltIn().run_keyword(name, *args)

def run_sdk_initialization(portmode):
    dLibObj = getSdkLibObj()

    return dLibObj.load_sdk_init(portmode)

def go_to_centos():
    dLibObj = getSdkLibObj()

    dLibObj.getback_2_centos()

def check_sdk_port_status(portmode):
    log.debug('Entering procedure check_sdk_port_status with input [%s]\n '%(str(locals())))
    dLibObj = getSdkLibObj()

    return dLibObj.check_sdk_port_status(ok_keyword, portmode)

def run_mac_port_ber_test(portmode):
    log.debug('Entering procedure run_mac_port_ber_test with input [%s]\n '%(str(locals())))
    dLibObj = getSdkLibObj()
    dLibObj.run_mac_port_ber_test(portmode)

def check_mac_port_ber_status(portmode):
    log.debug('Entering procedure check_mac_port_ber_status with input [%s]\n '%(str(locals())))
    dLibObj = getSdkLibObj()
    dLibObj.check_mac_port_ber_status(portmode, ber_threshold)

def test_manufacture():
    Log_Debug("Entering procedure test_manufacture.\n")
    dLibObj = getSdkLibObj()
    dLibObj.run_manufacture_test()

def reinit_test():
    Log_Debug("Entering procedure reinit_test.\n")
    dLibObj = getSdkLibObj()
    dLibObj.reinit_test()

def check_reinit_port_status():
    Log_Debug("Entering procedure check_reinit_port_status.\n")
    dLibObj = getSdkLibObj()
    check_keywords = [r'.*do_reinit_test- TEST.*PASS', r'Reload SDK\(MBIST\) Test']
    dLibObj.check_reinit_port_status(check_keywords)

def run_port_enable_disable():
    Log_Debug("Entering procedure run_port_enable_disable.\n")
    dLibObj = getSdkLibObj()
    dLibObj.run_port_enable_disable()

def check_port_enable_disable_status():
    Log_Debug("Entering procedure check_port_enable_disable_status.\n")
    dLibObj = getSdkLibObj()
    check_keywords = [r'-do_port_linkup_validation_test- TEST.* PASS', r'META Wedge400C Run Test All.*PASS']
    dLibObj.check_port_enable_disable_status(check_keywords)

def copy_sdk_soc_files_w400():
    Log_Debug("Entering procedure copy_sdk_soc_files_w400.\n")
    dLibObj = getSdkLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    eth_tool = ETH_TOOL
    dhcp_tool = DHCP_TOOL
    #var_filelist = sdk_soc_files
    var_filepath = sdk_soc_dir_w400
    var_destination_path = SDK_PATH
    #var_mode = centos_mode
    #dLibObj.get_ipv6_addr(eth_tool, dhcp_tool)
    #get_dhcp_ipv6_addresses('eth0')
    #var_interface = eth_int_params['interface']

    dLibObj.prepare_sdk_soc_images(eth_tool, dhcp_tool, var_server_ip, var_username, var_password, var_filepath, var_destination_path)
    #output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

###################MINIPACK2#############################

def verify_load_HSDK(script_name='auto_load_user.sh'):
    Log_Debug("Entering procedure verify_load_HSDK.\n")
    dLibObj = getSdkLibObj()
    cmd = "./{}".format(script_name)
    remark = cmd

    return dLibObj.check_load_HSDK(cmd, pattern=[BCM_promptstr])

def verify_load_HSDK2(script_name='auto_load_user.sh'):
    Log_Debug("Entering procedure verify_load_HSDK2.\n")
    dLibObj = getSdkLibObj()

    cmd = "./{} ".format(script_name) + " -m 64x200_32x400"
    remark = cmd

    return dLibObj.check_load_HSDK(cmd, pattern=[BCM_promptstr])

def verify_load_HSDK_w400(script_name='auto_load_user.sh'):
    Log_Debug("Entering procedure verify_load_HSDK.\n")
    dLibObj = getSdkLibObj()
    cmd = "./{}".format(script_name)
    remark = cmd

    return dLibObj.check_load_HSDK_w400(cmd, pattern=[BCM_promptstr])

def pcie_lsmod_check():
    Log_Debug("Entering procedure pcie_lsmod_check.\n")
    dLibObj = getSdkLibObj()
    cmd = "lsmod |grep linux; sleep 1; ./auto_load_user.sh -r; sleep 1; lsmod |grep linux"
    return dLibObj.pcie_lsmod_check_w400(cmd)

def do_power_cycle():
    Log_Debug("Entering procedure do_power_cycle.\n")
    dLibObj = getSdkLibObj()
    return dLibObj.do_power_system_w400()

def exit_BCM():
    Log_Debug("Entering procedure exit_BCM.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.exit_BCM_mode()

def exit_mode(pre_prompt='>>>', dest_prompt='os', exit_cmd="exit()"):
    Log_Debug("Entering procedure exit_mode.\n")
    dLibObj = getSdkLibObj()
    dest_prompt = dLibObj.device.promptDiagOS if dest_prompt == "os" else dest_prompt

    return dLibObj.exit_console_mode(previous_prompt=pre_prompt, dest_prompt=dest_prompt, exit_cmd=exit_cmd)

def verify_BCM_version():
    Log_Debug("Entering procedure verify_BCM_version.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.check_BCM_version()

def enter_SDKLT_mode():
    Log_Debug("Entering procedure enter_SDKLT_mode.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.enter_SDKLT()

def verify_PCIe_version():
    Log_Debug("Entering procedure verify_PCIe_version.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.check_PCIe_version()

def exit_SDKLT_mode():
    Log_Debug("Entering procedure exit_SDKLT_mode.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.exit_SDKLT()

def startup_default_port_group(use_xphyback=True, init_cmd=xphy_init_mode2):
    Log_Debug("Entering procedure startup_default_port_group.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.startup_default_port(use_xphyback=use_xphyback, init_cmd=init_cmd)

def check_pim_number():
    Log_Debug("Entering procedure check_pim_number.\n")
    dLibObj = getSdkLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'minipack2_dc' in devicename.lower():
        return dLibObj.mp2_pim_number()
    else:
        return 0

def set_port_lb_mac(port_speed, pim_NA_num):
    Log_Debug("Entering procedure set_port_lb_mac.\n")
    dLibObj = getSdkLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'minipack2_dc' in devicename.lower():
        return dLibObj.port_lb_mac_set(port_type=port_speed, pim_NA_sum=pim_NA_num)

def check_all_port_status(port_status_pattern=port_up_status, port_cmd=ps_cd_cmd, port_search_pattern=port_pattern):
    Log_Debug("Entering procedure check_all_port_status.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.verify_all_port_status(port_status_pattern=port_status_pattern, port_cmd=port_cmd,
            port_search_pattern=port_search_pattern)


def check_all_port_status_w400(port_cmd=ps_cd_cmd):
    Log_Debug("Entering procedure check_all_port_status_w400.\n")
    dLibObj = getSdkLibObj()
    rpkt = r"CDMIB_RPKT\.\w+.*?([\d,]+)\s+.(\S+)"
    tpkt = r"CDMIB_TPKT\.\w+.*?([\d,]+)\s+.(\S+)"
    return dLibObj.verify_all_port_status_w400(port_cmd=port_cmd, port_rpkt=rpkt, port_tpkt=tpkt)

def check_all_ports_disabled(port_cmd=ps_cd_cmd):
    Log_Debug("Entering procedure check_all_ports_disabled.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.verify_all_port_status(port_status_pattern=port_disable_status, port_cmd=port_cmd)

def check_port_mode_setting(port_setting_pattern, port_cmd=ps_cd_cmd, port_search_pattern=port_pattern):
    Log_Debug("Entering procedure check_port_mode_setting.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.verify_all_port_status(port_status_pattern=port_setting_pattern,
            port_cmd=port_cmd, port_search_pattern=port_search_pattern)

def disable_all_ports(port_cmd=port_disable_cmd):
    Log_Debug("Entering procedure disable_all_ports.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.change_ports_status(port_config_cmd=port_cmd)

def enable_all_ports(port_cmd=port_enable_cmd):
    Log_Debug("Entering procedure enable_all_ports.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.change_ports_status(port_config_cmd=port_cmd)

def switch_port_mode_to_phy():
    Log_Debug("Entering procedure switch_port_mode_to_phy.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.change_ports_status(port_config_cmd=port_phy_cmd)

def set_prbs_mode_and_run_PRBS_test(prbs_cmd=set_prbs_run_PRBS_cmd):
    Log_Debug("Entering procedure set_prbs_mode_and_run_PRBS_test.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.change_ports_status(port_config_cmd=prbs_cmd)

def check_PRBS_result():
    Log_Debug("Entering procedure check_PRBS_result.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.check_port_PRBS()

def check_BER_level(ber_cmd=get_port_BER_level_cmd, ber_cmd_second=get_port_BER_level_cmd_second):
    Log_Debug("Entering procedure check_BER_level.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.check_port_BER(level_cmd=ber_cmd, level_cmd_second=ber_cmd_second)

def set_snake_vlan_to_all_ports(port_cmd=set_snake_vlan_200G_cmd):
    Log_Debug("Entering procedure set_snake_vlan_to_all_ports.\n")
    dLibObj = getSdkLibObj()
    patterns = fail_pattern
    output = ""
    for port_cmd in (port_cmd, pvlan_show_cmd, vlan_show_cmd):
        output += dLibObj.run_command(port_cmd, deviceObj=dLibObj.device,
                prompt=BCM_promptstr.replace(".","\."), timeout=300)
    check_status = dLibObj.check_output(output, patterns=patterns, is_negative_test=True)
    if not check_status:
        raise Exception("Execute {} failed.".format(port_cmd))

def set_snake_vlan_to_all_ports_w400(port_cmd=set_snake_vlan_400G_cmd, sustain_time=" ", sp=False):
    Log_Debug("Entering procedure set_snake_vlan_to_all_ports_w400.\n")
    dLibObj = getSdkLibObj()
    patterns = fail_pattern
    output = ""
    if sp == True:
        for port_cmd in (clear_c, port_cmd):
            output += dLibObj.run_command(port_cmd, deviceObj=dLibObj.device,
                                          prompt=BCM_promptstr.replace(".", "\."), timeout=300)
    else:
        for port_cmd in (clear_c, port_cmd, sustain_time):
            output += dLibObj.run_command(port_cmd, deviceObj=dLibObj.device,
                prompt=BCM_promptstr.replace(".","\."), timeout=300)
        check_status = dLibObj.check_output(output, patterns=patterns, is_negative_test=True)
        if not check_status:
            raise Exception("Execute {} failed.".format(port_cmd))

def show_temp():
    Log_Debug("Entering procedure show_temp.\n")
    dLibObj = getSdkLibObj()
    avgTemp = "average current temperature is\s+(\d+.\d)"
    maxTemp = "maximum peak temperature is\s+(\d+.\d)"
    traffic_time = "sleep 30"
    after_time = "sleep 10"
    normal = dLibObj.check_show_temp(temp_cmd=show_temp_cmd, avg_temp=avgTemp, max_temp=maxTemp)
    set_snake_vlan_to_all_ports_w400(port_cmd=set_snake_vlan_400G_cmd, sustain_time=traffic_time)
    traffic = dLibObj.check_show_temp(temp_cmd=show_temp_cmd, avg_temp=avgTemp, max_temp=maxTemp)
    stop_traffic(stop_traffic_cmd)
    check_all_port_status_w400(portdump_counters_cmd)
    dLibObj.run_command(after_time, deviceObj=dLibObj.device,
                prompt=BCM_promptstr.replace(".","\."), timeout=300)
    traffic_after = dLibObj.check_show_temp(temp_cmd=show_temp_cmd, avg_temp=avgTemp, max_temp=maxTemp)
    dLibObj.check_lst_cmp(normal, traffic, traffic_after)

def clear_all_port_counter():
    Log_Debug("Entering procedure clear_all_port_counter.\n")
    dLibObj = getSdkLibObj()
    dLibObj.change_ports_status(port_config_cmd=clear_c_cmd)
    patterns = fail_pattern

    return dLibObj.read_and_check_port(patterns)

def let_CPU_send_packages(port_cmd=let_CPU_send_package_cmd, port_len=''):
    Log_Debug("Entering procedure let_CPU_send_packages.\n")
    dLibObj = getSdkLibObj()
    #port_cmd = dLibObj.verify_TH4L(port_cmd)
    #port_len = verify_TH4L_or_TH4()
    # support other platforms
    if 'length' in port_cmd:
        dLibObj.change_ports_status(port_config_cmd=port_cmd)
    else:
        dLibObj.change_ports_status(port_config_cmd=port_cmd + port_len)
    patterns = fail_pattern
    finish_prompt = "{}[\s\S]+{}".format(port_cmd[:5], BCM_promptstr)
    output = dLibObj.device.read_until_regexp(finish_prompt, timeout=100)
    dLibObj.check_output(output, patterns=patterns, is_negative_test=True)

def verify_TH4L_or_TH4():
    Log_Debug("Entering procedure verify_TH4L_or_TH4.\n")
    dLibObj = getSdkLibObj()

    verify_th4_command = 'lspci -s 06:00.0'
    #length = ''
    return dLibObj.verify_TH4L(verify_th4_command)

def sleep_300s():
    Log_Debug("Entering procedure sleep_300s.\n")
    dLibObj = getSdkLibObj()
    dLibObj.change_ports_status(port_config_cmd=sleep_300s_cmd)
    time.sleep(300)
    finish_prompt = "{}[\s\S]+{}".format(sleep_300s_cmd[:5], BCM_promptstr)
    output = dLibObj.device.read_until_regexp(finish_prompt, timeout=400)
    dLibObj.check_output(output, patterns=sleep_pattern, is_negative_test=False)

def port_sleep(seconds=30):
    Log_Debug("Entering procedure port_sleep.\n")
    dLibObj = getSdkLibObj()
    seconds = int(seconds)
    cmd = "sleep {}".format(seconds)
    dLibObj.change_ports_status(port_config_cmd=cmd)
    time.sleep(seconds)
    finish_prompt = "{}[\s\S]+{}".format(cmd[:5], BCM_promptstr)
    output = dLibObj.device.read_until_regexp(finish_prompt, timeout=seconds+10)
    dLibObj.check_output(output, patterns=sleep_pattern, is_negative_test=False)

def stop_traffic(port_cmd=stop_traffic_cmd):
    Log_Debug("Entering procedure stop_traffic.\n")
    dLibObj = getSdkLibObj()
    dLibObj.change_ports_status(port_config_cmd=port_cmd)
    patterns = fail_pattern

    return dLibObj.read_and_check_port(patterns)

def check_power_sensor_value():
    Log_Debug("Entering procedure check_power_sensor_value.\n")
    dLibObj = getSdkLibObj()
    before_traffic_sensor = dLibObj.get_th3_core_power(port_cmd=check_power_cmd)
    dLibObj.change_to_sdk_bcm(cmd='sol.sh')
    set_snake_vlan_to_all_ports_w400(port_cmd=set_snake_vlan_all, sustain_time=sleep_time_sensor)
    Switch_To_Openbmc()
    after_traffic_sensor = dLibObj.get_th3_core_power(port_cmd=check_power_cmd)
    dLibObj.change_to_sdk_bcm(cmd='sol.sh')
    return dLibObj.check_value_cmp(before_traffic_sensor, after_traffic_sensor)

def check_show_c():
    Log_Debug("Entering procedure check_show_c.\n")
    dLibObj = getSdkLibObj()
    dLibObj.change_ports_status(port_config_cmd=show_c_cmd)
    finish_prompt = "{}[\s\S]+{}".format(show_c_cmd[:5], BCM_promptstr)
    output = dLibObj.device.read_until_regexp(finish_prompt, timeout=500)

    return dLibObj.check_XLMIB_RPKT(output=output)

def check_same_port(port_cmd=mac_port_counter_cmd, pattern=mac_port_counter_pattern, prompt_str=sdkConsole):
    Log_Debug("Entering procedure check_same_port.\n")
    dLibObj = getSdkLibObj()
    dLibObj.change_ports_status(port_config_cmd=port_cmd)
    finish_prompt = "{}[\s\S]+{}".format(port_cmd[:5], prompt_str)
    output = dLibObj.device.read_until_regexp(finish_prompt, timeout=500)

    return dLibObj.check_XLMIB_RPKT(pattern=pattern, output=output)

def check_lane_common_ucode_version(serdes_cmd=get_lane_serdes_version_cmd):
    Log_Debug("Entering check_lane_common_ucode_version.\n")
    dLibObj = getSdkLibObj()
    dLibObj.change_ports_status(port_config_cmd=serdes_cmd)

    return dLibObj.check_lane_common_version(patterns=lane_serdes_version_pattern)

def check_hmon_temperature():
    Log_Debug("Entering procedure check_temperature.\n")
    dLibObj = getSdkLibObj()
    dLibObj.change_ports_status(port_config_cmd=get_hmon_temperature_cmd)
    patterns = fail_pattern
    keywords_to_check = hmon_temperature_pattern
    SDKLT_prompt = SDKLT_array["SDKLT_prompt"]
    output = dLibObj.device.readUntil(SDKLT_prompt, timeout=100)
    dLibObj.check_output(output, patterns=patterns, is_negative_test=True)
    parserSDKLibs.PARSE_port_value_range_check(output, keywords_to_check, valid_value_range=(0, max_temperature))

def change_port_mode(port_mode_cmd=None):
    Log_Debug("Entering procedure clear_all_port_counter.\n")
    dLibObj = getSdkLibObj()
    dLibObj.change_ports_status(port_config_cmd=port_mode_cmd)
    patterns = fail_pattern

    return dLibObj.read_and_check_port(patterns)

def verify_remote_shell(cmd=None, patterns=None, is_negative_test=True):
    Log_Debug("Entering procedure verify_remote_shell.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.execute_check_dict(cmd=cmd, mode=centos_mode,
            patterns_dict=patterns, is_negative_test=is_negative_test)

def verify_remote_shell_port_status():
    Log_Debug("Entering procedure verify_remote_shell_port_status.\n")
    dLibObj = getSdkLibObj()
    time.sleep(2)
    dLibObj.device.sendMsg("\n")
    dLibObj.device.readMsg()

    cmd = cls_shell_port_status
    patterns = port_up_dict
    finish_prompt = "{}[\s\S]+{}".format(cmd[:30].rstrip(), dLibObj.device.promptDiagOS)
    output = dLibObj.device.sendCmdRegexp(cmd + "\n", finish_prompt, timeout=60)
    devicename = os.environ.get("deviceName", "")
    if 'minipack2_dc' in devicename.lower():
        port_sum = len(re.findall(port_pattern_dc, output))
    else:
        port_sum = len(re.findall(port_pattern, output))

    return dLibObj.execute_check_num(cmd="", mode=centos_mode, patterns_dict=patterns,
        expected_num=port_sum,check_output=output)

def check_remote_shell_port(sp=False):
    Log_Debug("Entering procedure check_remote_shell_port.\n")
    dLibObj = getSdkLibObj()
    dLibObj.device.sendMsg("\n")
    shell_cmd = cls_shell_port_status
    expect_port = port_pattern
    patterns = port_up_dict
    dLibObj.execute_check_shell_port(cmd=shell_cmd, patterns_dict=patterns, expect_value=expect_port, remark=sp)

def verify_load_user(cmd=None, patterns=init_pass_pattern, port_sum_pattern=init_port_pattern,
                     port_total=32, is_negative_test=False, timeout=3600):
    Log_Debug("Entering procedure verify_load_user.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.check_load_user(cmd, pattern_dict=patterns, port_sum_pattern=port_sum_pattern,
                                   port_total=port_total, prompt_str=sdkConsole, timeout=timeout)

def test_load_user(cmd=None, patterns=init_pass_pattern, prompt_str=sdkConsole, timeout=3300):
    Log_Debug("Entering procedure test_load_user.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.init_load_user(cmd, pattern_dict=patterns, prompt_str=prompt_str, timeout=timeout)

def scp_file_from_PC(mode=centos_mode, file_list=None, source_path=SOC_400G_file_path, dest_path=SDK_PATH):
    Log_Debug("Entering procedure scp_file_from_PC.\n")
    file_list = globals()[file_list]

    return CommonLib.copy_files_through_scp(Const.DUT, scp_username, scp_password, scp_ip, file_list, source_path, dest_path, mode)

def prepare_check_log_script():
    Log_Debug("Entering procedure prepare_check_log_script.\n")
    dLibObj = getSdkLibObj()

    return dLibObj.create_check_log_script()






def get_new_sdk_version(image_type,name, platform):
    if 'minipack3' in  platform:
        platform='minipack3'
    if 'minerva_janga' in platform:
        platform='minerva_janga'
    if 'minerva_th5' in platform:
        platform='minerva_th5'
    updater_info_dict = CommonLib.get_swinfo_dict("SDK")
    ver1= updater_info_dict.get(platform).get(name,"")
    print('The ver is ',ver1)
    return ver1
    
    
    
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
    if "minerva_janga" in devicename.lower():
        port_group_cmd=port_group_cmd+" "+port_enable_tag
    load_into_bcm_prompt(device, port_group_cmd)
    device= Device.getDeviceObject(device)
    device.sendCmd('\n')
    time.sleep(5)
    if "minipack3" in devicename.lower() or "minerva_th5" in devicename.lower():
        #CommonLib.run_command(port_enable_cmd,deviceObj=device, prompt=BCM_prompt)
        c1=CommonLib.run_command(portdump_status_cmd,deviceObj=device, prompt=BCM_prompt)
        if not check_port_status_output(c1, "passed"):
            flag=True
            log.fail("Port status check failed")
        
    device.sendCmd(exit_BCM_Prompt)
    if flag:
        raise RuntimeError("'load and initialization test' failed")
    log.success("'load and initialization test' passed successfully for "+port_group +" port group")

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
    
def check_version_sdk(device):
    """
    Check the SDK and PCIe version on the given device.

    Args:
        device (str): The device name.

    Returns:
        None
    """
    
    flag= False
    SDK_SHELL_cmd=SDK_SHELL
    if "minipack3" in devicename.lower() or "minerva_th5" in devicename.lower():
        SDK_SHELL_cmd='./'+SDK_SHELL
    load_into_bcm_prompt(device,SDK_SHELL_cmd)
    device= Device.getDeviceObject(device)
    time.sleep(5)
    
    
    if "minipack3" in devicename.lower() or "minerva_th5" in devicename.lower():
        PCIe_version = get_new_sdk_version('SDK','PCIe_FW',devicename.lower())
        BCM_version = get_new_sdk_version('SDK','bcm_version',devicename.lower())
        c1=CommonLib.run_command('version',deviceObj=device, prompt=BCM_prompt)
        try:
            CommonKeywords.should_match_a_regexp(c1,BCM_VERSION_MiniPack3+BCM_version)
            log.info('SDK Version matched') 
        except:
            flag=True
            log.fail("SDK Version mismatched")
        time.sleep(2)
        CommonLib.run_command('dsh', deviceObj=device,prompt='sdklt.0>')
        c2=CommonLib.run_command('pciephy fwinfo',deviceObj=device,prompt='sdklt.0>')
        try:
            CommonKeywords.should_match_a_regexp(c2,PCIe_version_regex+PCIe_version)
            log.info('PCIe Version matched') 
        except:
            flag=True
            log.fail("PCIe Version mismatched")
        
    if "minerva_janga" in devicename.lower():
        broadcom_sdk_version = get_new_sdk_version('SDK','broadcom_SDK_version','minerva_janga')
        cls_sdk_version = get_new_sdk_version('SDK','cls_sdk_version','minerva_janga')
        PCIe_version = get_new_sdk_version('SDK','PCIe_FW',devicename.lower())
        c1=CommonLib.run_command(BCM_SDK_version_cmd,deviceObj=device,prompt=BCM_prompt)
        if not ((broadcom_sdk_version in c1) and (cls_sdk_version in c1) and (show_version_test_passed_regex in c1)):
            flag=True
            log.fail('SDK version not matching')
        else:
            log.info('SDK version matched successfully')
        time.sleep(2)
        c2=CommonLib.run_command(PCIe_version_cmd,deviceObj=device,prompt=BCM_prompt)
        if (PCIe_version_check+PCIe_version) in c2:
            log.info('PCIe Version matched') 
        else:
            flag=True
            log.fail("PCIe Version mismatched")
            
    device.sendCmd(exit_BCM_Prompt)
    if flag:
        raise RuntimeError("'SDK Version Test' failed")
    log.success('SDK version test passed')
        
    

def test_port_default_info(device, port_group_cmd):
    """
    Test the port default information.

    Args:
        device (str): The device name.
        port_group_cmd (str): The port group command.

    Raises:
        RuntimeError: If the 'load and initialization test' fails.

    Returns:
        None
    """
    if "minerva_janga" in devicename.lower():
        port_group_cmd= port_group_cmd+' '+port_enable_tag
    load_into_bcm_prompt(device,port_group_cmd)
    device= Device.getDeviceObject(device)
    flag= False
    time.sleep(5)
    if "minipack3" in devicename.lower() or  "minerva_th5" in devicename.lower():
        c1=CommonLib.run_command(portdump_status_cmd,deviceObj=device,prompt=BCM_prompt)
        if not check_port_details_output(c1, port_group_cmd, "passed"):
            flag=True
            log.fail("Portdump status all is showing 'FAILED' as overall status")
        
        
    if "minerva_janga" in devicename.lower():
        c1=CommonLib.run_command(portdump_status_cmd,deviceObj=device,prompt=BCM_prompt)
        if not check_detailed_port_dump_output(c1, port_group_cmd):
            flag=True
            log.fail("Portdump output is not correct")
            
    device.sendCmd(exit_BCM_Prompt)
    if flag:
        raise RuntimeError("'Default_Port_Info_Test test' failed")
    log.success("'Default_Port_Info_Test test' passed successfully for "+port_group_cmd.split()[-2] +" port group")
 
        
        
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
    if "minerva_janga" in devicename.lower():
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
    if "minerva_janga" in devicename.lower():
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
        
        
def check_dump_ports_status(output, result):
    output_lst = output.splitlines()
    for item in output_lst:
        if re.search(port_name_regex, item):
            if not (result in item):
                log.fail(item+" not matching the expected port status")
                return False
    log.info("port status is as Expected (" +result +")")
    return True
            
        
    
    
    
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
            except Exception as error:
                log.info(str(error))
                log.fail(item)
                return False
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
    c1 = CommonLib.run_command(port_group_cmd ,deviceObj=device, prompt=BCM_prompt,timeout=150)
    log.success('successfully loaded into BCM.0> Prompt')


def check_port_PRBS_BER(device, port_group_cmd):
    """
    Check the Port PSBR/BER test for a specific port group.

    Args:
        device (str): The device name.
        port_group_cmd (str): The command for the port group.

    Raises:
        RuntimeError: If the 'Port PSBR/BER test' fails.

    Returns:
        None
    """
    flag= False
    if "minipack3" in devicename.lower() or  "minerva_th5" in devicename.lower():
        load_into_bcm_prompt(device,port_group_cmd)
        device= Device.getDeviceObject(device)
        c1=CommonLib.run_command(bertest_cmd,deviceObj=device,prompt=BCM_prompt, timeout=500)
        if not check_bertest_output(c1):
            flag=True
            log.fail("Bertest check failed")
        
    if "minerva_janga" in devicename.lower():
        device= Device.getDeviceObject(device)
        c1=CommonLib.run_command(port_group_cmd+bertest_cmd+" "+port_enable_tag,deviceObj=device,prompt=BCM_prompt, timeout=800)
        if not ((PSBR_passed_pattern in c1) and check_bertest_output(c1)):
            flag=True
            log.fail("PSBR/BER test failed")
        
        else:
            log.info('PSBR/BER test passed successfully')
    
    if flag:
        raise RuntimeError("'Port PSBR/BER test' failed")
    log.success("'Port PSBR/BER test' passed successfully for "+port_group_cmd.split()[-1] +" port group")


    
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
    if "minipack3" in devicename.lower()  or  "minerva_th5" in devicename.lower():
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
                
                
    if "minerva_janga" in devicename.lower():
        device= Device.getDeviceObject(device)
        c1=CommonLib.run_command(port_group_cmd+L2_cpu_traffic_cmd+" "+port_enable_tag,deviceObj=device,prompt=BCM_prompt, timeout=400)
        if not ((L2_cpu_traffic_passed_pattern in c1) and (check_CPU_L2_traffic_test_output(c1))):
            flag=True
            log.fail("Counters Consistency Check Failed (l2_cpu_traffic test failed)")
        
        else:
            log.info('Counters Consistency Check passed (l2_cpu_traffic passed successfully)')
        
    if flag:
        raise RuntimeError("'L2 CPU Traffic test' failed")
    log.success("'L2 CPU Traffic test' passed successfully for "+port_group_cmd.split()[-1] +" port group")

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
        
    
def check_remote_shell(device):
    """
    Checks the remote shell on the specified device.

    Args:
        device: The device object representing the remote device.

    Raises:
        RuntimeError: If the './cls_shell ps d3c check' fails.

    """
    device= Device.getDeviceObject(device)
    CommonLib.run_command('./'+SDK_SHELL+' -d', deviceObj=device, prompt=sdk_prompt)
    flag= False
    
    time.sleep(5)
    device.sendCmd('\n')
    
    device.sendCmd(cls_shell_d3c)
    time.sleep(10)
    device.sendCmd('\n')
    try:
        c1=device.read_until_regexp(cls_shell_d3c_output_regex, timeout=50)
        
        if not check_cls_shell_d3c_output(c1):
            flag=True
            log.fail("./cls_shell ps d3c check failed")
    except:
        flag=True
        log.fail("./cls_shell ps d3c check failed")
        
    
    device.sendCmd(cls_shell_exit)
    try:
        device.read_until_regexp(cls_shell_exit_output_regex, timeout=50)
    except:
        flag=True
        log.fail("./cls_shell exit check failed")
        
    
    device.sendCmd('cd')
    if flag:
        log.fail("Remote shell test failed")
        raise RuntimeError("'./cls_shell ps d3c check' failed")
    
    

def check_serdes_fw(device, port_group_cmd):
    """
    Check the serdes firmware version on the specified device.

    Args:
        device (str): The device name.
        port_group_cmd (str): The command to load the port group.

    Raises:
        RuntimeError: If the lane serdes version check fails.
    """
    
    
    if "minerva_janga" in devicename.lower():
        port_group_cmd=port_group_cmd+" "+port_enable_tag
    load_into_bcm_prompt(device,port_group_cmd)
    device= Device.getDeviceObject(device)
    flag= False
    time.sleep(5)
    device.sendCmd('\n')
    prompt = BCM_prompt
    if "minipack3" in devicename.lower() or "minerva_th5" in devicename.lower():
        if "minipack3" in devicename.lower():
            prompt='sdklt.0>'
            CommonLib.run_command('dsh', deviceObj=device, prompt='sdklt.0>')
        c1=CommonLib.run_command(lane_serdes_version_cmd ,deviceObj=device,prompt=prompt, timeout=5000)
        if not lane_serdes_version_check(c1):
            flag=True
            log.fail("lane serdes version check failed")
            raise RuntimeError("'lane serdes version check' failed")
        if "minipack3" in devicename.lower():
            device.sendCmd(exit_BCM_Prompt)
    if "minerva_janga" in devicename.lower():
        port_group=port_group_cmd.split()[-2]
        port_group_lst=port_group.split('x')
        
                
        for i in range(1, int(port_group_lst[0]) * int(port_group_lst[1])+1):
            c1=CommonLib.run_command(lane_serdes_version_cmd.format(str(0),str(i)) ,deviceObj=device,prompt=BCM_prompt, timeout=5000)
            if not lane_serdes_version_check(c1):
                flag=True
                log.fail("lane serdes version check failed")
                raise RuntimeError("'lane serdes version check' failed")
        for i in range(1, int(port_group_lst[0]) * int(port_group_lst[1])+1):
            c1=CommonLib.run_command(lane_serdes_version_cmd.format(str(1), str(i)) ,deviceObj=device,prompt=BCM_prompt, timeout=5000)
            if not lane_serdes_version_check(c1):
                flag=True
                log.fail("lane serdes version check failed")
                raise RuntimeError("'lane serdes version check' failed")
                
        
    device.sendCmd(exit_BCM_Prompt)
        
        
    
def check_cls_shell_d3c_output(output):
    """
    Function to check the output of cls_shell_d3c command.

    Args:
        output (str): The output of cls_shell_d3c command.

    Returns:
        bool: True if the output matches the expected pattern, False otherwise.
    """
    output_lst = output.splitlines()
    port_count = 0
    for item in output_lst:
        if re.search(cls_shell_d3c_check[0], item):
            try:
                regex= '[\s+\S+]+'.join(cls_shell_d3c_check)
                CommonKeywords.should_match_a_regexp(item,regex)
                port_count = port_count+1
            except:
                log.fail(item)
                return False
    log.info(str(port_count))
    if port_count!=64:
        log.fail('Port count is not equal to 64')
        return False
    log.success("cls_shell_d3c output is correct")
    return True


def lane_serdes_version_check(output):
    """
    Checks the version of the lane serdes and common ucode in the given output.

    Args:
        output (str): The output containing the lane serdes and common ucode version information.

    Returns:
        bool: True if the lane serdes and common ucode versions match the expected patterns, False otherwise.
    """
    output_lst = output.split('**** SERDES DISPLAY DIAG DATA END ****')
    serdes_api_version = get_new_sdk_version('SDK','serdes_api_version',devicename.lower())
    ucode_version = get_new_sdk_version('SDK','ucode_version',devicename.lower())
    for item in output_lst:
        if (item!='\n') and ('sdklt.0>' not in item) and ('>>>' not in item) and (item.strip()!='BCM.0>'):
            if not ((serdes_api_version_regex+serdes_api_version in item) and (ucode_version_regex+ucode_version in item)):
    
                log.fail("Serdes api version or Common Ucode version are not matching")
                log.info(item)
                return False
    
    log.info("Serdes api version or Common Ucode version are matching")
    return True

def check_bertest_output(output):
    """
    Check if the output of bertest is within the threshold value.

    Args:
        output (str): The output of bertest.

    Returns:
        bool: True if the output is within the threshold value, False otherwise.
    """
    output_lst = output.splitlines()
    for item in output_lst:
        item_match = re.match(bertest_regex, item)
        
        if item_match:
            log.info(item)
            
            if "minerva_janga" in devicename.lower() and item_match.group(1)=='0.0':
                log.info("no packet loss for {}".format(item))
                continue
            threshold_value = "{:.25f}".format(float(bertest_threshold_value))
            current_value = "{:.25f}".format(float(item_match.group(1)))
            if not (current_value<threshold_value):
                log.fail("bertest output is exceeding threshold")
                log.info(item)
                return False
    return True
    
    
def check_temperature_sensors(device, port_group_cmd):
    if "minerva_janga" in devicename.lower():
        port_group_cmd=port_group_cmd+" "+port_enable_tag
    load_into_bcm_prompt(device,port_group_cmd)
    device= Device.getDeviceObject(device)
    
    flag= False
    
    time.sleep(5)
    device.sendCmd('\n')
    
    if "minipack3" in devicename.lower() or "minerva_th5" in devicename.lower():
        CommonLib.run_command('dsh', deviceObj=device,prompt='sdklt.0>')
        c1=CommonLib.run_command(get_hmon_temperature_cmd ,deviceObj=device, prompt='sdklt.0>', timeout=500)
        temp_sensor_list_before_traffic=getSensorTemperatureList(c1)
        CommonLib.run_command(exit_BCM_Prompt, deviceObj=device, prompt=BCM_prompt)
        
        if "minipack3" in devicename.lower():
            device.sendCmd(traffic_test_cmd+ ' 300')
            device.read_until_regexp(traffic_test_end_regex, timeout=500)
            time.sleep(10)
        if "minerva_th5" in devicename.lower():
            c1 =CommonLib.run_command(temperature_test_cmd ,deviceObj=device, prompt=BCM_prompt, timeout=100)
            c2=CommonLib.run_command(traffic_temp_traffic_cmd_1 ,deviceObj=device, prompt=BCM_prompt, timeout=100)
            c3=CommonLib.run_command(traffic_temp_traffic_cmd_2 ,deviceObj=device, prompt=BCM_prompt, timeout=100)
            c4=CommonLib.run_command(show_c_rate_cmd ,deviceObj=device, prompt=BCM_prompt, timeout=100)
            time.sleep(10)
        
        CommonLib.run_command('dsh', deviceObj=device, prompt='sdklt.0>')
        c1=CommonLib.run_command(get_hmon_temperature_cmd ,deviceObj=device, prompt='sdklt.0>', timeout=500)
        temp_sensor_list_after_traffic=getSensorTemperatureList(c1)
        if not compare_temperature_sensor(temp_sensor_list_before_traffic,temp_sensor_list_after_traffic):
            flag=True
            log.fail("Sensors temperature are not higher than normal")
        
    if "minerva_janga" in devicename.lower():
        c1=CommonLib.run_command(show_temperature_cmd ,deviceObj=device, prompt=BCM_prompt, timeout=60)
        temp_sensor_list_before_traffic=getSensorTemperatureList(c1)
        c2=CommonLib.run_command(snake_config_cmd ,deviceObj=device, prompt=BCM_prompt, timeout=60)
        c3=CommonLib.run_command(snake_test_start_cmd ,deviceObj=device, prompt=BCM_prompt, timeout=60)
        c4=CommonLib.run_command(show_temperature_cmd ,deviceObj=device, prompt=BCM_prompt, timeout=60)
        temp_sensor_list_after_traffic=getSensorTemperatureList(c4)
        c5=CommonLib.run_command(snake_test_stop_cmd ,deviceObj=device, prompt=BCM_prompt, timeout=60)
        if not compare_temperature_sensor(temp_sensor_list_before_traffic,temp_sensor_list_after_traffic):
            flag=True
            log.fail("Sensors temperature are not higher than normal")
        
    device.sendCmd(exit_BCM_Prompt)
    if flag:
        raise RuntimeError("'Temperature sensor test' failed")
    log.success("'Temperature sensor test' passed successfully")

def getSensorTemperatureList(output):
    sensor_list = output.splitlines()
    sensor_dict={}
    for item in sensor_list:
        if "minerva_janga" in devicename.lower():
            x= re.search('\|\s+(\d+)\s+\|\s+\S+\s+\|\s+(\d+\.\d+)\s+\|\s+\d+\.\d+\s+\|', item)
            if x:
                if not (x.group(1) in sensor_dict.keys()):
                    sensor_dict[x.group(1)]=[]
                sensor_dict[x.group(1)].append(x.group(2))
        else:
            x= re.search('(\d+)\s+(\d+\.\d+)\s+\d+\.\d+\s+\d+\.\d+\s+\S+', item)
            if x:
                sensor_dict[x.group(1)]=x.group(2)
    if len(sensor_dict)==0:
        log.fail("No sensor present")
        raise RuntimeError("'No sensor present'")
    log.info(str(sensor_dict))
    return sensor_dict
            
def compare_temperature_sensor(output1, output2):
    for i in output1.keys():
        if "minerva_janga" in devicename.lower():
            if not (float(output1[i][0])<float(output2[i][0]) and float(output1[i][1])<float(output2[i][1])):
                log.fail(i+" sensor temperature "+ output2[i]+" is higher than normal "+ output1[i])
                return False
        else:
            if not float(output1[i])<float(output2[i]):
                log.fail(i+" sensor temperature "+ output2[i]+" is higher than normal "+ output1[i])
                return False
    log.info("Temperature is higher than normal as expected")
    return True
       
            
     

def port_loopback_test(device, port_fec_type=''):
    device= Device.getDeviceObject(device)
    time.sleep(10)
    flag=False
    if "minerva_janga" in devicename.lower():
        c1=CommonLib.run_command(SDK_SHELL+" "+port_loopback_test_tag+" "+port_enable_tag, deviceObj=device, prompt=BCM_prompt, timeout=500)
        if not check_port_loopback_command_output(c1, port_fec_type):
            flag=True
            log.fail("Port loopback test failed")
        device.sendCmd(exit_BCM_Prompt)
        
        
    if "minipack3" in devicename.lower():
        CommonLib.run_command(port_d3c_lb_cmd+port_fec_type, deviceObj=device, prompt=BCM_prompt)
        time.sleep(30)
        c1 = CommonLib.run_command('ps d3c', deviceObj=device, prompt=BCM_prompt)
        
        
        if not check_cls_shell_d3c_output(c1):
            flag=True
            log.fail("ps d3c check failed")
            
        device.sendCmd(clear_c_command)
        device.sendCmd(show_c_cmd)
        
        device.sendCmd(traffic_test_cmd+ ' 60')
        
        device.read_until_regexp(traffic_test_end_regex, timeout=500)
    
        time.sleep(20)
        
        device.sendCmd(show_c_cmd)
        c2=CommonLib.run_command(portdump_counters_all_cmd, deviceObj=device, prompt=BCM_prompt)
        if port_fec_type=='EBD':
            if not check_port_status_output(c2, "failed"):
                flag = True
                log.fail("portdump counters all output is showing PASSED as overall status")
            else:
                log.info("portdump counters all output is showing FAILED as overall status")
        else:
            if not check_port_status_output(c2, "passed"):
                flag = True
                log.fail("portdump counters all output is showing FAILED as overall status")
            else:
                log.info("portdump counters all output is showing PASSED as overall status")

    if flag:
        raise RuntimeError("'Port loopback test' failed")
    log.success("'Port loopback test' passed successfully for "+port_fec_type)
    

################################################ MINERVA J3 ############################################


    
    
def check_manufacturing_test(device, port_group_cmd):
    port_group_cmd=port_group_cmd+" "+port_enable_tag+" "+manufacturing_test_command
    log.info(port_group_cmd)
    device= Device.getDeviceObject(device)
    flag= False
    device.sendCmd('\n')
    device.sendCmd(port_group_cmd)
    time.sleep(100)
    c1 = device.read_until_regexp('>>>', timeout=600)
    for item in manufacturing_test_pattern_lst:
        if not (item in c1):
            flag=True
            log.fail(item+" check FAILED") 
    if flag:
        log.fail("manufacturing test failed")
        raise RuntimeError("'Manufacturing test' failed")
    log.success("'manufacturing test' Passed Successfully")

def check_detailed_port_dump_output(output, port_group_cmd):
    log.info(port_group_cmd)
    port_group= port_group_cmd.split()[-2]
    port_count= 2* int(port_group.split('x')[0]) * int(port_group.split('x')[1])
    total_port_count = port_count
    port_speed= port_group.split('x')[2]
    port_detail_passed_pattern.insert(2,port_speed)
    print(str(port_detail_passed_pattern))
    port_details_pattern = '([\s+\S+]+)'.join(port_detail_passed_pattern)
    log.info(str(port_details_pattern))
    del port_detail_passed_pattern[2]
    output_lst = output.splitlines()
    for item in output_lst:
        if re.search(port_detail_passed_pattern[0], item):
            if re.search(port_details_pattern, item):
                port_count= port_count-1 
            elif re.search(mgmt_port_regex, item):
                log.info(str(total_port_count//2+1))
                if 'eth'+str(total_port_count//2+1) in item:
                    log.info(item+" -> management port")
                else:
                    log.fail(item)
                    return False
            else:
                log.fail(item)
                return False
    if port_count!=0:
        log.fail("Total number of ports are not equal to {}".format(total_port_count/2))
        return False
    log.info("All ports are up, autoneg is set to No and port count is equal to {}".format(total_port_count/2))
    return True
    
def check_port_loopback_command_output(output, port_fec_type):
    output_lst = output.splitlines()
    port_fec_type=port_fec_type.upper()
    check=False
    for item in output_lst:
        if 'port_loopback_set' in item:
            check=True
        if check:
            if re.search(port_detail_passed_pattern[0], item):
                if port_fec_type in item:
                    continue
                elif re.search(mgmt_port_regex, item):
                    if 'MAC' in item:
                        log.info(item+" -> management port")
                        continue
                    else:
                        log.fail(item)
                        return False
                        
                else:
                    log.fail(item)
                    return False
    if port_loopback_test_pass_regex in output:
        log.info("port loopback test passed")
        return True
    log.fail("Port loopback test Failed")
    return False
    
    
def check_CPU_L2_traffic_test_output(output):
    output_lst = output.splitlines()
    total_tx_rx_packets_check='Ingress Mirror Destroy success'
    check=False
    total_tx_rx_packets_list=[]
    for item in output_lst:
        if total_tx_rx_packets_check in item:
            check=True
        if re.search(L2_traffic_test_item_check_regex, item):
            item_lst= item.split('|')
            item_lst =list(filter(lambda x: x != '', item_lst))
            if item_lst[2].strip()!=item_lst[4].strip():
                log.fail("rx_packets and rx_good_packets are not equal for {}".format(item))
                return False
            if check:
                total_tx_rx_packets_list=item_lst
                
        
    check_mib_counters = re.search(l2_traffic_total_tx_rx_packets_regex, output)
    log.info("rx_packets and rx_good_packets are equal")
    if check_mib_counters:
        if check_mib_counters.group(1)==check_mib_counters.group(3) and check_mib_counters.group(2)==check_mib_counters.group(4):
            log.info("rx_gold_frames and  tx_gold_frames,  rx_gold_bytes and tx_gold_bytes are equal")
            return True
        else:
            log.fail("rx_gold_frames and  tx_gold_frames,  rx_gold_bytes and tx_gold_bytes are not equal")
            return False
    if check:
        log.info(total_tx_rx_packets_list[2].strip())
        log.info(total_tx_rx_packets_list[4].strip())
        log.info(total_tx_rx_packets_list[8].strip())
        log.info(total_tx_rx_packets_list[10].strip())
        if total_tx_rx_packets_list[2].strip()==total_tx_rx_packets_list[4].strip() and total_tx_rx_packets_list[8].strip()==total_tx_rx_packets_list[10].strip():
            log.info("total rx_packets and rx_good_packets,  tx_packets and tx_good_packets are equal")
            return True
        else:
            log.fail("total rx_packets and rx_good_packets,  tx_packets and tx_good_packets are not equal")
            return False
        
    return True
            

    
def check_preemphasis_config_file(device, port_group):

    load_into_bcm_prompt(device,port_group_cmd)
    device= Device.getDeviceObject(device)
    flag= False
    time.sleep(5)
   
    c1=CommonLib.run_command(lane_serdes_version_cmd,deviceObj=device,prompt=BCM_prompt, timeout=5000)
            
    device.sendCmd(exit_BCM_Prompt)
    if flag:
        raise RuntimeError("'Preemphasis config  test' failed")
    log.success("'Preemphasis config test' passed successfully for "+port_group_cmd.split()[-1] +" port group")

        
    
    
