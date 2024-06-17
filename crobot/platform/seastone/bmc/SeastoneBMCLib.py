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
#import openbmc
#import openbmc_lib

from SeastoneBMCVariable import *
from datetime import datetime, timedelta
from dataStructure import nestedDict, parser
from SwImage import SwImage
from pexpect import pxssh
import sys
import getpass
import SEASTONECommonLib
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
def check_bmc_version_info(device):
    device_obj = Device.getDeviceObject(device)
    cmd='ipmitool mc info'
    c1=device_obj.executeCmd(cmd)
    CommonKeywords.should_match_paired_regexp_list(c1,bmc_version_info_list)
    log.success("BMC version info is as expected.")


@logThis
def bmc_reset(device, coldOrwarm, lanplus=False):
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd = lanplus_ipmitool_cmd.format("mc reset " + coldOrwarm)
    else:
        cmd="ipmitool mc reset " + coldOrwarm
    c1=device_obj.executeCmd(cmd)
    pattern = "Sent "+ coldOrwarm +" reset command to MC"
    log.info("Sleeping for 300 seconds for device to come up")
    time.sleep(300)
    CommonKeywords.should_match_a_regexp(c1,pattern)
    power_status = check_sel_list_info(device, sel_list_pattern=sel_list_mc_reset_pattern, lanplus=lanplus)
    if(power_status):
        log.success("bmc reset " + coldOrwarm + " executed successfully.")
    else:
        raise RuntimeError("bmc reset "+ coldOrwarm + " failed !!")
    

def set_power_cycle(device, lanplus=False):
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin power cycle \r" % mgmt_ip
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
            cmd = "ipmitool -I lanplus -H %s -U admin -P admin lan set 1 ipaddr %s" % (mgmt_ip, ipaddr)
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
            cmd = "ipmitool -I lanplus -H %s -U admin -P admin lan set 1 netmask %s" % (mgmt_ip, netmask)
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
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin lan set 1 ipsrc %s" % (mgmt_ip, ip_status)
    else:
        cmd = "ipmitool lan set 1 ipsrc %s" % ip_status
    output=device_obj.executeCmd(cmd) 
    
    if r"rror|Fail|fail" in output:
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
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin lan print 1" % mgmt_ip
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
    if "rror" in output:
        log.fail("BMC Memory enable command failed!!")
    else:
        log.success("BMC Memory enable command executed successfully")
	
 
def disable_bmc_memory():
    cmd = "ipmitool raw 0x3a 0x2c 0x00"
    output = run_command(cmd)
    log.cprint(output)
    if "rror" in output:
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
    
    pattern = "Updating Field.*'"+previous_fru_mac+"' with '"+mac_address+"'"
    CommonKeywords.should_match_a_regexp(res, pattern)
    log.success("Success!! new mac address %s is edited through ipmitool successfully." %mac_address)
    
    cmd2="ipmitool raw 0x06 0x02"
    output=device_obj.executeCmd(cmd2)
    if "rror|Fail|fail" in output:
        raise RuntimeError("Error in executing command '%s'" %cmd)
    log.info("Sleeping for 300 seconds to update new mac address in bmc.")
    time.sleep(300)
    
    
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
    
        if "rror|Fail|fail|invalid" in res:
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
    if "rror|Fail|fail|invalid" in res1:
        raise RuntimeError("User id %s is unable to execuete '%s' command" %(str(user_id), cmd1))
        
    res2=device_obj.executeCmd(cmd2)
    if "rror|Fail|fail|invalid" in res2:
        raise RuntimeError("User id %s is unable to execuete '%s' command" %(str(user_id), cmd2))
        
    user_list_pattern = "%s\s+%s\s+true\s+false\s+true\s+ADMINISTRATOR" %(str(user_id), user_name)
    output=device_obj.executeCmd(cmd_ipmitool_user_list_1)
    CommonKeywords.should_match_a_regexp(output, user_list_pattern)
    log.success("User with user id %s and user name %s has changed its priviledge to ADMINISTRATOR successfully." %(str(user_id), user_name))
    

def check_lanplus_communication_through_user(device, user_id, user_name, user_pass):
    device_obj = Device.getDeviceObject(device)
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
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
        if "rror|Fail|fail|invalid" in res:
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
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    
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
    if("rror|Fail|fail|invalid" in res):
        raise RuntimeError("Not able to use 'ipmitool user enable' command for user_id %s" %user_id)
        
    priv_dict = {"ADMINISTRATOR":"4", "OPERATOR":"3", "USER":"2"}
    for key,value in priv_dict.items():
        priviledge_cmd = "ipmitool raw 0x06 0x43 0x91 %s %s" %(user_id, value)
    
        res =  device_obj.executeCmd(priviledge_cmd)
        if("rror|Fail|fail|invalid" in res):
            raise RuntimeError("Unable to give %s access to user_id %s" %(key,user_id))
        pattern = "%s\s+%s\s+true\s+false\s+true\s+%s" %(user_id, user_name, key)
        user_list_output = device_obj.executeCmd(cmd_ipmitool_user_list_1)
        CommonKeywords.should_match_a_regexp(user_list_output, pattern)
        log.success("Successfully updated priviledge access to %s for user_id %s" %(key, user_id))
        log.info("Trying to access lanplus command through %s priviledge access of user_id %s" %(key, user_id) )
        check_user_priviledge_lanplus_communication(device, user_id, user_name, user_pass, key)
    
    log.success("Successfully, verified priviledge modes on user_id %s" %user_id)
      

def set_user_privilege(device, user_id,priv_level):
    device_obj = Device.getDeviceObject(device)
    cmd='ipmitool user enable %s' %user_id
    res=device_obj.executeCmd(cmd)
    if("rror|Fail|fail|invalid" in res):
        raise RuntimeError("Not able to use 'ipmitool user enable' command for user_id %s" %user_id)

    cmd='ipmitool user priv %s %s 1' %(user_id,priv_level)
    res=device_obj.executeCmd(cmd)
    if("rror|Fail|fail|invalid" in res):
        raise RuntimeError("Not able to use 'ipmitool user priv' command for user_id %s" %user_id)

    log.success("Successfully, verified priviledge modes on user_id %s" %user_id)
      
# TC - BMC Console Baudrate Setting

def check_set_baurd_rate(device, end_baurd_rate, start_baurd_rate):
    device_obj = Device.getDeviceObject(device)
    
    for baurd in range(int(end_baurd_rate), int(start_baurd_rate)-1, -1):
      SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
      write_baurd_cmd=lanplus_ipmitool_cmd.format("raw 0x3a 0x23 0x01 0x0%s" %str(baurd))
      read_baurd_cmd=lanplus_ipmitool_cmd.format("raw 0x3a 0x23 0x00")
      
      log.info("Updating Baurd rate of device to 0x0%s" %str(baurd))
      res=device_obj.executeCmd(write_baurd_cmd)
      log.cprint(res)
      if "rror|Fail|fail|invalid" in res:
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
    if "rror|Fail|fail|invalid" in res:
          raise RuntimeError("Unable to update sol information through cmd %s" %cmd1)
    check_sol_configuration(device, parameter, value)

def set_and_check_sol_config(device, parameter, value):
    device_obj = Device.getDeviceObject(device)
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    cmd1 = lanplus_ipmitool_cmd.format("sol set %s %s 1" %(parameter, value))
    promptServer=device_obj.promptServer
    res=device_obj.executeCmd(cmd1)
    log.cprint(res)
    log.info("Setting Sol parameter %s with %s value" %(parameter, value))
    if "rror|Fail|fail|invalid" in res:
          raise RuntimeError("Unable to update sol information through cmd %s" %cmd1)
    check_sol_config(device, parameter, value)
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")
    
    
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

def check_sol_config(device, parameter, value):
    device_obj = Device.getDeviceObject(device)
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
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
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")

def set_and_check_sol_auth(device, parameter, value):
    device_obj = Device.getDeviceObject(device)
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    cmd1 = lanplus_ipmitool_cmd.format("sol set %s %s 1" %(parameter, value))
    promptServer=device_obj.promptServer
    res=device_obj.executeCmd(cmd1)
    log.cprint(res)
    log.info("Setting Sol parameter %s with %s value" %(parameter, value))
    if "rror|Fail|fail|invalid" in res:
          raise RuntimeError("Unable to update sol information through cmd %s" %cmd1)
    check_sol_priv(device, parameter, value)
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")

def set_sol_payload(device, parameter, value):
    device_obj = Device.getDeviceObject(device)
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    cmd1 = lanplus_ipmitool_cmd.format("sol payload enable %s %s" %(parameter, value))
    promptServer=device_obj.promptServer
    res=device_obj.executeCmd(cmd1)
    log.cprint(res)
    log.info("Setting Sol parameter %s with %s value" %(parameter, value))
    if "rror|Fail|fail|invalid" in res:
          raise RuntimeError("Unable to update sol payload through cmd %s" %cmd1)
    #check_sol_config(device, parameter, value)
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")

def check_sol_priv(device, parameter, value):
    device_obj = Device.getDeviceObject(device)
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    cmd2 = lanplus_ipmitool_cmd.format("sol info 1")
    promptServer=device_obj.promptServer
    res=device_obj.executeCmd(cmd2)
    log.cprint(res)

    if re.search('Privilege.*OPERATOR',res):
        log.success("Privilege Level set to Operator")
    else:
        raise RuntimeError("Privilege Level not set")
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")

def check_sol_activate(device):
    device_obj = Device.getDeviceObject(device)
    #SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    #log.info("Sol Activate with admin user")
    #cmd2 = lanplus_ipmitool_cmd.format("sol activate\n\n")
    #output1 = Device.execute_local_cmd(device_obj, cmd2, timeout=20)
    #output2 = Device.execute_local_cmd(device_obj, "\n", timeout=20)
    #log.info(output1)
    log.info("Sol Activate with USER user fails")
    cmd2 = lanplus_ipmitool_tester_cmd.format("sol activate\n\n")
    output1 = Device.execute_local_cmd(device_obj, cmd2, timeout=20)
    output2 = Device.execute_local_cmd(device_obj, "\n", timeout=20)
    log.info(output1)
    #log.info("Sol Activate with OPERATOR user works")
    #cmd2 = lanplus_ipmitool_tester1_cmd.format("sol activate\n\n")
    #output1 = Device.execute_local_cmd(device_obj, cmd2, timeout=20)
    #output2 = Device.execute_local_cmd(device_obj, "\n", timeout=20)
    #log.info(output1)
    #promptServer=device_obj.promptServer
    #res=device_obj.executeCmd(cmd2)

    
    
# TC - KCS Interface Test

def set_modprobe(device):
    device_obj = Device.getDeviceObject(device)
    cmd1="modprobe ipmi_si"
    cmd2="modprobe ipmi_devintf"
    res1=device_obj.executeCmd(cmd1)
    res2=device_obj.executeCmd(cmd2)
    if "rror|Fail|fail|invalid" in res1:
          raise RuntimeError("Unable to execute cmd %s" %cmd1)
    if "rror|Fail|fail|invalid" in res2:
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
    cmd2="ipmitool raw 0 2 3"
    res1 = device_obj.executeCmd(cmd1)
    boot_device_pattern = "Set Boot Device to bios"
    CommonKeywords.should_match_a_regexp(res1,boot_device_pattern)
    
    log.info("Boot bios dut..")
    res2 = device_obj.sendCmd(cmd2)
    pattern="Primary BIOS boot in progress"
    device_obj.read_until_regexp(pattern, timeout=300)
    time.sleep(30)
    bios_menu_lib.send_key(device, "KEY_ESC")

    time.sleep(5)
    bios_menu_lib.send_key(device, "KEY_ENTER",2)
    log.info("Primary Bios Booting started")
    device_obj.read_until_regexp("localhost login:.*", timeout=300)
    device_obj.loginToDiagOS()
    log.success("Bios Boot through ipmitool is executed successfully")
    

# TC - Online Update through LAN

def check_bmc_version_through_raw_cmd(device, version, lanplus=False):  
    device_obj = Device.getDeviceObject(device)
    if(lanplus):
        mgmt_ip = device_obj.managementIP
        promptServer=device_obj.promptServer
        cmd = lanplus_ipmitool_cmd.format("raw 0x32 0x8f 0x08 0x01")
    else:
        cmd = "ipmitool raw 0x32 0x8f 0x08 0x01"
    res=device_obj.executeCmd(cmd)
    log.cprint(res)
    CommonKeywords.should_match_a_regexp(res,version)
    log.success("Primary bmc version is as expected : %s" %version)
    
    
def update_primary_bmc(device, image):
    device_obj = Device.getDeviceObject(device)
    promptServer=device_obj.promptServer
    
    log.info("Updating primary bmc..")
    update_primary_bmc_cmd="./CFUFLASH -nw -ip "+ mgmt_ip +" -u admin -p admin -d 1 -mse 1 %s" %image
    device_obj.sendCmd(update_primary_bmc_cmd, timeout=90)
    c1 = device_obj.read_until_regexp(r'Enter your Option : ', timeout=90)
    if(no_update_required_pattern in c1):
        device_obj.sendline("n")
    else:
        device_obj.sendline("y")
        
    c2 = device_obj.read_until_regexp(promptServer, timeout=300)
    if r"rror|fail|Fail" in c2:
        raise RuntimeError("Error in updating Primary BMC")
    else:
        log.success("Successfully updated primary BMC.")
    if(reset_firmware_pattern in c2):
        log.info("Sleeping for 300 seconds for BMC to come up after bmc update")
        time.sleep(300)
        
    log.info("Check sel list after updation.")
    flag = check_sel_list_info(device, sel_list_pattern=sel_list_after_updating_image, lanplus=True)
    if flag:
        log.info("Sel list is cleared after updation of image")
    else:
        raise RuntimeError("Sel list is not empty yet")
        

# TC Clear CMOS by IPMI
def clear_cmos_by_ipmi_lanplus(device):
    cmd = lanplus_ipmitool_cmd.format("chassis bootdev disk clear-cmos=yes")
    device_obj = Device.getDeviceObject(device)
    c1=Device.execute_local_cmd(device_obj, cmd)
    log.info(c1)
    if "rror|Fail|fail|invalid" in c1:
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
    
    log.info("Sleeping for 150 seconds.")
    time.sleep(150)
    
    CommonKeywords.should_match_a_regexp(c1,pattern)
    if(status=='on'):
        log.info("Sleeping for 150 seconds.")
        time.sleep(150)
        log.info("Login into device")
        device_obj.loginToDiagOS()
        sel_list_pattern=sel_list_power_on_pattern
        sel_cmd = lanplus_ipmitool_cmd.format('sel list | tail')
        log.info("Fetching BMC sel list after setting power chassis status")
        c2=Device.execute_local_cmd(device_obj, sel_cmd, timeout=120)
        log.info("Output : "+c2)
        c2=c2.split("\n")
        c2=c2[-3:]
        log.cprint(c2)
        log.cprint("next line" )
        log.cprint(sel_list_pattern)
        CommonKeywords.should_match_ordered_regexp_list(c2,sel_list_pattern)
        log.success("Sel list is as expected after power %s" %status)
    

def power_cycle_and_login(device):
    device_obj = Device.getDeviceObject(device)
    SEASTONECommonLib.powercycle_device(device)
    log.info("Login into device")
    device_obj.loginToDiagOS()

        
# TC - Extensional read write


def write_data_to_bus(device):
    device_obj = Device.getDeviceObject(device)
    cmd = 'ipmitool raw 0x3a 0x3e 0x02 0xae 0x03 0 0 0xaa 0xbb 0xcc'
    res = device_obj.executeCmd(cmd)
    if "rror|Fail|fail|invalid" in res:
          raise RuntimeError("Unable to write data to bus 2 through cmd %s" %cmd)
    else:
        log.success("Successfully write data to bus 2 through cmd %s" %cmd)
        

def read_data_from_bus(device):
    device_obj = Device.getDeviceObject(device)
    cmd="ipmitool raw 0x3a 0x3e 0x02 0xae 0x03 0 0"
    res = device_obj.executeCmd(cmd)
    if "rror|Fail|fail|invalid" in res:
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
    path = "cd diag/home/cel_diag/seastone2v2/firmware/fru_eeprom/"
    device_obj.executeCmd(path)
    res=device_obj.executeCmd("./bin_produce.sh")
    if "rror|Fail|fail|invalid" in res:
        raise RuntimeError("Unable to update FRU devices through bin_produce sh file")
    else:
        log.success("FRU devices are updated sucessfully through bin_produce sh file")
    
    device_obj.executeCmd("cd bin")
    bin_lst = ["bmc.bin",   "fan1/.bin",  "fan3/.bin",  "switch/.bin", "come.bin",  "fan2/.bin",  "fan4/.bin",  "system/.bin"]
    for item in bin_lst:
        cmd = "hexdump -C %s" %item
        device_obj.executeCmd(cmd)
        if "rror|Fail|fail|invalid" in res:
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
    if "rror|Fail|fail|invalid" in res1:
        raise RuntimeError("Unable to disable fru write protection " )
    else:
        log.success("Successful disabled fru write protection for device %s" %str(fru_device_name[int(id_)]))
    
    log.info("Read FRU data through raw command")
    res3 = device_obj.executeCmd(cmd3)
    if "rror|Fail|fail|invalid" in res3:
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
    if "rror|Fail|fail|invalid" in res1:
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
    device_obj.executeCmd("cd diag/home/cel_diag/seastone2v2/bin")
    res1 = device_obj.executeCmd(cmd)
    write_pattern = "Result.*Passed"
    CommonKeywords.should_match_a_regexp(res1,write_pattern)
    log.success("Date and Name gets updated properly for fru device %s" %str(id_))
    
    
def reset_fru_device_to_default(device, device1, device2):
    device_obj = Device.getDeviceObject(device)
    write_fru_through_diag(device, str(device1))
    write_fru_through_diag(device, str(device2))
    device_obj.executeCmd("cd")
    


# TC - Bios update via lan
def update_bios_image(device, image, boot_type, lanplus=False):
    device_obj = Device.getDeviceObject(device)
    mse=1 if str(boot_type)=='0' else 2
    if lanplus:
        promptServer=device_obj.promptServer
        device_obj.sendCmd("dhclient -v ma1")
        time.sleep(20)
        SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
        update_bios_cmd="./CFUFLASH -nw -ip "+ mgmt_ip +" -u admin -p admin -d 2 -mse "+ str(mse) +" %s -fb" %image
    else:
        update_bios_cmd="./CFUFLASH -cd -d 2 -mse "+ str(mse) +" %s -fb" %image
        
    log.info("Updating bios with image %s" %image)
    
    
    c1 = device_obj.executeCmd(update_bios_cmd, timeout=300)
    if "rror|Fail|fail|invalid" not in c1:
        log.success("Bios is updated through command : %s" %update_bios_cmd)
    else:
        raise RuntimeError("Some error found while updating primary bios")
    if str(boot_type)=='0':
        CommonKeywords.should_match_a_regexp(c1, "BIOS Image To be updated is Primary")
        log.success("Primary Image is being updating")
    else:
        CommonKeywords.should_match_a_regexp(c1, "BIOS Image To be updated is Backup")
        log.success("Backup Image is being updating")
    
    if lanplus:
        CommonKeywords.should_match_a_regexp(c1, "Creating IPMI session via network with address.*Done")
        log.success("Updation is being done through Lan")
        SEASTONECommonLib.exit_the_server(device) 
    else:
        CommonKeywords.should_match_a_regexp(c1, "Creating IPMI session via USB.*Done")
        log.success("Updation is being done through USB.")
        #Creating IPMI session via USB...Done
        #BIOS Image To be u dated is Primary
    
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
    device_obj.read_until_regexp("localhost login", timeout=300)
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
    image_name=image.split(".bin")
    pattern = "Version: %s" %image_name[0]
    match = re.findall(pattern, res)
    log.cprint(match)
    if match:
        log.success("Bios version is successfully updated to %s" %image)
    else:
        raise RuntimeError("expected Bios version should be %s but got %s" %(image, pattern))
        
        
#TC - SSH Access
           
@logThis
def ssh_into_seastonev2_device(device, host_ip, host_name, host_passwd, server_prompt):
    deviceObj = Device.getDeviceObject(device)
    devicePc = Device.getDeviceObject('PC')
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    cmd = 'ssh ' + host_name + '@' + host_ip
    #cmd = "ssh sysadmin@10.208.80.112"
    cmd2 = 'ssh-keygen -f "/home/seastonev2/.ssh/known_hosts" -R "'+host_ip+'"'

    deviceObj.sendCmd("dhclient -v ma1")
    log.info("Add correct host key in /home/seastonev2/.ssh/known_hosts")
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
    
    res = deviceObj.executeCmd("ipmitool -H 127.0.0.1 -U admin -P admin mc info")
    CommonKeywords.should_match_paired_regexp_list(res,bmc_version_info_list)
    log.success("BMC version info is as expected.")
    deviceObj.sendCmd('exit')
    SEASTONECommonLib.exit_the_server(device)
    
    
def exit_from_seastonev2_device(device):
    deviceObj = Device.getDeviceObject(device)
    deviceObj.sendCmd('exit')
    

# TC - 3.15.4.1 Baseboard CPLD Update Test
def update_baseboard_clpd_image(device, image):
    device_obj = Device.getDeviceObject(device)
    promptServer=device_obj.promptServer
    device_obj.sendCmd("dhclient -v ma1")
    time.sleep(20)
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    log.info("Updating baseboard clpd with image %s" %image)
    update_clpd_cmd="./CFUFLASH -nw -ip "+ mgmt_ip +" -u admin -p admin -d 4 "+ image +" -fb"

    c1 = device_obj.executeCmd(update_clpd_cmd, timeout=400)
    if "rror|Fail|fail|invalid" not in c1:
        log.success("Baseboard CLPD is updated through command : %s" %update_clpd_cmd)
    else:
        raise RuntimeError("Some error found while updating Baseboard CLPD")
    SEASTONECommonLib.exit_the_server(device)     
    
    log.success("Baseboard CLPD is updated successfully with image %s ." %image)
    

def check_baseboard_clpd_version(device, image):
    device_obj = Device.getDeviceObject(device)
    cmd = "ipmitool raw 0x3a 0x64 0 1 0"
    time.sleep(60)
    res = device_obj.executeCmd(cmd)
    CommonKeywords.should_match_a_regexp(res,clpd_image_to_version_mapping[image])
    log.success("Baseboard CLPD version is successfully updated to %s" %image)
   

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
    if "rror|Fail|fail|invalid" in res:
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
    
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    
    log.info("Downloading script into server...")
    device_obj.executeCmd("wget http://"+scp_ip+":"+seastone_home_path+event_generation_script)
    
    log.info("Allocating permissions to execute this script.")
    device_obj.executeCmd("chmod 777 %s" %event_generation_script)
    for id_ in sensor_name_list.keys():
        cmd = "./" +event_generation_script+" -L %s" %str(id_)
        device_obj.sendCmd(cmd)
        out=device_obj.read_until_regexp('Please input BMC LAN IP.*',timeout=60)
        device_obj.sendCmd(mgmt_ip)
        out=device_obj.read_until_regexp('seastonev2@cinaen21.*',timeout=300)
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
    device_obj.executeCmd("wget http://"+scp_ip+":"+seastone_home_path+event_generation_script)
    log.info("Allocating permissions to execute this script.")
    device_obj.executeCmd("chmod 777 %s" %event_generation_script)
    for id_ in sensor_name_list.keys():
        cmd = "./"+event_generation_script+" -K %s" %str(id_)
        out=device_obj.executeCmd(cmd, timeout=300)
        sensor_pattern = ["%s.*Lower Critical going low.*Asserted " %sensor_name_list[str(id_)],
         "%s.*Lower Critical going low.*Deasserted" %sensor_name_list[str(id_)]]
        CommonKeywords.should_match_paired_regexp_list(out,sensor_pattern)
        log.success("%s is Asserted and Deasserted successfully." %sensor_name_list[str(id_)])
    log.info("Remove the script from device now.")
    device_obj.sendCmd("rm %s" %event_generation_script)
    

#********************************************  DONE  ************************************************************************

#############

################
def connect(device, wait_time=180, timeout=300, prodect_name="seastone_e01"):
    """
    Connect tested product
    :param device: the name of the tested product
    :param wait_time: wait some time before connect
    :param timeout: connect out time
    :param prodect_name: product name
    """
    device_obj = Device.getDeviceObject(device)
    prodect_info = YamlParse.getDeviceInfo()[prodect_name]
    login_prompt = prodect_info["loginPromptDiagOS"]
    all_info = ""
    if wait_time:
        log.info("pls wait %d s" % int(wait_time))
    start_time = time.time()
    while time.time() - start_time < int(timeout):
        try:
            part_info = device_obj.readMsg()
            if part_info:
                part_info = part_info.strip()
                all_info = all_info + "\n" + part_info
                log.cprint(part_info)
                if "System Date" and "System Time" and "Access Level" in all_info:
                    log.error("Fail! device has enter Bios!! Part of the information "
                              "obtained during the waiting phase is:\n%s" % all_info)
                    whitebox_exit_bios_setup(device)
                    break
                elif login_prompt in all_info:
                    log.cprint("gdcvghdc")
                    log.cprint(login_prompt)
                    device_obj.getPrompt("DIAGOS", timeout=30)
                    break
        except Exception as E:
            log.info(str(E))
            set_wait(20)
    log.cprint("Outsode loop")
    log.info("outside loop")
    set_root_hostname(device)
    check_bmc_ready(device)

def check_bmc_ready(device, wait_time=None):
    """
    Check whether the BMC is in a normal state (has been restarted)
    :param device:product under test
    :param wait_time:Waiting time before inspection
    """
    device_obj = Device.getDeviceObject(device)
    if wait_time:
        set_wait(wait_time)
    s_time = time.time()
    while time.time() - s_time <= 200:
        try:

            device_obj.switchToBmc()
            set_wait(40)
            cmd = "ipmitest mc info"
            res = run_command(cmd, "OPENBMC")
            log.cprint("vscxsvc")
            #res = openbmc_lib.execute(device_obj, cmd, mode="OPENBMC")
            if "Device ID" in res:
                log.info("BMC has ready!")
                break
        except Exception:
            time.sleep(10)
    log.info("Inside check_bmc_ready")
    device_obj.trySwitchToCpu()
    cmd = r"ipmitool mc info"
    res = run_command(cmd)
    #res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if "Device ID" not in res:
        log.info("Fail! Switch To Cpu: fail")


def PRINTE(*agr, decide=True):
    """
    Log output as an error stream and throw an exception
    :param agr: error description
    :param decide: if True,throw an exception
    Author Yagami
    """
    error_fun_name = stack()[1][3]
    log.error(*agr)
    if decide:
        raise RuntimeError("[%s]: Fail! Function Name:%s" % (datetime.now(), error_fun_name))

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
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin chassis power %s" % (ip, status)
        Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = "ipmitool chassis power %s" % status
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if connection:
        connect(device)
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
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin chassis power status" % ip
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

def check_info_equal(info_1, info_2, decide=True):
    """
    Check whether the two messages (both will be converted to strings) are equal
    """
    info_1 = str(info_1).strip()
    info_2 = str(info_2).strip()
    if decide:
        if info_1 != info_2:
            PRINTE("Fail!\ninfo_1: %s\ninfo_2: %s" % (info_1, info_2))
    else:
        if info_1 == info_2:
            PRINTE("Fail!\ninfo_1: %s\ninfo_2: %s" % (info_1, info_2))
def verify_get_sel_info(hostip, username, userpassword, expected_result):
    log.debug("Entering verify_get_sel_info with args : %s" % (str(locals())))
    err_count = 0
    cmd1 = 'ipmitool sel list|wc -l'
    output = parse_ssh_command_cmd(username, hostip, userpassword, cmd1)
    cmd2 = "ipmitool sel list|awk 'NR==%s'" % output
    sel_data = parse_sel_info_data(hostip, username, userpassword, cmd2)
    cmd3 = 'ipmitool raw 0x0a 0x40'
    output = parse_ssh_command_cmd(username, hostip, userpassword, cmd3)
    raw_data_1 = " ".join(output.split()[0:1])
    raw_data_2 = " ".join(output.split()[1:3])
    if raw_data_1 == expected_result:
        log.success("Successfully verify_get_sel_info: byte1 = %s" % expected_result)
    else:
        log.error("FAIL: raw_data byte1 %s mismatch expected %s" % (raw_data_1, expected_result))
        err_count += 1
    if raw_data_2 == sel_data:
        log.success("Successfully verify_get_sel_info: byte2-3: %s" % raw_data_2)
    else:
        log.error("FAIL: raw_data byte2-3 %s mismatch sel_data %s" % (raw_data_2, sel_data))
        err_count += 1
    if err_count:
        raise testFailed("Failed verify_get_sel_info")

def parse_sel_info_data(hostip, username, userpassword, cmd):
    log.debug("Entering parse_sel_info_data with args : %s" % (str(locals())))
    p = r'^(\S+)\s+.+'
    err_count = 0
    output = parse_ssh_command_cmd(username, hostip, userpassword, cmd)
    match = re.search(p, output)
    if match:
        value = match.group(1).strip()
        if len(value) == 1:
            new_value = '0' + value + ' 00'
            return new_value
        elif len(value) == 2:
            new_value = value + ' 00'
            return new_value
        elif len(value) == 3:
            new_value_1 = '0' + value
            new_value = "".join(list(new_value_1)[-2:]) + ' ' + "".join(list(new_value_1)[0:2])
            return new_value
        elif len(value) == 4:
            new_value = "".join(list(value)[-2:]) + ' ' + "".join(list(value)[0:2])
            return new_value
        else:
            log.error("the value is not correct, please check it maually")
            err_count += 1
    else:
        log.error("can't match your pattern")
        err_count += 1
    if err_count:
        raise testFailed("Failed parse_sel_info_data")

def parse_ssh_command_cmd(username, hostip, userpassword, cmd, title_p=False):
    log.debug("Entering parse_ssh_command_cmd with args : %s" % (str(locals())))
    child = ssh_command(username, hostip, userpassword, cmd, title_p=title_p)
    child.expect(pexpect.EOF, timeout=30)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    return output



@logThis
def sdr_test(device):
    device_obj = Device.getDeviceObject(device)
    log.info("Clear Sel list before running sensor event generation script")
    device_obj.executeCmd("ipmitool sel clear")
    time.sleep(20)
    device_obj.executeCmd("dhclient -v ma1")
    log.info("Downloading script into server...")
    device_obj.executeCmd("wget http://"+scp_ip+":"+seastone_home_path+sdr_variable_file)
    device_obj.executeCmd("wget http://"+scp_ip+":"+seastone_home_path+sdr_generation_script)
    log.info("Allocating permissions to execute this script.")
    device_obj.executeCmd("chmod 777 %s" %sdr_variable_file)
    device_obj.executeCmd("chmod 777 %s" %sdr_generation_script)
    cmd1 = run_command("./sdr_info_get.sh",prompt ='root@localhost',timeout=1800)


@logThis
def switch_bmc(device):
    device= Device.getDeviceObject(device)
    device.switchToBmc()
    pass

@logThis
def switch_cpu(device):
    device= Device.getDeviceObject(device)
    device.switchToCpu()
    pass

def ssh_login(device, ip, username, userpassword):
    DeviceMgr.usingSsh = True
    deviceObj = DeviceMgr.getDevice(device)
    deviceObj.connect(username, ip)
    deviceObj.loginDev(username, userpassword)

def ssh_command(username, hostip, password, command, title_p=False):
    key_password = "Password" if title_p else "password"
    ssh_newkey = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s %s' % (username, hostip, command))
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, '%s: ' % key_password])
    if i == 0:  # Timeout
        print('ERROR_1!')
        print('SSH could not login. Here is what SSH said:')
        # print(child.before, child.after)
        return None
    if i == 1:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        child.sendline('\r')
        child.expect('%s: ' % key_password)
        i = child.expect([pexpect.TIMEOUT, '%s: ' % key_password])
        if i == 0:
            # Timeout
            print('ERROR_2!')
            print('SSH could not login. Here is what SSH said:')
            #print(child.before, child.after)
            return None
        child.sendline(password)
        return child
    if i == 2:
        child.sendline(password)
        #        log.debug(str(child))
        return child

def ssh_command_test():
    username = 'seastonev2'
    hostip = '10.208.29.3'
    password = 'welcome123'
    command = 'ls'
    child = ssh_command(username, hostip, password, command)
    print(child)
    child.expect(pexpect.EOF, timeout=180)
    print(child.before.strip().decode('utf-8'))


def changePowerRestorePolicyStatus(device, ip, status, expectedvalue):
    """
    Set Power restore policy status to always off
    :param device       : product under test
    :param ip           : passing BMC IP
    :param expectedvalue: passing expected pattern 
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin raw 00 06 {status}"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd)
    if re.search(expectedvalue, output):
    	log.success("Verify IPMI command “Set Power Restore Policy” executed successfully")
    else:
        log.fail("Failed! IPMI command “Set Power Restore Policy” not executed :{output}")
        raise Exception("Failed! IPMI command “Set Power Restore Policy” not executed")

def verifyPowerRestorestatus(device, ip, exp_policy_status, exp_chassis_status, cycle=None):
    """
    verify the chassis power status and Power Restore Status through the BMC IP
    :param device            : product under test
    :param ip                : passing BMC IP 
    :param exp_policy_status : passing Expected Power Restore status
    :param exp_chassis_status: passing Expected Chassis power status
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin chassis status"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    power_restore_policy_status = re.findall(r"Power Restore Policy : (always-off|previous|always-on)", output, re.I|re.M)[0]
    Chassis_power_status = whitebox_lib.get_chassis_power_status(device=device, ip=ip)
    if (power_restore_policy_status == exp_policy_status) and (Chassis_power_status == exp_chassis_status):
        log.success(f"Verifed Power Restore Policy status is changed to {power_restore_policy_status} \
                \n      Chassis power status is {Chassis_power_status}")
    else:
        log.fail(f"Fail! Expected Power Restore Policy status:{exp_policy_status}, Power Restore Policy status:{power_restore_policy_status}")
        log.fail(f"Fail! Expected chassis power status:{exp_chassis_status}, chassis power status:{Chassis_power_status}")
        raise Exception("Fail! Power Restore Policy and chassis power status not matched")
    ChassisPower_Status = Chassis_power_status
    if cycle != None:
        if ChassisPower_Status == Chassis_power_status:
            log.success(f"Verifed the SUT power status is always restored last power state")
        else:
            log.fail(f"Fail! the SUT power status is not restored last power state")
            raise Exception("Fail! the SUT power status is not restored last power state")

def poweruptheunit(device, ip, exp_chassis_status):
    """
    After AC cycle, need to power up the unit through the BMC IP
    :param device            : product under test
    :param ip                : passing BMC IP
    :param exp_chassis_status: passing Expected Chassis power status
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin power on"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    time.sleep(120)
    Chassis_power_status = get_chassis_power_status(device=device, ip=ip)
    if Chassis_power_status == exp_chassis_status:
        log.success(f"Verifed Chassis power status is {Chassis_power_status}")
    else:
        log.fail(f"Fail! Expected chassis power status:{exp_chassis_status}, chassis power status:{Chassis_power_status}")
        raise Exception("Fail! Chassis power status not changed")

def verify_bmc_time_is_synced(device,time_output,dt=None):
    log.debug('Entering procedure verify_bmc_time_is_synced with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    line1 = '([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]).*([0-9][0-9]):([0-9][0-9]):([0-9][0-9])'

    match1 = re.search(line1, time_output)

    if match1:
        if match1.group(1) == dt['Month'] and match1.group(2) == dt['Day'] and match1.group(3) == dt['Year'] and match1.group(4) == dt['Hour']:
           log.success("BMC SEL Date and Time is in Sync with OS Time")
           Flag = True
    else:
        log.fail("BMC SEL Date and Time is not in Sync with OS Time")
        raise testFailed("BMC SEL Date and Time is not in Sync with OS Time")

def verifyIPMIcommandBMCcoldreset(device, ip):
    """
    Set Power restore policy status to always off
    :param device       : product under test
    :param ip           : passing BMC IP
    :param expectedvalue: passing expected pattern
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin mc reset cold"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    if re.search(r"Sent cold reset command to MC", output) and not(re.search("rror", output)):
        log.success("IPMI command BMC cold reset successfully")
    else:
        log.fail(f"Failed! IPMI command BMC cold reset :{output}")
        raise Exception("Failed! IPMI command not executed")

def verifyIPMIChassisControltopoweroffon(device, ip, status):
    """
    Set Power restore policy status to always off
    :param device       : product under test
    :param ip           : passing BMC IP
    :param expectedvalue: passing expected pattern
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin raw 00 02 {status}"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    if not(re.search(r"Error|error", output)):
        log.success(f"IPMI command Chassis Control to power off/on the server successfully")
    else:
        log.fail(f"Failed! IPMI command Chassis Control not able to power off/on the server :{output}")
        raise Exception("Failed! IPMI command not executed")




def verify_power_cycle_after_watchdog_timer_expiry(device):
    log.debug('Entering procedure verify_power_cycle_after_watchdog_timer_expiry with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.read_until_regexp('Sending SIGKILL to remaining processes', timeout=60)
    match = re.search('Sending SIGKILL to remaining processes', output)
    if match:
        log.success("System Power Cycled successfully after watchdog timer expiry")
    else:
        log.fail("System waw not Power Cycled after watchdog timer expiry")
        raise testFailed("System waw not Power Cycled after watchdog timer expiry")

def verify_hard_reset_after_watchdog_timer_expiry(device):
    log.debug('Entering procedure verify_hard_reset_after_watchdog_timer_expiry with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.read_until_regexp('Linux version.*gcc version', timeout=200)
    match = re.search('Linux version.*gcc version', output)
    if match:
        log.success("System Hard reset successfully after watchdog timer expiry")
    else:
        log.fail("System waw not Hard reset after watchdog timer expiry")
        raise testFailed("System waw not Hard reset after watchdog timer expiry")

def verify_power_down_after_watchdog_timer_expiry(device):
    log.debug('Entering procedure verify_power_down_after_watchdog_timer_expiry with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.read_until_regexp('Starting Power-Off', timeout=200)
    match = re.search('Starting Power-Off', output)
    if match:
        log.success("System Power Down successfully after watchdog timer expiry")
    else:
        log.fail("System waw not Power Down after watchdog timer expiry")
        raise testFailed("System waw not Power Down after watchdog timer expiry")

def Verify_IPMI_Get_Watchdog_Timer_output(output1, output2, testname, expect_same=True):
    log.debug('Entering procedure Verify_IPMI_Get_Watchdog_Timer_output with args : %s\n' %(str(locals())))
    split_output1 = output1.splitlines()[1];
    split_output2 = output2.splitlines()[1];
    log.debug(split_output1)
    log.debug(split_output2)
    if expect_same:
        if split_output1 == split_output2:
            log.info("Successfully {}: {}".format(testname, output2))
        else:
            log.fail("Fail to {}".format(testname))
            raise RuntimeError("{}".format(testname))
    else:
        if split_output1 == split_output2:
            log.fail("Fail to {}".format(testname))
            raise RuntimeError("{}".format(testname))
        else:
            log.info("Successfully {}: {}".format(testname, output2))

def verifyeventlogSELclear(device, ip):
    cmd1 = f"ipmitool -I lanplus -H {ip} -U admin -P admin sel clear"
    cmd2 = f"ipmitool -I lanplus -H {ip} -U admin -P admin sel list"
    device_obj = Device.getDeviceObject(device)
    output1 = Device.execute_local_cmd(device_obj, cmd1)
    output2 = Device.execute_local_cmd(device_obj, cmd2)
    expectedoutput1='Clearing SEL.  Please allow a few seconds to erase.'
    expectedoutput2='Event Logging Disabled #0xa0 | Log area reset/cleared | Asserted'
    if re.search(expectedoutput1, output1) and not(re.search('rror', output1)):
        log.success('IPML command cleared SEL Successfully')
    else:
        log.fail(f'IPML command failed {output1}')
        raise RuntimeError("ESM Command Failed")
    if re.search(expectedoutput2, output2) and not(re.search('rror', output2)):
        log.success('SEL is cleared and SEL event log can be read out successfully')
    else:
        log.fail(f'SEL event log not able to read out successfully {output2}')
        raise RuntimeError("ESM Command Failed")



def verifyabnormaleventlog(device, ip):
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin sel list"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd)
    expectedoutput='abnormal'
    if re.search(expectedoutput, output) and re.search('rror', output):
        log.fail(f"Abnormal event recorded in SEL :{output}")
        raise RuntimeError('Abnormal event recorded in SEL')
    else:
        log.success('Abnormal event message is not recorded in SEL')



def Generate_SEL_Logs(device,module="Athena_FW",key='SEL_GEN'):
    log.debug("Entering Generate_SEL_Logs with args : %s" %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    imageObj = SwImage.getSwImage(module)
    localdir = imageObj.localImageDir
    deviceObj.sendline('cd %s' %(localdir))
    sel_gen = imageObj.newImage[key]
    toolname='./%s' %(sel_gen)

    msg="Looks like SEL Log is Full"
    deviceObj.sendCmd(toolname,msg,10000)

    log.debug("Exited Generate_SEL_Logs proc")



def compare_mc_info_before_and_after_reset(output1, output2):
    log.debug('Entering procedure compare_mc_info_before_and_after_reset with args : %s\n' %(str(locals())))
    pattern1="Firmware Revision.*: (\S+)"
    pattern2="Manufacturer ID.*: (\S+)"
    pattern3="Manufacturer Name.*: Unknown \((\S+)\)"
    pattern4="Product ID.*: (\S+) \((\S+)\)"
    pattern5="Product Name.*: Unknown \((\S+)\)"
    output1_split=output1.splitlines()
    for line in output1_split:
        match1=re.search(pattern1,line)
        match2=re.search(pattern2,line)
        match3=re.search(pattern3,line)
        match4=re.search(pattern4,line)
        match5=re.search(pattern5,line)
        if match1:
            version=match1.group(1)
        if match2:
            mfg_id=match2.group(1)
        if match3:
            mfg_name=match3.group(1)
        if match4:
            pdct_id_1=match4.group(1)
            pdct_id_2=match4.group(2)
        if match5:
            pdct_name=match5.group(1)
    pattern1="Firmware Revision.*: {}".format(version)
    pattern2="Manufacturer ID.*: {}".format(mfg_id)
    pattern3="Manufacturer Name.*: Unknown \({}\)".format(mfg_name)
    pattern4="Product ID.*: {} \({}\)".format(pdct_id_1,pdct_id_2)
    pattern5="Product Name.*: Unknown \({}\)".format(pdct_name)
    match1=re.search(pattern1,output2)
    match2=re.search(pattern2,output2)
    match3=re.search(pattern3,output2)
    match4=re.search(pattern4,output2)
    match5=re.search(pattern5,output2)
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


def verify_command_execution(device,ip,cmd,fail_pattern):
    cmd = "{} {}".format(cmd,ip)
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    if re.search(fail_pattern, output):
        log.fail("Command not executed successfully")
        raise testFailed("Command not executed successfully")
    else:
        log.success("Command executed successfully")


def get_bmc_version_ipmitool(device,ip):
    log.debug("Entering get_bmc_version_ipmitool details args : %s" %(str(locals())))
    cmd_FM_Version = f"ipmitool -I lanplus -H {ip} -U admin -P admin mc info"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd_FM_Version)
    log.info(output)
    CurrentFWversion=re.search(r"Firmware Revision\s+:\s(\d+.\d+)",output,re.I|re.M)[1]
    return CurrentFWversion

def get_SOL_info_remote_client(device,ip,sol_active1,sol_progress1='set-complete'):
    log.debug("Entering get_SOL_info_remote_client details args : %s" %(str(locals())))
    cmd_sol_info = f"ipmitool -I lanplus -H {ip} -U admin -P admin sol info"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd_sol_info)
    sol_progress=re.search(r"Set in progress\s+:\s(.*)",output,re.I|re.M)[1]
    sol_active=re.search(r"Enabled\s+:\s(.*)",output,re.I|re.M)[1]
    if sol_active1 == sol_active and sol_progress == sol_progress1:
        log.success(f"Pass! SOL operation is {sol_active} from ipmitool")
        log.success(f"Pass! SOL \"Set in progress\" is {sol_progress} from ipmitool")
    else:
        log.fail(f"Fail! SOL operation is {sol_active} from ipmitool")
        log.fail(f"Fail! SOL \"Set in progress\" is {sol_progress} from ipmitool")
        raise RuntimeError("Fail! SOL \"Set in progress\" is not set-complete from ipmitool")

def set_SOL_looptest(device,ip,testloopcycle):
    log.debug("Entering set_SOL_looptest details args : %s" %(str(locals())))
    cmd_sol_testloop = f"ipmitool -I lanplus -H {ip} -U admin -P admin sol looptest {testloopcycle} 5000 1"
    device_obj = Device.getDeviceObject(device)
    Looptest_timeout=int(testloopcycle) * 6
    log.debug(f"Sleep {Looptest_timeout} seconds for loop test completion")
    output = Device.execute_local_cmd(device_obj, cmd_sol_testloop, timeout=int(Looptest_timeout)).strip()
    log.info(output)
    match1=re.search(r"(remain loop test counter: 1$)",output,re.I|re.M)[1]
    if match1:
        log.success(f"Successfully! SOL loop test is completed")
    else:
        raise RuntimeError(f"Fail! SOL loop test is not completed within expected time")

def compare_mc_info(output1,output2):
    log.debug('Entering procedure compare mc info before and after with some action')
    pattern1="Firmware Revision.*: (\S+)"
    output1_split=output1.splitlines()
    for line in output1_split:
        match1=re.search(pattern1,line)
        if match1:
            version=match1.group(1)
    pattern1="Firmware Revision.*: {}".format(version)
    match1=re.search(pattern1,output2)
    if match1:
        log.info("Firmware Revision check successful")
    else:
        log.info("Firmware Revision check Failed")
        raise RuntimeError("Firmware Revision check Failed")

def get_BIOS_version(device):
    log.debug("Entering get BIOS version details args : %s" %(str(locals())))
    cmd = "dmidecode -t 0"
    device_obj = Device.getDeviceObject(device)
    output = whitebox_lib.execute(device, cmd, mode=CENTOS_MODE)
    log.info(output)
    CurrentBIOSversion=re.search(r"BIOS Revision: (\S+)",output,re.I|re.M)[1]
    log.debug(f"Installed BIOS version :{CurrentBIOSversion}")
    return CurrentBIOSversion

def compare_BIOS_info(output1,output2):
    log.debug("Entering procedure compare BIOS info before and after with some action: %s" %(str(locals())))
    pattern1="BIOS Revision: (\S+)"
    output1_split=output1.splitlines()
    for line in output1_split:
        match1=re.search(pattern1,line)
        if match1:
            version=match1.group(1)
    pattern1="BIOS Revision: {}".format(version)
    match1=re.search(pattern1,output2)
    if match1:
        log.info("BIOS Revision check successful")
    else:
        log.info("BIOS Revision check Failed")
        raise RuntimeError("BIOS Revision check Failed")


def get_EventTimestamp_sel_list(sel_list_output):
    log.debug("Entering procedure get_EventTimestamp_sel_list: %s" %(str(locals())))
    pattern = r'^\W\s+2\s+\|\s+(\d{1,2}/\d{1,2}/\d{2,4})\s+\|\s+([0-9]{2}:[0-9]{2}:[0-9]{2})'
    if sel_list_output:
        match=re.search(pattern, sel_list_output, re.I|re.M)
        date_var = match.group(1).replace("/", "-")
        data_var_next = match.group(2) + "+00:00"
        date_update = date_var.split("-")
        date_update=date_update[2] + "-" + date_update[0] + "-" + date_update[1]
        return date_update + "T" + data_var_next
    else:
        log.fail("Sel output is not valide")



def check_fan_info(device,bmc_ip):
    log.debug("Entering procedure to verify fan info show up")
    device_obj = Device.getDeviceObject(device)
    mc_info_cmd="ipmitool -I lanplus -H {} -U admin -P admin mc info".format(bmc_ip)
    mc_info_op=Device.execute_local_cmd(device_obj,mc_info_cmd,timeout=60)
    log.info(mc_info_op)
    sensor_list_cmd="ipmitool -I lanplus -H {} -U admin -P admin sensor list | grep -i FAN".format(bmc_ip)
    sensor_list_op=Device.execute_local_cmd(device_obj,sensor_list_cmd,timeout=90)
    log.info(sensor_list_op)
    if re.search(fail_pattern, mc_info_op):
        log.fail("{} Command not executed successfully".format(mc_info_cmd))
        raise testFailed("{} Command not executed successfully".format(mc_info_cmd))
    else:
        log.success("{} Command executed successfully".format(mc_info_cmd))
    if re.search(fail_pattern, sensor_list_op):
        log.fail("Fan info not verified successfully")
        raise testFailed("Fan info not verified successfully")
    else:
        log.success("Fan info verified successfully")





@logThis
def check_date(device):
    device_obj = Device.getDeviceObject(device)
    c1=run_command('date')

@logThis
def disable_enable_fan_sensor(val):
    device.sendCmd('ipmitool raw 0x04 0x28 0x11 0x00 0x00 0x00 0x00 0x00')
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device.executeCmd('ipmitool raw 0x04 0x29 0x11')
    if val not in out1:
        log.success('Fan1 Rear Sensor disabled')
    else:
        raise RuntimeError('Fan1 Rear Sensor not disabled')


    #raise RuntimeError(f"Not Terminated the flash process {bmcupgrade} during bmc load driver with {module}")
    c1=run_command('ipmitool sensor list | grep -i rpm',prompt="root@localhost:~#")
    if not re.search('Fan1_Rear',c1):
        log.success(" Fan1_Rear not present")
    else:
        raise RuntimeError(" Fan1_Rear present even after sensor disabled")

    device.sendCmd('ipmitool raw 0x04 0x28 0x11 0xc0 0x04 0x00 0x04 0x00')
    c1=run_command('\n',prompt="root@localhost:~#")
    out2=device.executeCmd('ipmitool raw 0x04 0x29 0x11')
    if val in out2:
        log.success('Fan1 Rear Sensor enabled')
    else:
        raise RuntimeError('Fan1 Rear Sensor not enabled')

    c1=run_command('ipmitool sensor list | grep -i rpm',prompt="root@localhost:~#")
    if re.search('Fan1_Rear',c1):
        log.success(" Fan1_Rear present")
    else:
        raise RuntimeError(" Fan1_Rear not present even after sensor enabled")

@logThis
def disable_enable_virtual_usb(val1,val2):
    log.debug("Disable the Virtual USB status")
    device.sendCmd('ipmitool raw 0x32 0xaa 0x01')
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device.executeCmd('ipmitool raw 0x32 0xab')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Virtual USB disabled')
    else:
        raise RuntimeError('Virtual USB not disabled')

    log.debug("Enable the Virtual USB status")
    device.sendCmd('ipmitool raw 0x32 0xaa 0x00')
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device.executeCmd('ipmitool raw 0x32 0xab')
    if re.search(r'[\s]00[\s]',out1):
        log.success('Virtual USB enabled')
    else:
        raise RuntimeError('Virtual USB not enabled')

    log.debug("Disable the Virtual USB status")
    device.sendCmd('ipmitool raw 0x32 0xaa 0x01')
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device.executeCmd('ipmitool raw 0x32 0xab')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Virtual USB disabled')
    else:
        raise RuntimeError('Virtual USB not disabled')


@logThis
def verify_sel_list_power_cycle():
    log.debug("Checking for assert/working log")
    device.sendCmd('ipmitool sel list')
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device.executeCmd('ipmitool sel list')
    log.debug("Checking for the soft-off assert")
    if re.search(r'System ACPI Power State #0x0a | S5/G2: soft-off | Asserted',out1):
        log.success('Soft-off asserted')
    else:
        raise RuntimeError('Soft-off assertnot present')

    log.debug("Checking for the S0 assert")
    if re.search(r'System ACPI Power State #0x0a | S0/G0: working | Asserted',out1):
        log.success('Working log asserted')
    else:
        raise RuntimeError('Working log not present')


@logThis
def verify_sel_operation_test():
    log.debug("Checking for Sel info")
    device.sendCmd('ipmitool sel info')
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device.executeCmd('ipmitool sel list')
    log.debug("Checking if only 1 event is logged")
    if not re.search(r'[\s]+2[\s]',out1):
        log.success('Only 1 event is present')
    else:
        raise RuntimeError('More than 1 event is present')
    log.debug("Setting log filter to Circular")
    device.sendCmd('ipmitool raw 0x32 0x7F 0x01')
    out1=device.executeCmd('ipmitool raw 0x32 0x7E')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Circular log')
    else:
        raise RuntimeError('Linear log')

    log.debug("Setting log filter to Linear")
    device.sendCmd('ipmitool raw 0x32 0x7F 0x00')
    out1=device.executeCmd('ipmitool raw 0x32 0x7E')
    if re.search(r'[\s]00[\s]',out1):
        log.success('Linear log')
    else:
        raise RuntimeError('Circular log')


@logThis
def sel_policy_test(device):
    device_obj = Device.getDeviceObject(device)
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    log.debug("Generating Linear logs")
    cmd="./SELPolicy.sh"+" "+ mgmt_ip +" "+" 0" +" 10"
    res1=device_obj.executeCmd(cmd)
    time.sleep(20)
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")

    log.debug("Checking for Sel get")
    device_obj.sendCmd("ipmitool sel get 9")
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device_obj.executeCmd('ipmitool sel list')
    log.debug("Checking if only 10 event is logged")
    if not re.search(r'[\s]+11[\s]',out1):
        log.success('Only 10 event is present')
    else:
        raise RuntimeError('More than 10 event is present')
    #cmd1 = run_command(cmd,prompt ='root@localhost',timeout=1800)
    #cmd2 = "ipmitool -I lanplus -H %s -U admin -P admin chassis power %s" % (ip, status)
    #output1 = Device.execute_local_cmd(device_obj, cmd, timeout=300)
    #log.info(output1)
    verifyeventlogSELclear(device,mgmt_ip)
    log.debug("Generating Cicular logs")
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    cmd="./SELPolicy.sh"+" "+ mgmt_ip +" "+" 1" +" 10"
    res1=device_obj.executeCmd(cmd)
    time.sleep(20)
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")


    log.debug("Checking for Sel get")
    device_obj.sendCmd("ipmitool sel get 9")
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device_obj.executeCmd('ipmitool sel list')
    log.debug("Checking if only 10 event is logged")
    if not re.search(r'[\s]+11[\s]',out1):
        log.success('Only 10 event is present')
    else:
        raise RuntimeError('More than 10 event is present')
    #output1 = Device.execute_local_cmd(device_obj, cmd, timeout=300)
    #cmd1 = run_command(cmd,prompt ='root@localhost',timeout=1800)
    verifyeventlogSELclear(device,mgmt_ip)


@logThis
def out_of_record_sel(device):
    device_obj = Device.getDeviceObject(device)
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    log.debug("Generating Linear logs")
    cmd="./SELPolicy.sh"+" "+ mgmt_ip +" "+" 0" +" 3660"
    res1=device_obj.executeCmd(cmd)
    time.sleep(7200)
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")

    log.debug("Checking for Sel get")
    device_obj.sendCmd("ipmitool sel get 16")
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device_obj.executeCmd('ipmitool sel info')
    log.debug("Checking if only 100% sel is used")
    if re.search(r'Percent.*100%',out1):
        log.success('SEL is full with Linear log')
    else:
        raise RuntimeError('SEL is not full')
    #cmd1 = run_command(cmd,prompt ='root@localhost',timeout=1800)
    #cmd2 = "ipmitool -I lanplus -H %s -U admin -P admin chassis power %s" % (ip, status)
    #output1 = Device.execute_local_cmd(device_obj, cmd, timeout=300)
    #log.info(output1)
    verifyeventlogSELclear(device,mgmt_ip)
    log.debug("Generating Cicular logs")
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    cmd="./SELPolicy.sh"+" "+ mgmt_ip +" "+" 1" +" 64500"
    res1=device_obj.executeCmd(cmd)
    time.sleep(7200)
    log.info("Exiting from server..")
    device_obj.sendCmd("exit")


    log.debug("Checking for Sel get")
    device_obj.sendCmd("ipmitool sel get E10")
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device_obj.executeCmd('ipmitool sel info')
    log.debug("Checking if only 100% sel is used")
    if re.search(r'Percent.*100%',out1):
        log.success('SEL is full with Linear log')
    else:
        raise RuntimeError('SEL is not full')
    #output1 = Device.execute_local_cmd(device_obj, cmd, timeout=300)
    #cmd1 = run_command(cmd,prompt ='root@localhost',timeout=1800)
    verifyeventlogSELclear(device,mgmt_ip)

@logThis
def verify_sel_list_Fan_assert_deassert():
    log.debug("Checking for assert/deassert log")
    device.sendCmd('ipmitool sel list')
    c1=run_command('\n',prompt="root@localhost:~#")
    out1=device.executeCmd('ipmitool sel list')
    log.debug("Checking for the Fan_Front assert")
    if re.search(r'.*#.*Lower.*low.*Asserted',out1):
        log.success('Fan Low asserted')
    else:
        raise RuntimeError('Fan Low not asserted')
    log.debug("Checking for the Fan_Front deassert")
    if re.search(r'.*#.*Lower.*low.*Deasserted',out1):
        log.success('Fan Low deasserted')
    else:
        raise RuntimeError('Fan Low not Deasserted')



@logThis
def verify_fan_led_policy():
    log.debug("Switch to automatic led policy")
    device.sendCmd('ipmitool raw 0x3a 0x42 0x02 0x01')
    log.debug("Print the current LEd Policy Control")
    out1=device.executeCmd('ipmitool raw 0x3a 0x42 0x01')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Automatic LEd policy enabled')
    else:
        raise RuntimeError('Manual led policy enabled')

    log.debug("Switch to manual led policy")
    device.sendCmd('ipmitool raw 0x3a 0x42 0x02 0x00')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Print the current LEd Policy Control")
    out1=device.executeCmd('ipmitool raw 0x3a 0x42 0x01')
    if re.search(r'[\s]00[\s]',out1):
        log.success('Manual Led policy enabled')
    else:
        raise RuntimeError('Automatic led policy enabled')

    log.debug("Set Fan led color to green")
    device.sendCmd('ipmitool raw 0x3a 0x39 0x02 0x03 0x01')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify Fan led color to green")
    out1=device.executeCmd('ipmitool raw 0x3a 0x39 1 3')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Fan Led color set to green')
    else:
        raise RuntimeError('Fan led color not green')

    log.debug("Set Fan led color to amber")
    device.sendCmd('ipmitool raw 0x3a 0x39 0x02 0x03 0x02')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify Fan led color to amber")
    out1=device.executeCmd('ipmitool raw 0x3a 0x39 1 3')
    if re.search(r'[\s]02[\s]',out1):
        log.success('Fan Led color set to amber')
    else:
        raise RuntimeError('Fan led color not amber')

    log.debug("Switch to automatic led policy")
    device.sendCmd('ipmitool raw 0x3a 0x42 0x02 0x01')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Print the current LEd Policy Control")
    out1=device.executeCmd('ipmitool raw 0x3a 0x42 0x01')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Automatic Led policy enabled')
    else:
        raise RuntimeError('Manual led policy enabled')


@logThis
def verify_read_write_cpld():
    log.debug("Switch to automatic led policy")
    device.sendCmd('ipmitool raw 0x3a 0x42 0x02 0x01')
    log.debug("Turn off Write protect")
    device.sendCmd('ipmitool raw 0x3A 0x64 0x00 0x02 0x31 0x03')
    log.debug("Print the current LEd Policy Control")
    out1=device.executeCmd('ipmitool raw 0x3a 0x42 0x01')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Automatic LEd policy enabled')
    else:
        raise RuntimeError('Manual led policy enabled')

    log.debug("Switch to manual led policy")
    device.sendCmd('ipmitool raw 0x3a 0x42 0x02 0x00')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Print the current LEd Policy Control")
    out1=device.executeCmd('ipmitool raw 0x3a 0x42 0x01')
    if re.search(r'[\s]00[\s]',out1):
        log.success('Manual Led policy enabled')
    else:
        raise RuntimeError('Automatic led policy enabled')


    log.debug("Write Fan1 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xb3 0x01')

    log.debug("Write Fan2 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xb9 0x01')

    log.debug("Write Fan3 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xbf 0x01')

    log.debug("Write Fan4 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xc5 0x01')

    log.debug("Switch to default scratch register value")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0x01 0x55')

    log.debug("Get Fan1 Control LED CPLD value")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 1 0xb3')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify default CPLD Value")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0xb3')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Fan1 Led CPLD Value')
    else:
        raise RuntimeError('Fan1 CPLD Value not correct')

    log.debug("Write Fan1 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xb3 0x02')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify Fan1 CPLD Value after writing")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0xb3')
    if re.search(r'[\s]02[\s]',out1):
        log.success('Fan1 Led CPLD value written successfully')
    else:
        raise RuntimeError('Fan1 LED CPLD value not written successfully')


    log.debug("Get Fan2 Control LED CPLD value")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 1 0xb9')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify default CPLD Value")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0xb9')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Fan2 Led CPLD Value')
    else:
        raise RuntimeError('Fan2 CPLD Value not correct')

    log.debug("Write Fan2 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xb9 0x02')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify Fan2 CPLD Value after writing")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0xb9')
    if re.search(r'[\s]02[\s]',out1):
        log.success('Fan2 Led CPLD value written successfully')
    else:
        raise RuntimeError('Fan2 LED CPLD value not written successfully')

    log.debug("Get Fan3 Control LED CPLD value")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 1 0xbf')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify default CPLD Value")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0xbf')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Fan3 Led CPLD Value')
    else:
        raise RuntimeError('Fan3 CPLD Value not correct')

    log.debug("Write Fan3 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xbf 0x02')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify Fan3 CPLD Value after writing")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0xbf')
    if re.search(r'[\s]02[\s]',out1):
        log.success('Fan3 Led CPLD value written successfully')
    else:
        raise RuntimeError('Fan3 LED CPLD value not written successfully')

    log.debug("Get Fan4 Control LED CPLD value")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 1 0xc5')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify default CPLD Value")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0xc5')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Fan4 Led CPLD Value')
    else:
        raise RuntimeError('Fan4 CPLD Value not correct')

    log.debug("Write Fan4 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xc5 0x02')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify Fan4 CPLD Value after writing")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0xc5')
    if re.search(r'[\s]02[\s]',out1):
        log.success('Fan4 Led CPLD value written successfully')
    else:
        raise RuntimeError('Fan4 LED CPLD value not written successfully')

    log.debug("Write Default Fan1 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xb3 0x01')

    log.debug("Write Default Fan2 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xb9 0x01')

    log.debug("Write Default Fan3 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xbf 0x01')

    log.debug("Write Default Fan4 Led CPLD register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0xc5 0x01')

    log.debug("Get CPLD Scratch Register Value")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 1 0x01')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify default CPLD Value for scratch register")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0x01')
    if re.search(r'[\s]55[\s]',out1):
        log.success('Scratch Register Value is correct')
    else:
        raise RuntimeError('Scratch Register value not correct')

    log.debug("Write Scratch Register")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0x01 0xde')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify Scratch Register value after writing")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0x01')
    if re.search(r'[\s]de[\s]',out1):
        log.success('Scratch Register CPLD value written successfully')
    else:
        raise RuntimeError('Scratch Register CPLD value not written successfully')

    log.debug("Switch to automatic led policy")
    device.sendCmd('ipmitool raw 0x3a 0x42 0x02 0x01')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Print the current LEd Policy Control")
    out1=device.executeCmd('ipmitool raw 0x3a 0x42 0x01')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Automatic Led policy enabled')
    else:
        raise RuntimeError('Manual led policy enabled')

    log.debug("Switch to default scratch register value")
    device.sendCmd('ipmitool raw 0x3a 0x64 0 2 0x01 0x55')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify the current Scratch Register")
    out1=device.executeCmd('ipmitool raw 0x3a 0x64 0 1 0x01')
    if re.search(r'[\s]55[\s]',out1):
        log.success('Scratch Register Value is correct')
    else:
        raise RuntimeError('Scratch Register value not correct')

@logThis
def verify_alarm_led_policy():
    log.debug("Switch to automatic led policy")
    device.sendCmd('ipmitool raw 0x3a 0x42 0x02 0x01')
    log.debug("Print the current LEd Policy Control")
    out1=device.executeCmd('ipmitool raw 0x3a 0x42 0x01')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Automatic LEd policy enabled')
    else:
        raise RuntimeError('Manual led policy enabled')

    log.debug("Switch to manual led policy")
    device.sendCmd('ipmitool raw 0x3a 0x42 0x02 0x00')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Print the current LEd Policy Control")
    out1=device.executeCmd('ipmitool raw 0x3a 0x42 0x01')
    if re.search(r'[\s]00[\s]',out1):
        log.success('Manual Led policy enabled')
    else:
        raise RuntimeError('Automatic led policy enabled')

    log.debug("Set Alarm led color to green")
    device.sendCmd('ipmitool raw 0x3a 0x39 0x02 0x01 0x01')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify alarm led color to green")
    out1=device.executeCmd('ipmitool raw 0x3a 0x39 1 1')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Alarm Led color set to green')
    else:
        raise RuntimeError('alarm led color not green')

    log.debug("Set alarm led color to amber")
    device.sendCmd('ipmitool raw 0x3a 0x39 0x02 0x01 0x02')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Verify alarm led color to amber")
    out1=device.executeCmd('ipmitool raw 0x3a 0x39 1 1')
    if re.search(r'[\s]02[\s]',out1):
        log.success('alarm Led color set to amber')
    else:
        raise RuntimeError('Alarm led color not amber')

    log.debug("Switch to automatic led policy")
    device.sendCmd('ipmitool raw 0x3a 0x42 0x02 0x01')
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Print the current LEd Policy Control")
    out1=device.executeCmd('ipmitool raw 0x3a 0x42 0x01')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Automatic Led policy enabled')
    else:
        raise RuntimeError('Manual led policy enabled')


@logThis
def dual_bmc_test(val):
    log.debug("Print current bmc image")
    out1=device.executeCmd('ipmitool raw 0x32 0x8f 0x07')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Primary Version is selected')
    else:
        log.success('Secondary Version is selected')

    log.debug("Switching the image with user provided value")
    device.sendCmd("ipmitool raw 0x32 0x8f 0x01 %s" %(val))
    c1=run_command('\n',prompt="root@localhost:~#")
    log.debug("Print the switched version")
    out1=device.executeCmd('ipmitool raw 0x32 0x8f 0x02')
    if re.search(r'[\s]01[\s]',out1):
        log.success('Primary version is selected')
    else:
        log.success('Secondary version is selected')


@logThis
def check_switched_bmc(val):
    log.debug("Print current bmc image")
    out1=device.executeCmd('ipmitool raw 0x32 0x8f 0x07')
    cmd='ipmitool raw 0x32 0x8f 0x07'
    c1=run_command(cmd,prompt="root@localhost:~#")
    match=re.search(val,c1)
    if match:
        log.success("bmc version info is correct.")
    else:
        raise RuntimeError('bmc version is not correct')

@logThis
def event_generation_test(device,sensor_num):
    device_obj = Device.getDeviceObject(device)
    log.info("Clear Sel list before running sensor event generation script")
    device_obj.executeCmd("ipmitool sel clear")
    time.sleep(20)
    device_obj.executeCmd("dhclient -v ma1")
    log.info("Downloading script into server...")
    device_obj.executeCmd("wget http://"+scp_ip+":"+seastone_home_path+event_generation_script)
    log.info("Allocating permissions to execute this script.")
    device_obj.executeCmd("chmod 777 %s" %event_generation_script)
    cmd1 = run_command("./event_generation_test.sh -K %s" %(sensor_num),prompt ='root@localhost',timeout=1800)

@logThis
def power_cycle_via_linux_server(device):
    device_obj = Device.getDeviceObject(device)
    SEASTONECommonLib.check_server_seastone(device, scp_ip, scp_username, scp_password, dhcp_prompt)
    cmd1 = 'ipmitool -I lanplus -H '+ mgmt_ip + ' -U '+user_name+' -P '+ str(user_pass) +' chassis power cycle'

    res1=device_obj.executeCmd(cmd1)

    log.info("Device Power cycled")
    device_obj.sendCmd("exit")

@logThis
def power_cycle_onl(device,bmc_ip):
    device_obj = Device.getDeviceObject(device)
    mc_info_cmd="ipmitool -I lanplus -H {} -U admin -P admin mc info".format(bmc_ip)
    mc_info_op=Device.execute_local_cmd(device_obj,mc_info_cmd,timeout=60)
    log.info(mc_info_op)
    #cmd2 = "ipmitool -I lanplus -H %s -U admin -P admin chassis power %s" % (ip, status)
    output1 = Device.execute_local_cmd(device_obj, mc_info_cmd, timeout=300)
    log.info(output1)

@logThis
def power_off_onl(device,bmc_ip):
    device_obj = Device.getDeviceObject(device)
    mc_info_cmd="ipmitool -I lanplus -H {} -U admin -P admin mc info".format(bmc_ip)
    mc_info_op=Device.execute_local_cmd(device_obj,mc_info_cmd,timeout=60)
    log.info(mc_info_op)
    #cmd2 = "ipmitool -I lanplus -H %s -U admin -P admin chassis power %s" % (ip, status)
    output1 = Device.execute_local_cmd(device_obj, mc_info_cmd, timeout=300)
    log.info(output1)

@logThis
def power_on_onl(device,bmc_ip):
    device_obj = Device.getDeviceObject(device)
    mc_info_cmd="ipmitool -I lanplus -H {} -U admin -P admin mc info".format(bmc_ip)
    mc_info_op=Device.execute_local_cmd(device_obj,mc_info_cmd,timeout=60)
    log.info(mc_info_op)
    #cmd2 = "ipmitool -I lanplus -H %s -U admin -P admin chassis power %s" % (ip, status)
    output1 = Device.execute_local_cmd(device_obj, mc_info_cmd, timeout=300)
    log.info(output1)

@logThis
def power_reset_onl(device,bmc_ip):
    device_obj = Device.getDeviceObject(device)
    mc_info_cmd="ipmitool -I lanplus -H {} -U admin -P admin mc info".format(bmc_ip)
    mc_info_op=Device.execute_local_cmd(device_obj,mc_info_cmd,timeout=60)
    log.info(mc_info_op)
    #cmd2 = "ipmitool -I lanplus -H %s -U admin -P admin chassis power %s" % (ip, status)
    output1 = Device.execute_local_cmd(device_obj, mc_info_cmd, timeout=160)
    log.info(output1)


@logThis
def show_pef_filter():
    log.debug("Show PEF Filter list")
    device.sendCmd('ipmitool pef filter list')

def send_cmd(device, cmd, ip=None, return_res=False):
    device_obj = Device.getDeviceObject(device)
    if ip:
        if "ipmitool " in cmd:
            cmd = cmd.replace("ipmitool ", "")
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin %s" % (ip, cmd)
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        res = device_obj.executeCmd(cmd)
   
    if return_res:
        return res

def check_cmd_response(device, cmd, re_exp, decide=True, ip=None, re_S=False):
    """
    send cmd and check the return if re_exp in it.
    :param device: product under test
    :param cmd: send cmd
    :param re_exp: Expected return value, supports regular expressions
    :param decide: Does the expectation exist？
    :param ip:bmc ip
    :param re_S:re.S
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        if "ipmitool " in cmd:
            cmd = cmd.replace("ipmitool ", "")
        cmd = r"ipmitool -I lanplus -H %s -U admin -P admin %s" % (ip, cmd)
        res, errs = Device.execute_local_cmd(device_obj, cmd, return_errs=True)
        res = res + errs
        rec = re.findall("%s" % re_exp, res)
        if re_S:
            rec = re.findall("%s" % re_exp, res, re.S)
        if rec:
            if not decide:
                PRINTE("expected [%s] does not exist, but it actually exists：\n[%s]" % (re_exp, res))
        else:
            if decide:
                PRINTE("expected [%s] exist, but it does not actually exist. response:\n%s" % (re_exp, res))
    else:
        res = device_obj.executeCmd(cmd)
        if "ipmitool" in cmd:
            b = re.findall(".*ipmitool(.*)real.*", res, re.S)
        else:
            b = re.findall("time %s[\r|\n]*(.*)real.*" % cmd, res, re.S)
        a = b[0].split("\n")
        a.remove(a[0])
        res_c = ""
        for i in a:
            res_c += i + "\n"
        rec = re.findall(r"%s" % re_exp, res_c)
        if re_S:
            rec = re.findall(r"%s" % re_exp, res_c, re.S)
        if rec:
            if not decide:
                PRINTE("expected [%s] does not exist, but it actually exists[%s]" % (re_exp, res))
        else:
            if decide:
                PRINTE("expected [%s] exist, but it does not actually exist. response:\n%s" % (re_exp, res))

def set_pef_config(device, num, data):
    """
    Use with get_pef_config，Set PEF according to its return value
    :param device:product under test
    :param num:Location to be set
    :param data:get_pef_config  return value
    """
    data = re.findall(r"\s{0,}11(.*)", data)[0].strip()
    a = data.split(" ")
    all_info = ""
    for i in a:
        i = "0x%s" % i
        all_info = all_info + " %s" % i
    cmd = "ipmitool raw 04 0x12 0x%s %s" % (num, all_info)
    send_cmd(device, cmd)

def set_pef_filter_close(device, num):
    """
    Close PEF filter
    :param device: product under test
    :param num: Fill in the decimal number 1 to 40 or 'all' to close all filter
    """
    device_obj = Device.getDeviceObject(device)
    if num.lower() == "all":
        for i in range(1, 41):
            cmd = "ipmitool raw 0x04 0x12 0x06 %s 0x00 0x05 0x01 0x10 0x20 0x00 0x02 0xff 0xff 0xff 0xff 0 0 0 0 0 0 " \
                  "0 0 0" % str(hex(i))
            res = device_obj.executeCmd(cmd)

##Watchdog####################
def set_watchdog_timer(device, use, actions, timeout="1"):
    """
    Set watchdog timer: "timer use", "and timer action", "countdown value".
    :param device: the name of the tested product
    :param use:
             0:reserved reserved bit, useless
             1:BIOS FRB2
             2: BIOS/POST power-on self-test
             3: OS Land system loading
             4: SMS/OS
             5: Customized functions generated by OEM
    :param actions:
             0: do nothing
             1: BMC restart
             2: Power off the system (remember to power it back on at the end)
             3: system restart
    :param timeout: After the watchdog is set, the trigger time countdown, in seconds
    """
    device_obj = Device.getDeviceObject(device)
    cmd = r"ipmitool raw 0x06 0x24 0x%s 0x%s 0x%s 0x00 0x1f 0x00" % (use.zfill(2), actions.zfill(2), timeout.zfill(2))
    res = device_obj.executeCmd(cmd)
    if "Unable to send RAW command" in res:
        PRINTE("Fail! send cmd: %s \t response:\n%s" % (cmd, res))

def set_watchdog_start(device):
    """
    Send 'ipmitool raw 0x06 0x22' to start watchdog
    """
    cmd = "ipmitool raw 0x06 0x22"
    device_obj = Device.getDeviceObject(device)
    res = device_obj.executeCmd(cmd)

def check_watchdog_update(device, use, actions, timeout=1, decide=True):
    """
    Check whether the watchdog has been set successfully (check only the first three bytes returned by the command)
    :param device: the name of the tested product
    :param use: expected use, parameter range view set_watchdog_timer
    :param actions: expected actions, parameter range view set_watchdog_timer
    :param timeout: expected timeout, parameter range see set_watchdog_timer
    :param decide: whether it meets expectations
    """
    cmd = "ipmitool raw 0x06 0x25"
    device_obj = Device.getDeviceObject(device)
    res = device_obj.executeCmd(cmd)
    res_info = re.findall(r"\w+ \w+ \w+ \w+ \w+ \w+ \w+ \w+", res)
    if not res_info:
        PRINTE("Fail! can not get watchdog info. response:\n%s" % res)
    exp_set = "%s %s %s" % (use.zfill(2), actions.zfill(2), str(timeout).zfill(2))
    if exp_set == res_info[0][:8]:
        if decide:
            log.info("Pass!")
            return True
        else:
            PRINTE("Fail! response:\n%s,exp_set=%s" % (res_info, exp_set))
    else:
        if decide:
            PRINTE("Fail! response:\n%s,exp_set=%s" % (res_info, exp_set))
        else:
            log.info("Pass!")
            return True

def check_watchdog_counting_down(device, step=1, timeout=20, continue_wait=0, ip=None):
    """
    Check if the watchdog is counting down
    :param device: product under test
    :param step: wait time after each check
    :param timeout: check timeout
    :param continue_wait: Continue to wait after the timeout period. Generally used when the product is in the restart
                          waiting time after the watchdog expires
    :param ip: When there is no IP, telnet is the tested product, otherwise, enter BMC through IP to obtain information
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin  raw 0x06 0x25" % ip
    else:
        cmd = "ipmitool raw 0x06 0x25"
    count_list = list()
    start = time.time()
    while time.time() - start <= int(timeout):
        if ip:
            res = Device.execute_local_cmd(device_obj, cmd)
            res_info = re.findall(r"\w+ \w+ \w+ \w+ \w+ \w+ (\w+) \w+", res)
            if not res_info:
                PRINTE("Fail! can not get watchdog info. response:\n%s" % res)
            count_num = int(res_info[0], 16)
            if count_num != 0:
                count_list.append(count_num)
            else:
                break
            time.sleep(step)
        else:
            res = device_obj.executeCmd(cmd)
            res_info = re.findall(r"\w+ \w+ \w+ \w+ \w+ \w+ (\w+) \w+", res)
            if not res_info:
                PRINTE("Fail! can not get watchdog info. response:\n%s" % res)
            count_num = int(res_info[0], 16)
            if count_num != 0:
                count_list.append(count_num)
            else:
                break
            time.sleep(step)
    if len(list(set(count_list))) == 1:
        PRINTE("Fail! watchdog isn't counting down, got counting down info:%s" % str(count_list))
    count_list_old = count_list.copy()
    count_list.sort(reverse=True)
    if count_list != count_list_old:
        PRINTE("Fail! counting down list:%s, expected list:%s" % (str(count_list_old), str(count_list)))
    set_wait(continue_wait)

def check_bmc_sel_list_keyword(device, keyword, decide=True, ip=None):
    """
    Check whether there are expected keywords in the log records of ipmitool sel list in BMC.
    Please clear sel information before calling
    Avoid false detections
    :param device: the name of the tested product
    :param keyword: Incoming string, when multiple expected characters need to be checked, write them as the same string
                    separated by','
    :param decide: whether the expectation exists
    :param ip: When ip is None, use direct access to obtain information, otherwise use remote access to obtain information
    """
    res = get_sel_list(device, ip=ip, return_info=True)
    flag = True
    if "," in keyword:
        keyword_list = keyword.split(",")
        for word in keyword_list:
            res_re = re.findall(r"%s" % word, res)
            if len(res_re) > 1:
                PRINTE("Fail! Keyword:%s Frequency of occurrence is greater than 1" % word)
            if decide:
                if not res_re:
                    PRINTE("Fail! couldn't find the keyword:[%s].response:\n%s" % (word, res), decide=False)
                    flag = False
            else:
                if res_re:
                    PRINTE("Fail! find the keyword:[%s].response:\n%s" % (word, res), decide=False)
                    flag = False
    else:
        res_re = re.findall(r"%s" % keyword, res)
        if len(res_re) > 1:
            PRINTE("Fail! Keyword:%s Frequency of occurrence is greater than 1" % keyword)
        if decide:
            if not res_re:
                PRINTE("Fail! couldn't find the keyword:[%s].response:\n%s" % (keyword, res), decide=False)
                flag = False
        else:
            if res_re:
                PRINTE("Fail! find the keyword:[%s].response:\n%s" % (keyword, res), decide=False)
                flag = False
    if not flag:
        raise RuntimeError("Fail! check_bmc_sel_list_keyword") 

def get_sel_list(device, ip=None, return_info=False):
    """
    get sel info
    :param device: the name of the tested product
    :param ip: BMC ip
    :param return_info: return info or not
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin sel list" % ip
        res = Device.execute_local_cmd(device_obj, cmd, 120)
    else:
        cmd = r"ipmitool sel list"
        res = device_obj.executeCmd(cmd)
    if return_info:
        return res

def set_wait(wait_time):
    log.info("[%s]: pls wait %s s" % (datetime.now(), wait_time))
    time.sleep(float(wait_time))

####

@logThis
def check_reboot(device):
    device=Device.getDeviceObject(device)
    device.sendCmd('reboot')
    device.read_until_regexp('localhost login:',timeout=300)
    device.loginDiagOS()

@logThis
def check_date(device):
    device_obj = Device.getDeviceObject(device)
    c1=run_command('date')

@logThis
def check_date_os(device):
    c1=run_command('date',prompt="root@localhost:~#")

@logThis
def get_dhcp_onl_ip(device):
    c1=run_command('dhclient -v ma1',prompt="root@localhost:~#")

# TC - 11.1.4
@logThis
def check_bmc_version():
    cmd='ipmitool mc info'
    c1=run_command(cmd,prompt="root@localhost:~#")
    CommonKeywords.should_match_paired_regexp_list(c1,bmc_version_info_list)
    log.success("bmc version info is correct.")

@logThis
def reset_bmc(coldOrwarm):
    cmd="ipmitool mc reset "+coldOrwarm
    c1=run_command(cmd,prompt="root@localhost:~#")
    pattern = "Sent "+ coldOrwarm +" reset command to MC"
    if(pattern in c1):
        log.success("bmc reset " + coldOrwarm + " executed successfully.")
    else:
        raise RuntimeError("bmc reset "+ coldOrwarm + " failed !!")
    time.sleep(300)

