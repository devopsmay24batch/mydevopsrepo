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
import CRobot
import sys
import os
import json
from Decorator import *
import re
import Logger as log
import CommonLib
import whitebox_lib
import WhiteboxLibAdapter
import time
import pexpect
from functools import partial
import Const
from ses_variable import *
from cronus_ses_variable import *
import difflib
import filecmp
import parser_openbmc_lib
import YamlParse
from SwImage import SwImage
from Server import Server
import random
import ses_lib

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/whitebox'))

#run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
#run_command_cli = partial(CommonLib.run_command, deviceObj=device, prompt='ESM\s\w.*')



@logThis
def CronuslistTemperatureSensor(hdd):
    log.info("Inside listTemperatureSensor procedure")
    cmd = "sg_ses --page=0x02 {}".format(hdd)
    p_sensor = "Element\s+(\d+)\s+descriptor.*?\n.*?\n.*?\n.*?\n.*?Temperature=\d+\s+C"
    output_temp = ses_lib.run_command(cmd)
    print("out temp is {}".format(output_temp))
    error_msg1 = "Didn't find available any temperature sensor."
    sensors = ses_lib.find_matches(p_sensor, output_temp, error_msg1)
    log.info("Found sensors: {}".format(sensors))

    return sensors


@logThis
def CronusgetSensorTemperature(sensorID, hdd):
    cmd = "sg_ses --page=0x02 --index=ts,{} {}".format(sensorID, hdd)
    p_temper = "Temperature=(\d+)\s+C"
    output = ses_lib.run_command(cmd)
    error_msg = "Didn't get temperature value."
    temper = ses_lib.find_matches(p_temper, output, error_msg)

    return temper[0]


@logThis
def CronuscheckSensorValueOnPage5(sensor, hdd, alarm_level, checking_value,
        sensor_type="Temperature sensor"):
    index_abbr = index_abbr_dict[sensor_type]
    cmd = "sg_ses --page=0x05 --index={},{} --get={} {}".format(
            index_abbr, sensor,
            threshold_type_dict[alarm_level], hdd)
    pattern = f"{checking_value}\s*$"
    output = ses_lib.run_command(cmd)
    match = re.search(pattern, output, re.M)
    if not match:
        raise Exception(f"Failed: {checking_value}")
    print('The match found here is ',match)

@logThis
def CronusverifyDescriptorLength(hdd, fru_log):
    log.info("Inside verifyDescriptorLength procedure")
    log.debug(f"hdd      :{hdd}")
    log.debug(f"fru_log  :{fru_log}")
    get_elements_info_cmd = "sg_ses --page=0x07 {}".format(hdd)
    output = ses_lib.run_command(get_elements_info_cmd)
    contents = output.split("Element type:")
    mismatches = []
    elements_dict = {}
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    ProductNameInfo = ses_lib.get_deviceinfo_from_config("UUT","name")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        descriptor_length_dict = {
        "Array device slot" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Power supply" : [0x48, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Cooling": [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Temperature sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Enclosure services controller electronics" : [0x50, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Enclosure" : [0x50, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Voltage sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "SAS expander" : [0x20, "Element \d+ descriptor:\s+(.*)\r\n"],
        "SAS connector" : [0x52, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Current sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Display" : [0x40, "Element \d+ descriptor:\s+(.*)\r\n"]
        }
    elif ProductTypeInfo == "SD4100":
        descriptor_length_dict = {"Array device slot" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Power supply" : [0x48, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Cooling": [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Temperature sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Enclosure services controller electronics" : [0x50, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Enclosure" : [0x50, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Voltage sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "SAS expander" : [0x20, "Element \d+ descriptor:\s+(.*)\r\n"],
        "SAS connector" : [0x52, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Current sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Display" : [0x40, "Element \d+ descriptor:\s+(.*)\r\n"]}
    elif ProductTypeInfo == "Nebula_Gen2F":
        descriptor_length_dict = {"Array device slot overall" : [0x11, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Array device slot" : [0x7, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Power supply overall" : [0x0c, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Power supply" : [0x04, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Cooling overall": [0x07, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Temperature sensor overall" : [0x12, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Enclosure services controller electronics overall" : [0x0c, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Enclosure" : [0xc, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Voltage sensor overall" : [0x0e, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Display" : [0xa, "Element \d+ descriptor:\s+(.*)\r\n"]}
    elif ProductTypeInfo == "CELESTIC  P2523":
        descriptor_length_dict = {"Array device slot overall" : [0x11, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Array device slot" : [0x14, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Power supply overall" : [0x0c, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Power supply" : [0x050, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Cooling overall": [0x07, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Temperature sensor overall" : [0x12, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Enclosure services controller electronics overall" : [0x0c, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Enclosure" : [0x4c, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Voltage sensor overall" : [0x0e, "Element \d+ descriptor:\s+(.*)\r\n"],
                "Display" : [0xa, "Element \d+ descriptor:\s+(.*)\r\n"]}
    if ProductNameInfo == "Titan_G2_Lenovo" or ProductTypeInfo == "TITAN-4U90":
            log.debug(f"Product Name :{ProductNameInfo}")      
            descriptor_length_dict = {
                    "Power supply" : [0x54, "Element \d+ descriptor:\s+(.*)\r\n"]
            }
    for content in contents:
        for descriptor, checks in descriptor_length_dict.items():
            if descriptor+"," in content:
                elements = re.findall(checks[1], content, re.M)
                if not elements:
                    raise Exception("Didn't find any element of {}".format(descriptor))
                for element in elements:
                    if int(checks[0])!=len(element):
                        error_msg = "{} length is mismatched, expect {},".format(descriptor,
                                hex(checks[0]))
                        error_msg += " current {}:\n***{}***".format(hex(len(element)), element)
                        mismatches.append(error_msg)
                        break
                elements_dict.update({descriptor:elements})
    if mismatches:
        for error_msg in mismatches:
            log.info(error_msg)
        exception_msg = "Element lenghth is mismatched, "
        exception_msg += "total number of mismatched length types: {}".format(len(mismatches))
        raise Exception(exception_msg)
    log.info("element dict is {}".format(elements_dict))
    for descriptor, elements in elements_dict.items():
        log.info("descriptor is {}".format(descriptor))
        log.info("elements is {}".format(elements))
        if descriptor not in ("Power supply",):
            continue
        for element in elements:
            log.info("element is {}".format(element))
            infos = element.strip(" ").split("  ")
            infos = [x.strip() for x in infos]
            infos = list(filter(lambda x:x, infos))
            log.info("Info list is {}".format(infos))
            if not [ x for x in infos[1:] if x != "SD4100"]:
                continue
            if len(infos) < 5 and descriptor in ("Power supply",):
                continue
            if len(infos) < 3 and descriptor in ("Display",):
                continue
            if re.search("Reg",infos[0]):
                continue
            infos = [CommonLib.escapeString(x) for x in infos]
            log.info("Info is {}".format(str(infos)))
            log.info("fru log is {}".format(fru_log))
            if descriptor in ("Power supply",):
                if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90" or ProductTypeInfo == "SD4100":
                    pass_pattern = ".*{}.*?\n.*?\n.*?\n.*?{}.*?\n.*?\n.*?{}.*?\n.*?{}".format(
                     infos[1], infos[2], infos[4],infos[3])
                    if ProductNameInfo == "Titan_G2_Lenovo":
                        log.debug(f"Product Name :{ProductNameInfo}")
                        pass_pattern = ".*{}.*?\n.*?{}.*?\n.*?{}.*\n.*?{}".format(infos[2], infos[1], infos[4],infos[3])
                        log.info(pass_pattern)
                    elif ProductTypeInfo == "CELESTIC  P2523":
                        pass_pattern=".*{}.*?\n.*?{}.*?\n.*?{}.*\n.*?{}".format(infos[2], infos[1], infos[3],infos[4])
                        log.info(pass_pattern)
                else:
                    pass_pattern = "{}.*?\n.*?{}.*?\n.*?\n.*?\n.*?{}.*?\n.*?\n.*?{}.*?\n.*?{}".format(infos[0],
                    infos[1], infos[2], infos[4],infos[3])
            elif descriptor in ("Display",):
                pass_pattern = infos[2]
            elif descriptor in ("Product Info",):
                if ProductTypeInfo == "SD4100":
                    pass_pattern = ".*{}.*?\n.*?\n.*?\n.*?{}.*?\n.*?\n.*?{}.*?\n.*?{}".format(
                     infos[1], infos[2], infos[4],infos[3])
                    log.info(pass_pattern)
            if not re.search(pass_pattern, fru_log, re.M):
                err_msg = "Didn't find {} in 'fru get' output.".format(element)
                raise Exception(err_msg)

@logThis
def CronussetAndVerifyUW():
    log.info("Inside  UW")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90" or ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = ses_lib.run_command_cli(cmd)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern="^(\S+)          .*?(\S+)'C\s+Normal\s+\[(\S+)\].*"
        match=re.search(pattern,line)
        if match:
            log.info(line)
            count+=1
            break
    if count==0:
        log.info("No Temp ID with numerical display available")
        raise RuntimeError("No Temp ID with numerical display available")
    temp_id=match.group(1)
    reading_value=match.group(2)
    threshold_value = match.group(3)
    list_threshold=list(threshold_value.split(","))
    modify_value=random.randint(0,int(reading_value)-1)
    clr_cmd="log clear" + "\r"
    ses_lib.run_command_cli(clr_cmd)
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],modify_value,list_threshold[3])  + "\r"
    output2=ses_lib.run_command_cli(cmd2)
    time.sleep(15)
    output3=ses_lib.run_command_cli(cmd)
    output4=output3.splitlines()
    pattern1="^{}\s+(\S+.*)\s+\d+'C\s+UW\s+\[{},{},{},{}\].*".format(temp_id,list_threshold[0],list_threshold[1],modify_value,list_threshold[3])
    count1=0
    for line1 in output4:
        match1=re.search(pattern1,line1)
        if match1:
            log.info(line1)
            temp_name=match1.group(1)
            temp_name=temp_name.rstrip()
            count1+=1
            break
    if count1==0:
        log.info("Threshold  value is not modified as expected")
        #raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("UW verfication successfull")
    cmd3="log get" + "\r"
    output5=ses_lib.run_command_cli(cmd3)
    output6=output5.splitlines()
    pattern2=".*{}.*Temp Failure\s+Assert, OverThres, w\s+\d+ 'C.*".format(temp_name)
    count2=0
    for line2 in output6:
       match2=re.search(pattern2,line2)
       if match2:
           log.info("Log updated for UW")
           count2+=1
           break
    if count2==0:
       log.info("Log not updated for UW")
       #raise RuntimeError("Log not updated for UW")
    else:
        log.info("UW verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3])  + "\r"
    output=ses_lib.run_command_cli(cmd2)
    time.sleep(20)
    cmd4="log get" + "\r"
    output7=ses_lib.run_command_cli(cmd4)
    output8=output7.splitlines()
    pattern3=".*{}.*Temp Failure\s+De-assert, OverThres, i\s+\d+ 'C.*".format(temp_name)
    count3=0
    for line2 in output8:
       match3=re.search(pattern3,line2)
       if match3:
           log.info("Log updated after setting threshold back to normal")
           count3+=1
           break
    if count3==0:
       log.info("Log not updated after setting threshold back to normal")
       #raise RuntimeError("Log not updated for UW")
    else:
        log.info("verfication in log successfull after setting threshold back to normal")
    if (count1 == 0):
       raise RuntimeError("Threshold  value is not modified as expected")
    if (count2==0) or (count3==0):
       raise RuntimeError("Log not updated properly")

@logThis
def CronussetAndVerifyUC():
    log.info("Inside  UC")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90" or ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = ses_lib.run_command_cli(cmd)
    log.info(output)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern="^(\S+)          .*?(\S+)'C\s+Normal\s+\[(\S+)\].*"
        match=re.search(pattern,line)
        if match:
            log.info(line)
            count+=1
            break
    if count==0:
        log.info("No Temp ID with numerical display available")
        raise RuntimeError("No Temp ID with numerical display available")
    temp_id=match.group(1)
    reading_value=match.group(2)
    threshold_value = match.group(3)
    list_threshold=list(threshold_value.split(","))
    modify_value_4=random.randint(0,int(reading_value)-1)
    modify_value_3=random.randint(0,int(modify_value_4))
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],modify_value_3,modify_value_4) + "\r"
    output2=ses_lib.run_command_cli(cmd2)
    time.sleep(15)
    output3=ses_lib.run_command_cli(cmd)
    log.info(output3)
    output4=output3.splitlines()
    pattern1="^{}\s+(\S+.*)\s+\d+'C\s+UC\s+\[{},{},{},{}\].*".format(temp_id,list_threshold[0],list_threshold[1],modify_value_3,modify_value_4)
    count1=0
    for line1 in output4:
        match1=re.search(pattern1,line1)
        if match1:
            log.info(line1)
            temp_name=match1.group(1)
            temp_name=temp_name.rstrip()
            count1+=1
            break
    if count1==0:
        log.info("Threshold  value is not modified as expected")
        #raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("UC verfication successfull")
    cmd3="log get" + "\r"
    output5=ses_lib.run_command_cli(cmd3)
    output6=output5.splitlines()
    log.info(output5)
    pattern2=".*{}.*Temp Failure\s+Assert, OverThres, c\s+\d+ 'C.*".format(temp_name)
    count2=0
    for line2 in output6:
       match2=re.search(pattern2,line2)
       if match2:
           log.info("Log updated for UC")
           count2+=1
           break
    if count2==0:
       log.info("Log not updated for UC")
       #raise RuntimeError("Log not updated for UC")
    else:
        log.info("UC verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3]) + "\r"
    output=ses_lib.run_command_cli(cmd2)
    cmd4="log get" + "\r"
    output7=ses_lib.run_command_cli(cmd4)
    output8=output7.splitlines()
    log.info(output7)
    pattern3=".*{}.*Temp Failure\s+De-assert, OverThres, i\s+\d+ 'C.*".format(temp_name)
    count3=0
    for line2 in output8:
       match3=re.search(pattern3,line2)
       if match3:
           log.info("Log updated after setting threshold back to normal")
           count3+=1
           break
    if count3==0:
       log.info("Log not updated after setting threshold back to normal")
    else:
        log.info("verfication in log successfull after setting threshold back to normal")
    if (count1 == 0): 
        raise RuntimeError("Threshold  value is not modified as expected")
    if (count2==0) or (count3==0):
        raise RuntimeError("Log not updated properly")

@logThis
def CronussetAndVerifyLW():
    log.info("Inside  LW")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90" or ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = ses_lib.run_command_cli(cmd)
    log.info(output)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern="^(\S+)          .*?(\S+)'C\s+Normal\s+\[(\S+)\].*"
        match=re.search(pattern,line)
        if match:
            log.info(line)
            count+=1
            break
    if count==0:
        log.info("No Temp ID with numerical display available")
        raise RuntimeError("No Temp ID with numerical display available")
    temp_id=match.group(1)
    reading_value=match.group(2)
    threshold_value = match.group(3)
    list_threshold=list(threshold_value.split(","))
    modify_value_2=random.randint(int(reading_value)+1,int(list_threshold[2])-1)
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],modify_value_2,list_threshold[2],list_threshold[3]) + "\r"
    output2=ses_lib.run_command_cli(cmd2)
    time.sleep(15)
    output3=ses_lib.run_command_cli(cmd)
    log.info(output3)
    output4=output3.splitlines()
    pattern1="^{}\s+(\S+.*)\s+\d+'C\s+LW\s+\[{},{},{},{}\].*".format(temp_id,list_threshold[0],modify_value_2,list_threshold[2],list_threshold[3])
    count1=0
    for line1 in output4:
        match1=re.search(pattern1,line1)
        if match1:
            log.info(line1)
            temp_name=match1.group(1)
            temp_name=temp_name.rstrip()
            count1+=1
            break
    if count1==0:
        log.info("Threshold  value is not modified as expected")
        #raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("LW verfication successfull")
    cmd3="log get" + "\r"
    output5=ses_lib.run_command_cli(cmd3)
    output6=output5.splitlines()
    log.info(output5)
    pattern2=".*{}.*Temp Failure\s+Assert, UnderThres, w\s+\d+ 'C.*".format(temp_name)
    count2=0
    for line2 in output6:
       match2=re.search(pattern2,line2)
       if match2:
           log.info("Log updated for LW")
           count2+=1
           break
    if count2==0:
       log.info("Log not updated for LW")
       #raise RuntimeError("Log not updated for LW")
    else:
        log.info("LW verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3]) + "\r"
    output=ses_lib.run_command_cli(cmd2)
    time.sleep(15)
    cmd4="log get" + "\r"
    output7=ses_lib.run_command_cli(cmd4)
    output8=output7.splitlines()
    log.info(output7)
    pattern3=".*{}.*Temp Failure\s+De-assert, UnderThres, i\s+\d+ 'C.*".format(temp_name)
    count3=0
    for line2 in output8:
       match3=re.search(pattern3,line2)
       if match3:
           log.info("Log updated after setting threshold back to normal")
           count3+=1
           break
    if count3==0:
       log.info("Log not updated after setting threshold back to normal")
    else:
        log.info("verfication in log successfull after setting threshold back to normal")
    if count1==0:
       raise RuntimeError("Threshold  value is not modified as expected")
    if (count2==0) or (count3==0):
       raise RuntimeError("Log not updated properly")

@logThis
def CronussetAndVerifyLC():
    log.info("Inside  LC")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90" or ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = ses_lib.run_command_cli(cmd)
    log.info(output)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern="^(\S+)          .*?(\S+)'C\s+Normal\s+\[(\S+)\].*"
        match=re.search(pattern,line)
        if match:
            log.info(line)
            count+=1
            break
    if count==0:
        log.info("No Temp ID with numerical display available")
        raise RuntimeError("No Temp ID with numerical display available")
    temp_id=match.group(1)
    reading_value=match.group(2)
    threshold_value = match.group(3)
    list_threshold=list(threshold_value.split(","))
    modify_value_2=random.randint(int(reading_value)+1,int(list_threshold[2])-1)
    modify_value_1=random.randint(int(reading_value)+1,modify_value_2)
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,modify_value_1,modify_value_2,list_threshold[2],list_threshold[3]) + "\r"
    output2=ses_lib.run_command_cli(cmd2)
    time.sleep(15)
    output3=ses_lib.run_command_cli(cmd)
    log.info(output3)
    output4=output3.splitlines()
    pattern1="^{}\s+(\S+.*)\s+\d+'C\s+LC\s+\[{},{},{},{}\].*".format(temp_id,modify_value_1,modify_value_2,list_threshold[2],list_threshold[3])
    count1=0
    for line1 in output4:
        match1=re.search(pattern1,line1)
        if match1:
            log.info(line1)
            temp_name=match1.group(1)
            temp_name=temp_name.rstrip()
            count1+=1
            break
    if count1==0:
        log.info("Threshold  value is not modified as expected")
        #raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("LC verfication successfull")
    cmd3="log get" + "\r"
    output5=ses_lib.run_command_cli(cmd3)
    output6=output5.splitlines()
    log.info(output5)
    pattern2=".*{}.*Temp Failure\s+Assert, UnderThres, c\s+\d+ 'C.*".format(temp_name)
    count2=0
    for line2 in output6:
       match2=re.search(pattern2,line2)
       if match2:
           log.info("Log updated for LC")
           count2+=1
           break
    if count2==0:
       log.info("Log not updated for LC")
       #raise RuntimeError("Log not updated for LC")
    else:
        log.info("LC verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3]) + "\r"
    output=ses_lib.run_command_cli(cmd2)
    time.sleep(15)
    cmd4="log get" + "\r"
    output7=ses_lib.run_command_cli(cmd4)
    output8=output7.splitlines()
    log.info(output7)
    pattern3=".*{}.*Temp Failure\s+De-assert, UnderThres, i\s+\d+ 'C.*".format(temp_name)
    count3=0
    for line2 in output8:
       match3=re.search(pattern3,line2)
       if match3:
           log.info("Log updated after setting threshold back to normal")
           count3+=1
           break
    if count3==0:
       log.info("Log not updated after setting threshold back to normal")
    else:
        log.info("verfication in log successfull after setting threshold back to normal")
    if count1==0:
        raise RuntimeError("Threshold  value is not modified as expected")
    if (count2==0) or (count3==0):
       raise RuntimeError("Log not updated properly")    


@logThis
def CronussetvoltageandverifyUW():
    log.info("Inside  UW")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="power get"
    output = ses_lib.run_ESM_command(cmd)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern=".*Normal.*"
        match=re.search(pattern,line)
        if match:
            pattern1="^(\S+)\s+(\S+)\s(\S+).*\s(\S+)V.*"
            if ProductTypeInfo == "SD4100":
                pattern1="^(\S+)\s+(\S+\s+\S+)\s+(\S+)\s+(\S+)V.*"
            match1=re.search(pattern1,line)
            if match1:
                sensor_ID=match1.group(1)
                log.info(sensor_ID)
                sensor_name=match1.group(2)
                log.info(sensor_name)
                sensor_value=match1.group(3)
                log.info(sensor_value)
                read_value=match1.group(4)
                log.info(read_value)
                log.info("%s %s %s %s" %(sensor_ID,sensor_name,sensor_value,read_value))
                actual_value=((float(read_value)-float(sensor_value))/float(sensor_value))*100
                if actual_value < 0:
                    log.info("pass")
                    count+=1
                    break
    if count==0:
        log.info("No Voltage ID available for UW")
        raise RuntimeError("No Voltage ID available for UW")
    clr_cmd="log clear"
    ses_lib.run_ESM_command(clr_cmd)
    cmd1="threshold set {} 10 0 5 6".format(sensor_ID)
    output2=ses_lib.run_ESM_command(cmd1)
    time.sleep(15)
    output3=ses_lib.run_ESM_command(cmd)
    output3=output3.splitlines()
    count=0
    for line in output3:
        pattern="^{}.*Abnormal\s+\[-10%,-0%,\+5%,\+6%\].*".format(sensor_ID)
        match2=re.search(pattern,line)
        if match2:
            log.success("UW check successful")
            count+=1
            break
    if count==0:
        log.fail("UW check not updated")
        #raise RuntimeError("UW check not updated")
    cmd3="log get"
    output5=ses_lib.run_ESM_command(cmd3)
    output6=output5.splitlines()
    pattern2=".*{} {}.*Vol Failure\s+Assert, UnderThres, w.*".format(sensor_name,sensor_value)
    log.info(pattern2)
    count2=0
    for line2 in output6:
       match2=re.search(pattern2,line2)
       if match2:
           log.info("Log updated for UW")
           count2+=1
           break
    if count2==0:
       log.info("Log not updated for UW")
       #raise RuntimeError("Log not updated for UW")
    else:
        log.info("UW verfication in log successfull")
    #Cleanup
    clr_cmd="log clear"
    ses_lib.run_ESM_command(clr_cmd)
    cmd1="threshold set {} 10 5 5 6".format(sensor_ID)
    ses_lib.run_ESM_command(cmd1)
    time.sleep(15)
    cmd4="log get"
    output7=ses_lib.run_ESM_command(cmd4)
    output8=output7.splitlines()
    pattern3=".*{} {}.*Vol Failure\s+De-assert, UnderThres, i.*".format(sensor_name,sensor_value)
    log.info(pattern3)
    count3=0
    for line2 in output8:
       match3=re.search(pattern3,line2)
       if match3:
           log.info("Log updated for UW after clearning threshold")
           count3+=1
           break
    if count3==0:
       log.info("Log not updated for UW after clearning threshold")
       #raise RuntimeError("Log not updated for UW")
    else:
        log.info("UW verfication in log successfull after clearning threshold") 
    if (count == 0):
        raise RuntimeError("UW check not updated")
    if (count2 == 0) or (count3 == 0):
        raise RuntimeError("Log verification not successful")

@logThis
def CronussetvoltageandverifyUC():
    log.info("Inside  UC")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90" or ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="power get"
    output = ses_lib.run_ESM_command(cmd)
    log.info(output)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern=".*Normal.*"
        match=re.search(pattern,line)
        if match:
            pattern1="^(\S+)\s+(\S+)\s(\S+).*\s(\S+)V.*"
            match1=re.search(pattern1,line)
            if match1:
                sensor_ID=match1.group(1)
                sensor_name=match1.group(2)
                sensor_value=match1.group(3)
                read_value=match1.group(4)
                #actual_value=((float(read_value)-float(sensor_value))/float(sensor_value))*100
                #if actual_value < 0:
                #    log.info("pass")
                #    log.info(line)
                #    count+=1
                #    break
    #if count==0:
    #    log.fail("No Voltage ID available for UC")
        #raise RuntimeError("No Voltage ID available for UC")
    clr_cmd="log clear"
    ses_lib.run_ESM_command(clr_cmd)
    cmd1="threshold set {} 0 5 5 6".format(sensor_ID)
    output2=ses_lib.run_ESM_command(cmd1)
    time.sleep(15)
    output3=ses_lib.run_ESM_command(cmd)
    output3=output3.splitlines()
    count=0
    for line in output3:
        pattern="^{}.*Abnormal\s+\[-0%,-5%,\+5%,\+6%\].*".format(sensor_ID)
        match2=re.search(pattern,line)
        if match2:
            log.success("UC check successful")
            count+=1
            break
    if count==0:
        log.fail("UC check not updated")
        #raise RuntimeError("UV check not updated")
    cmd3="log get"
    output5=ses_lib.run_ESM_command(cmd3)
    output6=output5.splitlines()
    pattern2=".*{} {}.*Vol Failure\s+Assert, UnderThres, c.*".format(sensor_name,sensor_value)
    count2=0
    for line2 in output6:
       match2=re.search(pattern2,line2)
       if match2:
           log.info("Log updated for UC")
           count2+=1
           break
    if count2==0:
       log.info("Log not updated for UC")
       #raise RuntimeError("Log not updated for UV")
    else:
        log.info("UC verfication in log successfull")
    #Cleanup
    clr_cmd="log clear"
    ses_lib.run_ESM_command(clr_cmd)
    cmd1="threshold set {} 10 5 5 6".format(sensor_ID)
    ses_lib.run_ESM_command(cmd1)
    time.sleep(15)
    cmd4="log get"
    output7=ses_lib.run_ESM_command(cmd4)
    output8=output7.splitlines()
    pattern3=".*{} {}.*Vol Failure\s+De-assert, UnderThres, i.*".format(sensor_name,sensor_value)
    log.info(pattern3)
    count3=0
    for line2 in output8:
       match3=re.search(pattern3,line2)
       if match3:
           log.info("Log updated for UC after clearning threshold")
           count3+=1
           break
    if count3==0:
       log.info("Log not updated for UC after clearning threshold")
       #raise RuntimeError("Log not updated for UW")
    else:
        log.info("UC verfication in log successfull after clearning threshold")
    if (count == 0):
        raise RuntimeError("UC check not updated")
    if (count2 == 0) or (count3 == 0):
        raise RuntimeError("Log verification not successful")

@logThis
def CronussetvoltageandverifyOW():
    log.info("Inside  OW")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90" or ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="power get"
    output = ses_lib.run_ESM_command(cmd)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern=".*Normal.*"
        match=re.search(pattern,line)
        if match:
            pattern1="^(\S+)\s+(\S+)\s(\S+).*\s(\S+)V.*"
            match1=re.search(pattern1,line)
            if match1:
                sensor_ID=match1.group(1)
                sensor_name=match1.group(2)
                sensor_value=match1.group(3)
                read_value=match1.group(4)
                #actual_value=((float(read_value)-float(sensor_value))/float(sensor_value))*100
                #if actual_value >= 1:
                #    log.info("pass")
                #    log.info(line)
                #    count+=1
                #    break
    #if count==0:
    #    log.fail("No Voltage ID available for OW")
        #raise RuntimeError("No Voltage ID available for OW")
    clr_cmd="log clear"
    ses_lib.run_ESM_command(clr_cmd)
    cmd1="threshold set {} 10 8 3 3".format(sensor_ID)
    output2=ses_lib.run_ESM_command(cmd1)
    time.sleep(15)
    output3=ses_lib.run_ESM_command(cmd)
    output3=output3.splitlines()
    count=0
    for line in output3:
        pattern="^{}.*Abnormal\s+\[-10%,-8%,\+3%,\+3%\].*".format(sensor_ID)
        match2=re.search(pattern,line)
        if match2:
            log.success("OW check successful")
            count+=1
            break
    if count==0:
        log.fail("OW check not updated")
        #raise RuntimeError("OW check not updated")
    cmd3="log get"
    output5=ses_lib.run_ESM_command(cmd3)
    output6=output5.splitlines()
    pattern2=".*{} {}.*Vol Failure\s+Assert, OverThres, c.*".format(sensor_name,sensor_value)
    log.info(pattern2)
    count2=0
    for line2 in output6:
       match2=re.search(pattern2,line2)
       if match2:
           log.info("Log updated for OW")
           count2+=1
           break
    if count2==0:
       log.info("Log not updated for OW")
       #raise RuntimeError("Log not updated for OW")
    else:
        log.info("OW verfication in log successfull")
    #Cleanup
    clr_cmd="log clear"
    ses_lib.run_ESM_command(clr_cmd)
    cmd1="threshold set {} 10 8 8 10".format(sensor_ID)
    ses_lib.run_ESM_command(cmd1)
    time.sleep(15)
    cmd4="log get"
    output7=ses_lib.run_ESM_command(cmd4)
    output8=output7.splitlines()
    pattern3=".*{} {}.*Vol Failure\s+De-assert, OverThres, i.*".format(sensor_name,sensor_value)
    log.info(pattern3)
    count3=0
    for line2 in output8:
       match3=re.search(pattern3,line2)
       if match3:
           log.info("Log updated for OW after clearning threshold")
           count3+=1
           break
    if count3==0:
       log.info("Log not updated for OW after clearning threshold")
       #raise RuntimeError("Log not updated for UW")
    else:
        log.info("OW verfication in log successfull after clearning threshold")
    if (count == 0):
        raise RuntimeError("OW check not updated")
    if (count2 == 0) or (count3 == 0):
        raise RuntimeError("Log verification not successful")

@logThis
def CronussetvoltageandverifyOC():
    log.info("Inside  OC")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90" or ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="power get"
    output = ses_lib.run_ESM_command(cmd)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern=".*Normal.*"
        match=re.search(pattern,line)
        if match:
            pattern1="^(\S+)\s+(\S+)\s(\S+).*\s(\S+)V.*"
            match1=re.search(pattern1,line)
            if match1:
                sensor_ID=match1.group(1)
                sensor_name=match1.group(2)
                sensor_value=match1.group(3)
                read_value=match1.group(4)
                #actual_value=((float(read_value)-float(sensor_value))/float(sensor_value))*100
                #if actual_value >= 1:
                #    log.info("pass")
                #    log.info(line)
                #    count+=1
                #    break
    #if count==0:
    #    log.fail("No Voltage ID available for OC")
        #raise RuntimeError("No Voltage ID available for OC")
    clr_cmd="log clear"
    ses_lib.run_ESM_command(clr_cmd)
    cmd1="threshold set {} 10 8 3 5".format(sensor_ID)
    output2=ses_lib.run_ESM_command(cmd1)
    time.sleep(15)
    output3=ses_lib.run_ESM_command(cmd)
    output3=output3.splitlines()
    count=0
    for line in output3:
        pattern="^{}.*Abnormal\s+\[-10%,-8%,\+3%,\+5%\].*".format(sensor_ID)
        match2=re.search(pattern,line)
        if match2:
            log.success("OC check successful")
            count+=1
            break
    if count==0:
        log.fail("OC check not updated")
        #raise RuntimeError("OC check not updated")
    cmd3="log get"
    output5=ses_lib.run_ESM_command(cmd3)
    output6=output5.splitlines()
    pattern2=".*{} {}.*Vol Failure\s+Assert, OverThres, w.*".format(sensor_name,sensor_value)
    log.info(pattern2)
    count2=0
    for line2 in output6:
       match2=re.search(pattern2,line2)
       if match2:
           log.info("Log updated for OC")
           count2+=1
           break
    if count2==0:
       log.info("Log not updated for OC")
       #raise RuntimeError("Log not updated for OC")
    else:
        log.info("OC verfication in log successfull")
    #Cleanup
    clr_cmd="log clear"
    ses_lib.run_ESM_command(clr_cmd)
    cmd1="threshold set {} 10 8 8 10".format(sensor_ID)
    ses_lib.run_ESM_command(cmd1)
    time.sleep(15)
    cmd4="log get"
    output7=ses_lib.run_ESM_command(cmd4)
    output8=output7.splitlines()
    pattern3=".*{} {}.*Vol Failure\s+De-assert, OverThres, i.*".format(sensor_name,sensor_value)
    log.info(pattern3)
    count3=0
    for line2 in output8:
       match3=re.search(pattern3,line2)
       if match3:
           log.info("Log updated for OC after clearning threshold")
           count3+=1
           break
    if count3==0:
       log.info("Log not updated for OC after clearning threshold")
       #raise RuntimeError("Log not updated for UW")
    else:
        log.info("OC verfication in log successfull after clearning threshold")
    if (count == 0):
        raise RuntimeError("OC check not updated")
    if (count2 == 0) or (count3 == 0):
        raise RuntimeError("Log verification not successful")

@logThis
def CronusqueryExpanders(index='3'):
  cmd="ls /dev/bsg/expander-%s\:*" %index
  p_device = "(/dev/bsg/expander\-%s\:\d+).*" %index
  output = ses_lib.run_command(cmd)
  error_msg = "Didn't find available expander."
  device_list = ses_lib.find_matches(p_device, output, error_msg)
  return device_list

@logThis
def setESCIDENTBit(hdd):
    Ident_1 = { "Ident=1" : "Ident=1"}
    Ident_0 = { "Ident=0" : "Ident=0"}
    check_esc0_ident_cmd = "sg_ses --page=0x02 --index=esc,0 {}".format(hdd)
    check_esc1_ident_cmd = "sg_ses --page=0x02 --index=esc,1 {}".format(hdd)
    output1 = ses_lib.run_command(check_esc0_ident_cmd)
    output11 = ses_lib.run_command(check_esc1_ident_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_0,check_output=output1)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_0,check_output=output11)
    set_ESC_IDENT_cmd = "sg_ses --page=0x02 --index=esc,-1 --set=1:7:1=1 {}".format(hdd)
    ses_lib.run_command(set_ESC_IDENT_cmd)
    time.sleep(5)
    output2 = ses_lib.run_command(check_esc0_ident_cmd)
    output22 = ses_lib.run_command(check_esc1_ident_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_1,check_output=output2)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_1,check_output=output22)
    clear_ESC_IDENT_cmd = "sg_ses --page=0x02 --index=esc,-1 --clear=1:7:1=0 {}".format(hdd)
    ses_lib.run_command(clear_ESC_IDENT_cmd)
    time.sleep(5)
    output3 = ses_lib.run_command(check_esc0_ident_cmd)
    output33 = ses_lib.run_command(check_esc1_ident_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_0,check_output=output3)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_0,check_output=output33)

@logThis
def setdiskIDENTBit(hdd):
    Ident_1 = { "Ident=1" : "Ident=1"}
    Ident_0 = { "Ident=0" : "Ident=0"}
    Ident_1_pattern = "Ident=1"
    err_count = 0
    for i in range(12):
          check_disk_ident_cmd = "sg_ses --page=0x02 --index=arr,{} {}".format(i,hdd)
          output1 = ses_lib.run_command(check_disk_ident_cmd)
          CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_0,check_output=output1)
    set_disk_IDENT_cmd = "sg_ses --page=0x02 --index=arr,-1 --set=2:1:1=1 {}".format(hdd)
    ses_lib.run_command(set_disk_IDENT_cmd)
    time.sleep(5)
    for i in range(12):
          check_disk_ident_cmd = "sg_ses --page=0x02 --index=arr,{} {}".format(i,hdd)
          output2 = ses_lib.run_command(check_disk_ident_cmd)
          match = re.search(Ident_1_pattern, output2)
          if match:
             log.info("Disk ident bit verification is successful")
          else:
             log.info("Disk ident bit verification failed")
             err_count += 1
    clear_disk_IDENT_cmd = "sg_ses --page=0x02 --index=arr,-1 --clear=2:1:1=0 {}".format(hdd)
    ses_lib.run_command(clear_disk_IDENT_cmd)
    time.sleep(5)
    for i in range(12):
          check_disk_ident_cmd = "sg_ses --page=0x02 --index=arr,{} {}".format(i,hdd)
          output3 = ses_lib.run_command(check_disk_ident_cmd)
          CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_0,check_output=output3)
    if err_count:
        raise RuntimeError('Disk ident bit set failed')

@logThis
def setdiskFaultBit(hdd):
    Fault_reqstd_0 = { "Fault_reqstd=0" : "Fault reqstd=0"}
    Fault_reqstd_1_pattern = "Fault reqstd=1"
    err_count = 0
    for i in range(12):
          check_disk_fault_cmd = "sg_ses --page=0x02 --index=arr,{} {}".format(i,hdd)
          output1 = ses_lib.run_command(check_disk_fault_cmd)
          CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fault_reqstd_0,check_output=output1)
    set_disk_fault_reqs_cmd = "sg_ses --page=0x02 --index=arr,-1 --set=3:5:1=1 {}".format(hdd)
    ses_lib.run_command(set_disk_fault_reqs_cmd)
    time.sleep(5)
    for i in range(12):
          check_disk_fault_cmd = "sg_ses --page=0x02 --index=arr,{} {}".format(i,hdd)
          output2 = ses_lib.run_command(check_disk_fault_cmd)
          match = re.search(Fault_reqstd_1_pattern, output2)
          if match:
             log.info("Disk fault requested bit verification is successful")
          else:
             log.info("Disk fault requested bit verification failed")
             err_count += 1
    clear_disk_fault_reqs_cmd = "sg_ses --page=0x02 --index=arr,-1 --clear=3:5:1=0 {}".format(hdd)
    ses_lib.run_command(clear_disk_fault_reqs_cmd)
    time.sleep(5)
    for i in range(12):
          check_disk_fault_cmd = "sg_ses --page=0x02 --index=arr,{} {}".format(i,hdd)
          output3 = ses_lib.run_command(check_disk_fault_cmd)
          CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fault_reqstd_0,check_output=output3)
    if err_count:
        raise RuntimeError('Disk fault request bit set failed')

@logThis
def setdiskremapledBit(hdd):
    rebuild_remap_led_0 = { "rebuild remap=0" : " Rebuild/remap=0"}
    rebuild_remap_led_1_pattern = "Rebuild/remap=1"
    err_count = 0
    for i in range(12):
          check_rebuild_remap_cmd = "sg_ses --page=0x02 --index=arr,{} {}".format(i,hdd)
          output1 = ses_lib.run_command(check_rebuild_remap_cmd)
          CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=rebuild_remap_led_0,check_output=output1)
    set_rebuild_remap_led_cmd = "sg_ses --page=0x02 --index=arr,-1 --set=1:1:1=1 {}".format(hdd)
    ses_lib.run_command(set_rebuild_remap_led_cmd)
    time.sleep(5)
    for i in range(12):
          check_rebuild_remap_cmd = "sg_ses --page=0x02 --index=arr,{} {}".format(i,hdd)
          output2 = ses_lib.run_command(check_rebuild_remap_cmd)
          match = re.search(rebuild_remap_led_1_pattern, output2)
          if match:
             log.info("Disk Rebuild/Remap bit verification is successful")
          else:
             log.info("Disk Rebuild/Remap bit verification failed")
             err_count += 1
    clear_rebuild_remap_cmd = "sg_ses --page=0x02 --index=arr,-1 --clear=1:1:1=0 {}".format(hdd)
    ses_lib.run_command(clear_rebuild_remap_cmd)
    time.sleep(5)
    for i in range(12):
          check_rebuild_remap_cmd = "sg_ses --page=0x02 --index=arr,{} {}".format(i,hdd)
          output3 = ses_lib.run_command(check_rebuild_remap_cmd)
          CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=rebuild_remap_led_0,check_output=output3)
    if err_count:
        raise RuntimeError('Disk Rebuild/Remap bit set failed')

@logThis
def setESCFaultBit(hdd):
    Fail_1 = { "Fail=1" : "Fail=1"}
    Fail_0 = { "Fail=0" : "Fail=0"}
    check_esc0_fail_cmd = "sg_ses --page=0x02 --index=esc,0 {}".format(hdd)
    check_esc1_fail_cmd = "sg_ses --page=0x02 --index=esc,1 {}".format(hdd)
    output1 = ses_lib.run_command(check_esc0_fail_cmd)
    output11 = ses_lib.run_command(check_esc1_fail_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fail_0,check_output=output1)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fail_0,check_output=output11)
    set_ESC_Fault_cmd = "sg_ses --page=0x02 --index=esc,-1 --set=1:6:1=1 {}".format(hdd)
    ses_lib.run_command(set_ESC_Fault_cmd)
    time.sleep(5)
    output2 = ses_lib.run_command(check_esc0_fail_cmd)
    output22 = ses_lib.run_command(check_esc1_fail_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fail_1,check_output=output2)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fail_1,check_output=output22)
    clear_ESC_fail_cmd = "sg_ses --page=0x02 --index=esc,-1 --clear=1:6:1=0 {}".format(hdd)
    ses_lib.run_command(clear_ESC_fail_cmd)
    time.sleep(5)
    output3 = ses_lib.run_command(check_esc0_fail_cmd)
    output33 = ses_lib.run_command(check_esc1_fail_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fail_0,check_output=output3)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fail_0,check_output=output33)

@logThis
def setencIdentBit(hdd):
    Ident_1 = { "Ident=1" : "Ident=1"}
    Ident_0 = { "Ident=0" : "Ident=0"}
    check_enc0_ident_cmd = "sg_ses --page=0x02 --index=enc,0 {}".format(hdd)
    output1 = ses_lib.run_command(check_enc0_ident_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_0,check_output=output1)
    set_ENC_IDENT_cmd = "sg_ses --page=0x02 --index=enc,-1 --set=1:7:1=1 {}".format(hdd)
    ses_lib.run_command(set_ENC_IDENT_cmd)
    time.sleep(5)
    output2 = ses_lib.run_command(check_enc0_ident_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_1,check_output=output2)
    clear_ENC_IDENT_cmd = "sg_ses --page=0x02 --index=enc,-1 --clear=1:7:1=0 {}".format(hdd)
    ses_lib.run_command(clear_ENC_IDENT_cmd)
    time.sleep(5)
    output3 = ses_lib.run_command(check_enc0_ident_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Ident_0,check_output=output3)

@logThis
def setencFaultBit(hdd):
    Fail_1 = { "Fail_ind=1" : "Failure indication=1","Fail_reqs=1" : "Failure requested=1" }
    Fail_0 = { "Fail_ind=0" : "Failure indication=0","Fail_reqs=0" : "Failure requested=0" }
    check_enc0_fail_cmd = "sg_ses --page=0x02 --index=enc,0 {}".format(hdd)
    output1 = ses_lib.run_command(check_enc0_fail_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fail_0,check_output=output1)
    set_ENC_Fail_cmd = "sg_ses --page=0x02 --index=enc,-1 --set=3:1:1=1 {}".format(hdd)
    ses_lib.run_command(set_ENC_Fail_cmd)
    time.sleep(5)
    output2 = ses_lib.run_command(check_enc0_fail_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fail_1,check_output=output2)
    clear_ENC_Fail_cmd = "sg_ses --page=0x02 --index=enc,-1 --set=3:1:1=0 {}".format(hdd)
    ses_lib.run_command(clear_ENC_Fail_cmd)
    time.sleep(5)
    output3 = ses_lib.run_command(check_enc0_fail_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Fail_0,check_output=output3)

@logThis
def setencWarningBit(hdd):
    Warning_1 = { "Warning_ind=1" : "Warning indication=1","Warning_reqs=1" : "Warning requested=1" }
    Warning_0 = { "Warning_ind=0" : "Warning indication=0","Warning_reqs=0" : "Warning requested=0" }
    check_enc0_warning_cmd = "sg_ses --page=0x02 --index=enc,0 {}".format(hdd)
    output1 = ses_lib.run_command(check_enc0_warning_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Warning_0,check_output=output1)
    set_ENC_Warning_cmd = "sg_ses --page=0x02 --index=enc,-1 --set=3:0:1=1 {}".format(hdd)
    ses_lib.run_command(set_ENC_Warning_cmd)
    time.sleep(5)
    output2 = ses_lib.run_command(check_enc0_warning_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Warning_1,check_output=output2)
    clear_ENC_Warning_cmd = "sg_ses --page=0x02 --index=enc,-1 --set=3:0:1=0 {}".format(hdd)
    ses_lib.run_command(clear_ENC_Warning_cmd)
    time.sleep(5)
    output3 = ses_lib.run_command(check_enc0_warning_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=Warning_0,check_output=output3)

@logThis
def CLITempVerifyNormal():
    log.info("Inside  Normal")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = ses_lib.run_command_cli(cmd)
    log.info(output)
    output1=output.splitlines()
    count=0
    for line in output1:
         pattern="^(\S+)          .*?(\S+)'C\s+Normal\s+\[(\S+)\].*"
         match=re.search(pattern,line)
         if match:
            log.info(line)
            count+=1
            break
    if count==0:
        log.info("No Temp ID with numerical display available")
        raise RuntimeError("No Temp ID with numerical display available")
    clr_cmd="log clear" + "\r"
    ses_lib.run_command_cli(clr_cmd)

@logThis
def CLITempVerifyUC():
    log.info("Inside  UC")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = ses_lib.run_command_cli(cmd)
    log.info(output)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern="^(\S+)          .*?(\S+)'C\s+UC\s+\[(\S+)\].*"
        match=re.search(pattern,line)
        if match:
            log.info(line)
            count+=1
            break
    if count==0:
        log.info("No Temp ID with numerical display available")
        raise RuntimeError("No Temp ID with numerical display available")
    clr_cmd="log clear" + "\r"
    ses_lib.run_command_cli(clr_cmd)

@logThis
def CLITempVerifyLC():
    log.info("Inside  LC")
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = ses_lib.run_command_cli(cmd)
    log.info(output)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern="^(\S+)          .*?(\S+)'C\s+LC\s+\[(\S+)\].*"
        match=re.search(pattern,line)
        if match:
            log.info(line)
            count+=1
            break
    if count==0:
        log.info("No Temp ID with numerical display available")
        raise RuntimeError("No Temp ID with numerical display available")
    clr_cmd="log clear" + "\r"
    ses_lib.run_command_cli(clr_cmd)

@logThis
def SetSMPPhyPartialandSlumber(expander):
   smp_discover_cmd="{}{}".format("smp_discover ",expander)
   output=ses_lib.run_command(smp_discover_cmd)
   output=output.splitlines()
   pattern=".*phy\s+(\S+)\:U\:attached.*"
   for line in output:
      match=re.search(pattern,line)
      if match:
          attached_phy=match.group(1)
          break
   smp_discover_pg_cmd="{}{} -p {}".format("smp_discover ",expander,attached_phy)
   discover_output=ses_lib.run_command(smp_discover_pg_cmd)
   pattern="sas slumber enabled: 0"
   pattern1="sas partial enabled: 0"
   pattern2="sata slumber enabled: 0"
   pattern3="sata partial enabled: 0"
   ses_lib.common_check_patern_2(discover_output,pattern,"sas slumber disabled check",expect=True)
   ses_lib.common_check_patern_2(discover_output,pattern1,"sas partial disabled check",expect=True)
   ses_lib.common_check_patern_2(discover_output,pattern2,"sata slumber disabled check",expect=True)
   ses_lib.common_check_patern_2(discover_output,pattern3,"sata partial disabled check",expect=True)
   phy_control_cmd="smp_phy_control {} -p {} -q 1 -l 1".format(expander,attached_phy)
   output=ses_lib.run_command(phy_control_cmd)
   time.sleep(5)
   updated_discover_output=ses_lib.run_command(smp_discover_pg_cmd)
   pattern4="sas slumber enabled: 1"
   pattern5="sas partial enabled: 1"
   pattern6="sata slumber enabled: 0"
   pattern7="sata partial enabled: 0"
   ses_lib.common_check_patern_2(discover_output,pattern4,"sas slumber enabled check",expect=True)
   ses_lib.common_check_patern_2(discover_output,pattern5,"sas partial enabled check",expect=True)
   ses_lib.common_check_patern_2(discover_output,pattern6,"sata slumber disabled check",expect=True)
   ses_lib.common_check_patern_2(discover_output,pattern7,"sata partial disabled check",expect=True)
   restore_cmd="smp_phy_control {} -p {} -q 0 -l 0".format(expander,attached_phy)
   ses_lib.run_command(restore_cmd)
   pattern14="sas slumber enabled: 0"
   pattern15="sas partial enabled: 0"
   ses_lib.common_check_patern_2(discover_output,pattern14,"sas slumber disabled check",expect=True)
   ses_lib.common_check_patern_2(discover_output,pattern15,"sas partial disabled check",expect=True)
   sata_phy_control_cmd="smp_phy_control {} -p {} -Q 1 -L 1".format(expander,attached_phy)
   output=ses_lib.run_command(sata_phy_control_cmd)
   time.sleep(5)
   updated_discover_output=ses_lib.run_command(smp_discover_pg_cmd)
   pattern10="sata slumber enabled: 1"
   pattern11="sata partial enabled: 1"
   ses_lib.common_check_patern_2(discover_output,pattern10,"sata slumber enabled check",expect=True)
   ses_lib.common_check_patern_2(discover_output,pattern11,"sata partial enabled check",expect=True)
   restore_cmd="smp_phy_control {} -p {} -Q 0 -L 0".format(expander,attached_phy)
   ses_lib.run_command(restore_cmd)
   pattern12="sata slumber enabled: 0"
   pattern13="sata partial enabled: 0"
   ses_lib.common_check_patern_2(discover_output,pattern12,"sata slumber disabled check",expect=True)
   ses_lib.common_check_patern_2(discover_output,pattern13,"sata partial disabled check",expect=True)

@logThis
def checkLogStatusCronus(device):
     cmd = 'log get' + "\r"
     ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
     if ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
     ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
     output = ses_lib.run_command_cli(cmd)
     log.info(output)
     pattern1="Event Log.*: 1/510 entries"
     pattern2="Critical: 0/1"
     pattern3="Warning: 0/1"
     pattern4="Info: 1/1"
     ses_lib.common_check_patern_2(output, pattern1, "Event Log Check", expect=True)
     ses_lib.common_check_patern_2(output, pattern2, "Critical Log Check", expect=True)
     ses_lib.common_check_patern_2(output, pattern3, "Warning Log Check", expect=True)
     ses_lib.common_check_patern_2(output, pattern4, "Info Log Check", expect=True)

@logThis
def checkPSUDetailsWithCLICronus(psu_pattern,cmd,PSU_NO, HDD, device):
    cmd1 = "{} {}".format(cmd,HDD)
    output = ses_lib.run_command(cmd1)
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "SD4100":
       ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
       ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cli_cmd = 'fru get' + "\r"
    output1 = ses_lib.run_command_cli(cli_cmd)
    log.info(output1)
    if PSU_NO == "1" or PSU_NO == "2" or PSU_NO == "3":
        psu_page_pattern='Element \d descriptor: \S+ \d\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s.*'
    else:
        psu_page_pattern='Element \d descriptor: \S+ \d\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s.*'
    log.info(psu_page_pattern)
    match=re.search(psu_page_pattern,output)
    if match:
        if PSU_NO == "4":
            PART_num=match.group(1)
            SRV_TAG=match.group(2)
            HW=match.group(3)
            psu_pattern = psu_pattern.format(PART_num,SRV_TAG,HW)
        else:
            PSTYPE=match.group(1)
            PSTYPE_1=match.group(2)
            SRV_TAG=match.group(3)
            EC_LEVEL=match.group(4)
            PSTYPE_CONCAT=PSTYPE+" "+PSTYPE_1
            psu_pattern = psu_pattern.format(PSTYPE_CONCAT,SRV_TAG,EC_LEVEL)
    log.info(psu_pattern)
    match=re.search(psu_pattern,output1)
    if match:
        log.info("Expected pattern found in CLI command as expected")
    else:
        log.info("Expected pattern not found in CLI command")
        raise RuntimeError("Pattern match failed")

@logThis
def verify_PHY_enable_disable_on_secondaryexpander1_Cronus():
   log.info("Inside secondary expander1")
   ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
   if ProductTypeInfo == "SD4100":
       ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
       ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
   ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
   drv_cmd="drv get\r"
   disable_cmd="phy disable 10\r"
   enable_cmd="phy enable 10\r"
   enable_pattern=".*10\s+Slot11\s+OK.*"
   disable_pattern=".*10\s+Slot11\s+Not Available.*"
   disable_cmd_pattern="PHY 10 disabled"
   enable_cmd_pattern="PHY 10 enabled"
   output=ses_lib.run_command_cli(drv_cmd)
   match=re.search(enable_pattern,output)
   if match:
       log.info("Slot ID 10 is enabled.Verify disable and enable function")
       disable_cmd_output=ses_lib.run_command_cli(disable_cmd)
       ses_lib.common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       time.sleep(20)
       disable_update_output=ses_lib.run_command_cli(drv_cmd)
       ses_lib.common_check_patern_2(disable_update_output,disable_pattern,"PHY Disabled Update check in Slot",expect=True)
       ses_lib.enable_cmd_output=run_command_cli(enable_cmd)
       ses_lib.common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "PHY Enable Check", expect=True)
       time.sleep(60)
       enable_update_output=ses_lib.run_command_cli(drv_cmd)
       ses_lib.common_check_patern_2(enable_update_output,enable_pattern,"PHY Enable Update check in slot",expect=True)
   else :
       log.info("Slot ID 10 is diabled.Verify enable and disable function")
       enable_cmd_output=ses_lib.run_command_cli(enable_cmd)
       ses_lib.common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "PHY Enable Check", expect=True)
       time.sleep(60)
       enable_update_output=ses_lib.run_command_cli(drv_cmd)
       ses_lib.common_check_patern_2(enable_update_output,enable_pattern,"PHY Enable Update check in slot",expect=True)
       disable_cmd_output=ses_lib.run_command_cli(disable_cmd)
       ses_lib.common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       time.sleep(20)
       disable_update_output=ses_lib.run_command_cli(drv_cmd)
       ses_lib.common_check_patern_2(disable_update_output,disable_pattern,"PHY Disabled Update check in Slot",expect=True)

@logThis
def VerifyDrivesTempCheck():
    cmd = 'hdd_temp get' + "\r"
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    output = ses_lib.run_command_cli(cmd)
    output1=output.splitlines()
    pattern="Drive\[(\d+)\].*Temp\: (\d+)\'C"
    for i in output1:
        match=re.search(pattern,i)
        if match:
            Drive_num = match.group(1)
            temperature = match.group(2)
            if int(temperature) >= 0 and int(temperature) < 300:
                log.info("Temperature of the dslot in expected range")
            else:
                log.info("Temperature value not recommended for particular slot")
                raise RuntimeError("Temperature not in expected range")
@logThis
def verifyportmappingtables():
    port_cmd = 'port get' + "\r"
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    drv_cmd = 'drv get' + "\r"
    output = ses_lib.run_command_cli(drv_cmd)
    output1=output.splitlines()
    pattern = "Available"
    slot_num = []
    for i in output1:
     match=re.search(pattern,i)
     if match:
        slot_num.append(i[15:22])
    port=ses_lib.run_command_cli(port_cmd)
    port1=port.splitlines()
    for j in slot_num:
        count = 1
        pattern="{}.*\d+.*SAS.*YES.*\S+.*\d+G0.*".format(j)
        for i in port1:
            match = re.search(pattern,i)
            if match:
                log.info("Pattern match found with expected SAS and speed info")
                count=0
                break
        if count == 1:
            log.info("No Pattern match found with expected SAS and speed info")
            raise RuntimeError("Pattern match failed")

@logThis
def Verifydriveinventorycheck():
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    drv_cmd = 'drv get' + "\r"
    output = ses_lib.run_command_cli(drv_cmd)
    time.sleep(10)
    output1=output.splitlines()
    pattern = "(\d+).*OK.*"
    slot_id=[]
    for i in output1:
      match = re.search(pattern,i)
      if match:
        slot=match.group(1)
        slot_id.append(slot)
    hdds = ses_lib.querySGDevices()
    pattern1 = "status: OK"
    for slot in slot_id:
        cmd = "sg_ses --page=0x02 --index={} {}".format(slot,hdds[0])
        cmd1 = "sg_ses --page=0x02 --index={} {}".format(slot,hdds[1])
        output = ses_lib.run_command(cmd)
        output2 = ses_lib.run_command(cmd1)
        match2=re.search(pattern1,output2)
        match=re.search(pattern1,output)
        if match and match2:
            log.success("Drive status of the page check successful")
        else:
            log.fail("Drive status of the page check  Failed")
            raise RuntimeError("Pattern match failed")

@logThis
def CronusverifyFlagAsValid(cmd,index,HDD):
    cmd1="{}{} {}".format(cmd,index,HDD)
    output=ses_lib.run_command(cmd1)
    index=index.split('-')
    start_index=int(index[0]) + 1
    end_index=int(index[1]) + 2
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    for i in range(start_index,end_index,1):
        if ProductTypeInfo == "SD4100":
           log.info("Inside cronus loop")
           pattern=""".*Element index: {0}  eiioe=1.*
        .*Transport protocol: SAS.*
        .*number of phys: 1, not all phys: 0, device slot number: \d+.*
        .*phy index: 0.*
          .*SAS device type: end device.*
          .*initiator port for:.*
          .*target port for: SSP.*
          .*attached SAS address: \\S+.*
          .*SAS address: \\S+.*
          .*phy identifier: 0x.*"""
        pattern=pattern.format(i)
        log.info(pattern)
        match=re.search(pattern,output)
        if match:
            log.success("Pattern match passed as expected")
        else:
            log.fail("Pattern match failed as expected")
            raise RuntimeError("Pattern match failed")

@logThis
def CronusverifyDescriptorLength(hdd, fru_log):
    log.info("Inside verifyDescriptorLength procedure")
    log.debug(f"hdd      :{hdd}")
    log.debug(f"fru_log  :{fru_log}")
    get_elements_info_cmd = "sg_ses --page=0x07 {}".format(hdd)
    output = ses_lib.run_command(get_elements_info_cmd)
    contents = output.split("Element type:")
    mismatches = []
    elements_dict = {}
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    ProductNameInfo = ses_lib.get_deviceinfo_from_config("UUT","name")
    if ProductTypeInfo == "SD4100":
        descriptor_length_dict = {"Array device slot" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Power supply" : [0x48, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Cooling": [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Temperature sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Enclosure services controller electronics" : [0x50, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Enclosure" : [0x50, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Voltage sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "SAS expander" : [0x20, "Element \d+ descriptor:\s+(.*)\r\n"],
        "SAS connector" : [0x52, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Current sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"]}
    for content in contents:
        for descriptor, checks in descriptor_length_dict.items():
            if descriptor+"," in content:
                elements = re.findall(checks[1], content, re.M)
                if not elements:
                    raise Exception("Didn't find any element of {}".format(descriptor))
                for element in elements:
                    if int(checks[0])!=len(element):
                        error_msg = "{} length is mismatched, expect {},".format(descriptor,
                                hex(checks[0]))
                        error_msg += " current {}:\n***{}***".format(hex(len(element)), element)
                        mismatches.append(error_msg)
                        break
                elements_dict.update({descriptor:elements})
    if mismatches:
        for error_msg in mismatches:
            log.info(error_msg)
        exception_msg = "Element lenghth is mismatched, "
        exception_msg += "total number of mismatched length types: {}".format(len(mismatches))
        raise Exception(exception_msg)
    log.info("element dict is {}".format(elements_dict))
    for descriptor, elements in elements_dict.items():
        log.info("descriptor is {}".format(descriptor))
        log.info("elements is {}".format(elements))
        if descriptor not in ("Power supply",):
            continue
        for element in elements:
            log.info("element is {}".format(element))
            infos = element.strip(" ").split("  ")
            infos = [x.strip() for x in infos]
            infos = list(filter(lambda x:x, infos))
            log.info("Info list is {}".format(infos))
            if not [ x for x in infos[1:] if x != "SD4100"]:
                continue
            if len(infos) < 5 and descriptor in ("Power supply",):
                continue
            if len(infos) < 3 and descriptor in ("Display",):
                continue
            if re.search("Reg",infos[0]):
                continue
            infos = [CommonLib.escapeString(x) for x in infos]
            log.info("Info is {}".format(str(infos)))
            log.info("fru log is {}".format(fru_log))
            if descriptor in ("Power supply",):
                if ProductTypeInfo == "SD4100":
                    pass_pattern = ".*{}.*?\n.*?\n.*?\n.*?{}.*?\n.*?\n.*?{}.*?\n.*?{}".format(
                     infos[1], infos[2], infos[4],infos[3])
                else:
                    pass_pattern = "{}.*?\n.*?{}.*?\n.*?\n.*?\n.*?{}.*?\n.*?\n.*?{}.*?\n.*?{}".format(infos[0],
                    infos[1], infos[2], infos[4],infos[3])
            elif descriptor in ("Display",):
                pass_pattern = infos[2]
            elif descriptor in ("Product Info",):
                if ProductTypeInfo == "SD4100":
                    pass_pattern = ".*{}.*?\n.*?\n.*?\n.*?{}.*?\n.*?\n.*?{}.*?\n.*?{}".format(
                     infos[1], infos[2], infos[4],infos[3])
                    log.info(pass_pattern)
            if not re.search(pass_pattern, fru_log, re.M):
                err_msg = "Didn't find {} in 'fru get' output.".format(element)
                raise Exception(err_msg)

@logThis
def set_voltage_sensor_high_crit(hdd):
  cmd_vol = "sg_ses --page=0x05 --index=vs,11 --set=high_crit=0 {}".format(hdd)
  stats = ses_lib.run_command(cmd_vol)
  if not re.search('rror',stats):
     log.success('Successfully execute set voltage sensor status')
  else:
     raise RuntimeError('Something wrong, the system fail to provide the voltage status')



@logThis
def get_voltage_sensor_threshold(hdd):
  cmd_sen = "sg_ses -p 2 {}".format(hdd)
  threshold_status1 = ses_lib.run_command(cmd_sen)
  if not re.search('rror',threshold_status1):
     log.success('The system successfully gave threshold status')
  else:
     raise RuntimeError('Something wrong, the system fail to provide the threshold status')
  cmd_threshold = "sg_ses -p 5 {}".format(hdd)
  threshold_status2 = ses_lib.run_command(cmd_threshold)
  if not re.search('rror',threshold_status2):
     log.success('The system successfully gave threshold status')
  else:
     raise RuntimeError('Something is wrong when execute get threshold status')
  if all (i in threshold_status1 for i in element_voltage_sensor_status):
     log.success('The elements change to HIGH CRITICAL')
  else:
     raise RuntimeError('Something wrong, fail to change to HIGH CRITICAL')
  if all (i in threshold_status2 for i in element_threshold_status):
     log.success('The elements change to HIGH CRITICAL')
  else:
     raise RuntimeError('Something wrong, fail to change to HIGH CRITICAL')


@logThis
def get_power_and_threshold_status():
  ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
  cmd="power get"
  output1 = ses_lib.run_ESM_command(cmd)
  log.info(output1)
  if not re.search('rror',output1):
     log.success('Successfully get power info status')
  else:
     raise RuntimeError('Something wrong, the system fail to provide the voltage status')
  cmd1="threshold get"
  output2 = ses_lib.run_ESM_command(cmd1)
  log.info(output2)
  if not re.search('rror',output2):
     log.success('Successfully get led info status')
  else:
     raise RuntimeError('Something wrong, the system fail to provide the voltage status')
  if all (i in output1 for i in power):
     log.success('The system succesfully get power sensor info')
  else:
     raise RuntimeError('Something wrong, fail to get power sensor info')
  if all (x in output2 for x in threshold_get_cronus):
     log.success('The system succesfully get threshold info')
  else:
     raise RuntimeError('Something wrong, fail to get threshold info')

@logThis
def set_voltage_sensor_low_crit(hdd):
  cmd = "sg_ses --page=0x05 --index=vs,0 --set=3:7:8=0 {}".format(hdd)
  output = ses_lib.run_command(cmd)
  if not re.search('rror',output):
          log.success('Successfully execute set voltage sensor cmd')
  else:
          raise RuntimeError('Something is wrong when execute set voltage sensor cmd')

@logThis
def get_voltage_sensor_threshold_status(hdd):
  cmd1 = "sg_ses -p 2 {}".format(hdd)
  output1 = ses_lib.run_command(cmd1)
  if not re.search('rror',output1):
          log.success('Successfully execute get voltage sensor status cmd')
  else:
          raise RuntimeError('Something is wrong when execute get voltage sensor status cmd')
  cmd2 = "sg_ses -p 5 {}".format(hdd)
  output2 = ses_lib.run_command(cmd2)
  if not re.search('rror',output2):
          log.success('Successfully execute get threshold cmd')
  else:
          raise RuntimeError('Something is wrong when execute get threshold cmd')
  if all (x in output1 for x in var_voltage_sensor_status):
          log.success('Successfully change to LOW CRITICAL THRESHOLD in voltage sensor status')
  else:
          raise RuntimeError('Something wrong, fail to change to LOW CRITICAL THRESHOLD in voltage sensor status')
  if all (x in output2 for x in var_threshold):
          log.success('Successfully change to LOW CRITICAL THRESHOLD in get threshold cmd')
  else:
          raise RuntimeError('Something wrong, fail to change to LOW CRITICAL THRESHOLD in get threshold cmd')

@logThis
def check_power_and_threshold_status():
  ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
  cmdP = "power get"
  output1 = ses_lib.run_ESM_command(cmdP)
  if not re.search('rror',output1):
          log.success('Successfully execute power get with no error')
  else:
          raise RuntimeError('Something is wrong when execute power get')
  cmdT = "threshold get"
  output2 = ses_lib.run_ESM_command(cmdT)
  if not re.search('rror',output2):
          log.success('Successfully execute threshold get with no error')
  else:
          raise RuntimeError('Something is wrong when execute power get')
  if all (x in output1 for x in var_checkPower):
          log.success('Successfully get power status')
  else:
          raise RuntimeError('Something wrong, fail to get power status')
  if all (x in output2 for x in var_checkthreshold):
          log.success('Successfully get threshold status')
  else:
          raise RuntimeError('Something wrong, fail to get threshold status')

@logThis
def verifySMPCommandsCronus():
  cmd="find /dev/bsg/ -name expander-*"
  pattern="^/dev/bsg/expander.*"
  output = ses_lib.run_command(cmd)
  expanders_list =[]
  output1=output.splitlines()
  for line in output1:
     line =line.strip()
     if re.search(pattern,line):
         log.info(line)
         expanders_list.append(line)
  err_count = 0
  fail_info_list = ['command not found', 'No such file or directory', 'cannot read file', 'Unknown command', 'not found', 'no space left on device', 'Command exited with non-zero status',"ERROR","Failure", "No such file","fail","CLI_UNKNOWN_CMD"]
  cmds_list=['smp_rep_general','smp_rep_manufacturer','smp_read_gpio','smp_rep_self_conf_stat','smp_rep_zone_perm_tbl','smp_rep_broadcast -b 3','smp_discover','smp_rep_phy_err_log -p 3','smp_rep_phy_sata','smp_rep_route_info','smp_rep_phy_event  -p 3','smp_discover_list','smp_rep_phy_event_list','smp_rep_exp_route_tbl','smp_ena_dis_zoning','smp_zone_lock','smp_zone_activate','smp_zone_unlock','smp_conf_zone_man_pass -P 1','smp_phy_control -p 3 -P 15','smp_conf_phy_event -p 3 -C']
  for i in range(0,1):
      for cmd in cmds_list:
         expander_cmd="{} {}".format(cmd,expanders_list[i])
         output = ses_lib.run_command(expander_cmd)
         log.info(output)
         for error in fail_info_list:
            match = re.search(error, output)
            if match:
                log.error("fail to get output, error info:{}".format(error))
                err_count += 1
         if err_count:
            err_count = 0
            raise RuntimeError('{} command execution fail'.format(expander_cmd))
         else:
            log.info("Successfully executed  {} command".format(expander_cmd))

@logThis
def VerifyEnclosureInventorydetailscronus(page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(page_cmd,HDD)
    page_output = ses_lib.run_command(cmd1)
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    pattern1="Element 0 descriptor: Enclosure"
    pattern2="Assembly PN: (\S+)"
    pattern3="Assembly SN: (\S+)"
    pattern4="Assembly Rev: (\S+)"
    cli_output=ses_lib.run_command_cli(CLI_cmd)
    log.info(cli_output)
    match1=re.search(pattern2,cli_output)
    if match1:
        ASM_PN=match1.group(1)
        log.info(ASM_PN)
    match2=re.search(pattern3,cli_output)
    if match2:
        ASM_SN=match2.group(1)
        log.info(ASM_SN)
    match3=re.search(pattern4,cli_output)
    if match3:
        ASM_REV=match3.group(1)
        log.info(ASM_REV)
    pattern_to_check=".*{}.*{}.*{}{}.*N\/A.*N\/A.*".format(pattern1,ASM_PN,ASM_SN,ASM_REV)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,page_output)
    if match:
        log.success("Pattern check got passed as expected")
    else:
        log.fail("Pattern check failed")
        raise RuntimeError("Pattern match failed")

@logThis
def Cronussetthresholdvoltageerror():
    ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "SD4100":
        ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
    ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="power get"
    output = ses_lib.run_ESM_command(cmd)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern=".*Normal.*"
        match=re.search(pattern,line)
        if match:
            if ProductTypeInfo == "SD4100":
                pattern1="^(\S+)\s+(\S+\s+\S+)\s+(\S+)\s+(\S+)V.*"
            match1=re.search(pattern1,line)
            if match1:
                sensor_ID=match1.group(1)
                log.info(sensor_ID)
                sensor_name=match1.group(2)
                log.info(sensor_name)
                sensor_value=match1.group(3)
                log.info(sensor_value)
                read_value=match1.group(4)
                log.info(read_value)
                log.info("%s %s %s %s" %(sensor_ID,sensor_name,sensor_value,read_value))
                actual_value=((float(read_value)-float(sensor_value))/float(sensor_value))*100
                if actual_value < 0:
                    log.info("pass")
                    count+=1
                    break
    if count==0:
        log.info("No Voltage ID available")
        raise RuntimeError("No Voltage ID available")
    clr_cmd="log clear"
    ses_lib.run_ESM_command(clr_cmd)
    cmd1="threshold set {} 0 1 6 5".format(sensor_ID)
    output2=ses_lib.run_ESM_command(cmd1)
    time.sleep(15)
    error_pattern=".*TAMFW_ERR_INVALID_PARAMETERS.*"
    match3=re.search(error_pattern,output2)
    if match3:
        log.info("high_crit_thres must be greater than high_warn_thres and low_crit_thres > low_warn_thres")
    else:
        raise RuntimeError("thrshold value accepted for invalid range")

def set_voltage_sensor_low_warning(hdd):
  cmd_vol = "sg_ses --page=0x05 --index=vs,0 --set=2:7:8=0 {}".format(hdd)
  stats = ses_lib.run_command(cmd_vol)
  if not re.search('rror',stats):
     log.success('Successfully execute set voltage sensor status')
  else:
     raise RuntimeError('Something wrong, the system fail to provide the voltage status')

def get_voltage_sensor_threshold_low_warning(hdd):
  cmd_sen = "sg_ses -p 2 {}".format(hdd)
  threshold_status1 = ses_lib.run_command(cmd_sen)
  if not re.search('rror',threshold_status1):
     log.success('The system successfully gave threshold status')
  else:
     raise RuntimeError('Something wrong, the system fail to provide the threshold status')
  cmd_threshold = "sg_ses -p 5 {}".format(hdd)
  threshold_status2 = ses_lib.run_command(cmd_threshold)
  if not re.search('rror',threshold_status2):
     log.success('The system successfully gave threshold status')
  else:
     raise RuntimeError('Something is wrong when execute get threshold status')
  if all (i in threshold_status1 for i in low_warning_sensor_status):
     log.success('The elements change to LOW WARNING')
  else:
     raise RuntimeError('Something wrong, fail to change to LOW WARNING')
  if all (i in threshold_status2 for i in low_warning_threshold_status):
     log.success('The elements change to LOW WARNING')
  else:
     raise RuntimeError('Something wrong, fail to change to LOW WARNING')

def set_voltage_sensor_high_warning(hdd):
  cmd_vol = "sg_ses --page=0x05 --index=vs,6 --set=1:7:8=0 {}".format(hdd)
  stats = ses_lib.run_command(cmd_vol)
  if not re.search('rror',stats):
     log.success('Successfully execute set voltage sensor status')
  else:
     raise RuntimeError('Something wrong, the system fail to provide the voltage status')

@logThis
def get_voltage_sensor_threshold_high_warning(hdd):
  cmd_sen = "sg_ses -p 2 {}".format(hdd)
  threshold_status1 = ses_lib.run_command(cmd_sen)
  if not re.search('rror',threshold_status1):
     log.success('The system successfully gave threshold status')
  else:
     raise RuntimeError('Something wrong, the system fail to provide the threshold status')
  cmd_threshold = "sg_ses -p 5 {}".format(hdd)
  threshold_status2 = ses_lib.run_command(cmd_threshold)
  if not re.search('rror',threshold_status2):
     log.success('The system successfully gave threshold status')
  else:
     raise RuntimeError('Something is wrong when execute get threshold status')
  if all (i in threshold_status1 for i in high_warning_sensor_status):
     log.success('The elements change to HIGH WARNING')
  else:
     raise RuntimeError('Something wrong, fail to change to HIGH WARNING')
  if all (i in threshold_status2 for i in high_warning_threshold_status):
     log.success('The elements change to HIGH WARNING')
  else:
     raise RuntimeError('Something wrong, fail to change to HIGH WARNING')

@logThis
def verifyDriveDiskPowerOn_OffCronus():
   ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
   if ProductTypeInfo == "SD4100":
       ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
       ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
   ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
   phy_info_cmd="drv get\r"
   disable_cmd="drv set 10 off\r"
   enable_cmd="drv set 10 on\r"
   enable_pattern=".*10.*Slot 11.*OK.*"
   disable_pattern=".*10.*Slot 11.*Not Available.*"
   disable_cmd_pattern="operation done."
   enable_cmd_pattern="operation done."
   output=ses_lib.run_command_cli(phy_info_cmd)
   log.info(output)
   match=re.search(enable_pattern,output)
   if match:
       log.info("Drive ID 10 is enabled.Verify drive off and on function")
       disable_cmd_output=ses_lib.run_command_cli(disable_cmd)
       ses_lib.common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "Drive off Check", expect=True)
       time.sleep(5)
       disable_update_output=ses_lib.run_command_cli(phy_info_cmd)
       ses_lib.common_check_patern_2(disable_update_output,disable_pattern,"Drive off Update check in Slot",expect=True)
       enable_cmd_output=ses_lib.run_command_cli(enable_cmd)
       ses_lib.common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "Drive on Check", expect=True)
       time.sleep(5)
       enable_update_output=ses_lib.run_command_cli(phy_info_cmd)
       ses_lib.common_check_patern_2(enable_update_output,enable_pattern,"Drive on Update check in slot",expect=True)
   else :
       log.info("Drive ID 10 is disabled.Verify drive on and off function")
       enable_cmd_output=ses_lib.run_command_cli(enable_cmd)
       ses_lib.common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "Drive on Check", expect=True)
       time.sleep(5)
       enable_update_output=ses_lib.run_command_cli(phy_info_cmd)
       ses_lib.common_check_patern_2(enable_update_output,enable_pattern,"Drive on Update check in slot",expect=True)
       disable_cmd_output=ses_lib.run_command_cli(disable_cmd)
       ses_lib.common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "Drive off Check", expect=True)
       time.sleep(5)
       disable_update_output=ses_lib.run_command_cli(phy_info_cmd)
       ses_lib.common_check_patern_2(disable_update_output,disable_pattern,"Drive off Update check in Slot",expect=True)

@logThis
def verifyPHYenable_disableCronus():
   ProductTypeInfo = ses_lib.get_deviceinfo_from_config("UUT","platformType")
   if ProductTypeInfo == "SD4100":
       ESMA_IP_1 = ses_lib.get_deviceinfo_from_config("UUT","consoleIP")
       ESMA_port_1 = ses_lib.get_deviceinfo_from_config("UUT","consolePort")
   ses_lib.ESMAConnect(ESMA_IP_1,ESMA_port_1)
   phy_info_cmd="drv get\r"
   disable_cmd="phy disable 10\r"
   enable_cmd="phy enable 10\r"
   enable_pattern=".*10.*Slot 11.*OK.*"
   disable_pattern=".*10.*Slot 11.*Not Available.*"
   disable_cmd_pattern="PHY 10 disabled"
   enable_cmd_pattern="PHY 10 enabled"
   output=ses_lib.run_command_cli(phy_info_cmd)
   match=re.search(enable_pattern,output)
   if match:
       log.info("PHY ID 10 is enabled.Verify disable and enable function")
       disable_cmd_output=ses_lib.run_command_cli(disable_cmd)
       ses_lib.common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       time.sleep(5)
       disable_update_output=ses_lib.run_command_cli(phy_info_cmd)
       ses_lib.common_check_patern_2(disable_update_output,disable_pattern,"PHY Disabled Update check in Slot",expect=True)
       enable_cmd_output=ses_lib.run_command_cli(enable_cmd)
       ses_lib.common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "PHY Enable Check", expect=True)
       time.sleep(5)
       enable_update_output=ses_lib.run_command_cli(phy_info_cmd)
       ses_lib.common_check_patern_2(enable_update_output,enable_pattern,"PHY Enable Update check in slot",expect=True)
   else :
       log.info("PHY ID 10 is disabled.Verify enable and disable function")
       enable_cmd_output=ses_lib.run_command_cli(enable_cmd)
       ses_lib.common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "PHY Enable Check", expect=True)
       time.sleep(5)
       enable_update_output=ses_lib.run_command_cli(phy_info_cmd)
       ses_lib.common_check_patern_2(enable_update_output,enable_pattern,"PHY Enable Update check in slot",expect=True)
       disable_cmd_output=ses_lib.run_command_cli(disable_cmd)
       ses_lib.common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       time.sleep(5)
       disable_update_output=ses_lib.run_command_cli(phy_info_cmd)
       ses_lib.common_check_patern_2(disable_update_output,disable_pattern,"PHY Disabled Update check in Slot",expect=True)

@logThis
def set_verify_altitude_config(username, hostip, password, devicename, expect='c0     20 20 08'):
    """
    verify ses page altitude config page 4 
    :param username
    :param hostip: host ip
    :param password
    :param devicename:sg_ses use devicename to get ses page
    :param expect: altitude value must be st 
    """
    err_count = 0
    cmd1 = 'sg_senddiag -p -r 04,00,00,04,a4,00,00,1e {}'.format(devicename)
    output=ses_lib.get_output_from_ssh_command(username, hostip, password, cmd1)
    cmd2 = 'sg_ses --page=0x04 ' + devicename + ' -H'
    p = 'c0     20 20 08'
    output2 = ses_lib.get_output_from_ssh_command(username, hostip, password, cmd2)
    #err_count = ses_lib.parse_pattern_value(p, output2, expect, err_count)
    ses_lib.common_check_patern_2(output2,p,"altitude verification",expect=True)
    #if err_count:
    #    raise RuntimeError('set_altitude_config fail')
