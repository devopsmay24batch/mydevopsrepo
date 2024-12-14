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
from JuniperAberlourSdkVariable import *
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
    cmd="./%s %s"%(SDK_SCRIPT, option)
    prompt=Device.promptDiagOs if option == "-d" else BCM_promptstr
    output=device.executeCommand(cmd, prompt, timeout=90)
    for pattern in fail_pattern:
        if pattern in output:
            raise Exception("Find errors when execute {}.".format(cmd))
    log.info('%s is passed\n' %cmd)


@logThis
def check_phy_info():
    output=device.executeCommand("epdm phy info all",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output,phy_info_patterns)
    log.success("check_phy_info successfully.")


@logThis
def check_mdio_advisor():
    output = device.executeCommand('config show rate_ext_mdio_divisor', BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output, mdio_advisor_pattern)
    log.success('check_mdio_advisor successfully.')





@logThis
def check_prbs_ports_sys_side():
    device.executeCommand("phy diag ce0-ce1 prbs get",BCM_promptstr)

    output1=device.executeCommand("phy diag ce0-ce1 prbs get",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output1, prbs_get_pattern)
    time.sleep(300)

    output2=device.executeCommand("epdm prbs get ce0-ce1 lane=all if=sys",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output2, prbs_sys_ce_pattern)

    output3=device.executeCommand("phy diag ce0-ce1 prbs get",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output3, prbs_get_pattern)

    device.executeCommand("phy diag ce0-ce1 prbs clear",BCM_promptstr)
    log.success("check_prbs_ports_sys_side successfully executes.")



@logThis
def check_prbs_ports_line_side():
    output1=device.executeCommand("epdm prbs get ce0 lane=1 if=line",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output1, prbs_ce_pattern)

    output2=device.executeCommand("epdm prbs get ce1 lane-0 if=line",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output2, prbs_ce_pattern)

    log.success("check_prbs_ports_line_side successfylly executes")

@logThis
def remove_all_related_modules():
    output=device.executeCommand("./auto_load_user.sh -r",'root@localhost') 
    CommonKeywords.should_match_a_regexp(output,"uninstall all modules and files.")
    log.success("remove_all_related_modules executes successfully.")


@logThis
def change_qsfp28_100g_speed_to_40g_speed():
    #device.executeCommand("config add plp_speed_25=40000",BCM_promptstr)
    #device.executeCommand("config add plp_speed_26=40000",BCM_promptstr)
    #device.executeCommand("config add plp_speed_27=40000",BCM_promptstr)
    #device.executeCommand("config add portmap_25=65:40:4",BCM_promptstr)
    #device.executeCommand("config add portmap_26=69:40:4",BCM_promptstr)
    #device.executeCommand("config add portmap_27=73:40:4",BCM_promptstr)
    #device.executeCommand("config add epdm_speed_24=40000",BCM_promptstr)
    #device.executeCommand("config add epdm_speed_25=40000",BCM_promptstr)
    #device.executeCommand("config add epdm_speed_26=40000",BCM_promptstr)
    #device.executeCommand("config add epdm_system_intf_24=24",BCM_promptstr)
    #device.executeCommand("config add epdm_system_intf_25=24",BCM_promptstr)
    #device.executeCommand("config add epdm_system_intf_26=24",BCM_promptstr)
    #device.executeCommand("config save",BCM_promptstr)
    #device.executeCommand("exit",'root@localhost SDK')
    check_ps_and_epdm_port_link_status_and_speed()

    output1= device.executeCommand("epdm speed europa 40000",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output1, "first =europa,second=40000 speed1=40000")

    cmd="port ce sp=40000"
    output2= device.executeCommand(cmd,BCM_promptstr)
    for value in fail_pattern:
        if value in output2:
            raise Exception("Error in executing "+ cmd)
    log.success("change_qsfp28_100g_speed_to_40g_speed executes successfully.")


@logThis
def check_port_link_status_changes_to_40G_from_100G():
    #device.executeCommand("./bcm.user", BCM_promptstr, timeout=90)
    time.sleep(5)
    output=device.executeCommand("ps",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output, ps_40G_pattern)

    output2= device.executeCommand("epdm link all",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output2, epdm_40G_pattern)

    log.success("check_port_link_status_changes_to_40G_from_100G executes successfully.")


@logThis
def check_100G_stacking_packet_counter():
    cmd="linespeed run exts 25-26 1518 20 60"
    linespeed_output=device.executeCommand(cmd,BCM_promptstr,timeout=90)
    CommonKeywords.should_match_ordered_regexp_list(linespeed_output,linespeed_100G_stacking_traffic_pattern_start)
    CommonKeywords.should_match_ordered_regexp_list(linespeed_output,linespeed_100G_stacking_traffic_pattern_end)

    linespeed_dict=CommonLib.parseDict(output=linespeed_output, pattern_dict=linespeed_100G_stacking_dict_pattern, sep_field=" ")


    for port in range(24,26):
        linespeed_port_key="Port"+str(port+1)+" 100G Linespeed test"
        value= linespeed_dict[linespeed_port_key]
        tpok_rpok_dict= CommonLib.parseDict(output=value, pattern_dict=tpok_rpok_dict_pattern, sep_field=":")

        tpok_val=list(tpok_rpok_dict["TPOK"].split())
        tpok_val=tpok_val[0].strip()

        rpok_val=list(tpok_rpok_dict["RPOK"].split())
        rpok_val=rpok_val[0].strip()


        if(tpok_val!= rpok_val):
            raise Exception("TPOK and RPOK values of port "+str(port +1) +" is not equal : "+tpok_val + rpok_val)



        cmd="epdm counter show "+str(port)
        output=device.executeCommand(cmd,BCM_promptstr)

        epdm_counter_tpok_rpok_value_list=[]
        epdm_counter_tpok_rpok_value_list.append("MIB_TPOK\."+str(port)+".*?"+tpok_val)
        epdm_counter_tpok_rpok_value_list.append("MIB_RPOK\."+str(port)+".*?"+tpok_val)
        epdm_counter_tpok_rpok_value_list.append("MIB_TPKT\."+str(port)+".*?"+tpok_val)
        epdm_counter_tpok_rpok_value_list.append("MIB_RPKT\."+str(port)+".*?"+tpok_val)


        CommonKeywords.should_match_ordered_regexp_list(output, epdm_counter_tpok_rpok_value_list)



    log.success("check_100G_stacking_packet_counter executest successfully")

@logThis
def check_100G_stacking_packet_counter_after_clear():
    for i in range(24,26):
        cmd="epdm counter show "+str(i)
        A_100G_packet_pattern="MIB.*?"+str(i)+".*?0.*"
        output=device.executeCommand(cmd,BCM_promptstr)
        CommonKeywords.should_match_a_regexp(output,A_100G_packet_pattern)

    log.success("check_100G_stacking_packet_counter_after_clear executest successfully")


@logThis
def clear_100G_stacking_packet_counter():
    for i in range(24,26):
        cmd="epdm counter clear "+str(i)
        device.executeCommand(cmd,BCM_promptstr)
    log.success("clear_100G_stacking_packet_counter executes successfully")


@logThis
def check_10G_packet_counter():
    cmd="linespeed run exts 1-24 1518 20 60"
    linespeed_output=device.executeCommand(cmd,BCM_promptstr,timeout=90)
    CommonKeywords.should_match_ordered_regexp_list(linespeed_output,linespeed_10G_traffic_pattern_start)
    CommonKeywords.should_match_ordered_regexp_list(linespeed_output,linespeed_10G_traffic_pattern_end)
    
    linespeed_dict=CommonLib.parseDict(output=linespeed_output, pattern_dict=linespeed_10G_dict_pattern, sep_field=" ")


    for port in range(24):
        linespeed_port_key="Port"+str(port+1)+" 10G Linespeed test"
        value= linespeed_dict[linespeed_port_key]
        tpok_rpok_dict= CommonLib.parseDict(output=value, pattern_dict=tpok_rpok_dict_pattern, sep_field=":")

        tpok_val=list(tpok_rpok_dict["TPOK"].split())
        tpok_val=tpok_val[0].strip()

        rpok_val=list(tpok_rpok_dict["RPOK"].split())
        rpok_val=rpok_val[0].strip()


        if(tpok_val!= rpok_val):
            raise Exception("TPOK and RPOK values of port "+str(port +1) +" is not equal : "+tpok_val + rpok_val)
    
        

        cmd="epdm counter show "+str(port)
        output=device.executeCommand(cmd,BCM_promptstr)

        epdm_counter_tpok_rpok_value_list=[]
        epdm_counter_tpok_rpok_value_list.append("MIB_TPOK\."+str(port)+".*?"+tpok_val)
        epdm_counter_tpok_rpok_value_list.append("MIB_RPOK\."+str(port)+".*?"+tpok_val)
        epdm_counter_tpok_rpok_value_list.append("MIB_TPKT\."+str(port)+".*?"+tpok_val)
        epdm_counter_tpok_rpok_value_list.append("MIB_RPKT\."+str(port)+".*?"+tpok_val)


        CommonKeywords.should_match_ordered_regexp_list(output, epdm_counter_tpok_rpok_value_list)



    log.success("check_10G_packet_counter executes successfully")

@logThis
def check_10G_packet_counter_after_clear():
    for i in range(24):
        A_10G_packet_pattern="MIB.*?"+str(i)+".*?0.*"

        cmd="epdm counter show "+str(i)
        output=device.executeCommand(cmd,BCM_promptstr)
        o1=list(output.split("\n"))
        cnt=0

        for line in o1:
            status=bool(re.search(A_10G_packet_pattern,line))
            if status:
                cnt+=1
        if(cnt!=25):
            log.fail("Check_10G_packet_counter has some error")
    log.success("check_10G_packet_counter_after_clear executest successfully")

@logThis
def clear_10G_packet_counter():
    for i in range(24):

        cmd="epdm counter clear "+str(i)
        device.executeCommand(cmd,BCM_promptstr)
    log.success("clear_10G_packet_counter executes successfully")


@logThis
def check_100G_uplink_packet_counter():
    cmd="linespeed run exts 27 1518 20 60"
    linespeed_output=device.executeCommand(cmd,BCM_promptstr,timeout=90)
    CommonKeywords.should_match_ordered_regexp_list(linespeed_output,linespeed_100G_uplink_traffic_pattern_start)
    CommonKeywords.should_match_ordered_regexp_list(linespeed_output,linespeed_100G_uplink_traffic_pattern_end)

    linespeed_dict=CommonLib.parseDict(output=linespeed_output, pattern_dict=linespeed_100G_uplink_dict_pattern, sep_field=" ")


    for port in range(26,27):
        linespeed_port_key="Port"+str(port+1)+" 100G Linespeed test"
        value= linespeed_dict[linespeed_port_key]
        tpok_rpok_dict= CommonLib.parseDict(output=value, pattern_dict=tpok_rpok_dict_pattern, sep_field=":")

        tpok_val=list(tpok_rpok_dict["TPOK"].split())
        tpok_val=tpok_val[0].strip()

        rpok_val=list(tpok_rpok_dict["RPOK"].split())
        rpok_val=rpok_val[0].strip()


        if(tpok_val!= rpok_val):
            raise Exception("TPOK and RPOK values of port "+str(port +1) +" is not equal : "+tpok_val + rpok_val)



        cmd="epdm counter show "+str(port)
        output=device.executeCommand(cmd,BCM_promptstr)

        epdm_counter_tpok_rpok_value_list=[]
        epdm_counter_tpok_rpok_value_list.append("MIB_TPOK\."+str(port)+".*?"+tpok_val)
        epdm_counter_tpok_rpok_value_list.append("MIB_RPOK\."+str(port)+".*?"+tpok_val)
        epdm_counter_tpok_rpok_value_list.append("MIB_TPKT\."+str(port)+".*?"+tpok_val)
        epdm_counter_tpok_rpok_value_list.append("MIB_RPKT\."+str(port)+".*?"+tpok_val)


        CommonKeywords.should_match_ordered_regexp_list(output, epdm_counter_tpok_rpok_value_list)




    log.success("check_100G_uplink_packet_counter executest successfully")

@logThis
def check_100G_uplink_packet_counter_after_clear():

    cmd="epdm counter show 26"
    output=device.executeCommand(cmd,BCM_promptstr)
    o1=list(output.split("\n"))
    cnt=0

    for line in o1:
        status=bool(re.search(A_100G_uplink_packet_pattern,line))
        if status:
            cnt+=1
    if(cnt!=25):
        log.fail("Check_100G_uplink_packet_counter has some error")
    log.success("check_100G_uplink_packet_counter_after_clear executest successfully")


@logThis
def clear_100G_uplink_packet_counter():

    cmd="epdm counter clear 26"
    device.executeCommand(cmd,BCM_promptstr)
    log.success("clear_100G_uplink_packet_counter executes successfully")


@logThis
def check_uplink_prbs_ports_sys_side():
    device.executeCommand("phy diag ce2 prbs get",BCM_promptstr)

    output1=device.executeCommand("phy diag ce2 prbs get",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output1, prbs_get_pattern)
    time.sleep(300)

    output2=device.executeCommand("epdm prbs get ce2 lane=all if=sys",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output2, prbs_ce_pattern)

    output3=device.executeCommand("phy diag ce2 prbs get",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output3, prbs_get_pattern)

    device.executeCommand("phy diag ce2 prbs clear",BCM_promptstr)
    log.success("check_uplink_prbs_ports_sys_side successfully executes.")


@logThis
def check_uplink_prbs_ports_line_side():
    output1=device.executeCommand("epdm prbs get ce2 lane=all if=line",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output1, prbs_ce_pattern)

    log.success("check_uplink_prbs_ports_line_side successfylly executes")


@logThis
def start_prbs_sys_generator():
    output1=device.executeCommand("epdm link all", BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output1, epdm_pattern)

    lane=0
    for port in range(0,24):
        cmd="epdm prbs set xe"+ str(port) + " tx_rx=0 p=5 lane="+str(lane)+" inv=0 if=sys"
        lane+=1
        if lane==4:
            lane=0

        output=device.executeCommand(cmd,BCM_promptstr)
        for value in fail_pattern:
            if value in output:
                raise Exception(" Error in " +cmd)

 

    device.executeCommand("phy diag xe0-xe23 prbs set p=3",BCM_promptstr)
    device.executeCommand("phy diag xe0-xe23 prbs get",BCM_promptstr)

    output2=device.executeCommand("phy diag xe0-xe23 prbs get",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output2, all_prbs_get_pattern)
    log.success("start_prbs_sys_generator executes successfully.")


@logThis
def check_all_sys_prbs():
    lane=0
    for port in range(0,24):
        cmd="epdm prbs get xe"+ str(port) + " lane="+str(lane)+" if=sys"
        lane+=1
        if lane==4:
            lane=0

        output=device.executeCommand(cmd,BCM_promptstr)
        CommonKeywords.should_match_ordered_regexp_list(output,prbs_xe_pattern)  

    o1=device.executeCommand("phy diag xe0-xe23 prbs get", BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(o1,all_prbs_get_pattern)

    device.executeCommand("phy diag xe0-xe23 prbs clear", BCM_promptstr)

    log.success("check_all_sys_prbs executes successfully.")


def start_prbs_line_generator():
    output1=device.executeCommand("epdm link all", BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output1, epdm_pattern)

    lane=0
    for port in range(0,24):
        cmd="epdm prbs set xe"+ str(port) + " tx_rx=0 p=5 lane="+str(lane)+" inv=0 if=line"
        lane+=1
        if lane==4:
            lane=0

        output=device.executeCommand(cmd,BCM_promptstr)
        for value in fail_pattern:
            if value in output:
                raise Exception(" Error in " +cmd)
    
    log.success("start_prbs_line_generator executes successfully.")

@logThis
def check_all_line_prbs():
    lane=0
    for port in range(0,24):
        cmd="epdm prbs get xe"+ str(port) + " lane="+str(lane)+" if=line"
        lane+=1
        if lane==4:
            lane=0

        output=device.executeCommand(cmd,BCM_promptstr)
        CommonKeywords.should_match_ordered_regexp_list(output,prbs_xe_pattern)

    log.success("check_all_line_prbs executes successfully.")



@logThis 
def check_downlink_10g_fec_status(enable, typo_, sys_or_line):
    cmd="epdm fec status xe0 if="+sys_or_line
    output=device.executeCommand(cmd, BCM_promptstr)

    status="enable" if enable=="1" else "disable"
    typo_=typo_.upper()
    pattern="xe0.*?1.*?FEC.*?"+str(typo_)+".*Status : "+status
    

    CommonKeywords.should_match_a_regexp(output,pattern)
    log.success(cmd+"executes successfylly.")
    
  



@logThis 
def downlink_10g_interface_enable_disable(enable,typo_,sys_or_line):
    cmd="epdm fec set xe0 enable="+enable+" if="+sys_or_line+" type="+typo_
    device.executeCommand(cmd, BCM_promptstr)
    check_downlink_10g_fec_status(enable=enable, typo_=typo_, sys_or_line=sys_or_line)

@logThis
def check_uplink_100g_fec_status(enable, typo_, sys_or_line):
    cmd="epdm fec status ce2 if="+sys_or_line
    output=device.executeCommand(cmd, BCM_promptstr)

    status="enable" if enable=="1" else "disable"
    typo_=typo_.upper()
    pattern="ce2.*?27.*?FEC.*?"+str(typo_)+".*Status : "+status+".*"


    CommonKeywords.should_match_a_regexp(output,pattern)
    log.success(cmd+"executes successfylly.")





@logThis
def uplink_100g_interface_enable_disable(enable,typo_,sys_or_line):
    cmd="epdm fec set ce2 enable="+enable+" if="+sys_or_line+" type="+typo_
    device.executeCommand(cmd, BCM_promptstr)
    check_uplink_100g_fec_status(enable=enable, typo_=typo_, sys_or_line=sys_or_line)



@logThis
def check_stacking_100g_fec_status(enable, typo_, sys_or_line):
    cmd="epdm fec status ce0-ce1 if="+sys_or_line
    output=device.executeCommand(cmd, BCM_promptstr)

    status="enable" if enable=="1" else "disable"
    typo_=typo_.upper()
    pattern1="ce0.*?25.*?FEC.*?"+str(typo_)+".*Status : "+status+".*"
    pattern2="ce1.*?26.*?FEC.*?"+str(typo_)+".*Status : "+status+".*"
    
    CommonKeywords.should_match_a_regexp(output,pattern1)
    CommonKeywords.should_match_a_regexp(output,pattern2)
    log.success(cmd+"executes successfylly.")





@logThis
def stacking_100g_interface_enable_disable(enable,typo_,sys_or_line):
    cmd="epdm fec set ce0-ce1 enable="+enable+" if="+sys_or_line+" type="+typo_
    device.executeCommand(cmd, BCM_promptstr)
    check_stacking_100g_fec_status(enable=enable, typo_=typo_, sys_or_line=sys_or_line)



@logThis
def check_port_link_and_status():
    output=device.executeCommand("ps",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output, ps_100G_pattern)
    log.success("check_port_link_status executes successfully.")

@logThis
def start_led_status():
    device.executeCommand("led auto on",BCM_promptstr)
    device.executeCommand("led start",BCM_promptstr)
    log.success("start_led_status executes successfully.")


@logThis
def check_uplink_100g_port_led_status():
    output=device.executeCommand("linespeed run exts 27 1024 95 60",BCM_promptstr,timeout=90)
    CommonKeywords.should_match_a_regexp(output,uplink_100g_led_pattern1)
    CommonKeywords.should_match_a_regexp(output,linespeed_test_pattern)
    log.info("Semi automation and this item just focus on traffic test.For LED test,it need to check by manual test")
    log.success("check_uplink_100g_port_led_status executes successfully.")



@logThis
def check_uplink_40g_port_led_status():
    output=device.executeCommand("linespeed run exts 27 1518 20 60",BCM_promptstr,timeout=90)
    CommonKeywords.should_match_a_regexp(output,uplink_40g_led_pattern1)
    CommonKeywords.should_match_a_regexp(output,linespeed_test_pattern)

    log.info("Semi automation and this item just focus on traffic test.For LED test,it need to check by manual test")
    log.success("check_uplink_40g_port_led_status executes successfully.")


@logThis
def check_stacking_100g_port_led_status():
    output=device.executeCommand("linespeed run exts 25-26 1024 100 60",BCM_promptstr,timeout=90)
    CommonKeywords.should_match_a_regexp(output,stacking_100g_led_pattern1)
    CommonKeywords.should_match_a_regexp(output,stacking_100g_led_pattern2)
    CommonKeywords.should_match_a_regexp(output,linespeed_test_pattern)

    log.success("check_stacking_100g_port_led_status executes successfully.")

@logThis
def check_stacking_40g_port_led_status():
    output=device.executeCommand("linespeed run exts 25-26 1024 100 60",BCM_promptstr,timeout=90)
    CommonKeywords.should_match_a_regexp(output,stacking_40g_led_pattern1)
    CommonKeywords.should_match_a_regexp(output,stacking_40g_led_pattern2)
    CommonKeywords.should_match_a_regexp(output,linespeed_test_pattern)

    log.info("Semi automation and this item just focus on traffic test.For LED test,it need to check by manual test")
    log.success("check_stacking_40g_port_led_status executes successfully.")


@logThis
def check_10g_port_link_and_status():
    output1=device.executeCommand("ps", BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output1, ps_10g_link_pattern)

    output2=device.executeCommand("epdm link all", BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output2, epdm_10g_link_pattern)
    log.success("check_10g_port_link_ans_status executes successfully.")

@logThis
def check_downlink_10g_port_status():
    output1=device.executeCommand("linespeed run exts 1-24 1024 100 60", BCM_promptstr,timeout=90)
    for port in range(1,25):
        pattern1= "Start port"+str(port)+" linespeed test with speed 10G"
        pattern2= "Port"+str(port)+" 10G Linespeed test.*?PASS"
        CommonKeywords.should_match_a_regexp(output1,pattern1)
        CommonKeywords.should_match_a_regexp(output1,pattern2)
    CommonKeywords.should_match_a_regexp(output1,linespeed_test_pattern)
    log.info("Semi automation and this item just focus on traffic test.For LED test,it need to check by manual test")
    log.success("check_downlink_10g_port_status executes successfully.")

@logThis
def change_port_speed_to_1g():
    device.executeCommand("port xe0-xe23 sp=1000",BCM_promptstr)
    output=device.executeCommand("epdm speed miura 1000",BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output, speed_10g_to_1g_pattern)
    log.success("change_port_speed_to_1g executes successfully.")

@logThis
def check_1g_port_link_and_status():
    output1=device.executeCommand("ps", BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output1, ps_1g_link_pattern)

    output2=device.executeCommand("epdm link all", BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output2, epdm_1g_link_pattern)
    log.success("check_1g_port_link_ans_status executes successfully.")


@logThis
def check_downlink_1g_port_status():
    output1=device.executeCommand("linespeed run exts 1-24 1024 100 60", BCM_promptstr,timeout=90)
    for port in range(1,25):
        pattern1= "Start port"+str(port)+" linespeed test with speed 1G"
        pattern2= "Port"+str(port)+" 1000M Linespeed test.*?PASS"
        CommonKeywords.should_match_a_regexp(output1,pattern1)
        CommonKeywords.should_match_a_regexp(output1,pattern2)
    CommonKeywords.should_match_a_regexp(output1,linespeed_test_pattern)
    log.info("Semi automation and this item just focus on traffic test.For LED test,it need to check by manual test")
    log.success("check_downlink_1g_port_status executes successfully.")


@logThis
def check_downlink_10G_port_MAC_side_FEC_and_check_port_status():
    device.executeCommand("c",'cint')
    device.executeCommand("unsigned int enable;",'cint')
    device.executeCommand("bcm_port_phy_control_get(0,1,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,&enable);",'cint')
    output1=device.executeCommand('printf("FEC enable=%d \n",enable);','cint')
    CommonKeywords.should_match_a_regexp(output1,"FEC enable=0")

    device.executeCommand("exit;",BCM_promptstr)
    output2=device.executeCommand("ps xe0",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output2,"up|UP|Up")

    output3=device.executeCommand("phy diag xe0 pcs",BCM_promptstr)
    result=CommonLib.parseDict(output=output3, pattern_dict=phy_diag_xe0_pattern, sep_field=":")
    CommonKeywords.should_match_a_regexp(result["PCS SYNC"], "Y")
    CommonKeywords.should_match_a_regexp(result["PCS LINK"], "Y")

    log.success("enable_downlink_10G_port_MAC_side_FEC_and_check_port_status executes successfully.")

@logThis
def  enable_downlink_10G_port_MAC_side_FEC_and_check_port_status():
    device.executeCommand("c",'cint')
    device.executeCommand("bcm_port_phy_control_set(0,1,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,1);",'cint')
    device.executeCommand("bcm_port_phy_control_get(0,1,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,&enable);",'cint')
    output1=device.executeCommand('printf("FEC enable=%d \n",enable);','cint')
    CommonKeywords.should_match_a_regexp(output1,"FEC enable=1")

    device.executeCommand("exit;",BCM_promptstr)
    output2=device.executeCommand("ps xe0",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output2,"down")

    output3=device.executeCommand("phy diag xe0 pcs",BCM_promptstr)
    result=CommonLib.parseDict(output=output3, pattern_dict=phy_diag_xe0_pattern, sep_field=":")
    CommonKeywords.should_match_a_regexp(result["PCS SYNC"], "N")
    CommonKeywords.should_match_a_regexp(result["PCS LINK"], "N")

    log.success("enable_downlink_10G_port_MAC_side_FEC_and_check_port_status_second executes successfully.")


@logThis
def disable_downlink_10G_port_MAC_side_FEC_and_check_port_status():
    device.executeCommand("c",'cint')
    device.executeCommand("bcm_port_phy_control_set(0,1,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,0);",'cint')
    device.executeCommand("bcm_port_phy_control_get(0,1,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,&enable);",'cint')
    output1=device.executeCommand('printf("FEC enable=%d \n",enable);','cint')
    CommonKeywords.should_match_a_regexp(output1,"FEC enable=0")

    device.executeCommand("exit;",BCM_promptstr)
    output2=device.executeCommand("ps xe0",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output2,"up")

    output3=device.executeCommand("phy diag xe0 pcs",BCM_promptstr)
    result=CommonLib.parseDict(output=output3, pattern_dict=phy_diag_xe0_pattern, sep_field=":")
    CommonKeywords.should_match_a_regexp(result["PCS SYNC"], "Y")
    CommonKeywords.should_match_a_regexp(result["PCS LINK"], "Y")

    log.success("disable_downlink_10G_port_MAC_side_FEC_and_check_port_status executes successfully.")




def check_uplink_100G_port_MAC_side_FEC_status_and_check_port_status():
    device.executeCommand("c",'cint')
    device.executeCommand("unsigned int enable;",'cint')
    device.executeCommand("bcm_port_phy_control_get(0,27,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,&enable);",'cint')
    
    output1=device.executeCommand('printf("FEC enable=%d \n",enable);','cint')
    CommonKeywords.should_match_a_regexp(output1, fec_disable_pattern)    

    device.executeCommand("exit;",BCM_promptstr)
    output2=device.executeCommand("ps ce2",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output2, "up")

    log.success("check_uplink_100G_port_MAC_side_FEC_status_and_check_port_status executes successfully.")

def enable_uplink_100G_port_MAC_side_FEC_and_check_port_status():
    device.executeCommand("c",'cint')
    device.executeCommand("bcm_port_phy_control_set(0,27,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,1);",'cint')
    device.executeCommand("bcm_port_phy_control_get(0,27,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,&enable);",'cint')
    
    output1=device.executeCommand('printf("FEC enable=%d \n",enable);','cint')
    CommonKeywords.should_match_a_regexp(output1, fec_enable_pattern)

    device.executeCommand("exit;",BCM_promptstr)
    output2=device.executeCommand("ps ce2",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output2, "down")

    output3=device.executeCommand("phy diag ce2 pcs",BCM_promptstr)
    result_dict = CommonLib.parseDict(output=output3, pattern_dict=phy_diag_ce_dict, sep_field=" ")
    CommonKeywords.should_match_a_regexp(result_dict["FEC ENA:"], "0x1")


    log.success("enable_uplink_100G_port_MAC_side_FEC_and_check_port_status executes successfully.")

def disable_uplink_100G_port_MAC_side_FEC_and_check_port_status():
    device.executeCommand("c",'cint')
    device.executeCommand("bcm_port_phy_control_set(0,27,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,0);",'cint')
    device.executeCommand("bcm_port_phy_control_get(0,27,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,&enable);",'cint')
    
    output1=device.executeCommand('printf("FEC enable=%d \n",enable);','cint')
    CommonKeywords.should_match_a_regexp(output1, fec_disable_pattern)

    device.executeCommand("exit;",BCM_promptstr)
    output2=device.executeCommand("ps ce2",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output2, "up")

    output3=device.executeCommand("phy diag ce2 pcs",BCM_promptstr)
    result_dict = CommonLib.parseDict(output=output3, pattern_dict=phy_diag_ce_dict, sep_field=" ")
    CommonKeywords.should_match_a_regexp(result_dict["FEC ENA:"], "0x0")


    log.success("disable_uplink_100G_port_MAC_side_FEC_and_check_port_status executes successfully.")




def check_stacking_100G_port_MAC_side_FEC_status_and_check_port_status():
    device.executeCommand("c",'cint')
    device.executeCommand("unsigned int enable;",'cint')
    device.executeCommand("bcm_port_phy_control_get(0,25,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,&enable);",'cint')

    output1=device.executeCommand('printf("FEC enable=%d \n",enable);','cint')
    CommonKeywords.should_match_a_regexp(output1, fec_disable_pattern)

    device.executeCommand("exit;",BCM_promptstr)
    output2=device.executeCommand("ps ce0",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output2, "up")

    log.success("check_stacking_100G_port_MAC_side_FEC_status_and_check_port_status executes successfully.")

def enable_stacking_100G_port_MAC_side_FEC_and_check_port_status():
    device.executeCommand("c",'cint')
    device.executeCommand("bcm_port_phy_control_set(0,25,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,1);",'cint')
    device.executeCommand("bcm_port_phy_control_get(0,25,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,&enable);",'cint')

    output1=device.executeCommand('printf("FEC enable=%d \n",enable);','cint')
    CommonKeywords.should_match_a_regexp(output1, fec_enable_pattern)

    device.executeCommand("exit;",BCM_promptstr)
    output2=device.executeCommand("ps ce0",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output2, "down")

    output3=device.executeCommand("phy diag ce0 pcs",BCM_promptstr)
    result_dict = CommonLib.parseDict(output=output3, pattern_dict=phy_diag_ce_dict, sep_field=" ")
    CommonKeywords.should_match_a_regexp(result_dict["FEC ENA:"], "0x1")


    log.success("enable_stacking_100G_port_MAC_side_FEC_and_check_port_status executes successfully.")

def disable_stacking_100G_port_MAC_side_FEC_and_check_port_status():
    device.executeCommand("c",'cint')
    device.executeCommand("bcm_port_phy_control_set(0,25,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,0);",'cint')
    device.executeCommand("bcm_port_phy_control_get(0,25,BCM_PORT_PHY_CONTROL_FORWARD_ERROR_CORRECTION,&enable);",'cint')

    output1=device.executeCommand('printf("FEC enable=%d \n",enable);','cint')
    CommonKeywords.should_match_a_regexp(output1, fec_disable_pattern)

    device.executeCommand("exit;",BCM_promptstr)
    output2=device.executeCommand("ps ce0",BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output2, "up")

    output3=device.executeCommand("phy diag ce0 pcs",BCM_promptstr)
    result_dict = CommonLib.parseDict(output=output3, pattern_dict=phy_diag_ce_dict, sep_field=" ")
    CommonKeywords.should_match_a_regexp(result_dict["FEC ENA:"], "0x0")


    log.success("disable_stacking_100G_port_MAC_side_FEC_and_check_port_status executes successfully.")



@logThis
def check_ps_and_epdm_port_link_status_and_speed():
    check_port_link_and_status()
    output1=device.executeCommand("epdm link all", BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output1, epdm_pattern)
    log.success("check_ps_and_epdm_port_link_status_and_speed executes successfully.")

@logThis
def change_all_port_speed_to_minimum():
    output=device.executeCommand("portminspeed.soc", BCM_promptstr)
    log.info("portminspeed.soc command is under progress and can not be tested now")
    for value in fail_pattern:
        if value in output:
            log.fail("Something wrong in command portminspeed.soc")
    CommonKeywords.should_match_ordered_regexp_list(output, portmin_pattern)
    log.success("change_all_port_speed_to_minimum executes successfully.")

@logThis
def change_all_port_speed_to_maximum():
    device.executeCommand("portmaxspeed.soc", BCM_promptstr)
    log.info("portmaxspeed.soc command is under progress and can not be tested now")
    for value in fail_pattern:
        if value in output:
            log.fail("Something wrong in command portmaxspeed.soc")
    CommonKeywords.should_match_ordered_regexp_list(output, portmax_pattern)
    log.success("change_all_port_speed_to_maximum executes successfully.")

@logThis
def verify_eeprom():
    output=device.executeCommand("./PHY8239x_FW_2_Flash_Verify.sh",'root@localhost',timeout=90)
    log.info("This command is not functioal for this device, it is under development process.")
    for value in fail_pattern:
        if value in output:
            raise Exception("Find errors when execute ./PHY8239x_FW_2_Flash_Verify.sh.")

    log.success("verify_eeprom executes successfully.")
  
@logThis
def verify_detached_load_sdk():
    cmd="./auto_load_user.sh -a -d"
    output=device.executeCommand(cmd,'root@localhost',timeout=90)
    for pattern in fail_pattern:
        if pattern in output:
            raise Exception("Find errors when execute {}.".format(cmd))
    log.info('%s is passed\n'%cmd )

@logThis
def check_port_status_by_remote_shell_command():
    output = device.sendCmd('./cls_shell ps','SDK', timeout ='5')
    output = device.read_until_regexp("ce2.*?IEEE", timeout='120')
    CommonKeywords.should_match_ordered_regexp_list(output, ps_100G_pattern)
      
    log.success("check_port_status_by_remote_shell_command executes successfully.")


@logThis
def remote_shell_command_to_exit_sdk_and_check_bcm_process():
    output = device.sendCmd('./cls_shell exit','SDK',timeout='5')
    for pattern in fail_pattern:
        if pattern in output:
            raise Exception("Find errors when execute {}.".format(cmd))

    device.executeCommand('ps -a | grep "bcm.u"','SDK')
    
    log.success("remote_shell_command_to_exit_sdk_and_check_bcm_process executes successfully.")





@logThis
def check_downlink_port_link_serde_version():
    cmd="phy diag xe dsc"
    output=device.executeCommand(cmd,BCM_promptstr,timeout=90)
    splited_output=output.split("\n")
    flag=False
    for line in splited_output:

        if flag:
            if downlink_serde_port not in line:
                log.fail(cmd+" has different UCODE_VER")
            flag=False

        if "UCODE_VER" in line:
            if "Microcode Version [majorversion_minorversion]" not in line:
                flag=True



    log.success("check_downlink_link_serde_version exeutes successfully.")


@logThis
def check_uplink_port_link_serde_version():
    cmd="phy diag ce dsc"
    flag=False
    output=device.executeCommand(cmd,BCM_promptstr)
    splited_output=output.split("\n")
    for line in splited_output:

        if flag:
            if uplink_serde_port not in line:
                log.fail(cmd+" has different UCODE_VER")
            flag=False

        if "UCODE_VER" in line:
            if "Microcode Version [majorversion_minorversion]" not in line:
                flag=True


    log.success("check_uplink_link_serde_version exeutes successfully.")


@logThis
def  check_each_port_serde_version_phy_side():
    for port in range(0,27):
        cmd="epdm dumpphyinfo "+str(port)+" 0"
        output=device.executeCommand(cmd,BCM_promptstr,timeout=300)
        if output is None :
            raise Exception(cmd+"does not executed properly.")
        for value in fail_pattern:
            if value in output:
                raise Exception(cmd+" does not executed properly.")
        log.success(cmd+" executed successfully")

    for port in range(0,27):
        cmd="epdm dumpphyinfo "+str(port)+" 1"
        output=device.executeCommand(cmd,BCM_promptstr,timeout=300)
        if output is None :
            raise Exception(cmd+" does not executed properly.")
        for value in fail_pattern:
            if value in output:
                raise Exception(cmd+" does not executed properly.")
        log.success(cmd+" executed successfully")



@logThis
def enable_macsec_function():
    for port in range(0,27):
        cmd="epdm macsec enable "+str(port)
        output=device.executeCommand(cmd,BCM_promptstr)
        CommonKeywords.should_match_ordered_regexp_list(output, enable_macsec_pattern)
        log.success(cmd+" executes successfully.")
    log.success("enable_macsec_function executes successfully.")

@logThis
def check_macsec_enable_counters():
    for port in range(0,27):
        cmd="epdm macsec show stats "+str(port)
        output=device.executeCommand(cmd,BCM_promptstr)
        if output is None:
            raise Exception(cmd+" has nothing to show. Maybe it is disable")
        for value in fail_pattern:
            if value in output:
                raise Exception(cmd+" has some fail logs.")
        for key,value in enable_macsec_counters_pattern_dict.items():
            count=output.count(key)
            if count != value:
                raise Exception(cmd+" output has some missing params.")
        log.success(cmd+" executes successfully.")
    log.success("check_macsec_enable_counters executes successfuly.")

@logThis
def send_snake_traffic_and_check_macsec_counters():

    output=device.executeCommand("linespeed run exts 1-27 1518 10 60",BCM_promptstr,timeout=90)
    CommonKeywords.should_match_ordered_regexp_list(output,linespeed_24h_traffic_pattern_start)
    CommonKeywords.should_match_ordered_regexp_list(output,linespeed_24h_traffic_pattern_end)

    show_c_tpkt_rpkt_xe0_xe23()
    show_c_tpkt_rpkt_ce0_ce1()
    show_c_tpkt_rpkt_ce2()

    check_macsec_enable_counters()
    log.success("send_snake_traffic_and_check_macsec_counters executes successfuly.")


@logThis
def check_macsec_disable_counters():
    for port in range(0,27):
        cmd="epdm macsec show stats "+str(port)
        output=device.executeCommand(cmd,BCM_promptstr)
        for value in fail_pattern:
            if value in output:
                raise Exception(cmd+" has some fail logs.")
        for key,value in enable_macsec_counters_pattern_dict.items():
            count=output.count(key)
            if count != 0:
                raise Exception(cmd+" output is not disabled properly.")
        log.success(cmd+" executes successfully.")

    log.success("check_macsec_disable_counters executes successfuly.")



@logThis
def disable_macsec_and_check_macsec_counters():
    for port in range(0,27):
        cmd="epdm macsec bypass "+str(port)
        output=device.executeCommand(cmd,BCM_promptstr)
        CommonKeywords.should_match_ordered_regexp_list(output, disable_macsec_pattern)
        log.success(cmd+" executes successfully.")
    

    check_macsec_disable_counters()
    log.success("disable_macsec_and_check_macsec_counters executes successfully.")

@logThis
def run_command_to_test_24h_traffic():
    output=device.executeCommand("linespeed run exts all 1518 20 60",BCM_promptstr,timeout=90)
    CommonKeywords.should_match_ordered_regexp_list(output,linespeed_24h_traffic_pattern_start)
    CommonKeywords.should_match_ordered_regexp_list(output,linespeed_24h_traffic_pattern_end)
    log.success("run_command_to_test_24h_traffic executes successfully.")

@logThis
def show_c_tpkt_rpkt_xe0_xe23():
    output1=device.executeCommand("show c XLMIB_TPKT.xe0-xe23;show c XLMIB_RPKT.xe0-xe23;show c XLMIB_RFCS" ,BCM_promptstr,timeout=300)
    o1=output1.split("\n")
    o1=o1[2:]
    for lineNumber in range(24):
        line=o1[lineNumber]

        tpkt_pattern="XLMIB_TPKT.xe"+str(lineNumber)
        if tpkt_pattern not in line:
            log.fail(tpkt_pattern+" is not present in "+line)
        #CommonKeywords.should_match_a_regexp(line,tpkt_pattern)

        tpkt_result=line.split(":")
        tpkt_values=tpkt_result[1].strip()
        tpkt_number_list= list(map(str,tpkt_values.split("+")))

        tpkt_number_list[0]=tpkt_number_list[0].strip()
        tpkt_number_list[1]=tpkt_number_list[1].strip()
        # print(number_list[0] == number_list[1])

        if (tpkt_number_list[0] != tpkt_number_list[1]):
            log.fail(line+" : ->values does not match")


        line=o1[lineNumber+24]

        rpkt_pattern="XLMIB_RPKT.xe"+str(lineNumber)
        if rpkt_pattern not in line:
            log.fail(rpkt_pattern+" is not present in "+line)

        #CommonKeywords.should_match_a_regexp(line,rpkt_pattern)

        rpkt_result=line.split(":")
        rpkt_values=rpkt_result[1].strip()
        rpkt_number_list= list(map(str,rpkt_values.split("+")))

        rpkt_number_list[0]=rpkt_number_list[0].strip()
        rpkt_number_list[1]=rpkt_number_list[1].strip()
        #print(number_list[0] == number_list[1])
        if (rpkt_number_list[0] != rpkt_number_list[1]):
            log.fail(line+" :->values does not match")

        if(not(rpkt_number_list[0] == rpkt_number_list[1] == tpkt_number_list[0] == tpkt_number_list[1])):
            log.fail("TPKT and RPKT values of xe"+str(lineNumber)+" is not same")
    log.success("show_c_tpkt_rpkt_xe0_xe23 executes successfully.")

@logThis
def show_c_tpkt_rpkt_ce0_ce1():
    output2=device.executeCommand("show c CLMIB_TPKT.ce0-ce1;show c CLMIB_RPKT.ce0-ce1;show c CLMIB_RFCS",BCM_promptstr)

    o2=output2.split("\n")
    o2=o2[2:]
    for lineNumber in range(2):
        line=o2[lineNumber]

        tpkt_pattern="CLMIB_TPKT.ce"+str(lineNumber)
        if tpkt_pattern not in line:
            log.fail(tpkt_pattern+" is not present in "+line)

        #CommonKeywords.should_match_a_regexp(line,tpkt_pattern)

        tpkt_result=line.split(":")
        tpkt_values=tpkt_result[1].strip()

        tpkt_number_list= list(map(str,tpkt_values.split("+")))

        tpkt_number_list[0]=tpkt_number_list[0].strip()
        tpkt_number_list[1]=tpkt_number_list[1].strip()

        if (tpkt_number_list[0] != tpkt_number_list[1]):
            log.fail(line+" : ->values does not match")


        # FOR TPKT and RPKT values check

        line=o2[lineNumber+2]
        #print(line)

        rpkt_pattern="CLMIB_RPKT.ce"+str(lineNumber)
        if rpkt_pattern not in line:
            log.fail(rpkt_pattern+" is not present in "+line)


        rpkt_result=line.split(":")
        rpkt_values=rpkt_result[1].strip()

        rpkt_number_list= list(map(str,rpkt_values.split("+")))

        rpkt_number_list[0]=rpkt_number_list[0].strip()
        rpkt_number_list[1]=rpkt_number_list[1].strip()
        # print(number_list[0] == number_list[1])

        if (rpkt_number_list[0] != rpkt_number_list[1]):
            log.fail(line+" :->values does not match")
        if(not(rpkt_number_list[0] == rpkt_number_list[1] == tpkt_number_list[0] == tpkt_number_list[1])):
            log.fail("TPKT and RPKT values of ce"+str(lineNumber)+" is not same")
    log.success("show_c_tpkt_rpkt_ce0_ce1 executes successfully.")

@logThis
def show_c_tpkt_rpkt_ce2():
    output3=device.executeCommand("show c CLMIB_TPKT.ce2;show c CLMIB_RPKT.ce2;show c CLMIB_RFCS",BCM_promptstr)
    splited_output3=output3.split("\n")
    splited_output3=splited_output3[2:]
    for lineNumber in range(1):
        line=splited_output3[lineNumber]

        tpkt_pattern="CLMIB_TPKT.ce2"
        if tpkt_pattern not in line:
            log.fail(tpkt_pattern+" is not present in "+line)

        #CommonKeywords.should_match_a_regexp(line,tpkt_pattern)

        tpkt_result=line.split(":")
        tpkt_values=tpkt_result[1].strip()

        tpkt_number_list= list(map(str,tpkt_values.split("+")))

        tpkt_number_list[0]=tpkt_number_list[0].strip()
        tpkt_number_list[1]=tpkt_number_list[1].strip()

        if (tpkt_number_list[0] != tpkt_number_list[1]):
            log.fail(line+" : ->values does not match")


        # FOR TPKT and RPKT values check

        line=splited_output3[lineNumber+1]
        #print(line)

        rpkt_pattern="CLMIB_RPKT.ce2"
        if rpkt_pattern not in line:
            log.fail(rpkt_pattern+" is not present in "+line)


        rpkt_result=line.split(":")
        rpkt_values=rpkt_result[1].strip()

        rpkt_number_list= list(map(str,rpkt_values.split("+")))

        rpkt_number_list[0]=rpkt_number_list[0].strip()
        rpkt_number_list[1]=rpkt_number_list[1].strip()
        # print(number_list[0] == number_list[1])

        if (rpkt_number_list[0] != rpkt_number_list[1]):
            log.fail(line+" :->values does not match")
        if(not(rpkt_number_list[0] == rpkt_number_list[1] == tpkt_number_list[0] == tpkt_number_list[1])):
            log.fail("TPKT and RPKT values of ce2 are not same.")
    log.success("show_c_tpkt_rpkt_ce2 executes successfully.")




@logThis
def check_port_counter_and_system_status():

    show_c_tpkt_rpkt_xe0_xe23()
    show_c_tpkt_rpkt_ce0_ce1()
    show_c_tpkt_rpkt_ce2()
    log.success("check_port_counter_and_system_status executes successfully.")
        



@logThis
def scp(filename):
    password = 'intel@1234'
    device.sendCmd("cd")
    device.sendCmd(f'scp root@192.168.0.152:/home/aberlour_image/{filename} .')
    promptList = ["(y/n)", "(yes/no)", "password:"]
    patternList = re.compile('|'.join(promptList))
    output1 = device.read_until_regexp(patternList, timeout= '180')
    log.info('output1: ' + str(output1))

    if re.search("(yes/no)",output1):
        device.transmit("yes")
        device.receive("password:")
        device.transmit("%s"%password)
    elif re.search("(y/n)",output1):
        device.transmit("y")
        device.receive("password:")
        device.transmit("%s"%password)
    elif re.search("password:",output1):
        device.transmit("%s"%password)
    else:
        log.fail("pattern mismatch")

    device.executeCommand(f'mv {filename} /root/Diag/aberlour/SDK',"root@localhost ~")
    device.executeCommand("cd /root/Diag/aberlour/SDK",prompt='root@localhost SDK')
    output = device.executeCommand('ls -la', prompt='root@localhost SDK')
    if filename in output:
        log.success(f"file {filename} successfully fetched!")
    else:
        raise RuntimeError(f"Please add the file {filename} in 192.168.0.152/root server or add the file to the unit and run the test!")


@logThis
def all_port_enable_disable_stress_test():
    output = device.executeCommand('ls -la', prompt='root@localhost SDK')
    if filename1 in output:
        log.success(f"file {filename1} present")
    else:
        scp(filename1)

    device.sendCmd('chmod 777 '+ filename1)
    if "allport_stress.txt" in output:
        device.sendCmd('rm allport_stress.txt')
    
    console_output = device.executeCommand('./'+filename1, prompt='root@localhost SDK', timeout = '700')
    output_txt_file= device.executeCommand('cat allport_stress.txt',prompt = 'root@localhost SDK')
    

    if "Failed" in output:
        raise Exception("This stress test case is failed.")

    if "Failed" in output_txt_file:
        raise Exception("This stress test case is failed.")

    if "No such file or directory" in console_output:
        raise Exception("Please add necessary .soc file and try again.")

    for value in fail_pattern:
        if (value in console_output) or (value in output_txt_file):
            raise Exception("This stress test case is failed.")

    CommonKeywords.should_match_a_regexp(console_output, enale_disable_1000_times_done_pattern)
    CommonKeywords.should_match_a_regexp(output_txt_file, enale_disable_1000_times_done_pattern)
    
    device.sendCmd('rm allport_stress.txt')
  

@logThis
def sdk_re_init_stress_test():
    output = device.executeCommand('ls -la', prompt='root@localhost SDK')
    if filename2 in output:
        log.success(f"file {filename2} present")
    else:
        scp(filename2)

    device.sendCmd('chmod 777 '+ filename2)
    if "allport_stress.txt" in output:
        device.sendCmd('rm allport_stress.txt')

    console_output = device.executeCommand('./'+filename2, prompt='root@localhost SDK', timeout = '700')
    output_txt_file= device.executeCommand('cat allport_stress.txt',prompt = 'root@localhost SDK')


    if "Failed" in output:
        raise Exception("This stress test case is failed.")

    if "Failed" in output_txt_file:
        raise Exception("This stress test case is failed.")

    if "No such file or directory" in console_output:
        raise Exception("Please add necessary .soc file and try again.")

    for value in fail_pattern:
        if (value in console_output) or (value in output_txt_file):
            raise Exception("This stress test case is failed.")

    CommonKeywords.should_match_a_regexp(console_output, sdk_reinit_stress_1000_times_done_pattern)

    device.sendCmd('rm allport_stress.txt')
    log.info("This stress test runs for 3 time for verification, it needs to be executed 1000 time in real environment.")
    log.success("sdk_re_init_stress_test executes successfully.")



