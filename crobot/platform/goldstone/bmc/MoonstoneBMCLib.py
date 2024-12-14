##############################################################################
# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
import re
import CRobot
from inspect import getframeinfo, stack
import os.path
import time
import yaml
import Logger as log
import CommonLib
import CommonKeywords
import random
import Const
from functools import partial
import Const
import YamlParse
import bios_menu_lib
import Logger as log
import pexpect
import getpass
import os
import json
import openbmc
import openbmc_lib
import multiprocessing

from MoonstoneBMCVariable import *
from datetime import datetime, timedelta
from dataStructure import nestedDict, parser
from SwImage import SwImage
from pexpect import pxssh
import sys
import getpass
import MOONSTONECommonLib
from Decorator import *
try:
    import DeviceMgr
    from Device import Device

except Exception as err:
    log.cprint(str(err))


device= DeviceMgr.getDevice()
run_command = partial(CommonLib.run_command, deviceObj=device, prompt="root@localhost:~#")

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common','commonlib'))

# TC1 - BMC_Device_Info_Check_Test
@logThis
def check_bmc_version_info(device, lanplus=False):
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd = lanplus_ipmitool_cmd.format("mc info")
    else:
        cmd='ipmitool mc info'
    c1=device_obj.executeCmd(cmd)
    CommonKeywords.should_match_paired_regexp_list(c1,bmc_version_info_list)
    log.success("BMC version info is as expected.")


@logThis
def bmc_reset(device, coldOrwarm, lanplus=False, sleep=200):
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd = lanplus_ipmitool_cmd.format("mc reset " + coldOrwarm)
    else:
        cmd="ipmitool mc reset " + coldOrwarm
    c1=device_obj.executeCmd(cmd)
    pattern = "Sent "+ coldOrwarm +" reset command to MC"
    log.info("Sleeping for {} seconds for device to come up".format(sleep))
    time.sleep(sleep)
    CommonKeywords.should_match_a_regexp(c1,pattern)
    # power_status = check_sel_list_info(device, sel_list_pattern=sel_list_mc_reset_pattern, lanplus=lanplus)
    # if(power_status):
        # log.success("bmc reset " + coldOrwarm + " executed successfully.")
    # else:
        # raise RuntimeError("bmc reset "+ coldOrwarm + " failed !!")
    log.success("bmc reset " + coldOrwarm + " executed successfully.")

def set_power_cycle(device, lanplus=False):
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd = "ipmitool -I lanplus -H %s -U root -P 0penBmc -C 17 power cycle \r" % mgmt_ip
    else:
        cmd = "ipmitool power cycle \r"
    res = device_obj.sendMsg(cmd) 
    out=device_obj.read_until_regexp('localhost login:*',timeout=400)
    log.cprint("login into it ")
    device_obj.loginToDiagOS()
    log.cprint("login into it ")
    power_status = check_sel_list_info(device, sel_list_power_on_pattern, lanplus)
    if power_status:
        log.success("Device is UP after power cycle successfully, verified through sel list log.")
    else:
        raise RuntimeError("Device is not powercycled properly, as power status of sel log is not as expected.")
    
    
def check_sel_list_info(device, sel_list_pattern, lanplus=False):
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        promptServer=device_obj.promptServer
        cmd = lanplus_ipmitool_cmd.format('sel list')
    else:
        cmd = "ipmitool sel list"
    log.info("Fetching BMC sel list ")
    c1=device_obj.executeCmd(cmd, timeout=120)
    c1=c1.split("\n")
    c1=c1[-6:]
    log.cprint(c1)
    log.cprint(sel_list_pattern)
    CommonKeywords.should_match_paired_regexp_list(c1,sel_list_pattern)
    return True


# TC - Lan Communication/Configuration Test
        
def set_bmc_ip_netmask(device, ipaddr=None, netmask=None, lanplus=False):
    device_obj = Device.getDeviceObject(device)
    if ipaddr:
        if(lanplus):
            mgmt_ip = device_obj.managementIP
            promptServer=device_obj.promptServer
            cmd = "ipmitool -I lanplus -H %s -U root -P 0penBmc -C 17 lan set 1 ipaddr %s" % (mgmt_ip, ipaddr)
        else:
            cmd = r"ipmitool lan set 1 ipaddr %s" % (ipaddr)
        output1=device_obj.executeCmd(cmd) 
        pattern = "Setting LAN IP Address to %s" %ipaddr
        CommonKeywords.should_match_a_regexp(output1,pattern)
        log.success("IP address is updated via ipmitool lan command successfully.")
    if netmask:
        if(lanplus):
            mgmt_ip = device_obj.managementIP
            promptServer=device_obj.promptServer
            cmd = "ipmitool -I lanplus -H %s -U root -P 0penBmc -C 17 lan set 1 netmask %s" % (mgmt_ip, netmask)
        else:
            cmd = r" ipmitool lan set 1 netmask %s" % (netmask)
        output2=device_obj.executeCmd(cmd) 
        pattern="Setting LAN Subnet Mask to %s" %netmask
        CommonKeywords.should_match_a_regexp(output2,pattern)
        log.success("Subnet Mask is updated via ipmitool lan command successfully.")
        
        
def set_bmc_ip_status(device, ip_status, lanplus=False):
    ip_status = ip_status.lower()
    if ip_status not in ["dhcp", "static"]:
        PRINTE("Fail! set_bmc_ip_status parameter must be 'dhcp' or 'static'")
    ip_status = "static" if ip_status.lower() == "static" else "dhcp"
    device_obj = Device.getDeviceObject(device)
    
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd = "ipmitool -I lanplus -H %s -U root -P 0penBmc -C 17 lan set 1 ipsrc %s" % (mgmt_ip, ip_status)
    else:
        cmd = "ipmitool lan set 1 ipsrc %s" % ip_status
    output=device_obj.executeCmd(cmd) 
    
    if re.findall(r"rror|Fail|fail|invalid", output):
        raise RuntimeError("Unable to set lan ip status!!")
    else:
        log.success("IP status %s is being set successfully through ipmitool lan command" %ip_status)
    if(ip_status=='dhcp'):
        log.info("Sleeping for 120 seconds to recieve dynamic ip through dhcp protocol.")
        time.sleep(120)
		
   
def check_lan_print_info(device, exp_ip_addr=None, exp_ip_status=None, exp_mac_addr=None, exp_subnet_mask=None, lanplus=False):
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd = "ipmitool -I lanplus -H %s -U root -P 0penBmc -C 17 lan print 1" % mgmt_ip
    else:
        cmd = "ipmitool lan print 1"
    res = device_obj.executeCmd(cmd) 
    ip_status = re.findall(r"IP Address Source\s+:\s+(.*)", res)[0]
    ip_address = re.findall(r"IP Address\s+:\s+(\d+\..*\d+)", res)[0]
    mac_address = re.findall(r'MAC Address\s+:\s+((?:[0-9a-fA-F]:?){12})', res)[0]
    subnet_mask = re.findall(r"Subnet Mask\s+:\s+(\d+\..*\d+)", res)[0]
    log.cprint(ip_status)
    log.cprint(ip_address)
    log.cprint(mac_address)
    log.cprint(subnet_mask)
    
    flag=False
    if(exp_ip_status!=None):
        if exp_ip_status in ip_status: 
            log.success("Actual and Expected IP Status Matched in lan print 1")
        else:
            flag=True
            log.fail("IP status mismatched!! Expected IP Status should be %s but got %s." %(exp_ip_status, ip_status))
            
    if(exp_ip_addr!=None):
        if exp_ip_addr in ip_address: 
            log.success("Actual and Expected IP address Matched in lan print 1")
        else:
            flag=True
            log.fail("IP address mismatched!! Expected IP address should be %s but got %s." %(exp_ip_addr, ip_address))
            
    if(exp_mac_addr!=None):
        if exp_mac_addr in mac_address: 
            log.success("Actual and Expected Mac address Matched in lan print 1")
        else:
            flag=True
            log.fail("Mac address mismatched!! Expected Mac address should be %s but got %s." %(exp_mac_addr, mac_address))
            
    if(exp_subnet_mask!=None):
        if exp_subnet_mask in subnet_mask: 
            log.success("Actual and Expected Subnet mask Matched in lan print 1")
        else:
            flag=True
            log.fail("Subnet mask mismatched!! Expected Subnet mask should be %s but got %s." %(exp_subnet_mask, subnet_mask))
            
    if flag:
        raise RuntimeError("Expected and actual lan print information mismatched!!")
        
        
# TC - BMC Memory Test
def check_memory_status(bmc_memory_pattern):
    cmd = "ipmitool raw 0x3a 0x2c 0x02"
    output = run_command(cmd)
    flag=False
    log.cprint(output)
    if bmc_memory_pattern not in output:
        log.fail("Expected status does not match")
    else:
        log.success("Memory is correct")

	
def enable_bmc_memory():
    cmd = "ipmitool raw 0x3a 0x2c 0x01"
    output = run_command(cmd)
    log.cprint(output)
    if re.findall(r"rror|Fail|fail|invalid", output):
        log.fail("BMC Memory enable command failed!!")
    else:
        log.success("BMC Memory enable command executed successfully")
	
 
def disable_bmc_memory():
    cmd = "ipmitool raw 0x3a 0x2c 0x00"
    output = run_command(cmd)
    log.cprint(output)
    if re.findall(r"rror|Fail|fail|invalid", output):
        log.fail("BMC Memory disable command failed!!")
    else:
        log.success("BMC Memory disable command executed successfully")

# TC - BMC MAC Address test

def get_fru1_mac(device):
    cmd = r"ipmitool fru print 1"
    device_obj = Device.getDeviceObject(device)
    res = device_obj.executeCmd(cmd)
    board_list = re.findall(r"Board Extra\s+:\s+(.*)\n", res)
    if len(board_list) < 2:
        PRINTE("Fail! [%s] Insufficient information. Response:\n%s" % (cmd, res))
    return board_list[1].strip()


def set_fru1_mac(device, mac_address):
    device_obj = Device.getDeviceObject(device)
    previous_fru_mac = get_fru1_mac(device)
    
    cmd = r"ipmitool fru edit 1 field b 6 %s" % mac_address
    res = device_obj.executeCmd(cmd)
    
    pattern = "Updating Field '"+previous_fru_mac+"' with '"+mac_address+"' ..."
    CommonKeywords.should_match_a_regexp(res, pattern)
    log.success("Success!! new mac address %s is edited through ipmitool successfully." %mac_address)
    
    cmd2="ipmitool raw 0x06 0x02"
    output=device_obj.executeCmd(cmd2)
    if re.findall(r"rror|Fail|fail|invalid", output):
        raise RuntimeError("Error in executing command '%s'" %cmd)
    log.info("Sleeping for 200 seconds to update new mac address in bmc.")
    time.sleep(200)
    
    
def check_mac_in_lan_and_fru(device, fru_mac_add, lan_mac_add):
    log.info("Checking MAC address in ipmitool lan print 1.")
    check_lan_print_info(device,  exp_mac_addr=lan_mac_add)
    
    log.info("Checking MAC address in ipmitool fru print 1.")
    actual_fru_mac = get_fru1_mac(device)
    if actual_fru_mac==fru_mac_add:
        log.success("Successful, MAC address in fru info is as expected.")
    else:
        raise RuntimeError("Expected Mac address %s but got %s in fru information" %(fru_mac_add, lan_mac_add))
    

# TC - User Operation Test
      
def check_add_single_user(device, user_id, user_name, possible=True):
    device_obj = Device.getDeviceObject(device)
    cmd = "ipmitool user set name %s %s" %(str(user_id), user_name)
    res = device_obj.executeCmd(cmd)
    if not possible:
       pattern = "Set User Name command failed (user %s, name %s): Invalid data field in request" %(str(user_id), user_name)
       if pattern in res:
           log.success("Can not add user %s with invalid user id %s" %(user_name, str(user_id)))
       else:
           raise RuntimeError("This user id %s should not be added according to specifications")
    else:
    
        if re.findall(r"rror|Fail|fail|invalid", res):
            raise RuntimeError("User id %s with user name %s is unable to add in ipmitool user list" %s(str(user_id), user_name))
        user_list_pattern = "%s\s+%s\s+true\s+false\s+false\s+NO ACCESS" %(str(user_id), user_name)
        output=device_obj.executeCmd(cmd_ipmitool_user_list_1)
        CommonKeywords.should_match_a_regexp(output, user_list_pattern)
        log.success("User with user id %s and user name %s added successfully." %(str(user_id), user_name))
    
      
def check_default_user_list(device):
    device_obj = Device.getDeviceObject(device)
    res = device_obj.executeCmd(cmd_ipmitool_user_list_1)
    CommonKeywords.should_match_paired_regexp_list(res,bmc_default_user_list)
    log.success("Success! Default user list is a s expected.")
    
    
def set_user_password(device, user_id, user_pass, length):
    device_obj = Device.getDeviceObject(device)
    cmd = "ipmitool user set password %s %s %s" %(str(user_id), user_pass, str(length))  
    res = device_obj.executeCmd(cmd)
    pattern = r"Set User Password command successful.*%s" %str(user_id)
    log.cprint(res)
    CommonKeywords.should_match_a_regexp(res, pattern)
    log.success("Password is set successfully for user %s" %str(user_id))
    
    
def test_user_password(device, user_id, correct_pass, incorrect_pass, len16=False, len20=False):  
    device_obj = Device.getDeviceObject(device)
    cmd1 = "ipmitool user test %s 16 %s" %(str(user_id), correct_pass)
    cmd2 = "ipmitool user test %s 16 %s" %(str(user_id), incorrect_pass)
    cmd3 = "ipmitool user test %s 20 %s" %(str(user_id), correct_pass)
    cmd4 = "ipmitool user test %s 20 %s" %(str(user_id), incorrect_pass)
    
    res1 = device_obj.executeCmd(cmd1)
    res2 = device_obj.executeCmd(cmd2)
    res3 = device_obj.executeCmd(cmd3)
    res4 = device_obj.executeCmd(cmd4)
    
    if(len16):
        log.info("Testing password for length 16 bytes")
        CommonKeywords.should_match_a_regexp(res1, success_pass)
        log.success("Password matched.")
        CommonKeywords.should_match_a_regexp(res2, error_pass_incorrect)
        log.success("Password mismatched")
        CommonKeywords.should_match_a_regexp(res3, error_pass_size)
        log.success("Password length is not 16 byte hence wrong.")
        CommonKeywords.should_match_a_regexp(res4, error_pass_size)
        log.success("Password length is not 16 byte hence wrong. ")
    else:
        log.info("Testing password for length 20 bytes")
        CommonKeywords.should_match_a_regexp(res1, error_pass_size)
        log.success("Password length is not 20 byte hence wrong. ")
        CommonKeywords.should_match_a_regexp(res2, error_pass_size)
        log.success("Password length is not 20 byte hence wrong. ")
        CommonKeywords.should_match_a_regexp(res3, success_pass)
        log.success("Password mismatched")
        CommonKeywords.should_match_a_regexp(res4, error_pass_incorrect)
        log.success("Password matched")
        
        
def enable_user_and_ipmi_message(device, user_id, user_name):  
    device_obj = Device.getDeviceObject(device)
    cmd1="ipmitool user enable %s" %str(user_id)
    cmd2="ipmitool raw 0x06 0x43 0x91 %s 4" %str(user_id)
    
    res1=device_obj.executeCmd(cmd1)
    if re.findall(r"rror|Fail|fail|invalid", res1):
        raise RuntimeError("User id %s is unable to execuete '%s' command" %(str(user_id), cmd1))
        
    res2=device_obj.executeCmd(cmd2)
    if re.findall(r"rror|Fail|fail|invalid", res2):
        raise RuntimeError("User id %s is unable to execuete '%s' command" %(str(user_id), cmd2))
        
    user_list_pattern = "%s\s+%s\s+true\s+false\s+true\s+ADMINISTRATOR" %(str(user_id), user_name)
    output=device_obj.executeCmd(cmd_ipmitool_user_list_1)
    CommonKeywords.should_match_a_regexp(output, user_list_pattern)
    log.success("User with user id %s and user name %s has changed its priviledge to ADMINISTRATOR successfully." %(str(user_id), user_name))
    

def check_lanplus_communication_through_user(device, user_id, user_name, user_pass):
    device_obj = Device.getDeviceObject(device)
    MOONSTONECommonLib.check_server_moonstone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    cmd1 = 'ipmitool -I lanplus -H '+ mgmt_ip + ' -U '+user_name+' -P '+ str(user_pass) +' mc info'
    cmd2 = 'ipmitool -I lanplus -H '+ mgmt_ip + ' -U '+user_name+' -P '+ str(user_pass) +' user list 1'
    
    res1=device_obj.executeCmd(cmd1)
    CommonKeywords.should_match_paired_regexp_list(res1,bmc_version_info_list)
    log.success("BMC version info is verified through a new user %s with administrator access." %user_name)
    
    res2=device_obj.executeCmd(cmd2)
    user_list_pattern = "%s\s+%s\s+true\s+false\s+true\s+ADMINISTRATOR" %(str(user_id), user_name)
    CommonKeywords.should_match_a_regexp(res2, user_list_pattern)
    log.success("User list is verified with new user % having administrator access" %user_name)
    
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")
    
    
def check_add_all_users(device, start_id, end_id):
    device_obj = Device.getDeviceObject(device)
    for user_id in range(int(start_id), int(end_id)+1):
        cmd = "ipmitool user set name %s user_%s" %(str(user_id), str(user_id))
        res = device_obj.executeCmd(cmd)
        if re.findall(r"rror|Fail|fail|invalid", res):
            raise RuntimeError("User id %s with user name user_%s is unable to add in ipmitool user list" %s(str(user_id), str(user_id)))
            
    output=device_obj.executeCmd(cmd_ipmitool_user_list_1)
    for user_id in range(int(start_id), int(end_id)+1): 
        user_list_pattern = "%s\s+user_%s\s+true\s+false\s+false\s+NO ACCESS" %(str(user_id), str(user_id))
        CommonKeywords.should_match_a_regexp(output, user_list_pattern)
        
    log.success("All new users are added successfully in ipmitool user list.")
    
    
def delete_all_new_user_info(device):
    device_obj = Device.getDeviceObject(device)
    error_info = "Unable to send command: Invalid argument"
    for user_id in range(3,16):
        cmd = "ipmitool raw 6 0x45 %s 0xff 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0" % str(user_id)
        res = run_command(cmd)
        if error_info in res:
            raise RuntimeError("Unable to delete user information at user id %s" %str(user_id))
    log.info("Command to delete new users from ipmitool executed successfully.")
    check_default_user_list(device)
    log.success("Successfully deleted user information from user id 3 to 15.")   
     
       
# TC - User Priviledge test

def check_user_priviledge_lanplus_communication(device, user_id, user_name, user_pass, user_priv):
    device_obj = Device.getDeviceObject(device)
    MOONSTONECommonLib.check_server_moonstone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    
    priv=["ADMINISTRATOR", "OPERATOR", "USER"]
    for val in priv:
        cmd1 = 'ipmitool -I lanplus -H '+ mgmt_ip + ' -U '+user_name+' -P '+ str(user_pass) +' -L '+ val+' chassis power status'
        
        higher_priv_error="Set Session Privilege Level to %s failed" %val
        res1 = device_obj.executeCmd(cmd1)
        
        if user_priv=='OPERATOR' and val=='ADMINISTRATOR' :
            CommonKeywords.should_match_a_regexp(res1, higher_priv_error)
            log.success("User %s with %s privileged can not access bmc through %s priviledge access" %(user_name, user_priv, val))
            
        elif user_priv=='USER' and (val=='ADMINISTRATOR' or val=='OPERATOR'):
            CommonKeywords.should_match_a_regexp(res1, higher_priv_error)
            log.success("User %s with %s privileged can not access bmc through %s priviledge access" %(user_name, user_priv, val))
        else :   
            CommonKeywords.should_match_a_regexp(res1, chassis_status_pattern)
            log.success("Successfully able to communicate to lanplus command for chassis power status through user %s with %s priviledge" 
            %(user_name, user_priv))
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")
        

def check_set_user_priviledge(device, user_id, user_name, user_pass):
    device_obj = Device.getDeviceObject(device)
    cmd='ipmitool user enable %s' %user_id
    res=device_obj.executeCmd(cmd)
    if re.findall(r"rror|Fail|fail|invalid", res):
        raise RuntimeError("Not able to use 'ipmitool user enable' command for user_id %s" %user_id)
        
    priv_dict = {"ADMINISTRATOR":"4", "OPERATOR":"3", "USER":"2"}
    for key,value in priv_dict.items():
        priviledge_cmd = "ipmitool raw 0x06 0x43 0x91 %s %s" %(user_id, value)
    
        res =  device_obj.executeCmd(priviledge_cmd)
        if re.findall(r"rror|Fail|fail|invalid", res):
            raise RuntimeError("Unable to give %s access to user_id %s" %(key,user_id))
        pattern = "%s\s+%s\s+true\s+false\s+true\s+%s" %(user_id, user_name, key)
        user_list_output = device_obj.executeCmd(cmd_ipmitool_user_list_1)
        CommonKeywords.should_match_a_regexp(user_list_output, pattern)
        log.success("Successfully updated priviledge access to %s for user_id %s" %(key, user_id))
        log.info("Trying to access lanplus command through %s priviledge access of user_id %s" %(key, user_id) )
        check_user_priviledge_lanplus_communication(device, user_id, user_name, user_pass, key)
    
    log.success("Successfully, verified priviledge modes on user_id %s" %user_id)
      
      
# TC - BMC Console Baudrate Setting

def check_set_baurd_rate(device, end_baurd_rate, start_baurd_rate):
    device_obj = Device.getDeviceObject(device)
    
    for baurd in range(int(end_baurd_rate), int(start_baurd_rate)-1, -1):
      MOONSTONECommonLib.check_server_moonstone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
      write_baurd_cmd=lanplus_ipmitool_cmd.format("raw 0x3a 0x23 0x01 0x0%s" %str(baurd))
      read_baurd_cmd=lanplus_ipmitool_cmd.format("raw 0x3a 0x23 0x00")
      
      log.info("Updating Baurd rate of device to 0x0%s" %str(baurd))
      res=device_obj.executeCmd(write_baurd_cmd)
      log.cprint(res)
      if re.findall(r"rror|Fail|fail|invalid", res):
          raise RuntimeError("Unable to update baurd rate.")
      else:
          log.success("Successfully, updated braud rate to 0x0%s" %str(baurd))
          
      log.info("Reading Baurd rate of device.")
      output=device_obj.executeCmd(read_baurd_cmd)
      output=output.split("\n")[1].strip()
      log.cprint(output)
      baurd_rate = "0"+str(baurd)
      if baurd_rate not in output:
          raise RuntimeError("Expected baurd rate should be %s but got %s" %(baurd_rate, output))
      else:
          log.success("Successfully, verified new baurd_rate '%s' through read operation." %(baurd_rate))
      
      log.info("Exiting from server..")
      device_obj.sendCmd("exit")
      
      log.info("Reset bmc cold after updating baurd rate to %s" %str(baurd))
      bmc_reset(device, "cold")
      log.success("Successfully able to reset cold and get back to required prompt.")

    
#TC - BMC SOL Configuration Test

def set_and_check_sol_configuration(device, parameter, value):
    device_obj = Device.getDeviceObject(device)
    cmd1 = lanplus_ipmitool_cmd.format("sol set %s %s 1" %(parameter, value))
    promptServer=device_obj.promptServer
    res=device_obj.executeCmd(cmd1)
    log.cprint(res)
    log.info("Setting Sol parameter %s with %s value" %(parameter, value))
    if re.findall(r"rror|Fail|fail|invalid", res):
          raise RuntimeError("Unable to update sol information through cmd %s" %cmd1)
    check_sol_configuration(device, parameter, value)
    
    
def check_default_sol_configuration(device):
    device_obj = Device.getDeviceObject(device)
    cmd2 = lanplus_ipmitool_cmd.format("sol info 1")
    promptServer=device_obj.promptServer
    res=device_obj.executeCmd(cmd2)
    log.cprint(res)
    CommonKeywords.should_match_ordered_regexp_list(res,sol_default_pattern)
    log.success("Successful, Sol configuration parameters are set with their default values.")
    
    
def check_sol_configuration(device, parameter, value):
    device_obj = Device.getDeviceObject(device)
    cmd2 = lanplus_ipmitool_cmd.format("sol info 1")
    promptServer=device_obj.promptServer
    res=device_obj.executeCmd(cmd2)
    log.cprint(res)
    sol_info_pattern = r"%s.*:\s+(.*)\n" %sol_info_dict[parameter]
    match = re.findall(sol_info_pattern, res)[0].strip()
    if value not in match:
        raise RuntimeError("Expected value of %s should be %s but got %s" %(sol_info_dict[parameter], value, match))
    else:
        log.success("Successfully changed value of %s to %s " %(sol_info_dict[parameter], value))
    
    
# TC - KCS Interface Test

def set_modprobe(device):
    device_obj = Device.getDeviceObject(device)
    cmd1="modprobe ipmi_si"
    cmd2="modprobe ipmi_devintf"
    res1=device_obj.executeCmd(cmd1)
    res2=device_obj.executeCmd(cmd2)
    if re.findall(r"rror|Fail|fail|invalid", res1):
          raise RuntimeError("Unable to execute cmd %s" %cmd1)
    if re.findall(r"rror|Fail|fail|invalid", res2):
          raise RuntimeError("Unable to execute cmd %s" %cmd2)
    log.success("Successfully executed modeprobe commands")
    
    
def initialize_kcs_interface(device):
    device_obj = Device.getDeviceObject(device)
    cmd1 = "dmesg | grep ipmi"
    kcs_pattern = r"kcs interface initialized"
    res = device_obj.executeCmd(cmd1)
    CommonKeywords.should_match_a_regexp(res,kcs_pattern)
    log.success("Successful, System can communicate with BMC with default KCS port 0xca0")

    
def clear_sel_list(device, lanplus=False):
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd1 = lanplus_ipmitool_cmd.format("sel clear")
        cmd2 = lanplus_ipmitool_cmd.format("sel list")
    else:
        cmd1 = "ipmitool sel clear"
        cmd2 = "ipmitool sel list"
    res1 = device_obj.executeCmd(cmd1)
    CommonKeywords.should_match_a_regexp(res1,sel_clear_pattern)
    res2 = device_obj.executeCmd(cmd2)
    CommonKeywords.should_match_a_regexp(res2,sel_list_after_clear_pattern)
    log.success("Sel list is cleared successfully.")
    
    
def ipmitool_self_test(device, lanplus=False):
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd = lanplus_ipmitool_cmd.format("raw 6 4")
    else:
        cmd = "ipmitool raw 6 4"
    res = device_obj.executeCmd(cmd)
    CommonKeywords.should_match_a_regexp(res,self_test_pattern)
    log.success("Successfully verified ipmitool self test command '%s' " %cmd)
    

def boot_bios_through_ipmitool_raw(device):
    device_obj = Device.getDeviceObject(device)
    cmd1="ipmitool chassis bootdev bios"
    res1 = device_obj.executeCmd(cmd1)
    boot_device_pattern = "Set Boot Device to bios"
    CommonKeywords.should_match_a_regexp(res1,boot_device_pattern)
    
    log.info("Boot bios dut..")
    cmd2="ipmitool raw 0 2 3"
    device_obj.sendCmd(cmd2)
    pattern="Boot from Primary BIOS"
    device_obj.read_until_regexp(pattern, timeout=100)
    time.sleep(30)
    bios_menu_lib.send_key(device, "KEY_ESC")

    time.sleep(5)
    bios_menu_lib.send_key(device, "KEY_ENTER",2)
    log.info("Primary Bios Booting started")
    device_obj.read_until_regexp("localhost login:.*", timeout=200)
    device_obj.loginToDiagOS()
    log.success("Bios Boot through ipmitool is executed successfully")
    

# TC - Online Update through LAN

def check_bmc_firmware_revision(device, version, lanplus=False):  
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd = lanplus_ipmitool_cmd.format("mc info")
    else:
        cmd = "ipmitool mc info"
    res=device_obj.executeCmd(cmd)
    # log.cprint(res)
    pattern="Firmware Revision         : {}".format(version)
    CommonKeywords.should_match_a_regexp(res,pattern)
    log.success("BMC firmware revision is as expected : %s" %version)
    
    
def update_primary_bmc(device, image):
    device_obj = Device.getDeviceObject(device)
    promptServer=device_obj.promptServer
    
    log.info("Copy bmc image file..")
    copy_bmc_image_cmd="scp "+ image_path_in_server + image + " root@" + mgmt_ip + ":" + image_path_in_bmc + "image-bmc"
    device_obj.sendCmd(copy_bmc_image_cmd, timeout=90)
    c1 = device_obj.read_until_regexp(r'password:', timeout=90)
    device_obj.sendCmd("0penBmc", timeout=90)
    c2 = device_obj.read_until_regexp(promptServer, timeout=90)
    
    if re.findall(r"rror|Fail|fail|invalid", c2) or (not r"100%" in c2):
        raise RuntimeError("Error in copying BMC image")
    else:
        log.success("Successfully copied BMC image.")
    time.sleep(5)
    log.info("Reboot BMC (using mc reset cold)")
    bmc_reset(device, "cold", lanplus=True, sleep=500)
    # if(reset_firmware_pattern in c2):
        # log.info("Sleeping for 200 seconds for BMC to come up after bmc update")
        # time.sleep(200)
        
    # log.info("Check sel list after updation.")
    # flag = check_sel_list_info(device, sel_list_pattern=sel_list_after_updating_image, lanplus=True)
    # if flag:
        # log.info("Sel list is cleared after updation of image")
    # else:
        # raise RuntimeError("Sel list is not empty yet")
        

# TC Clear CMOS by IPMI
def clear_cmos_by_ipmi_lanplus(device):
    cmd = lanplus_ipmitool_cmd.format("chassis bootdev disk clear-cmos=yes")
    device_obj = Device.getDeviceObject(device)
    c1=Device.execute_local_cmd(device_obj, cmd)
    log.info(c1)
    if re.findall(r"rror|Fail|fail|invalid", c1):
          raise RuntimeError("Unable to clear CMOS through cmd %s" %cmd)
    else:
        log.success("Successfully cleared CMOS by IPMI")
    
    
    
# TC Power Chassis test

def check_power_chasis_status(device, status):
    device_obj = Device.getDeviceObject(device)
    mgmt_ip = device_obj.managementIP 
    promptServer=device_obj.promptServer
    cmd=lanplus_ipmitool_cmd.format('chassis power status')
    log.info("Checking chassis status through cmd : %s" %cmd)
    c1=Device.execute_local_cmd(device_obj, cmd)
    log.info("Output : "+c1)
    
    chassis_pattern = "Chassis Power is %s" %status
    if chassis_pattern in c1:
        log.info("Chassis Status is as expected!! "+chassis_pattern)
    else:
        raise RuntimeError("Expected value of Chassis Status should be %s but got opposite of it." %status)
        

def set_power_chasis(device, status):
    device_obj = Device.getDeviceObject(device)
    mgmt_ip = device_obj.managementIP
    promptServer=device_obj.promptServer
    cmd = lanplus_ipmitool_cmd.format("power %s" %status)
    
    log.info("Turn %s power through cmd %s" %(status, cmd))
    c1=Device.execute_local_cmd(device_obj, cmd)
    log.info('Output : '+c1)
    
    val = "Down/Off" if status == 'off' else "Up/On"
    pattern = "Chassis Power Control: %s" %val
    
    log.info("Sleeping for 10 seconds.")
    time.sleep(10)
    
    CommonKeywords.should_match_a_regexp(c1,pattern)
    if(status=='on'):
        log.info("Sleeping for 150 seconds.")
        time.sleep(150)
        # log.info("Login into device")
        # device_obj.loginToDiagOS()
        # sel_list_pattern=sel_list_power_on_pattern
        # sel_cmd = lanplus_ipmitool_cmd.format('sel list | tail')
        # log.info("Fetching BMC sel list after setting power chassis status")
        # c2=Device.execute_local_cmd(device_obj, sel_cmd, timeout=120)
        # log.info("Output : "+c2)
        # c2=c2.split("\n")
        # c2=c2[-3:]
        # log.cprint(c2)
        # log.cprint("next line" )
        # log.cprint(sel_list_pattern)
        # CommonKeywords.should_match_ordered_regexp_list(c2,sel_list_pattern)
        # log.success("Sel list is as expected after power %s" %status)
    

def power_cycle_and_login(device):
    device_obj = Device.getDeviceObject(device)
    MOONSTONECommonLib.powercycle_device(device)
    log.info("Login into device")
    device_obj.loginToDiagOS()

        
# TC - Extensional read write


def write_data_to_bus(device):
    device_obj = Device.getDeviceObject(device)
    cmd = 'ipmitool raw 0x3a 0x3e 0x02 0xae 0x03 0 0 0xaa 0xbb 0xcc'
    res = device_obj.executeCmd(cmd)
    if re.findall(r"rror|Fail|fail|invalid", res):
          raise RuntimeError("Unable to write data to bus 2 through cmd %s" %cmd)
    else:
        log.success("Successfully write data to bus 2 through cmd %s" %cmd)
        

def read_data_from_bus(device):
    device_obj = Device.getDeviceObject(device)
    cmd="ipmitool raw 0x3a 0x3e 0x02 0xae 0x03 0 0"
    res = device_obj.executeCmd(cmd)
    if re.findall(r"rror|Fail|fail|invalid", res):
          raise RuntimeError("Unable to read data to bus 2 through cmd %s" %cmd)
    else:
        log.success("Successfully read data to bus 2 through cmd %s" %cmd)
    
    
def read_data_with_invalid_length(device):
    device_obj = Device.getDeviceObject(device)
    cmd="ipmitool raw 0x3a 0x3e 0x02 0xae"
    res = device_obj.executeCmd(cmd)
    pattern = "Unable to send RAW command.*rsp=0xc7.*Request data length invalid"
    CommonKeywords.should_match_a_regexp(res,pattern)
    log.success("Can not read data with invalid data length")
       
    
    
# TC - FRU Acces Test

def check_fru_list(device):
    device_obj = Device.getDeviceObject(device)
    cmd = "ipmitool fru list"
    res = device_obj.executeCmd(cmd)
    CommonKeywords.should_match_ordered_regexp_list(res,fru_list_pattern)
    log.success("All fru devices are according to specifications.")
    
    
def execute_fru_eeprom_bin_sh(device):
    device_obj = Device.getDeviceObject(device)
    device_obj.executeCmd("cd")
    path = "cd diag/home/cel_diag/moonstone2/firmware/fru_eeprom/"
    device_obj.executeCmd(path)
    res=device_obj.executeCmd("./bin_produce.sh")
    if re.findall(r"rror|Fail|fail|invalid", res):
        raise RuntimeError("Unable to update FRU devices through bin_produce sh file")
    else:
        log.success("FRU devices are updated sucessfully through bin_produce sh file")
    
    device_obj.executeCmd("cd bin")
    bin_lst = ["bmc.bin",   "fan1/.bin",  "fan3/.bin",  "switch/.bin", "come.bin",  "fan2/.bin",  "fan4/.bin",  "system/.bin"]
    for item in bin_lst:
        cmd = "hexdump -C %s" %item
        device_obj.executeCmd(cmd)
        if re.findall(r"rror|Fail|fail|invalid", res):
            raise RuntimeError("Unable to read %s" %item)
        else:
            log.success("Successful read %s file" %item)
   
    
def check_fru_size(device):
    device_obj = Device.getDeviceObject(device)
    fru_size = ["00 20 00","00 04 00"]
    for item in range(10):
        cmd = "ipmitool raw 0x0a 0x10 0x0%s" %str(item)
        res = device_obj.executeCmd(cmd)
        CommonKeywords.should_match_one_of_regexp_list(res, fru_size)
        log.success("FRU size for id %s is %s" %(str(item), res))
        
    
def update_fru_data(device, id_):
    device_obj = Device.getDeviceObject(device)
    
    # disable fru write
    cmd1 = "ipmitool raw 0x3a 0x61 0x0%s 0x00" %str(id_)
    # fru print
    cmd2 = "ipmitool fru print %s" %str(id_)
    # read fan3
    cmd3 = "ipmitool raw 0x0a 0x11 0x0%s 0x20 0x00 0xff" %str(id_)
    # write fan3
    cmd4 = "ipmitool raw 0x0a 0x12 %s 0 0 0x01 0x02 0x03 0x4" %str(id_)
    
    
    log.info("Disable fru write protection for device %s" %str(id_))
    res1 = device_obj.executeCmd(cmd1)
    if re.findall(r"rror|Fail|fail|invalid", res1):
        raise RuntimeError("Unable to disable fru write protection " )
    else:
        log.success("Successful disabled fru write protection for device %s" %str(fru_device_name[int(id_)]))
    
    log.info("Read FRU data through raw command")
    res3 = device_obj.executeCmd(cmd3)
    if re.findall(r"rror|Fail|fail|invalid", res3):
        raise RuntimeError("Unable to read %s" %str(id_))
    else:
        log.success("Successful read %s file" %str(id_))
        
    log.info("Writing to device %s" %str(id_))
    res4 = device_obj.executeCmd(cmd4)
    CommonKeywords.should_match_a_regexp(res4,"04")
    log.success("Successfully wrote to fru device %s" %(id_))
    
    log.info("FRU print for device %s" %str(id_))
    res5 = device_obj.executeCmd(cmd2)
    
    write_fru_through_diag(device, id_)
    
    log.info("FRU print for device %s" %str(id_))
    res5 = device_obj.executeCmd(cmd2)
    log.success("FRU print is as expected")
    
    
def update_date_and_mfg_name(device, id_):
    device_obj = Device.getDeviceObject(device)
    # disable fru write
    cmd1 = "ipmitool raw 0x3a 0x61 0x0%s 0x00" %str(id_)
    # date change
    cmd2 = "ipmitool raw 0x0a 0x12 0x00 0x00 0x00 0xaa 0xbb 0xcc 0xdd"
    # get date
    cmd3 = "ipmitool raw 0x0a 0x11 0x00 0x00 0x00 0x04"
    # fru print
    cmd4 = "ipmitool fru print %s" %str(id_)
    # name change
    cmd5 = 'ipmitool fru edit 0 field b 0 "CelesticaTest"'
    
    log.info("Disable fru write protection for device %s" %str(id_))
    res1 = device_obj.executeCmd(cmd1)
    if re.findall(r"rror|Fail|fail|invalid", res1):
        raise RuntimeError("Unable to disable fru write protection " )
    else:
        log.success("Successful disabled fru write protection for device %s" %str(fru_device_name[int(id_)]))
    
    log.info("Change date of device %s through ipmi tool raw cmd : %s" %(str(fru_device_name[int(id_)]), cmd1))
    res2 = device_obj.executeCmd(cmd2)
    CommonKeywords.should_match_a_regexp(res2,"04")
    log.success("Successfully write new date to fru device %s" %(id_))
    
    log.info("Validate date changed for device %s" %str(fru_device_name[int(id_)]))
    res3 = device_obj.executeCmd(cmd3)
    device_obj.executeCmd("ipmitool raw 0x0a 0x12 0x00 0x00 0x00 0x01 0x02 0x03 0x041")
    date_pattern = "04 aa bb cc dd"
    CommonKeywords.should_match_a_regexp(res3,date_pattern)
    log.success("Successfully changed to new date in fru device %s" %(id_))
    
    log.info("Updating mfg name field for device %s" %str(fru_device_name[int(id_)]))
    res4 = device_obj.executeCmd(cmd5)
    mfg_pattern = "Updating Field.*with.*CelesticaTest"
    CommonKeywords.should_match_a_regexp(res4, mfg_pattern)
    log.success("Field gets updated successfully.")
    
    log.info("FRU print for device %s" %str(id_))
    res5 = device_obj.executeCmd(cmd4)
    mfg_pattern = ["Board Mfg Date.*2027","Board Mfg.*CelesticaTest"]
    CommonKeywords.should_match_ordered_regexp_list(res5, mfg_pattern)
    log.success("Date and Name gets updated properly for fru device %s" %str(id_))
    
    write_fru_through_diag(device, id_)
    
    log.info("FRU print for device %s" %str(id_))
    res7 = device_obj.executeCmd(cmd4)
    
    
def write_fru_through_diag(device, id_):
    device_obj = Device.getDeviceObject(device)
    cmd = "./cel-eeprom-bmc-test -w -t %s" %str(fru_device_name[int(id_)])
    
    log.info("Update the writen information into device %s "%(str(id_)))
    device_obj.executeCmd("cd")
    device_obj.executeCmd("cd diag/home/cel_diag/moonstone2/bin")
    res1 = device_obj.executeCmd(cmd)
    write_pattern = "Result.*Passed"
    CommonKeywords.should_match_a_regexp(res1,write_pattern)
    log.success("Date and Name gets updated properly for fru device %s" %str(id_))
    
    
def reset_fru_device_to_default(device, device1, device2):
    device_obj = Device.getDeviceObject(device)
    write_fru_through_diag(device, str(device1))
    write_fru_through_diag(device, str(device2))
    device_obj.executeCmd("cd")

def copy_bios_image_from_server_via_scp(device, image):
    device_obj = Device.getDeviceObject(device)
    promptServer=device_obj.promptServer

    log.info("Copy bios image file..")
    copy_bios_image_cmd="scp {}{} root@{}:{}".format(image_path_in_server, image, mgmt_ip, image_path_in_bmc)
    device_obj.sendCmd(copy_bios_image_cmd, timeout=90)
    c1 = device_obj.read_until_regexp(r'password:', timeout=90)
    device_obj.sendCmd("0penBmc", timeout=90)
    c2 = device_obj.read_until_regexp(promptServer, timeout=90)
    if re.findall(r"rror|Fail|fail|invalid", c2) or (not r"100%" in c2):
        raise RuntimeError("Error in copying BIOS image")
    else:
        log.success("Successfully copied BIOS image.")
    time.sleep(5)



# TC - Bios update via lan
def update_bios_image(device, image, boot_type, lanplus=False):
    device_obj = Device.getDeviceObject(device)

    mse='primary' if str(boot_type)=='0' else 'secondary'

    update_bios_cmd="/usr/bin/bmcbiosflash.sh {}{} {}".format(image_path_in_bmc, image, mse)
    log.info("Updating %s bios with image %s" %(mse, image))
    
    c1 = device_obj.executeCmd(update_bios_cmd, timeout=300)
    # if not re.findall(r"rror|Fail|fail|invalid", c1):
        # log.success("Bios is updated through command : %s" %update_bios_cmd)
    # else:
        # raise RuntimeError("Some error found while updating bios")
    if str(boot_type)=='0':
        CommonKeywords.should_match_a_regexp(c1, "Program Primary BIOS Successful!")
        log.success("Primary BIOS Image is updated")
    else:
        CommonKeywords.should_match_a_regexp(c1, "Program Secondary BIOS Successful!")
        log.success("Backup BIOS Image is updated")

    remove_bios_image_cmd="rm {}{}".format(image_path_in_bmc, image)
    log.info("Removing %s from %s" %(image, image_path_in_bmc))
    
    c2 = device_obj.executeCmd(remove_bios_image_cmd, timeout=60)
    if not re.findall(r"rror|Fail|fail|invalid", c2):
        log.success("Bios image is deleted through command : %s" %remove_bios_image_cmd)
    else:
        raise RuntimeError("Some error found while deleting bios image")

    log.info("power cycle from BMC console")
    cmd = "ipmitool power cycle"
    out=device_obj.executeCmd(cmd, timeout=300)
    pattern = "Chassis Power Control: Cycle"
    CommonKeywords.should_match_a_regexp(out,pattern)

    log.info("Sleeping for 200 seconds for COMe reboot.")
    time.sleep(200)
    cmd = "ipmitool power status"
    out=device_obj.executeCmd(cmd, timeout=300)
    pattern = "Chassis Power is on"
    CommonKeywords.should_match_a_regexp(out,pattern)
    log.success("Power cycle from BMC console passed")

    log.success("Bios is updated successfully with image %s ." %image)
    
    
def bios_boot(device, boot_type):
    device_obj = Device.getDeviceObject(device)
    if str(boot_type) not in ['0','1']:
        raise RuntimeError("Invalid boot type")
    cmd1="ipmitool raw 0x3a 0x25 0x0%s" %str(boot_type)
    cmd2="reboot"
    device_obj.executeCmd(cmd1)
    device_obj.sendCmd(cmd2)
    primary_boot_pattern="Primary BIOS boot in progress"
    backup_boot_pattern="Back up BIOS boot in progress"
    
    if str(boot_type)=='0':
        output = device_obj.read_until_regexp(primary_boot_pattern, timeout=120)
        match1 = re.findall(primary_boot_pattern, output)
    else:
        output = device_obj.read_until_regexp(backup_boot_pattern, timeout=120)
        match1 = re.findall(backup_boot_pattern, output)
    device_obj.read_until_regexp("localhost login", timeout=200)
    log.info("Login into device")
    device_obj.loginToDiagOS()

    
    if match1 and str(boot_type)=='0':
        log.success("Bios is rebooted in primary mode")
    elif match1 and str(boot_type)=='1':
        log.success("Bios is rebooted in Backup mode")
    else:
        raise RuntimeError("Error while rebooting bios!!")
    
    
def verify_the_bios_version(device, image):
    device_obj = Device.getDeviceObject(device)
    cmd = "dmidecode -t bios"
    res = device_obj.executeCmd(cmd)
    image_name=image.split("Moonstone_Offline_BIOS_")[1].split(".BIN")
    pattern = "Version: %s" %image_name[0]
    match = re.findall(pattern, res)
    log.cprint(match)
    if match:
        log.success("Bios version is as expected: %s" %pattern)
    else:
        raise RuntimeError("expected Bios version should be %s" %(pattern))
        
        
#TC - SSH Access
           
@logThis
def ssh_into_moonstone_device(device, host_ip, host_name, host_passwd, server_prompt):
    deviceObj = Device.getDeviceObject(device)
    devicePc = Device.getDeviceObject('PC')
    MOONSTONECommonLib.check_server_moonstone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    cmd = 'ssh ' + host_name + '@' + host_ip
    #cmd = "ssh sysadmin@10.208.80.112"
    cmd2 = 'ssh-keygen -f "/home/moonstone/.ssh/known_hosts" -R "'+host_ip+'"'

    deviceObj.sendCmd("dhclient -v ma1")
    log.info("Add correct host key in /home/moonstone/.ssh/known_hosts")
    deviceObj.sendCmd(cmd2)
    time.sleep(15)
    deviceObj.sendCmd(cmd)
    promptList = ["(y/n)", "(yes/no)", "password:"]
    patternList = re.compile('|'.join(promptList))
    output = deviceObj.read_until_regexp(patternList, 20)
    if re.search("(y/n)", output):
        deviceObj.sendCmd("yes")
        deviceObj.read_until_regexp("password:", 20)
        deviceObj.sendCmd(host_passwd)
        deviceObj.read_until_regexp(server_prompt, 20)
    elif re.search("(yes/no)", output):
        deviceObj.sendCmd("yes")
        deviceObj.read_until_regexp("password:", 20)
        deviceObj.sendCmd(host_passwd)
        deviceObj.read_until_regexp(server_prompt, 20)
    elif re.search("password:", output):
        deviceObj.sendCmd(host_passwd)
        deviceObj.read_until_regexp(server_prompt, 20)
    else:
        log.fail("pattern mismatch")
    deviceObj.sendline('\n')
    
    res = deviceObj.executeCmd("ipmitool mc info")
    CommonKeywords.should_match_paired_regexp_list(res,bmc_version_info_list)
    log.success("BMC version info is as expected.")
    deviceObj.sendCmd('exit')
    MOONSTONECommonLib.exit_the_server(device)
    
    
def exit_from_moonstone_device(device):
    deviceObj = Device.getDeviceObject(device)
    deviceObj.sendCmd('exit')
    

# TC - 3.15.4.1 Baseboard CPLD Update Test
def update_baseboard_cpld_image(device, image):
    device_obj = Device.getDeviceObject(device)
    promptServer=device_obj.promptServer
    device_obj.sendCmd("dhclient -v ma1")
    time.sleep(20)
    MOONSTONECommonLib.check_server_moonstone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    log.info("Updating baseboard cpld with image %s" %image)
    update_cpld_cmd="./CFUFLASH -nw -ip "+ mgmt_ip +" -U root -P 0penBmc -C 17 -d 4 "+ image +" -fb"

    c1 = device_obj.executeCmd(update_cpld_cmd, timeout=400)
    if not re.findall(r"rror|Fail|fail|invalid", c1):
        log.success("Baseboard CPLD is updated through command : %s" %update_cpld_cmd)
    else:
        raise RuntimeError("Some error found while updating Baseboard CPLD")
    MOONSTONECommonLib.exit_the_server(device)     
    
    log.success("Baseboard CPLD is updated successfully with image %s ." %image)
    

def check_baseboard_cpld_version_through_bmc_console(device, version):
    device_obj = Device.getDeviceObject(device)
    cmd = "i2cget -f -y 2 0x0d 0x00"
    res = device_obj.executeCmd(cmd)
    CommonKeywords.should_match_a_regexp(res,version)
    log.success("Baseboard CPLD version is as expected in BMC console: %s" %version)

def check_baseboard_cpld_version_through_lpc(device, version):
    device_obj = Device.getDeviceObject(device)
    log.debug("Go to diag tools path")
    cmd = "cd /home/cel_diag/moonstone/tools"
    device_obj.executeCmd(cmd)
    log.debug("Get CPLD version via LPC")
    cmd = "./lpc_cpld_x86_64 blu r 0xa100"
    res = device_obj.executeCmd(cmd)
    CommonKeywords.should_match_a_regexp(res,version)
    log.success("Baseboard CPLD version is as expected in LPC: %s" %version)
    log.debug("Go to root path")
    cmd = "cd /root"
    device_obj.executeCmd(cmd)

# TC - Get/Set Fan Settings


def check_fcs_status(device, status):
    device_obj = Device.getDeviceObject(device)
    time.sleep(10)
    cmd = "ipmitool raw 0x3a 0x26 0x00"
    res = device_obj.executeCmd(cmd)
    res = res.split("\n")
    res = res[1].strip()
    log.cprint(res)
    if res == status:
        log.success("FCS status is as expected .i.e. %s" %status)
    else:
        raise RuntimeError("Expected status should be %s but got %s " %(status, res))
        

def check_set_fcs_status(device, status):
    device_obj = Device.getDeviceObject(device)
    cmd = "ipmitool raw 0x3a 0x26 0x01 %s" %status
    res = device_obj.executeCmd(cmd)
    if re.findall(r"rror|Fail|fail|invalid", res):
        raise RuntimeError("Unable to set FCS status to %s" %status)
    log.success("Successfully executed command to change fcs status to %s" %status)
    check_fcs_status(device, status)
    
    
def check_all_fan_psu_status(device):
    device_obj = Device.getDeviceObject(device)
    for val in range(6):
        cmd = "ipmitool raw 0x3a 0x26 0x03 0x0%s" %str(val)
        res = device_obj.executeCmd(cmd)
        res = res.split("\n")
        res = res[1].strip()
        log.cprint(res)
        if res == "00":
           log.success("%s is present in device" %sensor_device[val])
        else:
           raise RuntimeError("%s is not present in device" %sensor_device[val])
        
# TC - Discrete sensor monitor sel
    
def run_script_through_lan(device):
    device_obj = Device.getDeviceObject(device)
    log.info("Clear Sel list before running sensor event generation script")
    device_obj.executeCmd("ipmitool sel clear")
    time.sleep(20)
    device_obj.executeCmd("dhclient -v ma1")
    
    MOONSTONECommonLib.check_server_moonstone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    
    log.info("Downloading script into server...")
    device_obj.executeCmd("wget http://"+scp_ip+":"+moonstone_home_path+event_generation_script)
    
    log.info("Allocating permissions to execute this script.")
    device_obj.executeCmd("chmod 777 %s" %event_generation_script)
    for id_ in sensor_name_list.keys():
        cmd = "./" +event_generation_script+" -L %s" %str(id_)
        device_obj.sendCmd(cmd)
        out=device_obj.read_until_regexp('Please input BMC LAN IP.*',timeout=30)
        device_obj.sendCmd(mgmt_ip)
        out=device_obj.read_until_regexp('moonstone@cinaen21.*',timeout=300)
        sensor_pattern = ["%s.*Lower Critical going low.*Asserted " %sensor_name_list[str(id_)],
         "%s.*Lower Critical going low.*Deasserted" %sensor_name_list[str(id_)]]
        CommonKeywords.should_match_paired_regexp_list(out,sensor_pattern)
        log.success("%s is Asserted and Deasserted successfully." %sensor_name_list[str(id_)])
        
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")
    log.info("Remove the script from server now.")
    device_obj.sendCmd("rm %s" %event_generation_script)
        
        
def run_script_through_kcs(device):
    device_obj = Device.getDeviceObject(device)
    log.info("Clear Sel list before running sensor event generation script")
    device_obj.executeCmd("ipmitool sel clear")
    time.sleep(20)
    device_obj.executeCmd("dhclient -v ma1")
    log.info("Downloading script into server...")
    device_obj.executeCmd("wget http://"+scp_ip+":"+moonstone_home_path+event_generation_script)
    log.info("Allocating permissions to execute this script.")
    device_obj.executeCmd("chmod 777 %s" %event_generation_script)
    for id_ in sensor_name_list.keys():
        cmd = "./"+event_generation_script+" -K %s" %str(id_)
        out=device_obj.executeCmd(cmd)
        sensor_pattern = ["%s.*Lower Critical going low.*Asserted " %sensor_name_list[str(id_)],
         "%s.*Lower Critical going low.*Deasserted" %sensor_name_list[str(id_)]]
        CommonKeywords.should_match_paired_regexp_list(out,sensor_pattern)
        log.success("%s is Asserted and Deasserted successfully." %sensor_name_list[str(id_)])
    log.info("Remove the script from device now.")
    device_obj.sendCmd("rm %s" %event_generation_script)
    

@logThis
def get_ip_address_from_ipmitool(device, eth_type='dedicated', ipv6=False):
    """
    Use IPMI command to get IP address
    :param device: product name
    :param eth_type: Network port type: dedicated, shared
    :param ipv6: Whether to get IPV6, if False, get IPV4
    :return: IP address
    """
    device_obj = Device.getDeviceObject(device)
    cmd1 = 'ipmitool lan print 1'
    cmd2 = 'ipmitool lan6 print 1'
    cmd3 = 'ipmitool lan print 8'
    cmd4 = 'ipmitool lan6 print 8'
    if ipv6:
        ip_re = r'IPv6 Dynamic Address 0.+\n.+\n.+Address:\s+(.+)/'
        cmd = cmd2 if eth_type == 'dedicated' else cmd4
    else:
        ip_re = r"IP Address\s+:\s+(\d+\..*\d+)"
        cmd = cmd1 if eth_type == 'dedicated' else cmd3
    output = run_command(cmd,prompt="root@localhost:~#")
    #output = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    ip_res = re.findall(ip_re, output)
    if ip_res:
        ip = ip_res[0]
        if ip == "0.0.0.0":
            PRINTE("Fail! Got bmc ip:0.0.0.0")
        log.success('Pass! get ip address from ipmitool: %s' % ip)
        return ip
    else:
        log.fail('Fail! can not get ip address from ipmitool response:\n%s' % output)
        raise RuntimeError("Fail! get_ip_address_from_ipmitool")

@logThis
def power_cycle_onl(device,bmc_ip):
    device_obj = Device.getDeviceObject(device)
    mc_info_cmd="ipmitool -I lanplus -H {} -U root -P 0penBmc -C 17 mc info".format(bmc_ip)
    mc_info_op=Device.execute_local_cmd(device_obj,mc_info_cmd,timeout=60)
    log.info(mc_info_op)
    #cmd2 = "ipmitool -I lanplus -H %s -U root -P 0penBmc -C 17 chassis power %s" % (ip, status)
    output1 = Device.execute_local_cmd(device_obj, mc_info_cmd, timeout=300)
    log.info(output1)

def set_power_status(device, status, ip=None, connection=False):
    """
    OS
    On the PC, send 'ipmitest chassis power' to bmc (bmc is not powered off) to power on and off the system
    :param device: the name of the tested product
    :param status:on/off/reset/cycle
    :param ip: BMC IP of the tested product
    :param connection:Whether to connect DUT
    """
    status = status.lower()
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U root -P 0penBmc -C 17 chassis power %s" % (ip, status)
        Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = "ipmitool chassis power %s" % status
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if connection:
        connect(device)

def poweruptheunit(device, ip, exp_chassis_status):
    """
    After AC cycle, need to power up the unit through the BMC IP
    :param device            : product under test
    :param ip                : passing BMC IP
    :param exp_chassis_status: passing Expected Chassis power status
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U root -P 0penBmc -C 17 power on"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    time.sleep(120)
    Chassis_power_status = get_chassis_power_status(device=device, ip=ip)
    if Chassis_power_status == exp_chassis_status:
        log.success(f"Verifed Chassis power status is {Chassis_power_status}")
    else:
        log.fail(f"Fail! Expected chassis power status:{exp_chassis_status}, chassis power status:{Chassis_power_status}")
        raise Exception("Fail! Chassis power status not changed")

@logThis
def power_reset_onl(device,bmc_ip):
    device_obj = Device.getDeviceObject(device)
    mc_info_cmd="ipmitool -I lanplus -H {} -U root -P 0penBmc -C 17 mc info".format(bmc_ip)
    mc_info_op=Device.execute_local_cmd(device_obj,mc_info_cmd,timeout=60)
    log.info(mc_info_op)
    #cmd2 = "ipmitool -I lanplus -H %s -U root -P 0penBmc -C 17 chassis power %s" % (ip, status)
    output1 = Device.execute_local_cmd(device_obj, mc_info_cmd, timeout=160)
    log.info(output1)

def get_chassis_power_status(device, ip=None):
    """
    Get the chassis power status through ipmitool chassis power status when no IP is passed in. Otherwise, obtain the
    chassis power status through the BMC IP
    :param device: product under test
    :param ip: BMC IP can not be passed in
    :return: chassis power status
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U root -P 0penBmc -C 17 chassis power status" % ip
        res = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    else:
        cmd = "ipmitool chassis power status"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if res:
        power_status = re.findall(r"Chassis Power is (on|off)", res)[0]
        log.info("Pass! get chassis power status:%s" % power_status)
        return power_status
    else:
        PRINTE("Fail! couldn't get chassis power status.response:\n%s" % res)

def check_chassis_power_status(device, ip, exp_status):
    """
    Check whether the current chassis power state meets expectations
    :param device: product under test
    :param ip: BMC IP can not be passed in
    :param exp_status: Expected chassis power status
    """
    exp_status = exp_status.lower()
    power_status = get_chassis_power_status(device=device, ip=ip)
    if power_status != exp_status:
        PRINTE("Fail! exp_status:%s, chassis power status:%s" % (exp_status, power_status))

def check_bmc_channel_info(device, channel_id, lanplus=False):
    channel_id = channel_id.lower()
    if channel_id not in ["0x00", "0x01", "0x0f"]:
        PRINTE("Fail! check_bmc_channel_info parameter must be '0x00', '0x01', '0x0f'")
    device_obj = Device.getDeviceObject(device)
    
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        # cmd = "ipmitool -I lanplus -H %s -U root -P 0penBmc -C 17 channel info %s" %(mgmt_ip, channel_id)
        cmd = lanplus_ipmitool_cmd.format("channel info %s" %channel_id)
    else:
        cmd = "ipmitool channel info %s" % channel_id

    output=device_obj.executeCmd(cmd)
    if channel_id == "0x00" : 
        pattern = "Channel Medium Type   : IPMB"
    if channel_id == "0x01" : 
        pattern = "Channel Medium Type   : 802.3 LAN"
    if channel_id == "0x0f" : 
        pattern = "Channel Protocol Type : KCS" 		
    match = re.findall(pattern, output)
    if match:
        log.success("Channel info for ID %s is correct!!" %channel_id)
    else:
        raise RuntimeError("Fail! Channel info for ID %s is not correct!!" %channel_id)

@logThis
def switch_bmc(device):
    device= Device.getDeviceObject(device)
    device.switchToBmc()
    device.loginToNEWBMC()
    pass

@logThis
def switch_cpu(device):
    device= Device.getDeviceObject(device)
    device.switchToCpu()
    device.loginToDiagOS()
    pass

@logThis
def verify_read_write_cpld_through_bmc_console():

    log.debug("Verify default CPLD scratch register value")
    out1=device.executeCmd('i2cget -f -y 2 0x0d 0x01')
    if re.search('0xde',out1):
        log.success('Scratch Register value is correct')
    else:
        raise RuntimeError('Scratch Register value is not correct')

    log.debug("Write Scratch Register")
    device.executeCmd('i2cset -f -y 2 0x0d 0x1 0xff')
    log.debug("Verify Scratch Register value after writing")
    out1=device.executeCmd('i2cget -f -y 2 0x0d 0x01')
    if re.search('0xff',out1):
        log.success('Scratch Register value is written successfully')
    else:
        raise RuntimeError('Scratch Register value is not written successfully')

    log.debug("Switch to default scratch register value")
    device.executeCmd('i2cset -f -y 2 0x0d 0x1 0xde')
    log.debug("Verify current CPLD scratch register value")
    out1=device.executeCmd('i2cget -f -y 2 0x0d 0x01')
    if re.search('0xde',out1):
        log.success('Scratch Register value is switched to default')
    else:
        raise RuntimeError('Scratch Register value is not switched to default')


def verify_dependent_image_using_diag():

    log.debug("Go to diag path")
    cmd = "cd /home/cel_diag/moonstone/bin"
    device.executeCmd(cmd)

    log.debug("Check Dependent Image Versions using Diag")
    cmd = "./cel-sysinfo-test -all"
    res = device.executeCmd(cmd)
    BIOS_version=new_bios_image.split("Moonstone_Offline_BIOS_")[1].split(".BIN")[0]
    pattern = []
    pattern.append("BIOS .* Version: {}".format(BIOS_version))
    pattern.append("COMe CPLD .*: {}".format(come_cpld_version))
    pattern.append("Baseboard CPLD .*: {}".format(cpld_image_version_lpc))
    pattern.append("Diag Version: {}".format(diag_version))
    pattern.append("BMC Version:  {}".format(moonstone_bmc_firmware_revision))
    pattern.append("Switch CPLD 1 .*: {}".format(switch_cpld_1_version))
    pattern.append("Switch CPLD 2 .*: {}".format(switch_cpld_2_version))
    pattern.append("FPGA .*: {}".format(fpga_version))
    pattern.append("OPT test all .* | PASS |")
    CommonKeywords.should_match_ordered_regexp_list(res,pattern)

    # cmd = "cat /etc/issue"
    # output1=device.executeCmd(cmd) 
    # pattern1 = "Open Network Linux OS {}".format(onl_version)
    # CommonKeywords.should_match_a_regexp(output1,pattern1)
    # log.success('Dependent Image Versions are correct')

    log.debug("Go to root path")
    cmd = "cd /root"
    device.executeCmd(cmd)


def check_lan_interface_stress_test(device):

    log.debug("Executing ipmi lanplus commands in parallel using script")

    device_obj = Device.getDeviceObject(device)

    cmd = "./"+ image_path_in_server + lan_stress_script + " " + mgmt_ip
    out=device_obj.executeCmd(cmd, timeout=300)
    sensor_pattern = "LAN stress test passed"
    CommonKeywords.should_match_a_regexp(out,sensor_pattern)
    log.success("LAN stress test using script passed")


def check_kcs_interface_stress_test(device):

    device_obj = Device.getDeviceObject(device)
    duration = 20
    promptServer=device_obj.promptServer

    log.info("Executing ksc interface stress test using script")
    
    MOONSTONECommonLib.check_server_moonstone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    
    log.info("Copy script to switch..")
    copy_script_cmd="scp "+ image_path_in_server + kcs_stress_script + " root@" + mgmt_ip_onl + ":/root/"
    device_obj.sendCmd(copy_script_cmd, timeout=90)
    c1 = device_obj.read_until_regexp(r'password:', timeout=90)
    device_obj.sendCmd("onl", timeout=90)
    c2 = device_obj.read_until_regexp(promptServer, timeout=90)
    if re.findall(r"rror|Fail|fail|invalid", c2) or (not r"100%" in c2):
        raise RuntimeError("Error in copying script to switch")
    else:
        log.success("Successfully copied script to switch.")
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")
    
    log.info("Allocating permissions to execute this script.")
    device_obj.executeCmd("chmod 777 %s" %kcs_stress_script)
    
    log.info("Execute the script.")
    cmd = "./" + kcs_stress_script + " " + str(duration)
    out=device_obj.executeCmd(cmd, timeout=300)
    pattern = "KCS stress test passed"
    CommonKeywords.should_match_a_regexp(out,pattern)
    log.success("KCS stress test using script passed")

    log.info("Remove the script and log from switch now.")
    device_obj.sendCmd("rm %s" %kcs_stress_script)
    device_obj.sendCmd("rm %s" %kcs_stress_script_log)

def set_power_cycle_bmc_console(device):
    device_obj = Device.getDeviceObject(device)
    log.info("power cycle from BMC console")
    cmd = "ipmitool power cycle"
    out=device_obj.executeCmd(cmd, timeout=300)
    pattern = "Chassis Power Control: Cycle"
    CommonKeywords.should_match_a_regexp(out,pattern)

    time.sleep(200)
    cmd = "ipmitool power status"
    out=device_obj.executeCmd(cmd, timeout=300)
    pattern = "Chassis Power is on"
    CommonKeywords.should_match_a_regexp(out,pattern)
    log.success("Power cycle from BMC console passed")


#********************************************  DONE  ************************************************************************
