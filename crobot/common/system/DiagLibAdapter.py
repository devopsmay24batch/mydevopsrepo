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
from InitFrameworkLib import *
import Const
from Utils import NumPlus
import sys
from Decorator import *
sys.path.append("..")
from sdk import *
import Logger as log
import traceback
from robot.libraries.BuiltIn import BuiltIn
from datetime import datetime
device = DeviceMgr.getDevice()
from Diag_OS_variable import *

curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curDir, '../commonlib'))
sys.path.append(os.path.join(curDir, '../../crobot'))
sys.path.append(os.path.join(curDir, '../../crobot/legacy'))

###################################################################################
# Common Wrapper Library Functions
###################################################################################
def critical_step(StepNumber, name):
    log.debug('Entering procedure critical_step[%s]\n '%(str(locals())))
    return BuiltIn().run_keyword(name)

def step(StepNumber, name, *args):
    """ when use this api/keyword , if one step fail, the following steps will not be executed """

    log.debug('Entering procedure step[%s]\n '%(str(locals())))
    return BuiltIn().run_keyword(name, *args)

def ssh_login_bmc():
    dLibObj = getDiagLibObj()
    dLibObj.ssh_login_bmc()


def ssh_disconnect():
    dLibObj = getDiagLibObj()
    dLibObj.ssh_disconnect()


def set_verbose_level():
    dLibObj = getDiagLibObj()

    var_verbose_level=0

    return dLibObj.set_verbose_level(var_verbose_level)


def enable_terminal_log_file():
    dLibObj = getDiagLibObj()

    enable_flag = '1'

    dLibObj.check_system_log_dir_exists()
    return dLibObj.wpl_enable_terminal_log_file(enable_flag)


def Log_Debug(msg):
    dLibObj = getDiagLibObj()
    dLibObj.wpl_log_debug(msg)


def Log_Info(msg):
    dLibObj = getDiagLibObj()
    dLibObj.wpl_log_info(msg)


def Log_Success(msg):
    dLibObj = getDiagLibObj()
    dLibObj.wpl_log_success(msg)


def Log_Fail(msg):
    dLibObj = getDiagLibObj()
    dLibObj.wpl_log_fail(msg)


def switch_to_centos():
    return CommonLib.switch_to_centos()


def switch_to_openbmc():
    return CommonLib.switch_to_openbmc()

def reboot_to_bmc():
    return CommonLib.reboot("openbmc")


def get_common_system_sdk_path():
    Log_Debug("Entering procedure get_common_system_sdk_path.\n")

    cur_sdk_path = SYSTEM_SDK_PATH
    return cur_sdk_path


def check_all_bmc_test_directories_and_fw_version():
    Log_Debug("Entering procedure check_all_bmc_test_directories.\n")
    dLibObj = getDiagLibObj()
    return dLibObj.check_test_directories()

def startup_default_port_group(use_xphyback=True, init_cmd=xphy_init_mode2):
    Log_Debug("Entering procedure startup_default_port_group.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.startup_default_port(use_xphyback=use_xphyback, init_cmd=init_cmd)

def search_for_preferred_ipaddr(var_centos_ipAddr_list,  var_openbmc_ipAddr_list, preferred_network):
    Log_Debug("Entering procedure search_for_preferred_ipaddr.\n")
    dLibObj = getDiagLibObj()

    ipList = []

    var_centos_ipAddr = ''
    found_centos_ipAddr = False
    for centos_ipAddr in var_centos_ipAddr_list:
        match = re.search(preferred_network, centos_ipAddr)
        if match:
            found_centos_ipAddr = True
            var_centos_ipAddr = centos_ipAddr
            break

    var_openbmc_ipAddr = ''
    found_openbmc_ipAddr = False
    for openbmc_ipAddr in var_openbmc_ipAddr_list:
        match = re.search(preferred_network, openbmc_ipAddr)
        if match:
            found_openbmc_ipAddr = True
            var_openbmc_ipAddr = openbmc_ipAddr
            break

    if (found_centos_ipAddr == True) and (found_openbmc_ipAddr == True):
        ipList.append(var_centos_ipAddr)
        ipList.append(var_openbmc_ipAddr)
        return ipList
    else:
        return


def get_dut_ipv6_addresses(interface_type, var_scp_ipv6, var_scp_static_ipv6, preferred_jenkins_network=True):
    Log_Debug("Entering procedure get_dut_ipv6_addresses.\n")
    dLibObj = getDiagLibObj()

    IP_ADDR = []

    switch_to_centos()

    if preferred_jenkins_network == False:
        preferred_network = 'None'
    else:
        # Some machines have multiple IPV6 addresses from different network
        # IPV6 from server, dut centos and dut openbmc must be from the same network in order to ping each other.
        var_server_ip = var_scp_ipv6
        if re.search(':', var_server_ip):
            slist = var_server_ip.split(':')
            preferred_network = slist[0]
        else:
            dLibObj.wpl_raiseException('Error: Unable to get server IPV6 address.')

    # get IPV6 address in centos
    var_centos_ipAddr = check_centos_ip_address_list(interface_type, preferred_network, True)
    if var_centos_ipAddr is None:
        dLibObj.wpl_raiseException('Error: Unable to get IPV6 address in centos.')

    switch_to_openbmc()

    # get IPV6 address in openbmc from same network
    var_openbmc_ipAddr = check_openbmc_ip_address_list(interface_type, preferred_network, True)
    if var_openbmc_ipAddr is None:
        dLibObj.wpl_raiseException('Error: Unable to get IPV6 address in openbmc.')

    ##### no need to set static ip here, because it was set in check_centos_ip_address_list and check_openbmc_ip_address_list
    ##### which call CommonLib.check_ip_address_list()
    # IP_ADDR = search_for_preferred_ipaddr(var_centos_ipAddr_list, var_openbmc_ipAddr_list, preferred_network)
    # if IP_ADDR is None:
    #     var_static_ip = var_scp_static_ipv6
    #     if re.search(':', var_static_ip):
    #         slist = var_static_ip.split(':')
    #         preferred_static_network = slist[0]
    #         IP_ADDR = search_for_preferred_ipaddr(var_centos_ipAddr_list, var_openbmc_ipAddr_list, preferred_static_network)
    #         if IP_ADDR is None:
    #             dLibObj.wpl_raiseException('Error: Unable to get static IPV6 addresses from DUT.')
    #     else:
    #         dLibObj.wpl_raiseException('Error: Unable to get server static IPV6 address.')

    if interface_type == 'usb':
        var_interface = openbmc_eth_params['usb_interface']
    else:
        var_interface = openbmc_eth_params['interface']

    # var_centos_ipAddr = IP_ADDR[0]
    # var_openbmc_ipAddr = IP_ADDR[1]
    IP_ADDR.append(var_centos_ipAddr)
    IP_ADDR.append(var_openbmc_ipAddr)

    Log_Info("Using DUT centos IPV6 address: [%s]" %var_centos_ipAddr)
    Log_Info("Using DUT openbmc IPV6 address: [%s]" %var_openbmc_ipAddr)

    Log_Info("Ping centos ethernet interface from openbmc...")
    ping_ipv6_address(var_interface, var_centos_ipAddr, 'openbmc')

    return IP_ADDR


def check_centos_ip_address(interface_type='eth'):
    Log_Debug("Entering procedure check_centos_ip_address.\n")
    dLibObj = getDiagLibObj()

    if interface_type == 'eth':
        var_interface = centos_eth_params['interface']
    else:
        var_interface = centos_eth_params['usb_interface']

    var_mode='centos'

    return CommonLib.check_ip_address(Const.DUT, var_interface, var_mode)


def check_centos_ip_address_list(interface_type='eth', preferred_network='None', ipv6=True):
    Log_Debug("Entering procedure check_centos_ip_address_list.\n")
    dLibObj = getDiagLibObj()

    if interface_type == 'eth':
        var_interface = centos_eth_params['interface']
    else:
        var_interface = centos_eth_params['usb_interface']

    var_mode='centos'

    return CommonLib.check_ip_address_list(Const.DUT, var_interface, var_mode, preferred_network, ipv6)


def ping_ip_address(ip, mode):
    Log_Debug("Entering procedure ping_ip_address.\n")
    dLibObj = getDiagLibObj()

    var_ipAddr = ip
    var_mode = mode
    var_count = 10

    return CommonLib.exec_ping(Const.DUT, var_ipAddr, var_count, var_mode)


def ping_ipv6_address(interface, ipv6, mode):
    Log_Debug("Entering procedure ping_ipv6_address.\n")
    dLibObj = getDiagLibObj()

    var_interface = interface
    var_ipAddr = ipv6
    var_mode = mode
    var_count = 10

    return CommonLib.exec_ping6(Const.DUT, var_interface, var_ipAddr, var_count, var_mode)


def check_openbmc_ip_address(interface_type='eth'):
    Log_Debug("Entering procedure check_openbmc_ip_address.\n")
    dLibObj = getDiagLibObj()

    if interface_type == 'eth':
        var_interface = openbmc_eth_params['interface']
    else:
        var_interface = openbmc_eth_params['usb_interface']

    var_mode='openbmc'

    return CommonLib.check_ip_address(Const.DUT, var_interface, var_mode)


def check_openbmc_ip_address_list(interface_type='eth', preferred_network='None', ipv6=True):
    Log_Debug("Entering procedure check_openbmc_ip_address_list.\n")
    dLibObj = getDiagLibObj()

    if interface_type == 'eth':
        var_interface = openbmc_eth_params['interface']
    else:
        var_interface = openbmc_eth_params['usb_interface']

    var_mode='openbmc'

    return CommonLib.check_ip_address_list(Const.DUT, var_interface, var_mode, preferred_network, ipv6)


def get_server_dhcp_or_static_ip(dhcp_ipv6, static_ipv6):
    Log_Debug("Entering procedure get_server_dhcp_or_static_ip.\n")
    dLibObj = getDiagLibObj()

    # make sure dhcp or static ipv6 available
    ipList = get_dut_ipv6_addresses('eth', dhcp_ipv6, static_ipv6)
    if ipList is None:
        dLibObj.wpl_raiseException('Error: Unable to get DUT IPV6 addresses.')

    if re.search(':', dhcp_ipv6):
        slist = dhcp_ipv6.split(':')
        preferred_network = slist[0]
    else:
        dLibObj.wpl_raiseException('Error: Unable to get server dhcp IPV6 address.')

    var_centos_ip = ipList[0]
    centos_slist = var_centos_ip.split(':')
    centos_network = centos_slist[0]

    var_openbmc_ip = ipList[1]
    openbmc_slist = var_openbmc_ip.split(':')
    openbmc_network = openbmc_slist[0]

    if (centos_network == preferred_network) and (openbmc_network == preferred_network):
        Log_Info('Using server dhcp IPV6 address: [%s]' %dhcp_ipv6)
        var_server_ip = dhcp_ipv6
    else:
        if re.search(':', static_ipv6):
            Log_Info('Using server static IPV6 address: [%s]' %static_ipv6)
            var_server_ip = static_ipv6
        else:
            dLibObj.wpl_raiseException('Error: Unable to get server static IPV6 address.')

    return var_server_ip


def copy_bmc_files():
    Log_Debug("Entering procedure copy_bmc_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = get_server_dhcp_or_static_ip(scp_ipv6, scp_static_ipv6)
    var_filelist = get_image_list('BMC')
    var_filepath = get_host_image_path('BMC')
    var_destination_path = get_local_image_path('BMC')
    var_mode = openbmc_mode
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def copy_bios_files():
    Log_Debug("Entering procedure copy_bios_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = get_server_dhcp_or_static_ip(scp_ipv6, scp_static_ipv6)
    var_filelist = get_image_list('BIOS')
    var_filepath = get_host_image_path('BIOS')
    var_destination_path = get_local_image_path('BIOS')
    var_mode = openbmc_mode
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def copy_th3_files():
    Log_Debug("Entering procedure copy_th3_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = get_server_dhcp_or_static_ip(scp_ipv6, scp_static_ipv6)
    var_filelist = get_image_list('TH3')
    var_filepath = get_host_image_path('TH3')
    var_destination_path = get_local_image_path('TH3')
    var_mode=openbmc_mode
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def copy_fpga_files():
    Log_Debug("Entering procedure copy_fpga_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = get_server_dhcp_or_static_ip(scp_ipv6, scp_static_ipv6)
    var_filelist = get_image_list('FPGA')
    var_filepath = get_host_image_path('FPGA')
    var_destination_path = get_local_image_path('FPGA')
    var_mode = openbmc_mode
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def copy_bic_files():
    Log_Debug("Entering procedure copy_bic_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = get_server_dhcp_or_static_ip(scp_ipv6, scp_static_ipv6)
    var_filelist = get_image_list('BIC')
    var_filepath = get_host_image_path('BIC')
    var_destination_path = get_local_image_path('BIC')
    var_mode = openbmc_mode
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def copy_all_cpld_files():
    Log_Debug("Entering procedure copy_all_cpld_files.\n")
    dLibObj = getDiagLibObj()

    copy_system_cpld_files()
    copy_fcm_files()
    copy_power_cpld_files()
    copy_scm_files()
    return True


def copy_fcm_files():
    Log_Debug("Entering procedure copy_fcm_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = get_server_dhcp_or_static_ip(scp_ipv6, scp_static_ipv6)
    var_filelist = get_sub_image_list('CPLD', 'fcm')
    var_filepath = get_host_image_path('CPLD')
    var_destination_path = get_local_image_path('CPLD')
    var_mode = openbmc_mode
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def copy_scm_files():
    Log_Debug("Entering procedure copy_scm_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = get_server_dhcp_or_static_ip(scp_ipv6, scp_static_ipv6)
    var_filelist = get_sub_image_list('CPLD', 'scm')
    var_filepath = get_host_image_path('CPLD')
    var_destination_path = get_local_image_path('CPLD')
    var_mode = openbmc_mode
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def copy_system_cpld_files():
    Log_Debug("Entering procedure copy_system_cpld_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = get_server_dhcp_or_static_ip(scp_ipv6, scp_static_ipv6)
    var_filelist = get_sub_image_list('CPLD', 'smb')
    var_filepath = get_host_image_path('CPLD')
    var_destination_path = get_local_image_path('CPLD')
    var_mode = openbmc_mode
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def copy_power_cpld_files():
    Log_Debug("Entering procedure copy_power_cpld_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = get_server_dhcp_or_static_ip(scp_ipv6, scp_static_ipv6)
    var_filelist = get_sub_image_list('CPLD', 'pwr')
    var_filepath = get_host_image_path('CPLD')
    var_destination_path = get_local_image_path('CPLD')
    var_mode = openbmc_mode
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def switch_to_centos_diag_tool():
    Log_Debug("Entering procedure switch_to_centos_diag_tool.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.switch_to_centos_and_go_to_diag_tool()


def switch_to_openbmc_check_tool():
    Log_Debug("Entering procedure switch_to_openbmc_check_tool.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.switch_to_openbmc_and_check_tool()


def verify_mac_help_dict_option_h():
    Log_Debug("Entering procedure verify_mac_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_mac_help_array
    var_toolName = cel_mac_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_mac_help_dict_option_help():
    Log_Debug("Entering procedure verify_mac_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_mac_help_array
    var_toolName = cel_mac_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_mac_help_dict_option_a():
    Log_Debug("Entering procedure verify_mac_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mac_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = mac_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_mac_help_dict_option_all():
    Log_Debug("Entering procedure verify_mac_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mac_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = mac_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_cpu_help_dict_option_h():
    Log_Debug("Entering procedure verify_cpu_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_cpu_help_array
    var_toolName = cel_cpu_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_cpu_help_dict_option_help():
    Log_Debug("Entering procedure verify_cpu_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_cpu_help_array
    var_toolName = cel_cpu_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_cpu_help_dict_option_a():
    Log_Debug("Entering procedure verify_cpu_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_cpu_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = cpu_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_cpu_help_dict_option_all():
    Log_Debug("Entering procedure verify_cpu_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_cpu_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = cpu_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_mem_help_dict_option_h():
    Log_Debug("Entering procedure verify_mem_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_mem_help_array
    var_toolName = cel_mem_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_mem_help_dict_option_help():
    Log_Debug("Entering procedure verify_mem_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_mem_help_array
    var_toolName = cel_mem_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_mem_help_dict_option_a():
    Log_Debug("Entering procedure verify_mem_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mem_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = mem_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_parse_output_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_mem_help_dict_option_all():
    Log_Debug("Entering procedure verify_mem_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mem_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = mem_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_parse_output_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_mem_help_dict_option_K():
    Log_Debug("Entering procedure verify_mem_help_dict_option_K.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mem_help_array["bin_tool"]
    var_option = "-K"
    var_keywords = 'none'
    var_pattern= mem_check_pattern
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_parse_output_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_mem_help_dict_option_check():
    Log_Debug("Entering procedure verify_mem_help_dict_option_check.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mem_help_array["bin_tool"]
    var_option = "--check"
    var_keywords = 'none'
    var_pattern = mem_check_pattern
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_parse_output_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_usb_help_dict_option_h():
    Log_Debug("Entering procedure verify_usb_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_usb_help_array
    var_toolName = cel_usb_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_usb_help_dict_option_help():
    Log_Debug("Entering procedure verify_usb_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_usb_help_array
    var_toolName = cel_usb_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_usb_help_dict_option_a():
    Log_Debug("Entering procedure verify_usb_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_usb_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = usb_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_usb_help_dict_option_all():
    Log_Debug("Entering procedure verify_usb_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_usb_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = usb_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_usb_help_dict_option_i():
    Log_Debug("Entering procedure verify_usb_help_dict_option_i.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = usb_info_array
    var_toolName = cel_usb_help_array["bin_tool"]
    var_option = "-i"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_usb_help_dict_option_info():
    Log_Debug("Entering procedure verify_usb_help_dict_option_info.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = usb_info_array
    var_toolName = cel_usb_help_array["bin_tool"]
    var_option = "--info"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_led_help_dict_option_h():
    Log_Debug("Entering procedure verify_usb_help_dict_option_info.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_led_help_array
    var_toolName = cel_led_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_led_help_dict_option_help():
    Log_Debug("Entering procedure verify_led_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_led_help_array
    var_toolName = cel_led_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_led_help_dict_option_r():
    Log_Debug("Entering procedure verify_led_help_dict_option_r.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_led_help_array["bin_tool"]
    var_option = "-r -p 0"
    var_keywords = 'none'
    var_pattern = led_read_pattern
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_led_help_dict_option_read():
    Log_Debug("Entering procedure verify_led_help_dict_option_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_led_help_array["bin_tool"]
    var_option = "--read -p 0"
    var_keywords = 'none'
    var_pattern = led_read_pattern
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_tpm_help_dict_option_h():
    Log_Debug("Entering procedure verify_tpm_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_tpm_help_array
    var_toolName = cel_tpm_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_tpm_help_dict_option_help():
    Log_Debug("Entering procedure verify_tpm_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_tpm_help_array
    var_toolName = cel_tpm_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_tpm_help_dict_option_a():
    Log_Debug("Entering procedure verify_tpm_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_tpm_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = tpm_test_keyword
    var_pattern = 'none'
    var_data = 'none'
    var_port = 'none'
    var_color = 'none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_tpm_help_dict_option_all():
    Log_Debug("Entering procedure verify_tpm_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_tpm_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = tpm_test_keyword
    var_pattern = 'none'
    var_data = 'none'
    var_port = 'none'
    var_color = 'none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_tpm_help_dict_option_l():
    Log_Debug("Entering procedure verify_tpm_help_dict_option_l.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = tpm_list_array
    var_toolName = cel_tpm_help_array["bin_tool"]
    var_option = "-l"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_tpm_help_dict_option_list():
    Log_Debug("Entering procedure verify_tpm_help_dict_option_list.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = tpm_list_array
    var_toolName = cel_tpm_help_array["bin_tool"]
    var_option = "--list"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def execute_bic_raw_get_command():
    Log_Debug("Entering procedure execute_bic_raw_get_command.\n")
    dLibObj = getDiagLibObj()

    var_toolName = ipmi_toolName
    var_netfn = CMD_APP_NETFN
    var_cmd_str = "0x1"
    var_expected_result = bic_res_ver_26
    var_test_name='None'

    return dLibObj.execute_raw_get_command(var_toolName, var_netfn, var_cmd_str, var_expected_result, var_test_name)


def verify_nvme_help_dict_option_h():
    Log_Debug("Entering procedure verify_nvme_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_nvme_help_array
    var_toolName = cel_nvme_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_nvme_help_dict_option_help():
    Log_Debug("Entering procedure verify_nvme_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_nvme_help_array
    var_toolName = cel_nvme_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_nvme_help_dict_option_a():
    Log_Debug("Entering procedure verify_nvme_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_nvme_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = nvme_test_keyword
    var_pattern = 'none'
    var_data = 'none'
    var_port = 'none'
    var_color = 'none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_nvme_help_dict_option_all():
    Log_Debug("Entering procedure verify_nvme_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_nvme_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = nvme_test_keyword
    var_pattern = 'none'
    var_data = 'none'
    var_port = 'none'
    var_color = 'none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_nvme_help_dict_option_i():
    Log_Debug("Entering procedure verify_nvme_help_dict_option_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_nvme_help_array["bin_tool"]
    var_option = "-i"
    var_keywords = 'none'
    var_pattern = nvme_info_patternList
    var_data = 'none'
    var_port = 'none'
    var_color = 'none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_nvme_help_dict_option_info():
    Log_Debug("Entering procedure verify_nvme_help_dict_option_info.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_nvme_help_array["bin_tool"]
    var_option = "--info"
    var_keywords = 'none'
    var_pattern = nvme_info_patternList
    var_data = 'none'
    var_port = 'none'
    var_color = 'none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_oob_help_dict_option_h():
    Log_Debug("Entering procedure verify_oob_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_oob_help_array
    var_toolName = cel_oob_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_oob_help_dict_option_help():
    Log_Debug("Entering procedure verify_oob_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_oob_help_array
    var_toolName = cel_oob_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def config_file_add_ip():
    Log_Debug("Entering procedure config_file_add_ip.\n")
    dLibObj = getDiagLibObj()

    var_ip = scp_ip
    var_config_file = oob_config_file

    return dLibObj.add_ip_to_config_file(var_ip, var_config_file)


def verify_oob_help_dict_option_a():
    Log_Debug("Entering procedure verify_oob_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_oob_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = oob_test_keyword
    var_pattern = 'none'
    var_data = 'none'
    var_port = 'none'
    var_color = 'none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_oob_help_dict_option_all():
    Log_Debug("Entering procedure verify_oob_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_oob_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = oob_test_keyword
    var_pattern = 'none'
    var_data = 'none'
    var_port = 'none'
    var_color = 'none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_cpld_scm():
    Log_Debug("Entering procedure verify_cpld_scm.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cpld_verify_tool
    var_module = scm_cpld
    var_set_reg = scm_set_reg
    var_get_reg = scm_get_reg_list
    var_set_val = scm_set_value

    return dLibObj.verify_scm_cpld(var_toolName, var_module, var_set_reg, var_get_reg, var_set_val)


def verify_cpld_smb():
    Log_Debug("Entering procedure verify_cpld_smb.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cpld_verify_tool
    var_module = smb_cpld
    var_set_reg = smb_set_reg
    var_get_reg = smb_get_reg_list
    var_set_val = smb_set_value

    return dLibObj.verify_smb_cpld(var_toolName, var_module, var_set_reg, var_get_reg, var_set_val)


def verify_bmc_tool_option_a():
    Log_Debug("Entering procedure verify_bmc_tool_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_initialize_bin
    var_option = "-a"

    return dLibObj.EXEC_bmc_diag_tool_command(var_toolName, var_option)


def verify_bmc_tool_option_d():
    Log_Debug("Entering procedure verify_bmc_tool_option_d.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_initialize_bin
    var_option = "-a"

    return dLibObj.EXEC_bmc_diag_tool_command(var_toolName, var_option)


def diag_switch_to_bmc_master_region():
    Log_Debug("Entering procedure diag_switch_to_bmc_master_region.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_bmc_boot_bin
    var_region = "master"

    return dLibObj.switch_and_check_bmc_by_diag_command(var_toolName, var_region)


def diag_switch_to_bmc_slave_region():
    Log_Debug("Entering procedure diag_switch_to_bmc_slave_region.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_bmc_boot_bin
    var_region = "slave"

    return dLibObj.switch_and_check_bmc_by_diag_command(var_toolName, var_region)


def flash_upgrade_bmc():
    Log_Debug("Entering procedure flash_upgrade_bmc.\n")
    dLibObj = getDiagLibObj()

    var_toolName = flashtool
    var_img_path = get_local_image_path('BMC')
    var_bmc_image = get_new_image_name('BMC')
    var_flash_device = flash_device_path

    return dLibObj.flash_bmc_image(var_toolName, var_img_path, var_bmc_image, var_flash_device)


def flash_downgrade_bmc():
    Log_Debug("Entering procedure flash_downgrade_bmc.\n")
    dLibObj = getDiagLibObj()

    var_toolName = flashtool
    var_img_path = get_local_image_path('BMC')
    var_bmc_image = get_old_image_name('BMC')
    var_flash_device = flash_device_path

    return dLibObj.flash_bmc_image(var_toolName, var_img_path, var_bmc_image, var_flash_device)


def check_bmc_downgrade_version():
    Log_Debug("Entering procedure check_bmc_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_bmc_version = get_old_image_version('BMC')

    return dLibObj.check_bmc_version(var_bmc_version)


def check_bmc_upgrade_version():
    Log_Debug("Entering procedure check_bmc_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_bmc_version = get_new_image_version('BMC')

    return dLibObj.check_bmc_version(var_bmc_version)


def switch_to_master_and_check_bios():
    Log_Debug("Entering procedure switch_to_master_and_check_bios.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_bmc_boot_bin
    var_region = "master"
    var_checkTool = boot_info_util
    var_toolOption = "bios"

    return dLibObj.switch_and_check_bios_by_diag_command(var_toolName, var_region, var_checkTool, var_toolOption)


def switch_to_slave_and_check_bios():
    Log_Debug("Entering procedure switch_to_slave_and_check_bios.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_bmc_boot_bin
    var_region = "slave"
    var_checkTool = boot_info_util
    var_toolOption = "bios"

    return dLibObj.switch_and_check_bios_by_diag_command(var_toolName, var_region, var_checkTool, var_toolOption)


def spi_util_exec_write_bios_downgrade():
    Log_Debug("Entering procedure spi_util_exec_write_bios_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spiUtil_tool
    var_opt = "write"
    var_spiNum = "spi1"
    var_dev = "BIOS"
    var_check_pattern = spiUtil_write_pattern
    var_imageFile = get_old_image_name('BIOS')
    var_readFile = 'none'
    var_img_path = get_local_image_path('BIOS')
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def spi_util_exec_write_bios_upgrade():
    Log_Debug("Entering procedure spi_util_exec_write_bios_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spiUtil_tool
    var_opt = "write"
    var_spiNum = "spi1"
    var_dev = "BIOS"
    var_check_pattern = spiUtil_write_pattern
    var_imageFile = get_new_image_name('BIOS')
    var_readFile = 'none'
    var_img_path =  get_local_image_path('BIOS')
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def spi_util_exec_bios_option_read():
    Log_Debug("Entering procedure spi_util_exec_option_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spiUtil_tool
    var_opt = "read"
    var_spiNum = "spi1"
    var_dev = "BIOS"
    var_check_pattern = spiUtil_read_pattern
    var_imageFile = 'none'
    var_readFile="bios"
    var_img_path = get_local_image_path('BIOS')
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def verify_bios_downgrade_file():
    Log_Debug("Entering procedure verify_bios_downgrade_file.\n")
    dLibObj = getDiagLibObj()

    var_bios_image = get_old_image_name('BIOS')
    var_readFile = "bios"
    var_img_path = get_local_image_path('BIOS')

    return dLibObj.verify_bios(var_bios_image, var_readFile, var_img_path)


def verify_bios_upgrade_file():
    Log_Debug("Entering procedure verify_bios_upgrade_file.\n")
    dLibObj = getDiagLibObj()

    var_bios_image = get_new_image_name('BIOS')
    var_readFile = "bios"
    var_img_path = get_local_image_path('BIOS')

    return dLibObj.verify_bios(var_bios_image, var_readFile, var_img_path)


def verify_bios_downgrade_version():
    Log_Debug("Entering procedure verify_bios_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_cpu_bios_ver_bin
    var_opt = "--show"
    var_pattern = bios_ver_pattern
    var_dev_version = get_old_image_version('BIOS')
    var_dev = "BIOS"

    return dLibObj.verify_cpu_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def verify_bios_upgrade_version():
    Log_Debug("Entering procedure verify_bios_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_cpu_bios_ver_bin
    var_opt = "--show"
    var_pattern = bios_ver_pattern
    var_dev_version = get_new_image_version('BIOS')
    var_dev = "BIOS"

    return dLibObj.verify_cpu_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def fw_util_exec_bios_downgrade():
    Log_Debug("Entering procedure fw_util_exec_bios_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "update"
    var_dev = "bios"
    var_image = get_old_image_name('BIOS')
    var_pattern = fwUtil_update_pattern
    var_img_path = get_local_image_path('BIOS')
    var_tool_path = FW_UTIL_PATH
    var_mode = "openbmc"

    return dLibObj.fw_util_exec(var_toolName, var_fru, var_opt, var_dev, var_image, var_pattern, var_img_path, var_tool_path, var_mode)


def fw_util_exec_bios_upgrade():
    Log_Debug("Entering procedure fw_util_exec_bios_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "update"
    var_dev = "bios"
    var_image = get_new_image_name('BIOS')
    var_pattern = fwUtil_update_pattern
    var_img_path = get_local_image_path('BIOS')
    var_tool_path = FW_UTIL_PATH
    var_mode = "openbmc"

    return dLibObj.fw_util_exec(var_toolName, var_fru, var_opt, var_dev, var_image, var_pattern, var_img_path, var_tool_path, var_mode)


def check_bios_master_region():
    Log_Debug("Entering procedure check_bios_master_region.\n")
    dLibObj = getDiagLibObj()

    var_region = "master"
    var_checktool = boot_info_util
    var_toolOption = "bios"

    return dLibObj.check_bios_region(var_region, var_checktool, var_toolOption)


def verify_RTC_help_dict_option_h():
    Log_Debug("Entering procedure verify_RTC_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_RTC_help_array
    var_toolName = cel_RTC_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_RTC_help_dict_option_help():
    Log_Debug("Entering procedure verify_RTC_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_RTC_help_array
    var_toolName = cel_RTC_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_RTC_help_dict_option_a():
    Log_Debug("Entering procedure verify_RTC_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_RTC_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = rtc_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_RTC_help_dict_option_all():
    Log_Debug("Entering procedure verify_RTC_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_RTC_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = rtc_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_RTC_help_dict_option_r():
    Log_Debug("Entering procedure verify_RTC_help_dict_option_r.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_RTC_help_array["bin_tool"]
    var_option = "-r"
    var_keywords = 'none'
    var_pattern = rtc_read_pattern
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_RTC_help_dict_option_read():
    Log_Debug("Entering procedure verify_RTC_help_dict_option_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_RTC_help_array["bin_tool"]
    var_option = "--read"
    var_keywords = 'none'
    var_pattern = rtc_read_pattern
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_RTC_help_dict_option_w():
    Log_Debug("Entering procedure verify_RTC_help_dict_option_w.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_RTC_help_array["bin_tool"]
    var_option = "-w"
    var_keywords = 'none'
    var_pattern = rtc_write_patternList
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_RTC_help_dict_option_write():
    Log_Debug("Entering procedure verify_RTC_help_dict_option_write.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_RTC_help_array["bin_tool"]
    var_option = "--write"
    var_keywords = 'none'
    var_pattern = rtc_write_patternList
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_RTC_help_dict_option_w_data():
    Log_Debug("Entering procedure verify_RTC_help_dict_option_w_data.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_RTC_help_array["bin_tool"]
    var_option = "-w"
    var_keywords = 'none'
    var_pattern = rtc_write_data_patternList
    var_data='20181231 235959'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def spi_util_exec_write_th3_downgrade():
    Log_Debug("Entering procedure spi_util_exec_write_th3_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spiUtil_tool
    var_opt = "write"
    var_spiNum = "spi1"
    var_dev = "TH3_PCIE_FLASH"
    var_check_pattern = spiUtil_write_pattern
    var_imageFile = th3_downgrade_file
    var_readFile = 'none'
    var_img_path = th3_img_path
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def power_cycle():
    Log_Debug("Entering procedure power_cycle.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.wpl_powerCycle()


def power_cycle_device_to_openbmc():
    Log_Debug("Entering procedure power_cycle_device_to_openbmc.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.wpl_powerCycleDeviceToOpenBmc()


def power_cycle_device_to_centos():
    Log_Debug("Entering procedure power_cycle_device_to_centos.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.wpl_powerCycleDeviceToCentOS()


def verify_th3_downgrade_version():
    Log_Debug("Entering procedure verify_th3_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_sdkFile = sdk_file
    var_pattern = th3_ver_pattern
    var_th3_ver = th3_downgrade_ver

    return dLibObj.verify_th3_version_by_sdk(var_sdkFile, var_pattern, var_th3_ver)


def spi_util_exec_write_th3_upgrade():
    Log_Debug("Entering procedure spi_util_exec_write_th3_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spiUtil_tool
    var_opt = "write"
    var_spiNum = "spi1"
    var_dev = "TH3_PCIE_FLASH"
    var_check_pattern = spiUtil_write_pattern
    var_imageFile = th3_upgrade_file
    var_readFile = 'none'
    var_img_path = th3_img_path
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def verify_th3_upgrade_version():
    Log_Debug("Entering procedure verify_th3_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_sdkFile = sdk_file
    var_pattern = th3_ver_pattern
    var_th3_ver = th3_upgrade_ver

    return dLibObj.verify_th3_version_by_sdk(var_sdkFile, var_pattern, var_th3_ver)


def spi_util_exec_write_fpga1_upgrade():
    Log_Debug("Entering procedure spi_util_exec_write_fpga1_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spiUtil_tool
    var_opt = "write"
    var_spiNum = "spi1"
    var_dev = "DOM_FPGA_FLASH1"
    var_check_pattern = spiUtil_write_pattern
    var_imageFile = get_new_image_name('FPGA')
    var_readFile = 'none'
    var_img_path = get_local_image_path('FPGA')
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def spi_util_exec_write_fpga2_upgrade():
    Log_Debug("Entering procedure spi_util_exec_write_fpga2_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spiUtil_tool
    var_opt = "write"
    var_spiNum = "spi1"
    var_dev = "DOM_FPGA_FLASH2"
    var_check_pattern = spiUtil_write_pattern
    var_imageFile = get_new_image_name('FPGA')
    var_readFile = 'none'
    var_img_path = get_local_image_path('FPGA')
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def verify_fpga1_upgrade_version():
    Log_Debug("Entering procedure verify_fpga1_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fpga_software_test
    var_opt = "-v"
    var_pattern = fpga1_ver_pattern
    var_dev_version = get_new_image_version('FPGA')
    var_dev = "fpga1"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def verify_fpga2_upgrade_version():
    Log_Debug("Entering procedure verify_fpga2_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fpga_software_test
    var_opt = "-v"
    var_pattern = fpga2_ver_pattern
    var_dev_version = get_new_image_version('FPGA')
    var_dev = "fpga2"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def spi_util_exec_write_fpga1_downgrade():
    Log_Debug("Entering procedure spi_util_exec_write_fpga1_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spiUtil_tool
    var_opt = "write"
    var_spiNum = "spi1"
    var_dev = "DOM_FPGA_FLASH1"
    var_check_pattern = spiUtil_write_pattern
    var_imageFile = get_old_image_name('FPGA')
    var_readFile = 'none'
    var_img_path = get_local_image_path('FPGA')
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def spi_util_exec_write_fpga2_downgrade():
    Log_Debug("Entering procedure spi_util_exec_write_fpga2_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spiUtil_tool
    var_opt = "write"
    var_spiNum = "spi1"
    var_dev = "DOM_FPGA_FLASH2"
    var_check_pattern = spiUtil_write_pattern
    var_imageFile = get_old_image_name('FPGA')
    var_readFile = 'none'
    var_img_path = get_local_image_path('FPGA')
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def verify_fpga1_downgrade_version():
    Log_Debug("Entering procedure verify_fpga1_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fpga_software_test
    var_opt = "-v"
    var_pattern = fpga1_ver_pattern
    var_dev_version = get_old_image_version('FPGA')
    var_dev = "fpga1"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def verify_fpga2_downgrade_version():
    Log_Debug("Entering procedure verify_fpga2_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fpga_software_test
    var_opt = "-v"
    var_pattern = fpga2_ver_pattern
    var_dev_version = get_old_image_version('FPGA')
    var_dev = "fpga2"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def verify_pcie_help_dict_option_h():
    Log_Debug("Entering procedure verify_pcie_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_pcie_help_array
    var_toolName = cel_pcie_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_pcie_help_dict_option_help():
    Log_Debug("Entering procedure verify_pcie_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_pcie_help_array
    var_toolName = cel_pcie_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_pcie_help_dict_option_a():
    Log_Debug("Entering procedure verify_pcie_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_pcie_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = pcie_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_pcie_help_dict_option_all():
    Log_Debug("Entering procedure verify_pcie_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_pcie_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = pcie_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def fw_util_exec_bic_downgrade():
    Log_Debug("Entering procedure fw_util_exec_bic_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "update"
    var_dev = "bic"
    var_image = get_old_image_name('BIC')
    var_pattern = bic_update_pattern
    var_img_path = get_local_image_path('BIC')
    var_tool_path = FW_UTIL_PATH
    var_mode = "openbmc"

    return dLibObj.fw_util_exec(var_toolName, var_fru, var_opt, var_dev, var_image, var_pattern, var_img_path, var_tool_path, var_mode)


def verify_bic_downgrade_version():
    Log_Debug("Entering procedure verify_bic_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = bic_software_test
    var_opt = "-v"
    var_pattern = bic_ver_pattern
    var_dev_version = get_old_image_version('BIC')
    var_dev = "bic"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def fw_util_exec_bic_upgrade():
    Log_Debug("Entering procedure fw_util_exec_bic_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "update"
    var_dev = "bic"
    var_image = get_new_image_name('BIC')
    var_pattern = bic_update_pattern
    var_img_path = get_local_image_path('BIC')
    var_tool_path = FW_UTIL_PATH
    var_mode = "openbmc"

    return dLibObj.fw_util_exec(var_toolName, var_fru, var_opt, var_dev, var_image, var_pattern, var_img_path, var_tool_path, var_mode)


def verify_bic_upgrade_version():
    Log_Debug("Entering procedure verify_bic_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = bic_software_test
    var_opt = "-v"
    var_pattern = bic_ver_pattern
    var_dev_version = get_new_image_version('BIC')
    var_dev = "bic"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_fcm_downgrade():
    Log_Debug("Entering procedure updateTool_exec_fcm_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fcm_cpld_tool
    var_image = get_old_sub_image_name('CPLD', 'fcm')
    var_opt = "hw"
    var_dev = "FCM-CPLD"
    var_pattern = fcm_update_pattern
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = CPLD_TOOL_PATH

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path, var_tool_path)


def verify_fcm_downgrade_version():
    Log_Debug("Entering procedure verify_fcm_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fcm_software_test
    var_opt = "-v"
    var_pattern = fcm_ver_pattern
    var_dev_version = get_old_sub_image_version('CPLD', 'fcm')
    var_dev = "FCM-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_fcm_upgrade():
    Log_Debug("Entering procedure updateTool_exec_fcm_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fcm_cpld_tool
    var_image = get_new_sub_image_name('CPLD', 'fcm')
    var_opt = "hw"
    var_dev = "FCM-CPLD"
    var_pattern = fcm_update_pattern
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = CPLD_TOOL_PATH

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path, var_tool_path)


def verify_fcm_upgrade_version():
    Log_Debug("Entering procedure verify_fcm_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fcm_software_test
    var_opt = "-v"
    var_pattern = fcm_ver_pattern
    var_dev_version = get_new_sub_image_version('CPLD', 'fcm')
    var_dev = "FCM-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_scm_downgrade():
    Log_Debug("Entering procedure updateTool_exec_scm_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = scm_cpld_tool
    var_image = get_old_sub_image_name('CPLD', 'scm')
    var_opt = "hw"
    var_dev = "SCM-CPLD"
    var_pattern = scm_update_pattern
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = CPLD_TOOL_PATH

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path, var_tool_path)


def verify_scm_downgrade_version():
    Log_Debug("Entering procedure verify_scm_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = scm_software_test
    var_opt = "-v"
    var_pattern = scm_ver_pattern
    var_dev_version = get_old_sub_image_version('CPLD', 'scm')
    var_dev = "SCM-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_scm_upgrade():
    Log_Debug("Entering procedure updateTool_exec_scm_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = scm_cpld_tool
    var_image = get_new_sub_image_name('CPLD', 'scm')
    var_opt = "hw"
    var_dev = "SCM-CPLD"
    var_pattern = scm_update_pattern
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = CPLD_TOOL_PATH

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path, var_tool_path)


def verify_scm_upgrade_version():
    Log_Debug("Entering procedure verify_scm_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = scm_software_test
    var_opt = "-v"
    var_pattern = scm_ver_pattern
    var_dev_version = get_new_sub_image_version('CPLD', 'scm')
    var_dev = "SCM-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_smb_downgrade():
    Log_Debug("Entering procedure updateTool_exec_smb_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = smb_cpld_tool
    var_image = get_old_sub_image_name('CPLD', 'smb')
    var_opt = "hw"
    var_dev = "SMB-CPLD"
    var_pattern = smb_update_pattern
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = CPLD_TOOL_PATH

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path, var_tool_path)


def verify_smb_downgrade_version():
    Log_Debug("Entering procedure verify_smb_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = smb_software_test
    var_opt = "-v"
    var_pattern = smb_ver_pattern
    var_dev_version = get_old_sub_image_version('CPLD', 'smb')
    var_dev = "SMB-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_smb_upgrade():
    Log_Debug("Entering procedure updateTool_exec_smb_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = smb_cpld_tool
    var_image = get_new_sub_image_name('CPLD', 'smb')
    var_opt = "hw"
    var_dev = "SMB-CPLD"
    var_pattern = smb_update_pattern
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = CPLD_TOOL_PATH

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path, var_tool_path)


def verify_smb_upgrade_version():
    Log_Debug("Entering procedure verify_smb_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = smb_software_test
    var_opt = "-v"
    var_pattern = smb_ver_pattern
    var_dev_version = get_new_sub_image_version('CPLD', 'smb')
    var_dev = "SMB-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def verify_fpga_help_dict_option_h():
    Log_Debug("Entering procedure verify_fpga_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_fpga_help_array
    var_toolName = cel_fpga_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_fpga_help_dict_option_help():
    Log_Debug("Entering procedure verify_fpga_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_fpga_help_array
    var_toolName = cel_fpga_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_fpga_help_dict_option_a():
    Log_Debug("Entering procedure verify_fpga_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fpga_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = fpga_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_fpga_help_dict_option_all():
    Log_Debug("Entering procedure verify_fpga_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fpga_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = fpga_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_sw_version_help_dict_option_h():
    Log_Debug("Entering procedure verify_sw_version_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_version_help_array
    var_toolName = cel_version_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_sw_version_help_dict_option_help():
    Log_Debug("Entering procedure verify_sw_version_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_version_help_array
    var_toolName = cel_version_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def updateTool_exec_pwr_cpld_downgrade():
    Log_Debug("Entering procedure updateTool_exec_pwr_cpld_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = pwr_cpld_tool
    var_image = get_old_sub_image_name('CPLD', 'pwr')
    var_opt = "hw"
    var_dev = "PWR-CPLD"
    var_pattern = pwr_update_pattern
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = CPLD_TOOL_PATH

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path, var_tool_path)


def verify_pwr_cpld_downgrade_version():
    Log_Debug("Entering procedure verify_pwr_cpld_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = pwr_software_test
    var_opt = "-v"
    var_pattern = pwr_ver_pattern
    var_dev_version = get_old_sub_image_version('CPLD', 'pwr')
    var_dev = "PWR-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_pwr_cpld_upgrade():
    Log_Debug("Entering procedure updateTool_exec_pwr_cpld_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = pwr_cpld_tool
    var_image = get_new_sub_image_name('CPLD', 'pwr')
    var_opt = "hw"
    var_dev = "PWR-CPLD"
    var_pattern = pwr_update_pattern
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = CPLD_TOOL_PATH

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path, var_tool_path)


def verify_pwr_cpld_upgrade_version():
    Log_Debug("Entering procedure verify_pwr_cpld_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = pwr_software_test
    var_opt = "-v"
    var_pattern = pwr_ver_pattern
    var_dev_version = get_new_sub_image_version('CPLD', 'pwr')
    var_dev = "PWR-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def verify_bmc_cpu_help_dict_option_h():
    Log_Debug("Entering procedure verify_bmc_cpu_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_bmc_cpu_help_array
    var_toolName = cel_bmc_cpu_help_array["bin_tool"]
    var_option = "-h"
    var_pattern = bmc_cpu_help_pattern

    return dLibObj.verify_option_bmc_diag_tool_simple_dict(var_inputArray, var_toolName, var_option, var_pattern)


def verify_bmc_cpu_help_dict_option_a():
    Log_Debug("Entering procedure verify_bmc_cpu_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpu_help_array["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = bmc_cpu_keyword_pattern
    var_pass_pattern = test_pass_pattern

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)


def verify_bmc_cpu_help_dict_option_i():
    Log_Debug("Entering procedure verify_bmc_cpu_help_dict_option_i.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_bmc_cpu_info_array
    var_toolName = cel_bmc_cpu_help_array["bin_tool"]
    var_option = "-i"
    var_pattern = bmc_cpu_info_pattern

    return dLibObj.verify_option_bmc_diag_tool_simple_dict(var_inputArray, var_toolName, var_option, var_pattern)


def verify_bmc_fpga_help_dict_option_h():
    Log_Debug("Entering procedure verify_bmc_fpga_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_bmc_fpga_help_array
    var_toolName = cel_bmc_fpga_help_array["bin_tool"]
    var_option = "-h"
    var_pattern = bmc_fpga_help_pattern

    return dLibObj.verify_option_bmc_diag_tool_simple_dict(var_inputArray, var_toolName, var_option, var_pattern)


def verify_bmc_fpga_device_write_read():
    Log_Debug("Entering procedure verify_bmc_fpga_device_write_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_help_array["bin_tool"]
    var_dev = "DOM_FPGA_1"
    var_address = "4"
    var_data = "0xaa"

    return dLibObj.verify_device_write_read(var_toolName, var_dev, var_address, var_data)


def verify_bmc_fpga_help_dict_option_a():
    Log_Debug("Entering procedure verify_bmc_fpga_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_help_array["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = bmc_fpga_keyword_pattern
    var_pass_pattern = test_pass_pattern

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)


def verify_bmc_cpld_help_dict_option_h():
    Log_Debug("Entering procedure verify_bmc_cpld_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_bmc_cpld_help_array
    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_option = "-h"
    var_pattern = bmc_cpld_help_pattern

    return dLibObj.verify_option_bmc_diag_tool_simple_dict(var_inputArray, var_toolName, var_option, var_pattern)


def verify_bmc_cpld_device_write_read():
    Log_Debug("Entering procedure verify_bmc_cpld_device_write_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_dev = "FCM_CPLD"
    var_address = "4"
    var_data = "0xaa"

    return dLibObj.verify_device_write_read(var_toolName, var_dev, var_address, var_data)


def verify_bmc_cpld_help_dict_option_a():
    Log_Debug("Entering procedure verify_bmc_cpld_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = bmc_cpld_keyword_pattern
    var_pass_pattern = test_pass_pattern

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)


def verify_bmc_cpld_help_dict_option_v():
    Log_Debug("Entering procedure verify_bmc_cpld_help_dict_option_v.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = wedge400c_get_cpld_version_array()
    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_option = "-v"
    var_pattern = bmc_cpld_version_pattern

    return dLibObj.verify_option_bmc_diag_tool_simple_dict(var_inputArray, var_toolName, var_option, var_pattern)


def verify_bmc_i2c_help_dict_option_h():
    Log_Debug("Entering procedure verify_bmc_i2c_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_bmc_i2c_help_array
    var_toolName = cel_bmc_i2c_help_array["bin_tool"]
    var_option = "-h"
    var_pattern = bmc_i2c_help_pattern

    return dLibObj.verify_option_bmc_diag_tool_simple_dict(var_inputArray, var_toolName, var_option, var_pattern)


def verify_bmc_i2c_help_dict_option_a():
    Log_Debug("Entering procedure verify_bmc_i2c_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_i2c_help_array["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = bmc_i2c_keyword_pattern
    var_pass_pattern = test_pass_pattern

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)


def verify_bmc_i2c_help_dict_option_s():
    Log_Debug("Entering procedure verify_bmc_i2c_help_dict_option_s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_i2c_help_array["bin_tool"]
    var_option = "-s"
    var_keywords_pattern = i2c_scan_pattern
    var_pass_pattern = i2c_scan_pass_keyword

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)


def verify_bmc_scm_auto_eeprom_dict():
    Log_Debug("Entering procedure verify_bmc_scm_auto_eeprom_dict.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_scm_auto_eeprom["bin_tool"]
    var_option = ""
    var_keywords_pattern = cel_bmc_scm_auto_eeprom_pattern
    var_pass_pattern = ""

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, SCM_EEPROM_PATH)


def verify_bmc_fcm_auto_eeprom_dict():
    Log_Debug("Entering procedure verify_bmc_fcm_auto_eeprom_dict.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fcm_auto_eeprom["bin_tool"]
    var_option = ""
    var_keywords_pattern = cel_bmc_fcm_auto_eeprom_pattern
    var_pass_pattern = ""

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, FCM_EEPROM_PATH)


def verify_bmc_smb_auto_eeprom_dict():
    Log_Debug("Entering procedure verify_bmc_smb_auto_eeprom_dict.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_smb_auto_eeprom["bin_tool"]
    var_option = ""
    var_keywords_pattern = cel_bmc_smb_auto_eeprom_pattern
    var_pass_pattern = ""
    var_path = SMB_EEPROM_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def verify_bmc_eeprom_tool_dict_option_d():
    Log_Debug("Entering procedure verify_bmc_eeprom_tool_dict_option_d.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_eeprom_tool_d["bin_tool"]
    var_option = "-d"
    var_keywords_pattern = cel_bmc_eeprom_tool_d_pattern
    var_pass_pattern = ""
    var_path = SMB_EEPROM_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_bmc_cel_boot_test_h():
    Log_Debug("Entering procedure verify_bmc_cel_boot_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = bmc_cel_boot_test_h["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = bmc_cel_boot_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_boot_test_b_bmc_s():
    Log_Debug("Entering procedure verify_cel_boot_test_b_bmc_s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test_b_bmc_s["bin_tool"]
    var_option = "-b bmc -s"
    var_keywords_pattern = cel_boot_test_b_bmc_s_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_h():
    Log_Debug("Entering procedure verify_cel_fan_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_fan_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_g():
    Log_Debug("Entering procedure verify_cel_fan_test_g.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-g"
    var_keywords_pattern = cel_fan_test_g_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_s():
    Log_Debug("Entering procedure verify_cel_fan_test_s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-s"
    var_keywords_pattern = cel_fan_test_s_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_p_10():
    Log_Debug("Entering procedure verify_cel_fan_test_p_10.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-p 10"
    var_keywords_pattern = cal_fan_test_p_10_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_g_p_10():
    Log_Debug("Entering procedure verify_cel_fan_test_g_p_10.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-g"
    var_keywords_pattern = cel_fan_test_g_p_10_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_p_100():
    Log_Debug("Entering procedure verify_cel_fan_test_p_10.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-p 100"
    var_keywords_pattern = cal_fan_test_p_100_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_g_p_100():
    Log_Debug("Entering procedure verify_cel_fan_test_g_p_10.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-g"
    var_keywords_pattern = cel_fan_test_g_p_100_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_p_50():
    Log_Debug("Entering procedure verify_cel_fan_test_p_10.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-p 50"
    var_keywords_pattern = cal_fan_test_p_50_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_g_p_50():
    Log_Debug("Entering procedure verify_cel_fan_test_g_p_10.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-g"
    var_keywords_pattern = cel_fan_test_g_p_50_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_a():
    Log_Debug("Entering procedure verify_cel_fan_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_fan_test_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_c_sanyo():
    Log_Debug("Entering procedure verify_cel_fan_test_c_sanyo.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-c SANYO"
    var_keywords_pattern = cel_fan_test_c_sanyo_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_e():
    Log_Debug("Entering procedure verify_cel_fan_test_e.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-e"
    var_keywords_pattern = cel_fan_test_e_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_memory_test_h():
    Log_Debug("Entering procedure cel_memory_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_memory_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_memory_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_memory_test_i():
    Log_Debug("Entering procedure cel_memory_test_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_memory_test["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = cel_memory_test_i_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_memory_test_m():
    Log_Debug("Entering procedure cel_memory_test_m.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_memory_test["bin_tool"]
    var_option = "-m"
    var_keywords_pattern = cel_memory_test_m_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_memory_test_a():
    Log_Debug("Entering procedure cel_memory_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_memory_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_memory_test_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_emmc_test_h():
    Log_Debug("Entering procedure cel_emmc_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_emmc_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_emmc_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_emmc_test_i():
    Log_Debug("Entering procedure cel_emmc_test_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_emmc_test["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = cel_emmc_test_i_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_emmc_test_s():
    Log_Debug("Entering procedure cel_emmc_test_s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_emmc_test["bin_tool"]
    var_option = "-s"
    var_keywords_pattern = cel_emmc_test_s_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_emmc_test_a():
    Log_Debug("Entering procedure cel_emmc_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_emmc_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_emmc_test_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

# This function is not begins used, because it is a bug on the terminal
# root@bmc-oob:/usr/bin# ./find /mnt/data1/BMC_Diag/bin/ -type f -name "*disk.dump"
# " <= This is a bug!
# root@bmc-oob:/usr/bin#
def check_the_file_disk_dump_is_deleted():
    Log_Debug("Entering procedure check_the_file_disk_dump_is_deleted.\n")
    dLibObj = getDiagLibObj()

    var_toolName ='find'
    var_option = BMC_DIAG_TOOL_PATH + ' -type f -name "*disk.dump"'
    var_keywords_pattern = cel_find_disk_dump_pattern
    var_pass_pattern = ""
    var_path = "/usr/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def check_the_cpu_os_version():
    Log_Debug("Entering procedure check_the_cpu_os_version.\n")
    dLibObj = getDiagLibObj()

    dLibObj.EXEC_bmc_diag_tool_command("sol.sh")

    var_toolName ='cat'
    var_option = "/etc/product/VERSION"
    var_keywords_pattern = check_cpu_os_version
    var_pass_pattern = ""
    var_path = "/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def check_the_issue_file():
    Log_Debug("Entering procedure check_the_issue_file.\n")
    dLibObj = getDiagLibObj()


    var_toolName ='cat'
    var_option = "/etc/issue"
    var_keywords_pattern = check_cpu_os_version
    var_pass_pattern = ""
    var_path = "/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_mdio_test_h():
    Log_Debug("Entering procedure cel_mdio_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mdio_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_mdio_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_mdio_test_a():
    Log_Debug("Entering procedure cel_mdio_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mdio_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_mdio_test_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_hotswap_test_h():
    Log_Debug("Entering procedure cel_hotswap_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_hotswap_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_hotswap_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_hotswap_test_a():
    Log_Debug("Entering procedure cel_hotswap_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_hotswap_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_hotswap_test_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def i2cset_scm_hotswap():
    Log_Debug("Entering procedure i2cset_scm_hotswap.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "i2cset"
    var_option = "-f -y 2 0x70 0x1 && i2cget -f -y 2 0x10 0x19"
    var_keywords_pattern = i2cset_scm_and_fcm_hotswap_pattern
    var_pass_pattern = ""
    var_path = "/usr/sbin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def i2cset_fcm_hotswap():
    Log_Debug("Entering procedure i2cset_fcm_hotswap.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "i2cset"
    var_option = "-f -y 11 0x76 0x8 && i2cget -f -y 11 0x10 0x19"
    var_keywords_pattern = i2cset_scm_and_fcm_hotswap_pattern
    var_pass_pattern = ""
    var_path = "/usr/sbin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_psu_test_h():
    Log_Debug("Entering procedure cel_psu_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_psu_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_psu_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_psu_test_s():
    Log_Debug("Entering procedure cel_psu_test_s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_psu_test["bin_tool"]
    var_option = "-s"
    var_keywords_pattern = cel_psu_test_s_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_psu_test_a():
    Log_Debug("Entering procedure cel_psu_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_psu_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_psu_test_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def read_current_bmc_version():
    Log_Debug("Entering procedure read_current_bmc_version.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.get_current_bmc_version()


def flash_update_and_verify_bmc_fw():
    Log_Debug("Entering procedure flash_update_and_verify_bmc_fw.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_toolName = flashtool

    var_img_path = get_local_image_path('BMC')
    var_downgrade_bmc_image = get_old_image_name('BMC')
    var_upgrade_bmc_image = get_new_image_name('BMC')
    var_downgrade_ver = get_old_image_version('BMC')
    var_upgrade_ver = get_new_image_version('BMC')
    var_flash_device = flash_device_path
    var_log_file = (pwdPath + '/' + LOG_PATH + bmc_update_stress_log + '.log')
    var_uartLog_file = (pwdPath + '/' + LOG_PATH + openbmc_uart_log + '.log')

    return dLibObj.flash_update_and_verify_bmc_ver(var_toolName, var_img_path, var_downgrade_bmc_image, var_upgrade_bmc_image,
                                               var_downgrade_ver, var_upgrade_ver, var_flash_device, var_log_file, var_uartLog_file)


def set_and_verify_cpld_register_before_update():
    Log_Debug("Entering procedure set_and_verify_cpld_register_before_update.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cpld_verify_tool
    var_module = smb_cpld
    var_set_reg = bios_smb_set_reg
    var_set_val = bios_smb_before_update_value
    var_toolPath = UTILITY_TOOL_PATH

    return dLibObj.set_and_verify_cpld_register(var_toolName, var_module, var_set_reg, var_set_val, var_toolPath)


def set_and_verify_cpld_register_after_update():
    Log_Debug("Entering procedure set_and_verify_cpld_register_after_update.\n")
    dLibObj = getDiagLibObj()

    # i2cset -f -y 12 0x3e 0x20 0x00
    var_setToolName = i2c_set_tool
    var_verifyToolName = i2c_get_tool
    var_option = i2c_default_options
    var_bus = bios_smb_cpld_bus
    var_chip_addr = bios_smb_cpld_chip_address
    var_data_addr = bios_smb_set_reg
    var_value = bios_smb_after_update_value

    return dLibObj.set_and_verify_i2c_register(var_setToolName, var_verifyToolName, var_option, var_bus, var_chip_addr, var_data_addr, var_value)


def check_bios_version():
    Log_Debug("Entering procedure check_bios_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "--version"
    var_tool_path = FW_UTIL_PATH

    return dLibObj.get_current_bios_version(var_toolName, var_fru, var_opt, var_tool_path)


def check_bmc_version():
    Log_Debug("Entering procedure check_bmc_version\n")
    dLibObj = getDiagLibObj()

    var_upgrade_ver = get_new_image_version('BMC')
    var_downgrade_ver = get_old_image_version('BMC')

    return dLibObj.check_current_bmc_version(var_upgrade_ver, var_downgrade_ver)


def check_bmc_master_region():
    Log_Debug("Entering procedure check_bmc_master_region.\n")
    dLibObj = getDiagLibObj()

    var_region = "Master"
    var_checktool = boot_info_util
    var_toolOption = "bmc"

    return dLibObj.check_bmc_region(var_region, var_checktool, var_toolOption)


def check_all_fw_sw_versions():
    Log_Debug("Entering procedure check_all_fw_sw_versions.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = get_fw_sw_version_array()
    var_toolName = fw_util_tool
    var_fru = "scm"
    var_option = "--version"
    var_tool_path = FW_UTIL_PATH
    var_key = "BIOS_VER"

    return dLibObj.verify_option_bmc_tool_system_dict(var_inputArray, var_toolName, var_fru, var_option, var_tool_path, var_key)


def set_bios_update_cycles(max_loop_count):
    Log_Debug("Entering procedure set_bios_update_cycle_count.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_max_bios_update_cycles(max_loop_count)


def flash_update_master_bios_region():
    Log_Debug("Entering procedure flash_update_master_bios_region.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "update"
    var_dev = "bios"
    var_check_pattern = fwUtil_update_pattern

    var_downgrade_bios_image = get_old_image_name('BIOS')
    var_upgrade_bios_image = get_new_image_name('BIOS')
    var_downgrade_ver = get_old_image_version('BIOS')
    var_upgrade_ver = get_new_image_version('BIOS')
    var_img_path = get_local_image_path('BIOS')
    var_tool_path = FW_UTIL_PATH
    var_log_file = (pwdPath + '/' + LOG_PATH + bios_update_stress_log + '.log')

    return dLibObj.flash_update_master_bios(var_toolName, var_fru, var_opt, var_dev, var_check_pattern, var_downgrade_bios_image,
                                            var_upgrade_bios_image, var_downgrade_ver, var_upgrade_ver, var_img_path, var_tool_path, var_log_file)


def verify_master_bios_version():
    Log_Debug("Entering procedure verify_master_bios.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_log_File = (pwdPath + '/' + LOG_PATH + openbmc_uart_log + '.log')

    return dLibObj.switch_and_verify_master_bios_version(var_log_File)


def check_bic_version():
    Log_Debug("Entering procedure check_bic_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "--version"
    var_tool_path = FW_UTIL_PATH

    return dLibObj.get_current_bic_version(var_toolName, var_fru, var_opt, var_tool_path)


def verify_cpld_register_before_update():
    Log_Debug("Entering procedure verify_cpld_register_before_update.\n")
    dLibObj = getDiagLibObj()

    var_verifyToolName = i2c_get_tool
    var_option = i2c_default_options
    var_bus = bios_smb_cpld_bus
    var_chip_addr = bios_smb_cpld_chip_address
    var_data_addr = bios_smb_set_reg
    var_value = bios_smb_before_update_value

    return dLibObj.verify_i2c_register(var_verifyToolName, var_option, var_bus, var_chip_addr, var_data_addr, var_value)


def flash_update_bic_fw():
    Log_Debug("Entering procedure flash_update_bic_fw.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "update"
    var_dev = "bic"
    var_check_pattern = bic_update_pattern
    var_downgrade_bic_image = get_old_image_name('BIC')
    var_upgrade_bic_image = get_new_image_name('BIC')
    var_downgrade_ver = get_old_image_version('BIC')
    var_upgrade_ver = get_new_image_version('BIC')
    var_img_path = get_local_image_path('BIC')
    var_tool_path = FW_UTIL_PATH
    var_log_file = (pwdPath + '/' + LOG_PATH + bic_update_stress_log + '.log')

    return dLibObj.flash_update_bic(var_toolName, var_fru, var_opt, var_dev, var_check_pattern, var_downgrade_bic_image,
                                    var_upgrade_bic_image, var_downgrade_ver, var_upgrade_ver, var_img_path, var_tool_path, var_log_file)


def power_reset_wedge400():
    Log_Debug("Entering procedure power_reset_wedge400.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_toolName = WEDGE400_POWER_RESET
    var_operation = "reset"
    var_opt = "-s"
    var_tool_path = SPI_UTIL_PATH
    var_log_file = (LOG_PATH + openbmc_uart_log + '.log')
    var_log_file = (pwdPath + '/' + LOG_PATH + openbmc_uart_log + '.log')

    return dLibObj.wedge400_power_reset(var_toolName, var_operation, var_opt, var_tool_path, var_log_file)


def set_bic_update_cycles(max_loop_count):
    Log_Debug("Entering procedure set_bic_update_cycle_count.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_max_bic_update_cycles(max_loop_count)


def verify_bic_update_version():
    Log_Debug("Entering procedure verify_bic_update_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "--version"
    var_tool_path = FW_UTIL_PATH

    return dLibObj.verify_bic_version(var_toolName, var_fru, var_opt, var_tool_path)


def backup_log_file(fileList, srcPath, destPath, mode):
    Log_Debug("Entering procedure backup_log_file.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    ROOT_DIR = os.path.abspath(os.curdir)
    Log_Debug("PWD = [%s]" %pwdPath)
    Log_Debug("ROOT_DIR = [%s]" %ROOT_DIR)

    if re.search('/home', pwdPath):
        # cap server
        var_username = dLibObj.wpl_get_pc_scp_username()
        var_password = dLibObj.wpl_get_pc_scp_password()
        dhcp_ipv6 = dLibObj.wpl_get_pc_scp_ipv6()
        static_ipv6 = dLibObj.wpl_get_pc_scp_static_ipv6()
        var_server_ip = get_server_dhcp_or_static_ip(dhcp_ipv6, static_ipv6)
        var_filepath = srcPath
    else:
        # jenkins server
        var_username = dLibObj.wpl_get_jenkins_scp_username()
        var_password = dLibObj.wpl_get_jenkins_scp_password()
        dhcp_ipv6 = dLibObj.wpl_get_jenkins_scp_ipv6()
        static_ipv6 = dLibObj.wpl_get_jenkins_scp_static_ipv6()
        var_server_ip = get_server_dhcp_or_static_ip(dhcp_ipv6, static_ipv6)
        var_filepath = JENKINS_WORKING_DIRECTORY + srcPath

    if mode == 'openbmc':
        var_interface = openbmc_eth_params['interface']
    else:
        var_interface = centos_eth_params['interface']

    for fileName in fileList:
        filePathName = var_filepath + fileName
        if dLibObj.check_local_file_exists(filePathName) == True:
            var_filelist = []
            var_filelist.append(fileName)
            var_destination_path = destPath
            var_mode = mode

            output = 0
            output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

            if output:
                dLibObj.wpl_raiseException("Failed copy_files_through_scp")

            Log_Debug("Successfully backup_log_file: [%s]\n" %fileName)

    return True


def backup_cpu_uart_log():
    Log_Debug("Entering procedure backup_cpu_uart_log.\n")
    dLibObj = getDiagLibObj()

    var_log_file = (cpu_uart_log + '.log')
    var_prefix = (cpu_uart_log + '_')
    var_src_path = VAR_LOG_PATH
    var_dest_path = SYSTEM_CONSOLE_LOG_PATH

    return dLibObj.backup_uart_log_file(var_log_file, var_prefix, True, var_src_path, var_dest_path)


def backup_openbmc_uart_log():
    Log_Debug("Entering procedure backup_openbmc_uart__log.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_log_file = (openbmc_uart_log + '.log')
    var_prefix = (openbmc_uart_log + '_')
    var_src_path = (pwdPath + '/' + LOG_PATH)
    var_dest_path = SYSTEM_CONSOLE_LOG_PATH
    var_file_list = []

    backupFilename = dLibObj.check_local_log_file(var_log_file, var_prefix, True, var_src_path, var_dest_path)
    if backupFilename != 'None':
        var_file_list.append(backupFilename)
        return backup_log_file(var_file_list, var_src_path, var_dest_path, openbmc_mode)
    else:
        return 'None'


def backup_bmc_update_stress_log():
    Log_Debug("Entering procedure backup_bmc_update_stress_log.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_log_file = (bmc_update_stress_log + '.log')
    var_prefix = (bmc_update_stress_log + '-')
    var_src_path = (pwdPath + '/' + LOG_PATH)
    var_dest_path = SYSTEM_CONSOLE_LOG_PATH
    var_file_list = []

    backupFilename = dLibObj.check_local_log_file(var_log_file, var_prefix, True, var_src_path, var_dest_path)
    if backupFilename != 'None':
        var_file_list.append(backupFilename)
        return backup_log_file(var_file_list, var_src_path, var_dest_path, openbmc_mode)
    else:
        return 'None'


def backup_bic_update_stress_log():
    Log_Debug("Entering procedure backup_bic_update_stress_log.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_log_file = (bic_update_stress_log + '.log')
    var_prefix = (bic_update_stress_log + '-')
    var_src_path = (pwdPath + '/' + LOG_PATH)
    var_dest_path = SYSTEM_CONSOLE_LOG_PATH
    var_file_list = []

    backupFilename = dLibObj.check_local_log_file(var_log_file, var_prefix, True, var_src_path, var_dest_path)
    if backupFilename != 'None':
        var_file_list.append(backupFilename)
        return backup_log_file(var_file_list, var_src_path, var_dest_path, openbmc_mode)
    else:
        return 'None'


def backup_bios_update_stress_log():
    Log_Debug("Entering procedure backup_bios_update_stress_log.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_log_file = (bios_update_stress_log + '.log')
    var_prefix = (bios_update_stress_log + '-')
    var_src_path = (pwdPath + '/' + LOG_PATH)
    var_dest_path = SYSTEM_CONSOLE_LOG_PATH
    var_file_list = []

    backupFilename = dLibObj.check_local_log_file(var_log_file, var_prefix, True, var_src_path, var_dest_path)
    if backupFilename != 'None':
        var_file_list.append(backupFilename)
        return backup_log_file(var_file_list, var_src_path, var_dest_path, openbmc_mode)
    else:
        return 'None'


def backup_uart_logs():
    Log_Debug("Entering procedure backup_uart_logs.\n")
    dLibObj = getDiagLibObj()

    backup_openbmc_uart_log()
    backup_cpu_uart_log()


def read_current_cpld_versions():
    Log_Debug("Entering procedure read_current_cpld_versions.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cpld_version_tool
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.get_current_cpld_versions(var_toolName, var_tool_path)


def flash_update_smb_cpld_fw():
    Log_Debug("Entering procedure flash_update_smb_cpld_fw.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_dev = 'cpld'
    var_cpld_type = 'smb'
    var_toolName = smb_cpld_tool
    var_check_pattern = cpld_update_pattern
    var_downgrade_cpld_image = get_old_sub_image_name('CPLD', 'smb')
    var_upgrade_cpld_image = get_new_sub_image_name('CPLD', 'smb')
    var_downgrade_ver = get_old_sub_image_version('CPLD', 'smb')
    var_upgrade_ver = get_new_sub_image_version('CPLD', 'smb')
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = SPI_UTIL_PATH
    var_log_file = (pwdPath + '/' + LOG_PATH + cpld_update_stress_log + '.log')

    return dLibObj.flash_update_cpld(var_dev, var_cpld_type, var_toolName, var_check_pattern, var_downgrade_cpld_image,
                                    var_upgrade_cpld_image, var_downgrade_ver, var_upgrade_ver, var_img_path, var_tool_path, var_log_file)


def flash_update_fcm_cpld_fw():
    Log_Debug("Entering procedure flash_update_fcm_cpld_fw.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_dev = 'cpld'
    var_cpld_type = 'fcm'
    var_toolName = fcm_cpld_tool
    var_check_pattern = cpld_update_pattern
    var_downgrade_cpld_image = get_old_sub_image_name('CPLD', 'fcm')
    var_upgrade_cpld_image = get_new_sub_image_name('CPLD', 'fcm')
    var_downgrade_ver = get_old_sub_image_version('CPLD', 'fcm')
    var_upgrade_ver = get_new_sub_image_version('CPLD', 'fcm')
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = SPI_UTIL_PATH
    var_log_file = (pwdPath + '/' + LOG_PATH + cpld_update_stress_log + '.log')

    return dLibObj.flash_update_cpld(var_dev, var_cpld_type, var_toolName, var_check_pattern, var_downgrade_cpld_image,
                                    var_upgrade_cpld_image, var_downgrade_ver, var_upgrade_ver, var_img_path, var_tool_path, var_log_file)


def flash_update_pwr_cpld_fw():
    Log_Debug("Entering procedure flash_update_pwr_cpld_fw.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_dev = 'cpld'
    var_cpld_type = 'pwr'
    var_toolName = pwr_cpld_tool
    var_check_pattern = cpld_update_pattern
    var_downgrade_cpld_image = get_old_sub_image_name('CPLD', 'pwr')
    var_upgrade_cpld_image = get_new_sub_image_name('CPLD', 'pwr')
    var_downgrade_ver = get_old_sub_image_version('CPLD', 'pwr')
    var_upgrade_ver = get_new_sub_image_version('CPLD', 'pwr')
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = SPI_UTIL_PATH
    var_log_file = (pwdPath + '/' + LOG_PATH + cpld_update_stress_log + '.log')

    return dLibObj.flash_update_cpld(var_dev, var_cpld_type, var_toolName, var_check_pattern, var_downgrade_cpld_image,
                                    var_upgrade_cpld_image, var_downgrade_ver, var_upgrade_ver, var_img_path, var_tool_path, var_log_file)


def flash_update_scm_cpld_fw():
    Log_Debug("Entering procedure flash_update_scm_cpld_fw.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_dev = 'cpld'
    var_cpld_type = 'scm'
    var_toolName = scm_cpld_tool
    var_check_pattern = cpld_update_pattern
    var_downgrade_cpld_image = get_old_sub_image_name('CPLD', 'scm')
    var_upgrade_cpld_image = get_new_sub_image_name('CPLD', 'scm')
    var_downgrade_ver = get_old_sub_image_version('CPLD', 'scm')
    var_upgrade_ver = get_new_sub_image_version('CPLD', 'scm')
    var_img_path = get_local_image_path('CPLD')
    var_tool_path = SPI_UTIL_PATH
    var_log_file = (pwdPath + '/' + LOG_PATH + cpld_update_stress_log + '.log')

    return dLibObj.flash_update_cpld(var_dev, var_cpld_type, var_toolName, var_check_pattern, var_downgrade_cpld_image,
                                    var_upgrade_cpld_image, var_downgrade_ver, var_upgrade_ver, var_img_path, var_tool_path, var_log_file)


def verify_cpld_versions_after_update():
    Log_Debug("Entering procedure verify_cpld_versions_after_update.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cpld_version_tool
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.verify_cpld_versions_after_flash_update(var_toolName, var_tool_path)


def verify_cpld_versions_after_power_cycle():
    Log_Debug("Entering procedure verify_cpld_versions_after_power_cycle.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cpld_version_tool
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.verify_cpld_versions_after_pwr_cycle(var_toolName, var_tool_path)


def backup_cpld_update_stress_log():
    Log_Debug("Entering procedure backup_cpld_update_stress_log.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_log_file = (cpld_update_stress_log + '.log')
    var_prefix = (cpld_update_stress_log + '-')
    var_src_path = (pwdPath + '/' + LOG_PATH)
    var_dest_path = SYSTEM_CONSOLE_LOG_PATH
    var_file_list = []

    backupFilename = dLibObj.check_local_log_file(var_log_file, var_prefix, True, var_src_path, var_dest_path)
    if backupFilename != 'None':
        var_file_list.append(backupFilename)
        return backup_log_file(var_file_list, var_src_path, var_dest_path, openbmc_mode)
    else:
        return 'None'


def set_openbmc_update_cycles(max_loop_count):
    Log_Debug("Entering procedure set_openbmc_update_cycles.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_max_openbmc_update_cycles(max_loop_count)


def set_cpld_update_cycles(max_loop_count):
    Log_Debug("Entering procedure set_cpld_update_cycles.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_max_cpld_update_cycles(max_loop_count)


def copy_fpga_files():
    Log_Debug("Entering procedure copy_fpga_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = get_server_dhcp_or_static_ip(scp_ipv6, scp_static_ipv6)
    var_filelist = get_image_list('FPGA')
    var_filepath = get_host_image_path('FPGA')
    var_destination_path = get_local_image_path('FPGA')
    var_mode = openbmc_mode
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def set_fpga_update_cycles(max_loop_count):
    Log_Debug("Entering procedure set_fpga_update_cycles.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_max_fpga_update_cycles(max_loop_count)


def read_cpld_fpga_bic_fpga_pcie_fw_versions():
    Log_Debug("Entering procedure read_cpld_fpga_bic_fpga_pcie_fw_versions.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_inputArray = wedge400c_get_cpld_fpga_bic_version_array()
    var_toolName = fw_util_tool
    var_dev = "all"
    var_option = "--version"
    var_tool_path = FW_UTIL_PATH
    var_log_File = (pwdPath + '/' + LOG_PATH + openbmc_uart_log + '.log')

    dLibObj.read_cpld_fpga_bic_fw_versions(var_toolName, var_dev, var_option, var_tool_path, var_log_File)

    var_toolName1 = fpga1_list_cmd
    var_toolName2 = fpga2_list_cmd

    dLibObj.read_fpga_pcie_fw_versions(var_toolName1, var_toolName2, var_log_File)

    return True


def flash_update_fpga1_fw():
    Log_Debug("Entering procedure flash_update_fpga1_fw.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_toolName = spiUtil_tool
    var_opt = "write"
    var_spiNum = "spi1"
    var_dev = "DOM_FPGA_FLASH1"
    var_check_pattern = spiUtil_write_pattern
    var_downgrade_fpga_image = get_old_image_name('FPGA')
    var_upgrade_fpga_image = get_new_image_name('FPGA')
    var_downgrade_ver = get_old_sub_image_version('FPGA', 'DOMFPGA1')
    var_upgrade_ver = get_new_sub_image_version('FPGA', 'DOMFPGA1')
    var_img_path = get_local_image_path('FPGA')
    var_tool_path = SPI_UTIL_PATH
    var_log_file = (pwdPath + '/' + LOG_PATH + fpga_update_stress_log + '.log')

    return dLibObj.flash_update_fpga_firmware(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_downgrade_fpga_image, var_upgrade_fpga_image,
                                              var_downgrade_ver, var_upgrade_ver, var_img_path, var_tool_path, var_log_file)


def flash_update_fpga2_fw():
    Log_Debug("Entering procedure flash_update_fpga2_fw.\n")
    dLibObj = getDiagLibObj()

    pwdPath = dLibObj.get_pwd()
    var_toolName = spiUtil_tool
    var_opt = "write"
    var_spiNum = "spi1"
    var_dev = "DOM_FPGA_FLASH2"
    var_check_pattern = spiUtil_write_pattern
    var_downgrade_fpga_image = get_old_image_name('FPGA')
    var_upgrade_fpga_image = get_new_image_name('FPGA')
    var_downgrade_ver = get_old_sub_image_version('FPGA', 'DOMFPGA2')
    var_upgrade_ver = get_new_sub_image_version('FPGA', 'DOMFPGA2')
    var_img_path = get_local_image_path('FPGA')
    var_tool_path = SPI_UTIL_PATH
    var_log_file = (pwdPath + '/' + LOG_PATH + fpga_update_stress_log + '.log')

    return dLibObj.flash_update_fpga_firmware(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_downgrade_fpga_image, var_upgrade_fpga_image,
                                              var_downgrade_ver, var_upgrade_ver, var_img_path, var_tool_path, var_log_file)


def verify_fpga_versions_after_update():
    Log_Debug("Entering procedure verify_fpga_versions_after_update.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fpga_software_test
    var_opt = '-v'
    var_tool_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_fpga_versions_after_flash_update(var_toolName, var_opt, var_tool_path)


def set_fpga_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_fpga_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_fpga_stress_time(stress_time)


def run_fpga_pcie_bus_stress_test():
    Log_Debug("Entering procedure run_fpga_pcie_bus_stress_test.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fpga_stress_tool
    var_stress_time = dLibObj.fpga_stress_time
    var_toolPath = FPGA_STRESS_TOOL_PATH

    return dLibObj.perform_fpga_pcie_bus_stress_test(var_toolName, var_stress_time, var_toolPath)


def set_ipmi_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_ipmi_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_ipmi_stress_time(stress_time)


def set_ipmi_test_cycles(stress_cycles):
    Log_Debug("Entering procedure set_ipmi_test_cycles.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_ipmi_stress_cycles(stress_cycles)


def wedge400c_run_ipmi_command_stress_test():
    Log_Debug("Entering procedure wedge400c_run_ipmi_command_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower():
        Log_Info('Do not support minipack2 unit, skip!')
        return

    var_toolName = ipmi_toolName
    var_option = 'mc info'
    var_toolPath = IPMI_STRESS_TOOL_PATH
    var_pattern = cel_ipmitool_pattern

    return dLibObj.perform_ipmi_interface_stress_test(var_toolName, var_option, var_pattern, var_toolPath)


def set_openbmc_utility_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_openbmc_utility_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_openbmc_utility_stress_time(stress_time)


def set_openbmc_utility_test_cycles(stress_cycles):
    Log_Debug("Entering procedure set_openbmc_utility_test_cycles.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_openbmc_utility_stress_cycles(stress_cycles)


def run_openbmc_utility_stability_test():
    Log_Debug("Entering procedure run_openbmc_utility_stability_test.\n")
    dLibObj = getDiagLibObj()
    
    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower():
        Log_Info('Do not support minipack2 unit, skip!')
        return

    var_toolName1 = fw_util_tool
    var_optionStr1 = fw_util_optionStr
    var_pattern1 = cel_openbmc_util_all_version_pattern
    var_toolName2 = bic_util_tool
    var_optionStr2 = bic_util_optionStr
    var_pattern2 = cel_openbmc_util_dev_id_pattern
    var_toolPath = FW_UTIL_PATH
    var_platform = 'wedge400c_cloudripper'

    # get FW versions from SwImage
    fw_ver_array = get_latest_fw_ver_array()

    Log_Info("Latest BMC version from SwImage: [%s]" %fw_ver_array[0])
    Log_Info("Latest TPM version from SwImage: [%s]" %fw_ver_array[1])
    Log_Info("Latest FCM CPLD version from SwImage: [%s]" %fw_ver_array[2])
    Log_Info("Latest PWR CPLD version from SwImage: [%s]" %fw_ver_array[3])
    Log_Info("Latest SCM CPLD version from SwImage: [%s]" %fw_ver_array[4])
    Log_Info("Latest SMB CPLD version from SwImage: [%s]" %fw_ver_array[5])
    Log_Info("Latest FPGA1 version from SwImage: [%s]" %fw_ver_array[6])
    Log_Info("Latest FPGA2 version from SwImage: [%s]" %fw_ver_array[7])
    Log_Info("Latest BIC version from SwImage: [%s]" %fw_ver_array[8])
    Log_Info("Latest BIC BootLoader version from SwImage: [%s]" %fw_ver_array[9])
    Log_Info("Latest BIOS version from SwImage: [%s]" %fw_ver_array[10])
    Log_Info("Latest CPLD version from SwImage: [%s]" %fw_ver_array[11])
    Log_Info("Latest ME version from SwImage: [%s]" %fw_ver_array[12])
    Log_Info("Latest PVCCIN version from SwImage: [%s]" %fw_ver_array[13])
    Log_Info("Latest DDRAB version from SwImage: [%s]" %fw_ver_array[14])
    Log_Info("Latest P1V05 version from SwImage: [%s]" %fw_ver_array[15])
    Log_Info("Latest DIAG version from SwImage: [%s]" %fw_ver_array[16])
    Log_Info("Latest SDK version from SwImage: [%s]" %fw_ver_array[17])
    Log_Info("Latest DIAG OS version from SwImage: [%s]" %fw_ver_array[18])
    Log_Info("Latest PSU primary FW version from SwImage: [%s]" %fw_ver_array[19])
    Log_Info("Latest PSU secondary FW version from SwImage: [%s]" %fw_ver_array[20])

    switch_to_openbmc()

    return dLibObj.perform_openbmc_utility_stability_test(var_toolName1, var_optionStr1, var_pattern1, var_toolName2, var_optionStr2, var_pattern2, var_toolPath, fw_ver_array, var_platform)


def set_nvme_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_nvme_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_nvme_stress_time(stress_time)


def run_nvme_access_stress_test():
    Log_Debug("Entering procedure run_nvme_access_stress_test.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_nvme_stress_tool
    var_option = '-filename=./SSD_SPACE -direct=1 -iodepth=16 -thread -rw=randrw -ioengine=psync -bs=4k -size=1g -numjob=4 -time_based -runtim=5m -group_reporting -name=rw”'
    var_stress_time = dLibObj.nvme_stress_time
    var_toolPath = UTILITY_TOOL_PATH
    var_pattern = cel_nvme_pattern
    var_toolName1 = cel_nvme_smart_cmd
    if "minipack3" in devicename.lower()  or  "minerva" in devicename.lower():
        var_pattern1=minipack3_cel_nvme_smart_pattern
    else:
        var_pattern1 = cel_nvme_smart_pattern
    var_option1 = 'smart-log /dev/nvme0'

    return dLibObj.perform_nvme_access_stress_test(var_toolName, var_option, var_toolName1, var_option1, var_stress_time, var_toolPath, var_pattern, var_pattern1)


def set_eeprom_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_eeprom_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_eeprom_stress_time(stress_time)

@logThis
def meta_run_eeprom_access_stress_test():
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower():
        Log_Info('Do not support minipack2 unit, skip!')
        return
    # initialize the ports if not yet initialized
    #wedge400c_init_and_check_all_eloop_modules_presence()

    var_initTool = SDK_TOOL
    var_initOption = '-c init'
    var_initToolPath = get_common_system_sdk_path()
    var_resetTool = cel_qsfp_tool
    var_resetOption1 = '-port=0 --reset=on'
    var_resetOption2 = '-port=0 --reset=off'
    var_resetToolPath = DIAG_TOOL_PATH
    var_toolName = cel_eeprom_stress_tool
    var_option = '10 58 2970 3630 10'
    var_toolPath = UTILITY_TOOL_PATH
    var_pattern = ''

    return dLibObj.perform_eeprom_access_stress_test(var_initTool, var_initOption, var_initToolPath, var_resetTool, var_resetOption1, var_resetOption2, var_resetToolPath, var_toolName, var_option, var_toolPath, var_pattern)


@logThis
def wedge400c_run_eeprom_access_stress_test():
    dLibObj = getDiagLibObj()

    # initialize the ports if not yet initialized
    #wedge400c_init_and_check_all_eloop_modules_presence()

    var_initTool = SDK_TOOL
    var_initOption = '-c init'
    var_initToolPath = get_common_system_sdk_path()
    var_resetTool = cel_qsfp_tool
    var_resetOption1 = '-port=0 --reset=on'
    var_resetOption2 = '-port=0 --reset=off'
    var_resetToolPath = DIAG_TOOL_PATH
    var_toolName = cel_eeprom_stress_tool
    var_option = '10 58 2970 3630 1'
    var_toolPath = UTILITY_TOOL_PATH
    var_pattern = ''

    return dLibObj.perform_eeprom_access_stress_test(var_initTool, var_initOption, var_initToolPath, var_resetTool, var_resetOption1, var_resetOption2, var_resetToolPath, var_toolName, var_option, var_toolPath, var_pattern)


def set_bmc_cpu_link_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_bmc_cpu_link_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_bmc_cpu_link_stress_time(stress_time)


def run_bmc_cpu_oob_link_access_stress_test():
    Log_Debug("Entering procedure run_bmc_cpu_oob_link_access_stress_test.\n")
    dLibObj = getDiagLibObj()

    var_username = dLibObj.wpl_get_bmc_username()
    var_password = dLibObj.wpl_get_bmc_password()
    var_fileName = 'testFile1g.bin'
    var_filePath = '/tmp'
    # 1GB
    var_fileSize = 1000
    var_destPath = FW_IMG_PATH
    var_interface = centos_eth_params['interface']

    ip_list = get_dut_ipv6_addresses('eth', scp_ipv6, scp_static_ipv6)
    var_centos_ipAddr = ip_list[0]
    var_openbmc_ipAddr = ip_list[1]

    return dLibObj.start_bmc_cpu_network_link_stress_test(var_username, var_password, var_fileName, var_filePath, var_fileSize, var_destPath, var_openbmc_ipAddr, var_centos_ipAddr, var_interface)


def set_internal_usb_network_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_internal_usb_network_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_internal_usb_network_stress_time(stress_time)


def run_bmc_cpu_internal_usb_network_stress_test():
    Log_Debug("Entering procedure run_bmc_cpu_internal_usb_network_stress_test.\n")
    dLibObj = getDiagLibObj()

    var_username = dLibObj.wpl_get_bmc_username()
    var_password = dLibObj.wpl_get_bmc_password()
    var_fileName = 'testFile1g.bin'
    var_filePath = '/tmp'
    # 1GB
    var_fileSize = 1000
    var_destPath = FW_IMG_PATH
    var_interface = centos_eth_params['usb_interface']

    ip_list = get_dut_ipv6_addresses('usb', scp_ipv6, scp_static_ipv6, False)
    var_centos_ipAddr = ip_list[0]
    var_openbmc_ipAddr = ip_list[1]

    return dLibObj.start_bmc_cpu_network_link_stress_test(var_username, var_password, var_fileName, var_filePath, var_fileSize, var_destPath, var_openbmc_ipAddr, var_centos_ipAddr, var_interface)


def set_openbmc_memory_test_cycles(stress_cycles):
    Log_Debug("Entering procedure set_openbmc_memory_test_cycles.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_openbmc_memory_stress_cycles(stress_cycles)


def set_openbmc_memory_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_openbmc_memory_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_openbmc_memory_stress_time(stress_time)

def run_openbmc_memory_stress_test(param=''):
    Log_Debug("Entering procedure run_openbmc_memory_stress_test.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_memtest_stress_tool
    var_option = param
    if 'minipack3' or 'th5' in devicename.lower():
        var_toolPath = workspace_sys+'/MEM_TEST'
    else:
        var_toolPath = BMC_COMMON_TOOL_PATH
    var_stress_cycles = dLibObj.openbmc_memory_stress_cycles
    var_pattern = cel_openmbc_memtest_pattern

    return dLibObj.perform_openbmc_memory_stress_test(var_toolName, var_option, var_toolPath, var_stress_cycles, var_pattern)


def set_i2c_scan_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_i2c_scan_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_i2c_scan_stress_time(stress_time)

def w400_mp_copy_i2c_config_files():
    Log_Debug("Entering procedure w400_mp_copy_i2c_config_files.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'wedge400_mp' in devicename.lower():
        var_username = scp_username
        var_password = scp_password
        var_server_ip = scp_ip
        var_filelist = i2c_config_file_list
        var_filepath = DOWNLOADABLE_DIR_WEDGE400
        var_destination_path = BMC_DIAG_CONFIG_PATH
        var_mode = openbmc_mode
        #get_dhcp_ipv6_addresses('eth')
        var_interface = openbmc_eth_params['interface']

        output = 0
        output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, False, var_interface, DEFAULT_SCP_TIME)

def wedge400c_run_openbmc_i2c_scan_stress_test():
    Log_Debug("Entering procedure  wedge400c_run_openbmc_i2c_scan_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower() or 'wedge400_' in devicename.lower():
        Log_Info('Do not support mp2 and w400 unit, skip!')
        return

    var_toolName = cel_i2c_scan_stress_tool
    var_optionList = cel_openmbc_i2c_option_list
    var_keyList = cel_openmbc_i2c_key_list
    var_stress_time = dLibObj.i2c_scan_stress_time
    var_toolPath = BMC_DIAG_TOOL_PATH
    var_patternList = cel_openmbc_i2c_pattern_list
    var_platform = 'wedge400c'

    return dLibObj.perform_i2c_scan_stress_test(var_toolName, var_optionList, var_keyList, var_stress_time, var_toolPath, var_patternList, var_platform)

def wedge400_run_openbmc_i2c_scan_stress_test():
    Log_Debug("Entering procedure  wedge400_run_openbmc_i2c_scan_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower() or 'wedge400c' in devicename.lower():
        Log_Info('Do not support mp2 and w400c unit, skip!')
        return

    var_toolName = cel_i2c_scan_stress_tool
    var_optionList = cel_openmbc_i2c_option_list
    var_keyList = cel_openmbc_i2c_key_list
    var_stress_time = dLibObj.i2c_scan_stress_time
    var_toolPath = BMC_DIAG_TOOL_PATH
    var_patternList = cel_openmbc_i2c_pattern_list
    var_platform = 'wedge400'

    return dLibObj.perform_i2c_scan_stress_test(var_toolName, var_optionList, var_keyList, var_stress_time, var_toolPath, var_patternList, var_platform)

def set_tpm_access_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_tpm_access_tress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_tpm_access_stress_time(stress_time)


def set_tpm_access_test_cycles(stress_cycles):
    Log_Debug("Entering procedure set_tpm_access_test_cycles.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_tpm_access_stress_cycles(stress_cycles)


def run_tpm_access_stress_test():
    Log_Debug("Entering procedure run_tpm_access_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower():
        Log_Info('Do not support mp2, skip!')
        return

    var_toolName = cel_tpm_stress_tool
    #var_verifyToolName = cel_eltt2_stress_tool
    var_verifyToolName = ''
    var_option = '-a'
    #var_verifyOption = '-R'
    var_verifyOption = ''
    var_stress_time = dLibObj.tpm_access_stress_time
    var_toolPath = DIAG_TOOL_PATH
    #var_verifyToolPath = UTILITY_TOOL_PATH
    var_verifyToolPath = ''
    var_pattern = cel_tpm_status_pattern

    return dLibObj.perform_tpm_access_stress_test(var_toolName, var_verifyToolName, var_option, var_verifyOption, var_stress_time, var_toolPath, var_verifyToolPath, var_pattern)


def set_serdes_stability_test_cycles(max_loop_count):
    Log_Debug("Entering procedure set_serdes_stability_test_cycles.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_serdes_stability_max_cycles(max_loop_count)


def check_cpu_and_openbmc_ipv6_interface():
    Log_Debug("Entering procedure check_cpu_and_openbmc_ipv6_interface.\n")
    dLibObj = getDiagLibObj()

    # make sure dhcp or static ipv6 available
    ipList = get_dut_ipv6_addresses('eth', scp_ipv6, scp_static_ipv6)
    if ipList is None:
        dLibObj.wpl_raiseException('Error: Unable to get DUT IPV6 addresses.')

    if re.search(':', scp_ipv6):
        slist = scp_ipv6.split(':')
        preferred_network = slist[0]
    else:
        dLibObj.wpl_raiseException('Error: Unable to get server dhcp IPV6 address.')

    var_centos_ipAddr = ipList[0]
    centos_slist = var_centos_ipAddr.split(':')
    centos_network = centos_slist[0]

    var_openbmc_ipAddr = ipList[1]
    openbmc_slist = var_openbmc_ipAddr.split(':')
    openbmc_network = openbmc_slist[0]

    if (centos_network == preferred_network) and (openbmc_network == preferred_network):
        Log_Info('Using server dhcp IPV6 address: [%s]' %scp_ipv6)
        var_server_ipAddr = scp_ipv6
    else:
        if re.search(':', scp_static_ipv6):
            Log_Info('Using server static IPV6 address: [%s]' %scp_static_ipv6)
            var_server_ipAddr = scp_static_ipv6
        else:
            dLibObj.wpl_raiseException('Error: Unable to get server static IPV6 address.')

    switch_to_centos()

    time.sleep(2)

    var_interface = centos_eth_params['interface']
    ping_ipv6_address(var_interface, var_openbmc_ipAddr, 'centos')

    time.sleep(2)

    ping_ipv6_address(var_interface, var_server_ipAddr, 'centos')

    switch_to_openbmc()

    time.sleep(2)

    var_interface = openbmc_eth_params['interface']
    ping_ipv6_address(var_interface, var_server_ipAddr, 'openbmc')


def check_usb_disk_presence():
    Log_Debug("Entering procedure check_usb_disk_presence.\n")
    dLibObj = getDiagLibObj()

    var_toolName = FDISK_UTIL
    var_option = "-l"

    return dLibObj.detect_usb_disk(var_toolName, var_option)


def wedge400c_read_current_fw_sw_util_versions():
    Log_Debug("Entering procedure wedge400c_read_current_fw_sw_util_versions.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_option = "all --version"
    var_tool_path = FW_UTIL_PATH
    var_toolName1 = fpga_software_test
    var_option1 = "-v"
    var_tool_path1 = BMC_DIAG_TOOL_PATH
    var_platform = 'wedge400c'

    return dLibObj.platform_read_fw_sw_util_versions(var_toolName, var_option, var_tool_path, var_toolName1, var_option1, var_tool_path1, var_platform)


def platform_read_current_sdk_version():
    Log_Debug("Entering procedure platform_read_current_sdk_version.\n")
    dLibObj = getDiagLibObj()

    var_sdkTool = SDK_TOOL
    var_sdkOptions = '-c version'
    var_toolPath = get_common_system_sdk_path()

    return dLibObj.platform_get_current_sdk_version(var_sdkTool, var_sdkOptions, var_toolPath)


def read_current_sdk_version():
    Log_Debug("Entering procedure read_current_sdk_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_cpu_bios_ver_bin
    var_opt = "--show"
    var_tool_path = DIAG_TOOL_PATH

    return dLibObj.minipack2_get_current_sdk_version(var_toolName, var_opt, var_tool_path)


def read_current_diagOS_version():
    Log_Debug("Entering procedure read_current_diagOS_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_cpu_bios_ver_bin
    var_opt = "--show"
    var_tool_path = DIAG_TOOL_PATH

    return dLibObj.get_current_diagos_version(var_toolName, var_opt, var_tool_path)


def read_current_psu_fw_versions(max_psu):
    Log_Debug("Entering procedure read_current_psu_fw_versions.\n")
    dLibObj = getDiagLibObj()

    var_toolName = PSU_UTIL
    var_max_psu = max_psu
    var_opt = "--get_psu_info"
    var_tool_path = BMC_DIAG_UTILITY_PATH

    return dLibObj.get_current_psu_fw_versions(var_toolName, var_max_psu, var_opt, var_tool_path)


def wedge400c_check_all_system_sw_fw_versions():
    Log_Debug("Entering procedure wedge400c_check_all_system_sw_fw_versions.\n")
    dLibObj = getDiagLibObj()

    fw_name_list = []
    current_fw_list = []
    fw_ver_array = []
    ERR_COUNT = 0

    fw_name_list.append("BMC")
    fw_name_list.append("TPM")
    fw_name_list.append("FCM_CPLD")
    fw_name_list.append("PWR_CPLD")
    fw_name_list.append("SCM_CPLD")
    fw_name_list.append("SMB_CPLD")
    fw_name_list.append("FPGA1")
    fw_name_list.append("FPGA2")
    fw_name_list.append("BIC")
    fw_name_list.append("BIC_BOOTLOADER")
    fw_name_list.append("BIOS")
    fw_name_list.append("CPLD")
    fw_name_list.append("ME")
    fw_name_list.append("PVCCIN")
    fw_name_list.append("DDRAB")
    fw_name_list.append("P1V05")
    fw_name_list.append("DIAG")
    fw_name_list.append("SDK")
    fw_name_list.append("DIAG_OS")
    fw_name_list.append("PSU_PRI")
    fw_name_list.append("PSU_SEC")

    switch_to_openbmc()

    # get FW versions from SwImage
    fw_ver_array = get_latest_fw_ver_array()

    Log_Info("Latest BMC version from SwImage: [%s]" %fw_ver_array[0])
    Log_Info("Latest TPM version from SwImage: [%s]" %fw_ver_array[1])
    Log_Info("Latest FCM CPLD version from SwImage: [%s]" %fw_ver_array[2])
    Log_Info("Latest PWR CPLD version from SwImage: [%s]" %fw_ver_array[3])
    Log_Info("Latest SCM CPLD version from SwImage: [%s]" %fw_ver_array[4])
    Log_Info("Latest SMB CPLD version from SwImage: [%s]" %fw_ver_array[5])
    Log_Info("Latest FPGA1 version from SwImage: [%s]" %fw_ver_array[6])
    Log_Info("Latest FPGA2 version from SwImage: [%s]" %fw_ver_array[7])
    Log_Info("Latest BIC version from SwImage: [%s]" %fw_ver_array[8])
    Log_Info("Latest BIC BootLoader version from SwImage: [%s]" %fw_ver_array[9])
    Log_Info("Latest BIOS version from SwImage: [%s]" %fw_ver_array[10])
    Log_Info("Latest CPLD version from SwImage: [%s]" %fw_ver_array[11])
    Log_Info("Latest ME version from SwImage: [%s]" %fw_ver_array[12])
    Log_Info("Latest PVCCIN version from SwImage: [%s]" %fw_ver_array[13])
    Log_Info("Latest DDRAB version from SwImage: [%s]" %fw_ver_array[14])
    Log_Info("Latest P1V05 version from SwImage: [%s]" %fw_ver_array[15])
    Log_Info("Latest DIAG version from SwImage: [%s]" %fw_ver_array[16])
    Log_Info("Latest SDK version from SwImage: [%s]" %fw_ver_array[17])
    Log_Info("Latest DIAG OS version from SwImage: [%s]" %fw_ver_array[18])
    if dLibObj.pwr_supply_type == 'psu':
        Log_Info("Latest PSU primary FW version from SwImage: [%s]" %fw_ver_array[19])
        Log_Info("Latest PSU secondary FW version from SwImage: [%s]" %fw_ver_array[20])

    # read current FW versions
    fw_list = wedge400c_read_current_fw_sw_util_versions()

    current_fw_list.append(fw_list[0])    # BMC
    current_fw_list.append(fw_list[1])    # TPM
    current_fw_list.append(fw_list[2])    # FCM CPLD
    current_fw_list.append(fw_list[3])    # PWR CPLD
    current_fw_list.append(fw_list[4])    # SCM CPLD
    current_fw_list.append(fw_list[5])    # SMB CPLD
    current_fw_list.append(fw_list[6])    # FPGA1
    current_fw_list.append(fw_list[7])    # FPGA2
    current_fw_list.append(fw_list[8])    # BIC
    current_fw_list.append(fw_list[9])    # BIC BOOTLOADER
    current_fw_list.append(fw_list[10])   # BIOS
    current_fw_list.append(fw_list[11])   # CPLD
    current_fw_list.append(fw_list[12])   # ME
    current_fw_list.append(fw_list[13])   # PVCCIN
    current_fw_list.append(fw_list[14])   # DDRAB
    current_fw_list.append(fw_list[15])   # P1V05
    current_fw_list.append(fw_list[16])   # DIAG

    Log_Debug("Current BMC version: [%s]" %current_fw_list[0])
    Log_Debug("Current TPM version: [%s]" %current_fw_list[1])
    Log_Debug("Current FCM CPLD version: [%s]" %current_fw_list[2])
    Log_Debug("Current PWR CPLD version: [%s]" %current_fw_list[3])
    Log_Debug("Current SCM CPLD version: [%s]" %current_fw_list[4])
    Log_Debug("Current SMB CPLD version: [%s]" %current_fw_list[5])
    Log_Debug("Current FPGA1 version: [%s]" %current_fw_list[6])
    Log_Debug("Current FPGA2 version: [%s]" %current_fw_list[7])
    Log_Debug("Current BIC version: [%s]" %current_fw_list[8])
    Log_Debug("Current BIC BOOTLOADERversion: [%s]" %current_fw_list[9])
    Log_Debug("Current BIOS version: [%s]" %current_fw_list[10])
    Log_Debug("Current CPLD version: [%s]" %current_fw_list[11])
    Log_Debug("Current ME version: [%s]" %current_fw_list[12])
    Log_Debug("Current PVCCIN version: [%s]" %current_fw_list[13])
    Log_Debug("Current DDRAB version: [%s]" %current_fw_list[14])
    Log_Debug("Current P1V05 version: [%s]" %current_fw_list[15])
    Log_Debug("Current DIAG version: [%s]" %current_fw_list[16])

    # currently there's no way to get PEM fw versions, only can get psu fw versions
    if dLibObj.pwr_supply_type == 'psu':
        # get PSU primary and secondary FW versions for each psu
        psu_fw_ver_array = read_current_psu_fw_versions(2)
        if psu_fw_ver_array[0] != fw_ver_array[19]:
            Log_Fail("Detected current PSU1 primary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[0], fw_ver_array[19]))
            dLibObj.wpl_raiseException('Failed wedge400c_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU1 primary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[0], fw_ver_array[19]))

        if psu_fw_ver_array[1] != fw_ver_array[20]:
            Log_Fail("Detected current PSU1 secondary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[1], fw_ver_array[20]))
            dLibObj.wpl_raiseException('Failed wedge400c_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU1 secondary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[1], fw_ver_array[20]))

        if psu_fw_ver_array[2] != fw_ver_array[19]:
            Log_Fail("Detected current PSU2 primary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[2], fw_ver_array[19]))
            dLibObj.wpl_raiseException('Failed wedge400c_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU2 primary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[2], fw_ver_array[19]))

        if psu_fw_ver_array[3] != fw_ver_array[20]:
            Log_Fail("Detected current PSU2 secondary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[3], fw_ver_array[20]))
            dLibObj.wpl_raiseException('Failed wedge400c_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU2 secondary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[3], fw_ver_array[20]))

    switch_to_centos()

    sdk_ver = platform_read_current_sdk_version()
    current_fw_list.append(sdk_ver)
    Log_Info("Current SDK version: [%s]" %current_fw_list[17])

    diagos_ver = read_current_diagOS_version()
    current_fw_list.append(diagos_ver)
    Log_Info("Current DIAG OS version: [%s]" %current_fw_list[18])

    for i in range(0, 19):
        if current_fw_list[i] != fw_ver_array[i]:
            ERR_COUNT += 1
            Log_Fail("Detected current %s version[%s] does not match expected version[%s]" %(fw_name_list[i], current_fw_list[i], fw_ver_array[i]))
        else:
            Log_Info("Current %s version[%s] matched expected version[%s]: PASSED" %(fw_name_list[i], current_fw_list[i], fw_ver_array[i]))

    if ERR_COUNT == 0:
        Log_Info('Checked all current FW versions matched expected FW versions.')
        Log_Success("wedge400c_check_all_system_sw_fw_versions result: PASSED.")
    else:
        dLibObj.wpl_raiseException('Failed wedge400c_check_all_system_sw_fw_versions.')

    return ERR_COUNT


def wedge400c_init_and_check_all_eloop_modules_presence():
    Log_Debug("Entering procedure wedge400c_init_and_check_all_eloop_modules_presence.\n")
    dLibObj = getDiagLibObj()

    var_initTool = SDK_TOOL
    var_initOption = '-c l2_cpu -d 60 -p dd_8x50g_qsfp_4x50g'
    var_initToolPath = get_common_system_sdk_path()
    var_resetTool = cel_qsfp_tool
    var_resetOption1 = '-port=0 --lpmode=off'
    var_resetOption2 = '-port=0 --reset=on'
    var_resetOption3 = '-port=0 --reset=off'
    var_resetToolPath = DIAG_TOOL_PATH
    var_force_reInit_sdk = False

    return dLibObj.wedge400c_perform_detect_all_eloop_modules(var_initTool, var_initOption, var_initToolPath, var_resetTool, var_resetOption1, var_resetOption2, var_resetOption3, var_resetToolPath, var_force_reInit_sdk)


def remove_all_cpu_logs():
    Log_Debug("Entering procedure remove_all_cpu_logs.\n")
    dLibObj = getDiagLibObj()

    var_mode = 'centos'

    return dLibObj.remove_all_system_log_files(var_mode)


def check_all_cpu_test_tools_and_fw_version():
    Log_Debug("Entering procedure check_all_cpu_test_tools.\n")
    dLibObj = getDiagLibObj()

    var_toolPath1 = DIAG_TOOL_PATH
    var_toolPath2 = UTILITY_TOOL_PATH
    var_mode = 'centos'

    return dLibObj.check_all_test_tools_exist(var_toolPath1, var_toolPath2, var_mode)


def check_emmc_available_space():
    Log_Debug("Entering procedure check_emmc_available_space.\n")
    dLibObj = getDiagLibObj()

    var_toolName = DISK_INFO_UTIL
    var_toolPath = '/mnt/data1'
    var_pattern = EMMC_DISK_INFO_PATTERN
    var_mode = 'openbmc'

    return dLibObj.check_available_storage_space(var_toolName, var_toolPath, var_pattern, var_mode)


def check_dev_ttyusb0():
    Log_Debug("Entering procedure check_dev_ttyusb0.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower():
        Log_Info('Do not support mp2 unit, skip!')
        return

    var_toolName = DEV_USB0_INFO_UTIL
    var_toolPath = '/mnt/data1'
    var_pattern = ''
    var_mode = 'openbmc'

    return dLibObj.check_ttyusb0_mounted(var_toolName, var_toolPath, var_pattern, var_mode)


def wedge400c_check_pem_psu_connection():
    Log_Debug("Entering procedure check_pem_psu_connection.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower():
        Log_Info('Do not support mp2 unit, skip!')
        return

    var_toolName1 = PEM_TEST_UTIL
    var_toolName2 = PSU_TEST_UTIL
    var_toolPath = BMC_DIAG_TOOL_PATH
    var_mode = 'openbmc'
    var_pattern = ''

    return dLibObj.check_system_pem_psu_slot_connection(var_toolName1, var_toolName2, var_toolPath, var_mode, var_pattern)


### FW image related functions ###
def get_image_object(image_type):
    dLibObj = getDiagLibObj()
    #imageObj = SwImage.getSwImage(image_type)

    if image_type == 'BMC':
        imageObj = SwImage.getSwImage('BMC')
    elif image_type == 'BIOS':
        imageObj = SwImage.getSwImage('BIOS')
    elif image_type == 'CPLD':
        imageObj = SwImage.getSwImage('CPLD')
    elif image_type == 'FPGA':
        imageObj = SwImage.getSwImage('FPGA')
    elif image_type == 'BIC':
        imageObj = SwImage.getSwImage('BIC')
    elif image_type == 'TH3':
        imageObj = SwImage.getSwImage('TH3')
    elif image_type == 'OOB':
        imageObj = SwImage.getSwImage('OOB')
    elif image_type == 'DIAG':
        imageObj = SwImage.getSwImage('DIAG')
    elif image_type == 'DIAG_OS':
        imageObj = SwImage.getSwImage('DIAG_OS')
    elif image_type == 'PSU':
        imageObj = SwImage.getSwImage('PSU')
    elif image_type == 'SDK':
        imageObj = SwImage.getSwImage('SDK')
    elif image_type == 'TPM':
        imageObj = SwImage.getSwImage('TPM')
    elif image_type == 'SCM':
        imageObj = SwImage.getSwImage('SCM')
    elif image_type == 'TH4_PCIE_FLASH':
        imageObj = SwImage.getSwImage('TH4_PCIE_FLASH')
    else:
        dLibObj.wpl_raiseException("Error: Unknown image type[%s]." %image_type)

    return imageObj


def get_image_list(image_type):
    imageObj = get_image_object(image_type)
    return imageObj.getImageList()


def get_old_image_name(image_type):
    imageObj = get_image_object(image_type)
    if (image_type == 'BMC') or (image_type == 'DIAG'):
        imageObj.getImageList()
    return imageObj.oldImage


def get_new_image_name(image_type):
    imageObj = get_image_object(image_type)
    if (image_type == 'BMC') or (image_type == 'DIAG'):
        imageObj.getImageList()
    return imageObj.newImage


def get_old_image_version(image_type):
    imageObj = get_image_object(image_type)
    if (image_type == 'BMC') or (image_type == 'DIAG'):
        imageObj.getImageList()
    return imageObj.oldVersion


def get_new_image_version(image_type):
    imageObj = get_image_object(image_type)
    if (image_type == 'BMC') or (image_type == 'DIAG'):
        imageObj.getImageList()
    return imageObj.newVersion


def get_local_image_path(image_type):
    imageObj = get_image_object(image_type)
    return imageObj.localImageDir


def get_host_image_path(image_type):
    imageObj = get_image_object(image_type)
    return imageObj.hostImageDir


def get_sub_image_list(image_type, name):
    imageObj = get_image_object(image_type)
    list = []
    oldImage = imageObj.oldImage[name]
    newImage = imageObj.newImage[name]
    list.append(oldImage)
    list.append(newImage)
    return list


def get_old_sub_image_name(image_type, name):
    imageObj = get_image_object(image_type)
    if (image_type == 'BMC') or (image_type == 'DIAG'):
        imageObj.getImageList()
    return imageObj.oldImage[name]


def get_new_sub_image_name(image_type, name):
    imageObj = get_image_object(image_type)
    if (image_type == 'BMC') or (image_type == 'DIAG'):
        imageObj.getImageList()
    return imageObj.newImage[name]


def get_old_sub_image_version(image_type, name):
    imageObj = get_image_object(image_type)
    if (image_type == 'BMC') or (image_type == 'DIAG'):
        imageObj.getImageList()
    return imageObj.oldVersion[name]


def get_new_sub_image_version(image_type, name):
    imageObj = get_image_object(image_type)
    if (image_type == 'BMC') or (image_type == 'DIAG'):
        imageObj.getImageList()
    return imageObj.newVersion[name]


def get_fw_sw_version_array():
    array = cel_fw_sw_version_array

    # replace with versions from SwImages.yaml
    array['BRIDGE_VER'] = get_new_image_version('BIC')
    array['BIOS_VER'] = get_new_image_version('BIOS')

    return array


def wedge400c_get_cpld_fpga_bic_version_array():
    array = cel_cpld_fpga_bic_version_array

    # replace with versions from SwImages.yaml
    array['FCMCPLD'] = get_new_sub_image_version('CPLD', 'fcm')
    array['PWRCPLD'] = get_new_sub_image_version('CPLD', 'pwr')
    array['SCMCPLD'] = get_new_sub_image_version('CPLD', 'scm')
    array['SMBCPLD'] = get_new_sub_image_version('CPLD', 'smb')
    array['DOMFPGA1'] = get_new_sub_image_version('FPGA', 'DOMFPGA1')
    array['DOMFPGA2'] = get_new_sub_image_version('FPGA', 'DOMFPGA2')
    array['BRIDGE_VER'] = get_new_image_version('BIC')

    return array


def wedge400c_get_cpld_version_array():
    array = cel_bmc_cpld_version_array

    # replace with versions from SwImages.yaml
    array['FCMCPLD'] = get_new_sub_image_version('CPLD', 'fcm')
    array['PWRCPLD'] = get_new_sub_image_version('CPLD', 'pwr')
    array['SCMCPLD'] = get_new_sub_image_version('CPLD', 'scm')
    array['SMBCPLD'] = get_new_sub_image_version('CPLD', 'smb')

    return array


def trim_fw_version_string(fw_ver_string):
    ver_string = fw_ver_string.strip()

    if len(ver_string) == 0:
        return '0.0'
    else:
        # trim off first character if it is 'v'
        if (ver_string[0] == 'v') or (ver_string[0] == 'V'):
            tmp_ver_string = ver_string[1:]
        else:
            tmp_ver_string = ver_string

        if len(tmp_ver_string) >= 4:
            if re.search(r'^0\.[\d]+', tmp_ver_string):
                vstr = tmp_ver_string
                vlist = vstr.split('.')
                if len(vlist) == 2:
                    # remove trailing decimal point zeros
                    tmp_ver = float(tmp_ver_string)
                    tmp_ver_string = str(tmp_ver)
        return tmp_ver_string

def run_sensor_option_u_and_verify_GB_run_test():
    Log_Debug("Entering procedure run_sensor_option_u_and_verify_GB_run_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400c' in devicename.lower():
        switch_to_centos()
    elif 'minipack2' in devicename.lower():
        Log_Info('Do not support mp2 unit, skip!')
        return
    
    var_toolName = 'python3 auto_load_user.py'
    var_option = '-c all --run_case 1'
    var_pass_message = COMMON_SDK_PROMPT
    var_pattern = sensor_u_pattern
    var_path = SYSTEM_SDK_PATH

    return dLibObj.test_GB_run_with_sensor_test(var_toolName, var_option, var_pass_message, var_pattern,var_path)

def exit_sdk_mode():
    Log_Debug("Entering procedure exit_sdk_mode\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower() or 'wedge400' in devicename.lower():
        Log_Info('Do not support mp2 and w400 unit, skip!')
        return

    return dLibObj.exit_sdk_mode_for_sensor_test()

def get_latest_fw_ver_array():
    Log_Debug("Entering procedure get_latest_fw_ver_array.\n")
    fw_ver_array = []

    bmcVer = get_new_image_version('BMC')
    bmc_ver = str(bmcVer)
    sw_bmc_ver = trim_fw_version_string(bmc_ver)
    fw_ver_array.append(sw_bmc_ver)

    tpmVer = get_new_image_version('TPM')
    tpm_ver = str(tpmVer)
    sw_tpm_ver = trim_fw_version_string(tpm_ver)
    fw_ver_array.append(sw_tpm_ver)

    fcmCpldVer = get_new_sub_image_version('CPLD', 'fcm')
    fcm_cpld_ver = str(fcmCpldVer)
    sw_fcm_cpld_ver = trim_fw_version_string(fcm_cpld_ver)
    fw_ver_array.append(sw_fcm_cpld_ver)

    pwrCpldVer = get_new_sub_image_version('CPLD', 'pwr')
    pwr_cpld_ver = str(pwrCpldVer)
    sw_pwr_cpld_ver = trim_fw_version_string(pwr_cpld_ver)
    fw_ver_array.append(sw_pwr_cpld_ver)

    scmCpldVer = get_new_sub_image_version('CPLD', 'scm')
    scm_cpld_ver = str(scmCpldVer)
    sw_scm_cpld_ver = trim_fw_version_string(scm_cpld_ver)
    fw_ver_array.append(sw_scm_cpld_ver)

    smbCpldVer = get_new_sub_image_version('CPLD', 'smb')
    smb_cpld_ver = str(smbCpldVer)
    sw_smb_cpld_ver = trim_fw_version_string(smb_cpld_ver)
    fw_ver_array.append(sw_smb_cpld_ver)

    fpga1Ver = get_new_sub_image_version('FPGA', 'DOMFPGA1')
    fpga1_ver = str(fpga1Ver)
    sw_fpga1_ver = trim_fw_version_string(fpga1_ver)
    fw_ver_array.append(sw_fpga1_ver)

    fpga2Ver = get_new_sub_image_version('FPGA', 'DOMFPGA2')
    fpga2_ver = str(fpga2Ver)
    sw_fpga2_ver = trim_fw_version_string(fpga2_ver)
    fw_ver_array.append(sw_fpga2_ver)

    bridgeVer = get_new_image_version('BIC')
    bridge_ver = str(bridgeVer)
    sw_bridge_ver = trim_fw_version_string(bridge_ver)
    fw_ver_array.append(sw_bridge_ver)

    bridgeBootloaderVer = get_new_sub_image_version('SCM', 'Bridge-IC Bootloader Version')
    bridge_bootloader_ver = str(bridgeBootloaderVer)
    sw_bridge_bootloader_ver = trim_fw_version_string(bridge_bootloader_ver)
    fw_ver_array.append(sw_bridge_bootloader_ver)

    biosVer = get_new_image_version('BIOS')
    bios_ver = str(biosVer)
    sw_bios_ver = trim_fw_version_string(bios_ver)
    fw_ver_array.append(sw_bios_ver)

    cpldVer = get_new_sub_image_version('SCM', 'CPLD Version')
    cpld_ver = str(cpldVer)
    sw_cpld_ver = trim_fw_version_string(cpld_ver)
    fw_ver_array.append(sw_cpld_ver)

    meVer = get_new_sub_image_version('SCM', 'ME Version')
    me_ver = str(meVer)
    sw_me_ver = trim_fw_version_string(me_ver)
    fw_ver_array.append(sw_me_ver)

    pvccinVer = get_new_sub_image_version('SCM', 'PVCCIN VR Version')
    pvccin_ver = str(pvccinVer)
    sw_pvccin_ver = trim_fw_version_string(pvccin_ver)
    fw_ver_array.append(sw_pvccin_ver)

    ddrabVer = get_new_sub_image_version('SCM', 'DDRAB VR Version')
    ddrab_ver = str(ddrabVer)
    sw_ddrab_ver = trim_fw_version_string(ddrab_ver)
    fw_ver_array.append(sw_ddrab_ver)

    p1v05Ver = get_new_sub_image_version('SCM', 'P1V05 VR Version')
    p1v05_ver = str(p1v05Ver)
    sw_p1v05_ver = trim_fw_version_string(p1v05_ver)
    fw_ver_array.append(sw_p1v05_ver)

    diagVer = get_new_image_version('DIAG')
    diag_ver = str(diagVer)
    sw_diag_ver = trim_fw_version_string(diag_ver)
    fw_ver_array.append(sw_diag_ver)

    sdkVer = get_new_image_version('SDK')
    sdk_ver = str(sdkVer)
    sw_sdk_ver = trim_fw_version_string(sdk_ver)
    fw_ver_array.append(sw_sdk_ver)

    diagOSVer = get_new_image_version('DIAG_OS')
    diag_os_ver = str(diagOSVer)
    sw_diag_os_ver = trim_fw_version_string(diag_os_ver)
    fw_ver_array.append(sw_diag_os_ver)

    psuPrimaryVer = get_new_sub_image_version('PSU', 'PRI_FW_VER')
    psu_primary_ver = str(psuPrimaryVer)
    sw_psu_primary_ver = trim_fw_version_string(psu_primary_ver)
    fw_ver_array.append(sw_psu_primary_ver)

    psuSecondaryVer = get_new_sub_image_version('PSU', 'SEC_FW_VER')
    psu_secondary_ver = str(psuSecondaryVer)
    sw_psu_secondary_ver = trim_fw_version_string(psu_secondary_ver)
    fw_ver_array.append(sw_psu_secondary_ver)

    ### only wedge400 has TH3 ###
    #th3LoaderVer = get_new_sub_image_version('TH3', 'PCIe FW loader version')
    #th3_loader_ver = str(th3LoaderVer)
    #sw_th3_loader_ver = trim_fw_version_string(th3_loader_ver)
    #fw_ver_array.append(sw_th3_loader_ver)

    #th3Ver = get_new_sub_image_version('TH3', 'PCIe FW version')
    #th3_ver = str(th3Ver)
    #sw_th3_ver = trim_fw_version_string(th3_ver)
    #fw_ver_array.append(sw_th3_ver)

    ### currently, there's no way to read back OOB version, so no checking required ###
    #oobVer = get_new_image_version('OOB')
    #oob_ver = str(oobVer)
    #sw_oob_ver = trim_fw_version_string(oob_ver)
    #fw_ver_array.append(sw_oob_ver)

    return fw_ver_array

def cloudripper_check_all_system_sw_fw_versions():
    Log_Debug("Entering procedure cloudripper_check_all_system_sw_fw_versions.\n")
    dLibObj = getDiagLibObj()

    fw_name_list = []
    current_fw_list = []
    fw_ver_array = []
    ERR_COUNT = 0

    fw_name_list.append("BMC")
    fw_name_list.append("TPM")
    fw_name_list.append("FCM_CPLD")
    fw_name_list.append("PWR_CPLD")
    fw_name_list.append("SCM_CPLD")
    fw_name_list.append("SMB_CPLD")
    fw_name_list.append("FPGA1")
    fw_name_list.append("FPGA2")
    fw_name_list.append("BIC")
    fw_name_list.append("BIC_BOOTLOADER")
    fw_name_list.append("BIOS")
    fw_name_list.append("CPLD")
    fw_name_list.append("ME")
    fw_name_list.append("PVCCIN")
    fw_name_list.append("DDRAB")
    fw_name_list.append("P1V05")
    fw_name_list.append("DIAG")
    fw_name_list.append("SDK")
    fw_name_list.append("DIAG_OS")
    fw_name_list.append("PSU_PRI")
    fw_name_list.append("PSU_SEC")

    switch_to_openbmc()

    # get FW versions from SwImage
    fw_ver_array = cloudripper_get_latest_fw_ver_array()

    Log_Info("Latest BMC version from SwImage: [%s]" %fw_ver_array[0])
    Log_Info("Latest TPM version from SwImage: [%s]" %fw_ver_array[1])
    Log_Info("Latest FCM CPLD version from SwImage: [%s]" %fw_ver_array[2])
    Log_Info("Latest PWR CPLD version from SwImage: [%s]" %fw_ver_array[3])
    Log_Info("Latest SCM CPLD version from SwImage: [%s]" %fw_ver_array[4])
    Log_Info("Latest SMB CPLD version from SwImage: [%s]" %fw_ver_array[5])
    Log_Info("Latest FPGA1 version from SwImage: [%s]" %fw_ver_array[6])
    Log_Info("Latest FPGA2 version from SwImage: [%s]" %fw_ver_array[7])
    Log_Info("Latest BIC version from SwImage: [%s]" %fw_ver_array[8])
    Log_Info("Latest BIC BootLoader version from SwImage: [%s]" %fw_ver_array[9])
    Log_Info("Latest BIOS version from SwImage: [%s]" %fw_ver_array[10])
    Log_Info("Latest CPLD version from SwImage: [%s]" %fw_ver_array[11])
    Log_Info("Latest ME version from SwImage: [%s]" %fw_ver_array[12])
    Log_Info("Latest PVCCIN version from SwImage: [%s]" %fw_ver_array[13])
    Log_Info("Latest DDRAB version from SwImage: [%s]" %fw_ver_array[14])
    Log_Info("Latest P1V05 version from SwImage: [%s]" %fw_ver_array[15])
    Log_Info("Latest DIAG version from SwImage: [%s]" %fw_ver_array[16])
    Log_Info("Latest SDK version from SwImage: [%s]" %fw_ver_array[17])
    Log_Info("Latest DIAG OS version from SwImage: [%s]" %fw_ver_array[18])
### Disable first, currently cloudripper psu-util not ready yet ###
    #if dLibObj.pwr_supply_type == 'psu':
        #Log_Info("Latest PSU primary FW version from SwImage: [%s]" %fw_ver_array[18])
        #Log_Info("Latest PSU secondary FW version from SwImage: [%s]" %fw_ver_array[19])

    # read current FW versions
    fw_list = cloudripper_read_current_fw_sw_util_versions()

    current_fw_list.append(fw_list[0])    # BMC
    current_fw_list.append(fw_list[1])    # TPM
    current_fw_list.append(fw_list[2])    # FCM CPLD
    current_fw_list.append(fw_list[3])    # PWR CPLD
    current_fw_list.append(fw_list[4])    # SCM CPLD
    current_fw_list.append(fw_list[5])    # SMB CPLD
    current_fw_list.append(fw_list[6])    # FPGA1
    current_fw_list.append(fw_list[7])    # FPGA2
    current_fw_list.append(fw_list[8])    # BIC
    current_fw_list.append(fw_list[9])    # BIC BOOTLOADER
    current_fw_list.append(fw_list[10])   # BIOS
    current_fw_list.append(fw_list[11])   # CPLD
    current_fw_list.append(fw_list[12])   # ME
    current_fw_list.append(fw_list[13])   # PVCCIN
    current_fw_list.append(fw_list[14])   # DDRAB
    current_fw_list.append(fw_list[15])   # P1V05
    current_fw_list.append(fw_list[16])   # DIAG

    Log_Debug("Current BMC version: [%s]" %current_fw_list[0])
    Log_Debug("Current TPM version: [%s]" %current_fw_list[1])
    Log_Debug("Current FCM CPLD version: [%s]" %current_fw_list[2])
    Log_Debug("Current PWR CPLD version: [%s]" %current_fw_list[3])
    Log_Debug("Current SCM CPLD version: [%s]" %current_fw_list[4])
    Log_Debug("Current SMB CPLD version: [%s]" %current_fw_list[5])
    Log_Debug("Current FPGA1 version: [%s]" %current_fw_list[6])
    Log_Debug("Current FPGA2 version: [%s]" %current_fw_list[7])
    Log_Debug("Current BIC version: [%s]" %current_fw_list[8])
    Log_Debug("Current BIC BOOTLOADERversion: [%s]" %current_fw_list[9])
    Log_Debug("Current BIOS version: [%s]" %current_fw_list[10])
    Log_Debug("Current CPLD version: [%s]" %current_fw_list[11])
    Log_Debug("Current ME version: [%s]" %current_fw_list[12])
    Log_Debug("Current PVCCIN version: [%s]" %current_fw_list[13])
    Log_Debug("Current DDRAB version: [%s]" %current_fw_list[14])
    Log_Debug("Current P1V05 version: [%s]" %current_fw_list[15])
    Log_Debug("Current DIAG version: [%s]" %current_fw_list[16])

### Disable first, currently cloudripper psu-util not ready yet ###
    # currently there's no way to get PEM fw versions, only can get psu fw versions
#    if dLibObj.pwr_supply_type == 'psu':
#        # get PSU primary and secondary FW versions for each psu
#        psu_fw_ver_array = read_current_psu_fw_versions(2)
#        if psu_fw_ver_array[0] != fw_ver_array[19]:
#            Log_Fail("Detected current PSU1 primary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[0], fw_ver_array[19]))
#            dLibObj.wpl_raiseException('Failed cloudripper_check_all_system_sw_fw_versions.')
#        else:
#            Log_Info("Current PSU1 primary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[0], fw_ver_array[19]))
#
#        if psu_fw_ver_array[1] != fw_ver_array[20]:
#            Log_Fail("Detected current PSU1 secondary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[1], fw_ver_array[20]))
#            dLibObj.wpl_raiseException('Failed cloudripper_check_all_system_sw_fw_versions.')
#        else:
#            Log_Info("Current PSU1 secondary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[1], fw_ver_array[20]))
#
#        if psu_fw_ver_array[2] != fw_ver_array[19]:
#            Log_Fail("Detected current PSU2 primary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[2], fw_ver_array[19]))
#            dLibObj.wpl_raiseException('Failed cloudripper_check_all_system_sw_fw_versions.')
#        else:
#            Log_Info("Current PSU2 primary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[2], fw_ver_array[19]))
#
#        if psu_fw_ver_array[3] != fw_ver_array[20]:
#            Log_Fail("Detected current PSU2 secondary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[3], fw_ver_array[20]))
#            dLibObj.wpl_raiseException('Failed cloudripper_check_all_system_sw_fw_versions.')
#        else:
#            Log_Info("Current PSU2 secondary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[3], fw_ver_array[20]))

    switch_to_centos()

    sdk_ver = platform_read_current_sdk_version()
    current_fw_list.append(sdk_ver)
    Log_Info("Current SDK version: [%s]" %current_fw_list[17])

    diagos_ver = read_current_diagOS_version()
    current_fw_list.append(diagos_ver)
    Log_Info("Current DIAG OS version: [%s]" %current_fw_list[18])

    for i in range(0, 19):
        if current_fw_list[i] != fw_ver_array[i]:
            ERR_COUNT += 1
            Log_Fail("Detected current %s version[%s] does not match expected version[%s]" %(fw_name_list[i], current_fw_list[i], fw_ver_array[i]))
        else:
            Log_Info("Current %s version[%s] matched expected version[%s]: PASSED" %(fw_name_list[i], current_fw_list[i], fw_ver_array[i]))

    if ERR_COUNT == 0:
        Log_Info('Checked all current FW versions matched expected FW versions')
        Log_Success("cloudripper_check_all_system_sw_fw_versions result: PASSED.")
    else:
        dLibObj.wpl_raiseException('Failed cloudripper_check_all_system_sw_fw_versions.')

    return ERR_COUNT

def cloudripper_get_latest_fw_ver_array():
    Log_Debug("Entering procedure get_latest_fw_ver_array.\n")
    fw_ver_array = []

    bmcVer = get_new_image_version('BMC')
    bmc_ver = str(bmcVer)
    sw_bmc_ver = trim_fw_version_string(bmc_ver)


    tpmVer = get_new_image_version('TPM')
    tpm_ver = str(tpmVer)
    sw_tpm_ver = trim_fw_version_string(tpm_ver)
    fw_ver_array.append(sw_tpm_ver)

    fcmCpldVer = get_new_sub_image_version('CPLD', 'fcm')
    fcm_cpld_ver = str(fcmCpldVer)
    sw_fcm_cpld_ver = trim_fw_version_string(fcm_cpld_ver)
    fw_ver_array.append(sw_fcm_cpld_ver)

    pwrCpldVer = get_new_sub_image_version('CPLD', 'pwr')
    pwr_cpld_ver = str(pwrCpldVer)
    sw_pwr_cpld_ver = trim_fw_version_string(pwr_cpld_ver)
    fw_ver_array.append(sw_pwr_cpld_ver)

    scmCpldVer = get_new_sub_image_version('CPLD', 'scm')
    scm_cpld_ver = str(scmCpldVer)
    sw_scm_cpld_ver = trim_fw_version_string(scm_cpld_ver)
    fw_ver_array.append(sw_scm_cpld_ver)

    smbCpldVer = get_new_sub_image_version('CPLD', 'smb')
    smb_cpld_ver = str(smbCpldVer)
    sw_smb_cpld_ver = trim_fw_version_string(smb_cpld_ver)
    fw_ver_array.append(sw_smb_cpld_ver)

    fpga1Ver = get_new_sub_image_version('FPGA', 'DOMFPGA1')
    fpga1_ver = str(fpga1Ver)
    sw_fpga1_ver = trim_fw_version_string(fpga1_ver)
    fw_ver_array.append(sw_fpga1_ver)

    fpga2Ver = get_new_sub_image_version('FPGA', 'DOMFPGA2')
    fpga2_ver = str(fpga2Ver)
    sw_fpga2_ver = trim_fw_version_string(fpga2_ver)
    fw_ver_array.append(sw_fpga2_ver)

    bridgeVer = get_new_image_version('BIC')
    bridge_ver = str(bridgeVer)
    sw_bridge_ver = trim_fw_version_string(bridge_ver)
    fw_ver_array.append(sw_bridge_ver)

    bridgeBootloaderVer = get_new_sub_image_version('SCM', 'Bridge-IC Bootloader Version')
    bridge_bootloader_ver = str(bridgeBootloaderVer)
    sw_bridge_bootloader_ver = trim_fw_version_string(bridge_bootloader_ver)
    fw_ver_array.append(sw_bridge_bootloader_ver)

    biosVer = get_new_image_version('BIOS')
    bios_ver = str(biosVer)
    sw_bios_ver = trim_fw_version_string(bios_ver)
    fw_ver_array.append(sw_bios_ver)

    cpldVer = get_new_sub_image_version('SCM', 'CPLD Version')
    cpld_ver = str(cpldVer)
    sw_cpld_ver = trim_fw_version_string(cpld_ver)
    fw_ver_array.append(sw_cpld_ver)

    meVer = get_new_sub_image_version('SCM', 'ME Version')
    me_ver = str(meVer)
    sw_me_ver = trim_fw_version_string(me_ver)
    fw_ver_array.append(sw_me_ver)

    pvccinVer = get_new_sub_image_version('SCM', 'PVCCIN VR Version')
    pvccin_ver = str(pvccinVer)
    sw_pvccin_ver = trim_fw_version_string(pvccin_ver)
    fw_ver_array.append(sw_pvccin_ver)

    ddrabVer = get_new_sub_image_version('SCM', 'DDRAB VR Version')
    ddrab_ver = str(ddrabVer)
    sw_ddrab_ver = trim_fw_version_string(ddrab_ver)
    fw_ver_array.append(sw_ddrab_ver)

    p1v05Ver = get_new_sub_image_version('SCM', 'P1V05 VR Version')
    p1v05_ver = str(p1v05Ver)
    sw_p1v05_ver = trim_fw_version_string(p1v05_ver)
    fw_ver_array.append(sw_p1v05_ver)

    diagVer = get_new_image_version('DIAG')
    diag_ver = str(diagVer)
    sw_diag_ver = trim_fw_version_string(diag_ver)
    fw_ver_array.append(sw_diag_ver)

    sdkVer = get_new_image_version('SDK')
    sdk_ver = str(sdkVer)
    sw_sdk_ver = trim_fw_version_string(sdk_ver)
    fw_ver_array.append(sw_sdk_ver)

    diagOSVer = get_new_image_version('DIAG_OS')
    diag_os_ver = str(diagOSVer)
    sw_diag_os_ver = trim_fw_version_string(diag_os_ver)
    fw_ver_array.append(sw_diag_os_ver)

    psuPrimaryVer = get_new_sub_image_version('PSU', 'PRI_FW_VER')
    psu_primary_ver = str(psuPrimaryVer)
    sw_psu_primary_ver = trim_fw_version_string(psu_primary_ver)
    fw_ver_array.append(sw_psu_primary_ver)

    psuSecondaryVer = get_new_sub_image_version('PSU', 'SEC_FW_VER')
    psu_secondary_ver = str(psuSecondaryVer)
    sw_psu_secondary_ver = trim_fw_version_string(psu_secondary_ver)
    fw_ver_array.append(sw_psu_secondary_ver)

    ### only wedge400 has TH3 ###
    #th3LoaderVer = get_new_sub_image_version('TH3', 'PCIe FW loader version')
    #th3_loader_ver = str(th3LoaderVer)
    #sw_th3_loader_ver = trim_fw_version_string(th3_loader_ver)
    #fw_ver_array.append(sw_th3_loader_ver)

    #th3Ver = get_new_sub_image_version('TH3', 'PCIe FW version')
    #th3_ver = str(th3Ver)
    #sw_th3_ver = trim_fw_version_string(th3_ver)
    #fw_ver_array.append(sw_th3_ver)

    ### currently, there's no way to read back OOB version, so no checking required ###
    #oobVer = get_new_image_version('OOB')
    #oob_ver = str(oobVer)
    #sw_oob_ver = trim_fw_version_string(oob_ver)
    #fw_ver_array.append(sw_oob_ver)

    return fw_ver_array

def minipack2_get_latest_fw_ver_array():
    Log_Debug("Entering procedure minipack2_get_latest_fw_ver_array.\n")
    fw_ver_array = []

    bmcVer = get_new_image_version('BMC')
    bmc_ver_str = str(bmcVer)
    bmc_ver = bmc_ver_str

    if re.search('fuji-', bmc_ver_str, re.IGNORECASE):
        slist = bmc_ver_str.split('-')
        bmc_ver = str(slist[1])
    elif re.search('fuji_', bmc_ver_str, re.IGNORECASE):
        slist = bmc_ver_str.split('_')
        bmc_ver = str(slist[1])
    sw_bmc_ver = trim_fw_version_string(bmc_ver)
    fw_ver_array.append(sw_bmc_ver)

    tpmVer = get_new_image_version('TPM')
    tpm_ver = str(tpmVer)
    sw_tpm_ver = trim_fw_version_string(tpm_ver)
    fw_ver_array.append(sw_tpm_ver)

    fcmBCpldVer = get_new_sub_image_version('CPLD', 'FCMCPLD B')
    fcm_B_cpld_ver = str(fcmBCpldVer)
    sw_fcm_B_cpld_ver = trim_fw_version_string(fcm_B_cpld_ver)
    fw_ver_array.append(sw_fcm_B_cpld_ver)

    fcmTCpldVer = get_new_sub_image_version('CPLD', 'FCMCPLD T')
    fcm_T_cpld_ver = str(fcmTCpldVer)
    sw_fcm_T_cpld_ver = trim_fw_version_string(fcm_T_cpld_ver)
    fw_ver_array.append(sw_fcm_T_cpld_ver)

    pwrLCpldVer = get_new_sub_image_version('CPLD', 'PWRCPLD L')
    pwr_L_cpld_ver = str(pwrLCpldVer)
    sw_pwr_L_cpld_ver = trim_fw_version_string(pwr_L_cpld_ver)
    fw_ver_array.append(sw_pwr_L_cpld_ver)

    pwrRCpldVer = get_new_sub_image_version('CPLD', 'PWRCPLD R')
    pwr_R_cpld_ver = str(pwrRCpldVer)
    sw_pwr_R_cpld_ver = trim_fw_version_string(pwr_R_cpld_ver)
    fw_ver_array.append(sw_pwr_R_cpld_ver)

    scmCpldVer = get_new_sub_image_version('CPLD', 'SCMCPLD')
    scm_cpld_ver = str(scmCpldVer)
    sw_scm_cpld_ver = trim_fw_version_string(scm_cpld_ver)
    fw_ver_array.append(sw_scm_cpld_ver)

    smbCpldVer = get_new_sub_image_version('CPLD', 'SMBCPLD')
    smb_cpld_ver = str(smbCpldVer)
    sw_smb_cpld_ver = trim_fw_version_string(smb_cpld_ver)
    fw_ver_array.append(sw_smb_cpld_ver)

    iobFpgaVer = get_new_sub_image_version('FPGA', 'SMB_IOB_FPGA')
    iob_fpga_ver = str(iobFpgaVer)
    sw_iob_fpga_ver = trim_fw_version_string(iob_fpga_ver)
    fw_ver_array.append(sw_iob_fpga_ver)

    fpga1Ver = get_new_sub_image_version('FPGA', 'PIM1 DOMFPGA')
    fpga1_ver = str(fpga1Ver)
    sw_fpga1_ver = trim_fw_version_string(fpga1_ver)
    fw_ver_array.append(sw_fpga1_ver)

    fpga2Ver = get_new_sub_image_version('FPGA', 'PIM2 DOMFPGA')
    fpga2_ver = str(fpga2Ver)
    sw_fpga2_ver = trim_fw_version_string(fpga2_ver)
    fw_ver_array.append(sw_fpga2_ver)

    fpga3Ver = get_new_sub_image_version('FPGA', 'PIM3 DOMFPGA')
    fpga3_ver = str(fpga3Ver)
    sw_fpga3_ver = trim_fw_version_string(fpga3_ver)
    fw_ver_array.append(sw_fpga3_ver)

    fpga4Ver = get_new_sub_image_version('FPGA', 'PIM4 DOMFPGA')
    fpga4_ver = str(fpga4Ver)
    sw_fpga4_ver = trim_fw_version_string(fpga4_ver)
    fw_ver_array.append(sw_fpga4_ver)

    fpga5Ver = get_new_sub_image_version('FPGA', 'PIM5 DOMFPGA')
    fpga5_ver = str(fpga5Ver)
    sw_fpga5_ver = trim_fw_version_string(fpga5_ver)
    fw_ver_array.append(sw_fpga5_ver)

    fpga6Ver = get_new_sub_image_version('FPGA', 'PIM6 DOMFPGA')
    fpga6_ver = str(fpga6Ver)
    sw_fpga6_ver = trim_fw_version_string(fpga6_ver)
    fw_ver_array.append(sw_fpga6_ver)

    fpga7Ver = get_new_sub_image_version('FPGA', 'PIM7 DOMFPGA')
    fpga7_ver = str(fpga7Ver)
    sw_fpga7_ver = trim_fw_version_string(fpga7_ver)
    fw_ver_array.append(sw_fpga7_ver)

    fpga8Ver = get_new_sub_image_version('FPGA', 'PIM8 DOMFPGA')
    fpga8_ver = str(fpga8Ver)
    sw_fpga8_ver = trim_fw_version_string(fpga8_ver)
    fw_ver_array.append(sw_fpga8_ver)

    bridgeVer = get_new_image_version('BIC')
    bridge_ver = str(bridgeVer)
    sw_bridge_ver = trim_fw_version_string(bridge_ver)
    fw_ver_array.append(sw_bridge_ver)

    bridgeBootloaderVer = get_new_sub_image_version('SCM', 'Bridge-IC Bootloader Version')
    bridge_bootloader_ver = str(bridgeBootloaderVer)
    sw_bridge_bootloader_ver = trim_fw_version_string(bridge_bootloader_ver)
    fw_ver_array.append(sw_bridge_bootloader_ver)

    biosVer = get_new_image_version('BIOS')
    bios_ver = str(biosVer)
    sw_bios_ver = trim_fw_version_string(bios_ver)
    fw_ver_array.append(sw_bios_ver)

    cpldVer = get_new_sub_image_version('SCM', 'CPLD Version')
    cpld_ver = str(cpldVer)
    sw_cpld_ver = trim_fw_version_string(cpld_ver)
    fw_ver_array.append(sw_cpld_ver)

    meVer = get_new_sub_image_version('SCM', 'ME Version')
    me_ver = str(meVer)
    sw_me_ver = trim_fw_version_string(me_ver)
    fw_ver_array.append(sw_me_ver)

    pvccinVer = get_new_sub_image_version('SCM', 'PVCCIN VR Version')
    pvccin_ver = str(pvccinVer)
    sw_pvccin_ver = trim_fw_version_string(pvccin_ver)
    fw_ver_array.append(sw_pvccin_ver)

    ddrabVer = get_new_sub_image_version('SCM', 'DDRAB VR Version')
    ddrab_ver = str(ddrabVer)
    sw_ddrab_ver = trim_fw_version_string(ddrab_ver)
    fw_ver_array.append(sw_ddrab_ver)

    p1v05Ver = get_new_sub_image_version('SCM', 'P1V05 VR Version')
    p1v05_ver = str(p1v05Ver)
    sw_p1v05_ver = trim_fw_version_string(p1v05_ver)
    fw_ver_array.append(sw_p1v05_ver)

    diagVer = get_new_image_version('DIAG')
    diag_ver = str(diagVer)
    sw_diag_ver = trim_fw_version_string(diag_ver)
    fw_ver_array.append(sw_diag_ver)

    sdkVer = get_new_image_version('SDK')
    sdk_ver = str(sdkVer)
    sw_sdk_ver = trim_fw_version_string(sdk_ver)
    fw_ver_array.append(sw_sdk_ver)

    diagOSVer = get_new_image_version('DIAG_OS')
    diag_os_ver = str(diagOSVer)
    sw_diag_os_ver = trim_fw_version_string(diag_os_ver)
    fw_ver_array.append(sw_diag_os_ver)

    psuPrimaryVer = get_new_sub_image_version('PSU', 'PRI_FW_VER')
    psu_primary_ver = str(psuPrimaryVer)
    sw_psu_primary_ver = trim_fw_version_string(psu_primary_ver)
    fw_ver_array.append(sw_psu_primary_ver)

    psuSecondaryVer = get_new_sub_image_version('PSU', 'SEC_FW_VER')
    psu_secondary_ver = str(psuSecondaryVer)
    sw_psu_secondary_ver = trim_fw_version_string(psu_secondary_ver)
    fw_ver_array.append(sw_psu_secondary_ver)

    th4LoaderVer = get_new_sub_image_version('TH4_PCIE_FLASH', 'PCIe FW loader version')
    th4_loader_ver = str(th4LoaderVer)
    sw_th4_loader_ver = trim_fw_version_string(th4_loader_ver)
    fw_ver_array.append(sw_th4_loader_ver)

    th4Ver = get_new_sub_image_version('TH4_PCIE_FLASH', 'PCIe FW version')
    th4_ver = str(th4Ver)
    sw_th4_ver = trim_fw_version_string(th4_ver)
    fw_ver_array.append(sw_th4_ver)

    ### currently, there's no way to read back OOB version, so no checking required ###
    #oobVer = get_new_image_version('OOB')
    #oob_ver = str(oobVer)
    #sw_oob_ver = trim_fw_version_string(oob_ver)
    #fw_ver_array.append(sw_oob_ver)

    return fw_ver_array
###################################


def cpu_stress_test(stress_time):
    dLibObj = getDiagLibObj()
    dLibObj.cpu_stress(stress_time)


def set_cpu_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_ipmi_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_cpu_stress_time(stress_time)


def run_cpu_stress_test():
    Log_Debug("Entering procedure run_fpga_pcie_bus_stress_test.\n")
    dLibObj = getDiagLibObj()

    var_stress_time = dLibObj.cpu_stress_time

    return dLibObj.cpu_stress(var_stress_time)


def set_come_memory_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_come_memory_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_come_memory_stress_time(stress_time)


def run_come_memory_test():
    Log_Debug("Entering procedure run_come_memory_test.\n")
    dLibObj = getDiagLibObj()
    var_stress_time = dLibObj.COMe_memory_stress_time

    return dLibObj.COMe_memory_stress(var_stress_time)


def set_auto_load_script_stress_loop_time(stress_time):
    Log_Debug("Entering procedure set_auto_load_script_stress_loop_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_auto_load_script_stress_time(stress_time)


def set_sensor_reading_stress_cycles(stress_cycle):
    Log_Debug("Entering procedure set_sensor_reading_stress_cycle.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.set_sensor_reading_stress_max_cycle(stress_cycle)


def run_sdk_for_init_sensor():
    Log_Debug("Entering procedure run_sdk_for_init_sensor.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.sdk_for_init_sensor()


def wedge400c_change_to_sdk_path():
    Log_Debug("Entering procedure wedge400c_change_to_sdk_path.\n")
    path = get_common_system_sdk_path()
    CommonLib.change_dir(path)


def change_to_bmc_diag_tool_path():
    Log_Debug("Entering procedure change_to_bmc_diag_tool_path.\n")
    path = BMC_DIAG_TOOL_PATH
    CommonLib.change_dir(path)


def run_sdk_sensor_high_loading():
    Log_Debug("Entering procedure run_sdk_sensor_hight_loading.\n")
    dLibObj = getDiagLibObj()
    dLibObj.sdk_for_init_sensor_high_load()


def run_sensor_reading_high_loading_stress_test():
    Log_Debug("Entering procedure run_sensor_reading_high_loading_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400_' in devicename.lower() or 'minipack2' in devicename.lower():
        Log_Info('Do not support w400 and mp2 unit, skip!')
        return

    # initialize the ports if not yet initialized
    wedge400c_init_and_check_all_eloop_modules_presence()

    var_toolName = ('python3 ' + SDK_TOOL)
    stress_time = int(dLibObj.auto_load_script_stress_time)
    var_option = ('-c l2_cpu -d %s -p dd_8x50g_qsfp_4x50g' %stress_time)
    var_toolPath = get_common_system_sdk_path()
    var_logFile = SDK_LOG_FILE
    var_completeMsg = 'L2 snake traffic with cpu injection'
    var_passMsg = 'L2.*?PASS'
    var_sensorToolName = cel_sensor_test["bin_tool"]
    var_sensorToolOption = '-u'
    var_sensorToolPath = BMC_DIAG_TOOL_PATH
    var_testType = 'high'
    var_platform = 'wedge400c'

    dLibObj.perform_sensor_reading_loading_stress_test(var_toolName, var_option, var_toolPath, var_logFile, var_completeMsg, var_passMsg, var_sensorToolName, var_sensorToolOption, var_sensorToolPath, var_testType, var_platform)


def w400_run_sensor_reading_high_loading_stress_test():
    Log_Debug("Entering procedure w400_run_sensor_reading_high_loading_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400c' in devicename.lower() or 'minipack2' in devicename.lower():
        Log_Info('Do not support w400c and mp2 unit, skip!')
        return
    
    var_toolName = W400_SDK_TOOL
    var_stress_time = dLibObj.auto_load_script_stress_time
    var_option = '-d'
    var_toolPath = SYSTEM_SDK_PATH
    var_start_traffic_cmd = w400_start_cpu_traffic_cmd
    var_stop_traffic_cmd = w400_stop_cpu_traffic_cmd
    var_exit_traffic_cmd = w400_exit_cpu_traffic_cmd
    port_status_pattern = port_up_status
    var_sensorToolName = cel_sensor_test["bin_tool"]
    var_sensorToolOption = '-u'
    var_sensorToolPath = BMC_DIAG_TOOL_PATH
    var_testType = 'high'
    var_platform = 'wedge400'

    dLibObj.w400_perform_sensor_reading_loading_stress_test(var_toolName, var_option, var_toolPath, var_start_traffic_cmd, port_status_pattern, var_stop_traffic_cmd, var_exit_traffic_cmd, var_stress_time, var_sensorToolName, var_sensorToolOption, var_sensorToolPath, var_testType, var_platform)


def run_sensor_reading_idle_stress_test():
    Log_Debug("Entering procedure run_sensor_reading_idle_stress_test.\n")
    dLibObj = getDiagLibObj()

    # initialize the ports if not yet initialized
    wedge400c_init_and_check_all_eloop_modules_presence()

    var_toolName = ('python3 ' + SDK_TOOL)
    stress_time = int(dLibObj.auto_load_script_stress_time)
    var_option = '-c init'
    var_toolPath = get_common_system_sdk_path()
    var_logFile = SDK_LOG_FILE
    var_completeMsg = 'GB Initialization Test'
    var_passMsg = 'GB.*Initialization Test.*?PASS'
    var_sensorToolName = cel_sensor_test["bin_tool"]
    var_sensorToolOption = '-u'
    var_sensorToolPath = BMC_DIAG_TOOL_PATH
    var_testType = 'idle'
    var_platform = 'wedge400c'

    dLibObj.perform_sensor_reading_loading_stress_test(var_toolName, var_option, var_toolPath, var_logFile, var_completeMsg, var_passMsg, var_sensorToolName, var_sensorToolOption, var_sensorToolPath, var_testType, var_platform)


def set_snake_traffic_test_stress_time(stress_time):
    Log_Debug("Entering procedure set_snake_traffic_test_stress_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.platform_set_snake_traffic_test_stress_time(stress_time)


def check_board_type():
    Log_Debug("Entering procedure get_board_type_function.\n")
    dLibObj = getDiagLibObj()
    dLibObj.get_board_type()


def wedge400c_run_snake_traffic_test():
    Log_Debug("Entering procedure wedge400c_run_snake_traffic_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower() or 'wedge400_' in devicename.lower():
        Log_Info('Do not support mp2 and w400 unit, skip!')
        return

    # initialize the ports if not yet initialized
    wedge400c_init_and_check_all_eloop_modules_presence()

    var_toolName = SDK_TOOL
    var_toolPath = get_common_system_sdk_path()
    var_stress_time = dLibObj.snake_traffic_test_time
    var_portMode = 'dd_8x50g_qsfp_4x50g'

    return dLibObj.perform_snake_traffic_stress_test(var_toolName, var_toolPath, var_stress_time, var_portMode)


def set_re_init_test_stress_cycles(stress_cycles):
    Log_Debug("Entering procedure set_re_init_test_stress_cycles.\n")
    dLibObj = getDiagLibObj()

    dLibObj.platform_set_re_init_test_stress_cycles(stress_cycles)


def set_re_init_test_stress_time(stress_time):
    Log_Debug("Entering procedure set_re_init_test_stress_time.\n")
    dLibObj = getDiagLibObj()

    dLibObj.platform_set_re_init_test_stress_time(stress_time)


def wedge400c_run_sdk_re_init_test():
    Log_Debug("Entering procedure wedge400c_run_sdk_re_init_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower() or 'wedge400_' in devicename.lower():
        Log_Info('Do not support mp2 and w400 unit, skip!')
        return 

    # initialize the ports if not yet initialized
    wedge400c_init_and_check_all_eloop_modules_presence()

    var_cycle = dLibObj.re_init_cycles
    var_stress_time = dLibObj.re_init_stress_time
    var_toolPath = get_common_system_sdk_path()

    return dLibObj.SDK_re_init_test(var_cycle, var_stress_time, var_toolPath)


def set_port_linkup_test_stress_cycles(stress_cycles):
    Log_Debug("Entering procedure set_port_linkup_test_stress_cycles.\n")
    dLibObj = getDiagLibObj()

    dLibObj.platform_set_port_linkup_test_stress_cycles(stress_cycles)


def set_port_linkup_test_stress_time(stress_time):
    Log_Debug("Entering procedure set_port_linkup_test_stress_time.\n")
    dLibObj = getDiagLibObj()

    dLibObj.platform_set_port_linkup_stress_time(stress_time)


def wedge400c_run_port_enable_disable_test():
    Log_Debug("Entering procedure wedge400c_run_port_enable_disable_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower() or 'wedge400_' in devicename.lower():
        Log_Info('Do not support mp2 and w400 unit, skip!')
        return

    # initialize the ports if not yet initialized
    wedge400c_init_and_check_all_eloop_modules_presence()

    # python3 auto_load_user.py -c linkup -l 10 -d 5 -p dd_8x50g_qsfp_4x50g
    # total test time for 10 cycles = ~ 485 seconds
    var_sdkTool = SDK_TOOL
    var_stress_cycles = dLibObj.port_linkup_stress_cycles
    var_stress_time = dLibObj.port_linkup_stress_time
    #var_sdkOptions = ('-c linkup -l %s -d %s -p dd_8x50g_qsfp_4x50g' %(var_stress_cycles, var_stress_time))
    var_sdkOptions = '-c all --run_case 6 -p dd_8x50g_qsfp_4x50g'
    var_toolPath = get_common_system_sdk_path()

    dLibObj.perform_port_enable_disable_stress_test(var_sdkTool, var_sdkOptions, var_toolPath, var_stress_cycles)


def replace_the_sensor_cfg_file():
    Log_Debug("Entering procedure replce_the_sensor_cfg_file.\n")
    dLibObj = getDiagLibObj()
    dLibObj.replace_sensor_cfg_and_diag_init()


##### Minipack2 #####
def minipack2_change_to_sdk_path():
    Log_Debug("Entering procedure minipack2_change_to_sdk_path.\n")
    path = minipack2_get_current_system_sdk_path()
    CommonLib.change_dir(path)


def minipack2_init_and_check_all_eloop_modules_presence():
    Log_Debug("Entering procedure minipack2_init_and_check_all_eloop_modules_presence.\n")
    dLibObj = getDiagLibObj()

    var_sdkBackTool = xphyback
    var_initTool = xphy_tool
    var_initOption = xphy_init_options
    var_sdkTool = MINIPACK2_SDK_TOOL
    var_initToolPath = minipack2_get_current_system_sdk_path()
    var_max_pims = xphy_max_pims
    var_xphy_status = xphy_init_status
    var_force_reInit_sdk = False

    return dLibObj.minipack2_init_and_check_all_eloop_modules(var_sdkBackTool, var_initTool, var_initOption, var_sdkTool, var_initToolPath, var_max_pims, var_xphy_status, var_force_reInit_sdk)


def minipack2_run_openbmc_i2c_scan_stress_test():
    Log_Debug("Entering procedure minipack2_run_openbmc_i2c_scan_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        Log_Info('Do not support w400c and w400 unit, skip!')
        return

    var_toolName = cel_i2c_scan_stress_tool
    var_optionList = minipack2_cel_openmbc_i2c_dev_option_list
    var_keyList = minipack2_cel_openmbc_i2c_dev_key_list
    var_stress_time = dLibObj.i2c_scan_stress_time
    var_toolPath = BMC_DIAG_TOOL_PATH
    var_patternList = minipack2_cel_openmbc_i2c_dev_pattern_list
    var_platform = 'minipack2'

    return dLibObj.perform_i2c_scan_stress_test(var_toolName, var_optionList, var_keyList, var_stress_time, var_toolPath, var_patternList, var_platform)


def minipack2_run_openbmc_utility_stability_test():
    Log_Debug("Entering procedure minipack2_run_openbmc_utility_stability_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        Log_Info('Do not support w400c and w400 unit, skip!')
        return

    var_toolName1 = fw_util_tool
    var_optionStr1 = fw_util_optionStr
    var_pattern1 = minipack2_cel_openbmc_util_all_version_pattern
    var_toolName2 = bic_util_tool
    var_optionStr2 = bic_util_optionStr
    var_pattern2 = cel_openbmc_util_dev_id_pattern
    var_toolPath = FW_UTIL_PATH
    var_platform = 'minipack2'

    # get FW versions from SwImage
    fw_ver_array = minipack2_get_latest_fw_ver_array()

    numPlus = NumPlus(-1)
    Log_Info("Latest BMC version from SwImage: [%s]" %fw_ver_array[numPlus()])
    #Log_Info("Latest ROM version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest TPM version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest FCM B CPLD version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest FCM T CPLD version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PWR L CPLD version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PWR R CPLD version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest SCM CPLD version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest SMB CPLD version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest IOB FPGA version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PIM1 FPGA1 version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PIM2 FPGA2 version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PIM3 FPGA3 version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PIM4 FPGA4 version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PIM5 FPGA5 version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PIM6 FPGA6 version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PIM7 FPGA7 version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PIM8 FPGA8 version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest BIC version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest BIC BootLoader version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest BIOS version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest CPLD version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest ME version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PVCCIN version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest DDRAB version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest P1V05 version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest DIAG version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest SDK version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest DIAG OS version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PSU primary version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest PSU secondary version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest TH4 PCIE LOADER version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest TH4 PCIE version from SwImage: [%s]" %fw_ver_array[numPlus()])

    switch_to_openbmc()

    return dLibObj.perform_openbmc_utility_stability_test(var_toolName1, var_optionStr1, var_pattern1, var_toolName2, var_optionStr2, var_pattern2, var_toolPath, fw_ver_array, var_platform)

def minipack2_run_ipmi_command_stress_test():
    Log_Debug("Entering procedure minipack2_run_ipmi_command_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        Log_Info('Do not support w400c and w400 unit, skip!')
        return

    var_toolName = ipmi_toolName
    var_option = 'mc info'
    var_toolPath = IPMI_STRESS_TOOL_PATH
    var_pattern = minipack2_cel_ipmitool_pattern

    return dLibObj.perform_ipmi_interface_stress_test(var_toolName, var_option, var_pattern, var_toolPath)


def minipack2_run_tpm_access_stress_test():
    Log_Debug("Entering procedure run_tpm_access_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        Log_Info('Do not support w400c and w400 unit, skip!')
        return

    var_toolName = cel_tpm_stress_tool
    #var_verifyToolName = cel_eltt2_stress_tool
    var_verifyToolName = ''
    var_option = '-a'
    #var_verifyOption = '-R'
    var_verifyOption = ''
    var_stress_time = dLibObj.tpm_access_stress_time
    var_toolPath = DIAG_TOOL_PATH
    #var_verifyToolPath = UTILITY_TOOL_PATH
    var_verifyToolPath = ''
    var_pattern = minipack2_cel_tpm_status_pattern

    return dLibObj.perform_tpm_access_stress_test(var_toolName, var_verifyToolName, var_option, var_verifyOption, var_stress_time, var_toolPath, var_verifyToolPath, var_pattern)


def minipack2_check_pem_psu_connection():
    Log_Debug("Entering procedure check_pem_psu_connection.\n")
    dLibObj = getDiagLibObj()

    var_toolName1 = PEM_TEST_UTIL
    var_toolName2 = PSU_TEST_UTIL
    var_toolPath = BMC_DIAG_TOOL_PATH
    var_mode = 'openbmc'
    var_max_psu = 4

    return dLibObj.check_system_pem_psu_slot_connection(var_toolName1, var_toolName2, var_toolPath, var_max_psu, var_mode)


def minipack2_read_current_fw_sw_util_versions():
    Log_Debug("Entering procedure minipack2_read_current_fw_sw_util_versions.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_option = "all --version"
    var_tool_path = FW_UTIL_PATH
    var_toolName1 = fpga_software_test
    var_option1 = "-v"
    var_tool_path1 = BMC_DIAG_TOOL_PATH

    return dLibObj.minipack2_read_fw_sw_util_versions(var_toolName, var_option, var_tool_path, var_toolName1, var_option1, var_tool_path1)


def minipack2_get_current_system_sdk_path():
    Log_Debug("Entering procedure minipack2_get_current_system_sdk_path.\n")
    dLibObj = getDiagLibObj()

    #sdk_ver = get_new_image_version('SDK')
    cur_sdk_path = (SYSTEM_SDK_PATH + '/v*')
    return cur_sdk_path


def minipack2_get_current_th4_fw_versions():
    Log_Debug("Entering procedure minipack2_get_current_th4_fw_versions.\n")
    dLibObj = getDiagLibObj()

    var_toolName = MINIPACK2_SDK_TOOL
    var_tool_path = minipack2_get_current_system_sdk_path()

    return dLibObj.minipack2_get_TH4_versions(var_toolName, var_tool_path)


def minipack2_check_all_system_sw_fw_versions():
    Log_Debug("Entering procedure minipack2_check_all_system_sw_fw_versions.\n")
    dLibObj = getDiagLibObj()

    fw_name_list = []
    current_fw_list = []
    fw_ver_array = []
    psu_fw_ver_array = []
    ERR_COUNT = 0

    fw_name_list.append("BMC")
    fw_name_list.append("TPM")
    fw_name_list.append("FCM_B_CPLD")
    fw_name_list.append("FCM_T_CPLD")
    fw_name_list.append("PWR_L_CPLD")
    fw_name_list.append("PWR_R_CPLD")
    fw_name_list.append("SCM_CPLD")
    fw_name_list.append("SMB_CPLD")
    fw_name_list.append("IOB_FPGA")
    fw_name_list.append("PIM1_FPGA")
    fw_name_list.append("PIM2_FPGA")
    fw_name_list.append("PIM3_FPGA")
    fw_name_list.append("PIM4_FPGA")
    fw_name_list.append("PIM5_FPGA")
    fw_name_list.append("PIM6_FPGA")
    fw_name_list.append("PIM7_FPGA")
    fw_name_list.append("PIM8_FPGA")
    fw_name_list.append("BIC")
    fw_name_list.append("BIC_BOOTLOADER")
    fw_name_list.append("BIOS")
    fw_name_list.append("CPLD")
    fw_name_list.append("ME")
    fw_name_list.append("PVCCIN")
    fw_name_list.append("DDRAB")
    fw_name_list.append("P1V05")
    fw_name_list.append("DIAG")
    fw_name_list.append("SDK")
    fw_name_list.append("DIAG_OS")
    fw_name_list.append("PSU_PRI")
    fw_name_list.append("PSU_SEC")
    fw_name_list.append("TH4_PCIE_LOADER")
    fw_name_list.append("TH4_PCIE")

    switch_to_openbmc()

    # get FW versions from SwImage
    fw_ver_array = minipack2_get_latest_fw_ver_array()

    Log_Info("Latest BMC version from SwImage: [%s]" %fw_ver_array[0])
    Log_Info("Latest TPM version from SwImage: [%s]" %fw_ver_array[1])
    Log_Info("Latest FCM B CPLD version from SwImage: [%s]" %fw_ver_array[2])
    Log_Info("Latest FCM T CPLD version from SwImage: [%s]" %fw_ver_array[3])
    Log_Info("Latest PWR L CPLD version from SwImage: [%s]" %fw_ver_array[4])
    Log_Info("Latest PWR R CPLD version from SwImage: [%s]" %fw_ver_array[5])
    Log_Info("Latest SCM CPLD version from SwImage: [%s]" %fw_ver_array[6])
    Log_Info("Latest SMB CPLD version from SwImage: [%s]" %fw_ver_array[7])
    Log_Info("Latest IOB FPGA version from SwImage: [%s]" %fw_ver_array[8])
    Log_Info("Latest FPGA1 version from SwImage: [%s]" %fw_ver_array[9])
    Log_Info("Latest FPGA2 version from SwImage: [%s]" %fw_ver_array[10])
    Log_Info("Latest FPGA3 version from SwImage: [%s]" %fw_ver_array[11])
    Log_Info("Latest FPGA4 version from SwImage: [%s]" %fw_ver_array[12])
    Log_Info("Latest FPGA5 version from SwImage: [%s]" %fw_ver_array[13])
    Log_Info("Latest FPGA6 version from SwImage: [%s]" %fw_ver_array[14])
    Log_Info("Latest FPGA7 version from SwImage: [%s]" %fw_ver_array[15])
    Log_Info("Latest FPGA8 version from SwImage: [%s]" %fw_ver_array[16])
    Log_Info("Latest BIC version from SwImage: [%s]" %fw_ver_array[17])
    Log_Info("Latest BIC BootLoader version from SwImage: [%s]" %fw_ver_array[18])
    Log_Info("Latest BIOS version from SwImage: [%s]" %fw_ver_array[19])
    Log_Info("Latest CPLD version from SwImage: [%s]" %fw_ver_array[20])
    Log_Info("Latest ME version from SwImage: [%s]" %fw_ver_array[21])
    Log_Info("Latest PVCCIN version from SwImage: [%s]" %fw_ver_array[22])
    Log_Info("Latest DDRAB version from SwImage: [%s]" %fw_ver_array[23])
    Log_Info("Latest P1V05 version from SwImage: [%s]" %fw_ver_array[24])
    Log_Info("Latest DIAG version from SwImage: [%s]" %fw_ver_array[25])
    Log_Info("Latest SDK version from SwImage: [%s]" %fw_ver_array[26])
    Log_Info("Latest DIAG OS version from SwImage: [%s]" %fw_ver_array[27])
    if dLibObj.pwr_supply_type == 'psu':
        Log_Info("Latest PSU primary version from SwImage: [%s]" %fw_ver_array[28])
        Log_Info("Latest PSU secondary version from SwImage: [%s]" %fw_ver_array[29])
    Log_Info("Latest TH4 PCIE LOADER version from SwImage: [%s]" %fw_ver_array[30])
    Log_Info("Latest TH4 PCIE version from SwImage: [%s]" %fw_ver_array[31])

    # read current FW versions
    fw_list = minipack2_read_current_fw_sw_util_versions()

    current_fw_list.append(fw_list[0])    # BMC
    current_fw_list.append(fw_list[1])    # TPM
    current_fw_list.append(fw_list[2])    # FCM B CPLD
    current_fw_list.append(fw_list[3])    # FCM T CPLD
    current_fw_list.append(fw_list[4])    # PWR L CPLD
    current_fw_list.append(fw_list[5])    # PWR R CPLD
    current_fw_list.append(fw_list[6])    # SCM CPLD
    current_fw_list.append(fw_list[7])    # SMB CPLD
    current_fw_list.append(fw_list[8])    # IOB FPGA
    current_fw_list.append(fw_list[9])    # PIM1 FPGA
    current_fw_list.append(fw_list[10])   # PIM2 FPGA
    current_fw_list.append(fw_list[11])   # PIM3 FPGA
    current_fw_list.append(fw_list[12])   # PIM4 FPGA
    current_fw_list.append(fw_list[13])   # PIM5 FPGA
    current_fw_list.append(fw_list[14])   # PIM6 FPGA
    current_fw_list.append(fw_list[15])   # PIM7 FPGA
    current_fw_list.append(fw_list[16])   # PIM8 FPGA
    current_fw_list.append(fw_list[17])   # BIC
    current_fw_list.append(fw_list[18])   # BIC BOOTLOADER
    current_fw_list.append(fw_list[19])   # BIOS
    current_fw_list.append(fw_list[20])   # CPLD
    current_fw_list.append(fw_list[21])   # ME
    current_fw_list.append(fw_list[22])   # PVCCIN
    current_fw_list.append(fw_list[23])   # DDRAB
    current_fw_list.append(fw_list[24])   # P1V05
    current_fw_list.append(fw_list[25])   # DIAG

    Log_Debug("Current BMC version: [%s]" %current_fw_list[0])
    Log_Debug("Current TPM version: [%s]" %current_fw_list[1])
    Log_Debug("Current FCM B CPLD version: [%s]" %current_fw_list[2])
    Log_Debug("Current FCM T CPLD version: [%s]" %current_fw_list[3])
    Log_Debug("Current PWR L CPLD version: [%s]" %current_fw_list[4])
    Log_Debug("Current PWR R CPLD version: [%s]" %current_fw_list[5])
    Log_Debug("Current SCM CPLD version: [%s]" %current_fw_list[6])
    Log_Debug("Current SMB CPLD version: [%s]" %current_fw_list[7])
    Log_Debug("Current IOB FPGA version: [%s]" %current_fw_list[8])
    Log_Debug("Current PIM1 FPGA version: [%s]" %current_fw_list[9])
    Log_Debug("Current PIM2 FPGA version: [%s]" %current_fw_list[10])
    Log_Debug("Current PIM3 FPGA version: [%s]" %current_fw_list[11])
    Log_Debug("Current PIM4 FPGA version: [%s]" %current_fw_list[12])
    Log_Debug("Current PIM5 FPGA version: [%s]" %current_fw_list[13])
    Log_Debug("Current PIM6 FPGA version: [%s]" %current_fw_list[14])
    Log_Debug("Current PIM7 FPGA version: [%s]" %current_fw_list[15])
    Log_Debug("Current PIM8 FPGA version: [%s]" %current_fw_list[16])
    Log_Debug("Current BIC version: [%s]" %current_fw_list[17])
    Log_Debug("Current BIC BOOTLOADER version: [%s]" %current_fw_list[18])
    Log_Debug("Current BIOS version: [%s]" %current_fw_list[19])
    Log_Debug("Current CPLD version: [%s]" %current_fw_list[20])
    Log_Debug("Current ME version: [%s]" %current_fw_list[21])
    Log_Debug("Current PVCCIN version: [%s]" %current_fw_list[22])
    Log_Debug("Current DDRAB version: [%s]" %current_fw_list[23])
    Log_Debug("Current P1V05 version: [%s]" %current_fw_list[24])
    Log_Debug("Current DIAG version: [%s]" %current_fw_list[25])

    if dLibObj.pwr_supply_type == 'psu':
        # get PSU primary and secondary FW versions for each psu
        psu_fw_ver_array = read_current_psu_fw_versions(4)

        if psu_fw_ver_array[0] != fw_ver_array[28]:
            Log_Info("********psu[0]=%s********" % psu_fw_ver_array[0])
            Log_Info("**********fw_ver[28]=%s********" % fw_ver_array[28])
            Log_Fail("Detected current PSU1 primary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[0], fw_ver_array[28]))
            dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU1 primary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[0], fw_ver_array[28]))

        if psu_fw_ver_array[1] != fw_ver_array[29]:
            Log_Fail("Detected current PSU1 secondary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[1], fw_ver_array[29]))
            dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU1 secondary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[1], fw_ver_array[29]))

        if psu_fw_ver_array[2] != fw_ver_array[28]:
            Log_Fail("Detected current PSU2 primary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[2], fw_ver_array[28]))
            dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU2 primary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[2], fw_ver_array[28]))

        if psu_fw_ver_array[3] != fw_ver_array[29]:
            Log_Fail("Detected current PSU2 secondary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[3], fw_ver_array[29]))
            dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU2 secondary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[3], fw_ver_array[29]))

        if psu_fw_ver_array[4] != fw_ver_array[28]:
            Log_Fail("Detected current PSU3 primary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[4], fw_ver_array[28]))
            dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU3 primary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[4], fw_ver_array[28]))

        if psu_fw_ver_array[5] != fw_ver_array[29]:
            Log_Fail("Detected current PSU3 secondary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[5], fw_ver_array[29]))
            dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU3 secondary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[5], fw_ver_array[29]))

        if psu_fw_ver_array[6] != fw_ver_array[28]:
            Log_Fail("Detected current PSU4 primary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[6], fw_ver_array[28]))
            dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU4 primary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[6], fw_ver_array[28]))

        if psu_fw_ver_array[7] != fw_ver_array[29]:
            Log_Fail("Detected current PSU4 secondary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[7], fw_ver_array[29]))
            dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current PSU4 secondary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[7], fw_ver_array[29]))

    else:
        Log_Fail("Error: Minipack2 does not support PEM.")
        dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
    switch_to_centos()

    # th4Presence = dLibObj.minipack2CheckTH4Presence()
    if(dLibObj.minipack2CheckTH4Presence()):
        # get TH4 FW versions
        Log_Info("get TH4 FW versions !!!!")

        th4_fw_ver_array = minipack2_get_current_th4_fw_versions()
        if th4_fw_ver_array[0] != fw_ver_array[30]:
            Log_Fail("Detected current TH4 PCIe Loader FW version[%s] does not match expected version[%s]" %(th4_fw_ver_array[0], fw_ver_array[30]))
            dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current TH4 PCIe Loader FW version[%s] matched expected version[%s]: PASSED" %(th4_fw_ver_array[0], fw_ver_array[30]))

        if th4_fw_ver_array[1] != fw_ver_array[31]:
            Log_Fail("Detected current TH4 PCIe FW version[%s] does not match expected version[%s]" %(th4_fw_ver_array[0], fw_ver_array[31]))
            dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')
        else:
            Log_Info("Current TH4 PCIe FW version[%s] matched expected version[%s]: PASSED" %(th4_fw_ver_array[0], fw_ver_array[31]))

    # get SDK version
    sdk_ver = read_current_sdk_version()
    current_fw_list.append(sdk_ver)
    Log_Info("Current SDK version: [%s]" %current_fw_list[26])

    # get diagOS version
    diagos_ver = read_current_diagOS_version()
    current_fw_list.append(diagos_ver)
    Log_Info("Current DIAG OS version: [%s]" %current_fw_list[27])

    for i in range(0,28):
        #skip SMB CPLD check for now, not upgradable due to failure during upgrade process.
        if i == 7:
            continue

        if current_fw_list[i] != fw_ver_array[i]:
            ERR_COUNT += 1
            Log_Fail("Detected current %s version[%s] does not match expected version[%s]" %(fw_name_list[i], current_fw_list[i], fw_ver_array[i]))
        else:
            Log_Info("Current %s version[%s] matched expected version[%s]: PASSED" %(fw_name_list[i], current_fw_list[i], fw_ver_array[i]))

    if ERR_COUNT == 0:
        Log_Info('All current FW versions matched expected FW versions')
        Log_Success("minipack2_check_all_system_sw_fw_versions result: PASSED.")
    else:
        dLibObj.wpl_raiseException('Failed minipack2_check_all_system_sw_fw_versions.')

    return ERR_COUNT


def set_port_enable_disable_test_stress_cycles(stress_cycles):
    Log_Debug("Entering procedure set_port_enable_disable_test_stress_cycles.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.platform_set_port_enable_disable_test_stress_cycles(stress_cycles)


def set_port_enable_disable_test_stress_time(stress_time):
    Log_Debug("Entering procedure set_port_enable_disable_test_stress_time.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.platform_set_port_enable_disable_test_stress_time(stress_time)

##### w400 ######
def w400_run_port_enable_disable_test(AllPort):
    Log_Debug("Entering procedure w400_run_port_enable_disable_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower() or 'wedge400c' in devicename.lower():
        Log_Info('Do not support mp2 and w400c unit, skip!')
        return

    var_sdkTool = W400_SDK_TOOL
    var_sdkToolPath = '/usr/local/cls_diag/SDK/'
    var_vlan_cmd = w400_set_vlan_cmd
    var_start_DD_cmd = w400_DD_traffic_cmd
    var_start_56_cmd = w400_56_traffic_cmd
    var_stress_cycles = dLibObj.port_enable_disable_stress_cycles
    #var_stress_time = dLibObj.re_init_stress_time
    var_stress_time = 'sleep 60'
    var_stop_DD_cmd = w400_DD_stop_cmd
    var_stop_56_cmd = w400_56_stop_cmd
    var_DD_counters = w400_DD_counters
    var_56_counters = w400_56_counters
    var_up_status = port_up_status
    var_down_status = port_down_status
    var_rpkt = w400_rpkt
    var_tpkt = w400_tpkt
    var_portStatusCmd = w400_port_cmd
    var_setPortCmd = SDK_SET_PORT_COMMAND
    var_portEnable = SDK_PORT_ENABLE_OPTION
    var_portDisable = SDK_PORT_DISABLE_OPTION

    # perform port enable disable stress test
    return dLibObj.w400_perform_port_enable_disable_stress_test(AllPort, var_sdkTool, var_sdkToolPath, var_vlan_cmd, var_start_DD_cmd, var_start_56_cmd, var_stress_cycles, var_stress_time, var_stop_DD_cmd, var_stop_56_cmd, var_up_status, var_down_status, var_portStatusCmd, var_setPortCmd, var_portEnable, var_portDisable, var_DD_counters, var_56_counters, var_rpkt, var_tpkt)


def w400_run_sdk_re_init_test():
    Log_Debug("Entering procedure w400_run_sdk_re_init_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower() or 'wedge400c' in devicename.lower():
        Log_Info('Do not support mp2 and w400c unit, skip!')
        return

    var_sdkTool = W400_SDK_TOOL
    var_sdkOption = ' '
    var_sdkToolPath = SYSTEM_SDK_PATH
    var_vlan_cmd = w400_set_vlan_cmd
    var_start_DD_cmd = w400_DD_traffic_cmd
    var_start_56_cmd = w400_56_traffic_cmd
    var_stop_DD_cmd = w400_Reinit_DD_stop_cmd
    var_stop_56_cmd = w400_Reinit_56_stop_cmd
    # var_stress_time = dLibObj.re_init_stress_time
    var_stress_time = 'sleep 120'
    var_port_cmd = w400_port_cmd
    var_up_status = port_up_status
    var_traffic_counters = w400_traffic_counters
    var_rpkt = w400_rpkt
    var_tpkt = w400_tpkt

    # run sdk re-init stress test
    return dLibObj.w400_SDK_re_init_test(var_sdkTool, var_sdkOption, var_sdkToolPath, var_vlan_cmd, var_start_DD_cmd, var_start_56_cmd, var_stress_time, var_stop_DD_cmd, var_stop_56_cmd, var_port_cmd, var_up_status, var_traffic_counters, var_rpkt, var_tpkt)


def w400_run_snake_traffic_test():
    Log_Debug("Entering procedure w400_run_snake_traffic_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower() or 'wedge400c' in devicename.lower():
        Log_Info('Do not support mp2 and w400c unit, skip!')
        return

    var_sdkTool = MINIPACK2_SDK_TOOL
    var_sdkOption = '-m 16x400G_32x200G_PAM4'
    var_sdkToolPath = SYSTEM_SDK_PATH
    var_start_cpu_traffic_cmd = w400_traffic_cmd
    var_stress_time = dLibObj.snake_traffic_test_time
    var_port_cmd = w400_port_cmd
    var_up_status = port_up_status
    var_stop_DD_cmd = w400_snake_DD_stop_cmd
    var_stop_56_cmd = w400_snake_56_stop_cmd
    var_traffic_counters = w400_snake_traffic_counters
    var_rpkt = w400_rpkt
    var_tpkt = w400_tpkt

    # run snake stress test
    return dLibObj.w400_perform_snake_traffic_stress_test(var_sdkTool, var_sdkOption, var_sdkToolPath, var_start_cpu_traffic_cmd, var_stress_time, var_port_cmd, var_up_status, var_stop_DD_cmd, var_stop_56_cmd, var_traffic_counters, var_rpkt, var_tpkt)


def minipack2_run_port_enable_disable_test(AllPort):
    Log_Debug("Entering procedure minipack2_run_port_enable_disable_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower():
        startup_default_port_group
    elif 'wedge400' in devicename.lower():
        Log_Info('Do not support w400c and w400 unit, skip!')
        return

    # initialize the ports if not yet initialized
    minipack2_init_and_check_all_eloop_modules_presence()

    var_sdkTool = MINIPACK2_SDK_TOOL
    var_sdkToolPath = '/usr/local/cls_diag/SDK/v*'
    var_set_vlan_cmd = minipack2_set_vlan_cmd
    var_start_cpu_traffic_cmd = minipack2_start_cpu_traffic_cmd
    var_stress_cycles = dLibObj.port_enable_disable_stress_cycles
    var_stress_time = dLibObj.re_init_stress_time
    var_stop_cpu_traffic_cmd = minipack2_stop_cpu_traffic_cmd
    var_pattern1 = minipack2_vlan_output_pattern
    var_portStatusCmd = SDK_PORT_STATUS_COMMAND
    var_setPortCmd = SDK_SET_PORT_COMMAND
    var_portEnableOption = SDK_PORT_ENABLE_OPTION
    var_portDisableOption = SDK_PORT_DISABLE_OPTION

    # perform port enable disable stress test
    return dLibObj.minipack2_perform_port_enable_disable_stress_test(AllPort, var_sdkTool, var_sdkToolPath, var_set_vlan_cmd, var_start_cpu_traffic_cmd, var_stress_cycles, var_stress_time, var_stop_cpu_traffic_cmd, var_pattern1, var_portStatusCmd, var_setPortCmd, var_portEnableOption, var_portDisableOption)


def minipack2_run_sensor_reading_high_loading_stress_test():
    Log_Debug("Entering procedure minipack2_run_sensor_reading_high_loading_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        Log_Info('Do not support w400c and w400 unit, skip!')
        return
    switch_to_centos_diag_tool()
    startup_default_port_group()

    # initialize the ports if not yet initialized
    minipack2_init_and_check_all_eloop_modules_presence()

    var_sdkTool = MINIPACK2_SDK_TOOL
    var_sdkOption = ' '
    var_sdkToolPath = minipack2_get_current_system_sdk_path()
    var_set_vlan_cmd = minipack2_set_vlan_cmd
    var_start_cpu_traffic_cmd = minipack2_start_cpu_traffic_cmd
    var_stress_time = dLibObj.auto_load_script_stress_time
    var_stop_cpu_traffic_cmd = minipack2_stop_cpu_traffic_cmd
    var_pattern1 = minipack2_vlan_output_pattern
    var_sensorToolName = cel_sensor_test["bin_tool"]
    var_sensorToolOption = '-b all -c'
    var_sensorToolPath = BMC_DIAG_TOOL_PATH

    # run sensor reading high loading stress test
    return dLibObj.minipack2_perform_sensor_reading_high_loading_stress_test(var_sdkTool, var_sdkOption, var_sdkToolPath, var_set_vlan_cmd, var_start_cpu_traffic_cmd, var_stop_cpu_traffic_cmd, var_stress_time, var_pattern1, var_sensorToolName, var_sensorToolOption, var_sensorToolPath)


def minipack2_run_sensor_reading_idle_stress_test():
    Log_Debug("Entering procedure minipack2_run_sensor_reading_idle_stress_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        Log_Info('Do not support w400c and w400 unit, skip!')
        return
    ## add the func 08/18
    switch_to_centos_diag_tool()
    startup_default_port_group()

    # initialize the ports if not yet initialized
    minipack2_init_and_check_all_eloop_modules_presence()

    var_toolName = MINIPACK2_SDK_TOOL
    stress_time = int(dLibObj.auto_load_script_stress_time)
    var_option = ' '
    var_toolPath = minipack2_get_current_system_sdk_path()
    var_logFile = SDK_LOG_FILE
    var_passMsg = 'SDK init done'
    var_completeMsg = 'GB Initialization Test'
    var_sensorToolName = cel_sensor_test["bin_tool"]
    var_sensorToolOption = '-b all -c'
    var_sensorToolPath = BMC_DIAG_TOOL_PATH
    var_testType = 'idle'
    var_platform = 'minipack2'

    dLibObj.perform_sensor_reading_loading_stress_test(var_toolName, var_option, var_toolPath, var_logFile, var_completeMsg, var_passMsg, var_sensorToolName, var_sensorToolOption, var_sensorToolPath, var_testType, var_platform)


def minipack2_run_eeprom_access_stress_test():
    Log_Debug("Entering procedure minipack2_run_eeprom_access_stress_test.\n")
    dLibObj = getDiagLibObj()

    # initialize the ports if not yet initialized
    minipack2_init_and_check_all_eloop_modules_presence()

    var_sdkTool = MINIPACK2_SDK_TOOL
    var_sdkOption = ' '
    var_sdkToolPath = minipack2_get_current_system_sdk_path()
    var_resetTool = cel_qsfp_tool
    var_resetOption1 = '--pim=0 --port=0 --reset=on'
    var_resetOption2 = '--pim=0 --port=0 --reset=off'
    var_resetToolPath = DIAG_TOOL_PATH
    var_toolName = cel_eeprom_stress_tool
    var_option = '10 58 2970 3630 1'
    var_stress_time = dLibObj.eeprom_stress_time
    var_toolPath = UTILITY_TOOL_PATH
    var_pattern1 = minipack2_cel_temp_volt_limit_pattern1
    var_pattern2 = cel_temp_volt_limit_pattern2
    var_pattern3 = cel_temp_volt_limit_pattern3
    var_pattern4 = cel_temp_volt_limit_start_pattern

    # run eeprom access stress test
    return dLibObj.minipack2_perform_eeprom_access_stress_test(var_sdkTool, var_sdkOption, var_sdkToolPath, var_resetTool, var_resetOption1, var_resetOption2, var_resetToolPath, var_toolName, var_option, var_stress_time, var_toolPath, var_pattern1, var_pattern2, var_pattern3, var_pattern4)


def minipack2_run_snake_traffic_test():
    Log_Debug("Entering procedure minipack2_run_snake_traffic_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        Log_Info('Do not support w400 and w400c unit, skip!')
        return
    startup_default_port_group()

    # initialize the ports if not yet initialized
    minipack2_init_and_check_all_eloop_modules_presence()

    var_sdkTool = MINIPACK2_SDK_TOOL
    var_sdkOption = ' '
    var_sdkToolPath = minipack2_get_current_system_sdk_path()
    var_set_vlan_cmd = minipack2_set_vlan_cmd
    var_start_cpu_traffic_cmd = minipack2_start_cpu_traffic_cmd
    var_stress_time = dLibObj.snake_traffic_test_time
    var_stop_cpu_traffic_cmd = minipack2_stop_cpu_traffic_cmd
    var_pattern1 = minipack2_vlan_output_pattern

    # run snake stress test
    return dLibObj.minipack2_perform_snake_traffic_stress_test(var_sdkTool, var_sdkOption, var_sdkToolPath, var_set_vlan_cmd, var_start_cpu_traffic_cmd, var_stress_time, var_stop_cpu_traffic_cmd, var_pattern1)


def minipack2_run_sdk_re_init_test():
    Log_Debug("Entering procedure minipack2_run_sdk_re_init_test.\n")
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        Log_Info('Do not support w400 and w400c unit, skip!')
        return

    # initialize the ports if not yet initialized
    minipack2_init_and_check_all_eloop_modules_presence()

    var_sdkTool = MINIPACK2_SDK_TOOL
    var_sdkOption = ' '
    var_sdkToolPath = minipack2_get_current_system_sdk_path()
    var_set_vlan_cmd = minipack2_set_vlan_cmd
    var_start_cpu_traffic_cmd = minipack2_start_cpu_traffic_cmd
    var_stress_time = dLibObj.re_init_stress_time
    var_stop_cpu_traffic_cmd = minipack2_stop_cpu_traffic_cmd
    var_pattern1 = minipack2_vlan_output_pattern

    # run sdk re-init stress test
    return dLibObj.minipack2_SDK_re_init_test(var_sdkTool, var_sdkOption, var_sdkToolPath, var_set_vlan_cmd, var_start_cpu_traffic_cmd, var_stress_time, var_stop_cpu_traffic_cmd, var_pattern1)


##### Cloudripper ####
def cloudripper_read_current_fw_sw_util_versions():
    Log_Debug("Entering procedure cloudripper_read_current_fw_sw_util_versions.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_option = "all --version"
    var_tool_path = FW_UTIL_PATH
    var_toolName1 = fpga_software_test
    var_option1 = "-v"
    var_tool_path1 = BMC_DIAG_TOOL_PATH
    var_platform = 'cloudripper'

    return dLibObj.platform_read_fw_sw_util_versions(var_toolName, var_option, var_tool_path, var_toolName1, var_option1, var_tool_path1, var_platform)


def cloudripper_check_all_system_sw_fw_versions():
    Log_Debug("Entering procedure cloudripper_check_all_system_sw_fw_versions.\n")
    dLibObj = getDiagLibObj()

    fw_name_list = []
    current_fw_list = []
    fw_ver_array = []
    ERR_COUNT = 0

    fw_name_list.append("BMC")
    fw_name_list.append("TPM")
    fw_name_list.append("FCM_CPLD")
    fw_name_list.append("PWR_CPLD")
    fw_name_list.append("SCM_CPLD")
    fw_name_list.append("SMB_CPLD")
    fw_name_list.append("FPGA1")
    fw_name_list.append("FPGA2")
    fw_name_list.append("BIC")
    fw_name_list.append("BIC_BOOTLOADER")
    fw_name_list.append("BIOS")
    fw_name_list.append("CPLD")
    fw_name_list.append("ME")
    fw_name_list.append("PVCCIN")
    fw_name_list.append("DDRAB")
    fw_name_list.append("P1V05")
    fw_name_list.append("DIAG")
    fw_name_list.append("SDK")
    fw_name_list.append("DIAG_OS")
    fw_name_list.append("PSU_PRI")
    fw_name_list.append("PSU_SEC")

    switch_to_openbmc()

    # get FW versions from SwImage
    fw_ver_array = get_latest_fw_ver_array()

    Log_Info("Latest BMC version from SwImage: [%s]" %fw_ver_array[0])
    Log_Info("Latest TPM version from SwImage: [%s]" %fw_ver_array[1])
    Log_Info("Latest FCM CPLD version from SwImage: [%s]" %fw_ver_array[2])
    Log_Info("Latest PWR CPLD version from SwImage: [%s]" %fw_ver_array[3])
    Log_Info("Latest SCM CPLD version from SwImage: [%s]" %fw_ver_array[4])
    Log_Info("Latest SMB CPLD version from SwImage: [%s]" %fw_ver_array[5])
    Log_Info("Latest FPGA1 version from SwImage: [%s]" %fw_ver_array[6])
    Log_Info("Latest FPGA2 version from SwImage: [%s]" %fw_ver_array[7])
    Log_Info("Latest BIC version from SwImage: [%s]" %fw_ver_array[8])
    Log_Info("Latest BIC BootLoader version from SwImage: [%s]" %fw_ver_array[9])
    Log_Info("Latest BIOS version from SwImage: [%s]" %fw_ver_array[10])
    Log_Info("Latest CPLD version from SwImage: [%s]" %fw_ver_array[11])
    Log_Info("Latest ME version from SwImage: [%s]" %fw_ver_array[12])
    Log_Info("Latest PVCCIN version from SwImage: [%s]" %fw_ver_array[13])
    Log_Info("Latest DDRAB version from SwImage: [%s]" %fw_ver_array[14])
    Log_Info("Latest P1V05 version from SwImage: [%s]" %fw_ver_array[15])
    Log_Info("Latest DIAG version from SwImage: [%s]" %fw_ver_array[16])
    Log_Info("Latest SDK version from SwImage: [%s]" %fw_ver_array[17])
    Log_Info("Latest DIAG OS version from SwImage: [%s]" %fw_ver_array[18])
### Disable first, currently cloudripper psu-util not ready yet ###
    #if dLibObj.pwr_supply_type == 'psu':
        #Log_Info("Latest PSU primary FW version from SwImage: [%s]" %fw_ver_array[18])
        #Log_Info("Latest PSU secondary FW version from SwImage: [%s]" %fw_ver_array[19])

    # read current FW versions
    fw_list = cloudripper_read_current_fw_sw_util_versions()

    current_fw_list.append(fw_list[0])    # BMC
    current_fw_list.append(fw_list[1])    # TPM
    current_fw_list.append(fw_list[2])    # FCM CPLD
    current_fw_list.append(fw_list[3])    # PWR CPLD
    current_fw_list.append(fw_list[4])    # SCM CPLD
    current_fw_list.append(fw_list[5])    # SMB CPLD
    current_fw_list.append(fw_list[6])    # FPGA1
    current_fw_list.append(fw_list[7])    # FPGA2
    current_fw_list.append(fw_list[8])    # BIC
    current_fw_list.append(fw_list[9])    # BIC BOOTLOADER
    current_fw_list.append(fw_list[10])   # BIOS
    current_fw_list.append(fw_list[11])   # CPLD
    current_fw_list.append(fw_list[12])   # ME
    current_fw_list.append(fw_list[13])   # PVCCIN
    current_fw_list.append(fw_list[14])   # DDRAB
    current_fw_list.append(fw_list[15])   # P1V05
    current_fw_list.append(fw_list[16])   # DIAG

    Log_Debug("Current BMC version: [%s]" %current_fw_list[0])
    Log_Debug("Current TPM version: [%s]" %current_fw_list[1])
    Log_Debug("Current FCM CPLD version: [%s]" %current_fw_list[2])
    Log_Debug("Current PWR CPLD version: [%s]" %current_fw_list[3])
    Log_Debug("Current SCM CPLD version: [%s]" %current_fw_list[4])
    Log_Debug("Current SMB CPLD version: [%s]" %current_fw_list[5])
    Log_Debug("Current FPGA1 version: [%s]" %current_fw_list[6])
    Log_Debug("Current FPGA2 version: [%s]" %current_fw_list[7])
    Log_Debug("Current BIC version: [%s]" %current_fw_list[8])
    Log_Debug("Current BIC BOOTLOADERversion: [%s]" %current_fw_list[9])
    Log_Debug("Current BIOS version: [%s]" %current_fw_list[10])
    Log_Debug("Current CPLD version: [%s]" %current_fw_list[11])
    Log_Debug("Current ME version: [%s]" %current_fw_list[12])
    Log_Debug("Current PVCCIN version: [%s]" %current_fw_list[13])
    Log_Debug("Current DDRAB version: [%s]" %current_fw_list[14])
    Log_Debug("Current P1V05 version: [%s]" %current_fw_list[15])
    Log_Debug("Current DIAG version: [%s]" %current_fw_list[16])

### Disable first, currently cloudripper psu-util not ready yet ###
    # currently there's no way to get PEM fw versions, only can get psu fw versions
#    if dLibObj.pwr_supply_type == 'psu':
#        # get PSU primary and secondary FW versions for each psu
#        psu_fw_ver_array = read_current_psu_fw_versions(2)
#        if psu_fw_ver_array[0] != fw_ver_array[19]:
#            Log_Fail("Detected current PSU1 primary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[0], fw_ver_array[19]))
#            dLibObj.wpl_raiseException('Failed cloudripper_check_all_system_sw_fw_versions.')
#        else:
#            Log_Info("Current PSU1 primary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[0], fw_ver_array[19]))
#
#        if psu_fw_ver_array[1] != fw_ver_array[20]:
#            Log_Fail("Detected current PSU1 secondary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[1], fw_ver_array[20]))
#            dLibObj.wpl_raiseException('Failed cloudripper_check_all_system_sw_fw_versions.')
#        else:
#            Log_Info("Current PSU1 secondary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[1], fw_ver_array[20]))
#
#        if psu_fw_ver_array[2] != fw_ver_array[19]:
#            Log_Fail("Detected current PSU2 primary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[2], fw_ver_array[19]))
#            dLibObj.wpl_raiseException('Failed cloudripper_check_all_system_sw_fw_versions.')
#        else:
#            Log_Info("Current PSU2 primary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[2], fw_ver_array[19]))
#
#        if psu_fw_ver_array[3] != fw_ver_array[20]:
#            Log_Fail("Detected current PSU2 secondary FW version[%s] does not match expected version[%s]" %(psu_fw_ver_array[3], fw_ver_array[20]))
#            dLibObj.wpl_raiseException('Failed cloudripper_check_all_system_sw_fw_versions.')
#        else:
#            Log_Info("Current PSU2 secondary FW version[%s] matched expected version[%s]: PASSED" %(psu_fw_ver_array[3], fw_ver_array[20]))

    switch_to_centos()

    sdk_ver = platform_read_current_sdk_version()
    current_fw_list.append(sdk_ver)
    Log_Info("Current SDK version: [%s]" %current_fw_list[17])

    diagos_ver = read_current_diagOS_version()
    current_fw_list.append(diagos_ver)
    Log_Info("Current DIAG OS version: [%s]" %current_fw_list[18])

    for i in range(0, 19):
        if current_fw_list[i] != fw_ver_array[i]:
            ERR_COUNT += 1
            Log_Fail("Detected current %s version[%s] does not match expected version[%s]" %(fw_name_list[i], current_fw_list[i], fw_ver_array[i]))
        else:
            Log_Info("Current %s version[%s] matched expected version[%s]: PASSED" %(fw_name_list[i], current_fw_list[i], fw_ver_array[i]))

    if ERR_COUNT == 0:
        Log_Info('Checked all current FW versions matched expected FW versions')
        Log_Success("cloudripper_check_all_system_sw_fw_versions result: PASSED.")
    else:
        dLibObj.wpl_raiseException('Failed cloudripper_check_all_system_sw_fw_versions.')

    return ERR_COUNT


def cloudripper_run_openbmc_i2c_scan_stress_test():
    Log_Debug("Entering procedure cloudripper_run_openbmc_i2c_scan_stress_test.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_i2c_scan_stress_tool
    var_optionList = cel_openmbc_i2c_option_list
    var_keyList = cel_openmbc_i2c_key_list
    var_stress_time = dLibObj.i2c_scan_stress_time
    var_toolPath = BMC_DIAG_TOOL_PATH
    var_patternList = cloudripper_cel_openmbc_i2c_pattern_list
    var_platform = 'cloudripper'

    return dLibObj.perform_i2c_scan_stress_test(var_toolName, var_optionList, var_keyList, var_stress_time, var_toolPath, var_patternList, var_platform)


def cloudripper_run_ipmi_command_stress_test():
    Log_Debug("Entering procedure cloudripper_run_ipmi_command_stress_test.\n")
    dLibObj = getDiagLibObj()

    var_toolName = ipmi_toolName
    var_option = 'mc info'
    var_toolPath = IPMI_STRESS_TOOL_PATH
    var_pattern = cloudripper_cel_ipmitool_pattern

    return dLibObj.perform_ipmi_interface_stress_test(var_toolName, var_option, var_pattern, var_toolPath)


def cloudripper_run_snake_traffic_test():
    Log_Debug("Entering procedure cloudripper_run_snake_traffic_test.\n")
    dLibObj = getDiagLibObj()

    # initialize the ports if not yet initialized
    cloudripper_init_and_check_all_eloop_modules_presence

    var_toolName = SDK_TOOL
    var_toolPath = get_common_system_sdk_path()
    #var_stress_time = int(dLibObj.snake_traffic_test_time/7)
    var_stress_time = 60
    var_portMode = '32x1x8x50g'

    return dLibObj.cloudripper_perform_snake_traffic_stress_test(var_toolName, var_toolPath, var_stress_time, var_portMode)


def cloudripper_init_and_check_all_eloop_modules_presence():
    Log_Debug("Entering procedure cloudripper_init_and_check_all_eloop_modules_presence.\n")
    dLibObj = getDiagLibObj()

    #python3 auto_load_user.py -c init -d 5 -p 32x1x8x50g
    var_initTool = SDK_TOOL
    var_initOption = '-c init -d 5 -p 32x1x8x50g'
    var_initToolPath = get_common_system_sdk_path()
    var_force_reInit_sdk = False

    return dLibObj.cloudripper_perform_detect_all_eloop_modules(var_initTool, var_initOption, var_initToolPath, var_force_reInit_sdk)


def cloudripper_run_sensor_reading_high_loading_stress_test():
    Log_Debug("Entering procedure cloudripper_run_sensor_reading_high_loading_stress_test.\n")
    dLibObj = getDiagLibObj()

    # initialize the ports if not yet initialized
    cloudripper_init_and_check_all_eloop_modules_presence()

    var_toolName = ('python3 ' + SDK_TOOL)
    stress_time = int(dLibObj.auto_load_script_stress_time)
    var_option = ('-c l2_cpu -d %s -p 32x1x8x50g' %stress_time)
    var_toolPath = get_common_system_sdk_path()
    var_logFile = SDK_LOG_FILE
    var_completeMsg = 'L2 snake traffic with cpu injection'
    var_passMsg = 'L2.*?PASS'
    var_sensorToolName = cel_sensor_test["bin_tool"]
    var_sensorToolOption = '-u'
    var_sensorToolPath = BMC_DIAG_TOOL_PATH
    var_testType = 'high'
    var_platform = 'cloudripper'

    dLibObj.perform_sensor_reading_loading_stress_test(var_toolName, var_option, var_toolPath, var_logFile, var_completeMsg, var_passMsg, var_sensorToolName, var_sensorToolOption, var_sensorToolPath, var_testType, var_platform)


def cloudripper_run_sensor_reading_idle_stress_test():
    Log_Debug("Entering procedure cloudripper_run_sensor_reading_idle_stress_test.\n")
    dLibObj = getDiagLibObj()

    # initialize the ports if not yet initialized
    cloudripper_init_and_check_all_eloop_modules_presence()

    var_toolName = ('python3 ' + SDK_TOOL)
    stress_time = int(dLibObj.auto_load_script_stress_time)
    var_option = '-c init'
    var_toolPath = get_common_system_sdk_path()
    var_logFile = SDK_LOG_FILE
    var_completeMsg = 'GB Initialization Test'
    var_passMsg = 'GB.*?Initialization Test.*?PASS'
    var_sensorToolName = cel_sensor_test["bin_tool"]
    var_sensorToolOption = '-u'
    var_sensorToolPath = BMC_DIAG_TOOL_PATH
    var_testType = 'idle'
    var_platform = 'cloudripper'

    dLibObj.perform_sensor_reading_loading_stress_test(var_toolName, var_option, var_toolPath, var_logFile, var_completeMsg, var_passMsg, var_sensorToolName, var_sensorToolOption, var_sensorToolPath, var_testType, var_platform)

@logThis
def cloudripper_run_sensor_with_init_stress_test():

    dLibObj = getDiagLibObj()
    var_toolName = 'python3 ' + SDK_TOOL + ' '
    var_option = '-c init'
    var_bmc_path = BMC_DIAG_TOOL_PATH
    var_toolName1 = './cel-sensor-test'
    var_option1 = ' -u'
    var_sdk_path = SYSTEM_SDK_PATH

    return dLibObj.run_sensor_with_init_stress_test(var_toolName, var_option, var_bmc_path, var_toolName1, var_option1, var_sdk_path)

@logThis
def check_psu_connection():
    dLibObj = getDiagLibObj()

    devicename = os.environ.get("deviceName", "")
    if 'wedge' in devicename.lower():
        Log_Info('Do not support wedge unit, skip!')
        return

    var_toolName = PSU_TEST_UTIL
    var_option = ' -s'
    var_pattern = psu_connection_pattern
    var_toolPath = BMC_DIAG_TOOL_PATH

    return dLibObj.check_psu_slot_connection_test(var_toolName, var_option, var_pattern, var_toolPath)

def cloudripper_run_sdk_re_init_test():
    Log_Debug("Entering procedure cloudripper_run_sdk_re_init_test.\n")
    dLibObj = getDiagLibObj()

    # initialize the ports if not yet initialized
    cloudripper_init_and_check_all_eloop_modules_presence

    var_cycle = dLibObj.re_init_cycles
    var_stress_time = dLibObj.re_init_stress_time
    var_toolPath = get_common_system_sdk_path()

    return dLibObj.SDK_re_init_test(var_cycle, var_stress_time, var_toolPath)


def cloudripper_run_port_enable_disable_test():
    Log_Debug("Entering procedure cloudripper_run_port_enable_disable_test.\n")
    dLibObj = getDiagLibObj()

    # initialize the ports if not yet initialized
    cloudripper_init_and_check_all_eloop_modules_presence()

    # python3 auto_load_user.py -c linkup -l 2
    # total test time for 2 cycles = ~ 2270 seconds
    var_sdkTool = SDK_TOOL
    var_stress_cycles = dLibObj.port_linkup_stress_cycles
    var_sdkOptions = ('-c linkup -l %s' %(var_stress_cycles))
    var_toolPath = get_common_system_sdk_path()

    dLibObj.perform_port_enable_disable_stress_test(var_sdkTool, var_sdkOptions, var_toolPath, var_stress_cycles)


def cloudripper_run_eeprom_access_stress_test():
    Log_Debug("Entering procedure cloudripper_run_eeprom_access_stress_test.\n")
    dLibObj = getDiagLibObj()

    # initialize the ports if not yet initialized
    #cloudripper_init_and_check_all_eloop_modules_presence()

    var_initTool = SDK_TOOL
    var_initOption = '-c init'
    var_initToolPath = get_common_system_sdk_path()
    var_resetTool = cel_qsfp_tool
    var_resetOption1 = '-port=0 --reset=on'
    var_resetOption2 = '-port=0 --reset=off'
    var_resetToolPath = DIAG_TOOL_PATH
    var_toolName = cel_eeprom_stress_tool
    var_option = '10 58 2970 3630 1'
    #var_stress_time = dLibObj.eeprom_stress_time
    var_toolPath = UTILITY_TOOL_PATH
    var_pattern1 = cel_temp_volt_limit_pattern1
    #var_pattern2 = cel_temp_volt_limit_pattern2
    #var_pattern3 = cel_temp_volt_limit_pattern3
    #var_pattern4 = cel_temp_volt_limit_start_pattern

    return dLibObj.perform_eeprom_access_stress_test(var_initTool, var_initOption, var_initToolPath, var_resetTool, var_resetOption1, var_resetOption2, var_resetToolPath, var_toolName, var_option, var_toolPath, var_pattern1)

def come_side_driver_auto_load_check():
    Log_Debug("Entering procedure come_side_driver_auto_load_check.\n")
    dLibObj = getDiagLibObj()
    var_toolName = ipmi_toolName
    var_option = DRIVE_LOAD
    var_expect = BMC_DEVICE_ID
    return dLibObj.driver_auto_load_check(var_toolName, var_option, var_expect)

def come_side_sdk_traffic_check():
    Log_Debug("Entering procedure come_side_sdk_traffic_check.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'wedge400_' in devicename.lower():
        w400_run_snake_traffic_test()
    elif 'wedge400c' in devicename.lower():
        wedge400c_run_snake_traffic_test()
    elif 'minipack2' in devicename.lower():
        # minipack2_run_snake_traffic_test()
        #1. init sdk
        mp2_sdk_init_quick()
        #2. run sdk and check traffic
        var_toolName = W400_SDK_TOOL
        var_vlanTool = minipack2_set_vlan_cmd
        var_portStatus = 'ps cd'
        var_clearTool = 'clear c'
        var_trafficCmd = minipack2_start_cpu_traffic_cmd
        var_stress_time = dLibObj.snake_traffic_test_time
        var_stopTraffic = minipack2_stop_cpu_traffic_cmd
        var_counterTool = mp2_traffic_counter
        var_sdkToolLst = [var_toolName, var_vlanTool, var_portStatus, var_clearTool, var_trafficCmd, var_stopTraffic]
        return dLibObj.run_mp2_come_side_sdk_traffic_check(var_sdkToolLst, var_stress_time, var_counterTool)

def fw_version_check_in_come_side():
    Log_Debug("Entering procedure fw_version_check_in_come_side.\n")
    dLibObj = getDiagLibObj()
    var_toolName = diag_cpu_bios_ver_bin
    var_option = '--show'
    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        DOMFPGA1_Ver = FPGA_Ver["DOMFPGA1"]
        DOMFPGA2_Ver = FPGA_Ver["DOMFPGA2"]
        SCM_Ver = CPLD_Ver['scm']
        SMB_Ver = CPLD_Ver['smb']
        wedge_show_version = {
            "Diag Version": DIAG_Ver,
            "OS Diag": DIAG_OS,
            "BIOS Version": BIOS_Ver,
            "FPGA1 Version": DOMFPGA1_Ver,
            "FPGA2 Version": DOMFPGA2_Ver,
            "SCM CPLD Version": SCM_Ver,
            "SMB CPLD Version": SMB_Ver,
            "I210 FW Version": I210_Ver
        }
        var_pattern = cel_wedge_version_show_pattern
        var_expect = wedge_show_version
    else:
        FPGA_Driver_Ver = SwImage.getSwImage(SwImage.FPGA_DRIVER).newVersion
        IOB_FPGA_Ver = FPGA_Ver["SMB_IOB_FPGA"]
        PIM1_DOMFPGA_Ver = FPGA_Ver["PIM1 DOMFPGA"]
        PIM2_DOMFPGA_Ver = FPGA_Ver["PIM2 DOMFPGA"]
        PIM3_DOMFPGA_Ver = FPGA_Ver["PIM3 DOMFPGA"]
        PIM4_DOMFPGA_Ver = FPGA_Ver["PIM4 DOMFPGA"]
        PIM5_DOMFPGA_Ver = FPGA_Ver["PIM5 DOMFPGA"]
        PIM6_DOMFPGA_Ver = FPGA_Ver["PIM6 DOMFPGA"]
        PIM7_DOMFPGA_Ver = FPGA_Ver["PIM7 DOMFPGA"]
        PIM8_DOMFPGA_Ver = FPGA_Ver["PIM8 DOMFPGA"]
        mp2_show_version = {
            "Diag Version": DIAG_Ver,
            "OS Diag": DIAG_OS,
            "SDK Diag": SDK_Ver,
            "BIOS Version": BIOS_Ver,
            "BIOS boot": BIOS_boot_type,
            "FPGA driver version": FPGA_Driver_Ver,
            "FPGA IOB": IOB_FPGA_Ver,
            "PIM 1 DOM": PIM1_DOMFPGA_Ver,
            "PIM 2 DOM": PIM2_DOMFPGA_Ver,
            "PIM 3 DOM": PIM3_DOMFPGA_Ver,
            "PIM 4 DOM": PIM4_DOMFPGA_Ver,
            "PIM 5 DOM": PIM5_DOMFPGA_Ver,
            "PIM 6 DOM": PIM6_DOMFPGA_Ver,
            "PIM 7 DOM": PIM7_DOMFPGA_Ver,
            "PIM 8 DOM": PIM8_DOMFPGA_Ver,
            "I210 FW Version": I210_Ver
        }
        var_pattern = cel_mp2_version_show_pattern
        var_expect = mp2_show_version

    switch_to_centos_diag_tool()
    return dLibObj.run_fw_version_check_in_come_side(var_toolName, var_option, var_pattern, var_expect)

def pcie_and_disk_scan_test_in_come_side():
    Log_Debug("Entering procedure minipack2_run_chassis_power_cycle_test.\n")
    dLibObj = getDiagLibObj()
    var_toolName = PCIE_TOOL
    var_pcieNum_Tool = PCIE_NUM
    var_fdiskTool = fdisk_tool
    devicename = os.environ.get("deviceName", "")
    if 'wedge400_' in devicename.lower():
        var_pcieNum = wedge_pcie_num
        var_pcie_bus= [ SCAN_BUS_05, SCAN_BUS_06, SCAN_BUS_07, SCAN_BUS_08 ]
        var_bus_pattern = [wedge_bus_05, wedge_bus_06, wedge_bus_07, wedge_bus_08]
    elif 'wedge400c' in devicename.lower():
        var_pcieNum = wedge_pcie_num
        var_pcie_bus = [SCAN_BUS_05, SCAN_BUS_06, SCAN_BUS_07, SCAN_BUS_08]
        var_bus_pattern = [wedge_bus_05, w400c_bus_06, wedge_bus_07, wedge_bus_08]
    else:
        var_pcieNum = mp2_pcie_num
        var_pcie_bus = [SCAN_BUS_06, SCAN_BUS_07, SCAN_BUS_08]
        var_bus_pattern = [mp2_bus_06, mp2_bus_07, mp2_bus_08]

    return dLibObj.run_pcie_and_disk_scan_test_in_come_side(var_toolName, var_pcieNum_Tool, var_pcieNum, var_pcie_bus, var_bus_pattern, var_fdiskTool)

def switch_unit_mode(mode):
    Log_Debug("Entering procedure switch_unit_mode.\n")
    if mode == 'openbmc':
        switch_to_openbmc()
    elif mode == 'centos':
        switch_to_centos()

def ipv6_ping_test(mode):
    Log_Debug("Entering procedure ipv6_ping_test.\n")
    dLibObj = getDiagLibObj()
    switch_unit_mode(mode)
    var_toolName = ETH_TOOL
    var_ethNum = var_toolName + ' |grep eth0: |wc -l'
    var_usb0Num = var_toolName + ' |grep usb0 |wc -l'

    return dLibObj.run_ipv6_ping_test(var_toolName,var_ethNum, var_usb0Num)

def current_version_check_in_bmc_side(mode):
    Log_Debug("Entering procedure current_version_check_in_bmc_side.\n")
    dLibObj = getDiagLibObj()
    switch_unit_mode(mode)
    var_toolName = fw_util_tool
    var_option = ' scm --version'
    var_bmc_ver_tool = 'cat /etc/issue'
    var_boot_util = boot_info_util
    Expect_bmc_ver = get_new_image_version('BMC')

    return dLibObj.run_current_version_check_in_bmc_side(var_toolName, var_option, var_bmc_ver_tool, var_boot_util, Expect_bmc_ver)

def sensor_info_check_in_bmc_side():
    Log_Debug("Entering procedure sensor_info_check_in_bmc_side.\n")
    dLibObj = getDiagLibObj()
    var_toolName = SENSOR_UTIL
    var_option = ' all'
    var_pattern = SENSOR_PATTERN
    var_expect = 'ok'

    return dLibObj.run_sensor_info_check_in_bmc_side(var_toolName, var_option, var_pattern, var_expect)

def fru_info_check_in_bmc_side():
    Log_Debug("Entering procedure sensor_info_check_in_bmc_side.\n")
    dLibObj = getDiagLibObj()
    var_weutil_tool = WEUTIL_TOOL  #for wedge:smb, mp2:sim
    var_feutil_tool = FEUTIL_TOOL  #for fcm/fan
    var_seutil_tool = SEUTIL_TOOL  #for scm
    var_peutil_tool = PEUTIL_TOOL  #for mp2 pim
    #eeprom path
    var_sim_path = SIM_EEPROM_PATH
    var_fcmT_path = FCMT_EEPROM_PATH
    var_fcmB_path = FCMB_EEPROM_PATH
    var_fan_path = FAN_EEPROM_PATH
    var_scm_path = SCM_EEPROM_PATH
    var_pim_path = PIM_EEPROM_PATH
    var_eeprom_path = EEPROM_PATH  #for wedge eeprom path

    var_eeprom_tool = EEPROM_TOOL
    var_fan_eeprom_tool = FAN_EEPROM_TOOL

    var_tool_lst = [var_weutil_tool, var_feutil_tool, var_seutil_tool, var_peutil_tool]
    var_tool_path_lst = [var_sim_path, var_fcmT_path, var_fcmB_path, var_fan_path, var_scm_path, var_pim_path, var_eeprom_path]

    return dLibObj.run_fru_info_check_in_bmc_side(var_tool_lst, var_tool_path_lst, var_eeprom_tool, var_fan_eeprom_tool)

def power_cycle_chassis_test(mode):
    Log_Debug("Entering procedure power_cycle_chassis_test.\n")
    dLibObj = getDiagLibObj()
    switch_unit_mode(mode)
    var_toolName = WEDGE400_POWER_RESET
    var_option = ' reset -s'
    return dLibObj.run_power_cycle_chassis_test(var_toolName, var_option)

def power_on_and_off_test(mode, var_toolName):
    Log_Debug("Entering procedure power_on_and_off_test.\n")
    dLibObj = getDiagLibObj()
    switch_unit_mode(mode)
    #var_toolName = WEDGE400_POWER_RESET
    var_option1 = ' on'
    var_option2 = ' off'
    return dLibObj.run_power_on_and_off_test(var_toolName, var_option1, var_option2)

def warm_reset_sdk_traffic_check(mode):
    Log_Debug("Entering procedure warm_reset_sdk_traffic_check.\n")
    dLibObj = getDiagLibObj()
    switch_unit_mode(mode)
    devicename = os.environ.get("deviceName", "")
    if 'wedge400c' in devicename.lower():
        var_toolName = SDK_TOOL
        var_toolPath = get_common_system_sdk_path()
        var_stress_time = dLibObj.snake_traffic_test_time
        var_portMode = 'dd_8x50g_qsfp_4x50g'
        return dLibObj.run_warm_reset_sdk_traffic_check(var_toolName, var_toolPath, var_stress_time, var_portMode)
    elif 'wedge400_' in devicename.lower():
        var_bcmTool = BCMTOOL
        var_toolPath = get_common_system_sdk_path()
        var_toolName = W400_SDK_TOOL
        var_option = ' -df temp.txt'
        var_catTool = 'cat temp.txt'
        var_clsTool = CLSTOOL
        var_trafficTool = w400_set_vlan_cmd
        return dLibObj.run_warm_reset_sdk_traffic_check_w400(var_bcmTool, var_toolPath, var_toolName, var_option, var_catTool, var_clsTool, var_trafficTool)
    elif 'minipack2' in devicename.lower():
        var_bcmTool = BCMTOOL
        var_xphybackTool = xphyback
        var_xphyTool = xphy_tool
        var_init_options = xphy_init_all_pims
        var_toolName = W400_SDK_TOOL
        var_option = ' -df temp.txt'
        var_catTool = 'tail -n +2 temp.txt'
        var_clearTool = truncateTool
        var_toolLst = [var_bcmTool, var_xphybackTool, var_xphyTool, var_init_options, var_catTool, var_clearTool]
        var_toolPath = minipack2_get_current_system_sdk_path()
        var_clsTool = CLSTOOL
        var_vlanTool = minipack2_set_vlan_cmd
        var_trafficTool = minipack2_start_cpu_traffic_cmd
        var_trafficLst = [var_clsTool, var_vlanTool, var_trafficTool]
        return dLibObj.run_warm_reset_sdk_traffic_check_mp2(var_toolName, var_option, var_toolPath, var_toolLst, var_trafficLst)

def come_warm_reset_test(mode):
    Log_Debug("Entering procedure warm_reset_sdk_traffic_check.\n")
    dLibObj = getDiagLibObj()
    switch_unit_mode(mode)
    var_toolName = 'reboot'
    return dLibObj.run_come_warm_reset_test(var_toolName)

def copy_sdk_soc_files_for_BCM(mode):
    Log_Debug("Entering procedure copy_sdk_soc_files_for_BCM.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'wedge400_' in devicename.lower() or 'minipack2' in devicename.lower():
        switch_unit_mode(mode)
        var_username = scp_username
        var_password = scp_password
        var_server_ip = scp_ipv6
        eth_tool = 'ifconfig eth0'
        dhcp_tool = 'dhclient -6 eth0'
        var_filepath = sdk_host_soc_dir_w400
        if 'minipack2' in devicename.lower():
            var_destination_path = sdk_working_dir + '/v*'
        else:
            var_destination_path = sdk_working_dir

        return dLibObj.run_copy_sdk_soc_files_for_BCM(eth_tool, dhcp_tool, var_server_ip, var_username, var_password, var_filepath,
                                   var_destination_path)

def check_scm_fw_version():
    Log_Debug("Entering procedure check_scm_fw_version.\n")
    dLibObj = getDiagLibObj()
    var_toolName = fw_util_tool
    var_option = ' scm --version'
    var_bmc_ver_tool = 'cat /etc/issue'
    Expect_bmc_ver = get_new_image_version('BMC')
    var_scm_pattern = scm_version_pattern
    var_scm_expect = get_new_image_version('SCM')

    return dLibObj.run_check_scm_fw_version(var_toolName, var_option, var_scm_pattern, var_scm_expect, var_bmc_ver_tool, Expect_bmc_ver)

def check_bmc_or_bios_master_status(image):
    Log_Debug("Entering procedure check_bmc_or_bios_master_status.\n")
    dLibObj = getDiagLibObj()
    var_toolName = boot_info_util
    if image == 'BMC':
        var_option = ' bmc'
        var_pattern = bmcModePattern
        var_expect = BMC_boot_type
    elif image == 'BIOS':
        var_option = ' bios'
        var_pattern = r'^([m|s]\w+)'
        var_expect = BIOS_boot_type
    return dLibObj.run_check_bmc_or_bios_master_status(var_toolName, var_option, var_pattern, var_expect)

def fw_update_check(status, image):
    Log_Debug("Entering procedure fw_update_check.\n")
    dLibObj = getDiagLibObj()
    if status == 'low':
        Log_Info('%s will do downgrade fw!'%(image))
        if image == 'BIOS':
            fw_util_exec_bios_downgrade()
            verify_bios_downgrade_version()
        elif image == 'BIC':
            fw_util_exec_bic_downgrade()
            time.sleep(5)
            power_cycle_chassis_test('openbmc')
            verify_bic_downgrade_version()
        elif image == 'BMC':
            flash_downgrade_bmc()
            time.sleep(5)
            CommonLib.reboot(openbmc_mode)
            check_bmc_downgrade_version()
    elif status == 'high':
        Log_Info('%s will do upgrade fw!'%(image))
        if image == 'BIOS':
            fw_util_exec_bios_upgrade()
            verify_bios_upgrade_version()
        elif image == 'BIC':
            fw_util_exec_bic_upgrade()
            time.sleep(5)
            power_cycle_chassis_test('openbmc')
            verify_bic_upgrade_version()
        elif image == 'BMC':
            flash_upgrade_bmc()
            time.sleep(5)
            CommonLib.reboot(openbmc_mode)
            check_bmc_upgrade_version()

def copy_image_file(mode, image):
    Log_Debug("Entering procedure copy_image_file.\n")
    dLibObj = getDiagLibObj()
    switch_unit_mode(mode)
    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    eth_tool = 'ifconfig eth0'
    dhcp_tool = 'dhclient -6 eth0'
    var_HostFilePath = get_host_image_path(image)
    var_LocalFilePath = get_local_image_path(image)
    if (image == 'BIOS') or (image == 'BIC') or (image == 'BMC'):
        var_oldImage = get_old_image_name(image)
        var_newImage = get_new_image_name(image)
        ImageLst = [var_oldImage, var_newImage]
    elif image == 'CPLD':
        fcmLst = get_sub_image_list(image, 'fcm')
        scmLst = get_sub_image_list(image, 'scm')
        smbLst = get_sub_image_list(image, 'smb')
        pwrLst = get_sub_image_list(image, 'pwr')
        ImageLst = [fcmLst[0], fcmLst[1], scmLst[0], scmLst[1], smbLst[0], smbLst[1], pwrLst[0], pwrLst[1]]

    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        if image == 'FPGA':
            var_oldImage = get_old_image_name(image)
            var_newImage = get_new_image_name(image)
            ImageLst = [var_oldImage, var_newImage]
    elif 'minipack2' in devicename.lower():
        if image == 'FPGA':
            iobLst = get_sub_image_list(image, 'iob')
            pimLst = get_sub_image_list(image, 'pim')
            ImageLst = [iobLst[0], iobLst[1], pimLst[0], pimLst[1]]

    return dLibObj.run_copy_image_file(image, eth_tool, dhcp_tool, var_server_ip, var_username, var_password, var_HostFilePath, var_LocalFilePath, ImageLst)

def check_all_fw_version():
    Log_Debug("Entering procedure check_all_fw_version.\n")
    dLibObj = getDiagLibObj()
    var_toolName = fw_util_tool
    var_option = fw_util_optionStr
    bmcDict = {}
    cpldVerDict = {}
    var_bmc_ver = get_new_image_version('BMC')
    bmcDict['BMC Version'] = var_bmc_ver
    cpldVer = get_new_image_version('CPLD')
    fpgaVer = get_new_image_version('FPGA')
    scmVer = get_new_image_version('SCM')
    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        var_all_pattern = wedge_all_version_pattern + scm_version_pattern
        for key, value in cpldVer.items():
            if key == 'fcm':
                cpldVerDict['FCMCPLD'] = cpldVer[key]
            elif key == 'pwr':
                cpldVerDict['PWRCPLD'] = cpldVer[key]
            elif key == 'scm':
                cpldVerDict['SCMCPLD'] = cpldVer[key]
            elif key == 'smb':
                cpldVerDict['SMBCPLD'] = cpldVer[key]
        cpldVer = cpldVerDict
    elif 'minipack2' in devicename.lower():
        var_all_pattern = mp2_all_version_pattern + scm_version_pattern
        for key, value in fpgaVer.items():
            if key == 'SMB_IOB_FPGA':
                fpgaVer['IOB FPGA'] = fpgaVer[key]
                del fpgaVer[key]

    bmcDict.update(cpldVer)
    bmcDict.update(fpgaVer)
    bmcDict.update(scmVer)
    var_all_expect = bmcDict
    return dLibObj.run_check_all_fw_version(var_toolName, var_option, var_all_pattern, var_all_expect)

def cpld_old_fw_version_check(image):
    Log_Debug("Entering procedure cpld_old_fw_version_check.\n")
    expectVerDict = {}
    var_smbVer = get_old_sub_image_version(image, 'smb')
    var_fcmVer = get_old_sub_image_version(image, 'fcm')
    var_pwrVer = get_old_sub_image_version(image, 'pwr')
    var_scmVer = get_old_sub_image_version(image, 'scm')
    expectVerDict['SMB_SYSCPLD'] = var_smbVer
    expectVerDict['FCMCPLD'] = var_fcmVer
    expectVerDict['SMB_PWRCPLD'] = var_pwrVer
    expectVerDict['SCMCPLD'] = var_scmVer
    return expectVerDict

def cpld_new_fw_version_check(image):
    Log_Debug("Entering procedure cpld_new_fw_version_check.\n")
    expectVerDict = {}
    var_smbVer = get_new_sub_image_version(image, 'smb')
    var_fcmVer = get_new_sub_image_version(image, 'fcm')
    var_pwrVer = get_new_sub_image_version(image, 'pwr')
    var_scmVer = get_new_sub_image_version(image, 'scm')
    expectVerDict['SMB_SYSCPLD'] = var_smbVer
    expectVerDict['FCMCPLD'] = var_fcmVer
    expectVerDict['SMB_PWRCPLD'] = var_pwrVer
    expectVerDict['SCMCPLD'] = var_scmVer
    return expectVerDict

def fw_online_update_check(status, image):
    Log_Debug("Entering procedure fw_online_update_check.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    var_imagePath = get_local_image_path(image)
    if image == 'CPLD':
        if 'minipack2' in devicename.lower():
            var_toolName = mp2_cpld_version_tool
            var_toolLst = mp2_cpld_update_tool
            var_option = 'sw'
        elif 'wedge400' in devicename.lower():
            var_toolName = cpld_version_tool
            var_smbTool = smb_cpld_tool
            var_fcmTool = fcm_cpld_tool
            var_pwrTool = pwr_cpld_tool
            var_scmTool = scm_cpld_tool
            var_option = 'hw'
            var_toolLst = [var_smbTool, var_fcmTool, var_pwrTool, var_scmTool]
        if status == 'low':
            var_smbImage = get_old_sub_image_name(image, 'smb')
            var_fcmImage = get_old_sub_image_name(image, 'fcm')
            var_pwrImage = get_old_sub_image_name(image, 'pwr')
            var_scmImage = get_old_sub_image_name(image, 'scm')
            if 'wedge400' in devicename.lower():
                var_expect = cpld_old_fw_version_check(image)
            elif 'minipack2' in devicename.lower():
                var_expect = get_old_image_version(image)
        elif status == 'high':
            var_smbImage = get_new_sub_image_name(image, 'smb')
            var_fcmImage = get_new_sub_image_name(image, 'fcm')
            var_pwrImage = get_new_sub_image_name(image, 'pwr')
            var_scmImage = get_new_sub_image_name(image, 'scm')
            if 'wedge400' in devicename.lower():
                var_expect = cpld_new_fw_version_check(image)
            elif 'minipack2' in devicename.lower():
                var_expect = get_new_image_version(image)
        var_imageLst = [var_smbImage, var_fcmImage, var_pwrImage, var_scmImage]
        var_pattern = fcm_update_pattern
    elif image == 'FPGA':
        if 'minipack2' in devicename.lower():
            var_toolName = mp2_fpga_version_tool
            var_toolLst = mp2_fpga_update_tool_lst
        elif 'wedge400' in devicename.lower():
            var_toolName = fpga_ver_tool
            var_toolLst = fpga_update_tool_lst
        if status == 'low':
            var_image = get_old_image_name(image)
            if 'wedge400' in devicename.lower():
                var_expect = get_old_image_version(image)
                var_imageLst = [var_image]
            elif 'minipack2' in devicename.lower():
                var_imageLst = [var_image['pim'], var_image['iob']]
                fpgaVer = get_old_image_version(image)
                for key, value in fpgaVer.items():
                    if key == 'SMB_IOB_FPGA':
                        fpgaVer['IOB FPGA'] = fpgaVer[key]
                        del fpgaVer[key]
                var_expect = fpgaVer
        elif status == 'high':
            var_image = get_new_image_name(image)
            if 'wedge400' in devicename.lower():
                var_expect = get_new_image_version(image)
                var_imageLst = [var_image]
            elif 'minipack2' in devicename.lower():
                var_imageLst = [var_image['pim'], var_image['iob']]
                fpgaVer = get_new_image_version(image)
                for key, value in fpgaVer.items():
                    if key == 'SMB_IOB_FPGA':
                        fpgaVer['IOB FPGA'] = fpgaVer[key]
                        del fpgaVer[key]
                var_expect = fpgaVer
        var_option = ''
        var_pattern = fpga_update_pattern
    var_mode = openbmc_mode

    return dLibObj.run_fw_online_update_check(image, var_toolName, var_toolLst, var_imageLst, var_option, var_imagePath, var_pattern, var_expect, var_mode)

def verify_cpld_update_version(status, image):
    Log_Debug("Entering procedure verify_cpld_update_version.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        var_toolName = cpld_version_tool
    elif 'minipack2' in devicename.lower():
        var_toolName = mp2_cpld_version_tool
    var_pattern = r'(.*):[ \t]+(.*)'
    if status == 'low':
        if 'minipack2' in devicename.lower():
            var_expect = get_old_image_version(image)
        else:
            var_expect = cpld_old_fw_version_check(image)
    elif status == 'high':
        if 'minipack2' in devicename.lower():
            var_expect = get_new_image_version(image)
        else:
            var_expect = cpld_new_fw_version_check(image)
    return dLibObj.run_verify_cpld_update_version(var_toolName, var_pattern, var_expect)

def verify_fpga_update_version(status, image):
    Log_Debug("Entering procedure verify_fpga_update_version.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'wedge400' in devicename.lower():
        var_toolName = fpga_ver_tool
    elif 'minipack2' in devicename.lower():
        var_toolName = mp2_fpga_version_tool
    var_pattern = r'(.*):[ \t]+(.*)'
    if status == 'low':
        if 'minipack2' in devicename.lower():
            var_expect = get_old_image_version(image)
        else:
            var_expect = get_old_image_version(image)
    elif status == 'high':
        if 'minipack2' in devicename.lower():
            var_expect = get_new_image_version(image)
        else:
            var_expect = get_new_image_version(image)
    return dLibObj.run_verify_cpld_update_version(var_toolName, var_pattern, var_expect)

def cpld_update_fw_check(status, image):
    Log_Debug("Entering procedure cpld_update_fw_check.\n")
    dLibObj = getDiagLibObj()
    res = fw_online_update_check(status, image)  #1. update fw
    time.sleep(3)
    if res == 'pass':
        power_cycle_chassis_test('openbmc')   #2. power cycle
        time.sleep(3)
        verify_cpld_update_version(status, image)  #3. verify fw version

def fpga_update_fw_check(status, image):
    Log_Debug("Entering procedure fpga_update_fw_check.\n")
    dLibObj = getDiagLibObj()
    res = fw_online_update_check(status, image)  #1. update fw
    time.sleep(3)
    if res == 'pass':
        power_cycle_chassis_test('openbmc')   #2. power cycle
        time.sleep(3)
        verify_fpga_update_version(status, image)  #3. verify fw version

def come_side_idle_check(mode):
    Log_Debug("Entering procedure come_side_idle_check.\n")
    dLibObj = getDiagLibObj()
    switch_unit_mode(mode)
    var_toolName = 'sleep'
    var_option = '300'
    return dLibObj.run_come_side_idle_check(var_toolName, var_option)

def eMMC_check_in_bmc_side():
    Log_Debug("Entering procedure eMMC_check_in_bmc_side.\n")
    dLibObj = getDiagLibObj()
    var_fdiskTool = fdisk_tool
    return dLibObj.run_eMMC_check_in_bmc_side(var_fdiskTool)

def check_system_idle_test():
    Log_Debug("Entering procedure check_system_idle_test.\n")
    dLibObj = getDiagLibObj()
    var_stress_time = dLibObj.snake_traffic_test_time
    var_toolName = 'tail -n 1 mTerm_wedge.log'
    var_log_path = VAR_LOG_PATH
    return dLibObj.run_check_system_idle_test(var_toolName, var_log_path, var_stress_time)

def check_some_log_files(status):
    Log_Debug("Entering procedure check_some_log_files.\n")
    dLibObj = getDiagLibObj()
    var_log_path = VAR_LOG_PATH
    var_mce_tool = 'mcelog'
    var_dmesg_tool = 'dmesg'
    var_stress_time = dLibObj.snake_traffic_test_time
    var_toolName = STRESSAPP_TOOL
    var_option = ' -m 8 -i 8 -C 8 -M -l &'
    return dLibObj.run_check_some_log_files(status, var_toolName, var_option, var_stress_time, var_mce_tool, var_dmesg_tool, var_log_path)

def check_sdk_result_and_exit(sdk_env):
    Log_Debug("Entering procedure check_sdk_result_and_exit.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'wedge400_' in devicename.lower():
        var_sdkToolPath = SYSTEM_SDK_PATH
        var_DDStop_tool = w400_DD_stop_traffic
        var_56Stop_tool = w400_56_stop_traffic
        var_stopTraffic_lst = [var_DDStop_tool, var_56Stop_tool]
        var_counter_tool = w400_traffic_counter
        var_exit_sdk_tool = w400_exit_traffic_cmd
        var_rpkt = w400_rpkt
        var_tpkt = w400_tpkt
        return dLibObj.run_check_sdk_result_and_exit_w400(sdk_env, var_sdkToolPath, var_stopTraffic_lst, var_counter_tool, var_rpkt, var_tpkt, var_exit_sdk_tool)
    elif 'wedge400c' in devicename.lower():
        time.sleep(120)
        var_toolName = 'tail -n 52 temp.txt'
        var_pattern = 'Counters Consistency Check Passed'
        return dLibObj.run_check_sdk_result_and_exit_w400c(sdk_env, var_toolName, var_pattern)
    elif 'minipack2' in devicename.lower():
        var_sdkToolPath = minipack2_get_current_system_sdk_path()
        var_clsTool = CLSTOOL
        var_stopTraffic = minipack2_stop_cpu_traffic_cmd
        var_clearTool = truncateTool
        var_counter_tool = mp2_traffic_counter
        var_exit_sdk_tool = w400_exit_traffic_cmd
        var_catTool = 'tail -n +2 temp.txt'
        var_stopTraffic_lst = [var_clsTool, var_stopTraffic, var_clearTool, var_counter_tool, var_exit_sdk_tool, var_catTool]
        var_pattern = TRAFFIC_PATTERN
        #var_pattern = 'port counters check test PASSED'
        return dLibObj.run_check_sdk_result_and_exit_mp2(sdk_env, var_sdkToolPath, var_stopTraffic_lst, var_pattern)

def check_sol_stress_test():
    Log_Debug("Entering procedure check_sol_stress_test.\n")
    dLibObj = getDiagLibObj()
    var_toolName = 'touch'
    var_path = '/home'
    var_option = 'test.log'
    var_bmc_path = 'ls /var/log/'
    var_bmc_log = 'mTerm_wedge.log'
    return dLibObj.run_check_sol_stress_test(var_toolName, var_option, var_path, var_bmc_path, var_bmc_log)

def clean_log_file(filePath, logfile):
    Log_Debug("Entering procedure clean_log_file.\n")
    dLibObj = getDiagLibObj()
    var_toolName = 'rm -rf'
    return dLibObj.run_clean_log_file(filePath, logfile, var_toolName)

def init_sdk_check():
    Log_Debug("Entering procedure init_skd_check.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower():
        var_bcmTool = BCMTOOL
        var_xphybackTool = xphyback
        var_xphyTool = xphy_tool
        var_init_options = xphy_init_all_pims
        var_toolName = W400_SDK_TOOL
        var_option = ' -df temp.txt'
        var_catTool = 'tail -n +2 temp.txt'
        var_clearTool = truncateTool
        var_clsTool = CLSTOOL
        var_toolLst = [var_bcmTool, var_xphybackTool, var_xphyTool, var_init_options, var_catTool, var_clearTool, var_clsTool]
        var_toolPath = minipack2_get_current_system_sdk_path()
        return dLibObj.run_init_sdk_check(var_toolName, var_option, var_toolPath, var_toolLst)
    elif 'wedge400_' in devicename.lower():
        var_bcmTool = BCMTOOL
        var_toolPath = get_common_system_sdk_path()
        var_toolName = W400_SDK_TOOL
        var_option = ' -df temp.txt'
        var_catTool = 'tail -n +2 temp.txt'
        var_clsTool = CLSTOOL
        var_clearTool = truncateTool
        var_toolLst = [var_bcmTool, var_catTool, var_clsTool, var_clearTool]
        return dLibObj.run_init_sdk_check_w400(var_toolName, var_option, var_toolPath, var_toolLst)

def check_reset_port_link_test():
    Log_Debug("Entering procedure check_reset_port_link_test.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower():
        var_clsTool = CLSTOOL
        var_option = RESET_PMD
        var_catTool = 'tail -n +2 temp.txt'
        var_vlanTool = minipack2_set_vlan_cmd
        var_trafficTool = minipack2_start_cpu_traffic_cmd
        var_stress_time = dLibObj.snake_traffic_test_time
        var_stopTraffic = minipack2_stop_cpu_traffic_cmd
        var_clearTool = truncateTool
        var_counter_tool = mp2_traffic_counter
        var_exit_sdk_tool = w400_exit_traffic_cmd
        var_toolLst = [var_catTool, var_vlanTool, var_trafficTool, var_stopTraffic, var_clearTool, var_counter_tool, var_exit_sdk_tool]
        return dLibObj.run_check_reset_port_link_test(var_clsTool, var_option, var_stress_time, var_toolLst)
    elif 'wedge400_' in devicename.lower():
        var_clsTool = CLSTOOL
        var_option = RESET_PMD_W400
        var_stress_time = dLibObj.snake_traffic_test_time
        var_catTool = 'tail -n +2 temp.txt'
        var_clearTool = truncateTool
        var_vlanTool = w400_set_vlan_cmd
        var_DDTraffic = w400_DD_traffic_cmd
        var_56Traffic = w400_56_traffic_cmd
        var_StopTraffic = w400_stop_cpu_traffic_cmd
        var_counter_tool = w400_traffic_counter
        var_exit_sdk_tool = w400_exit_traffic_cmd
        var_rpkt = w400_rpkt
        var_tpkt = w400_tpkt
        var_toolLst = [var_catTool, var_clearTool, var_vlanTool, var_DDTraffic, var_56Traffic, var_StopTraffic,
                       var_counter_tool, var_exit_sdk_tool, var_rpkt, var_tpkt]
        return dLibObj.run_check_reset_port_link_test_w400(var_clsTool, var_option, var_stress_time, var_toolLst)

def check_qsfp_on_or_off_test():
    Log_Debug("Entering procedure check_qsfp_on_or_off_test.\n")
    dLibObj = getDiagLibObj()
    var_toolName = cel_qsfp_tool
    var_option1 = LPMODE_OFF_TOOL
    var_option2 = RESET_ON_TOOL
    var_option3 = RESET_OFF_TOOL
    var_optionLst = [var_option1, var_option2, var_option3]
    return dLibObj.run_check_qsfp_on_or_off_test(var_toolName, var_optionLst)

def init_sdk_from_remote_shell():
    Log_Debug("Entering procedure init_sdk_from_remote_shell.\n")
    dLibObj = getDiagLibObj()
    var_toolName = W400_SDK_TOOL
    var_option = init_remote_shell
    var_BCMTool = BCMTOOL
    var_clsTool = CLSTOOL
    var_clearTool = truncateTool
    var_psceTool = PS_CE_TOOL
    var_TailTool = TAIL_TOOL
    var_sdkPath = SDK_UTIL_PATH
    var_pattern = upPort_lpmode
    return dLibObj.run_init_sdk_from_remote_shell(var_toolName, var_option, var_BCMTool, var_clsTool, var_clearTool, var_psceTool, var_TailTool, var_sdkPath, var_pattern)


def init_sdk_and_low_power_mode(type):
    Log_Debug("Entering procedure init_sdk_and_low_power_mode.\n")
    dLibObj = getDiagLibObj()
    var_clsTool = CLSTOOL
    var_clearTool = truncateTool
    var_psceTool = PS_CE_TOOL
    var_TailTool = TAIL_TOOL
    var_echoTool = ECHO_TOOL
    var_sqfpTool = cel_qsfp_tool
    var_sdkPath = SDK_UTIL_PATH
    var_diagPath = DIAG_TOOL_PATH
    if type == 'on':
        var_lpmodeTool = LPMODE_ON_TOOL
        var_pattern = downPort_lpmode
    elif type == 'off':
        var_lpmodeTool = LPMODE_OFF_TOOL
        var_pattern = upPort_lpmode
    var_toolLst = [var_clsTool, var_clearTool, var_psceTool, var_TailTool, var_echoTool, var_sqfpTool]
    var_pathLst = [var_sdkPath, var_diagPath]
    return dLibObj.run_init_sdk_and_low_power_mode(var_toolLst, var_pathLst, var_lpmodeTool, var_pattern)

def check_sdk_traffic_test():
    Log_Debug("Entering procedure check_sdk_traffic_test.\n")
    dLibObj = getDiagLibObj()
    var_clsTool = CLSTOOL
    var_option = optical_snake_vlan
    var_stress_time = dLibObj.snake_traffic_test_time
    var_catTool = 'tail -n +2 temp.txt'
    var_clearTool = truncateTool
    var_TrafficTool = traffic_snake
    var_StopTraffic = w400_stop_cpu_traffic_cmd
    var_counter_tool = w400_traffic_counter
    var_echoTool = ECHO_TOOL
    var_exit_sdk_tool = w400_exit_traffic_cmd
    var_rpkt = w400_rpkt
    var_tpkt = w400_tpkt
    var_toolLst = [var_catTool, var_clearTool, var_TrafficTool, var_StopTraffic, var_echoTool,
                       var_counter_tool, var_exit_sdk_tool, var_rpkt, var_tpkt]
    return dLibObj.run_check_sdk_traffic_test(var_clsTool, var_option, var_stress_time, var_toolLst)

def mp2_sdk_init_quick():
    Log_Debug("Entering procedure init_sdk_from_remote_shell.\n")
    dLibObj = getDiagLibObj()
    var_bcmTool = BCMTOOL
    var_xphybackTool = xphyback
    var_xphyTool = xphy_tool
    var_init_options = xphy_init_all_pims
    var_sdkPath = minipack2_get_current_system_sdk_path()
    return dLibObj.run_mp2_sdk_init_quick(var_bcmTool, var_xphybackTool, var_xphyTool, var_init_options, var_sdkPath)

def exit_sdk_env_test():
    Log_Debug("Entering procedure exit_sdk_env_test.\n")
    dLibObj = getDiagLibObj()
    var_clearTool = truncateTool
    var_exit_sdk_tool = w400_exit_traffic_cmd
    return dLibObj.run_exit_sdk_env_test(var_clearTool, var_exit_sdk_tool)


def create_dir(a,b):
    return CommonLib.create_dir(a,b)



def get_dhcp_ip_address(a,b,c):
    return CommonLib.get_dhcp_ip_address(a,b,c)

def download_images(a,b):
    return CommonLib.download_images(a,b)

