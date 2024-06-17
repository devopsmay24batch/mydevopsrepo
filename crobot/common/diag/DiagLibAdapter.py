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
import copy
import ipaddress
import os
from Decorator import *
current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(current_path, 'openbmc'))
sys.path.append(os.path.join(current_path, 'sdk'))
sys.path.append(os.path.join(current_path, '../crobot/legacy'))
import bios_menu_lib
import Const
import CommonLib

###################################################################################
# Common Wrapper Library Functions
###################################################################################
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


def Log_Debug(msg):
    dLibObj = getDiagLibObj()
    dLibObj.wpl_log_debug(msg)


def Log_Info(msg):
    dLibObj = getDiagLibObj()
    dLibObj.wpl_log_info(msg)


def switch_to_centos():
    return CommonLib.switch_to_centos()


def go_to_centos():
    return CommonLib.switch_to_centos()

def retry_to_centos():
    dLibObj = getDiagLibObj()
    return dLibObj.retry_centos()


def switch_to_openbmc():
    return CommonLib.switch_to_openbmc()


def go_to_openbmc():
    return CommonLib.switch_to_openbmc()


def reboot_to_centos():
    return CommonLib.reboot("centos")


def reboot_to_bmc():
    return CommonLib.reboot("openbmc")


def get_dhcp_ipv6_addresses(interface_type, preferred_jenkins_network=True):
    Log_Debug("Entering procedure get_dhcp_ipv6_addresses.\n")
    dLibObj = getDiagLibObj()

    IP_ADDR = []

    switch_to_centos()

    if preferred_jenkins_network == False:
        preferred_network = 'None'
    else:
        # Some machines have multiple IPV6 addresses from different network
        # IPV6 from server, dut centos and dut openbmc must be from the same network in order to ping each other.
        var_server_ip = scp_ipv6
        Log_Info("Using Jenkins IPV6: [%s]" %var_server_ip)

        if re.search(':', var_server_ip):
            slist = var_server_ip.split(':')
            preferred_network = slist[0]
        else:
            dLibObj.wpl_raiseException('Error: Unable to get Jenkins server IPV6 address.')

    # get dhcp IPV6 address in centos
    var_centos_ipAddr = check_centos_ip_address_list(interface_type, preferred_network, True)
    if var_centos_ipAddr is None:
        dLibObj.wpl_raiseException('Error: Unable to get IPV6 address in centos.')

    switch_to_openbmc()

    if preferred_jenkins_network == False:
        if re.search(':', var_centos_ipAddr):
            slist = var_centos_ipAddr.split(':')
            preferred_network = slist[0]
        else:
            dLibObj.wpl_raiseException('Error: Unable to get Jenkins server IPV6 address.')

    # get dhcp IPV6 address in openbmc from same network
    var_openbmc_ipAddr = check_openbmc_ip_address_list(interface_type, preferred_network, True)
    if var_openbmc_ipAddr is None:
        dLibObj.wpl_raiseException('Error: Unable to get IPV6 address in openbmc.')

    if interface_type == 'usb':
        var_interface = openbmc_eth_params['usb_interface']
    else:
        var_interface = openbmc_eth_params['interface']

    IP_ADDR.append(var_centos_ipAddr)
    IP_ADDR.append(var_openbmc_ipAddr)

    Log_Info("Using DUT centos IPV6 address: [%s]" %var_centos_ipAddr)
    Log_Info("Using DUT openbmc IPV6 address: [%s]" %var_openbmc_ipAddr)

    Log_Info("Ping centos ethernet interface from openbmc...")
    ping_ipv6_address(var_interface, var_centos_ipAddr, 'openbmc')

    return IP_ADDR


def check_and_ping_server_ip_from_centos():
    Log_Debug("Entering procedure check_and_ping_server_ip_from_centos.\n")

    check_centos_ip_address()
    var_ipAddr = scp_ip

    return ping_ip_address(var_ipAddr, 'centos')


def check_centos_ip_address():
    Log_Debug("Entering procedure check_centos_ip_address.\n")
    return CommonLib.check_ip_address('DUT', 'eth0', 'centos')


def check_and_ping_server_ipv6_from_centos():
    Log_Debug("Entering procedure check_and_ping_server_ipv6_from_centos.\n")
    dLibObj = getDiagLibObj()

    switch_to_centos()

    # Some machines have multiple IPV6 address from different network
    # IPV6 from server, dut centos and dut openbmc must be from the same network in order to ping each other.
    var_server_ip = scp_ipv6
    if re.search(':', var_server_ip):
        slist = var_server_ip.split(':')
        preferred_network = slist[0]
    else:
        dLibObj.wpl_raiseException('Error: Unable to get Jenkins server IPV6 address.')

    # get dhcp IPV6 address in centos
    var_centos_ipAddr = check_centos_ip_address_list('eth', preferred_network, True)
    if var_centos_ipAddr is None:
         dLibObj.wpl_raiseException('Error: Unable to get IPV6 address in centos.')

    var_interface = centos_eth_params['interface']

    ping_ipv6_address(var_interface, var_server_ip, 'centos')

    return var_centos_ipAddr


def check_centos_ip_address_list(interface_type='eth', preferred_network='None', ipv6=True):
    Log_Debug("Entering procedure check_centos_ip_address_list.\n")
    dLibObj = getDiagLibObj()

    if interface_type == 'eth':
        var_interface = centos_eth_params['interface']
    else:
        var_interface = centos_eth_params['usb_interface']

    var_mode='centos'

    return CommonLib.check_ip_address_list(Const.DUT, var_interface, var_mode, preferred_network, ipv6)


def check_centos_ipv6_address(interface_type='eth'):
    Log_Debug("Entering procedure check_centos_ipv6_address.\n")
    dLibObj = getDiagLibObj()

    if interface_type == 'eth':
        var_interface = centos_eth_params['interface']
    else:
        var_interface = centos_eth_params['usb_interface']

    # Some machines have multiple IPV6 address from different network
    # IPV6 from server, dut centos and dut openbmc must be from the same network in order to ping each other.
    var_server_ip = scp_ipv6
    var_mode = 'centos'
    if re.search(':', var_server_ip):
        slist = var_server_ip.split(':')
        preferred_network = slist[0]
    else:
        dLibObj.wpl_raiseException('Error: Unable to get Jenkins server IPV6 address.')

    return CommonLib.check_ip_address_list(Const.DUT, var_interface, var_mode, preferred_network, True)


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


def check_and_ping_server_ip_from_openbmc():
    Log_Debug("Entering procedure check_and_ping_server_ip_from_openbmc.\n")

    check_openbmc_ip_address()
    var_ipAddr = scp_ip

    return ping_ip_address(var_ipAddr, 'openbmc')


def check_and_ping_server_ipv6_from_openbmc():
    Log_Debug("Entering procedure check_and_ping_server_ipv6_from_openbmc.\n")
    dLibObj = getDiagLibObj()

    # get dhcp IPV6 address in openbmc from same network
    var_openbmc_ipAddr = check_openbmc_ip_address_list('eth', 'None', True)
    if var_openbmc_ipAddr is None:
        dLibObj.wpl_raiseException('Error: Unable to get IPV6 address in openbmc.')

    var_ipAddr = scp_ipv6
    var_interface = openbmc_eth_params['interface']

    return ping_ipv6_address(var_interface, var_ipAddr, 'openbmc')


def check_openbmc_ip_address():
    Log_Debug("Entering procedure check_openbmc_ip_address.\n")
    import CommonLib
    return CommonLib.check_ip_address('DUT', 'eth0', 'openbmc')
    # never user hard coded ip address, it will make all the units have same ip, and it can't work on SVT's units.
    # dLibObj = getDiagLibObj()
    #
    # var_interface=openbmc_eth_params['interface']
    # var_ipAddr=openbmc_eth_params['ipv4']
    # var_netmask=openbmc_eth_params['netmask']
    # var_ethStatus=openbmc_eth_params['status']
    # var_mode='openbmc'
    #
    # return dLibObj.check_ip_address(var_interface, var_ipAddr, var_netmask, var_ethStatus, var_mode)


def check_and_ping_centos_ipv6_from_openbmc():
    Log_Debug("Entering procedure check_and_ping_centos_ipv6_from_openbmc.\n")

    check_openbmc_ipv6_address()
    var_ipAddr = check_centos_ipv6_address()
    var_interface = openbmc_eth_params['interface']

    return ping_ipv6_address(var_interface, var_ipAddr, 'openbmc')


def check_openbmc_ip_address_list(interface_type='eth', preferred_network='None', ipv6=True):
    Log_Debug("Entering procedure check_openbmc_ip_address_list.\n")
    dLibObj = getDiagLibObj()

    if interface_type == 'eth':
        var_interface = openbmc_eth_params['interface']
    else:
        var_interface = openbmc_eth_params['usb_interface']

    var_mode='openbmc'

    return CommonLib.check_ip_address_list(Const.DUT, var_interface, var_mode, preferred_network, ipv6)


def check_openbmc_ipv6_address(interface_type='eth'):
    Log_Debug("Entering procedure check_openbmc_ipv6_address.\n")
    dLibObj = getDiagLibObj()

    if interface_type == 'eth':
        var_interface = openbmc_eth_params['interface']
    else:
        var_interface = openbmc_eth_params['usb_interface']

    # Some machines have multiple IPV6 address from different network
    # IPV6 from server, dut centos and dut openbmc must be from the same network in order to ping each other.
    var_server_ip = scp_ipv6
    var_mode='openbmc'
    if re.search(':', var_server_ip):
        slist = var_server_ip.split(':')
        preferred_network = slist[0]
    else:
        dLibObj.wpl_raiseException('Error: Unable to get Jenkins server IPV6 address.')

    return CommonLib.check_ip_address_list(Const.DUT, var_interface, var_mode, preferred_network, True)


def copy_bmc_files():
    Log_Debug("Entering procedure copy_bmc_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    var_filelist = bmc_package_copy_list
    var_filepath = scp_bmc_filepath
    var_destination_path = bmc_img_path
    var_mode = openbmc_mode
    # Don't ping to/from BMC <-> COMe
    # Because the file is copy from the SCP server, not the IP on above
    # get_dhcp_ipv6_addresses('eth')
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
    var_server_ip = scp_ipv6
    var_filelist = bios_package_copy_list
    var_filepath = scp_bios_filepath
    var_destination_path = bios_img_path
    var_mode = openbmc_mode
    # Don't ping to/from BMC <-> COMe
    # Because the file is copy from the SCP server, not the IP on above
    # get_dhcp_ipv6_addresses('eth')
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
    var_server_ip = scp_ipv6
    var_filelist = th3_package_copy_list
    var_filepath = scp_th3_filepath
    var_destination_path = th3_img_path
    var_mode=openbmc_mode
    # make sure ipv6 available
    get_dhcp_ipv6_addresses('eth')
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def copy_fpga_files(file_list="fpga_package_copy_list"):
    Log_Debug("Entering procedure copy_fpga_files.\n")
    dLibObj = getDiagLibObj()
    if file_list == "fpga_package_copy_list":
        file_list = fpga_package_copy_list

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    var_filelist = file_list
    var_filepath = scp_fpga_filepath
    var_destination_path = fpga_img_path
    var_mode = openbmc_mode
    # Don't ping to/from BMC <-> COMe
    # Because the file is copy from the SCP server, not the IP on above
    # get_dhcp_ipv6_addresses('eth')
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
    var_server_ip = scp_ipv6
    var_filelist = bic_package_copy_list
    var_filepath = scp_bic_filepath
    var_destination_path = bic_img_path
    var_mode = openbmc_mode
    # Don't ping to/from BMC <-> COMe
    # Because the file is copy from the SCP server, not the IP on above
    # get_dhcp_ipv6_addresses('eth')
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output

def minipack2_copy_bic_files():
    Log_Debug("Entering procedure minipack2_copy_bic_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    var_filelist = bic_package_copy_list
    var_filepath = scp_bic_filepath
    var_destination_path = bic_img_path
    var_mode = openbmc_mode
    # make sure ipv6 available
    get_dhcp_ipv6_addresses('eth')
    var_interface = minipack2_openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output

def copy_fcm_files():
    Log_Debug("Entering procedure copy_fcm_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    var_filelist = fcm_package_copy_list
    var_filepath = scp_fcm_filepath
    var_destination_path = fcm_img_path
    var_mode = openbmc_mode
    # Don't ping to/from BMC <-> COMe
    # Because the file is copy from the SCP server, not the IP on above
    # get_dhcp_ipv6_addresses('eth')
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
    var_server_ip = scp_ipv6
    var_filelist = scm_package_copy_list
    var_filepath = scp_scm_filepath
    var_destination_path = scm_img_path
    var_mode = openbmc_mode
    # Don't ping to/from BMC <-> COMe
    # Because the file is copy from the SCP server, not the IP on above
    # get_dhcp_ipv6_addresses('eth')
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
    var_server_ip = scp_ipv6
    var_filelist = smb_package_copy_list
    var_filepath = scp_smb_filepath
    var_destination_path = smb_img_path
    var_mode = openbmc_mode
    # Don't ping to/from BMC <-> COMe
    # Because the file is copy from the SCP server, not the IP on above
    # get_dhcp_ipv6_addresses('eth')
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
    var_server_ip = scp_ipv6
    var_filelist = pwr_package_copy_list
    var_filepath = scp_pwr_filepath
    var_destination_path = pwr_img_path
    var_mode = openbmc_mode
    # Don't ping to/from BMC <-> COMe
    # Because the file is copy from the SCP server, not the IP on above
    # get_dhcp_ipv6_addresses('eth')
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def copy_oob_image_files():
    Log_Debug("Entering procedure copy_oob_image_files.\n")
    dLibObj = getDiagLibObj()

    var_username=scp_username
    var_password=scp_password
    var_server_ip=scp_ip
    var_filelist=oob_package_copy_list
    var_filepath=scp_oob_filepath
    var_destination_path=oob_img_path
    var_mode=openbmc_mode
    # make sure ipv6 available
    get_dhcp_ipv6_addresses('eth')
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


def switch_to_centos_diag_system_log():
    Log_Debug("Entering procedure switch_to_centos_diag_system_log.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.switch_to_centos_and_go_to_diag_system_log_path()


def switch_to_openbmc_check_tool():
    Log_Debug("Entering procedure switch_to_openbmc_check_tool.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.switch_to_openbmc_and_check_tool()


def run_mcelog_under_daemon_mode():
    Log_Debug("Entering procedure run_mcelog_under_daemon_mode.\n")
    dLibObj = getDiagLibObj()

    var_cmd = cel_cpu_power_stress_test_mcelog_array["bin_cmd"]
    var_option = "--daemon"

    return dLibObj.switch_mcelog_to_daemon_mode(var_cmd, var_option)


def test_cpu_power_stress():
    Log_Debug("Entering procedure test_cpu_power_stress.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_cpu_power_stress_array["bin_tool"]
    var_log_1 = cel_cpu_power_stress_array["log_message_1"]
    var_log_2 = cel_cpu_power_stress_array["log_message_2"]

    return dLibObj.test_cpu_power_stress_and_check_status(var_toolName, var_log_1, var_log_2)


def test_cpu_stress():
    Log_Debug("Entering procedure test_cpu_stress.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_cpu_power_stress_array["cpu_stress_tool"]
    var_log_1 = cel_cpu_power_stress_array["log_message_1"]
    var_log_2 = cel_cpu_power_stress_array["log_message_2"]

    return dLibObj.test_cpu_stress_and_check_status(var_toolName, var_log_1, var_log_2)


def test_ssd_stress():
    Log_Debug("Entering procedure test_ssd_stress.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_ssd_stress_test_array["bin_tool"]
    var_run_time = cel_ssd_stress_test_array["run_time"]
    var_log_file = cel_ssd_stress_test_array["log_file"]

    return dLibObj.test_ssd_stress_and_check_status(var_toolName, var_run_time, var_log_file)


def test_lpmode_stress():
    Log_Debug("Entering procedure test_lpmode_stress.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_lpmode_stress_test_array["bin_tool"]
    var_option = cel_lpmode_stress_test_array["option"]
    var_run_time = cel_lpmode_stress_test_array["run_time"]

    return dLibObj.test_lpmode_stress_and_check_status(var_toolName, var_option, var_run_time)


def check_MCE_log():
    Log_Debug("Entering procedure check_MCE_log.\n")
    dLibObj = getDiagLibObj()

    var_cmd_str = "cat /var/log/mcelog | grep error"

    return dLibObj.view_and_check_the_mce_log(var_cmd_str)


def test_ddr_stress():
    Log_Debug("Entering procedure test_ddr_stress.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_DDR_stress_test_array
    var_toolName = cel_DDR_stress_test_array["bin_tool"]
    var_run_time = cel_DDR_stress_test_array["run_time"]
    var_percent = cel_DDR_stress_test_array["percent"]
    var_log_file = cel_DDR_stress_test_array["log_file"]

    return dLibObj.test_ddr_stress_and_check_status(var_inputArray, var_toolName, var_run_time, var_percent, var_log_file)

def minipack2_test_ddr_stress():
    Log_Debug("Entering procedure minipack2_test_ddr_stress.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = minipack2_cel_DDR_stress_test_array
    var_toolName = minipack2_cel_DDR_stress_test_array["bin_tool"]
    var_run_time = minipack2_cel_DDR_stress_test_array["run_time"]
    var_percent = minipack2_cel_DDR_stress_test_array["percent"]
    var_log_file = minipack2_cel_DDR_stress_test_array["log_file"]

    return dLibObj.test_ddr_stress_and_check_status(var_inputArray, var_toolName, var_run_time, var_percent, var_log_file)

def test_pcie_stress():
    Log_Debug("Entering procedure test_pcie_stress.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_pcie_stress_test_array["bin_tool"]
    var_run_time = cel_pcie_stress_test_array["run_time"]
    var_log_message = cel_pcie_stress_test_array["log_message"]

    return dLibObj.test_pcie_stress_and_check_status(var_toolName, var_run_time, var_log_message)


def check_sys_log():
    Log_Debug("Entering procedure check_sys_log.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_sys_log_check_array["bin_tool"]
    var_log_path = cel_sys_log_check_array["log_path"]
    var_option = "-c -l"

    return dLibObj.verify_sys_log(var_toolName, var_option, var_log_path)


def verify_usb_device_scan_help_dict_option_h():
    Log_Debug("Entering procedure verify_usb_device_scan_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    #var_inputArray = cel_usb_device_scan_help_array
    var_toolName = cel_usb_device_scan_help_array["bin_tool"]
    var_option = "-h"
    var_pattern = cel_usb_device_scan_help_pattern
    var_keywords_pattern = ''
    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pattern, var_keywords_pattern)

def verify_usb_device_scan_help_dict_option_help():
    Log_Debug("Entering procedure verify_usb_device_scan_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    #var_inputArray = cel_usb_device_scan_help_array
    var_toolName = cel_usb_device_scan_help_array["bin_tool"]
    var_option = "--help"
    #var_pattern = cel_usb_device_scan_help_pattern
    var_keywords_pattern = cel_usb_device_scan_help_pattern
    var_pass_pattern = ''
    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def verify_usb_device_scan_help_dict_option_a():
    Log_Debug("Entering procedure verify_usb_device_scan_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    #var_inputArray = cel_usb_device_scan_help_array
    var_toolName = cel_usb_device_scan_help_array["bin_tool"]
    var_option = "-a"
    var_pattern = cel_usb_device_scan_help_a
    var_keywords_pattern = test_pass_pattern_device_scan
    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pattern, var_keywords_pattern)

def verify_usb_device_scan_help_dict_option_all():
    Log_Debug("Entering procedure verify_usb_device_scan_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    #var_inputArray = cel_usb_device_scan_help_array
    var_toolName = cel_usb_device_scan_help_array["bin_tool"]
    var_option = "-all"
    var_pattern = cel_usb_device_scan_help_a
    var_keywords_pattern = test_pass_pattern
    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pattern, var_keywords_pattern)

def verify_usb_device_scan_help_dict_option_l():
    Log_Debug("Entering procedure verify_usb_device_scan_help_dict_option_l.\n")
    dLibObj = getDiagLibObj()

    #var_inputArray = cel_usb_device_scan_help_array
    var_toolName = cel_usb_device_scan_help_array["bin_tool"]
    var_option = "-l"
    var_pattern = cel_usb_device_scan_help_l
    var_keywords_pattern = ''
    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pattern, var_keywords_pattern)

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


def get_the_MAC_and_compare_with_command():
    Log_Debug("Entering procedure get_the_MAC_of_Ethernet_port_with_command.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mac_help_array["bin_tool"]
    var_option = "--all"
    var_pass_pattern = cel_mac_test_pattern

    return dLibObj.get_and_compare_mac_addrs(var_toolName, var_option, var_pass_pattern)


@logThis
def verify_diag_system_log_help_dict_option_h():
    dLibObj = getDiagLibObj()

    var_toolName = './cel_syslog'
    var_option = ' -h'
    var_pattern = ''
    var_path = '/usr/local/cls_diag/utility/stress/syslog'

    return dLibObj.verify_option_diag_system_log_tool_simple_dict(var_toolName, var_option, var_pattern, var_path)

@logThis
def run_system_load_stress(param):
    dLibObj = getDiagLibObj()

    var_toolName = './DDR_test.sh 14400 50 '
    var_option = '../log/CPU_DDR.log & 2>&1'
    var_pattern = ''
    var_path = '/usr/local/cls_diag/utility/stress'
    param = param

    return dLibObj.verify_run_system_load_stress_test(var_toolName, var_option, var_pattern, var_path, param)

@logThis
def clean_system_logs(param):
    dLibObj = getDiagLibObj()

    var_toolName = './cel_syslog'
    var_option = ' -l log/PCIE_sys_after -k -c'
    var_pattern = ''
    var_path = '/usr/local/cls_diag/utility/stress/syslog'
    param = param

    return dLibObj.verify_clean_log_for_system_test(var_toolName, var_option, var_pattern, var_path, param)

def verify_diag_system_log_dict_option_l():
    Log_Debug("Entering procedure verify_diag_system_log_dict_option_l.\n")
    dLibObj = getDiagLibObj()

    var_toolName = sys_log_help_array["bin_tool"]
    var_option = "-l"
    var_Filename = "sys.log"

    return dLibObj.verify_diag_system_log_simple_dict(var_toolName, var_option, var_Filename)


def verify_diag_system_log_dict_option_c():
    Log_Debug("Entering procedure verify_diag_system_log_dict_option_l.\n")
    dLibObj = getDiagLibObj()

    var_toolName = sys_log_help_array["bin_tool"]
    var_option = "-l sys.log -k -c"

    return dLibObj.verify_option_diag_system_log_simple_dict(var_toolName, var_option)


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

def verify_cpu_help_dict_option_a(param=''):
    Log_Debug("Entering procedure verify_cpu_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './' + cel_cpu_help_array["bin_tool"]
    var_option = "-a"
    if param == 'True':
        var_keywords = cpu_test_keyword_true
    elif param == 'False':
        var_keywords = cpu_test_keyword_false
    var_pattern = ''
    var_path= DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict_fpga(var_toolName, var_option, var_keywords, var_pattern, var_path)

def verify_cpu_help_dict_option_all(param=''):
    Log_Debug("Entering procedure verify_cpu_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './' + cel_cpu_help_array["bin_tool"]
    var_option = "--all"
    if param == 'True':
        var_keywords = cpu_test_keyword_true
    elif param == 'False':
        var_keywords = cpu_test_keyword_false
    var_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict_fpga(var_toolName, var_option, var_keywords, var_pattern, var_path)

def verify_lscpu_info(param=''):
    Log_Debug("Entering procedure verify_lscpu_info.\n")
    dLibObj = getDiagLibObj()

    var_cmd = "lscpu"
    var_param = param

    return dLibObj.verify_cpu_cmd_info(var_cmd, var_param)


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
    var_keywords = mem_a_keyword
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
    var_keywords = mem_a_keyword
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
    var_pattern= mem_check_pattern
    cmd = "./{} {} 2>&1".format(var_toolName, var_option)

    return dLibObj.execute_check_dict(cmd, mode=centos_mode, patterns_dict=var_pattern, path=DIAG_TOOL_PATH, line_mode=False, remark=cmd)

def verify_mem_help_dict_option_test_a():
    Log_Debug("Entering procedure verify_mem_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mem_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = mem_a_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_parse_output_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)

def verify_mem_help_dict_option_test_all():
    Log_Debug("Entering procedure verify_mem_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mem_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = mem_a_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_parse_output_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)

def handle_DOM_CPLD_scratch(fpga_cmd_name, patterns_name):
    Log_Debug("Entering procedure handle_DOM_CPLD_scratch.\n")
    dLibObj = getDiagLibObj()

    var_pattern= globals()[patterns_name]
    cmd = globals()[fpga_cmd_name]

    return dLibObj.execute_check_cmd(cmd, mode=centos_mode, patterns=var_pattern, path=FPGA_TOOL_PATH, line_mode=True, remark=cmd)


def verify_mem_help_dict_option_check():
    Log_Debug("Entering procedure verify_mem_help_dict_option_check.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mem_help_array["bin_tool"]
    var_option = "--check"
    var_pattern= mem_check_pattern
    cmd = "./{} {} 2>&1".format(var_toolName, var_option)

    return dLibObj.execute_check_dict(cmd, mode=centos_mode, patterns_dict=var_pattern, path=DIAG_TOOL_PATH, line_mode=False, remark=cmd)


def verify_meminfo_dmidecode():
    Log_Debug("Entering procedure verify_meminfo_dmidecode.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.check_meminfo_dmidecode()

def verify_dmidecode_t_bios():
    Log_Debug("Entering procedure verify_dmidecode_t_bios.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'dmidecode -t bios'
    var_option = ' '
    var_keywords_pattern = ''
    var_pass_pattern = dmidecode_t_bios
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_usb_help_dict_option_h():
    Log_Debug("Entering procedure verify_usb_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_usb_help_array
    var_toolName = cel_usb_help_array["bin_tool"]
    var_option = "-h"
    var_path=DIAG_TOOL_PATH_BKP

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option, var_path)


def verify_usb_help_dict_option_help():
    Log_Debug("Entering procedure verify_usb_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_usb_help_array
    var_toolName = cel_usb_help_array["bin_tool"]
    var_option = "--help"
    var_path=DIAG_TOOL_PATH_BKP

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option, var_path)


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
    var_path=DIAG_TOOL_PATH_BKP

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
    var_path=DIAG_TOOL_PATH_BKP

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_usb_help_dict_option_i():
    Log_Debug("Entering procedure verify_usb_help_dict_option_i.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = [ "{}.*?{}".format(key, value) for key, value in usb_info_array.items() ]
    var_toolName = cel_usb_help_array["bin_tool"]
    var_option = "-i"
    cmd = "./{} {}".format(var_toolName, var_option)
    remark = cmd

    return dLibObj.execute_check_cmd(cmd, mode=centos_mode, patterns=var_inputArray, path=DIAG_TOOL_PATH_BKP, remark=remark)


def verify_usb_help_dict_option_info():
    Log_Debug("Entering procedure verify_usb_help_dict_option_info.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = [ "{}.*?{}".format(key, value) for key, value in usb_info_array.items() ]
    var_toolName = cel_usb_help_array["bin_tool"]
    var_option = "--info"
    cmd = "./{} {}".format(var_toolName, var_option)
    remark = cmd

    return dLibObj.execute_check_cmd(cmd, mode=centos_mode, patterns=var_inputArray, path=DIAG_TOOL_PATH_BKP, remark=remark)


def verify_usb_smart_a():
    Log_Debug("Entering procedure verify_usb_smart_a.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = [ "{}.*?{}".format(key, value) for key, value in usb_info_array.items() ]
    var_toolName = usb_smarttool
    var_option = " -a /dev/sda1"
    cmd = "{} {}".format(var_toolName, var_option)
    remark = cmd

    return dLibObj.execute_check_cmd(cmd, mode=centos_mode, patterns=var_inputArray, path=DIAG_TOOL_PATH_BKP, remark=remark)


def verify_usb_smart_l():
    Log_Debug("Entering procedure verify_usb_smart_l.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.check_usb_smart_l()


def verify_file_is_removed():
    Log_Debug("Entering procedure verify_file_is_removed.\n")
    dLibObj = getDiagLibObj()

    cmd = "mount /dev/sda1 /mnt && cd /mnt && find . -maxdepth 1 -type f -mmin -10 |wc -l; umount /mnt"
    var_inputArray = ["[^ ]?0[ $]?"]
    remark = "verify_file_is_removed"

    return dLibObj.execute_check_cmd(cmd, mode=centos_mode, patterns=var_inputArray, path=DIAG_TOOL_PATH, remark=remark)


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

    var_toolName = cel_tpm_help_array["bin_tool"]
    var_option = "-l"
    var_pass_pattern = cel_tpm_test_l_pattern

    return dLibObj.verify_tpm_tool_simple_dict(var_toolName, var_option, var_pass_pattern)


def verify_tpm_help_dict_option_list():
    Log_Debug("Entering procedure verify_tpm_help_dict_option_list.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_tpm_help_array["bin_tool"]
    var_option = "-l"
    var_pass_pattern = cel_tpm_test_l_pattern

    return dLibObj.verify_tpm_tool_simple_dict(var_toolName, var_option, var_pass_pattern)


def execute_bmc_raw_get_command():
    Log_Debug("Entering procedure execute_bmc_raw_get_command.\n")
    dLibObj = getDiagLibObj()

    var_toolName = ipmi_toolName
    var_netfn = CMD_APP_NETFN
    var_cmd_str = "0x1"
    var_expected_result = bmc_res_ver_28
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


def verify_nvme_smart_tool_and_log():
    Log_Debug("Entering procedure verify_nvme_smart_tool_and_log.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.check_nvme_smart_tool_and_log()



def verify_nvme_test_file_is_removed():
    Log_Debug("Entering procedure verify_nvme_test_file_is_removed.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.check_nvme_test_file_is_removed()


def verify_nvme_help_dict_option_a():
    Log_Debug("Entering procedure verify_nvme_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_nvme_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = nvme_test_a
    cmd = "./{} {} 2>/dev/null".format(var_toolName, var_option)
    remark = cmd

    return dLibObj.execute_check_cmd(cmd, mode=centos_mode, patterns=var_keywords, path=DIAG_TOOL_PATH, remark=remark, timeout=80)


def verify_nvme_help_dict_option_all():
    Log_Debug("Entering procedure verify_nvme_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_nvme_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = nvme_test_a
    cmd = "./{} {} 2>/dev/null".format(var_toolName, var_option)
    remark = cmd

    return dLibObj.execute_check_cmd(cmd, mode=centos_mode, patterns=var_keywords, path=DIAG_TOOL_PATH, remark=remark, timeout=80)

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

    var_ip = ping_ip
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
    dLibObj.init_diag_test()
    # var_toolName = diag_initialize_bin
    # var_option = "-a"
    # return dLibObj.EXEC_bmc_diag_tool_command(var_toolName, var_option)


def verify_bmc_tool_option_d():
    Log_Debug("Entering procedure verify_bmc_tool_option_d.\n")
    dLibObj = getDiagLibObj()
    # dLibObj.init_diag_test()
    # var_toolName = diag_initialize_bin
    # var_option = "-a"
    #
    # return dLibObj.EXEC_bmc_diag_tool_command(var_toolName, var_option)


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
    var_img_path = bmc_img_path
    var_bmc_image = bmc_upgrade_file
    var_flash_device = flash_device_path

    return dLibObj.flash_bmc_image(var_toolName, var_img_path, var_bmc_image, var_flash_device)


def flash_downgrade_bmc():
    Log_Debug("Entering procedure flash_downgrade_bmc.\n")
    dLibObj = getDiagLibObj()

    var_toolName = flashtool
    var_img_path = bmc_img_path
    var_bmc_image = bmc_downgrade_file
    var_flash_device = flash_device_path

    return dLibObj.flash_bmc_image(var_toolName, var_img_path, var_bmc_image, var_flash_device)


def check_bmc_downgrade_version(bmc_flash=''):
    Log_Debug("Entering procedure check_bmc_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_bmc_version = bmc_downgrade_ver

    return dLibObj.check_bmc_version(var_bmc_version, bmc_flash)


def check_bmc_upgrade_version(bmc_flash=''):
    Log_Debug("Entering procedure check_bmc_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_bmc_version = bmc_upgrade_ver

    return dLibObj.check_bmc_version(var_bmc_version, bmc_flash)


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
    var_imageFile = bios_downgrade_file
    var_readFile = 'none'
    var_img_path = bios_img_path
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
    var_imageFile = bios_upgrade_file
    var_readFile = 'none'
    var_img_path = bios_img_path
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
    var_img_path = bios_img_path
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def verify_bios_downgrade_file():
    Log_Debug("Entering procedure verify_bios_downgrade_file.\n")
    dLibObj = getDiagLibObj()

    var_bios_image = bios_downgrade_file
    var_readFile = "bios"
    var_img_path = bios_img_path

    return dLibObj.verify_bios(var_bios_image, var_readFile, var_img_path)


def verify_bios_upgrade_file():
    Log_Debug("Entering procedure verify_bios_upgrade_file.\n")
    dLibObj = getDiagLibObj()

    var_bios_image = bios_upgrade_file
    var_readFile = "bios"
    var_img_path = bios_img_path

    return dLibObj.verify_bios(var_bios_image, var_readFile, var_img_path)


def verify_bios_downgrade_version():
    Log_Debug("Entering procedure verify_bios_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_cpu_bios_ver_bin
    var_opt = "--show"
    var_pattern = bios_ver_pattern
    var_dev_version = bios_downgrade_ver
    var_dev = "BIOS"

    return dLibObj.verify_cpu_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)

def verify_software_help_option_v():
    Log_Debug("Entering procedure verify_software_help_dict_option_v.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_software_test['bin_tool']
    var_option = ' -v'
    var_keywords_pattern = cel_software_test_v_pattern
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_bios_upgrade_version():
    Log_Debug("Entering procedure verify_bios_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = diag_cpu_bios_ver_bin
    var_opt = "--show"
    var_pattern = bios_ver_pattern
    var_dev_version = bios_upgrade_ver
    var_dev = "BIOS"

    return dLibObj.verify_cpu_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def fw_util_exec_bios_downgrade():
    Log_Debug("Entering procedure fw_util_exec_bios_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "update"
    var_dev = "bios"
    var_image = bios_downgrade_file
    var_pattern = fwUtil_update_pattern
    var_img_path = bios_img_path
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
    var_image = bios_upgrade_file
    var_pattern = fwUtil_update_pattern
    var_img_path = bios_img_path
    var_tool_path = FW_UTIL_PATH
    var_mode = "openbmc"

    return dLibObj.fw_util_exec(var_toolName, var_fru, var_opt, var_dev, var_image, var_pattern, var_img_path, var_tool_path, var_mode)


def check_boot_info(option="bios", regex="master"):
    Log_Debug("Entering procedure check_boot_info.\n")
    dLibObj = getDiagLibObj()

    var_region = regex
    var_checktool = boot_info_util
    var_toolOption = option

    return dLibObj.check_bios_region(var_region, var_checktool, var_toolOption)


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
    str_1 = rtc_test_keyword_1
    p = rtc_test_p1
    cmd = rtc_test_cmd
    print(str_1)
    dLibObj.check_cmd_output(cmd, p, str_1)

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_RTC_help_dict_option_help():
    Log_Debug("Entering procedure verify_RTC_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_RTC_help_array
    var_toolName = cel_RTC_help_array["bin_tool"]
    var_option = "--help"
    str_1 = rtc_test_keyword_1
    p = rtc_test_p1
    cmd1 = rtc_test_cmd1
    print(str_1)
    dLibObj.check_cmd_output(cmd1, p, str_1)

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
    cmd1 = rtc_test_cmd2
    cmd2 = rtc_test_cmd3
    p1 = rtc_test_p3
    p2 = rtc_test_p2
    dLibObj.check_rtc_time(cmd1, cmd2, p1, p2)

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
    cmd1 = rtc_test_cmd4
    cmd2 = rtc_test_cmd3
    p1 = rtc_test_p3
    p2 = rtc_test_p2
    dLibObj.check_rtc_time(cmd1, cmd2, p1, p2)

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

def make_power(param = ''):
    Log_Debug("Entering procedure make power off.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'wedge_power.sh ' + param
    var_option = ' '
    var_keywords_pattern = ''
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def check_power_status(param=''):
    Log_Debug("Entering procedure check power status is off.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'wedge_power.sh status ' + param
    var_option = ' '
    var_keywords_pattern = ''
    if param == 'off':
        var_pass_pattern = power_status_off
    else:
        var_pass_pattern = power_status_on

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def verify_ipmitool_mc_info():
    Log_Debug("Entering procedure verify_ipmitool_mc_info.\n")
    dLibObj = getDiagLibObj()
    var_toolName = ipmitool_test["bin_tool"]
    var_option = "mc info; " + "echo retcode=$?"
    var_keywords = 'none'
    var_pattern = ipmitool_mc_info_pattern
    var_data='none'
    var_port='none'
    var_color='none'
    var_path=FW_UTIL_PATH
    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color,var_path)

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
    var_imageFile = fpga_upgrade_file
    var_readFile = 'none'
    var_img_path = fpga_img_path
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
    var_imageFile = fpga_upgrade_file
    var_readFile = 'none'
    var_img_path = fpga_img_path
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def verify_fpga1_upgrade_version():
    Log_Debug("Entering procedure verify_fpga1_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fpga_software_test
    var_opt = "-v"
    var_pattern = fpga1_ver_pattern
    var_dev_version = fpga_upgrade_ver
    var_dev = "fpga1"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def verify_fpga2_upgrade_version():
    Log_Debug("Entering procedure verify_fpga2_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fpga_software_test
    var_opt = "-v"
    var_pattern = fpga2_ver_pattern
    var_dev_version = fpga_upgrade_ver
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
    var_imageFile = fpga_downgrade_file
    var_readFile = 'none'
    var_img_path = fpga_img_path
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
    var_imageFile = fpga_downgrade_file
    var_readFile = 'none'
    var_img_path = fpga_img_path
    var_tool_path = SPI_UTIL_PATH

    return dLibObj.spi_util_exec(var_toolName, var_opt, var_spiNum, var_dev, var_check_pattern, var_imageFile, var_readFile, var_img_path, var_tool_path)


def verify_fpga1_downgrade_version():
    Log_Debug("Entering procedure verify_fpga1_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fpga_software_test
    var_opt = "-v"
    var_pattern = fpga1_ver_pattern
    var_dev_version = fpga_downgrade_ver
    var_dev = "fpga1"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def verify_fpga2_downgrade_version():
    Log_Debug("Entering procedure verify_fpga2_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fpga_software_test
    var_opt = "-v"
    var_pattern = fpga2_ver_pattern
    var_dev_version = fpga_downgrade_ver
    var_dev = "fpga2"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)

def verify_pci_option_a():
    Log_Debug("Entering procedure verify_pcie_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './cel-pci-test'
    var_option = '-a'
    var_pattern = pci_option_a_pattern

    return dLibObj.verify_each_pcie_a(var_toolName, var_option, var_pattern)

def verify_pci_option_all():
    Log_Debug("Entering procedure verify_pcie_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './cel-pci-test'
    var_option = '--all'
    var_pattern = pci_option_a_pattern

    return dLibObj.verify_each_pcie_a(var_toolName, var_option, var_pattern)

def run_command_lspci_on_centos():
    Log_Debug("Entering procedure run command lspci.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'lspci'
    var_option = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.EXEC_centos_diag_tool_command(var_toolName, var_option, var_path)

def check_each_pice_lspci(parm = ''):
    Log_Debug("Entering procedure check_each_pice_lspci.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "lspci -s"
    var_option = parm + ' ' + '-xxxvvv'
    var_keywords = each_pice_lspci

    return dLibObj.verify_each_pcie_lspci(var_toolName, var_option, var_keywords)

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
    var_image = bic_downgrade_file
    var_pattern = bic_update_pattern
    var_img_path = bic_img_path
    var_tool_path = FW_UTIL_PATH
    var_mode = "openbmc"

    return dLibObj.fw_util_exec(var_toolName, var_fru, var_opt, var_dev, var_image, var_pattern, var_img_path, var_tool_path, var_mode)


def verify_bic_downgrade_version():
    Log_Debug("Entering procedure verify_bic_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = bic_software_test
    var_opt = "-v"
    var_pattern = bic_ver_pattern
    var_dev_version = bic_downgrade_ver
    var_dev = "bic"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def fw_util_exec_bic_upgrade():
    Log_Debug("Entering procedure fw_util_exec_bic_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "update"
    var_dev = "bic"
    var_image = bic_upgrade_file
    var_pattern = bic_update_pattern
    var_img_path = bic_img_path
    var_tool_path = FW_UTIL_PATH
    var_mode = "openbmc"

    return dLibObj.fw_util_exec(var_toolName, var_fru, var_opt, var_dev, var_image, var_pattern, var_img_path, var_tool_path, var_mode)


def verify_bic_upgrade_version():
    Log_Debug("Entering procedure verify_bic_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = bic_software_test
    var_opt = "-v"
    var_pattern = bic_ver_pattern
    var_dev_version = bic_upgrade_ver
    var_dev = "bic"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_fcm_downgrade():
    Log_Debug("Entering procedure updateTool_exec_fcm_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fcm_cpld_tool
    var_image = fcm_downgrade_file
    var_opt = "hw"
    var_dev = "FCM-CPLD"
    var_pattern = fcm_update_pattern
    var_img_path = fcm_img_path

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path)


def verify_fcm_downgrade_version():
    Log_Debug("Entering procedure verify_fcm_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fcm_software_test
    var_opt = "-v"
    var_pattern = fcm_ver_pattern
    var_dev_version = fcm_downgrade_ver
    var_dev = "FCM-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_fcm_upgrade():
    Log_Debug("Entering procedure updateTool_exec_fcm_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fcm_cpld_tool
    var_image = fcm_upgrade_file
    var_opt = "hw"
    var_dev = "FCM-CPLD"
    var_pattern = fcm_update_pattern
    var_img_path = fcm_img_path

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path)


def verify_fcm_upgrade_version():
    Log_Debug("Entering procedure verify_fcm_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fcm_software_test
    var_opt = "-v"
    var_pattern = fcm_ver_pattern
    var_dev_version = fcm_upgrade_ver
    var_dev = "FCM-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_scm_downgrade():
    Log_Debug("Entering procedure updateTool_exec_scm_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = scm_cpld_tool
    var_image = scm_downgrade_file
    var_opt = "hw"
    var_dev = "SCM-CPLD"
    var_pattern = scm_update_pattern
    var_img_path = scm_img_path

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path)


def verify_scm_downgrade_version():
    Log_Debug("Entering procedure verify_scm_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = scm_software_test
    var_opt = "-v"
    var_pattern = scm_ver_pattern
    var_dev_version = scm_downgrade_ver
    var_dev = "SCM-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_scm_upgrade():
    Log_Debug("Entering procedure updateTool_exec_scm_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = scm_cpld_tool
    var_image = scm_upgrade_file
    var_opt = "hw"
    var_dev = "SCM-CPLD"
    var_pattern = scm_update_pattern
    var_img_path = scm_img_path

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path)


def verify_scm_upgrade_version():
    Log_Debug("Entering procedure verify_scm_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = scm_software_test
    var_opt = "-v"
    var_pattern = scm_ver_pattern
    var_dev_version = scm_upgrade_ver
    var_dev = "SCM-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_smb_downgrade():
    Log_Debug("Entering procedure updateTool_exec_smb_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = smb_cpld_tool
    var_image = smb_downgrade_file
    var_opt = "hw"
    var_dev = "SMB-CPLD"
    var_pattern = smb_update_pattern
    var_img_path = smb_img_path

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path)


def verify_smb_downgrade_version():
    Log_Debug("Entering procedure verify_smb_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = smb_software_test
    var_opt = "-v"
    var_pattern = smb_ver_pattern
    var_dev_version = smb_downgrade_ver
    var_dev = "SMB-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_smb_upgrade():
    Log_Debug("Entering procedure updateTool_exec_smb_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = smb_cpld_tool
    var_image = smb_upgrade_file
    var_opt = "hw"
    var_dev = "SMB-CPLD"
    var_pattern = smb_update_pattern
    var_img_path = smb_img_path

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path)


def verify_smb_upgrade_version():
    Log_Debug("Entering procedure verify_smb_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = smb_software_test
    var_opt = "-v"
    var_pattern = smb_ver_pattern
    var_dev_version = smb_upgrade_ver
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


def verify_fpga_help_dict_option_i():
    Log_Debug("Entering procedure verify_fpga_help_dict_option_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fpga_help_array["bin_tool"]
    var_option = "-i"

    return dLibObj.verify_fpga_tool_simple_dict(var_toolName, var_option)


def verify_fpga_help_dict_option_info():
    Log_Debug("Entering procedure verify_fpga_help_dict_option_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fpga_help_array["bin_tool"]
    var_option = "--info"

    return dLibObj.verify_fpga_tool_simple_dict(var_toolName, var_option)


def verify_fpga_help_dict_option_a():
    Log_Debug("Entering procedure verify_fpga_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fpga_help_array["bin_tool"]
    var_option = "-a"
    var_option += option_str
    var_keywords = fpga_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)


def verify_fpga_help_dict_option_all_with_config():
    Log_Debug("Entering procedure verify_fpga_help_dict_option_all_with_config.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fpga_help_array["bin_tool"]
    var_option = "--all --config=../configs/fpgas.yaml"
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


def check_fpga_driver_version():
    Log_Debug("Entering procedure check_fpga_driver_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'fpga'
    var_option = 'ver'
    var_path = FPGA_TOOL_PATH
    var_pattern = fpga_version

    return dLibObj.verify_diag_tool_simple_dict(toolName=var_toolName, option=var_option, pattern=var_pattern, fpath=var_path)


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


def verify_sw_version_help_dict_option_S():
    Log_Debug("Entering procedure verify_sw_version_help_dict_option_S.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = show_version_array
    var_toolName = cel_version_help_array["bin_tool"]
    var_option = "-S"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_sw_version_help_dict_option_show():
    Log_Debug("Entering procedure verify_sw_version_help_dict_option_show.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = show_version_array
    var_toolName = cel_version_help_array["bin_tool"]
    var_option = "--show"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)

def Minipack2_verify_sw_version_help_dict_option_S():
    Log_Debug("Entering procedure Minipack2_verify_sw_version_help_dict_option_S.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = Minipack2_show_version_array
    var_toolName = cel_version_help_array["bin_tool"]
    var_option = "-S"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)

def Minipack2_verify_sw_version_help_dict_option_show():
    Log_Debug("Entering procedure Minipack2_verify_sw_version_help_dict_option_show.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = Minipack2_show_version_array
    var_toolName = cel_version_help_array["bin_tool"]
    var_option = "--show"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)

def cat_proc_version():
    Log_Debug("Entering procedure cat_proc_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cat'
    var_option = "/proc/version"
    var_keywords_pattern = cat_proc_version_pattern
    var_pass_pattern = ''
    var_path = ''

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern,
                                                        pass_pattern=var_pass_pattern, path=var_path)


def updateTool_exec_pwr_cpld_downgrade():
    Log_Debug("Entering procedure updateTool_exec_pwr_cpld_downgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = pwr_cpld_tool
    var_image = pwr_downgrade_file
    var_opt = "hw"
    var_dev = "PWR-CPLD"
    var_pattern = pwr_update_pattern
    var_img_path = pwr_img_path

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path)


def verify_pwr_cpld_downgrade_version():
    Log_Debug("Entering procedure verify_pwr_cpld_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = pwr_software_test
    var_opt = "-v"
    var_pattern = pwr_ver_pattern
    var_dev_version = pwr_downgrade_ver
    var_dev = "PWR-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def updateTool_exec_pwr_cpld_upgrade():
    Log_Debug("Entering procedure updateTool_exec_pwr_cpld_upgrade.\n")
    dLibObj = getDiagLibObj()

    var_toolName = pwr_cpld_tool
    var_image = pwr_upgrade_file
    var_opt = "hw"
    var_dev = "PWR-CPLD"
    var_pattern = pwr_update_pattern
    var_img_path = pwr_img_path

    return dLibObj.update_tool_exec(var_toolName, var_image, var_opt, var_dev, var_pattern, var_img_path)


def verify_pwr_cpld_upgrade_version():
    Log_Debug("Entering procedure verify_pwr_cpld_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = pwr_software_test
    var_opt = "-v"
    var_pattern = pwr_ver_pattern
    var_dev_version = pwr_upgrade_ver
    var_dev = "PWR-CPLD"

    return dLibObj.verify_bmc_software_version(var_toolName, var_opt, var_pattern, var_dev_version, var_dev)


def verify_bmc_cpu_help_dict_option_h():
    Log_Debug("Entering procedure verify_bmc_cpu_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpu_help_array["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = bmc_cpu_help_pattern
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_bmc_cpu_help_dict_option_a():
    Log_Debug("Entering procedure verify_bmc_cpu_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpu_help_array["bin_tool"]
    var_option = "-a"
    cmd = "./{} {} 2>&1".format(var_toolName, var_option)
    var_keywords_pattern = bmc_cpu_keyword_pattern
    remark = "{}".format(cmd)

    return dLibObj.execute_check_cmd(cmd, mode=openbmc_mode, path=BMC_DIAG_TOOL_PATH, remark=remark)


def verify_bmc_cpu_help_dict_option_i():
    Log_Debug("Entering procedure verify_bmc_cpu_help_dict_option_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpu_help_array["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = bmc_cpu_info_pattern
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def compare_bmc_cpu_info_and_option_i():
    Log_Debug("Entering procedure compare_bmc_cpu_info_and_option_i.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.compare_bmc_cpu_info()


def verify_bmc_top():
    Log_Debug("Entering procedure verify_bmc_top.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.check_bmc_top()

def verify_bmc_fpga_help_dict_option_h():
    Log_Debug("Entering procedure verify_bmc_fpga_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_help_array["bin_tool"]
    var_option = "-h"
    var_pattern = bmc_fpga_help_pattern
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pattern, var_pass_pattern, var_path)

def verify_bmc_fpga_1_device_write_read():
    Log_Debug("Entering procedure verify_bmc_fpga_1_device_write_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_help_array["bin_tool"]
    var_dev = "SMB_DOM_FPGA_1"
    var_address = "4"
    var_data = "0xaa"

    return dLibObj.verify_device_write_read(var_toolName, var_dev, var_address, var_data)


def verify_bmc_fpga_2_device_write_read():
    Log_Debug("Entering procedure verify_bmc_fpga_2_device_write_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_help_array["bin_tool"]
    var_dev = "SMB_DOM_FPGA_2"
    var_address = "4"
    var_data = "0xaa"

    return dLibObj.verify_device_write_read(var_toolName, var_dev, var_address, var_data)


def verify_bmc_fpga_help_dict_option_a():
    Log_Debug("Entering procedure verify_bmc_fpga_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_help_array["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = fpga_test_a_pattern[1:]
    var_pass_pattern = ""
    cmd = "./{} {} 2>&1".format(var_toolName, var_option)

    return dLibObj.check_patterns_list_pass(cmd, var_keywords_pattern, BMC_DIAG_TOOL_PATH)


def verify_bmc_fpga_help_dict_option_v():
    Log_Debug("Entering procedure verify_bmc_fpga_help_dict_option_v.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_help_array["bin_tool"]
    var_option = "-v"
    var_keywords_pattern = fpga_test_v_pattern
    var_pass_pattern = ""

    return dLibObj.verify_bmc_diag_tool_simple_dict_fpga(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

@logThis
def verify_bmc_fpga_help_dict_option_k():
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_help_array["bin_tool"]
    var_option = "-k"
    var_keywords_pattern = fpga_test_k_pattern
    var_pass_pattern = ""

    return dLibObj.verify_bmc_diag_tool_simple_dict_fpga(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)


def verify_cel_version_test_S_verify_fpga():
    Log_Debug("Entering procedure verify_cel_version_test_S_verify_fpga.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_version_test["bin_tool"]
    var_option = "-S"
    var_keywords_pattern = version_test_S_or_show_pattern
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict_fpga(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def verify_cel_version_test_option_show_verify_fpga():
    Log_Debug("Entering procedure verify_cel_version_test_S_verify_fpga.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_version_test["bin_tool"]
    var_option = "--show"
    var_keywords_pattern = version_test_S_or_show_pattern
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict_fpga(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)


def verify_bmc_cpld_help_dict_option_h():
    Log_Debug("Entering procedure verify_bmc_cpld_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = bmc_cpld_help_pattern
    var_pass_pattern = ""

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)


def verify_bmc_fcm_cpld_device_write_read():
    Log_Debug("Entering procedure verify_bmc_fcm_cpld_device_write_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_dev = "FCM_CPLD"
    var_address = "0x70"
    var_data = "0xaa"

    return dLibObj.verify_device_write_read(var_toolName, var_dev, var_address, var_data)


def verify_bmc_scm_cpld_device_write_read():
    Log_Debug("Entering procedure verify_bmc_scm_cpld_device_write_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_dev = "SCM_CPLD"
    var_address = "0x70"
    var_data = "0xaa"

    return dLibObj.verify_device_write_read(var_toolName, var_dev, var_address, var_data)


def verify_bmc_smb_cpld_device_write_read():
    Log_Debug("Entering procedure verify_bmc_smb_cpld_device_write_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_dev = "SMB_CPLD"
    var_address = "0x70"
    var_data = "0xaa"

    return dLibObj.verify_device_write_read(var_toolName, var_dev, var_address, var_data)


def verify_bmc_smb_pwr_cpld_device_write_read():
    Log_Debug("Entering procedure verify_bmc_smb_pwr_cpld_device_write_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_dev = "SMB_PWR_CPLD"
    var_address = "0x70"
    var_data = "0xaa"

    return dLibObj.verify_device_write_read(var_toolName, var_dev, var_address, var_data)


def verify_bmc_cpld_help_dict_option_a():
    Log_Debug("Entering procedure verify_bmc_cpld_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = bmc_cpld_keyword_pattern
    var_pass_pattern = test_pass_pattern

    return dLibObj.verify_bmc_swtest_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)


def verify_bmc_cpld_help_dict_option_v():
    Log_Debug("Entering procedure verify_bmc_cpld_help_dict_option_v.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_bmc_cpld_version_array
    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_option = "-v"
    var_pattern = bmc_cpld_version_pattern

    return dLibObj.verify_option_bmc_diag_tool_simple_dict(var_inputArray, var_toolName, var_option, var_pattern)

def verify_ucd_security_help_dict_option_h():
    Log_Debug("Entering procedure verify_ucd_security_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_ucd_security_help_array["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = ucd_security_help_pattern
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_ucd_security_help_dict_option(param = ''):
    Log_Debug("Entering procedure verify_ucd_security_help_dict_option.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_ucd_security_help_array["bin_tool"]
    var_option = " " + param
    var_keywords_pattern = ucd_security_pattern
    var_pass_pattern = ''

    return dLibObj.verify_bmc_i2c_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def verify_bmc_i2c_other_help_dict_option_h():
    Log_Debug("Entering procedure verify_bmc_i2c_other_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_i2c_other_help_array["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = bmc_i2c_other_help_pattern
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_bmc_i2c_other_help_dict_option(param = ''):
    Log_Debug("Entering procedure verify_bmc_i2c_other_help_dict_option.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_i2c_other_help_array["bin_tool"]
    var_option = " " + param
    var_keywords_pattern = i2c_scan_pattern
    var_pass_pattern = i2c_scan_pass_keyword

    return dLibObj.verify_bmc_i2c_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def verify_bmc_i2c_other_help_dict_option_a():
    Log_Debug("Entering procedure verify_bmc_i2c_other_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_i2c_other_help_array["bin_tool"]
    var_option = " " + "-a"
    var_keywords_pattern = bmc_i2c_other_keyword_pattern
    var_pass_pattern = test_pass_pattern

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def verify_bmc_i2c_help_dict_option_h():
    Log_Debug("Entering procedure verify_bmc_i2c_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_i2c_help_array["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = bmc_i2c_help_pattern
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_bmc_i2c_help_dict_option_a(param = ''):
    Log_Debug("Entering procedure verify_bmc_i2c_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_i2c_help_array["bin_tool"]
    var_option = " " + param + " " + "-a"
    var_keywords_pattern = bmc_i2c_keyword_pattern
    var_pass_pattern = test_pass_pattern

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)


def verify_bmc_i2c_help_dict_option_s(param = ''):
    Log_Debug("Entering procedure verify_bmc_i2c_help_dict_option_s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_i2c_help_array["bin_tool"]
    var_option = " " + param + " " + "-s"
    var_keywords_pattern = i2c_scan_pattern
    var_pass_pattern = i2c_scan_pass_keyword

    return dLibObj.verify_bmc_i2c_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

@logThis
def reboot_to_centos_and_disable_hyper_threading(device='DUT'):
    switch_to_centos()
    bios_menu_lib.enter_bios_setup(device)
    bios_menu_lib.send_key(device, 'KEY_RIGHT', 2)
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    bios_menu_lib.send_key(device, 'KEY_DOWN')
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    bios_menu_lib.send_key(device, 'KEY_DOWN')
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    bios_menu_lib.send_key(device, 'KEY_ESC')
    bios_menu_lib.send_key(device, 'KEY_LEFT', 3)
    bios_menu_lib.send_key(device, 'KEY_DOWN')
    bios_menu_lib.send_key(device, 'KEY_ENTER', 2)
    deviceObj.getPrompt("centos", timeout=600)

@logThis
def power_then_enable_threading(device='DUT'):
    power_the_whole_system()
    switch_to_centos()
    #deviceObj.sendline('sol.sh')

    ##1. Enter BIOS Setup Menu
    bios_menu_lib.enter_bios_setup(device)
    bios_menu_lib.send_key(device, 'KEY_RIGHT', 2)
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    bios_menu_lib.send_key(device, 'KEY_DOWN')
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    bios_menu_lib.send_key(device, 'KEY_DOWN')
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    bios_menu_lib.send_key(device, 'KEY_ESC')
    bios_menu_lib.send_key(device, 'KEY_LEFT', 3)
    bios_menu_lib.send_key(device, 'KEY_DOWN')
    bios_menu_lib.send_key(device, 'KEY_ENTER', 2)
    deviceObj.getPrompt("centos", timeout=600)
    time.sleep(5)

@logThis
def verify_bmc_i2c_help_dict_option_l(param = ''):
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_i2c_help_array["bin_tool"]
    var_option = "-b " + param + " -l"
    var_keywords_pattern = ''
    var_pass_pattern = ""

    return dLibObj.verify_bmc_i2c_tool_option_l_test(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def read_and_backup_eeprom_cfg():
    Log_Debug("Entering procedure read_and_backup_eeprom_cfg.\n")
    dLibObj = getDiagLibObj()

    var_cfg_out = EEPROM_OUT_CFG
    var_cfg_bak = EEPROM_OUT_BAK_CFG
    var_toolName = cel_bmc_eeprom_tool_d["bin_tool"]
    var_paths = [SCM_EEPROM_PATH, FCM_EEPROM_PATH, SMB_EEPROM_PATH]

    return dLibObj.backup_eeprom_cfg(var_cfg_out, var_cfg_bak, var_toolName, var_paths)


def restore_and_clean_eeprom_cfg():
    Log_Debug("Entering procedure restore_and_clean_eeprom_cfg.\n")
    dLibObj = getDiagLibObj()

    var_cfg = EEPROM_CFG
    var_cfg_out = EEPROM_OUT_CFG
    var_cfg_bak = EEPROM_OUT_BAK_CFG
    var_toolName = "./" + cel_bmc_eeprom_tool_d["bin_tool"]
    var_paths = [SCM_EEPROM_PATH, FCM_EEPROM_PATH, SMB_EEPROM_PATH]

    return dLibObj.restore_eeprom_cfg(var_cfg, var_cfg_out, var_cfg_bak, var_toolName, var_paths)



def verify_bmc_scm_auto_eeprom_dict():
    Log_Debug("Entering procedure verify_bmc_scm_auto_eeprom_dict.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_scm_auto_eeprom["bin_tool"]
    var_option = ""
    var_keywords_pattern = bmc_scm_auto_eeprom_pattern
    var_pass_pattern = ""

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, SCM_EEPROM_PATH)


def verify_bmc_fcm_auto_eeprom_dict():
    Log_Debug("Entering procedure verify_bmc_fcm_auto_eeprom_dict.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fcm_auto_eeprom["bin_tool"]
    var_option = ""
    var_keywords_pattern = bmc_fcm_auto_eeprom_pattern
    var_pass_pattern = ""

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, FCM_EEPROM_PATH)


def verify_bmc_smb_auto_eeprom_dict():
    Log_Debug("Entering procedure verify_bmc_smb_auto_eeprom_dict.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_smb_auto_eeprom["bin_tool"]
    var_option = ""
    var_keywords_pattern = bmc_smb_auto_eeprom_pattern
    var_pass_pattern = ""
    var_path = SMB_EEPROM_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def verify_bmc_eeprom_tool_dict_option_d():
    Log_Debug("Entering procedure verify_bmc_eeprom_tool_dict_option_d.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_eeprom_tool_d["bin_tool"]
    var_option = "-d"
    var_keywords_pattern = bmc_eeprom_tool_d_pattern
    var_pass_pattern = ""
    var_path = SMB_EEPROM_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def verify_bmc_cel_boot_test_h():
    Log_Debug("Entering procedure verify_bmc_cel_boot_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = bmc_cel_boot_test_h["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = bmc_boot_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def verify_cel_boot_test_b_bmc_s_master():
    Log_Debug("Entering procedure verify_cel_boot_test_b_bmc_s_master.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test_b_bmc_s["bin_tool"]
    var_option = "-b bmc -s"
    var_keywords_pattern = boot_test_b_bmc_s_master_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def verify_cel_boot_test_b_bmc_s_slave():
    Log_Debug("Entering procedure verify_cel_boot_test_b_bmc_s_slave.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test_b_bmc_s["bin_tool"]
    var_option = "-b bmc -s"
    var_keywords_pattern = boot_test_b_bmc_s_slave_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_pwmon_dict_option_h():
    Log_Debug("Entering procedure verify powmon dict option h")
    dLibObj = getDiagLibObj()

    var_toolName = cel_pwmon_test["bin_tool"]
    var_option = " -h"
    var_keywords_pattern = pwmon_option_h_pattern
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_fpga_option_h():
    Log_Debug("Entering procedure verify fpga option h")
    dLibObj = getDiagLibObj()

    var_toolName = 'fpga'
    var_option = ' -h'
    var_keywords_pattern = check_fpga_h
    var_pass_pattern = ''
    mode = 'centos'
    var_path = FPGA_TOOL_PATH

    return dLibObj.verify_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, mode, var_path)


def test_iob_fpga_access_smb_cpld_0():
    Log_Debug("Entering procedure test_iob_fpga_access_smb_cpld_0")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_tool_test_array['bin_tool']
    var_option_smb = cel_bmc_fpga_tool_test_array['option_smb']
    var_option_r = cel_bmc_fpga_tool_test_array['read_option']
    var_option_0 = cel_bmc_fpga_tool_test_array['option_0']
    var_path = FPGA_TOOL_PATH
    var_pass_pattern = bmc_smb_cpld_0_pass_pattern
    cmd = './' + var_toolName + ' ' + var_option_smb + ' ' + var_option_r + ' ' + var_option_0

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)


def test_iob_fpga_access_smb_cpld_1():
    Log_Debug("Entering procedure test_iob_fpga_access_smb_cpld_1")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_tool_test_array['bin_tool']
    var_option_smb = cel_bmc_fpga_tool_test_array['option_smb']
    var_option_r = cel_bmc_fpga_tool_test_array['read_option']
    var_option_1 = cel_bmc_fpga_tool_test_array['option_1']
    var_path = FPGA_TOOL_PATH
    var_pass_pattern = bmc_smb_cpld_1_pass_pattern
    cmd = './' + var_toolName + ' ' + var_option_smb + ' ' + var_option_r + ' ' + var_option_1

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

def rmmod_uio_pci():
    Log_Debug("Entering procedure rmmod_uio_pci.\n")
    dLibObj = getDiagLibObj()

    toolName = 'rmmod'
    option = ' uio_pci_generic'
    path = FPGA_TOOL_PATH
    
    return dLibObj.EXEC_centos_diag_tool_command(toolName, option, path)

def test_iob_fpga_access_smb_cpld_2():
    Log_Debug("Entering procedure test_iob_fpga_access_smb_cpld_2")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_tool_test_array['bin_tool']
    var_option_smb = cel_bmc_fpga_tool_test_array['option_smb']
    var_option_r = cel_bmc_fpga_tool_test_array['read_option']
    var_option_2 = cel_bmc_fpga_tool_test_array['option_2']
    var_path = FPGA_TOOL_PATH
    var_pass_pattern = bmc_smb_cpld_2_pass_pattern_DVT
    cmd = './' + var_toolName + ' ' + var_option_smb + ' ' + var_option_r + ' ' + var_option_2

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

def check_flashScan_option_h():
    Log_Debug("Entering procedure check_flashScan_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './cel-flashScan-test'
    var_option = '-h'
    var_keywords_pattern = flashScan_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def check_flashScan_option_a():
    Log_Debug("Entering procedure check_flashScan_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './cel-flashScan-test'
    var_option = '-a'
    var_keywords_pattern = flashScan_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def check_avs_option_h():
    Log_Debug("Entering procedure check_avs_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './cel-avs-test'
    var_option = '-h'
    var_keywords_pattern = avs_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def check_bios_boot_info():
    Log_Debug("Entering procedure check_bios_boot_info.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "boot_info.sh"
    var_option = "bmc"
    var_keywords_pattern = check_bios_boot_info_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def check_avs_option_a():
    Log_Debug("Entering procedure check_avs_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './cel-avs-test'
    var_option = '-a'
    var_keywords_pattern = avs_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def test_iob_fpga_access_smb_cpld_3():
    Log_Debug("Entering procedure test_iob_fpga_access_smb_cpld_3")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fpga_tool_test_array['bin_tool']
    var_option_smb = cel_bmc_fpga_tool_test_array['option_smb']
    var_option_r = cel_bmc_fpga_tool_test_array['read_option']
    var_option_3 = cel_bmc_fpga_tool_test_array['option_3']
    var_path = FPGA_TOOL_PATH
    var_pass_pattern = cel_bmc_smb_cpld_3_pass_pattern
    cmd = './' + var_toolName + ' ' + var_option_smb + ' ' + var_option_r + ' ' + var_option_3

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

def set_pim_ucd90160_level(param=''):
    Log_Debug("Entering procedure set_pim_ucd90160_level.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./pim_trim_" + param + ".sh"
    var_option = ' '
    var_keywords_pattern = set_pim_ucd90160_level_pattern
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, Utility_PATH)

def verify_sensor_port1_8_status():
    Log_Debug("Entering procedure verify_sensor_port1_8_status.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'minipack2_dc' in devicename.lower():
        pim_list = ['pim1', 'pim2', 'pim7', 'pim8']
    else:
        pim_list = ['pim1','pim2','pim3','pim4','pim5','pim6','pim7','pim8']
    for pim in range(len(pim_list)):
        Log_Debug("This test will test %s sensor now!" % pim)
        toolName = 'cel-sensor-test'
        option = '-b ' + pim_list[pim] + ' -c'
        keywords_pattern = sensor_port_status_pattern
        pass_pattern = ''
        path = BMC_DIAG_TOOL_PATH

        dLibObj.verify_bmc_diag_tool_simple_dict(toolName, option, keywords_pattern, pass_pattern, path)

def verify_scm_cpld_accessed(param=''):

    Log_Debug("Entering procedure verify_scm_cpld_accessed")
    dLibObj = getDiagLibObj()

    var_toolName = './fpga'
    var_option = 'scm r' + ' ' + param
    var_keywords = scm_cpld_accessed
    var_path = FPGA_TOOL_PATH

    return dLibObj.test_scm_cpld_accessed(var_toolName, var_option, var_keywords,var_path)

@logThis
def mdc_freq_mhz_test_option_w():
    dLibObj = getDiagLibObj()

    for param in range(1, 9):
        var_toolName = './fpga ' + 'pim w'
        var_option = 'pim=' + str(param) + ' 0x200 0x01000005'
        var_path = FPGA_TOOL_PATH

        dLibObj.check_high_power_mode_OBO_status(var_toolName, var_option, var_path)

@logThis
def mdc_freq_mhz_test_option_wA():
    dLibObj = getDiagLibObj()

    for param in range(1, 9):
        var_toolName = './fpga ' + 'pim ' + 'w'
        var_option = 'pim=' + str(param) + ' 0x200 0x0100000A'
        var_path = FPGA_TOOL_PATH

        dLibObj.check_high_power_mode_OBO_status(var_toolName, var_option, var_path)

@logThis
def mdc_freq_mhz_test_option_r():
    dLibObj = getDiagLibObj()

    for param in range(1, 9):
        var_toolName = './fpga ' + 'pim ' + 'r'
        var_option = 'pim=' + str(param) + ' 0x200'
        var_path = FPGA_TOOL_PATH

        dLibObj.check_high_power_mode_OBO_status(var_toolName, var_option, var_path)

def make_sure_bmc_boot_from_master():
    Log_Debug("Entering procedure make_sure_bmc_boot_from_master.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test_b_bmc_s["bin_tool"]
    var_option = "-b bmc -r master && echo 'To make sure bmc is boot from master first' && sysctl -w kernel.printk=3"
    var_keywords_pattern = ""
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                path=var_path, is_negative_test=False)

def verify_cel_boot_test_b_bmc_r_slave():
    Log_Debug("Entering procedure verify_cel_boot_test_b_bmc_r_slave.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test_b_bmc_s["bin_tool"]
    var_option = "-b bmc -r slave"
    var_keywords_pattern = cel_boot_test_b_bmc_r_slave_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                path=var_path, is_negative_test=False)


def verify_cel_boot_test_b_bmc_r_master():
    Log_Debug("Entering procedure verify_cel_boot_test_b_bmc_r_master.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test_b_bmc_s["bin_tool"]
    var_option = "-b bmc -r master"
    var_keywords_pattern = cel_boot_test_b_bmc_r_master_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                path=var_path, is_negative_test=False)


def wait_for_openbmc_prompt_back():
    Log_Debug("Entering procedure wait_for_openbmc_prompt_back.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.wait_for_openbmc_prompt_back()

def wait_for_centos_prompt_back():
    Log_Debug("Entering procedure wait_for_centos_prompt_back.\n")
    dLibObj = getDiagLibObj()

    time.sleep(5)
    #dLibObj.switch_to_centos_and_go_to_diag_tool()

    #return dLibObj.wait_for_centos_prompt_back()
    return dLibObj.wait_enter_centos()

def make_sure_bios_boot_from_master():
    Log_Debug("Entering procedure make_sure_bios_boot_from_master.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test_b_bmc_s["bin_tool"]
    var_option = "-b bios -r master && echo 'To make sure bios is boot from master first'"
    var_keywords_pattern = ""
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                path=var_path, is_negative_test=False)


def verify_boot_info_bios_master():
    Log_Debug("Entering procedure verify_boot_info_bios_master.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "boot_info.sh"
    var_option = "bios"
    var_keywords_pattern = boot_info_sh_bios_master_pattern
    var_pass_pattern = ""
    var_path = "/usr/local/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def verify_boot_info_bios_slave():
    Log_Debug("Entering procedure verify_boot_info_bios_slave.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "boot_info.sh"
    var_option = "bios"
    var_keywords_pattern = boot_info_sh_bios_slave_pattern
    var_pass_pattern = ""
    var_path = "/usr/local/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def verify_cel_boot_test_b_bios_r_slave():
    Log_Debug("Entering procedure verify_cel_boot_test_b_bios_r_slave.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test_b_bmc_s["bin_tool"]
    #var_option = "-b bios -r slave ; sleep 3 ; wedge_power.sh off ; sleep 5 ; wedge_power.sh on"
    var_option = "wedge_power.sh off ; sleep 5 ; ./" + var_toolName + " -b bios -r slave ; sleep 3 ; wedge_power.sh on"
    var_keywords_pattern = cel_boot_test_b_bios_r_slave
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                path=var_path, is_negative_test=False)

def verify_cel_boot_test_b_bios_r_master():
    Log_Debug("Entering procedure verify_cel_boot_test_b_bios_r_master.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test_b_bmc_s["bin_tool"]
    #var_option = "-b bios -r master ; wedge_power.sh off ; wedge_power.sh on"
    var_option = "wedge_power.sh off ; sleep 5 ; ./" + var_toolName + " -b bios -r master ; sleep 3 ; wedge_power.sh on"
    var_keywords_pattern = cel_boot_test_b_bios_r_master
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                path=var_path, is_negative_test=False)


def verify_cel_boot_test_a():
    Log_Debug("Entering procedure verify_cel_boot_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_boot_test_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                path=var_path, is_negative_test=False)


def verify_cel_boot_test_a_fail():
    Log_Debug("Entering procedure verify_cel_boot_test_a_fail.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_boot_test_a_pattern_fail
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                path=var_path, is_negative_test=False)


def verify_cel_boot_test_a_bios_fail():
    Log_Debug("Entering procedure verify_cel_boot_test_a_bios_fail.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test["bin_tool"]
    var_option = '-a | sed -r "s/\x1B\[([0-9]{1,3}(;[0-9]{1,3})?)?[m|K]//g"'
    var_keywords_pattern = cel_boot_test_a_bios_fail_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                path=var_path, is_negative_test=False)


def verify_cel_boot_test_a_bios_and_bmc_fail():
    Log_Debug("Entering procedure verify_cel_boot_test_a_bios_and_bmc_fail.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_boot_test["bin_tool"]
    var_option = '-a | sed -r "s/\x1B\[([0-9]{1,3}(;[0-9]{1,3})?)?[m|K]//g" && sysctl -w kernel.printk=7'
    var_keywords_pattern = cel_boot_test_a_bios_and_bmc_fail_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                path=var_path, is_negative_test=False)


def collect_all_fan_manufacturer_is_present():
    Log_Debug("Entering procedure collect_all_fan_manufacturer_is_present.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "feutil"
    var_option = "all"
    var_keywords_pattern = ""
    var_pass_pattern = ""
    var_path = "/usr/local/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path, is_negative_test=True)


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

    # sleep 10 s for speed changed of fan
    time.sleep(10)
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

    time.sleep(10)
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

    time.sleep(10)
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


def verify_cel_fan_test_c():
    Log_Debug("Entering procedure verify_cel_fan_test_c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-c"  # Have to append by self.fan_manufacturer
    var_keywords_pattern = cel_fan_test_c_pattern
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


def cel_memory_info_compare():
    Log_Debug("Entering procedure cel_memory_info_compare.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_memory_test["bin_tool"]
    var_option = "-a"
    var_cmd = 'cat /proc/meminfo'
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_memory_information(var_toolName, var_option, var_cmd, var_path)


def compare_cel_memory_info(mem_cmd1=get_mem_i_cmd, mem_cmd2=get_meminfo_cmd, mem_pattern=mem_compare_pattern_dict):
    Log_Debug("Entering procedure compare_cel_memory_info.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.compare_bmc_cel_memory_info(mem_cmd1, mem_cmd2, mem_pattern)


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


def cel_emmc_info_compare():
    Log_Debug("Entering procedure cel_emmc_info_compare.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_emmc_test["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = cel_emmc_test_i_pattern
    var_path = BMC_DIAG_TOOL_PATH
    var_cmd_str1 = "fdisk -l"
    var_cmd_str2 = "dmesg | grep mmc"

    return dLibObj.verify_emmc_information(var_toolName, var_option, var_cmd_str1, var_cmd_str2, var_keywords_pattern, var_path)


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
    devicename = os.environ.get("deviceName", "")
    if 'minipack2' in devicename.lower():
        var_keywords_pattern = cel_emmc_test_a_pattern
    else:
        var_keywords_pattern = cel_emmc_test_a_pattern_wedge
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

def check_the_cpu_version():
    Log_Debug("Entering procedure check_the_cpu_version.\n")
    dLibObj = getDiagLibObj()

    var_command = "cat /proc/cpuinfo"
    var_option = ''
    var_pass_pattern = ''

    return dLibObj.verify_centos_run_command(var_command, var_option, var_pass_pattern)

def check_emmc_info():
    Log_Debug("Entering procedure check emmc info.\n")
    dLibObj = getDiagLibObj()
    #dLibObj.EXEC_bmc_diag_tool_command("sol.sh", " ")

    var_toolName = 'fdisk -l'
    var_option = ' '
    var_keywords_pattern = ''
    var_pass_pattern = check_emmc_info_test

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def check_disk_dump_file():
    Log_Debug("Entering procedure check disk.dump.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'find . -name'
    var_option = ' disk.dump'
    var_pass_pattern = ''

    return dLibObj.verify_centos_run_command(var_toolName, var_option, var_pass_pattern)

def check_the_openbmc_version():
    Log_Debug("Entering procedure check_the_openbmc_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName= "cat /etc/issue"
    var_option = ' '
    var_pattern = ''
    var_pass_pattern = check_the_openbmc_version

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pattern, var_pass_pattern)

def check_the_cpu_os_version():
    Log_Debug("Entering procedure check_the_cpu_os_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName="cat"
    var_option="/etc/product/VERSION"
    var_keywords_pattern = check_cpu_os_version
    var_pass_pattern = ""
    var_path = "/usr/bin"

    return dLibObj.verify_tool_simple_dict(toolName=var_toolName, option=var_option,
                                           keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                                           mode='centos', path=var_path)

def minipack2_verify_fpga_option_h():
    Log_Debug("Entering procedure minipack2_verify_fpga_option_h")
    dLibObj = getDiagLibObj()

    var_toolName = 'fpga'
    var_option = ' -h'
    var_keywords_pattern = minipack2_check_fpga_h
    var_pass_pattern = ''
    mode = 'centos'
    var_path = FPGA_TOOL_PATH

    return dLibObj.verify_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, mode, var_path)
def check_loopback_high_power_mode():
    Log_Debug("Entering procedure check_loopback_high_power_mode.\n")
    dLibObj = getDiagLibObj()

    var_command = "./hpmode "
    var_option = '200 0xA0 93 0x0C 2>&1'
    var_pass_pattern = [r'ERROR', r'fail', r'failed', ]

    return dLibObj.verify_centos_run_command(command=var_command, options=var_option, pass_pattern=var_pass_pattern, is_negative_test=True, check_all_line=True)


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
    var_keywords_pattern = i2cset_scm_hotswap_pattern
    var_pass_pattern = ""
    var_path = "/usr/sbin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def i2cset_fcm_hotswap():
    Log_Debug("Entering procedure i2cset_fcm_hotswap.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "i2cset"
    var_option = "-f -y 11 0x76 0x8 && i2cget -f -y 11 0x10 0x19"
    var_keywords_pattern = i2cset_fcm_hotswap_pattern
    var_pass_pattern = ""
    var_path = "/usr/sbin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

@logThis
def verify_PSU_EEPROM_dict_option_a():
    dLibObj = getDiagLibObj()

    var_toolName = cel_psu_test["bin_tool"]
    var_option = '-a'
    var_keywords_pattern = PSU_EEPROM_dict_a
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)


def verify_PSU_EEPROM_dict_option_h():
    Log_Debug("Entering procedure verify_PSU_EEPROM_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_psu_test["bin_tool"]
    var_option = '-h'
    var_keywords_pattern = PSU_EEPROM_dict_h
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def verify_PSU_EEPROM_dict_option_i():
    Log_Debug("Entering procedure verify_PSU_EEPROM_dict_option_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_psu_test["bin_tool"]
    var_option = '-i'
    var_keywords_pattern = PSU_EEPROM_dict_i
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.PSU_EEPROM_dict_option_i(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def verify_PSU_EEPROM_dict_option_s():
    Log_Debug("Entering procedure verify_PSU_EEPROM_dict_option_s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_psu_test["bin_tool"]
    var_option = '-s'
    var_keywords_pattern = ''
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.PSU_EEPROM_dict_option_s(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def verify_get_psu_info(param = ''):
    Log_Debug("Entering procedure verify_get_psu_info.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'psu-util'
    var_option = param + ' ' + '--get_psu_info'
    var_keywords_pattern = ''
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.get_psu_eeprom_info(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_get_eeprom_info(param=''):
    Log_Debug("Entering procedure verify_get_eeprom_info.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'psu-util'
    var_option = param + ' ' + '--get_eeprom_info'
    var_keywords_pattern = ''
    var_pass_pattern = ''
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.get_psu_eeprom_info(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_psu_test_h():
    Log_Debug("Entering procedure cel_psu_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_psu_test["bin_tool"]
    var_option = "-h && sysctl -w kernel.printk=3"  # Disable the I2C notice message during PSU test
    var_keywords_pattern = cel_psu_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_psu_test_i():
    Log_Debug("Entering procedure cel_psu_test_i.\n")
    dLibObj = getDiagLibObj()
    if dLibObj.is_using_pem():
        return
    var_toolName = cel_psu_test["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = cel_psu_test_i_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_psu_test_s():
    Log_Debug("Entering procedure cel_psu_test_s.\n")
    dLibObj = getDiagLibObj()
    if dLibObj.is_using_pem():
        return
    var_toolName = cel_psu_test["bin_tool"]
    var_option = "-s"
    var_keywords_pattern = cel_psu_test_s_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_psu_test_a():
    Log_Debug("Entering procedure cel_psu_test_a.\n")
    dLibObj = getDiagLibObj()
    if dLibObj.is_using_pem():
        return
    var_toolName = cel_psu_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_psu_test_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def psu_util_psu1_get_psu_info():
    Log_Debug("Entering procedure psu_util_psu1_get_psu_info.\n")
    dLibObj = getDiagLibObj()
    if dLibObj.is_using_pem():
        return
    var_toolName = "psu-util"
    var_option = "psu1 --get_psu_info"
    var_keywords_pattern = psu_util_psu1_get_psu_info_pattern
    var_pass_pattern = ''
    var_path = "/usr/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)


def psu_util_psu2_get_psu_info():
    Log_Debug("Entering procedure psu_util_psu2_get_psu_info.\n")
    dLibObj = getDiagLibObj()
    if dLibObj.is_using_pem():
        return
    var_toolName = "psu-util"
    var_option = "psu2 --get_psu_info"
    var_keywords_pattern = psu_util_psu2_get_psu_info_pattern
    var_pass_pattern = ''
    var_path = "/usr/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)


def psu_util_psu1_get_eeprom_info():
    Log_Debug("Entering procedure psu_util_psu1_get_eeprom_info.\n")
    dLibObj = getDiagLibObj()
    if dLibObj.is_using_pem():
        return
    var_toolName = "psu-util"
    var_option = "psu1 --get_eeprom_info"
    var_keywords_pattern = catch_psu1_fru_info_pattern
    var_pass_pattern = ''
    var_path = "/usr/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)


def psu_util_psu2_get_eeprom_info():
    Log_Debug("Entering procedure psu_util_psu2_get_eeprom_info.\n")
    dLibObj = getDiagLibObj()
    if dLibObj.is_using_pem():
        return
    var_toolName = "psu-util"
    var_option = "psu2 --get_eeprom_info && sysctl -w kernel.printk=7"  # See the debug message level to default
    var_keywords_pattern = catch_psu2_fru_info_pattern
    var_pass_pattern = ''
    var_path = "/usr/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)


def compare_psu_info_diag_and_openbmc_tools():
    Log_Debug("Entering procedure compare_psu_info_diag_and_openbmc_tools.\n")
    dLibObj = getDiagLibObj()
    if dLibObj.is_using_pem():
        return
    return dLibObj.compare_psu_info_diag_and_openbmc_tools()


def read_current_bmc_version():
    Log_Debug("Entering procedure read_current_bmc_version.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.get_current_bmc_version()

def flashcp_flashfuji_low_level():
    Log_Debug("Entering procedure flashcp_flashfuji_low_level.\n")
    dLibObj = getDiagLibObj()

    var_toolName = flashtool
    var_flash_device = flash_fuji
    var_flash_path = flash_fuji_path10
    var_option = '-v'
    var_path = ''

    return dLibObj.EXEC_flashcp_flashfuji_lever(var_toolName, var_flash_device, var_flash_path, var_option, var_path)

def flashcp_flashfuji_update_level():
    Log_Debug("Entering procedure flashcp_flashfuji_update_level.\n")
    dLibObj = getDiagLibObj()

    var_toolName = flashtool
    var_flash_device = flash_fuji
    var_flash_path = flash_fuji_path11
    var_option = '-v'
    var_path = ''

    return dLibObj.EXEC_flashcp_flashfuji_lever(var_toolName, var_flash_device, var_flash_path, var_option, var_path)

def flashcp_option_v_upgrade_level():
    Log_Debug("Entering procedure flashcp_option_v_upgrade_level\n")
    dLibObj = getDiagLibObj()

    var_toolName = flashtool
    var_flash_device = flash_fuji
    var_flash_path = flash_fuji_path11
    var_option = '-v'
    var_path = ''

    return dLibObj.flash_option_v_upgrade_level(var_toolName, var_flash_device, var_flash_path, var_option, var_path)

def flash_update_and_verify_bmc_fw():
    Log_Debug("Entering procedure flash_update_and_verify_bmc_fw.\n")
    dLibObj = getDiagLibObj()

    var_toolName = flashtool
    var_img_path = bmc_img_path
    var_downgrade_bmc_image = bmc_downgrade_file
    var_upgrade_bmc_image = bmc_upgrade_file
    var_downgrade_ver = bmc_downgrade_ver
    var_upgrade_ver = bmc_upgrade_ver
    var_flash_device = flash_device_path

    return dLibObj.flash_update_and_verify_bmc(var_toolName, var_img_path, var_downgrade_bmc_image, var_upgrade_bmc_image,
                                               var_downgrade_ver, var_upgrade_ver, var_flash_device)


def set_and_verify_cpld_register_before_update():
    Log_Debug("Entering procedure set_and_verify_cpld_register_before_update.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cpld_verify_tool
    var_module = smb_cpld
    var_set_reg = bios_smb_set_reg
    var_set_val = bios_smb_before_update_value
    var_toolPath = FPGA_TOOL_PATH

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


def check_bmc_version(is_minipack2=False):
    Log_Debug("Entering procedure check_bmc_version\n")
    dLibObj = getDiagLibObj()

    toolName = 'OpenBMC Release'
    option = '-v'

    return dLibObj.check_current_bmc_version(toolName, option, is_minipack2)


def check_the_bmc_version(is_minipack2=False):
    Log_Debug("Entering procedure check_the_bmc_version\n")
    dLibObj = getDiagLibObj()

    toolName = 'OpenBMC Release'
    option = '-v'

    var_platform = 'cloudripper'

    return dLibObj.check_current_bmc_version(toolName, option, is_minipack2, var_platform)


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

    var_inputArray = cel_fw_sw_version_array
    var_toolName = fw_util_tool
    var_fru = "scm"
    var_option = "--version"
    var_tool_path = FW_UTIL_PATH
    var_key = "BIOS_VER"

    return dLibObj.verify_option_bmc_tool_system_dict(var_inputArray, var_toolName, var_fru, var_option, var_tool_path, var_key)


def flash_update_master_bios_region():
    Log_Debug("Entering procedure flash_update_master_bios_region.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "update"
    var_dev = "bios"
    var_check_pattern = fwUtil_update_pattern
    var_downgrade_bios_image = bios_downgrade_file
    var_upgrade_bios_image = bios_upgrade_file
    var_upgrade_ver = bios_upgrade_ver
    var_downgrade_ver = bios_downgrade_ver
    var_img_path = bios_img_path
    var_tool_path = FW_UTIL_PATH

    return dLibObj.flash_update_master_bios(var_toolName, var_fru, var_opt, var_dev, var_check_pattern, var_downgrade_bios_image,
                                                var_upgrade_bios_image, var_upgrade_ver, var_downgrade_ver, var_img_path, var_tool_path)


def verify_master_bios_version():
    Log_Debug("Entering procedure verify_master_bios.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.switch_and_verify_master_bios_version()


def check_bic_version():
    Log_Debug("Entering procedure check_bic_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_fru = "scm"
    var_opt = "--version"
    var_tool_path = FW_UTIL_PATH

    return dLibObj.get_current_bic_version(var_toolName, var_fru, var_opt, var_tool_path)


def cel_sensor_test_h():
    Log_Debug("Entering procedure cel_sensor_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_sensor_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_sensor_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_sensor_test_d():
    Log_Debug("Entering procedure cel_sensor_test_d.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_sensor_test["bin_tool"]
    var_option = "-d"
    var_keywords_pattern = ''
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_sensor_test_bc(param = ''):
    Log_Debug("Entering procedure cel_sensor_test_d.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_sensor_test["bin_tool"]
    var_option = "-b " + param + ' -c'
    var_keywords_pattern = cel_sensor_test_bc_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_sensor_test_a():
    Log_Debug("Entering procedure cel_sensor_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_sensor_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_sensor_test_bc_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_sensor_test_s():
    Log_Debug("Entering procedure cel_sensor_test_s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_sensor_test["bin_tool"]
    var_option = "-s"
    var_keywords_pattern = cel_sensor_test_s_pattern
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.sensors_test_option_s(var_toolName, var_option, var_keywords_pattern, var_path)

def sensors_test():
    Log_Debug("Entering procedure sensors test.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'sensors'
    var_option = ' '
    var_keywords_pattern = cel_sensor_test_s_pattern
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.sensors_test_option_s(var_toolName, var_option, var_keywords_pattern, var_path)

def sensor_util_all_threshold():
    Log_Debug("Entering procedure sensor_util_all_threshold.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'sensor-util all --threshold'
    var_option = ' '
    var_keywords_pattern = cel_sensor_test_u_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_sensor_test_u():
    Log_Debug("Entering procedure cel_sensor_test_u.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_sensor_test["bin_tool"]
    var_option = "-u"
    var_keywords_pattern = cel_sensor_test_u_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_ocp_test_h():
    Log_Debug("Entering procedure cel_ocp_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_ocp_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_ocp_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_ocp_test_a_come():
    Log_Debug("Entering procedure cel_ocp_test_a_come.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_ocp_test["bin_tool"]
    var_option = "-a come"
    var_keywords_pattern = cel_ocp_test_a_come_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_ocp_test_s_come():
    Log_Debug("Entering procedure cel_ocp_test_s_come.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_ocp_test["bin_tool"]
    var_option = "-s come"
    var_keywords_pattern = cel_ocp_test_s_come_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_ocp_test_g_come():
    Log_Debug("Entering procedure cel_ocp_test_g_come.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_ocp_test["bin_tool"]
    var_option = "-g"
    var_keywords_pattern = cel_ocp_test_g_come_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_ocp_test_fdisk_come():
    Log_Debug("Entering procedure cel_ocp_test_fdisk_come.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "fdisk"
    var_option = ""
    var_keywords_pattern = cel_ocp_test_fdisk_come_pattern
    var_pass_pattern = ""
    var_path = "/sbin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_ocp_test_s_bmc():
    Log_Debug("Entering procedure cel_ocp_test_s_bmc.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_ocp_test["bin_tool"]
    var_option = "-s bmc"
    var_keywords_pattern = cel_ocp_test_s_bmc_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_ocp_test_g_bmc():
    Log_Debug("Entering procedure cel_ocp_test_g_bmc.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_ocp_test["bin_tool"]
    var_option = "-g"
    var_keywords_pattern = cel_ocp_test_g_bmc_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_ocp_test_cat_bmc():
    Log_Debug("Entering procedure cel_ocp_test_cat_bmc.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "cat"
    var_option = "/etc/issue"
    var_keywords_pattern = cel_ocp_test_cat_bmc_pattern
    var_pass_pattern = ""
    var_path = "/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_ocp_test_a_bmc():
    Log_Debug("Entering procedure cel_ocp_test_a_bmc.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_ocp_test["bin_tool"]
    var_option = "-a bmc"
    var_keywords_pattern = cel_ocp_test_a_bmc_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def check_update_cpld_option_h():
    Log_Debug("Entering procedure check_update_cpld_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cel-cpld_update'
    var_option = '-h'
    var_keywords_pattern = check_update_cpld_h
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def check_update_cpld_SMB_option_f():
    Log_Debug("Entering procedure check_update_cpld_SMB_option_f.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cel-cpld_update '
    var_option = ' -s SMB -f' + ' ' + Update_CPLD_SMB_Image_PATH
    var_keywords_pattern = check_update_CPLD_SMB_image
    var_pass_pattern = ''

    return dLibObj.verify_cpld_update_SMB_version(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def check_i2c_upgrade_cpld_option_h():
    Log_Debug("Entering procedure check_i2c_upgrade_cpld_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cel-i2c_upgrade_cpld'
    var_option = '-h'
    var_keywords_pattern = check_i2c_upgrade_cpld_h
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def check_i2c_upgrade_cpld_SMB_option_f():
    Log_Debug("Entering procedure check_i2c_upgrade_cpld_SMB_option_f.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cel-i2c_upgrade_cpld'
    var_option = '-s SMB -f' + ' ' + CPLD_MiniPack2_SMB_CPLD_TOP_PATH
    var_keywords_pattern = check_i2c_upgrade_cpld_SMB_f
    var_pass_pattern = ''

    return dLibObj.verify_i2c_cpld_SMB_version(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def cel_software_test_h():
    Log_Debug("Entering procedure cel_software_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_software_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_software_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

@logThis
def fw_util_pim_fpga_version():
    dLibObj = getDiagLibObj()

    toolName = fw_util_tool
    option = ' fpga --version'
    keywords_pattern = pim_fpga_pattern
    pass_pattern = ''
    path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName, option, keywords_pattern, pass_pattern, path)

def fpga_check_sLPC(param=''):
    Log_Debug("Entering procedure verify fpga_check_sLPC")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fpga_sLPC["bin_tool"]
    command_list = [
        'pim w pim=' + param + ' 0x80 0x0',
        'pim r pim=' + param + ' 0',
        'reg r*16 0x40',
        'pim w pim=' + param + ' 0x80 0x1',
        'reg w 0x20 1',
        'pim r pim=' + param + ' 0',
        'reg r*16 0x40',
    ]
    for value in command_list:
        var_option = value
        var_keywords_pattern = cel_sLPC_test
        var_path = FPGA_TOOL_PATH

        dLibObj.verify_fpga_sLPC(var_toolName, var_option, var_keywords_pattern, var_path)

def cel_software_test_i():
    Log_Debug("Entering procedure cel_software_test_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_software_test["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = cel_software_test_i_or_v_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_software_v():
    Log_Debug("Entering procedure cel_software_test_v.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_software_test["bin_tool"]
    var_option = "-v"
    var_keywords_pattern = cel_software_v_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_software_test_v(check_fpga_version=True, bic_version=bic_upgrade_ver, bios_version=bios_upgrade_ver):
    Log_Debug("Entering procedure cel_software_test_v.\n")
    dLibObj = getDiagLibObj()

    _keywords_pattern = list()

    ####################### MINIPACK2 #############################
    devicename = os.environ.get("deviceName", "")
    import logging
    logging.info("devicename:{}".format(devicename))
    if "minipack2" in devicename.lower():
        _keywords_pattern = mp2_cel_software_test_v_pattern

        # BIOS Version replacement with condition
        for pindex, pattern in enumerate(_keywords_pattern):
            if str(pattern).__contains__("BIOS") and str(pattern).__contains__("Version"):
                _keywords_pattern[pindex] = r'^[ \t]*BIOS[ \t]+Version:[ \t]+' + bios_version + r'[ \t]*$'

    ####################### WEDGE400 ##############################
    elif "wedge400" in devicename.lower():
        _keywords_pattern = cel_software_test_i_or_v_pattern

        # FPGA 1&2 condition check
        if check_fpga_version == False:
            # Just check FPGA version for not show an error
            for pindex, pattern in enumerate(_keywords_pattern):
                if str(pattern).__contains__("DOM_FPGA_1"):
                    _keywords_pattern[pindex] = r'^[ \t]*(SMB_)?DOM_FPGA_1[ \t]+:[ \t]+\d+\.\d+'
                if str(pattern).__contains__("DOM_FPGA_2"):
                    _keywords_pattern[pindex] = r'^[ \t]*(SMB_)?DOM_FPGA_2[ \t]+:[ \t]+\d+\.\d+'

        # Bridge-IC Version replacement with condition
        for pindex, pattern in enumerate(_keywords_pattern):
            if str(pattern).__contains__("Bridge-IC") and str(pattern).__contains__("Version"):
                if bic_version == "False":
                    _keywords_pattern[pindex] = r'^[ \t]*Bridge-IC[ \t]+Version:[ \n\t]+v\d+\.\d+'
                else:
                    if not str(bic_version).__contains__(r"."):
                        str(bic_version).replace(".", r".")

                    _keywords_pattern[pindex] = r'^[ \t]*Bridge-IC[ \t]+Version:[ \n\t]+' + bic_version


    var_toolName = cel_software_test["bin_tool"]
    var_option = "-v"
    var_keywords_pattern = _keywords_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_software_test_a():
    Log_Debug("Entering procedure cel_software_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_software_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_software_test_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_swtest_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cat_etc_issue_bmc():
    Log_Debug("Entering procedure cat_etc_issue_bmc.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "cat"
    var_option = "/etc/issue"
    var_keywords_pattern = cat_etc_issue_bmc_pattern
    var_pass_pattern = ""
    var_path = "/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cpld_ver_sh():
    Log_Debug("Entering procedure cpld_ver_sh.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "cpld_ver.sh"
    var_option = ""
    var_keywords_pattern = cpld_ver_sh_pattern
    var_pass_pattern = ""
    var_path = "/usr/local/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def fpga_ver_sh():
    Log_Debug("Entering procedure fpga_ver_sh.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "fpga_ver.sh"
    var_option = ""
    var_keywords_pattern = ''
    var_pass_pattern = ""
    var_path = "/usr/local/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def minipack2_fpga_ver_sh():
    Log_Debug("Entering procedure minipack2_fpga_ver_sh.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "fpga ver"
    var_option = ""
    var_keywords_pattern = fpga_ver_sh_pattern
    var_pass_pattern = ""
    var_path = "/usr/local/cls_diag/utility/"

    return dLibObj.minipack2_fpga_ver_test(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cat_etc_product_version():
    Log_Debug("Entering procedure cat_etc_product_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "cat"
    var_option = "/etc/product/VERSION"
    var_keywords_pattern = cat_etc_product_version_pattern
    var_pass_pattern = ""
    var_path = "/bin"
    return dLibObj.verify_tool_simple_dict(toolName=var_toolName, option=var_option,
                                           keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern,
                                           mode='centos', path=var_path)

def cat_etc_redhat_release():
    Log_Debug("Entering procedure cat_redhat_release.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cat'
    var_option = "/etc/redhat-release"
    var_keywords_pattern = cat_etc_redhat_release_pattern
    var_pass_pattern = ''
    var_path = "/bin"

    return dLibObj.verify_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern,
                                                        pass_pattern=var_pass_pattern, mode='centos', path=var_path)

def cel_platform_test_h():
    Log_Debug("Entering procedure cel_platform_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_platform_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_i():
    Log_Debug("Entering procedure cel_platform_test_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = cel_platform_test_i_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

@logThis
def cel_platform_test_p():
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-p"
    var_keywords_pattern = cel_platform_test_p_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_platform_test_a():
    Log_Debug("Entering procedure cel_platform_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-a"
    var_keywords_pattern = cel_platform_test_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_e_all():
    Log_Debug("Entering procedure cel_platform_test_e_all.\n")
    dLibObj = getDiagLibObj()

    if not dLibObj.is_using_pem():
        for index, pattern in enumerate(cel_platform_test_e_all_pattern):
            if str(pattern).__contains__("get_eeprom_pem"):
                cel_platform_test_e_all_pattern[index] = r'^[ \t]*get_eeprom_pem[ \t\s]*.+FAIL'
                break

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-e all"
    var_keywords_pattern = cel_platform_test_e_all_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_e_fcm(fcm_option="fcm"):
    Log_Debug("Entering procedure cel_platform_test_e_fcm.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-e {}".format(fcm_option)
    var_keywords_pattern = cel_platform_test_e_fcm_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_e(option="sim", patterns=cel_platform_test_e_pattern):
    Log_Debug("Entering procedure cel_platform_test_e.\n")
    dLibObj = getDiagLibObj()

    Log_Debug("patterns:{}.".format(patterns))
    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-e {}".format(option)
    if "fan" in option:
        option = "fan"
    elif "pim" in option:
        option = "pim"
    var_keywords_pattern = copy.deepcopy(patterns)
    var_keywords_pattern[1] += option.upper()
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_e_fan1():
    Log_Debug("Entering procedure cel_platform_test_e_fan1.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-e fan1"
    var_keywords_pattern = cel_platform_test_e_fan1_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_e_fan2():
    Log_Debug("Entering procedure cel_platform_test_e_fan2.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-e fan2"
    var_keywords_pattern = cel_platform_test_e_fan2_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_e_fan3():
    Log_Debug("Entering procedure cel_platform_test_e_fan3.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-e fan3"
    var_keywords_pattern = cel_platform_test_e_fan3_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_e_fan4():
    Log_Debug("Entering procedure cel_platform_test_e_fan4.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-e fan4"
    var_keywords_pattern = cel_platform_test_e_fan4_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_e_smb():
    Log_Debug("Entering procedure cel_platform_test_e_smb.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-e smb"
    var_keywords_pattern = cel_platform_test_e_smb_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_e_scm():
    Log_Debug("Entering procedure cel_platform_test_e_scm.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_platform_test["bin_tool"]
    var_option = "-e scm"
    var_keywords_pattern = cel_platform_test_e_scm_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_platform_test_e_pem():
    Log_Debug("Entering procedure cel_platform_test_e_pem.\n")
    dLibObj = getDiagLibObj()

    if dLibObj.is_using_pem():
        var_toolName = cel_platform_test["bin_tool"]
        var_option = "-e pem"
        var_keywords_pattern = cel_platform_test_e_pem_pattern
        var_pass_pattern = ""
        var_path = BMC_DIAG_TOOL_PATH

        return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)
    else:
        Log_Debug('***PEM2 not present***')
        dLibObj.wpl_execute('echo ' + 'PEM2 not present')

def disable_watchdog_for_ddr_test():
    Log_Debug("Entering procedure disable_watchdog_for_ddr_test.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "devmem"
    var_option = "0x1e78500c 32 0"
    var_keywords_pattern = disable_watchdog_for_ddr_test_pattern
    var_pass_pattern = ""
    var_path = "/sbin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern,
                                                    var_pass_pattern, var_path)


def remove_ddr_log():
    Log_Debug("Entering procedure remove_ddr_log.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "rm"
    var_option = "-f /mnt/data1/BMC_Diag/utility/stress/DDR.log"
    var_keywords_pattern = rm_ddr_log_pattern
    var_pass_pattern = ""
    var_path = "/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern,
                                                    var_pass_pattern, var_path)


def ddr_test_sh():
    Log_Debug("Entering procedure ddr_test_sh.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.verify_the_free_mem_before_and_after_run_ddr_test_sh()


def syslog_h():
    Log_Debug("Entering procedure syslog_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = sys_log["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = sys_log_h_pattern
    var_pass_pattern = ""
    var_path = "/mnt/data1/BMC_Diag/utility/stress/syslog"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern,
                                                    var_pass_pattern, var_path)


def syslog_l():
    Log_Debug("Entering procedure syslog_l.\n")
    dLibObj = getDiagLibObj()

    var_toolName = sys_log["bin_tool"]
    var_option = "-l sys.log"
    var_keywords_pattern = sys_log_l_pattern
    var_pass_pattern = ""
    var_path = "/mnt/data1/BMC_Diag/utility/stress/syslog"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern,
                                                    var_pass_pattern, var_path)


def verify_fpga_downgrade_version():
    Log_Debug("Entering procedure verify_fpga_ver_sh_downgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "fpga_ver.sh"
    var_option = ""
    var_keywords_pattern = verify_fpga_ver_sh_downgrade_pattern
    var_pass_pattern = ""
    var_path = "/usr/local/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern,
                                                    var_pass_pattern, var_path)


def verify_fpga_upgrade_version():
    Log_Debug("Entering procedure verify_fpga_upgrade_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "fpga_ver.sh"
    var_option = ""
    var_keywords_pattern = verify_fpga_ver_sh_upgrade_pattern
    var_pass_pattern = ""
    var_path = "/usr/local/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern,
                                                    var_pass_pattern, var_path)


def wedge_reboot_whole_system():
    Log_Debug("Entering procedure wedge_reboot_whole_system.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.wedge_reboot_whole_system(mode='openbmc')


def test_all_sh():
    Log_Debug("Entering procedure test_all_sh.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "test_all.sh"
    var_option = ""
    var_keywords_pattern = test_all_sh_pattern
    var_pass_pattern = ""
    var_path = "/mnt/data1/BMC_Diag/utility"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern,
                                                    var_pass_pattern, var_path)


def cel_tpm_test_h():
    Log_Debug("Entering procedure cel_tpm_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_tpm_test["bin_tool"]
    var_option = "-h && sysctl -w kernel.printk=3"
    var_keywords_pattern = cel_tpm_test_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_tpm_test_c():
    Log_Debug("Entering procedure cel_tpm_test_c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_tpm_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_tpm_test_device_c_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def cel_tpm_device_test_i():
    Log_Debug("Entering procedure cel_tpm_device_test_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_tpm_test["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = cel_tpm_test_device_i_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_bmc_i2c_option_h():
    Log_Debug("Entering procedure verify_bmc_i2c_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_i2c_help_array["bin_tool"]
    var_option = "-h"
    var_pattern = bmc_i2c_help_option_pattern

    return dLibObj.verify_bmc_i2c_tool_simple_dict(var_toolName, var_option, var_pattern)

def cel_tpm_test_a():
    Log_Debug("Entering procedure cel_tpm_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_tpm_test["bin_tool"]
    var_option = '-a'
    var_keywords_pattern = cel_tpm_test_device_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_tpm_test_a(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

@logThis
def cel_tpm_test_c():
    dLibObj = getDiagLibObj()

    var_toolName = cel_tpm_test["bin_tool"]
    var_option = '-c'
    var_keywords_pattern = cel_tpm_test_device_c_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_tpm_test_a(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def cel_tpm_test_i():
    Log_Debug("Entering procedure cel_tpm_test_i.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_tpm_test["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = cel_tpm_test_i_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def spi_util_sh_write():
    Log_Debug("Entering procedure spi_util_sh_write.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spi_util_sh["bin_tool"]
    var_option = "write spi1 BCM5389_EE image.bin"
    var_keywords_pattern = spi_util_write_pattern
    var_pass_pattern = ""
    var_path = "/usr/local/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def spi_util_sh_read():
    Log_Debug("Entering procedure spi_util_sh_read.\n")
    dLibObj = getDiagLibObj()

    var_toolName = spi_util_sh["bin_tool"]
    var_option = "read spi1 BCM5389_EE image"
    var_keywords_pattern = spi_util_read_pattern
    var_pass_pattern = ""
    var_path = "/usr/local/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def create_oob_image_one():
    Log_Debug("Entering procedure create_oob_image_one.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'hexdump'
    var_option = oob_upgrade_file + " | head -n 2 > image1"
    var_keywords_pattern = ''
    var_pass_pattern = ""
    var_path = '/usr/bin'

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def create_oob_image_two():
    Log_Debug("Entering procedure create_oob_image_two.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'hexdump'
    var_option = "image | head -n 2 > image2"
    var_keywords_pattern = ''
    var_pass_pattern = ""
    var_path = '/usr/bin'

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def diff_oob_image():
    Log_Debug("Entering procedure diff_oob_image.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'diff'
    var_option = "image1 image2"
    var_keywords_pattern = ''
    var_pass_pattern = ""
    var_path = '/usr/bin'

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path, is_negative_test=True)


def get_ip_and_ping():
    Log_Debug("Entering procedure get_ip_and_ping.\n")
    remote_ip = scp_ip
    Log_Debug("remote_ip:%s"%(remote_ip))
    eth0 = "eth0"
    dLibObj = getDiagLibObj()
    COMe_ip = CommonLib.check_ip_address(Const.DUT, eth0, "centos")
    Log_Debug("COMe_ip:%s"%(COMe_ip))
    openbmc_ip = CommonLib.check_ip_address(Const.DUT, eth0, "openbmc")
    Log_Debug("openbmc_ip:%s"%(openbmc_ip))
    CommonLib.exec_ping(Const.DUT, remote_ip, 6, "openbmc")
    CommonLib.exec_ping(Const.DUT, COMe_ip, 6, "openbmc")
    CommonLib.exec_ping(Const.DUT, remote_ip, 6, "centos")
    CommonLib.exec_ping(Const.DUT, openbmc_ip, 6, "centos")


def run_and_verify_for_openbmc(tool="", args="", path="", regex=list(), match_count=int(), is_negative_test=False, prefix="./"):
    Log_Debug("Entering procedure run_and_verify_for_openbmc.\n")
    dLibObj = getDiagLibObj()

    var_toolName = tool
    var_option = args
    var_keywords_pattern = regex
    var_pass_pattern = ''
    var_path = path
    var_is_negative_test = is_negative_test
    var_prefix = prefix

    return dLibObj.verify_bmc_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
            keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path,
            is_negative_test=var_is_negative_test, prefix=var_prefix)


def run_and_verify_for_centos(tool="", args="", path=DIAG_TOOL_PATH, regex=list(), match_count=int()):
    Log_Debug("Entering procedure run_and_verify_for_centos.\n")
    dLibObj = getDiagLibObj()

    var_toolName = tool
    var_option = args
    var_keywords_pattern = regex
    var_pass_pattern = ''
    var_path = path

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
            keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path, matchCount=match_count)


def cel_qsfp_test_h():
    Log_Debug("Entering procedure cel_qsfp_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = ''
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)


def cel_qsfp_test_help():
    Log_Debug("Entering procedure cel_qsfp_test_help.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_option = "--help"
    var_keywords_pattern = ''
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)


def cel_qsfp_test_p_0_s(pattern):
    Log_Debug("Entering procedure cel_qsfp_test_cel_qsfp_test_p_0_s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_option = "-p0 -s"
    var_keywords_pattern = pattern
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
              keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path, matchCount=48)

def cloudripper_cel_qsfp_test_p_0_s(pattern):
    Log_Debug("Entering procedure cloudripper cel qsfp test port 0 s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_option = "-p0 -s"
    var_keywords_pattern = pattern
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
              keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path, matchCount=32)

def cloudripper_cel_qsfp_test_port_0_status(pattern):
    Log_Debug("Entering procedure cloudripper cel qsfp test port 0 status.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_option = "--port=0 --status"
    var_keywords_pattern = pattern
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
              keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path, matchCount=32)

@logThis
def cloudripper_cel_qsfp_test_check_port_s_one_by_one():
    
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 33):
        var_option = "--port=" + str(port) + " -s"
        var_keywords_pattern = [
            str(port) + r'[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
        ]

        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)
def cloudripper_cel_qsfp_test_check_port_status_one_by_one():
    Log_Debug("Entering procedure cloudripper cel qsfp test check port status one by one.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 33):
        var_option = "--port=" + str(port) + " --status"
        var_keywords_pattern = [
            str(port) + r'[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
        ]

        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

@logThis
def cloudripper_cel_qsfp_test_check_port_i_one_by_one():
    dLibObj = getDiagLibObj()

    cel_qsfp_test_set_reset('off')
    cel_qsfp_test_set_lpmode('off')
    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 33):
        var_option = "-p" + str(port) + " -i"
        var_keywords_pattern = cel_qsfp_test_eeprom_pattern
        cel_qsfp_test_set_reset('on')
        cel_qsfp_test_set_reset('off')
        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

@logThis
def cloudripper_cel_qsfp_test_check_port_info_one_by_one():
    dLibObj = getDiagLibObj()

    cel_qsfp_test_set_reset('off')
    cel_qsfp_test_set_lpmode('off')
    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 33):
        var_option = "--port=" + str(port) + " --info"
        var_keywords_pattern = cel_qsfp_test_eeprom_pattern
        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

@logThis
def cloudripper_cel_qsfp_test_check_port_is_one_by_one():
    dLibObj = getDiagLibObj()

    cel_qsfp_test_set_reset('off')
    cel_qsfp_test_set_lpmode('on')
    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 33):
        var_option = "-p" + str(port) + " -I"
        var_keywords_pattern = cel_qsfp_test_eeprom_pattern
        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

@logThis
def cloudripper_cel_qsfp_test_check_port_Simple_one_by_one():
    dLibObj = getDiagLibObj()

    cel_qsfp_test_set_reset('off')
    cel_qsfp_test_set_lpmode('on')
    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 33):
        var_option = "--port=" + str(port) + " --simple"
        var_keywords_pattern = cel_qsfp_test_eeprom_pattern
        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def cel_qsfp_test_port_0_status(pattern):
    Log_Debug("Entering procedure cel_qsfp_test_port_0_status.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_option = "--port=0 --status"
    var_keywords_pattern = pattern
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
              keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path, matchCount=48)

@logThis
def cel_qsfp_test_check_port_s_one_by_one():
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 49):
        var_option = "-p" + str(port) + " -s"
        var_keywords_pattern = [
            str(port) + r'[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
        ]

        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def cel_qsfp_test_check_port_status_one_by_one():
    Log_Debug("Entering procedure cel_qsfp_test_check_port_status_one_by_one.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 49):
        var_option = "--port=" + str(port) + " --status"
        var_keywords_pattern = [
            str(port) + r'[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
        ]

        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

@logThis
def cel_qsfp_test_check_port_i_one_by_one():
    dLibObj = getDiagLibObj()

    cel_qsfp_test_set_reset('off')
    cel_qsfp_test_set_lpmode('off')
    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 49):
        var_option = "-p" + str(port) + " -i"
        var_keywords_pattern = cel_qsfp_test_eeprom_pattern
        cel_qsfp_test_set_reset('on')
        cel_qsfp_test_set_reset('off')
        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

@logThis
def cel_qsfp_test_check_port_info_one_by_one():
    dLibObj = getDiagLibObj()

    cel_qsfp_test_set_reset('off')
    cel_qsfp_test_set_lpmode('off')
    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 49):
        var_option = "--port=" + str(port) + " --info"
        var_keywords_pattern = cel_qsfp_test_eeprom_pattern
        cel_qsfp_test_set_reset('on')
        cel_qsfp_test_set_reset('off')
        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

@logThis
def cel_qsfp_test_check_port_is_one_by_one():
    dLibObj = getDiagLibObj()

    cel_qsfp_test_set_reset('off')
    cel_qsfp_test_set_lpmode('off')
    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 49):
        var_option = "-p" + str(port) + " -I"
        var_keywords_pattern = cel_qsfp_test_eeprom_pattern
        cel_qsfp_test_set_reset('on')
        cel_qsfp_test_set_reset('off')
        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

@logThis
def cel_qsfp_test_check_port_Simple_one_by_one():
    dLibObj = getDiagLibObj()

    cel_qsfp_test_set_reset('off')
    cel_qsfp_test_set_lpmode('off')
    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    for port in range(1, 49):
        var_option = "--port=" + str(port) + " --simple"
        var_keywords_pattern = cel_qsfp_test_eeprom_pattern
        cel_qsfp_test_set_reset('on')
        cel_qsfp_test_set_reset('off')
        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def cel_qsfp_test_set_reset(status):
    Log_Debug("Entering procedure cel_qsfp_test_set_reset.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_option = "-p0 -r " + status
    var_keywords_pattern = ''
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def cel_qsfp_test_set_lpmode(status):
    Log_Debug("Entering procedure cel_qsfp_test_set_lpmode.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_option = "-p0 -l " + status
    var_keywords_pattern = ''
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def cel_qsfp_test_all():
    Log_Debug("Entering procedure cel_qsfp_test_all.\n")
    dLibObj = getDiagLibObj()
    for option in ['-a', '--all']:
        var_toolName = "./" + cel_qsfp_test["bin_tool"]
        var_option = option
        var_keywords_pattern = cel_qsfp_test_all_pattern
        var_pass_pattern = ''
        var_path = DIAG_TOOL_PATH

        dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def cel_qsfp_test_set_default():
    Log_Debug("Entering procedure cel_qsfp_test_set_default.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_qsfp_test["bin_tool"]
    var_keywords_pattern = ''
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    var_option = "-p0 -r off"
    dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                                                      keywords_pattern=var_keywords_pattern,
                                                      pass_pattern=var_pass_pattern, path=var_path)
    var_option = "-p0 -l on"
    dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                                                      keywords_pattern=var_keywords_pattern,
                                                      pass_pattern=var_pass_pattern, path=var_path)


@logThis
def check_diag_version_before():
    dLibObj = getDiagLibObj()

    var_toolName = './' + cel_version_test["bin_tool"]
    var_option = ' -S'
    var_keywords_pattern = ''
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_befor_diag_version(var_toolName,var_option,var_keywords_pattern,var_pass_pattern,var_path)

def check_diag_version():
    Log_Debug("Check diag version:\n")
    dLibObj = getDiagLibObj()

    var_toolName ='./' + cel_version_test["bin_tool"]
    var_option = ' -S'
    var_keywords_pattern = cel_version_S
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                                                      keywords_pattern=var_keywords_pattern,
                                                      pass_pattern=var_pass_pattern, path=var_path,
                                                      is_negative_test=False)


def cat_diag_version():
    Log_Debug("Check diag version:\n")
    dLibObj = getDiagLibObj()

    var_toolName ='./' + cel_version_test["bin_tool"]
    var_option = ' -S'
    var_keywords_pattern = cel_diag_version
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
                                                      keywords_pattern=var_keywords_pattern,
                                                      pass_pattern=var_pass_pattern, path=var_path,
                                                      is_negative_test=False)


def check_openbmc_version():
    Log_Debug("Check openbmc version:\n")
    dLibObj = getDiagLibObj()

    var_toolName = "ls"
    var_option = 'BMC_Diag/'
    var_pass_pattern = cel_diag_list
    var_path = "/mnt/data1"

    return dLibObj.verify_bmc_diag_installed(var_toolName, var_option, var_pass_pattern, var_path)

def clean_diag_rpm():
    Log_Debug("Entering procedure clean_diag_rpm.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'rpm -qa'
    var_option = '| grep Diag|xargs -I {} rpm -e {}'
    var_pass_pattern = ''
    var_path = ''

    return dLibObj.clean_diag_rpm_package(var_toolName, var_option, var_pass_pattern, var_path)

def delete_the_diag_on_centos():
    Log_Debug("Entering procedure delete_the_diag_on_centos.\n")
    dLibObj = getDiagLibObj()

    Diag_package = os.popen('rpm -qa | grep Diag').read()
    for package in Diag_package:
        os.system('rpm -e' + package)
    var_toolName = "rm"
    var_option = " -rf {}".format(DIAG_TOOL_PATH_CPU)
    var_keywords_pattern = ""
    var_pass_pattern = ""
    var_path = ""
    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option,
        keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path, is_negative_test=True)

def delete_the_diag_on_openbmc():
    Log_Debug("Entering procedure delete_the_diag_on_openbmc.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'rm'
    var_option = '-rf ' + BMC_DIAG_PATH
    var_keywords_pattern = ''
    var_pass_pattern = ""
    var_path = '/bin'

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path, is_negative_test=True)


def clear_diag_files():
    Log_Debug("Entering procedure clear_diag_files.\n")
    dLibObj = getDiagLibObj()

    extract_folder = diag_upgrade_file.rstrip(".zip")
    var_toolName = 'cd '
    var_option = ' ' + diag_img_path + ' && rm -rf {} {}'.format(diag_upgrade_file, extract_folder)
    var_keywords_pattern = ''
    var_pass_pattern = ""
    var_path = ''

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern,
                                                        pass_pattern=var_pass_pattern, path=var_path, is_negative_test=True)


def copy_diag_image_files():
    Log_Debug("Entering procedure copy_diag_image_files.\n")
    dLibObj = getDiagLibObj()

    var_username=scp_username
    var_password=scp_password
    var_server_ip=scp_ip
    var_filelist=diag_package_copy_list
    var_filepath=scp_diag_filepath
    var_destination_path=diag_img_path
    var_mode=centos_mode

    return CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode)


def extract_the_diag_installer_file():
    Log_Debug("Entering procedure extract_the_diag_installer_file.\n")
    dLibObj = getDiagLibObj()

    zip_file_path = os.path.join(diag_img_path, diag_upgrade_file)
    extract_path = os.path.join( diag_img_path, diag_upgrade_file.rstrip(".zip"))
    extract_inner_path = os.path.join(extract_path, "Wedge400_400C_Diag_" + diag_upgrade_version)
    var_toolName = 'unzip'
    var_option = os.path.join(diag_img_path, diag_upgrade_file) + " -d " + diag_img_path + \
        " && cd " + extract_path + \
        " && md5sum -c Wedge400_400C_Diag_" + diag_upgrade_version + ".zip.md5" + \
        " && unzip Wedge400_400C_Diag_" + diag_upgrade_version + ".zip" + \
        " && cd " + extract_inner_path
    Log_Info("var option:{}".format(var_option))
    var_keywords_pattern = extract_daig_installer_pattern
    var_pass_pattern = ''
    var_path = '/usr/bin'

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern,
                                                        pass_pattern=var_pass_pattern, path=var_path)


def install_diag_tools():
    Log_Debug("Entering procedure install_diag_tools.\n")
    dLibObj = getDiagLibObj()

    # extract_inner_path = os.path.join(diag_img_path, diag_upgrade_file.rstrip(".rpm"), "Wedge400_400C_Diag_" + diag_upgrade_version)
    var_toolName = 'rpm'
    var_option = " -ivh " + diag_upgrade_file + " --nodeps --force"
    var_keywords_pattern = diag_install_pattern
    var_pass_pattern = ''
    var_path = "/home"

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern,
                                                        pass_pattern=var_pass_pattern, path=var_path)

def init_diag_test():
    Log_Debug("Entering procedure init_diag_test.\n")
    dLibObj = getDiagLibObj()
    dLibObj.init_diag_test()

def compare_centos_version_diag_version_and_kernel_version():
    Log_Debug("Entering procedure compare_centos_version_diag_version_and_kernel_version.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.compare_centos_version_diag_version_and_kernel_version()


def run_eeupdate64e_nic2_adapterinfo():
    Log_Debug("Entering procedure run_eeupdate64e_nic2_adapterinfo.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './eeupdate64e'
    var_option = "/NIC=2 /ADAPTERINFO"
    var_keywords_pattern = ""
    var_pass_pattern = ''
    var_path = '/usr/local/cls_diag/utility'

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def cloudripper_run_eeupdate64e_nic2_adapterinfo():
    Log_Debug("Entering procedure cloudripper_run_eeupdate64e_nic2_adapterinfo.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './eeupdate64e'
    var_option = "/NIC=2 /ADAPTERINFO"
    var_keywords_pattern = ""
    var_pass_pattern = ''
    var_path = '/usr/local/cls_diag/utility'

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def minipack2_run_eeupdate64e_nic2_adapterinfo():
    Log_Debug("Entering procedure run_eeupdate64e_nic2_adapterinfo.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './eeupdate64e'
    var_option = "/NIC=2 /ADAPTERINFO"
    var_keywords_pattern = ""
    var_pass_pattern = ''
    var_path = '/usr/local/cls_diag/utility'

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern,
                                                        pass_pattern=var_pass_pattern, path=var_path)

def compare_i210_firmware_version():
    Log_Debug("Entering procedure compare_i210_firmware_version.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.compare_i210_firmware_version()


def fw_util_all_version():
    Log_Debug("Entering procedure fw_util_all_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "fw-util all --version"
    var_option = ' '
    var_keywords_pattern = fw_util_version
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)


def verify_cel_version_test_S():
    Log_Debug("Entering procedure verify_cel_version_test_S.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_version_test["bin_tool"]
    var_option = "-S"
    var_keywords_pattern = version_test_S_or_show_pattern
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern,
                                                        pass_pattern=var_pass_pattern, path=var_path)

def verify_cpld_test_h():
    Log_Debug("Entering procedure verify_cpld_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cel-cpld-test'
    var_option = '-h'
    var_keywords_pattern = cpld_option_h
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def verify_cpld_test_v():
    Log_Debug("Entering procedure verify_cpld_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cel-cpld-test'
    var_option = '-v'
    var_keywords_pattern = cpld_option_v
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def verify_cpld_test_k():
    Log_Debug("Entering procedure verify_cpld_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cel-cpld-test'
    var_option = '-k'
    var_keywords_pattern = ''
    var_pass_pattern = ''

    return dLibObj.verify_cpld_check_ok_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def verify_cpld_test_a():
    Log_Debug("Entering procedure verify_cpld_test_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cel-cpld-test'
    var_option = '-a'
    var_keywords_pattern = cpld_option_a
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def verify_cpld_help_dict_option_h():
    Log_Debug("Entering procedure verify_cpld_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_cpld_help_array
    var_toolName = cel_cpld_help_array["bin_tool"]
    var_option = "-h"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)


def verify_cpld_help_dict_option_help():
    Log_Debug("Entering procedure verify_cpld_help_dict_option_help.\n")
    dLibObj = getDiagLibObj()

    var_inputArray = cel_cpld_help_array
    var_toolName = cel_cpld_help_array["bin_tool"]
    var_option = "--help"

    return dLibObj.verify_option_diag_tool_simple_dict(var_inputArray, var_toolName, var_option)

def verify_cpld_help_dict_option_a():
    Log_Debug("Entering procedure verify_cpld_help_dict_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_cpld_help_array["bin_tool"]
    var_option = "-a"
    var_keywords = cpld_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)

def verify_cpld_help_dict_option_all():
    Log_Debug("Entering procedure verify_cpld_help_dict_option_all.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_cpld_help_array["bin_tool"]
    var_option = "--all"
    var_keywords = cpld_test_keyword
    var_pattern = 'none'
    var_data='none'
    var_port='none'
    var_color='none'

    return dLibObj.verify_diag_tool_simple_dict(var_toolName, var_option, var_keywords, var_pattern, var_data, var_port, var_color)

def verify_cel_version_test_show():
    Log_Debug("Entering procedure verify_cel_version_test_show.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_version_test["bin_tool"]
    var_option = "--show"
    var_keywords_pattern = version_test_S_or_show_pattern
    var_pass_pattern = ''
    var_path = '/usr/local/cls_diag/CPU_Diag/bin'

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern,
                                                        pass_pattern=var_pass_pattern, path=var_path)

def verify_pem_tool_option_h():
    Log_Debug("Entering procedure verify_pem_tool_option_h.\n")
    dLibObj = getDiagLibObj()
    var_toolName = cel_pem_tools["bin_tool"]
    var_option = "-h && sysctl -w kernel.printk=3"  # Disable the I2C notice message during test
    var_keywords_pattern = verify_pem_tool_option_h_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH
    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_pem_tool_option_i():
    Log_Debug("Entering procedure verify_pem_tool_option_i.\n")
    dLibObj = getDiagLibObj()
    if not dLibObj.is_using_pem():
        return
    var_toolName = cel_pem_tools["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = verify_pem_tool_option_i_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_pem_tool_option_s():
    Log_Debug("Entering procedure verify_pem_tool_option_s.\n")
    dLibObj = getDiagLibObj()
    if not dLibObj.is_using_pem():
        return
    var_toolName = cel_pem_tools["bin_tool"]
    var_option = "-s"
    var_keywords_pattern = verify_pem_tool_option_s_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH
    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_version_option_h():
    Log_Debug("Entering procedure verify_cel_version_test_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_version_test["bin_tool"]
    var_option = "-h"
    var_keywords_pattern = cel_version_test_h_or_help_pattern
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def verify_cel_version_option_help():
    Log_Debug("Entering procedure verify_cel_version_test_option_help.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_version_test["bin_tool"]
    var_option = "--help"
    var_keywords_pattern = cel_version_test_h_or_help_pattern
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def verify_cel_version_test_option_show():
    Log_Debug("Entering procedure verify_cel_version_test_option_show.\n")
    dLibObj = getDiagLibObj()

    var_toolName = "./" + cel_version_test["bin_tool"]
    var_option = "--show"
    var_keywords_pattern = cel_version_test_S_or_show_pattern
    var_pass_pattern = ''
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(toolName=var_toolName, option=var_option, keywords_pattern=var_keywords_pattern, pass_pattern=var_pass_pattern, path=var_path)

def verify_pem_tool_option_a():
    Log_Debug("Entering procedure verify_pem_tool_option_a.\n")
    dLibObj = getDiagLibObj()
    if not dLibObj.is_using_pem():
        return
    var_toolName = cel_pem_tools["bin_tool"]
    var_option = "-a && sysctl -w kernel.printk=7"  # Set the debug message level to default
    var_keywords_pattern = verify_pem_tool_option_a_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH
    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_pem_tool_option_main_information():
    Log_Debug("Entering procedure verify_pem_tool_option_main_information.\n")
    dLibObj = getDiagLibObj()
    if not dLibObj.is_using_pem():
        return
    return dLibObj.switch_and_verify_pem_info()

def run_sdk_init(path, sdk_script, cmd):
    Log_Debug("Entering procedure run_sdk_init.\n")
    dLibObj = getDiagLibObj()

    return dLibObj.run_sdk_init(cmd="cd " + path + " && python3 " + sdk_script + " " + cmd)

def run_cr_sdk_init(path, sdk_script, cmd):
    Log_Debug("Entering procedure run_cr_sdk_init.\n")
    dLibObj = getDiagLibObj()

    log_file = 'temp.log'
    cmd = "cd " + path + " && python3 " + sdk_script + " " + cmd + ' ' + '> ' + log_file

    return dLibObj.run_sdk_init(cmd=cmd, log_file=log_file)

def fpga_test():
    Log_Debug("Entering procedure fpga_test.\n")
    dLibObj = getDiagLibObj()

    var_cmd_list = cel_cmd_list
    pass_pattern = fpga_pass_pattern

    return dLibObj.test_fpga_function(var_cmd_list, pass_pattern)

def verify_eth_test_option_h():
    Log_Debug("Entering procedure verify_eth_test_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_eth_test_array['bin_tool']
    var_option = '-h'
    var_pattern = cel_eth_test_h_pattern
    var_pass_pattern = ''
    var_path = ''

    return dLibObj.verity_eth_test_dict_option(var_toolName, var_option, var_pattern, var_pass_pattern, var_path)

def verify_eth_test_option_a():
    Log_Debug("Entering procedure verify_eth_test_option_a.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_eth_test_array['bin_tool']
    var_option = '-a'
    var_pattern = cel_eth_test_a_pattern
    var_pass_pattern = ''
    var_path = ''

    return dLibObj.verity_eth_test_dict_option(var_toolName, var_option, var_pattern, var_pass_pattern, var_path)

def update_pcie_switch_firmware():
    Log_Debug("Entering procedure update_pcie_switch_firmware.\n")
    dLibObj = getDiagLibObj()

    var_cmd_str = pcie_update_cmd_str
    var_image = pcie_switch_image
    var_pass_pattern = pcie_pass_pattern_list

    return dLibObj.bmc_switch_firmware_update(var_cmd_str, var_image, var_pass_pattern)

def verify_bmc_command(bmc_cmd=None, patterns=None, is_negtive_test=False, path=BMC_DIAG_TOOL_PATH):
    Log_Debug("Entering procedure verify_bmc_command.\n")
    dLibObj = getDiagLibObj()
    bmc_cmd = globals()[bmc_cmd]
    patterns = globals()[patterns]

    return dLibObj.execute_check_dict(cmd=bmc_cmd, mode=openbmc_mode, patterns_dict=patterns, path=path,
            timeout=1600, line_mode=False, is_negative_test=is_negtive_test)

def verify_centos_command(centos_cmd=None, patterns=None, is_negtive_test=False, path=DIAG_TOOL_PATH):
    Log_Debug("Entering procedure verify_centos_command.\n")
    dLibObj = getDiagLibObj()
    centos_cmd = globals()[centos_cmd]
    patterns = globals()[patterns]

    return dLibObj.execute_check_dict(cmd=centos_cmd, mode=centos_mode, patterns_dict=patterns, path=path,
                                      timeout=600, line_mode=False, is_negative_test=is_negtive_test)

def update_oob_switch_firmware():
    Log_Debug("Entering procedure update_oob_switch_firmware.\n")
    dLibObj = getDiagLibObj()

    var_cmd_str = oob_update_cmd_str
    var_image = oob_switch_image
    var_pass_pattern = oob_pass_pattern_list
    var_path = oob_switch_image_path

    return  dLibObj.bmc_switch_firmware_update(var_cmd_str, var_image, var_pass_pattern, var_path)

def dump_flash_as_file():
    Log_Debug("Entering procedure dump_flash_as_file.\n")
    dLibObj = getDiagLibObj()

    var_cmd_str = oob_image_read_cmd
    var_image_read_path = image_read_path
    var_pass_pattern = oob_read_image_pass_pattern
    var_path = oob_switch_image_path

    return dLibObj.bmc_switch_firmware_update(var_cmd_str, var_image_read_path, var_pass_pattern, var_path)

def verify_info_contains(info_full_cmd, part_cmd, skip_lines=1, path=BMC_DIAG_TOOL_PATH, exclude=psu_eeprom_exclude_item, remove_pattern=psu_eeprom_remove_pattern):
    Log_Debug("Entering procedure verify_info_contains.\n")
    dLibObj = getDiagLibObj()
    info_full_cmd = globals()[info_full_cmd]
    part_cmd = globals()[part_cmd]

    return dLibObj.check_info_contains(info_full_cmd, part_cmd, skip_lines=skip_lines, path=path, exclude=exclude, remove_pattern=remove_pattern)

def check_default_of_usb_interface(mode, interface, ip):
    Log_Debug("Entering procedure check_default_of_usb_interface.\n")
    dLibObj = getDiagLibObj()

    toolName = "ifconfig "
    option = interface
    keywords_pattern = [ip,]
    pass_pattern = ""
    mode = mode
    path = "/sbin"

    return dLibObj.verify_tool_simple_dict(toolName=toolName, option=option, keywords_pattern=keywords_pattern,
                pass_pattern=pass_pattern, mode=mode, path=path)

def ping_to_check(mode, interface, ip):
    Log_Debug("Entering procedure ping_to_check.\n")
    dLibObj = getDiagLibObj()

    toolName = "ping"
    option = "-6 -c 6 " + ip + "%" + interface

    if mode == "openbmc":
        keywords_pattern = openbmc_ping_to_come_pattern
    elif mode == "centos":
        keywords_pattern = come_ping_to_openbmc_pattern

    pass_pattern = ""
    mode = mode
    path = "/bin"

    return dLibObj.verify_tool_simple_dict(toolName=toolName, option=option, keywords_pattern=keywords_pattern,
                pass_pattern=pass_pattern, mode=mode, path=path)


def update_fcm_b_cpld_via_i2c():
    Log_Debug("Entering procedure update_fcm_b_cpld_via_i2c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_fcm_b_i2c_array['bin_tool']
    var_option1 = cel_bmc_cpld_fcm_b_i2c_array['option1']
    var_dev = cel_bmc_cpld_fcm_b_i2c_array['dev']
    var_option2 = cel_bmc_cpld_fcm_b_i2c_array['option2']
    var_image = cel_bmc_cpld_fcm_b_i2c_array['newimage']
    var_pass_pattern = cel_bmc_cpld_i2c_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1 , var_dev, var_option2, var_image, var_pass_pattern, var_image_path)

def update_fcm_t_cpld_via_i2c():
    Log_Debug("Entering procedure update_fcm_t_cpld_via_i2c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_fcm_b_i2c_array['bin_tool']
    var_option1 = cel_bmc_cpld_fcm_b_i2c_array['option1']
    var_dev = cel_bmc_cpld_fcm_b_i2c_array['dev1']
    var_option2 = cel_bmc_cpld_fcm_b_i2c_array['option2']
    var_image = cel_bmc_cpld_fcm_b_i2c_array['newimage']
    var_pass_pattern = cel_bmc_cpld_t_i2c_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1 , var_dev, var_option2, var_image, var_pass_pattern, var_image_path)


def downgrade_fcm_b_cpld_via_i2c():
    Log_Debug("Entering procedure downgrade_fcm_b_cpld_via_i2c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_fcm_b_i2c_array['bin_tool']
    var_option1 = cel_bmc_cpld_fcm_b_i2c_array['option1']
    var_dev = cel_bmc_cpld_fcm_b_i2c_array['dev']
    var_option2 = cel_bmc_cpld_fcm_b_i2c_array['option2']
    var_image = cel_bmc_cpld_fcm_b_i2c_array['oldimage']
    var_pass_pattern = cel_bmc_cpld_i2c_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1 , var_dev, var_option2, var_image, var_pass_pattern, var_image_path)

def downgrade_fcm_t_cpld_via_i2c():
    Log_Debug("Entering procedure downgrade_fcm_t_cpld_via_i2c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_fcm_b_i2c_array['bin_tool']
    var_option1 = cel_bmc_cpld_fcm_b_i2c_array['option1']
    var_dev = cel_bmc_cpld_fcm_b_i2c_array['dev1']
    var_option2 = cel_bmc_cpld_fcm_b_i2c_array['option2']
    var_image = cel_bmc_cpld_fcm_b_i2c_array['oldimage']
    var_pass_pattern = cel_bmc_cpld_t_i2c_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1 , var_dev, var_option2, var_image, var_pass_pattern, var_image_path)


def check_fcm_oldversion_driver_version():
    Log_Debug("Entering procedure check_fcm_oldversion_driver_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_fcm_b_i2c_array['check_tool']
    var_option = cel_bmc_cpld_fcm_b_i2c_array['check_option']
    var_pass_pattern = cel_fcm_oldversion_pass_pattern
    var_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pass_pattern, var_pattern)

def check_fcm_newversion_driver_version():
    Log_Debug("Entering procedure check_fcm_newversion_driver_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_fcm_b_i2c_array['check_tool']
    var_option = cel_bmc_cpld_fcm_b_i2c_array['check_option1']
    var_pass_pattern = cel_fcm_newversion_pass_pattern
    var_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pass_pattern, var_pattern)

def check_cpld_test_h():
    Log_Debug("Entering procedure check_cpld_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_fcm_b_i2c_array['bin_tool']
    var_option = cel_bmc_cpld_fcm_b_i2c_array['option3']
    var_keywords_pattern = cpld_option_h_array
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def copy_fcm_hw_files():
    Log_Debug("Entering procedure copy_fcm_hw_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    var_filelist = fcm_hw_package_copy_list
    var_filepath = scp_fcm_filepath
    var_destination_path = fcm_img_path
    var_mode = openbmc_mode
    # make sure ipv6 available
    get_dhcp_ipv6_addresses('eth')
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output

def downgrade_scm_cpld_i2c():
    Log_Debug("Entering procedure downgrade_scm_cpld_i2c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_scm_i2c_array['bin_tool']
    var_option1 = cel_bmc_cpld_scm_i2c_array['option1']
    var_dev = cel_bmc_cpld_scm_i2c_array['dev']
    var_option2 = cel_bmc_cpld_scm_i2c_array['option2']
    var_image = cel_bmc_cpld_scm_i2c_array['oldimage']
    var_pass_pattern = cel_bmc_cpld_scm_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1 , var_dev, var_option2, var_image, var_pass_pattern, var_image_path)

def update_scm_cpld_i2c():
    Log_Debug("Entering procedure update_scm_cpld_i2c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_scm_i2c_array['bin_tool']
    var_option1 = cel_bmc_cpld_scm_i2c_array['option1']
    var_dev = cel_bmc_cpld_scm_i2c_array['dev']
    var_option2 = cel_bmc_cpld_scm_i2c_array['option2']
    var_image = cel_bmc_cpld_scm_i2c_array['newimage']
    var_pass_pattern = cel_bmc_cpld_scm_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1 , var_dev, var_option2, var_image, var_pass_pattern, var_image_path)


def check_scm_hw_new_driver_version():
    Log_Debug("Entering procedure check_scm_hw_new_driver_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_scm_i2c_array['check_tool']
    var_option = cel_bmc_cpld_scm_i2c_array['check_option1']
    var_pass_pattern = cel_scm_newversion_pass_pattern
    var_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pass_pattern, var_pattern)

def check_scm_hw_old_driver_version():
    Log_Debug("Entering procedure check_scm_hw_old_driver_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_scm_i2c_array['check_tool']
    var_option = cel_bmc_cpld_scm_i2c_array['check_option']
    var_pass_pattern = cel_scm_oldversion_pass_pattern
    var_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pass_pattern, var_pattern)

def copy_scm_hw_files():
    Log_Debug("Entering procedure copy_scm_hw_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    var_filelist = scm_hw_package_copy_list
    var_filepath = scp_scm_filepath
    var_destination_path = scm_img_path
    var_mode = openbmc_mode
    # make sure ipv6 available
    get_dhcp_ipv6_addresses('eth')
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output

def check_power_cycle_stress_option_h():
    Log_Debug("Entering procedure check_power_cycle_stress_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'power_cycle_stress.sh'
    var_option = '-h'
    var_keywords_pattern = power_cycle_stress_option_h
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, path=BMC_STRESS_POWER_CYCLE_PATH)

def check_power_cycle_stress_option_n(loop):
    Log_Debug("Entering procedure check_power_cycle_stress_option_n.\n")
    dLibObj = getDiagLibObj()
    return dLibObj.check_power_cycle_stress_option_n(loop)

def check_emmc_stress_option_h():
    Log_Debug("Entering procedure check_emmc_stress_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'emmc_stress_test.sh'
    var_option = '-h'
    var_keywords_pattern = emmc_stress_option_h
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, path=BMC_STRESS_EMMC_PATH)

def check_emmc_stress_option_n(loop):
    Log_Debug("Entering procedure check_emmc_stress_option_n.\n")
    dLibObj = getDiagLibObj()
    return dLibObj.check_emmc_stress_option_n(loop)

def update_fcm_b_cpld_via_jtag():
    Log_Debug("Entering procedure update_fcm_b_cpld_via_jtag.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fcm_cpld_jtag_array['bin_tool']
    var_option1 = cel_bmc_fcm_cpld_jtag_array['option1']
    var_dev = cel_bmc_fcm_cpld_jtag_array['dev']
    var_option2 = cel_bmc_fcm_cpld_jtag_array['option2']
    var_option3 = cel_bmc_fcm_cpld_jtag_array['option4']
    var_image = cel_bmc_fcm_cpld_jtag_array['newimage']
    var_pass_pattern = cel_bmc_cpld_fcm_b_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1 , var_dev, var_option2, var_image, var_pass_pattern, var_image_path, var_option3)

def update_fcm_t_cpld_via_jtag():
    Log_Debug("Entering procedure update_fcm_t_cpld_via_jtag.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fcm_cpld_jtag_array['bin_tool']
    var_option1 = cel_bmc_fcm_cpld_jtag_array['option1']
    var_dev = cel_bmc_fcm_cpld_jtag_array['dev1']
    var_option2 = cel_bmc_fcm_cpld_jtag_array['option2']
    var_option3 = cel_bmc_fcm_cpld_jtag_array['option4']
    var_image = cel_bmc_fcm_cpld_jtag_array['newimage']
    var_pass_pattern = cel_bmc_cpld_fcm_b_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1 , var_dev, var_option2, var_image, var_pass_pattern, var_image_path, var_option3)

def downgrade_fcm_b_cpld_via_jtag():
    Log_Debug("Entering procedure downgrade_fcm_b_cpld_via_jtag.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fcm_cpld_jtag_array['bin_tool']
    var_option1 = cel_bmc_fcm_cpld_jtag_array['option1']
    var_dev = cel_bmc_fcm_cpld_jtag_array['dev']
    var_option2 = cel_bmc_fcm_cpld_jtag_array['option2']
    var_option3 = cel_bmc_fcm_cpld_jtag_array['option4']
    var_image = cel_bmc_fcm_cpld_jtag_array['oldimage']
    var_pass_pattern = cel_bmc_cpld_fcm_b_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1 , var_dev, var_option2, var_image, var_pass_pattern, var_image_path, var_option3)

def downgrade_fcm_t_cpld_via_jtag():
    Log_Debug("Entering procedure downgrade_fcm_t_cpld_via_jtag.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fcm_cpld_jtag_array['bin_tool']
    var_option1 = cel_bmc_fcm_cpld_jtag_array['option1']
    var_dev = cel_bmc_fcm_cpld_jtag_array['dev1']
    var_option2 = cel_bmc_fcm_cpld_jtag_array['option2']
    var_option3 = cel_bmc_fcm_cpld_jtag_array['option4']
    var_image = cel_bmc_fcm_cpld_jtag_array['oldimage']
    var_pass_pattern = cel_bmc_cpld_fcm_b_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1 , var_dev, var_option2, var_image, var_pass_pattern, var_image_path, var_option3)

def check_cpld_update_test_h():
    Log_Debug("Entering procedure check_cpld_update_test_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_fcm_cpld_jtag_array['bin_tool']
    var_option = cel_bmc_fcm_cpld_jtag_array['option3']
    var_keywords_pattern = cel_cpld_update_option_h_array
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern)

def downgrade_scm_cpld_jtag():
    Log_Debug("Entering procedure downgrade_scm_cpld_jtag.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_scm_jtag_array['bin_tool']
    var_option1 = cel_bmc_cpld_scm_jtag_array['option1']
    var_dev = cel_bmc_cpld_scm_jtag_array['dev']
    var_option2 = cel_bmc_cpld_scm_jtag_array['option2']
    var_option3 = cel_bmc_cpld_scm_jtag_array['option4']
    var_image = cel_bmc_cpld_scm_jtag_array['oldimage']
    var_pass_pattern = cel_bmc_cpld_scm_jtag_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1, var_dev, var_option2, var_image, var_pass_pattern, var_image_path, var_option3)

def upgrade_scm_cpld_jtag():
    Log_Debug("Entering procedure upgrade_scm_cpld_jtag.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_scm_jtag_array['bin_tool']
    var_option1 = cel_bmc_cpld_scm_jtag_array['option1']
    var_dev = cel_bmc_cpld_scm_jtag_array['dev']
    var_option2 = cel_bmc_cpld_scm_jtag_array['option2']
    var_option3 = cel_bmc_cpld_scm_jtag_array['option4']
    var_image = cel_bmc_cpld_scm_jtag_array['newimage']
    var_pass_pattern = cel_bmc_cpld_scm_jtag_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1, var_dev, var_option2, var_image, var_pass_pattern, var_image_path, var_option3)

def downgrade_pdb_l_cpld_update_via_i2c():
    Log_Debug("Entering procedure downgrade_pdb_l_cpld_update_via_i2c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_pdb_array['bin_tool']
    var_option1 = cel_bmc_cpld_pdb_array['option1']
    var_dev = cel_bmc_cpld_pdb_array['dev']
    var_option2 = cel_bmc_cpld_pdb_array['option2']
    var_image = cel_bmc_cpld_pdb_array['oldimage']
    var_pass_pattern = cel_bmc_cpld_pwr_l_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1, var_dev, var_option2, var_image, var_pass_pattern, var_image_path)

def upgrade_pdb_l_cpld_update_via_i2c():
    Log_Debug("Entering procedure upgrade_pdb_l_cpld_update_via_i2c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_pdb_array['bin_tool']
    var_option1 = cel_bmc_cpld_pdb_array['option1']
    var_dev = cel_bmc_cpld_pdb_array['dev']
    var_option2 = cel_bmc_cpld_pdb_array['option2']
    var_image = cel_bmc_cpld_pdb_array['newimage']
    var_pass_pattern = cel_bmc_cpld_pwr_l_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1, var_dev, var_option2, var_image, var_pass_pattern, var_image_path)

def downgrade_pdb_r_cpld_update_via_i2c():
    Log_Debug("Entering procedure downgrade_pdb_r_cpld_update_via_i2c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_pdb_array['bin_tool']
    var_option1 = cel_bmc_cpld_pdb_array['option1']
    var_dev = cel_bmc_cpld_pdb_array['dev1']
    var_option2 = cel_bmc_cpld_pdb_array['option2']
    var_image = cel_bmc_cpld_pdb_array['oldimage']
    var_pass_pattern = cel_bmc_cpld_pwr_r_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1, var_dev, var_option2, var_image, var_pass_pattern, var_image_path)

def upgrade_pdb_r_cpld_update_via_i2c():
    Log_Debug("Entering procedure upgrade_pdb_r_cpld_update_via_i2c.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_pdb_array['bin_tool']
    var_option1 = cel_bmc_cpld_pdb_array['option1']
    var_dev = cel_bmc_cpld_pdb_array['dev1']
    var_option2 = cel_bmc_cpld_pdb_array['option2']
    var_image = cel_bmc_cpld_pdb_array['newimage']
    var_pass_pattern = cel_bmc_cpld_pwr_r_pass_pattern
    var_image_path = '/mnt/data1/'

    return dLibObj.update_cpld_fw(var_toolName, var_option1, var_dev, var_option2, var_image, var_pass_pattern, var_image_path)

def check_pdb_hw_old_driver_version():
    Log_Debug("Entering procedure check_pdb_hw_old_driver_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_pdb_array['check_tool']
    var_option = cel_bmc_cpld_pdb_array['check_option']
    var_pass_pattern = cel_pwr_hw_oldversion_pass_pattern
    var_pass = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pass_pattern, var_pass)

def check_pdb_hw_new_driver_version():
    Log_Debug("Entering procedure check_pdb_hw_new_driver_version.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_pdb_array['check_tool']
    var_option = cel_bmc_cpld_pdb_array['check_option1']
    var_pass_pattern = cel_pwr_hw_newversion_pass_pattern
    var_pass = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_pass_pattern, var_pass)

def copy_power_hw_cpld_files():
    Log_Debug("Entering procedure copy_power_hw_cpld_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    var_filelist = pwr_hw_package_copy_list
    var_filepath = scp_pwr_filepath
    var_destination_path = pwr_img_path
    var_mode = openbmc_mode
    # make sure ipv6 available
    get_dhcp_ipv6_addresses('eth')
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output


def fw_util_scm_version_bios(bios_version=bios_upgrade_ver):
    Log_Debug("Entering procedure fw_util_scm_version_bios.\n")
    dLibObj = getDiagLibObj()

    var_toolName = fw_util_tool
    var_args = ' scm --version bios'
    var_keywords_pattern = [bios_version_pattern + bios_version]
    var_pass_pattern = ""
    var_path = "/usr/bin"

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_args, var_keywords_pattern, var_pass_pattern, var_path)


def reboot_and_check_bios_version(bios_version=bios_upgrade_ver):
    Log_Debug("Entering procedure reboot_and_check_bios_version.\n")
    dLibObj = getDiagLibObj()

    dLibObj.reboot_and_check_bios_version(bios_version)

def check_i2c_stress_option_h():
    Log_Debug("Entering procedure check_i2c_stress_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'i2c_stress.sh'
    var_option = '-h'
    var_keywords_pattern = i2c_stress_option_h
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, path=BMC_STRESS_I2C_PATH)

def check_i2c_stress_option_n(loop):
    Log_Debug("Entering procedure check_i2c_stress_option_n.\n")
    dLibObj = getDiagLibObj()
    return dLibObj.check_i2c_stress_option_n(loop)

def verify_cel_fan_test_g_p_70():
    Log_Debug("Entering procedure verify_cel_fan_test_g_p_70.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-g"
    var_keywords_pattern = cel_fan_test_g_p_70_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_cel_fan_test_p_70():
    Log_Debug("Entering procedure verify_cel_fan_test_p_70.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_fan_test["bin_tool"]
    var_option = "-p 70"
    var_keywords_pattern = cal_fan_test_p_70_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_mdio_tool_fpga_option_h():
    Log_Debug("Entering procedure verify_mdio_tool_fpga_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_mdio_test_array['bin_tool']
    var_option = cel_mdio_test_array['option_h']
    var_pass_pattern = cel_mdio_option_h_pass_pattern
    var_path = FPGA_TOOL_PATH
    cmd = './' + var_toolName + ' ' + var_option

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

@logThis
def verify_mdio_tool_fpga_option_0x9c():
    dLibObj = getDiagLibObj()

    for param in range(1, 9):
        var_toolName = cel_mdio_test_array['bin_tool']
        var_option = cel_mdio_test_array['store_2'] + ' ' + cel_mdio_test_array['option_r'] + ' ' + \
                     cel_mdio_test_array['option_pim'] + str(param) +  ' ' + cel_mdio_test_array['ele1']
        var_pass_pattern = cel_mdio_option_0x9c_pass_pattern
        var_path = FPGA_TOOL_PATH
        cmd = './' + var_toolName + ' ' + var_option

        dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

@logThis
def verify_mdio_tool_fpga_option_0x5201d000():
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    for param in range(1, 9):
        if 'minipack2_dc' in devicename.lower():
            if (param == 3) or (param == 4) or (param == 5) or (param == 6):
                continue
        var_toolName = cel_mdio_test_array['bin_tool']
        var_option = cel_mdio_test_array['store_1'] + ' ' + cel_mdio_test_array['option_r'] + ' ' + \
                     cel_mdio_test_array['option_pim'] + str(param) +  ' ' + cel_mdio_test_array['option_type'] + ' ' + cel_mdio_test_array['option_phy'] + ' ' + cel_mdio_test_array['ele4']
        var_pass_pattern = cel_mdio_option_0x5201d000_pass_pattern
        var_path = FPGA_TOOL_PATH
        cmd = './' + var_toolName + ' ' + var_option

        dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)


@logThis
def verify_mdio_tool_fpga_option_0x5201d001():
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    for param in range(1, 9):
        if 'minipack2_dc' in devicename.lower():
            if (param == 3) or (param == 4) or (param == 5) or (param == 6):
                continue
        var_toolName = cel_mdio_test_array['bin_tool']
        var_option = cel_mdio_test_array['store_1'] + ' ' + cel_mdio_test_array['option_r'] + ' ' + \
                     cel_mdio_test_array['option_pim'] + str(param) +  ' ' + cel_mdio_test_array['option_type'] + ' ' + cel_mdio_test_array['option_phy'] + ' ' + cel_mdio_test_array['ele5']
        var_pass_pattern = cel_mdio_option_0x5201d001_pass_pattern
        var_path = FPGA_TOOL_PATH
        cmd = './' + var_toolName + ' ' + var_option

        dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

@logThis
def verify_mdio_tool_fpga_option_0xb2e9():
    dLibObj = getDiagLibObj()

    for param in range(1, 9):
        var_toolName = cel_mdio_test_array['bin_tool']
        var_option = cel_mdio_test_array['store_1'] + ' ' + cel_mdio_test_array['option_r'] + ' ' + \
                     cel_mdio_test_array['option_pim'] + str(param) + ' ' + cel_mdio_test_array['option_phy'] + ' ' + cel_mdio_test_array['ele2']
        var_pass_pattern = cel_mdio_option_0xb2e9_pass_pattern
        var_path = FPGA_TOOL_PATH
        cmd = './' + var_toolName + ' ' + var_option

        dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

@logThis
def verify_mdio_tool_fpga_option_0x210():
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    for param in range(1, 9):
        if 'minipack2_dc' in devicename.lower():
            if (param == 3) or (param == 4) or (param == 5) or (param == 6):
                continue
        var_toolName = cel_mdio_test_array['bin_tool']
        var_option = cel_mdio_test_array['store_2'] + ' ' + cel_mdio_test_array['option_r'] + ' ' + \
                     cel_mdio_test_array['option_pim'] + str(param) +' ' + cel_mdio_test_array['ele3']
        var_pass_pattern = cel_mdio_option_0x210_pass_pattern
        var_path = FPGA_TOOL_PATH
        cmd = './' + var_toolName + ' ' + var_option

        dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

@logThis
def verify_mdio_tool_fpga_option_0x214():
    dLibObj = getDiagLibObj()

    for param in range(1, 9):
        var_toolName = cel_mdio_interrupt_test_array['bin_tool']
        var_option = cel_mdio_interrupt_test_array['store_2'] + ' ' + cel_mdio_interrupt_test_array['option_w'] + ' ' + \
                     cel_mdio_interrupt_test_array['option_pim'] + str(param) + ' ' + cel_mdio_interrupt_test_array['ele1'] + ' 0'
        var_pass_pattern = cel_mdio_option_0x214_pass_pattern
        var_path = FPGA_TOOL_PATH
        cmd = './' + var_toolName + ' ' + var_option

        dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

@logThis
def verify_mdio_tool_fpga_option_0x5200cb20():
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    for param in range(1, 9):
        if 'minipack2_dc' in devicename.lower():
            if (param == 3) or (param == 4) or (param == 5) or (param == 6):
                continue
        var_toolName = cel_mdio_interrupt_test_array['bin_tool']
        var_option = cel_mdio_interrupt_test_array['store_1'] + ' ' + cel_mdio_interrupt_test_array['option_r'] + ' ' + \
                     cel_mdio_interrupt_test_array['option_pim'] + str(param) + ' ' + cel_mdio_interrupt_test_array['option_type'] + \
                    ' ' + cel_mdio_interrupt_test_array['option_phy'] + ' ' + cel_mdio_interrupt_test_array['ele2']
        var_pass_pattern = cel_mdio_option_0x5200cb20_pass_pattern
        var_path = FPGA_TOOL_PATH
        cmd = './' + var_toolName + ' ' + var_option

        dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

@logThis
def verify_mdio_tool_fpga_option_0x2c():
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "") 
    for param in range(1, 9):
        if 'minipack2_dc' in devicename.lower():
            if (param == 3) or (param == 4) or (param == 5) or (param == 6):
                continue
        var_toolName = cel_mdio_interrupt_test_array['bin_tool']
        var_option = cel_mdio_interrupt_test_array['store_2'] + ' ' + cel_mdio_interrupt_test_array['option_r'] + ' ' + \
                     cel_mdio_interrupt_test_array['option_pim'] + str(param) + ' ' + cel_mdio_interrupt_test_array['ele3']
        var_pass_pattern = cel_mdio_option_0x2c_pass_pattern
        var_path = FPGA_TOOL_PATH
        cmd = './' + var_toolName + ' ' + var_option

        dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

def check_bic_stress_option_h():
    Log_Debug("Entering procedure check_bic_stress_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'BIC_stress.sh'
    var_option = '-h'
    var_keywords_pattern = bic_stress_option_h
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, path=BMC_STRESS_BIC_PATH)

def check_bic_stress_option_n(loop):
    Log_Debug("Entering procedure check_bic_stress_option_n.\n")
    dLibObj = getDiagLibObj()
    return dLibObj.check_bic_stress_option_n(loop)

def check_fpga_pcie_stress_option_n(loop):
    Log_Debug("Entering procedure check_fpga_pcie_stress_option_n.\n")
    dLibObj = getDiagLibObj()
    return dLibObj.check_fpga_pcie_stress_option_n(loop)

def set_come_mgmt_port_ip_and_ping_to_remote_host(remote_ip="", remote_netmask="", interface=""):
    Log_Debug("Entering procedure set_come_mgmt_port_ip_and_ping_to_remote_host.\n")
    dLibObj = getDiagLibObj()

    _ip_network = object()
    _ip_version = int()
    _ip_hosts = object()
    _ping_target = str()
    _ping_args = str()

    dLibObj.wpl_execute(cmd="ip link set " + interface + " up", mode="centos", timeout=60)

    try:
        _ip_network = ipaddress.ip_network(remote_ip + "/" + remote_netmask, False)
    except ValueError:
        dLibObj.wpl_raiseException("The server IP is an unrecognized format")

    _ip_version = _ip_network.version
    _ip_hosts = _ip_network.hosts()

    _ping_args = " -c 1 -I " + interface

    if _ip_version == 6:
        _ping_args += " -6 "
    elif _ip_version == 4:
        _ping_args += " -4 "
    else:
        dLibObj.wpl_raiseException("Unknow IP version")

    for host in _ip_hosts:
        _output = dLibObj.wpl_execute(cmd="ping" + _ping_args + str(host), mode="centos", timeout=60)
        try:
            _loss = int(re.search(r"(?P<loss>\d+)% packet loss", _output).group("loss"))
        except IndexError:
             dLibObj.wpl_raiseException("Can't determine the ping loss percentage")

        if _loss == 100 and _ip_version == 4:
            dLibObj.wpl_execute(cmd="ip addr add " + str(host) + "/" + remote_netmask + " dev " + interface, mode="centos", timeout=60)

            _output = dLibObj.wpl_execute(cmd="ping" + _ping_args + remote_ip, mode="centos", timeout=60)
            try:
                _loss = int(re.search(r"(?P<loss>\d+)% packet loss", _output).group("loss"))
            except IndexError:
                dLibObj.wpl_raiseException("Can't determine the ping loss percentage")

            if _loss != 0:
                dLibObj.wpl_raiseException("Failed to assign new IP to " + interface + " and ping to " + remote_ip)

            break
        elif _loss == 100 and _ip_version == 6:
            dLibObj.wpl_execute(cmd="ifconfig " + interface + " inet6 add " + str(host) + "/" + remote_netmask + " up", mode="centos", timeout=60)

            _output = dLibObj.wpl_execute(cmd="ping" + _ping_args + remote_ip, mode="centos", timeout=60)
            try:
                _loss = int(re.search(r"(?P<loss>\d+)% packet loss", _output).group("loss"))
            except IndexError:
                dLibObj.wpl_raiseException("Can't determine the ping loss percentage")
            if _loss != 0:
                dLibObj.wpl_raiseException("Failed to assign new IP to " + interface + " and ping to " + remote_ip)

            break


def set_iob_fpga_card_to_present(regex="Card present"):
    Log_Debug("Entering procedure set_iob_fpga_card_to_present.\n")
    dLibObj = getDiagLibObj()

    dLibObj.setpci(argument="-s 9:8 0x3e.B=0x13", regex=regex, mode="centos")
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("setpci is return exit code " + _return_code)

def list_of_pci_devices_and_verify(device_list=list()):
    Log_Debug("Entering procedure list_of_pci_devices_and_verify.\n")
    dLibObj = getDiagLibObj()

    dLibObj.lspci(device_list=device_list)
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("lspci is return exit code " + _return_code)

def set_iob_fpga_card_to_not_present():
    Log_Debug("Entering procedure set_iob_fpga_card_to_not_present.\n")
    dLibObj = getDiagLibObj()

    dLibObj.setpci(argument="-s 12:0 0x3e.B", regex="00", mode="centos")
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("setpci is return exit code " + _return_code)

    dLibObj.setpci(argument="-s 9:8 0x3e.B", regex="13", mode="centos")
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("setpci is return exit code " + _return_code)

    dLibObj.setpci(argument="-s 9:8 0x3e.B=0x53", regex="Card not present", mode="centos")
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("setpci is return exit code " + _return_code)

def run_i2cdump_and_check_for_the_data_change(where=list()):
    Log_Debug("Entering procedure run_i2cdump_and_check_for_the_data_change.\n")
    dLibObj = getDiagLibObj()

    _i2cdump_before_edit = dLibObj.i2cdump(argument="-y -f 13 0x35", where=where, mode="openbmc", timeout=60)
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("i2cdump is return exit code " + _return_code)

    dLibObj.wpl_execute(cmd="i2cset -y -f " + bios_smb_cpld_bus + " " + bios_smb_cpld_chip_address + " 0x47 0", mode="openbmc", timeout=60)
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("i2cset is return exit code " + _return_code)

    dLibObj.wpl_execute(cmd="i2cset -y -f " + bios_smb_cpld_bus + " " + bios_smb_cpld_chip_address + " 0x47 2", mode="openbmc", timeout=60)
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("i2cset is return exit code " + _return_code)

    _i2cdump_after_edit = dLibObj.i2cdump(argument="-y -f 13 0x35", where=where, mode="openbmc", timeout=60)
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("i2cdump is return exit code " + _return_code)

    for o, e in zip(_i2cdump_before_edit, _i2cdump_after_edit):
        if o != e:
            for c, (o_x, e_x) in enumerate(zip( o[1:], e[1:])):
                if o_x != e_x:
                    addr = hex(int(o[0], base=16) + int(c))
                    if addr not in where:
                        dLibObj.wpl_raiseException("Failed the i2cdump reported on address " + addr + ", 0x" + o_x + " != 0x" + e_x)

    _i2cdump_before_edit = _i2cdump_after_edit
    dLibObj.wpl_execute(cmd="i2cset -y -f " + bios_smb_cpld_bus + " " + bios_smb_cpld_chip_address + " 0x47 3", mode="openbmc", timeout=60)
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("i2cset is return exit code " + _return_code)

    _i2cdump_after_edit = dLibObj.i2cdump(argument="-y -f 13 0x35", where=where, mode="openbmc", timeout=60)
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("i2cdump is return exit code " + _return_code)

    for o, e in zip(_i2cdump_before_edit, _i2cdump_after_edit):
        if o != e:
            for c, (o_x, e_x) in enumerate(zip( o[1:], e[1:])):
                if o_x != e_x:
                    addr = hex(int(o[0], base=16) + int(c))
                    if addr not in where:
                        dLibObj.wpl_raiseException("Failed the i2cdump reported on address " + addr + ", 0x" + o_x + " != 0x" + e_x)

def run_fb_sh():
    Log_Debug("Entering procedure run_fb_sh.\n")
    dLibObj = getDiagLibObj()

    dLibObj.wpl_getPrompt("centos", 600)
    dLibObj.wpl_execute("/etc/rc.d/fb.sh")
    _return_code = dLibObj.wpl_execute("echo $?")
    if "0" not in _return_code:
        dLibObj.wpl_raiseException("fb.sh is return exit code " + _return_code)

def run_fpga_ver():
    Log_Debug("Entering procedure run_fpga_ver.\n")
    dLibObj = getDiagLibObj()

    var_toolName = './fpga'
    var_option = 'ver'
    var_keywords_pattern = mp2_fpga_ver_pattern
    var_pass_pattern = ''
    var_path = FPGA_TOOL_PATH

    return dLibObj.verify_cenos_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_eeprom_qsfp_option_h():
    Log_Debug("Entering procedure verify_eeprom_tool_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_eeprom_qsfp_array['bin_tool']
    var_option = cel_eeprom_qsfp_array['option_h']
    var_pass_pattern = cel_qsfp_h_pass_pattern
    var_path = DIAG_TOOL_PATH
    cmd = './' + var_toolName + ' ' + var_option

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

def verify_eeprom_qsfp_option_help():
    Log_Debug("Entering procedure verify_eeprom_tool_option_help.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_eeprom_qsfp_array['bin_tool']
    var_option = cel_eeprom_qsfp_array['option_help']
    var_pass_pattern = cel_qsfp_h_pass_pattern
    var_path = DIAG_TOOL_PATH
    cmd = './' + var_toolName + ' ' + var_option

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

def verify_eeprom_qsfp_test():
    Log_Debug("Entering procedure verify_eeprom_qsfp_test.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_eeprom_qsfp_array['bin_tool']
    var_option_m = cel_eeprom_qsfp_array['pim']
    var_option_p = cel_eeprom_qsfp_array['port']
    var_option_i = cel_eeprom_qsfp_array['option_i']
    var_pass_pattern = cel_qsfp_pass_pattern
    var_path = DIAG_TOOL_PATH

    return dLibObj.verify_qsfp_test(var_toolName, var_option_m, var_option_p, var_option_i, var_pass_pattern, var_path)

def verify_scm_eeprom_update():
    Log_Debug("Entering procedure verify_scm_eeprom_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_fru_eeprom_update_array['read_tool']
    var_read_option = cel_fru_eeprom_update_array['read_option']
    var_write_tool = cel_fru_eeprom_update_array['write_tool']
    var_path = cel_fru_eeprom_update_array['scm_eeprom_path']
    var_pass_pattern = cel_fru_eeprom_update_array['pass_pattern']
    var_verify_tool = cel_fru_eeprom_update_array['verify_tool']

    return dLibObj.verify_fru_eeprom_update(var_read_tool, var_read_option, var_write_tool, var_path, var_pass_pattern, var_verify_tool)

def verify_smb_eeprom_update():
    Log_Debug("Entering procedure verify_smb_eeprom_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_fru_eeprom_update_array['read_tool']
    var_read_option = cel_fru_eeprom_update_array['read_option']
    var_write_tool = cel_fru_eeprom_update_array['write_tool']
    var_path = cel_fru_eeprom_update_array['smb_eeprom_path']
    var_pass_pattern = cel_fru_eeprom_update_array['pass_pattern']
    var_verify_tool = cel_fru_eeprom_update_array['verify_tool']

    return dLibObj.verify_fru_eeprom_update(var_read_tool, var_read_option, var_write_tool, var_path, var_pass_pattern, var_verify_tool)

def verify_sim_eeprom_update():
    Log_Debug("Entering procedure verify_sim_eeprom_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_fru_eeprom_update_array['read_tool']
    var_read_option = cel_fru_eeprom_update_array['read_option']
    var_write_tool = cel_fru_eeprom_update_array['write_tool']
    var_path = cel_fru_eeprom_update_array['sim_eeprom_path']
    var_pass_pattern = cel_fru_eeprom_update_array['pass_pattern']
    var_verify_tool = cel_fru_eeprom_update_array['verify_tool']

    return dLibObj.verify_fru_eeprom_update(var_read_tool, var_read_option, var_write_tool, var_path, var_pass_pattern, var_verify_tool)

def verify_bmc_eeprom_update():
    Log_Debug("Entering procedure verify_bmc_eeprom_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_fru_eeprom_update_array['read_tool']
    var_read_option = cel_fru_eeprom_update_array['read_option']
    var_write_tool = cel_fru_eeprom_update_array['write_tool']
    var_path = cel_fru_eeprom_update_array['bmc_eeprom_path']
    var_pass_pattern = cel_fru_eeprom_update_array['pass_pattern']
    var_verify_tool = cel_fru_eeprom_update_array['verify_tool']

    return dLibObj.verify_fru_eeprom_update(var_read_tool, var_read_option, var_write_tool, var_path, var_pass_pattern, var_verify_tool)

def verify_fcm_t_eeprom_update():
    Log_Debug("Entering procedure verify_fcm_t_eeprom_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_fru_eeprom_update_array['read_tool']
    var_read_option = cel_fru_eeprom_update_array['read_option']
    var_write_tool = cel_fru_eeprom_update_array['write_tool']
    var_path = cel_fru_eeprom_update_array['fcm-t_eeprom_path']
    var_pass_pattern = cel_fru_eeprom_update_array['pass_pattern']
    var_verify_tool = cel_fru_eeprom_update_array['verify_tool']

    return dLibObj.verify_fru_eeprom_update(var_read_tool, var_read_option, var_write_tool, var_path, var_pass_pattern, var_verify_tool)

def verify_fcm_b_eeprom_update():
    Log_Debug("Entering procedure verify_fcm_b_eeprom_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_fru_eeprom_update_array['read_tool']
    var_read_option = cel_fru_eeprom_update_array['read_option']
    var_write_tool = cel_fru_eeprom_update_array['write_tool']
    var_path = cel_fru_eeprom_update_array['fcm-b_eeprom_path']
    var_pass_pattern = cel_fru_eeprom_update_array['pass_pattern']
    var_verify_tool = cel_fru_eeprom_update_array['verify_tool']

    return dLibObj.verify_fru_eeprom_update(var_read_tool, var_read_option, var_write_tool, var_path, var_pass_pattern, var_verify_tool)

def verify_pim_eeprom_update():
    Log_Debug("Entering procedure verify_pim_eeprom_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_fru_eeprom_update_array['read_tool']
    var_read_option = cel_fru_eeprom_update_array['read_option']
    var_write_tool = cel_fru_eeprom_update_array['write_tool']
    var_verify_tool = cel_fru_eeprom_update_array['verify_tool']
    var_path = cel_fru_eeprom_update_array['pim_eeprom_path']
    var_pass_pattern = cel_fru_eeprom_update_array['pass_pattern']

    return dLibObj.check_fru_eeprom_update(var_read_tool, var_read_option, var_write_tool, var_verify_tool, var_path, var_pass_pattern)

def verify_fan_eeprom_update():
    Log_Debug("Entering procedure verify_fan_eeprom_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_fru_eeprom_update_array['read_tool']
    var_read_option = cel_fru_eeprom_update_array['read_option']
    var_write_option = cel_fru_eeprom_update_array['write_tool']
    var_verify_tool = cel_fru_eeprom_update_array['verify_tool']
    var_path = cel_fru_eeprom_update_array['fan_eeprom_path']
    var_pass_pattern = cel_fru_eeprom_update_array['pass_pattern']

    return dLibObj.check_fru_eeprom_update(var_read_tool, var_read_option, var_write_option, var_verify_tool, var_path, var_pass_pattern)

def set_E_Loopback_to_high_power_mode():
    Log_Debug("Entering procedure set_E_Loopback_to_high_power_mode.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_e_loopback_help_arry['bin_tool']
    var_option = cel_e_loopback_help_arry['option']
    var_pass_pattern = list_pass_pattern
    var_path = FPGA_TOOL_PATH
    cmd = './' + var_toolName + ' ' + var_option

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

def verify_bios_check_tool_help_dict():
    Log_Debug("Entering procedure verify_bios_check_tool_help_dict.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bios_config_check_help_dict['bin_tool']
    var_pass_pattern = cel_bios_check_tool_help_pattern
    var_path = FPGA_TOOL_PATH
    cmd = './' + var_toolName

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

def check_bios_default_config():
    Log_Debug("Entering procedure check_bios_default_config.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bios_config_check_help_dict['bin_tool']
    var_golden_file = cel_bios_config_check_help_dict['golden_file']
    var_option_tool = cel_bios_config_check_help_dict['option_tool']
    var_path = FPGA_TOOL_PATH
    var_pass_pattern = cel_bios_default_check_pass_pattern
    cmd = './' + var_toolName + ' ' + var_golden_file + ' ' + var_option_tool

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

def verify_bios_modified_info():
    Log_Debug("Entering procedure verify_bios_modified_info.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_bios_config_check_help_dict['bin_tool']
    var_golden_file = cel_bios_config_check_help_dict['golden_file']
    var_option_tool = cel_bios_config_check_help_dict['option_tool']
    var_path = FPGA_TOOL_PATH
    var_pass_pattern = cel_bios_default_check_fail_pattern
    cmd = './' + var_toolName + ' ' + var_golden_file + ' ' + var_option_tool

    return dLibObj.execute_check_cmd(cmd=cmd, mode='centos', patterns=var_pass_pattern, path=var_path)

def cloudripper_cel_psu_test_s():
    Log_Debug("Entering procedure cloudripper_cel_psu_test_s.\n")
    dLibObj = getDiagLibObj()

    var_toolName = 'cel-psu-test'
    var_option = "-s"
    var_keywords_pattern = cloudripper_cel_psu_test_s_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_cloudripper_cel_psu_option_s(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def reboot_and_reset_bios_setup_bootorder_1st(device='DUT'):
    Log_Debug("Entering procedure reboot_and_reset_bios_setup_bootorder_1st.\n")

    bios_menu_lib.enter_bios_setup(device)
    bios_menu_lib.send_key(device, 'KEY_LEFT', 2)
    bios_menu_lib.send_key(device, 'KEY_DOWN', 2)
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    bios_menu_lib.send_key(device, 'KEY_DOWN')
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    bios_menu_lib.send_key(device, 'KEY_RIGHT')
    bios_menu_lib.save_bios_setup(device)

def reboot_and_reset_bios_setup_to_default(device='DUT'):
    Log_Debug("Entering procedure reboot_and_reset_to_default.\n")

    bios_menu_lib.enter_bios_setup(device)
    bios_menu_lib.send_key(device, 'KEY_LEFT')
    bios_menu_lib.send_key(device, 'KEY_DOWN', 3)
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    time.sleep(3)
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    bios_menu_lib.send_key(device, 'KEY_UP', 2)
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    time.sleep(3)
    bios_menu_lib.send_key(device, 'KEY_ENTER')
    deviceObj.getPrompt("centos", timeout=420)

def verify_SCM_eeprom_tool_update():
    Log_Debug("Entering procedure verify_SCM_eeprom_tool_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_eeprom_test_array['read_tool']
    var_write_tool = cel_eeprom_test_array['write_tool']
    var_option = cel_eeprom_test_array['option_d'] + ' ' + cel_eeprom_test_array['option_e']
    var_path = EEPROM_TOOL_PATH
    var_line_string = cel_eeprom_test_array['line_string']
    var_part = cel_eeprom_test_array['part_SCM']
    var_pass_pattern = cel_eeprom_test_array['pass_pattern']

    return dLibObj.verify_and_update_eeprom(var_read_tool, var_write_tool, var_option, var_path, var_line_string, var_pass_pattern, var_part)

def verify_FCM_eeprom_tool_update():
    Log_Debug("Entering procedure verify_FCM_eeprom_tool_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_eeprom_test_array['read_tool']
    var_write_tool = cel_eeprom_test_array['write_tool']
    var_option = cel_eeprom_test_array['option_d'] + ' ' + cel_eeprom_test_array['option_e']
    var_path = EEPROM_TOOL_PATH
    var_line_string = cel_eeprom_test_array['line_string']
    var_part = cel_eeprom_test_array['part_FCM']
    var_pass_pattern = cel_eeprom_test_array['pass_pattern']

    return dLibObj.verify_and_update_eeprom(var_read_tool, var_write_tool, var_option, var_path, var_line_string, var_pass_pattern, var_part)

def verify_SMB_eeprom_tool_update():
    Log_Debug("Entering procedure verify_SMB_eeprom_tool_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_eeprom_test_array['read_tool']
    var_write_tool = cel_eeprom_test_array['write_tool']
    var_option = cel_eeprom_test_array['option_d'] + ' ' + cel_eeprom_test_array['option_e']
    var_path = EEPROM_TOOL_PATH
    var_line_string = cel_eeprom_test_array['line_string']
    var_part = cel_eeprom_test_array['part_SMB']
    var_pass_pattern = cel_eeprom_test_array['pass_pattern']

    return dLibObj.verify_and_update_eeprom(var_read_tool, var_write_tool, var_option, var_path, var_line_string, var_pass_pattern, var_part)

def verify_FAN_eeprom_tool_update():
    Log_Debug("Entering procedure verify_FAN_eeprom_tool_update.\n")
    dLibObj = getDiagLibObj()

    var_read_tool = cel_eeprom_test_array['read_tool']
    var_write_tool = cel_eeprom_test_array['write_tool']
    var_option = cel_eeprom_test_array['option_d'] + ' ' + cel_eeprom_test_array['option_e']
    var_path = EEPROM_TOOL_PATH
    var_line_string = cel_eeprom_test_array['line_string']
    var_part = cel_eeprom_test_array['part_FAN']
    var_pass_pattern = cel_eeprom_test_array['pass_pattern']

    return dLibObj.verify_and_update_eeprom(var_read_tool, var_write_tool, var_option, var_path, var_line_string, var_pass_pattern, var_part)

def verify_eeprom_tool_help_dict_option_h():
    Log_Debug("Entering procedure verify_eeprom_tool_help_dict_option_h.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_eeprom_test_array['read_tool']
    var_option = '-h'
    var_keywords_pattern = cel_eeprom_tool_opion_h_pass_pattern
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, EEPROM_TOOL_PATH)

def verify_eeprom_tool_BSM_info():
    Log_Debug("Entering procedure verify_eeprom_tool_BSM_info.\n")
    dLibObj = getDiagLibObj()

    var_toolName = cel_eeprom_test_array['read_tool']
    var_option = cel_eeprom_test_array['option_d'] + ' ' + cel_eeprom_test_array['option_e'] + ' ' +  cel_eeprom_test_array['part_BSM']
    var_keywords_pattern = cel_eeprom_tool_BSM_pass_pattern
    var_pass_pattern = ''

    return dLibObj.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, EEPROM_TOOL_PATH)

def mp2_copy_lpmode_script_files():
    Log_Debug("Entering procedure mp2_copy_tool_script_files.\n")
    dLibObj = getDiagLibObj()
    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ip
    devicename = os.environ.get("deviceName", "")
    if 'minipack2_dc' in devicename.lower():
        var_filelist = lpmode_script_file
        var_destination_path = UNIT_LPMODE_TOOL_PATH
        var_filepath = BIC_SCRIPT_PATH
        var_mode = centos_mode
        CommonLib.get_dhcp_ip_address(Const.DUT, openbmc_eth_params['interface'], centos_mode)
        var_interface = openbmc_eth_params['interface']
        output = 0
        output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist,
                                              var_filepath, var_destination_path, var_mode, False, False, var_interface,
                                              DEFAULT_SCP_TIME)

def mp2_copy_bic_script_files():
    Log_Debug("Entering procedure mp2_copy_bic_script_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ip
    devicename = os.environ.get("deviceName", "")
    if 'minipack2_dc' in devicename.lower():
        var_filelist = bic_script_file_dc
        var_destination_path = UNIT_BIC_TOOL_PATH_DC
    else:
        var_destination_path = UNIT_BIC_TOOL_PATH
        var_filelist = bic_script_file
    var_filepath = BIC_SCRIPT_PATH
    var_mode = openbmc_mode
    CommonLib.get_dhcp_ip_address(Const.DUT, openbmc_eth_params['interface'], openbmc_mode)
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist,
                                              var_filepath, var_destination_path, var_mode, False, False, var_interface,
                                              DEFAULT_SCP_TIME)

def w400_mp_copy_i2c_config_files():
    Log_Debug("Entering procedure w400_mp_copy_i2c_config_files.\n")
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    if 'wedge400_mp' in devicename.lower():
        var_username = scp_username
        var_password = scp_password
        var_server_ip = scp_ipv6
        var_filelist = i2c_config_file_list
        var_filepath = DOWNLOADABLE_DIR_WEDGE400
        var_destination_path = BMC_DIAG_CONFIG_PATH
        var_mode = openbmc_mode
        get_dhcp_ipv6_addresses('eth')
        var_interface = openbmc_eth_params['interface']

        output = 0
        output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

def wedge400c_copy_tool_files(toolName, toolPath, goalPath):
    Log_Debug("Entering procedure wedge400c_copy_tool_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    devicename = os.environ.get("deviceName", "")
    if 'wedge400c_dc' in devicename.lower() or 'wedge400c_rsp' in devicename.lower():
        var_filepath = toolPath
        var_filelist = toolName
        var_destination_path = goalPath
        var_mode = centos_mode
        get_dhcp_ipv6_addresses('eth')
        var_interface = openbmc_eth_params['interface']

        output = 0
        output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

def wedge400c_copy_bios_config_files():
    Log_Debug("Entering procedure copy_bios_config_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    devicename = os.environ.get("deviceName", "")
    #if 'wedge400_dc-01' in devicename.lower():
        #var_filepath = DOWNLOADABLE_DIR_WEDGE400_3A10
    #else:
    var_filepath = DOWNLOADABLE_DIR_WEDGE400C
    var_filelist = bios_config_file_list
    var_destination_path = FPGA_TOOL_PATH
    var_mode = centos_mode
    get_dhcp_ipv6_addresses('eth')
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

def copy_bios_config_files():
    Log_Debug("Entering procedure copy_bios_config_files.\n")
    dLibObj = getDiagLibObj()

    var_username = scp_username
    var_password = scp_password
    var_server_ip = scp_ipv6
    var_filelist = bios_config_file_list
    var_filepath = DOWNLOADABLE_DIR_CLOUDRIPPER
    var_destination_path = FPGA_TOOL_PATH
    var_mode = centos_mode
    get_dhcp_ipv6_addresses('eth')
    var_interface = openbmc_eth_params['interface']

    output = 0
    output = CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, var_mode, False, True, var_interface, DEFAULT_SCP_TIME)

    if output:
        dLibObj.wpl_raiseException("Failed copy_files_through_scp")
    return output

def cel_sensor_test_s_with_high_power():
    Log_Debug("Entering procedure cel_sensor_test_s_with_high_power.\n")
    dLibObj = getDiagLibObj()

    high_power_cmd = './cel-sensor-test -s'
    high_power_pattern = high_power_sensor_s_pattern
    path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_high_power_sensor_GB_test(high_power_cmd, high_power_pattern, path)

def cel_sensor_test_u_with_high_power():
    Log_Debug("Entering procedure cel_sensor_test_u_with_high_power.\n")
    dLibObj = getDiagLibObj()

    high_power_cmd = './cel-sensor-test -u'
    high_power_pattern = high_power_sensor_u_pattern
    path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_high_power_sensor_GB_test(high_power_cmd, high_power_pattern, path)

def cel_sensor_test_a_with_high_power():
    Log_Debug("Entering procedure cel_sensor_test_a_with_high_power.\n")
    dLibObj = getDiagLibObj()

    high_power_cmd = './cel-sensor-test -a'
    high_power_pattern = high_power_sensor_a_pattern
    path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_high_power_sensor_GB_test(high_power_cmd, high_power_pattern, path)

def sensor_util_all_threshold_with_high_power():
    Log_Debug("Entering procedure sensor_util_all_threshold_with_high_power.\n")
    dLibObj = getDiagLibObj()

    high_power_cmd = 'sensor-util all --threshold'
    high_power_pattern = high_power_sensor_s_pattern
    path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_high_power_sensor_GB_test(high_power_cmd, high_power_pattern, path)

def sensors_with_high_power():
    Log_Debug("Entering procedure sensors_with_high_power.\n")
    dLibObj = getDiagLibObj()

    high_power_cmd = 'sensors'
    high_power_pattern = high_power_sensor_s_pattern
    path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_high_power_sensor_GB_test(high_power_cmd, high_power_pattern, path)

def run_sdk_init_without_exit():
    Log_Debug("Entering procedure run sdk_init_without_exit.\n")
    dLibObj = getDiagLibObj()

    #toolName = ['snake_standalone.py']
    #toolPath = DOWNLOADABLE_DIR_WEDGE400C
    #goalPath1 = '/usr/local/cls_diag/SDK/examples/sanity'
    #goalPath2 = '/usr/local/cls_diag/SDK/cel_sdk/snake'
    #wedge400c_copy_tool_files(toolName, toolPath, goalPath1)
    #wedge400c_copy_tool_files(toolName, toolPath, goalPath2)

    high_power_variable = 'all --run_case 1'
    high_power_option = '-c'
    high_power_cmd = 'python3 auto_load_user.py' + ' ' + high_power_option + ' ' + high_power_variable
    path = SDK_UTIL_PATH

    return dLibObj.test_init_sdk_and_switch_to_bmc(high_power_cmd,path)

def exit_sdk_init_mode():
    Log_Debug("Entering procedure exit_sdk_init_mode.\n")
    
    CommonLib.change_dir(SDK_UTIL_PATH, centos_mode)

@logThis
def config_configs_yaml_file():
    dLibObj = getDiagLibObj()

    var_toolName = "./cel-tpm-test --all  --config=../configs/tpm.yaml"
    var_option = ' '
    var_keywords_pattern = tpm_all_config_yaml_patterns
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_config_yaml_test(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

@logThis
def read_eltt2_pcr():
    dLibObj = getDiagLibObj()

    var_toolName = './eltt2 -R '
    for i in range(0, 8):
        var_option = str(i)
        var_keywords_pattern = [
            'Read PCR.*?',
        ]
        var_pass_pattern = ""
        var_path = FPGA_TOOL_PATH
        dLibObj.verify_config_yaml_test(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

def verify_eth_test_option_s():
    Log_Debug("Entering procedure verify_eth_test_option_s.\n")
    dLibObj = getDiagLibObj()

    toolName = './cel-eth-test'
    option = ' -s '
    path = BMC_DIAG_TOOL_PATH

    return dLibObj.check_eth_dict_option_test(toolName, option, path)

def verify_eth_test_option_a():
    Log_Debug("Entering procedure verify_eth_test_option_a.\n")
    dLibObj = getDiagLibObj()

    toolName = './cel-eth-test'
    option = ' -a '
    path = BMC_DIAG_TOOL_PATH

    return dLibObj.check_eth_dict_option_test(toolName, option, path)

def ping_come_usb0_ip():
    Log_Debug("Entering procedure ping_come_usb0_ip.\n")
    dLibObj = getDiagLibObj()

    toolName = 'ifconfig'
    option = ' -a '
    path = BMC_DIAG_TOOL_PATH

    return dLibObj.check_eth_dict_option_test(toolName, option, path)

def minipack2_verify_sw_dict_option_S():
    Log_Debug("Entering procedure Minipack2_verify_sw_version_help_dict_option_S.\n")
    dLibObj = getDiagLibObj()

    toolName = 'cel-version-test'
    option = '-S'
    pattern = minipack2_sw_option_S_show
    path = '/usr/local/cls_diag/bin/'

    return dLibObj.verify_minipack2_sw_test(toolName, option, pattern, path)

def minipack2_verify_sw_dict_option_show():
    Log_Debug("Entering procedure Minipack2_verify_sw_version_help_dict_option_show.\n")
    dLibObj = getDiagLibObj()

    toolName = 'cel-version-test'
    option = '--show'
    pattern = minipack2_sw_option_S_show
    path = '/usr/local/cls_diag/bin/'

    return dLibObj.verify_minipack2_sw_test(toolName, option, pattern, path)

@logThis
def check_sys_before_log(param):
    dLibObj = getDiagLibObj()

    var_toolName = './cel_syslog -c -l'
    var_option = ' log/PCIE_sys_before'
    var_pattern = ''
    var_path = '/usr/local/cls_diag/utility/stress/syslog/'
    param = param

    return dLibObj.check_sys_before_and_after_log_test(var_toolName, var_option, var_pattern, var_path, param)

@logThis
def check_sys_after_log(param):
    dLibObj = getDiagLibObj()

    var_toolName = './cel_syslog -c -l'
    var_option = ' log/PCIE_sys_after'
    var_pattern = ''
    var_path = '/usr/local/cls_diag/utility/stress/syslog/'
    param = param

    return dLibObj.check_sys_before_and_after_log_test(var_toolName, var_option, var_pattern, var_path, param)

@logThis
def check_cpld_main_info():
    dLibObj = getDiagLibObj()

    var_toolName = cel_bmc_cpld_help_array["bin_tool"]
    var_option1 = ' -r -c'
    var_option2 = ' -w -c'
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.verify_check_cpld_main_info_func(var_toolName, var_option1, var_option2, var_path)

@logThis
def dhclient_to_set_ipv4_and_ipv6():

    dLibObj = getDiagLibObj()

    var_ipv4 = 'dhclient eth0'
    var_ipv6 = 'dhclient -6 eth0 --address-prefix-len 64'

    return  dLibObj.verify_client_ipv4_and_ipv6(var_ipv4, var_ipv6)

@logThis
def auto_pim_eeprom_update():
    dLibObj = getDiagLibObj()
    devicename = os.environ.get("deviceName", "")
    var_toolName = './auto_eeprom'
    for i in range(1, 9):
        if 'minipack2_dc' in devicename.lower():
            if (i == 3) or (i == 4) or (i == 5) or (i == 6):
                continue
        var_option = ' ' + str(i)
        var_pattern = ''
        var_path = '/mnt/data1/BMC_Diag/utility/PIM_eeprom'

        dLibObj.verify_pim_fan_eeprom_update(var_toolName, var_option, var_pattern, var_path)

@logThis
def auto_fan_eeprom_update():
    dLibObj = getDiagLibObj()

    var_toolName = './auto_eeprom'
    for i in range(1, 9):
        var_option = ' ' + str(i)
        var_pattern = ''
        var_path = '/mnt/data1/BMC_Diag/utility/FAN_eeprom'

        dLibObj.verify_pim_fan_eeprom_update(var_toolName, var_option, var_pattern, var_path)

@logThis
def reset_the_whole_system():
    dLibObj = getDiagLibObj()

    return dLibObj.reset_the_whole_system()

@logThis
def power_the_whole_system():
    dLibObj = getDiagLibObj()

    #return dLibObj.power_system()
    return dLibObj.power_reset_system()

@logThis
def check_dmesg_log_about_error():
    dLibObj = getDiagLibObj()
    var_toolName = cel_tpm_test["bin_tool"]
    var_option = "-i"
    var_keywords_pattern = cel_tpm_test_device_i_pattern
    var_pass_pattern = ""
    var_path = BMC_DIAG_TOOL_PATH

    return dLibObj.dmesg_log_check(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

@logThis
def power_chassis_system():
    dLibObj = getDiagLibObj()

    return dLibObj.power_system()

