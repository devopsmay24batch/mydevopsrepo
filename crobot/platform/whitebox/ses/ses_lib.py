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
import difflib
import filecmp
import parser_openbmc_lib
import YamlParse
from SwImage import SwImage
from Server import Server
import random

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/whitebox'))

run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
run_command_cli = partial(CommonLib.run_command, deviceObj=device, prompt='ESM\s\w.*')

def get_deviceinfo_from_config(device, expect):
    """
    :param expect: managementIProot|UserNameroot|Password|bmcIP|bmcPassword|bmcUserName
    """
    deviceInfo = YamlParse.getDeviceInfo()
    deviceDict = deviceInfo[device]
    return deviceDict.get(expect)

ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
if ProductTypeInfo == "TITAN-4U90":
    ESMprompt = get_deviceinfo_from_config("UUT","ESMprompt")
    run_command_cli = partial(CommonLib.run_command, deviceObj=device, prompt=ESMprompt)
if ProductTypeInfo == "SD4100":
        ESMprompt = get_deviceinfo_from_config("UUT","ESMprompt")
        run_command_cli = partial(CommonLib.run_command, deviceObj=device, prompt=ESMprompt)
#some_common_error_patterns = '[\s]*[eE]rror |[\s]*[eE]rror|[\s]*[Ff]ailed |[\s]*[Ff]ailed|[\s]*[Ff]ail |[\s]*[Ff]ail|[\s]*Abnormal|[\s]*[Ii]llegal'
some_common_error_patterns = '[\s]*[eE]rror |[\s]*[eE]rror'


@logThis
def DiagOSConnect(ip, port):
    device.consoleIP = ip
    device.consolePort = port
    device.loginOS()
    return

@logThis
def ServerConnect():
    DeviceMgr.usingSsh = True
    global device
    device = DeviceMgr.getDevice()
    device.connect(device.rootUserName, device.bmcIP)
    device.loginToDiagOS()
    device.readUntil(device.promptDiagOS)
    global run_command
    run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
    return

@logThis
def createSSHSession():
    origin_ssh_flag = DeviceMgr.usingSsh
    DeviceMgr.usingSsh = True
    deviceObj = DeviceMgr.getDevice()
    deviceObj.connect(deviceObj.bmcUserName, deviceObj.bmcIP)
    deviceObj.loginToBMC()
    deviceObj.readUntil(deviceObj.promptDiagOS)
    DeviceMgr.usingSsh = origin_ssh_flag
    return deviceObj

@logThis
def ServerDisconnect():
    global device
    device.disconnect()
    DeviceMgr.usingSsh = False

@logThis
def ConsolePortESMA():
    log.info("Inside ConsolePortESMA procedure")
    DeviceMgr.usingSsh = False
    global device
    device = DeviceMgr.getDevice()
    device.tryLoginESM()

@logThis
def ESMAConnect(ip, port):
    log.info("Inside ESMAConnect procedure")
    DeviceMgr.usingSsh = False
    global device
    device = DeviceMgr.getDevice()
    device.consoleIP = ip
    device.consolePort = port
    device.loginESMA()
    return

@logThis
def ESMBConnect(ip, port):
    device.consoleIP = ip
    device.consolePort = port
    device.loginESMB()
    return

@logThis
def Disconnect():
    device.disconnect()
    return

@logThis
def TelnetESM():
    from TelnetDevice import TelnetDevice
    global telnetObj
    telnetObj = TelnetDevice()
    telnetObj.telnetConnect.open_connection(ESMA_IP, port=ESMA_port)
    return telnetObj

@logThis
def disconnectTelnetObj():
    telnetObj.disconnect()

@logThis
def find_matches(p, output, error_msg=""):
    matches = re.findall(p, output)
    if not error_msg:
        error_msg = "Didn't find any match."
    if not matches:
        raise Exception(error_msg)

    return matches


@logThis
def querySGDevices():
    log.info("Inside querySGDevices procedure")
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90":
        log.debug(f"Platform type :{ProductTypeInfo}")
        p_device = ('(/dev/sg\d+).*?\n.*?CELESTIC  TITAN G2')
    elif ProductTypeInfo == "LENOVO":
        log.debug(f"Platform type :{ProductTypeInfo}")
        p_device = ('(/dev/sg\d+).*?\n.*?CELESTIC  LENOVO')
    elif ProductTypeInfo == "TITAN-4U90":
        log.debug(f"Platform type :{ProductTypeInfo}")
        p_device = ('(/dev/sg\d+).*?\n.*?CELESTIC  TITAN-4U90')
    elif ProductTypeInfo == "CELESTIC  P2523":
        log.debug(f"Platform type :{ProductTypeInfo}")
        p_device = "(/dev/sg\d+).*?\n.*?CELESTIC  P2523"
    elif ProductTypeInfo == "SD4100":
        log.debug(f"Platform type :{ProductTypeInfo}")
        p_device = ('(/dev/sg\d+).?\n.?CELESTIC  SD4100')
    else:
        p_device = "(/dev/sg\d+).*?\n.*?CELESTIC.*"

    output = run_command("sg_scan -ai")
    log.info(output)
    error_msg = "Didn't find available hard disk."
    device_list = find_matches(p_device, output, error_msg)

    return device_list


@logThis
def listArrayDevices(hdd):
    cmd = "sg_ses --page=0x02 {}".format(hdd)
    pattern = "Element\s+(\d+)\s+descriptor:.*?\n.*?status: OK.*?\n.*?\n.*?In crit array=0"
    output = run_command(cmd)
    error_msg = "Didn't find any available array device."
    devices = find_matches(pattern, output, error_msg)
    log.info("Found array devices: {}".format(devices))

    return devices


@logThis
def verifyRQSTFaultBit(hdd, idx):
    OK_1 = { "OK=1" : "OK=1,", "Fault sensed=0" : "Fault sensed=0", "Fault reqstd=0" : "Fault reqstd=0" }
    OK_0 = { "OK=0" : "OK=0," , "Fault sensed=0" : "Fault sensed=0", "Fault reqstd=1" : "Fault reqstd=1" }
    check_ok_cmd = "sg_ses --page=0x02 --index=arr,{} {}".format(idx, hdd)
    output1 = run_command(check_ok_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=OK_1,
            check_output=output1)
    set_RQST_fault_cmd = "sg_ses --page=0x02 --index=arr,{} --set=3:5:1=1 {}".format(idx, hdd)
    run_command(set_RQST_fault_cmd)
    time.sleep(5)
    output2 = run_command(check_ok_cmd)
    clear_RQST_fault_cmd = "sg_ses --page=0x02 --index=arr,{} --set=3:5:1=0 {}".format(idx, hdd)
    run_command(clear_RQST_fault_cmd)
    time.sleep(5)
    output3 = run_command(check_ok_cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=OK_0,
            check_output=output2)
    log.info("Checking after RQST fault is set to 0...")
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=OK_1,
            check_output=output3)


@logThis
def verifyDevicePowerOff(hdd, idx):
    poweron_status = { "0" : "^0$"}
    poweroff_status = { "1" : "^1$"}
    device_poweron_status = { "status: OK" : "Element 1 descriptor:.*?\n.*?status: OK"}
    device_poweroff_status = {
            "status: Not available" : "Element 1 descriptor:.*?\n.*?status: Not available"
            }
    poweroff_disks_cmd = "sg_ses --page=0x02 --index=arr,-1 --set=3:4:1=1 {}".format(hdd)
    get_disk_status_cmd = "sg_ses --page=0x02 --index=arr,{} --get=3:4:1 {}".format(idx, hdd)
    poweron_disks_cmd = "sg_ses --page=0x02 --index=arr,-1 --clear=3:4:1=0  {}".format(hdd)
    get_device_status_cmd = "sg_ses --page=0x02 {}".format(hdd)
    output = run_command(poweroff_disks_cmd)
    time.sleep(5)
    output1 = run_command([get_disk_status_cmd, get_device_status_cmd])
    output1 += output
    output = run_command(poweron_disks_cmd)
    time.sleep(90)
    output2 = run_command([get_disk_status_cmd, get_device_status_cmd])
    output2 += output
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=poweroff_status, check_output=output1)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=device_poweroff_status,
            check_output=output1, line_mode=False)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=poweron_status, check_output=output2)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=device_poweron_status,
            check_output=output2, line_mode=False)


@logThis
def listSensors(sensorType, hdd):
    cmd = "{} {}".format(get_page2_cmd, hdd)
    p_sensor = sensor_pattern_dict.get(sensorType, "Didn't Support Such Sensor Type.")
    output = run_command(cmd)
    error_msg = f"Didn't find any available {sensorType}."
    sensors = find_matches(p_sensor, output, error_msg)
    available_sensors = [sensor for sensor in sensors if float(sensor[1]) != 0]
    log.info("Found sensors: {}".format(available_sensors))

    return available_sensors

@logThis
def listTemperatureSensor(hdd):
    log.info("Inside listTemperatureSensor procedure")
    cmd = "sg_ses --page=0x02 {}".format(hdd)
    p_sensor = "Element\s+(\d+)\s+descriptor.*?\n.*?\n.*?\n.*?\n.*?Temperature=\d{2,}\s+C"
    output = run_command(cmd)
    error_msg = "Didn't find available any temperature sensor."
    sensors = find_matches(p_sensor, output, error_msg)
    log.info("Found sensors: {}".format(sensors))

    return sensors


@logThis
def getSensorTemperature(sensorID, hdd):
    cmd = "sg_ses --page=0x02 --index=ts,{} {}".format(sensorID, hdd)
    p_temper = "Temperature=(\d{2,})\s+C"
    output = run_command(cmd)
    error_msg = "Didn't get temperature value."
    temper = find_matches(p_temper, output, error_msg)

    return temper[0]


@logThis
def getTemperThreshold(sensorID, hdd):
    log.debug('Entering procedure getTemperThreshold with args : %s\n' % (str(locals())))
    log.debug(f"sensorID                        :{sensorID}")
    log.debug(f"hdd inside getTemperThreshold   :{hdd}")
    threshold_pattern_dict = {
            "high critical" : "(\d+),",
            "high warning"  : "(\d+)",
            "low warning"   : "(-?\d+)",
            "low critical"  : "(-?\d+)\s"
            }
    cmd = "sg_ses --page=0x05 --index=ts,{} {}".format(sensorID, hdd)
    output = run_command(cmd)
    threshold_dict = CommonLib.parseDict(output=output,
            pattern_dict=threshold_pattern_dict, sep_field="=")

    return threshold_dict


@logThis
def getSensorThreshold(sensorID, hdd, sensor_type=""):
    voltage_threshold_pattern = {
            "high critical" : "([.0-9]+)",
            "high warning"  : "([.0-9]+)",
            "low warning"   : "([.0-9]+)",
            "low critical"  : "([.0-9]+)"
            }
    temperature_threshold_pattern = {
            "high critical" : "(\d+),",
            "high warning"  : "(\d+)",
            "low warning"   : "(-?\d+)",
            "low critical"  : "(-?\d+)\s"
            }
    Element_type_dict = {
            "Voltage sensor": voltage_threshold_pattern,
            "Temperature sensor": temperature_threshold_pattern,
            }
    threshold_pattern_dict = Element_type_dict.get(sensor_type, {})
    index_abbr = index_abbr_dict.get(sensor_type, "Not Found Index Abbreviation")
    cmd = "sg_ses --page=0x05 --index={},{} {}".format(index_abbr, sensorID, hdd)
    output = run_command(cmd)
    threshold_dict = CommonLib.parseDict(output=output,
            pattern_dict=threshold_pattern_dict, sep_field="=")
    if not all(threshold_dict.values()):
        log.info(f"Got threshold: {threshold_dict}")
        raise Exception("Didn't get all thresholds")

    return threshold_dict


@logThis
def settingThreshold(sensorID, hdd, setting_value, new_threshold, threshold_type,
        sensor_type="Temperature sensor"):
    log.debug("Entering settingThreshold details args : %s" %(str(locals())))
    index_abbr = index_abbr_dict[sensor_type]
    cmd = "sg_ses --page=0x05 --index={},{} --set={}={} {}".format(index_abbr,
            sensorID, threshold_type_dict[threshold_type], new_threshold, hdd)
    output = run_command(cmd)
    time.sleep(setting_threshold_waiting)
    time.sleep(15)
    get_threshold_cmd = f"sg_ses --page=0x05 --index={index_abbr},{sensorID} {hdd}"
    output1 = run_command(get_threshold_cmd)
    pass_pattern = "{}={}".format(threshold_type, setting_value)
    if not re.search(pass_pattern, output1):
        raise Exception("Expect threshold: {}".format(pass_pattern))
    output += output1
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)


@logThis
def setTemperThreshold(sensorID, hdd, temper_value, threshold_type):
    log.debug("Entering setTemperThreshold details args : %s" %(str(locals())))
    setting_value = temper_value
    sensor_type = "Temperature sensor"
    if threshold_type in("low critical", "low warning"):
        setting_value = int(temper_value) + 5
    else:
        setting_value = int(temper_value) - 5
    new_threshold = setting_value + 20

    settingThreshold(sensorID, hdd, setting_value, new_threshold, threshold_type, sensor_type)
    return new_threshold


@logThis
def setVoltageThreshold(sensorID, hdd, threshold_dict, threshold_type):
    setting_value = threshold_dict[threshold_type]
    sensor_type = "Voltage sensor"
    if threshold_type in("low critical", "low warning"):
        setting_value = int(float(setting_value)) + 4
    else:
        setting_value = int(float(setting_value)) - 4
    new_threshold = setting_value * 2

    settingThreshold(sensorID, hdd, setting_value, new_threshold, threshold_type, sensor_type)
    return new_threshold


@logThis
def setBackThreshold(sensorID, hdd, threshold_dict, threshold_type,
        sensor_type="Temperature sensor"):
    log.debug('Entering procedure setBackThreshold with args : %s\n' % (str(locals())))

    setting_value = threshold_dict[threshold_type]
    if sensor_type == "Temperature sensor":
        new_threshold = int(setting_value) + 20
    elif sensor_type in ("Voltage sensor",):
        new_threshold = int(float(setting_value))*2

    settingThreshold(sensorID, hdd, setting_value, new_threshold, threshold_type, sensor_type)
    return new_threshold


@logThis
def queryAlarmBit(sensorID, hdd, pattern_dict):
    log.debug('Entering procedure queryAlarmBit with args : %s\n' % (str(locals())))
    cmd = "sg_ses --page=0x02 --index=ts,{} {}".format(sensorID, hdd)
    output = run_command(cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=pattern_dict,
            check_output=output, line_mode=False)


@logThis
def queryDeviceAlarmBit(hdd, pattern_dict):
    cmd = "sg_ses --page=0x02 {}".format(hdd)
    output = run_command(cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=pattern_dict,
            check_output=output, line_mode=False)


@logThis
def checkAlarmBit(sensorID, hdd, threshold_type):
    low_critical = {
            "UT failure=1"     : "UT failure=1",
            "status: Critical" : "status: Critical"
            }
    low_warning = {
            "UT warning=1"     : "UT warning=1",
            "status: Noncritical" : "status: Noncritical"
            }
    high_critical = {
            "OT failure=1"     : "OT failure=1",
            "status: Critical" : "status: Critical"
            }
    high_warning = {
            "OT warning=1"     : "OT warning=1",
            "status: Noncritical" : "status: Noncritical"
            }
    check_dict = {
            "low critical"  : low_critical,
            "low warning"   : low_warning,
            "high critical" : high_critical,
            "high warning"  : high_warning
            }
    index_alarm_check_dict = check_dict[threshold_type]
    queryAlarmBit(sensorID, hdd, index_alarm_check_dict)

    device_alarm = {
            "low critical"  : {"CRIT=1" : "Enclosure Status diagnostic page.*?\n.*?\sCRIT=1"},
            "low warning"   : {"NON-CRIT=1" : "Enclosure Status diagnostic page.*?\n.*?\sNON-CRIT=1"},
            "high critical" : {"CRIT=1" : "Enclosure Status diagnostic page.*?\n.*?\sCRIT=1"},
            "high warning"  : {"NON-CRIT=1" : "Enclosure Status diagnostic page.*?\n.*?\sNON-CRIT=1"}
            }
    device_check_dict = device_alarm[threshold_type]
    queryDeviceAlarmBit(hdd, device_check_dict)


@logThis
def checkAlarmNormal(sensorID, hdd, threshold_type):
    log.info("Inside checkAlarmNormal procedure details args : %s" %(str(locals())))
    low_critical = {
            "UT failure=0" : "UT failure=0",
            "status: OK"   : "status: OK",
            }
    low_warning = {
            "UT warning=0" : "UT warning=0",
            "status: OK"   : "status: OK",
            }
    high_critical = {
            "OT failure=0" : "OT failure=0",
            "status: OK"   : "status: OK",
            }
    high_warning = {
            "OT warning=0" : "OT warning=0",
            "status: OK"   : "status: OK",
            }
    check_dict = {
            "low critical"  : low_critical,
            "low warning"   : low_warning,
            "high critical" : high_critical,
            "high warning"  : high_warning
            }
    pattern_dict = check_dict[threshold_type]
    time.sleep(10)
    queryAlarmBit(sensorID, hdd, pattern_dict)


@logThis
def clearAlarmBit(hdd, alarm_level):
    cmd = "sg_ses --page=0x02 --index=ts,0 --set=1:1:1=0 --byte1=0x00 {}".format(hdd)
    critical_bit = {
            "CRIT=0" : "Enclosure Status diagnostic page.*?\n.*?\sCRIT=0"
            }
    warning_bit = {
            "NON-CRIT=0" : "Enclosure Status diagnostic page.*?\n.*?\sNON-CRIT=0"
            }
    device_alarm = {
            "low critical"  : critical_bit,
            "low warning"   : warning_bit,
            "high critical" : critical_bit,
            "high warning"  : warning_bit
            }

    output = run_command(cmd)
    log.info(output)
    time.sleep(10)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)
    device_check_dict = device_alarm[alarm_level]
    queryDeviceAlarmBit(hdd, device_check_dict)


@logThis
def checkSensorValueOnPage5(sensor, hdd, alarm_level, checking_value,
        sensor_type="Temperature sensor"):
    index_abbr = index_abbr_dict[sensor_type]
    cmd = "sg_ses --page=0x05 --index={},{} --get={} {}".format(
            index_abbr, sensor,
            threshold_type_dict[alarm_level], hdd)
    pattern = f"^{checking_value}\s*$"
    output = run_command(cmd)
    match = re.search(pattern, output, re.M)
    if not match:
        raise Exception(f"Expect value: {checking_value}")


@logThis
def verifyDescriptorLength(hdd, fru_log):
    log.info("Inside verifyDescriptorLength procedure")
    log.debug(f"hdd      :{hdd}")
    log.debug(f"fru_log  :{fru_log}")
    get_elements_info_cmd = "sg_ses --page=0x07 {}".format(hdd)
    output = run_command(get_elements_info_cmd)
    contents = output.split("Element type:")
    mismatches = []
    elements_dict = {}
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90" or ProductTypeInfo == "SD4100":
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
    for descriptor, elements in elements_dict.items():
        if descriptor not in ("Power supply",):
            continue
        for element in elements:
            log.info(element)
            infos = element.strip(" ").split("  ")
            infos = [x.strip() for x in infos]
            infos = list(filter(lambda x:x, infos))
            if not [ x for x in infos[1:] if x != "N/A"]:
                continue
            if len(infos) < 5 and descriptor in ("Power supply",):
                continue
            if len(infos) < 3 and descriptor in ("Display",):
                continue
            if re.search("Reg",infos[0]):
                continue
            infos = [CommonLib.escapeString(x) for x in infos]
            log.info(str(infos))
            log.info(fru_log)
            if descriptor in ("Power supply",):
                if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
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
            if not re.search(pass_pattern, fru_log, re.M):
                err_msg = "Didn't find {} in 'fru get' output.".format(element)
                raise Exception(err_msg)

@logThis
def verifyDiskInfo(hdd):
    get_disk_info_cmd = f"sg_ses --page=0x0a {hdd}"
    output = run_command(get_disk_info_cmd)
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "Nebula_Gen2F":
        log.debug(f"Platform type :{ProductTypeInfo}")
        array_info_p = "(Element type: Array device slot.*)"
        element_p = "(Element index:.*?)(?=Element index:|Element type:|eiioe=)"
        check_dict = {
            "Transport protocol: SAS" : "Transport protocol:\s+SAS",
            "number of phys: 1"       : "number of phys:\s+1,",
            "not all phys: 0"         : "not all phys:\s+0,",
            "device slot number is mismatched" :
                r"Element index:\s+(\d+).*?device slot number:\s+\1",
            "SAS device type: end device|no SAS device attached" :
                "SAS device type:\s+(no SAS device attached|end device)",
            "target port for: SSP|SATA_device" : "target port for: (SSP|SATA_device)",
            "attached SAS address:" : "attached SAS address:\s+\S+",
            "SAS address:" : "SAS address:\s+\S+",
            }
    elif ProductTypeInfo == "CELESTIC  P2523":
        log.debug(f"Platform type :{ProductTypeInfo}")
        array_info_p = "(Element type: Array device slot.*)"
        element_p = "(Element index:.*?)(?=Element index:.*eiioe=)"
        check_dict = {
            "Transport protocol: PCIe" : "Transport protocol:\s+PCIe",
            "PCIe protocol type: NVMe" : "PCIe protocol type:\sNVMe",
            "number of ports: (\d+), not all ports: (\d+), device slot number: (\d+)" :"number of ports: (\d+), not all ports: (\d+), device slot number: (\d+)",
            "PCIe vendor id: (\S+)" : "PCIe vendor id: (\S+)",
            "serial number: (\S+)" : "serial number: (\S+)",
            "model number: (\S+)" : "model number: (\S+)",
            "port index: (\d+)" : "port index: (\d+)",
            "PSN_VALID=(\d+), BDF_VALID=(\d+), CID_VALID=(\d+)" : "PSN_VALID=(\d+), BDF_VALID=(\d+), CID_VALID=(\d+)",
            }
    else:
        array_info_p = "(Element type: Array device slot.*?Element type:)"    
        element_p = "(Element index:.*?)(?=Element index:|Element type:|eiioe=)"
        check_dict = {
            "Transport protocol: SAS" : "Transport protocol:\s+SAS",
            "number of phys: 1"       : "number of phys:\s+1,",
            "not all phys: 0"         : "not all phys:\s+0,",
            "device slot number is mismatched" :
                r"Element index:\s+(\d+).*?device slot number:\s+\1",
            "SAS device type: end device|no SAS device attached" :
                "SAS device type:\s+(no SAS device attached|end device)",
            "target port for: SSP|SATA_device" : "target port for: (SSP|SATA_device)",
            "attached SAS address:" : "attached SAS address:\s+\S+",
            "SAS address:" : "SAS address:\s+\S+",
            }
    match_array_info = re.search(array_info_p, output, re.S)
    if not match_array_info:
        raise Exception("Didn't find Array device information.")
    else:
        log.info("match_array_info created")
    elements = re.findall(element_p, match_array_info.group(1), re.S|re.M)
    if not elements:
        raise Exception("Didn't find elements of Array.")
    available_num = 0
    element_index_p = "Element index:\s+(\d+)"
    for element in elements:
        log.info(element)
        pattern = ".*flagged as invalid.*"
        match= re.search(pattern,element)
        if match:
            log.info("Array Device info is empty")
            continue
        log.info("valid array device slot")
        available_num += 1
        match_element_index = re.search(element_index_p, element)
        if match_element_index:
            log.info("Checking element index: {}".format(match_element_index.group(1)))
            CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=check_dict,
                    check_output=element, line_mode=False)
    log.info(f"{available_num} installed disks have been checked.")


@logThis
def downloadSesFwImage(module="SES", upgrade=True):
    CommonLib.download_image(Const.SSH_DUT, module, upgrade=upgrade)

@logThis
def downloadCpldFwImage(module="CPLD", upgrade=True):
    CommonLib.download_image(Const.SSH_DUT, module, upgrade=upgrade)

@logThis
def updateSesFw(hdd, upgrade=True, image_file=None, tool=download_microcode_mode7_3k_cmd):
    log.debug("Entering updateSesFw procedure with args : %s" %(str(locals())))
    if image_file==None:
        if upgrade:
            image_file = CommonLib.get_swinfo_dict("SES").get("newImage", "NotFound")
        else:
            image_file = CommonLib.get_swinfo_dict("SES").get("oldImage", "NotFound")
    local_path = CommonLib.get_swinfo_dict("SES").get("localImageDir", "NotFound")
    upgrade_cmd = "{} -I {}{} {}".format(tool, local_path,image_file, hdd)
    upgrade_cmd = upgrade_cmd + '\r'
    output = run_command(upgrade_cmd, prompt='root@localhost', timeout=1500)
    time.sleep(100)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)

@logThis
def verifyESMSesFwVersion(upgrade=True):
    if upgrade:
        version="newVersion"
    else:
        version="oldVersion"
    version =  CommonLib.get_swinfo_dict("SES").get(version, "NotFound")
    fw_version = "FW Revision(\W)? {}".format(".".join(version.split(".")[:-1]))
    fw_version_sec1 = "FW Revision.+Sec 1.+{}".format(version)
    fw_version_sec2 = "FW Revision.+Sec 2.+{}".format(version)
    output = run_ESM_command("fru get")
    check_dict = {
            fw_version : CommonLib.escapeString(fw_version),
            fw_version_sec1 : CommonLib.escapeString(fw_version_sec1),
            fw_version_sec2 : CommonLib.escapeString(fw_version_sec2)
            }
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=check_dict,
            check_output=output)

@logThis
def checkPage7FwVersion(hdd, upgrade=True):
    if upgrade:
        version="newVersion"
    else:
        version="oldVersion"
    version =  CommonLib.get_swinfo_dict("SES").get(version, "NotFound")
    version_list = version.split(".")
    if len(version_list) != 4:
        raise Exception("Didn't get correct SES FW version format.")
    version_list = map(int, version_list)
    version_format = "{0:0>2d}{1:0>2d}{2:0>2d}{3:0>2d}".format(*version_list)
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        log.debug(f"Product Type 11111:{ProductTypeInfo}")
        esm = "ESM (A|B)"
    else:
        esm = "ESM(A|B)"
    primary_v = "Primary\s+B0\s+{}".format(version_format)
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        log.debug(f"Product Type 22222:{ProductTypeInfo}")
        SecondaryB0_1= "1 SecondarB0\s+{}".format(version_format)
        SecondaryB0_2= "2 SecondarB0\s+{}".format(version_format)
    else:
        SecondaryB0_1= "1 SecondaryB0\s+{}".format(version_format)
        SecondaryB0_2= "2 SecondaryB0\s+{}".format(version_format)
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        log.debug(f"Product Type 33333:{ProductTypeInfo}")
        check_dict = {
            esm + f" Primary   B0  {version_format}"      : esm + "\s+" + primary_v,
            esm + f" 1 SecondarB0  {version_format}"      : esm + "\s+" + SecondaryB0_1,
            esm + f" 2 SecondarB0  {version_format}"      : esm + "\s+" + SecondaryB0_2
            }
    else:
        check_dict = {
            esm + f" Primary B0   {version_format}"        : esm + "\s+" + primary_v,
            esm + f" 1 SecondaryB0  {version_format}"      : esm + "\s+" + SecondaryB0_1,
            esm + f" 2 SecondaryB0  {version_format}"      : esm + "\s+" + SecondaryB0_2
            }
    cmd = f"sg_ses --page=0x7 {hdd}"
    runAndCheck(cmd, checking=check_dict)

@logThis
def checkPage2Page10FwVersion(hdd, upgrade=True):
    if upgrade:
        version="newVersion"
    else:
        version="oldVersion"
    page2_cmd = f"sg_ses --page=0x2 {hdd}"
    page10_cmd = f"sg_ses --page=0xa {hdd}"
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    version =  CommonLib.get_swinfo_dict("SES").get(version, "NotFound")
    if ProductTypeInfo == "Nebula_Gen2F":
        version_list = map(int, version[1].split("."))
    else:
        version_list = map(int, version.split("."))
    version_format = "{0:0>2d}{1}{2}".format(*version_list)
    if ProductNameInfo == "Titan_G2_Lenovo":
        log.debug(f"Product Name :{ProductNameInfo}")
        if upgrade == True:
            version_format = 'C' + version_format[1:]
        else:
            version_format = 'CI' + version_format[2:]
            #version_format = version_format[:0] + 'CI' + version_format[0+1:]
    if ProductTypeInfo == "LENOVO":
        log.debug(f"Product Type :{ProductTypeInfo}")
        check_dict = { f"CELESTIC  LENOVO...  {version_format}" : f"CELESTIC  LENOVO.*?{version_format}" }
    elif ProductTypeInfo == "Nebula_Gen2F":
        log.debug(f"Product Type :{ProductTypeInfo}")
        check_dict = { f"CELESTIC  Nebula_Gen2F...  {version_format}" : f"CELESTIC  Nebula_Gen2F.*?{version_format}" }
    else:
        check_dict = { f"CELESTIC  TITAN...  {version_format}" : f"CELESTIC  TITAN.*?{version_format}" }
    runAndCheck(page2_cmd, checking=check_dict)
    runAndCheck(page10_cmd, checking=check_dict)

@logThis
def checkDiskAmount(HDDs):
    hdds_sg_scan = querySGDevices()
    if len(hdds_sg_scan) != len(HDDs):
        err_msg = "sg_scan -ai => "
        err_msg += f"Disk amount is mismatched, current: {hdds_sg_scan}, original: {HDDs}"
        raise Exception(err_msg)

    lsscsi_pattern = "CELESTIC.*?(/dev/sg\d+)"
    lsscsi_cmd = "lsscsi -g"
    output = run_command(lsscsi_cmd)
    hdds_lsscsi = re.findall(lsscsi_pattern, output)
    if len(hdds_lsscsi) != len(HDDs):
        err_msg = f"{lsscsi_cmd} => "
        err_msg += f"Disk amount is mismatched, current: {hdds_lsscsi}, original: {HDDs}"
        raise Exception(err_msg)


@logThis
def resetAllExpanders(HDDs, reset_cmd=reset_expander_00_cmd):
    log.debug("Entering resetAllExpanders details args : %s" %(str(locals())))
    output = ""
    for HDD in HDDs:
        cmd = "{} {}".format(reset_cmd, HDD)
        runAndCheck(cmd, checking=fail_dict, is_negative=True)
    #    break #reset one disk will reset all others on the same canister
    time.sleep(HDD_RESET_TIME)

@logThis
def checkSbbStatus(HDDs):
    log.debug("Entering checkSbbStatus details args : %s" %(str(locals())))
    for HDD in HDDs:
        cmd = "{} {}".format(check_sbb_cmd, HDD)
        ProductNameInfo = get_deviceinfo_from_config("UUT","name")
        if ProductNameInfo == "Titan_G2_Lenovo" or  ProductNameInfo == "Titan_G2_WB":
            log.debug(f"Product Name :{ProductNameInfo}")
            cmd = "{} {}".format(check_sbb_cmd, HDD)
            runAndCheck(cmd, checking=check_sbb_result_lenovo)
        else:
            cmd = "{} {}".format(check_sbb_cmd, HDD)
            runAndCheck(cmd, checking=check_sbb_result)

@logThis
def checkDevicesElementsOnPage2(HDDs, check_elements=None):
    log.debug("Entering checkDevicesElementsOnPage2 details args : %s" %(str(locals())))
    devices_dict = {}
    for HDD in HDDs:
        elements_status = checkElementsOnPage2(HDD)
        devices_dict[HDD] = elements_status
    if not check_elements:
        return devices_dict
    else:
        for hdd, elements_status in devices_dict.items():
            if elements_status not in check_elements.values():
                device_num = len(check_elements)
                count = 0
                for element_type, descriptor_status in elements_status.items():
                    for cmp_element in check_elements.values():
                        count += 1
                        if descriptor_status != cmp_element[element_type] \
                            and count == device_num:
                            err_msg = f"{element_type} status is changed."
                            raise Exception(err_msg)

@logThis
def checkElementsOnPage2(hdd):
    get_elements_info_cmd = "sg_ses -p 2 {}".format(hdd)
    output = run_command(get_elements_info_cmd)
    contents = output.split("Element type:")
    mismatches = []
    elements_dict = {}
    for content in contents:
        for descriptor, checks in elements_status_dict.items():
            if descriptor+"," in content:
                elements = re.findall(checks, content)
                if not elements:
                    mismatches.append(descriptor)
                    raise Exception("Didn't find normal element of {}".format(descriptor))
                elements_dict.update({descriptor : elements})
    return elements_dict

@logThis
def savePage7AndPageAInfo(HDDs):
    page_info = {"page7" : {}, "pageA" : {}}
    for HDD in HDDs:
        page7_cmd = "{} {}".format(get_page7_cmd, HDD)
        pageA_cmd = "{} {}".format(get_pageA_cmd, HDD)
        page7_output = runAndCheck(page7_cmd, checking=fail_dict, is_negative=True, timeout=300)
        pageA_output = runAndCheck(pageA_cmd, checking=fail_dict, is_negative=True, timeout=300)
        page_info["page7"].update({ HDD : page7_output })
        page_info["pageA"].update({ HDD : pageA_output})

    return page_info

@logThis
def comparePage7AndPageAInfo(HDDs, page_info=None):
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "CELESTIC  P2523":
        log.debug(f"Platform type :{ProductTypeInfo}")
        page_info_current = savePage7AndPageAInfoAthena(HDDs)
    else:
        page_info_current = savePage7AndPageAInfo(HDDs)    
    for page, item in page_info_current.items():
        if len(item) != len(page_info[page]):
            err_msg = "{} disk number mismatch: previous: {},".format(page,
                    len(page_info[page]))
            err_msg += " current: {}".format(len(item))
            raise Exception(err_msg)
        for disk, info in item.items():
            values = page_info[page].values()
            info_list = info.splitlines()[2:-2]
            values_list = [x.splitlines()[2:-2] for x in values]
            if info_list not in values_list:
                for i in range(len(info_list)-4):
                    cmp_list = [x[i] for x in values_list]
                    if info_list[i] not in cmp_list:
                        log.info(f"info: {info_list[i]}")
                        log.info(json.dumps(cmp_list))
                        err_msg = "{} {} infomation mismatch than previous.".format(page, disk)
                        raise Exception(err_msg)


@logThis
def savePage7Info(HDDs):
    page_info = {"page7" : {}}
    for HDD in HDDs:
        page7_cmd = "{} {}".format(get_page7_cmd, HDD)
        page7_output = runAndCheck(page7_cmd, checking=fail_dict, is_negative=True, timeout=300)
        page_info["page7"].update({ HDD : page7_output })
    return page_info

@logThis
def comparePage7Info(HDDs, page_info=None):
    page_info_current = savePage7Info(HDDs)
    for page, item in page_info_current.items():
        if len(item) != len(page_info[page]):
            err_msg = "{} disk number mismatch: previous: {},".format(page,
                    len(page_info[page]))
            err_msg += " current: {}".format(len(item))
            raise Exception(err_msg)
        for disk, info in item.items():
            values = page_info[page].values()
            info_list = info.splitlines()[2:-2]
            values_list = [x.splitlines()[2:-2] for x in values]
            if info_list not in values_list:
                for i in range(len(info_list)-4):
                    cmp_list = [x[i] for x in values_list]
                    if info_list[i] not in cmp_list:
                        log.info(f"info: {info_list[i]}")
                        log.info(json.dumps(cmp_list))
                        err_msg = "{} {} infomation mismatch than previous.".format(page, disk)
                        raise Exception(err_msg)

@logThis
def verifyCLILog():
    cmd = "log get"
    prompt="ESM \w \$"
    telnetObj.sendMsg(cmd + "\n")
    expect_str = f"{cmd}[\s\S]+{prompt}"
    output = telnetObj.read_until_regexp(expect_str)
    disconnectTelnetObj()
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)

@logThis
def verifyCLILog_Athena():
    cmd = "log get"
    CommonLib.send_command("$%^0\r",promptStr=None)
    output = run_ESM_command(cmd)
    log.info(output)
    CommonLib.send_command("$%^3\r",promptStr=None)
    return output

def verifyCLIResetInfoESM():
    log.info("Inside verifyCLIResetInfo procedure")
    cmd = "log get\r"
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "TITAN-4U90":
        log.debug(f"Platform type :{ProductTypeInfo}")
        prompt="ESM\s\S\s.*=\> "
    elif ProductTypeInfo == "LENOVO":
        log.debug(f"Platform type :{ProductTypeInfo}")
        prompt="ESM\s\w\s.*#"
    else:
        prompt="ESM \w \$"
    output = run_ESM_command(cmd)
    p = 'Hard Reset'
    expect_str = f"{cmd}[\s\S]+{prompt}"
    common_check_patern_2(output, p, 'reset_esm')
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)

def verifyCLIResetInfo():
    log.info("Inside verifyCLIResetInfo procedure")
    cmd = "log get\r"
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90":
        log.debug(f"Platform type :{ProductTypeInfo}")
        prompt="ESM\s\S\s.*=\> "
    elif ProductTypeInfo == "LENOVO":
        log.debug(f"Platform type :{ProductTypeInfo}")
        prompt="ESM\s\w\s.*#"
    else:
        prompt="ESM \w \$"
    telnetObj.sendMsg(cmd + "\n")
    p = 'Hard Reset'
    expect_str = f"{cmd}[\s\S]+{prompt}"
    output = telnetObj.read_until_regexp(expect_str)
    disconnectTelnetObj()
    common_check_patern_2(output, p, 'reset_esm')
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)

@logThis
def downloadMicrocode(image="FAULT_IMAGE", cmd=None, HDD=None):
    image_dict = CommonLib.get_swinfo_dict(image)
    imageName = image_dict.get("newImage", "NotFound")
    local_dir = image_dict.get("localImageDir", "NotFound")
    change_dir_cmd = f"cd {local_dir}"
    download_cmd = f"{cmd} -I {imageName} {HDD}"
    log.info(download_cmd)
    output = run_command([change_dir_cmd, download_cmd], timeout=180)
    check_pattern = "sg_ses_microcode failed: Aborted command"
    if not re.search(check_pattern, output) and image != "FAULT_IMAGE":
        raise Exception("Verify with fault image failed.")

@logThis
def downloadMicrocodeAthena(image,imageName,cmd,HDD):
    image_dict = CommonLib.get_swinfo_dict(image)
    local_dir = image_dict.get("localImageDir", "NotFound")
    change_dir_cmd = f"cd {local_dir}"
    download_cmd = f"{cmd} -I {imageName} {HDD}"
    log.info(download_cmd)
    output = run_command([change_dir_cmd, download_cmd], timeout=180)
    check_pattern = "sg_ses_mocrocode failed: Illegal request"
    if not re.search(check_pattern, output):
        raise Exception("Verify with fault image failed.")
    
@logThis
def sendDownloadMicrocode(cmd=None, HDD=None):
    image_dict = CommonLib.get_swinfo_dict("SES")
    imageName = image_dict.get("newImage", "NotFound")
    local_dir = image_dict.get("localImageDir", "NotFound")
    change_dir_cmd = f"cd {local_dir}"
    download_cmd = f"{cmd} -I {imageName} {HDD}\n"
    output = run_command(change_dir_cmd)
    device.sendMsg(download_cmd)
    output = device.readMsg()
    log.info(download_cmd)


@logThis
def clearLogs():
    ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
    ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    output = run_ESM_command("log clear")
    Disconnect()
    time.sleep(20)
    ESMB_IP_1 = get_deviceinfo_from_config("UUT","esmbConsoleIP")
    ESMB_port_1 = get_deviceinfo_from_config("UUT","esmbConsolePort")
    ESMBConnect(ESMB_IP_1,ESMB_port_1)
    output = run_ESM_command("log clear")
    Disconnect()
    time.sleep(20)


@logThis
def getESMVersionAndCheck(cmd="about", cmp_dict=None, version_pattern=None):
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
        ESMAConnect(ESMA_IP_1,ESMA_port_1)
        output = run_ESM_command(cmd)
        Disconnect()
    elif ProductTypeInfo == "CELESTIC  P2523":
        log.debug(f"Platform type :{ProductTypeInfo}")
        CommonLib.send_command("$%^0\r",promptStr=None)
        output = run_ESM_command(cmd)
        CommonLib.send_command("$%^3\r",promptStr=None)
    else:
        output = run_command_cli(cmd, deviceObj=telnetObj)
    current_version = CommonLib.parseDict(output=output,
            pattern_dict=version_pattern, sep_field=" ")
    if not cmp_dict:
        return current_version
    if not current_version:
        err_msg = f"Didn't get version info."
        raise Exception(err_msg)
    if current_version != cmp_dict:
        err_msg = f"Version is changed, expect: {cmp_dict}"
        raise Exception(err_msg)


@logThis
def checkESMUpdatedVersion(cmd="about", upgrade=True):
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
        ESMAConnect(ESMA_IP_1,ESMA_port_1)
        output = run_ESM_command(cmd)
        Disconnect()
    else:
        output = run_command_cli(cmd, deviceObj=telnetObj)
    if upgrade:
        version = CommonLib.get_swinfo_dict("SES").get("newVersion", "NotFound")
    else:
        version = CommonLib.get_swinfo_dict("SES").get("oldVersion", "NotFound")

    if version == "NotFound":
        err_msg = f"Didn't get version info in configuration."
        raise Exception(err_msg)
    main_version = "\.".join(version.strip().split(".")[:3])
    if not re.search(main_version, output):
        main_version = main_version.replace("\.", ".")
        err_msg = f"Expected verion: {main_version}"
        raise Exception(err_msg)

@logThis
def checkESMStatus(cmd="about"):
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN-4U90":
       output=run_ESM_command(cmd)
       current_version = getFWVersion("DUT")
    else:
       output = run_command_cli(cmd, deviceObj=telnetObj)
       current_version = CommonLib.parseDict(output=output,pattern_dict=esm_fw_version_pattern, sep_field=" ")
    if not current_version:
        err_msg = f"ESM status is abnormal."
        raise Exception(err_msg)


@logThis
def activeFW(HDD):
    cmd = "{} {}".format(fw_active_cmd, HDD)
    runAndCheck(cmd, checking=fail_dict, is_negative=True,timeout=240)
    time.sleep(HDD_RESET_TIME)

@logThis
def checkCLILog(timeout=60):
    cmd = "about"
    runAndCheckCLI(cmd, checking=fail_dict,
            is_negative=True, timeout=timeout)

@logThis
def checkInNewSSHSession(cmd, checking={},is_negative=False,
        timeout=180, prompt_cnt=1):
    device_new = createSSHSession()
    runAndCheck(cmd, checking={}, is_negative=False, timeout=180,
            prompt_cnt=1, device=device_new)


@logThis
def checkValuesLength(expect_length_dict=None, target_dict=None):
    for key, length in expect_length_dict.items():
        cur_length = len(target_dict[key])
        if cur_length > length:
            raise Exception(f"Expect {key}'s length: {length}, current length: {cur_length}")

@logThis
def checkReturnData(hdd, query_cmd=sg_inquiry_cmd, query_pattern=sq_inquiry_pattern,
        length_dict=sq_inquiry_length):
    cmd = "{} {}".format(query_cmd, hdd)
    output = run_command(cmd)
    sg_inqiry_data = CommonLib.parseDict(output=output, pattern_dict=query_pattern)
    checkValuesLength(expect_length_dict=length_dict, target_dict=sg_inqiry_data)


@logThis
def runAndCheck(cmd, checking={}, is_negative=False, timeout=180,
        prompt_cnt=1, device=device):
    log.debug("Entering runAndCheck details args : %s" %(str(locals())))
    prompt = device.promptDiagOS
    if prompt_cnt>1:
        prompt = f"{prompt}[\s\S]+"*prompt_cnt
    output = run_command(cmd, timeout=timeout, prompt=prompt)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=checking,
             check_output=output, is_negative_test=is_negative)
    return output

@logThis
def runAndCheckESMCLI(cmd, checking={}, is_negative=False, timeout=60):
    output = run_ESM_command(cmd)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=checking,
             check_output=output, is_negative_test=is_negative)
    return output

@logThis
def runAndCheckCLI(cmd, checking={}, is_negative=False, timeout=60):
    output = run_command_cli(cmd, deviceObj=telnetObj, timeout=timeout)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=checking,
             check_output=output, is_negative_test=is_negative)
    return output


@logThis
def run_ESM_command(cmd):
    log.info("Inside run_ESM_command procedure")
    cmd= cmd + '\r'
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90":
        log.debug(f"Platform type :{ProductTypeInfo}")
        output = run_command_cli(cmd, prompt='ESM\s\S\s=\>')
    elif ProductTypeInfo == "LENOVO":
        log.debug(f"Platform type :{ProductTypeInfo}")
        output = run_command_cli(cmd, prompt='ESM\s\w\s.*#')
    elif ProductTypeInfo == "Nebula_Gen2F":
        log.debug(f"Platform type :{ProductTypeInfo}")
        output = run_command_cli(cmd, prompt='0x00000000:.*>')
    elif ProductTypeInfo == "TITAN-4U90":
        log.debug(f"Platform type :{ProductTypeInfo}")
        ESMprompt = get_deviceinfo_from_config("UUT","ESMprompt")
        output = run_command_cli(cmd, prompt=ESMprompt)
    elif ProductTypeInfo == "SD4100":
        log.debug(f"Platform type :{ProductTypeInfo}")
        output = run_command_cli(cmd, prompt="ESM\s\w\s.*=>")
    else:
        output = run_command_cli(cmd, prompt="ESM\s\S\_\d\s=\>")
    return output


@logThis
def verify_esm_mode_cli_command(device, expect='Single'):
    log.info("Inside verify_esm_mode_cli_command procedure")
    """
    verify esm mode single or share by esm serial
    :param device:product under test
    :param expect:[single,share]
    """
    cmd = 'mode get\r'
    err_count = 0
    output = run_ESM_command(cmd)
    log.debug(output)
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    if ProductNameInfo == "Titan_G2_Lenovo":
        log.debug(f"Product Name :{ProductNameInfo}")
        p = r'State E:\s+(\S+)\s+Mode'
        expect='Shared'
    elif ProductNameInfo == "Titan_G2_Kiwi":
        log.debug(f"Product Name :{ProductNameInfo}")
        p = r'State D:\s+(\S+)\s+Mode'
    elif ProductNameInfo == "Nebula_Gen2F":
        log.debug(f"Product Name :{ProductNameInfo}")
        p = r'State E:\s+(\S+)\s+Mode'
        expect='Shared'
    elif ProductNameInfo == "Titan_G2_WB":
        log.debug(f"Product Name :{ProductNameInfo}")
        p = r'State E:\s+(\S+)\s+Mode'
        expect='Shared'
    elif ProductNameInfo == "athena_g2":
        log.debug(f"Product Name :{ProductNameInfo}")
        p = r'State E:\s+(\S+)\s+Mode'
        expect='Shared'
    else:
        p = r'State D:\s+(\S+)\s+Mode'
    match = re.search(p, output)
    log.debug(f"match  => {match.group(1)}")
    if match:
        current_status = match.group(1).strip()
        print(current_status)
        if current_status == expect:
            log.info("Successfully verify_esm_mode_cli_command: {}".format(expect))
        else:
            log.error("Current mode status : {} mismatch expect : {}".format(current_status, expect))
            err_count += 1
    else:
        log.error("Fail to get mode pattern")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_esm_mode_cli_command fail')

@logThis
def verify_ses_page_00h(username, hostip, password, devicename):
    """
    verify ses page 00h
    :param username
    :param hostip: host ip
    :param password
    :param devicename:sg_ses use devicename to get ses page
    """
    cmd = 'sg_ses --page=0x00 ' + devicename
    err_count = 0
    child = whitebox_lib.ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF,timeout=180)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90":
        p1 = ['\[0x0\]', '\[0x1\]', '\[0x2\]', '\[0x4\]', '\[0x5\]', '\[0x7\]', '\[0xa\]', '\[0xe\]', '\[0x13\]', '\[0x15\]']
    elif ProductTypeInfo == "LENOVO":
        p1 = ['\[0x0\]', '\[0x1\]', '\[0x2\]', '\[0x4\]', '\[0x5\]', '\[0x7\]', '\[0xa\]', '\[0xe\]', '\[0x10]', '\[0x11]', '\[0x13]', '\[0x15]', '\[0x17]']
    elif ProductTypeInfo == "Nebula_Gen2F":
        p1 = ['\[0x0\]', '\[0x1\]', '\[0x2\]', '\[0x4\]', '\[0x5\]', '\[0x7\]', '\[0xa\]', '\[0xe\]', '\[0x11]', '\[0x12]', '\[0x13]', '\[0x20]', '\[0x21]', '\[0x22]', '\[0x23]', '\[0x24]']
    elif ProductTypeInfo == "TITAN-4U90":
        p1 = ['\[0x0\]', '\[0x1\]', '\[0x2\]', '\[0x4\]', '\[0x5\]', '\[0x7\]', '\[0xa\]', '\[0xe\]', '\[0x11]', '\[0x13]', '\[0x15]']
    elif ProductTypeInfo == "SD4100":
        p1 = ['\[0x0\]', '\[0x1\]', '\[0x2\]', '\[0x4\]', '\[0x5\]', '\[0x7\]', '\[0xa\]', '\[0xe\]', '\[0x10\]', '\[0x11\]', '\[0x13\]', '\[0x15\]', '\[0x17\]']
    else:
        p1 = ['\[0x0\]', '\[0x1\]', '\[0x2\]', '\[0x4\]', '\[0x5\]', '\[0x7\]', '\[0xa\]', '\[0xe\]', '\[0x10\]', '\[0x12\]', '\[0x13\]', '\[0x14\]', '\[0x15\]', '\[0x17\]']
    for i in p1:
        count = len(re.findall(i, output))
        if count == 1:
            log.info("Successfully get {} in ses page 00h".format(i))
        else:
            log.error("Fail to match the count of {}, current is {}, should be 1".format(i, count))
            err_count += 1
    if err_count:
        raise RuntimeError('verify_ses_page_00h fail')

@logThis
def ssh_command_get_sg_device(username, hostip, password, cmd):
    """
    verify ses page 00h
    :param username
    :param hostip: host ip
    :param password
    """
    p = 'sg.+'
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    log.info(output)
    match = re.search(p, output)
    if match:
        log.info("Successfully get device name: {}".format(output))
        return output
    else:
        log.error("fail to get device name, please check the command")
        raise RuntimeError('ssh_command_get_sg_device fail')

@logThis
def ssh_command_set_ses_page_command(username, hostip, password, cmd):
    """
    verify set ses page command
    :param username
    :param hostip: host ip
    :param password
    :param devicename:sg_ses use devicename to get ses page
    """
    err_count = 0
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    log.info(cmd)
    log.info(output)
    output =  output + 'OK'
    log.info(output)
    if output == 'OK':
        log.info("Successfully to set ses page command: {}".format(cmd))
    else:
        log.error("Fail to set ses page command: {}".format(cmd))
        err_count += 1
    if err_count:
        raise RuntimeError('ssh_command_set_ses_page_command fail')

@logThis
def get_output_from_ssh_command(username, hostip, password, cmd, timeout=30):
    err_count = 0
    fail_info_list = ['command not found', 'No such file or directory', 'cannot read file', 'Unknown command', 'not found', 'no space left on device', 'Command exited with non-zero status']
    log.info(cmd)
    child = whitebox_lib.ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF, timeout=300)
    output = child.before.strip().decode('utf-8')
    for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
    if err_count:
        raise RuntimeError('get_output_from_ssh_command fail')
    else:
        log.info("Successfully get_output_from_ssh_command:{}".format(output))
        return output

@logThis
def verify_ses_page_02h_info_bit(username, hostip, password, devicename, expect='1'):
    """
    verify ses page 02h info bit
    :param username
    :param hostip: host ip
    :param password
    :param devicename:sg_ses use devicename to get ses page
    :param expect: bit value is 1 or 0
    """
    err_count = 0
    cmd1 = 'sg_ses --page=0x02 ' + devicename
    p = ['INFO=(\d+)']
    output = get_output_from_ssh_command(username, hostip, password, cmd1)
    err_count = parse_pattern_value(p, output, expect, err_count)
    if err_count:
        raise RuntimeError('verify_ses_page_02h_info_bit fail')

@logThis
def verify_page_02h_control_bits_via_raw_data(username, hostip, password, devicename, expect='1'):
    """
    verify ses page 02h set control bits via raw data
    :param username
    :param hostip: host ip
    :param password
    :param devicename:sg_ses use devicename to get ses page
    :param expect: bit value is 1 or 0
    """
    err_count = 0
    cmd1 = 'sg_ses --page=0x02 ' + devicename
    p = ['INFO=(\d+)', 'NON-CRIT=(\d+)', 'CRIT=(\d+)']
    output = get_output_from_ssh_command(username, hostip, password, cmd1)
    err_count = parse_pattern_value(p, output, expect, err_count)
    if err_count:
        raise RuntimeError('verify_page_02h_control_bits_via_raw_data fail')

@logThis
def parse_pattern_value(p, output, expect, err_count):
    """
    loop match pattern list
    :param p:pattern list
    :param output
    :param err_count: count error
    :param expect: bit value is 1 or 0
    """
    for i in p:
        match = re.search(i, output)
        if match:
            current_value = match.group(1).strip()
            print(current_value)
            if current_value == expect:
                log.info("Successfully verify {} value: {}".format(i, expect))
            else:
                log.error("current {} value is {}, mismatch expect : {}".format(i, current_value, expect))
                err_count += 1
        else:
            log.error("Fail to get match {} pattern".format(i))
            err_count += 1
    return err_count

@logThis
def get_ses_fw_version_by_ses_page_01h(username, hostip, password, devicename):
    log.debug('Entering procedure get_ses_fw_version_by_ses_page_01h with args : %s\n' % (str(locals())))
    """
    verify ses page 01h ses version
    :param username
    :param hostip: host ip
    :param password
    :param devicename:sg_ses use devicename to get ses page
    """
    cmd = 'sg_ses --page=0x01 ' + devicename
    p = 'rev:\s+(\S+)'
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    match = re.search(p, output)
    if match:
        version = match.group(1).strip()
        log.info("Successfully get ses version: {}".format(version))
        return version
    else:
        log.error("Fail to get ses version")
        raise RuntimeError('Fail to get_ses_fw_version_by_ses_page_01h')
        return None

@logThis
def verify_ses_page_01h_info(username, hostip, password, devicename, dict_info):
    log.debug('Entering procedure verify_ses_page_01h_info with args : %s\n' % (str(locals())))
    """
    verify ses page 01h info
    :param username
    :param hostip: host ip
    :param password
    :param devicename:sg_ses use devicename to get ses page
    :param dict_info: enclosure descriptor list
    """
    err_count = 0
    cmd = 'sg_ses --page=0x01 ' + devicename
    pattern = r'CELESTIC  LENOVO\s+([a-z0-9]+)'
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    log.info(output)
    product_version=get_deviceinfo_from_config("UUT","platformRev")
    if re.search(r"LENOVO", ProductTypeInfo,re.I|re.M):
        pattern = r'CELESTIC  LENOVO\s+([a-z0-9]+)'
        match=re.search(pattern, output,re.I|re.M)
        product_version=match.group(1)

    if re.search(r"TITAN G2", ProductTypeInfo,re.I|re.M):
        log.debug(f"TITAN G2 Product details found :{ProductTypeInfo}")
        dict_info['rev:\s+(\S+)']=get_deviceinfo_from_config("UUT","platformRev")
        dict_info['enclosure logical identifier \(hex\):\s+(.+)']=get_deviceinfo_from_config("UUT","enclosureLogicalIdentifier")
        dict_info['product:\s+(\S+\s\S+)']=ProductTypeInfo
    elif re.search(r"TITAN-4U90", ProductTypeInfo,re.I|re.M):
        log.debug(f"TITAN G2 WB Product details found :{ProductTypeInfo}")
        dict_info['rev:\s+(\S+)']=get_deviceinfo_from_config("UUT","platformRev")
        dict_info['enclosure logical identifier \(hex\):\s+(.+)']=get_deviceinfo_from_config("UUT","enclosureLogicalIdentifier")
        dict_info['product:\s+(\S+\s\S+)']=ProductTypeInfo
    elif re.search(r"SD4100", ProductTypeInfo,re.I|re.M):
        log.debug(f"Cronus WB Product details found :{ProductTypeInfo}")
        dict_info['rev:\s+(\S+)']=get_deviceinfo_from_config("UUT","platformRev")
        dict_info['enclosure logical identifier \(hex\):\s+(.+)']=get_deviceinfo_from_config("UUT","enclosureLogicalIdentifier")
        dict_info['product:\s+(\S+)']=ProductTypeInfo
    elif re.search(r"LENOVO", ProductTypeInfo,re.I|re.M):
        log.debug(f"Product details found :{ProductTypeInfo}")
        dict_info['rev:\s+(\S+)']=product_version
        dict_info['enclosure logical identifier \(hex\):\s+(.+)']=get_deviceinfo_from_config("UUT","enclosureLogicalIdentifier")
        dict_info['product:\s+(\S+\s\S+)']=ProductTypeInfo
    elif re.search(r"Nebula_Gen2F", ProductTypeInfo,re.I|re.M):
        pattern1 = r'CELESTIC  Nebula_Gen2F\s+([a-z0-9]+)'
        pattern2 = r'number of type descriptor headers:\s+([a-z0-9]+)'
        match1=re.search(pattern1, output,re.I|re.M)
        match2=re.search(pattern2, output,re.I|re.M)
        product_version=match1.group(1)
        product_descripter_headers=match2.group(1)
        dict_info['rev:\s+(\S+)']=product_version
        dict_info['enclosure logical identifier \(hex\):\s+(.+)']=get_deviceinfo_from_config("UUT","enclosureLogicalIdentifier")
        dict_info['product:\s+(\S+\s\S+)']=ProductTypeInfo
        dict_info['number of type descriptor headers:\s+(\S+)']=product_descripter_headers
    else:
        dict_info['product:\s+(\S+)']='TITAN-4U90'

    for (k,v) in dict_info.items():
        if ProductNameInfo == "Titan_G2_Lenovo" or ProductNameInfo == "LENOVO" or ProductNameInfo == "Nebula_Gen2F" or ProductNameInfo == "Titan_G2_WB":
            if k == 'relative ES process id:\s+(\w+)':
                match = re.search(k, output)
                dict_info['relative ES process id:\s+(\w+)']=match.group(1)
                if match.group(1) == "1" or match.group(1) == "2":
                    log.success("Successfully verify_ses_page_01h_info: expected {} = {}".format(k, match.group(1)))
                else:
                    err_count += 1
                    log.fail("{} acctual: {} mismatch expected: {}".format(k, v, match.group(1)))
            else:
                match = re.search(k, output)
                if match:
                    value = match.group(1).strip()
                    if value == v:
                        log.success("Successfully verify_ses_page_01h_info: expected {} = {}".format(k, v))
                    else:
                        err_count += 1
                        log.fail("{} acctual: {} mismatch expected: {}".format(k, value, v))
        else:
             match = re.search(k, output)
             if match:
                value = match.group(1).strip()
                if value == v:
                    log.success("Successfully verify_ses_page_01h_info: expected {} = {}".format(k, v))
                else:
                    err_count += 1
                    log.fail("{} acctual: {} mismatch expected: {}".format(k, value, v))
             else:
                err_count += 1
                log.error("Can't find {} in the log".format(k))
    if err_count:
        raise RuntimeError("verify_ses_page_01h_info")

@logThis
def Lenovo_JBOD_via_ses_command(username, hostip, password, diag_cmd, devicename):
    cmd1 = f'sg_senddiag --pf -r {diag_cmd} {devicename}'
    get_output_from_ssh_command(username, hostip, password, cmd1)

@logThis
def should_remove_line(line, remove_words):
    return any([word in line for word in remove_words])

@logThis
def create_gold_file(username, hostip, password, cmd, filename):
    """
    create gold file to check ses page info
    :param username
    :param hostip: host ip
    :param password
    :param filename
    """
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    a = open(filename, 'w')
    a.write(output)
    a.close()
    pattern=r"ses_page_1[0|7]h_gold_file"
    match1=re.search(pattern,filename)
    remove_words = ["Runn","ing Time","minu","seconds..", "hours"]
    if match1:
        log.debug(f"Maching ... create_gold_file :{filename}")
        with open(filename, "r") as f, open("temp.txt", "w") as working:
            for line in f:
                if not should_remove_line(line, remove_words):
                    working.write(line)
        # replace file with original name
        os.replace('temp.txt', filename)    

@logThis
def compare_file(file1, file2, testname=''):
    """
    compare file1 and fil2, same return true
    """
    result = filecmp.cmp(file1, file2)
    if result:
        log.success("Successfully compare files {}".format(testname))
    else:
        device_obj = Device.getDeviceObject(device)
        cmd = 'diff ' + file1 + ' ' +file2
        log.fail("compare files fail {}".format(testname))
        diff = Device.execute_local_cmd(device_obj, cmd)
        log.info('========the differences between two files========')
        log.info(diff)
        raise RuntimeError("FAIL compare_file fail {}".format(testname))

def compare_file_complex(file1, file2, file3, file4):
    """
    compare files complex
    """
    err_count = 0
    result1 = filecmp.cmp(file1, file3)
    result2 = filecmp.cmp(file2, file3)
    result3 = filecmp.cmp(file1, file4)
    result4 = filecmp.cmp(file2, file4)
    if result1 or result3:
        log.success("Successfully compare file 1")
    else:
        log.fail("compare file 1 fail")
        err_count += 1
    if result2 or result4:
        log.success("Successfully compare file 2")
    else:
        log.fail("compare file 2 fail")
        err_count += 1
    if  err_count:
        raise RuntimeError("FAIL compare files fail")

@logThis
def verify_ses_page_02_cooling_Mode(username, hostip, password, devicename, expect='external'):
    """
    verify ses page 02h external/internal mode
    :param username
    :param hostip: host ip
    :param password
    :param devicename:sg_ses use devicename to get ses page
    :param expect: external|internal
    """
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    err_count = 0
    if expect == 'external':
        cmd1 = 'sg_ses --page=0x02 --index=coo,-1 --set=3:3:1=1 ' + devicename
        output = get_output_from_ssh_command(username, hostip, password, cmd1)
        value = '1'
    else:
        cmd1 = 'sg_ses --page=0x02 --index=coo,-1 --set=3:3:1=0 ' + devicename
        output = get_output_from_ssh_command(username, hostip, password, cmd1)
        value = '0'
    time.sleep(10)
    for i in range(0, 5, 1):
        cmd2 = 'sg_ses --page=0x02 --index=coo,{} --get=3:3:1 '.format(i) + devicename
        log.info(cmd2)
        output = get_output_from_ssh_command(username, hostip, password, cmd2)
        if output == value:
            log.info("Successfully set/get fan {} mode: {}".format(i, expect))
        else:
            log.fail("Fail to set/get fan {} mode: {}".format(i, expect))
            err_count += 1
    if ProductTypeInfo == "CELESTIC  P2523":
        cmd2 = 'sg_ses --page=0x02 --index=coo,5 --get=3:3:1 '.format(i) + devicename
        log.info(cmd2)
        output = get_output_from_ssh_command(username, hostip, password, cmd2)
        if output == value:
            log.info("Successfully set/get fan {} mode: {}".format(i, expect))
        else:
            log.fail("Fail to set/get fan {} mode: {}".format(i, expect))
            err_count += 1
    if ProductTypeInfo == "Nebula_Gen2F":
        log.debug(f"Platform type :{ProductTypeInfo}")
        for i in range(0, 2, 1):
           cmd2 = 'sg_ses --page=0x02 --index=coo,{} --get=3:3:1 '.format(i) + devicename
           log.info(cmd2)
           output = get_output_from_ssh_command(username, hostip, password, cmd2)
           if output == value:
              log.info("Successfully set/get fan {} mode: {}".format(i, expect))
           else:
              log.fail("Fail to set/get fan {} mode: {}".format(i, expect))
              err_count += 1
        value = '0'
        for i in range(2, 5, 1):
           cmd2 = 'sg_ses --page=0x02 --index=coo,{} --get=3:3:1 '.format(i) + devicename
           log.info(cmd2)
           output = get_output_from_ssh_command(username, hostip, password, cmd2)
           if output == value:
              log.info("Successfully set/get fan {} mode: {}".format(i, expect))
           else:
              log.fail("Fail to set/get fan {} mode: {}".format(i, expect))
              err_count += 1
    if err_count:
        raise RuntimeError("verify_ses_page_02_Cooling_Mode:{} fail".format(expect))

@logThis
def verify_esm_fan_mode_cli_command(device, expect='external'):
    """
    verify esm fan mode external or internal by esm serial
    :param device:product under test
    :param expect:[external, internal]
    """
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    #change_to_ESM_mode()
    cmd = 'fan get\r'    
    err_count = 0
    out = " "
    #out = run_command_cli(cmd)
    out = run_ESM_command(cmd)
    time.sleep(10)
    log.info(out)
    if ProductTypeInfo == "Nebula_Gen2F":
        log.debug(f"Platform type :{ProductTypeInfo}")
        p=r'vFanG[0-9]_PS\s[0-9].*?RPM.*?(\S+)ternal'
        output1=out.splitlines()
        for i in output1:
            match = re.search(p, i,re.I|re.M)
            if match:
                mode = match.group(1).strip() + 'ternal'
                if mode.lower() == expect:
                    log.success(f"Successfully verify_esm_fan_mode_cli_command fan module : {expect}")
                else:
                    err_count += 1
                    log.fail(f"Fail to verify fan module acctual: {mode.lower()} mismatch expected: {expect}")
    elif ProductTypeInfo == "CELESTIC  P2523":
        log.debug(f"Platform type :{ProductTypeInfo}")
        output1=out.splitlines()
        pattern=".*FAN_GROUP.*?(\S+)ternal"
        for i in output1:
            match = re.search(pattern, i,re.I|re.M)
            if match:
                mode = match.group(1).strip() + 'ternal'
                if mode.lower() == expect:
                    log.success(f"Successfully verify_esm_fan_mode_cli_command fan module : {expect}")
                else:
                    err_count += 1
                    log.fail(f"Fail to verify fan module acctual: {mode.lower()} mismatch expected: {expect}")
    else:
        for i in range(1, 6):
            p = 'Module {}.*?RPM.*?(\S+)ternal'.format(i)
            match = re.search(p, out)
            if match:
                mode = match.group(1).strip() + 'ternal'
                if mode.lower() == expect:
                    log.success("Successfully verify_esm_fan_mode_cli_command fan module {}: {}".format(i, expect))
                else:
                    err_count += 1
                    log.fail("Fail to verify fan module {} acctual: {} mismatch expected: {}".format(i, mode.lower(), expect))
            else:
                err_count += 1
                log.error("Can't match {} in the log".format(p))
    if err_count:
        raise RuntimeError("verify_esm_fan_mode_cli_command fail" )
    #exit_ESM_mode()

@logThis
def verify_esm_fan_mode_cli_command_nebula(device, expect='external'):
    """
    verify esm fan mode external or internal by esm serial
    :param device:product under test
    :param expect:[external, internal]
    """
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    cmd = 'fan get\r'
    err_count = 0
    output = run_command_cli(cmd)
    #output = run_ESM_command(cmd)
    log.info(output)
    if ProductTypeInfo == "Nebula_Gen2F":
        log.debug(f"Platform type :{ProductTypeInfo}")
        for i in range(1, 3, 1):
            p = f'vFanG{i}_PS\s{i}.*?RPM.*?(\S+)ternal'
            match = re.search(p, output)
            if match:
                mode = match.group(1).strip() + 'ternal'
                if mode.lower() == expect:
                    log.success(f"Successfully verify_esm_fan_mode_cli_command fan module {i}: {expect}")
                else:
                    err_count += 1
                    log.fail(f"Fail to verify fan module {i} acctual: {mode.lower()} mismatch expected: {expect}")
            else:
                err_count += 1
                log.error(f"Can't match {p} in the log")
    for i in range(1, 3, 1):
        for j in range(1, 9, 1):
            p=f"sFan#0{j}_vFanG{i}.*?RPM.*?(\S+)"
            match = re.search(p, output)
            if match:
                Status=match.group(1).strip()
                if Status == 'Normal':
                    log.success(f"Successfully verify_esm_fan_mode_cli_command fan module Fan#0{j}_vFanG{i}: Normal")
                else:
                    err_count += 1
                    log.faila(f"Fail to verify fan module Fan#0{j}_vFanG{i}: Actual : {Status} Expected: Normal")
    if err_count:
        raise RuntimeError("verify_esm_fan_mode_cli_command_nebula fail" )

@logThis
def check_disk_number_via_ses_cmd(username, hostip, password, cmd, expect, not_test_hdd='0', status='on'):
    """
    :param expect: total disk number
    :param status: on(hdd is power on), off(hdd is power off)
    """
    cmd1 = 'sg_scan -ai'
    output = get_output_from_ssh_command(username, hostip, password, cmd1)
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    log.info(output)
    time.sleep(120)
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    time.sleep(140)
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    log.info(output)
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    if ProductTypeInfo == "TITAN G2-4U90":
        if expect!= '0':
            expect='90'
        not_test_hdd='6'
#  if status == 'on':
#        test_disk_amount = int(output) - int(not_test_hdd) - 2
#   else:
#        test_disk_amount = int(output) - int(not_test_hdd)
    test_disk_amount = int(output) - int(not_test_hdd)
    if test_disk_amount == int(expect):
        log.success("Successfully check_disk_number_via_ses_cmd")
    else:
        log.error("check_disk_number FAIL, expect {}, actual is {}".format(expect, test_disk_amount))
        raise RuntimeError("check_disk_number_via_ses_cmd")

def Reboot_OS_via_MGMT(username, hostip, password, cmd):
    log.debug("Entering Reboot_OS_via_MGMT details args : %s" %(str(locals())))
    output = get_output_from_ssh_command(username, hostip, password, cmd)


def check_disk_number_via_os_cmd(username, hostip, password, expect, remove_disk=''):
    """
    check disk number via ses command
    :param username
    :param hostip: host ip
    :param password
    :param cmd:command
    :param expect: total disk number
    """
    err_count = 0
    cmd = 'ls /sys/block/'
    p = 'sd\w+'
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    output = get_output_from_ssh_command(username, hostip, password, cmd)
#    number = len(re.findall(p, output))
    sd_list_1 = re.findall(p, output)
    remove_disk_list = remove_disk.replace(" ","").split(',')
    sd_list = [x for x in sd_list_1 if x not in remove_disk_list]
    number = len(sd_list)
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    #expect_os_number = (int(expect) * 2)
    expect_os_number = expect
    log.debug(f"expect_os_number ={expect_os_number},{type(expect_os_number)}   expect ={expect}, {type(expect)}")
    log.debug(f"number   ==>{number}, {type(number)}")
    if str(number) == expect_os_number:
        log.success("Successfully verify_total_sd_number in /sys/block: {}".format(expect_os_number))
    else:
        log.fail(" Fail to verify_total_sd_number in /sys/block, actual: {} mismatch expect: {}".format(number, expect_os_number))
        err_count += 1
    slot_list = []
    slot_count=0
    if ProductTypeInfo != "LENOVO":
        if ProductTypeInfo != "TITAN G2-4U90" and ProductTypeInfo != "LENOVO":
            log.debug(f"Product Name :{ProductNameInfo}")
            for sd in sd_list:
                cmd = 'ls /sys/block/{}/device/'.format(sd)
                output = get_output_from_ssh_command(username, hostip, password, cmd)
                p = 'enclosure_device:(Slot.*\w+)'
                match = re.search(p, output)
                if match:
                    slot = match.group(1).strip()
                    log.info(slot)
                    slot_list.append(slot)
                    log.success("Successfully find {} in /sys/block/{}/device/".format(slot, sd))
                else:
                    err_count += 1
                    log.fail("Fail to find slot_device in /sys/block/{}/device/".format(sd))
                    slot_count = len(slot_list)                
        else:
            cmd = 'ls /sys/block/*/device |grep -i slot|wc -l'
            slot_count = get_output_from_ssh_command(username, hostip, password, cmd)
            log.info(slot_count)
            #        time.sleep(60)
            slot_count = get_output_from_ssh_command(username, hostip, password, cmd)
            log.info(slot_count)
            #        time.sleep(60)
            slot_count = get_output_from_ssh_command(username, hostip, password, cmd)
            log.info(slot_count)
        if int(slot_count) == int(expect):
            log.success("Successfully verify_total_sd_number in /sys/block/*/device |grep -i slot|wc -l: {}".format(expect))
        else:
            log.fail(" Fail to verify_total_sd_number in /sys/block/*/device |grep -i slot|wc -l, actual: {} mismatch expect: {}".format(slot_count, expect))
            err_count += 1
#    for sd in sd_list:
#        cmd = 'smartctl -a /dev/{}'.format(sd)
#        output = get_output_from_ssh_command(username, hostip, #password, cmd)
#        p = ['SMART overall-health self-assessment test #result:\s+(.+)']
#        common_check_patern_1(output, p, 'PASSED', #'SMART_overall_health_self_test')
    if err_count:
        raise RuntimeError("check_disk_number_via_os_cmd")

@logThis
def run_cli_command(device, cmd):
    """
    :param device:product under test
    """
    output = run_command_cli(cmd)
    return output

@logThis
def turn_on_drive(username, hostip, password, devicename, drivenumber=60, mode='all'):
    """
    :param devicename:sg_ses use devicename to get ses page
    :param mode: mode all is turn on drives one time, not all mode is one by one.
    """
    if mode == 'all':
        cmd = 'sg_ses -p 2 -I arr,-1 --set=3:4:1=0 ' + devicename
        output = get_output_from_ssh_command(username, hostip, password, cmd)
        log.info(output)
        time.sleep(1)
    else:
        for i in range(int(drivenumber)):
            cmd = 'sg_ses -p 2 -I arr,{} --set=3:4:1=0 '.format(i) + devicename
            output = get_output_from_ssh_command(username, hostip, password, cmd)
            log.info(output)
            time.sleep(5)

@logThis
def turn_off_drive(username, hostip, password, devicename, drivenumber=60, mode='all'):
    """
    :param devicename:sg_ses use devicename to get ses page
    :param mode: mode all is turn on drives one time, not all mode is one by one.
    """
    if mode == 'all':
        cmd = 'sg_ses -p 2 -I arr,-1 --set=3:4:1=1 ' + devicename
        output = get_output_from_ssh_command(username, hostip, password, cmd)
        time.sleep(1)
    else:
        for i in range(int(drivenumber)):
            cmd = 'sg_ses -p 2 -I arr,{} --set=3:4:1=1 '.format(i) + devicename
            output = get_output_from_ssh_command(username, hostip, password, cmd)
            log.info(output)
            time.sleep(5)
@logThis
def verify_ses_page_02_fan_current_speed(username, hostip, password, devicename, fan_speed):
    """
    verify ses page 02h fan speed
    :param username
    :param hostip: host ip
    :param password
    :param devicename:sg_ses use devicename to get ses page
    :param fan speed: 9-15
    """
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        log.debug(f"Platform type :{ProductTypeInfo}")
        fan_speed = '14'
    elif ProductTypeInfo == "CELESTIC  P2523":
        log.debug(f"Platform type :{ProductTypeInfo}")
        fan_speed = fan_speed
    else:
        fan_speed = '15'
    err_count = 0
    cmd1 = 'sg_ses --page=0x02 --index=coo,-1 --set=3:3:4={} '.format(fan_speed) + devicename
    output = get_output_from_ssh_command(username, hostip, password, cmd1)
    time.sleep(20)
    for i in range(0, 2, 1):
        time.sleep(3)
        cmd2 = 'sg_ses --page=0x02 --index=coo,{} --get=3:3:4 '.format(i) + devicename
        output = get_output_from_ssh_command(username, hostip, password, cmd2)
        if output == fan_speed:
            log.info("Successfully set/get fan {} speed: {}".format(i, fan_speed))
        else:
            log.fail("Fail to set/get fan {} speed: {}".format(i, fan_speed))
            err_count += 1
    if ProductTypeInfo == "Nebula_Gen2F":
        log.debug(f"Platform type :{ProductTypeInfo}")
        fan_speed = '7'
    for i in range(2, 5, 1):
        time.sleep(3)
        cmd2 = 'sg_ses --page=0x02 --index=coo,{} --get=3:3:4 '.format(i) + devicename
        output = get_output_from_ssh_command(username, hostip, password, cmd2)
        if output == fan_speed:
            log.info("Successfully set/get fan {} speed: {}".format(i, fan_speed))
        else:
            log.fail("Fail to set/get fan {} speed: {}".format(i, fan_speed))
            err_count += 1
    if err_count:
        raise RuntimeError("verify_ses_page_02_fan_current_speed:{} fail".format(fan_speed))

def verify_fan_speed_cli_command(device, fan_speed):
    """
    verify esm fan mode external or internal by esm serial
    :param device:product under test

    :param fan speed:35%-90%
    """
    cmd = 'fan get\r'
    err_count = 0
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    #output = run_command_cli(cmd)
    output = run_ESM_command(cmd)
    log.info(output)   
    if ProductTypeInfo == "CELESTIC  P2523":
      log.debug(f"Platform type :{ProductTypeInfo}")
      p= '.*ESM.*_FAN.*RPM.*\[(.+)\]'
      output1=output.splitlines()
      count=0
      for line in output1:
        match = re.search(p, line)
        if match:
            speed = match.group(1).strip()
            log.info(speed)
            if speed == fan_speed:
               log.success("Successfully verify_fan_speed_cli_command fan speed")
            else:
                err_count += 1
                log.fail("Fail to verify fan speed  actual: {} mismatch expected: {}".format( speed, fan_speed))
            count= count +1 
      if count == 0 :
          log.error("Can't match {} in the log".format(p))
    else:
      for i in range(1, 6):
        if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == 'TITAN-4U90':
            p = 'Module {}.*?RPM.*?\S+ternal\s+(\d+)\[.+\]'.format(i)
            if ProductNameInfo == "Titan_G2_Lenovo":
                log.debug(f"Product Name :{ProductNameInfo}")
                fan_speed="50%"
            elif ProductTypeInfo == "LENOVO":
                log.debug(f"Product Name :{ProductNameInfo}")
                fan_speed="90%"
        elif ProductTypeInfo == "Nebula_Gen2F":
            log.debug(f"Product Name :{ProductNameInfo}")
            fan_speed="70%"
            p = 'PSU[0-9]_FAN_GROUP_PSU[0-9].*RPM.*?\S+ternal\s+\[(.+)\]'
        else:
            p = 'Module {}.*?RPM.*?\S+ternal\s+\[(.+)\]'.format(i)
        match = re.search(p, output)
        if match:
            speed = match.group(1).strip()
            if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == 'TITAN-4U90':
                speed = speed + '%'
                if speed >= fan_speed:
                    log.success("Successfully verify_fan_speed_cli_command fan module {} speed : {}".format(i, fan_speed))
                else:
                    err_count += 1
                    log.fail("Fail to verify fan module {} acctual: {} mismatch expected: {}".format(i, speed, fan_speed))
            else:
                if speed == fan_speed:
                    log.success("Successfully verify_fan_speed_cli_command fan module {} speed : {}".format(i, fan_speed))
                else:
                    err_count += 1
                    log.fail("Fail to verify fan module {} acctual: {} mismatch expected: {}".format(i, speed, fan_speed))
        else:
            err_count += 1
            log.error("Can't match {} in the log".format(p))
    if err_count:
        raise RuntimeError("verify_fan_speed_cli_command fail" )

@logThis
def set_ses_page_02_fan_speed(username, hostip, password, devicename, fan_speed):
    """
    :param devicename:sg_ses use devicename to set ses page
    :param fan speed: 9-15
    """
    cmd = 'sg_ses --page=0x02 --index=coo,-1 --set=3:3:4={} '.format(fan_speed) + devicename
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    time.sleep(20)

@logThis
def get_ses_page_02_fan_speed(username, hostip, password, devicename, fan_speed):
    log.debug("Entering get_ses_page_02_fan_speed details args : %s" %(str(locals())))
    """
    :param devicename:sg_ses use devicename to get ses page
    :param fan speed: 9-15
    """
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    if ProductNameInfo == "Titan_G2_Lenovo" or ProductNameInfo == "Titan_G2_Kiwi":
        log.debug(f"Platform type :{ProductNameInfo}")
        fan_speed = '14'
    elif ProductNameInfo == "Nebula_Gen2F":
        log.debug(f"Platform type :{ProductNameInfo}")
        fan_speed = '15'

    err_count = 0
    for i in range(0, 2, 1):
        time.sleep(3)
        cmd = 'sg_ses --page=0x02 --index=coo,{} --get=3:3:4 '.format(i) + devicename
        output = get_output_from_ssh_command(username, hostip, password, cmd)
        if output == fan_speed:
            log.info("Successfully get fan {} speed: {}".format(i, fan_speed))
        else:
            log.fail("Fail to get fan {} speed: {}".format(i, fan_speed))
            err_count += 1

    #if ProductNameInfo == "Nebula_Gen2F":
    #    fan_speed = '7'

    for i in range(2, 5, 1):
        time.sleep(3)
        cmd = 'sg_ses --page=0x02 --index=coo,{} --get=3:3:4 '.format(i) + devicename
        output = get_output_from_ssh_command(username, hostip, password, cmd)
        if output == fan_speed:
            log.info("Successfully get fan {} speed: {}".format(i, fan_speed))
        else:
            log.fail("Fail to get fan {} speed: {}".format(i, fan_speed))
            err_count += 1
    if ProductTypeInfo == "CELESTIC  P2523":
        cmd = 'sg_ses --page=0x02 --index=coo,{} --get=3:3:4 '.format(5) + devicename
        output = get_output_from_ssh_command(username, hostip, password, cmd)
        if output == fan_speed:
            log.info("Successfully get fan {} speed: {}".format(5, fan_speed))
        else:
            log.fail("Fail to get fan {} speed: {}".format(5, fan_speed))
            err_count += 1
    if err_count:
        raise RuntimeError("get_ses_page_02_fan_speed:{} fail".format(fan_speed))

@logThis
def verify_ses_page_04(username, hostip, password, devicename, expect_ESMA_IP, expect_gateway, expect_ESM_A_DHCP_Mode, expect_ESMA_up_time, \
                        expect_ESMB_up_time=0, expect_ESM_Zoning_Mode='00', expect_ESMB_IP='000.000.000.000', expect_ESM_B_DHCP_Mode='00', \
                        expect_netmask='255.255.255.000', expect_LCD_mask='ff', expect_LCD='00'):
    """
    :param devicename:sg_ses use devicename to get ses page
    :param '81':enable '80':disabled, '00':not support
    """
    err_count = 0
    dict_expect = {'esm_a_ip' : expect_ESMA_IP, 'esm_b_ip' : expect_ESMB_IP, 'gateway' : expect_gateway, 'esm_zoning_mode' : expect_ESM_Zoning_Mode, \
                    'esm_a_dpcp_mode' : expect_ESM_A_DHCP_Mode, 'esm_b_dpcp_mode' : expect_ESM_B_DHCP_Mode, 'netmask' : expect_netmask, \
                   'lcd_mask' : expect_LCD_mask, 'lcd' : expect_LCD}
    print(dict_expect)
    cmd = 'sg_ses --page=0x04 ' + devicename
    p = 'String.+\n\s+00\s+(.+)\s+\..+\n\s+10\s+(.+)\s+\.'
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    match = re.search(p, output)
    if match:
        page_4_list = match.group(1).strip().split() + match.group(2).strip().split()
        print(page_4_list)
        ESMA_up_time = parser_openbmc_lib.parse_hex_to_int("".join(page_4_list[0:4]))
        ESMB_up_time = parser_openbmc_lib.parse_hex_to_int("".join(page_4_list[4:8]))
        ESM_Zoning_Mode = page_4_list[9]
        ESM_A_DHCP_Mode = page_4_list[10]
        ESM_B_DHCP_Mode = page_4_list[11]
        ESMA_IP = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[12:16]])
        ESMB_IP = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[16:20]])
        netmask = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[20:24]])
        gateway = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[24:28]])
        LCD_mask = page_4_list[28]
        LCD = page_4_list[29]
        print(ESMA_up_time)
        print(ESMB_up_time)
        dict_actual = {'esm_a_ip' : ESMA_IP, 'esm_b_ip' : ESMB_IP, 'gateway' : gateway, 'esm_zoning_mode' : ESM_Zoning_Mode, \
                        'esm_a_dpcp_mode' : ESM_A_DHCP_Mode, 'esm_b_dpcp_mode' : ESM_B_DHCP_Mode, 'netmask' : netmask, 'lcd_mask' : LCD_mask, 'lcd' : LCD}
        print(dict_actual)
        for k in dict_expect.keys() & dict_actual.keys():
            if dict_expect[k] == dict_actual[k]:
                log.success("Successfully verify {}: {}".format(k, dict_expect[k]))
            else:
                log.fail("Fail to verify {}: {}, expect: {}".format(k, dict_actual[k], dict_expect[k]))
                err_count += 1
        if ESMA_up_time - expect_ESMA_up_time <= 10 and ESMA_up_time >= 0:
            log.success("Successfully verify ESMA_up_time: {}".format(ESMA_up_time))
        else:
            log.fail("Fail to verify ESMA_up_time: {}, expect: {}".format(ESMA_up_time, expect_ESMA_up_time))
            err_count += 1
        log.debug(f"ESMB_up_time ==>{ESMB_up_time} expect_ESMB_up_time =>{expect_ESMB_up_time} ESMB_up_time =>{ESMB_up_time}")
        if ESMB_up_time - expect_ESMB_up_time <= 10 and ESMB_up_time >= 0:
            log.success("Successfully verify ESMB_up_time: {}".format(ESMB_up_time))
        else:
            log.fail("Fail to verify ESMB_up_time: {}, expect: {}".format(ESMB_up_time, expect_ESMB_up_time))
            err_count += 1
    else:
        err_count += 1
        log.fail("Can't match the patern: {}".format(p))
    if err_count:
        raise RuntimeError("verify_ses_page_04")

@logThis
def get_ipconfig_cli(device, mode):
    """
    :param mode: ip|gateway|dhcp|mac
    """
    cmd = 'ipconfig\r'
    err_count = 0
    output = run_command_cli(cmd)
    if mode == 'dhcp':
        p = 'DHCP\s+\:\s+(\S+)'
    elif mode == 'ip':
        p = 'Local IP\s+\:\s+(\S+)'
    elif mode == 'gateway':
        p = 'Default Gate.+\:\s+(\S+)'
    elif mode == 'mac':
        p = 'MAC Address\s+\:\s+(\S+)'
    else:
        log.fail("Fail to match mode : ip|gateway|dhcp|mac")
        err_count += 1
    match = re.search(p, output)
    if match:
        keyword = match.group(1).strip()
        log.success("Successfully find {} in ipconfig".format(keyword))
        if keyword == 'ON':
            return '81'
        elif keyword == 'OFF':
            return '80'
        else:
            return keyword
    else:
        err_count += 1
        log.fail("Fail to find keyword: {} in ipconfig".format(p))
    if err_count:
        raise RuntimeError("get_ipconfig_cli")

@logThis
def get_esm_up_time(device):
    log.debug('Entering procedure get_esm_up_time ')
    cmd = 'log get\r'
    run_ESM_command('log clear\r')
    #output = run_command_cli(cmd)
    output = run_ESM_command(cmd)
    log.info(output)
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    if ProductNameInfo == "Titan_G2_Lenovo" or ProductNameInfo == "Titan_G2_Kiwi" or ProductNameInfo == "Titan_G2_WB" or ProductNameInfo == "Cronus_WB":
        log.debug(f"Product Name :{ProductNameInfo}")
        p = 'Local Canister Running Time\:\s+(\S+)\s+day\s+(\S+)\s+hours\s+(\S+)\s+minutes\s+(\S+)\s+seconds'
    else:
        p = 'Local ESM Running Time\:\s+(\S+)\s+day\s+(\S+)\s+hours\s+(\S+)\s+minutes\s+(\S+)\s+seconds'
    match = re.search(p, output)
    if match:
        esm_up_time = int(match.group(1).strip()) * 86400 + int(match.group(2).strip()) * 3600 + int(match.group(3).strip()) * 60 + int(match.group(4).strip())
        log.success("Successfully get esm up time: {}".format(esm_up_time))
        return esm_up_time
    else:
        log.fail("Fail to match: {} in log get".format(p))
        raise RuntimeError("get_esm_up_time")

@logThis
def verify_ses_page_05(username, hostip, password, devicename):
    """
    :param devicename:sg_ses use devicename to get ses page
    """
    err_count = 0
    p = '(.+)'
    cmd = 'sg_ses --page=0x05 ' + devicename + ' -r'
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    log.info(cmd)
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    match = re.search(p, output, flags=re.DOTALL)
    if match:
        page_5_list = match.group(1).strip().split()
        print(page_5_list)
        log.debug(f"match   page_5_list  :{page_5_list}")
        if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
            log.debug(f"Platform type :{ProductTypeInfo}")
            prase_ses_page_05(page_5_list, 'drive', 4, 368, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'SAS connector', 368, 404, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'SAS expander', 404, 432, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'psu', 432, 460, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'cooling', 460, 484, '00 00 00 00', '3c 28 28 3c')
            prase_ses_page_05(page_5_list, 'temp sensor', 484, 560, '00 00 00 00', ['00 00 00 00', '5f 5a 01 01', '62 5d 01 01', '87 82 01 01', '87 82 01 01', '87 82 01 01', '5f 5a 01 01', '62 5d 01 01', '87 82 01 01', '87 82 01 01', '87 82 01 01', '42 3d 14 0f', '42 3d 14 0f', '57 52 01 01', '57 52 01 01', '5a 55 01 01', '5a 55 01 01', '73 6e 01 01', '73 6e 01 01'])
            prase_ses_page_05(page_5_list, 'enclosure', 560, 568, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'Enclosure services controller electronics', 568, 580, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'Voltage sensor', 580, 648, '00 00 00 00', ['00 00 00 00', '08 06 06 08', '0c 0a 0a 0c', '0c 0a 0a 0c', '14 0a 0a 14', '08 06 06 08', '08 06 06 08', '08 06 06 08',
'0c 0a 0a 0c', '08 06 06 08', '0c 0a 0a 0c', '0c 0a 0a 0c', '14 0a 0a 14', '08 06 06 08', '08 06 06 08', '08 06 06 08', '0c 0a 0a 0c'])
            prase_ses_page_05(page_5_list, 'Current sensor', 648, 668, '00 00 00 00', ['00 00 00 00', '30 1c c8 c8', '30 1c c8 c8', '30 1c c8 c8', '30 1c c8 c8'])
            prase_ses_page_05(page_5_list, 'Display', 668, 676, '00 00 00 00', '00 00 00 00')
            expect_Temperature_Sensor = '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3c 28 28 3c 3c 28 28 3c 3c 28 28 3c 3c 28 28 3c 3c 28 28 3c 00 00 00 00 5f 5a 01 01 62 5d 01 01 87 82 01 01 87 82 01 01 87 82 01 01 5f 5a 01 01'
            Temperature_Sensor = " ".join([ str(i) for i in page_5_list[420:512]])
        elif ProductTypeInfo == "SD4100":
            log.debug(f"Platform type :{ProductTypeInfo}")
            prase_ses_page_05(page_5_list, 'drive', 4,56 , '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'SAS connector', 56, 76, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'SAS expander', 76, 88, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'psu', 88, 100, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'cooling', 100, 128, '00 00 00 00', '3c 28 28 3c')
            prase_ses_page_05(page_5_list, 'temp sensor', 128, 160, '00 00 00 00', ['00 00 00 00', '52 4d 15 20', '57 53 03 03', '8a 85 03 03', '52 4d 15 20', '54 51 06 05', '8b 86 02 02', '48 41 15 20'])
            prase_ses_page_05(page_5_list, 'enclosure', 160, 168, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'Enclosure services controller electronics', 168, 180, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'Voltage sensor', 180, 232, '00 00 00 00', ['00 00 00 00', '0c 0a 0a 0c', '0a 09 0b 0d', '07 05 07 09', '08 07 0d 0e', '07 05 07 09', '07 06 07 08', '0a 08 0c 0e',
'0b 09 0b 0d', '04 05 0a 09', '0b 09 0b 0d', '07 05 07 09', '05 03 09 0b'])
            prase_ses_page_05(page_5_list, 'Current sensor', 232, 244, '00 00 00 00', ['00 00 00 00', '30 1c c8 c8', '30 1c c8 c8'])
            expect_Temperature_Sensor = '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3c 28 28 3c 3c 28 28 3c 3c 28 28 3c 3c 28 28 3c 3c 28 28 3c 3c 28 28 3c 00 00 00 00 52 4d 15 20 57 53 03 03 8a 85 03 03 52 4d 15 20 54 51 06 05 8b 86 02 02 48 41 15 20'
            Temperature_Sensor = " ".join([ str(i) for i in page_5_list[76:160]])
        elif ProductTypeInfo == "Nebula_Gen2F":
            log.debug(f"Platform type :{ProductTypeInfo}")
            prase_ses_page_05(page_5_list, 'drive', 4, 104, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'psu', 104, 116, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'cooling', 116, 192, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'services controller electronic', 344, 356, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'Enclosure', 356, 364, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'Display', 424, 432, '00 00 00 00', '00 00 00 00')
            expect_Temperature_Sensor = '00 00 00 00 56 51 14 0f 5b 56 01 01 82 7d 01 01 56 51 14 0f 5b 56 01 01 82 7d 01 01 7f 7a 01 01 57 53 01 01 7a 75 01 01 7f 7a 01 01 57 53 01 01 7a 75 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 5f 5d 01 01 4c 47 14 0f'

            expect_Voltage_Sensor = '00 00 00 00 08 06 06 08 08 06 06 08 08 06 06 08 0c 0a 0a 0c 0c 0a 0a 0c 0c 0a 0a 0c 14 10 10 14 08 06 06 08 08 06 06 08 08 06 06 08 0c 0a 0a 0c 0c 0a 0a 0c 0c 0a 0a 0c 14 10 10 14'
            Temperature_Sensor = " ".join([ str(i) for i in page_5_list[192:344]])
            Voltage_Sensor = " ".join([ str(i) for i in page_5_list[364:424]])
            print(Voltage_Sensor)
            if expect_Voltage_Sensor != Voltage_Sensor:
                err_count += 1
                log.fail("The status of Voltage_Sensor is not OK:{}, expect:{}".format(Voltage_Sensor, expect_Voltage_Sensor))
            else:
                log.success("Successfully: the status of Voltage_Sensor is OK:{}".format(Voltage_Sensor))
        elif ProductTypeInfo == "CELESTIC  P2523":
            log.debug(f"Platform type :{ProductTypeInfo}")
            prase_ses_page_05(page_5_list, 'drive', 4, 104, '00 00 00 00', ['00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00'])
            prase_ses_page_05(page_5_list, 'psu', 104, 112, '00 00 00 00', ['00 00 00 00', '00 00 00 00', '00 00 00 00'])
            prase_ses_page_05(page_5_list, 'cooling', 112, 244, '00 00 00 00',['00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00', '00 00 00 00'])
            prase_ses_page_05(page_5_list, 'Voltage sensor', 612, 776, '00 00 00 00',['00 00 00 00', '0c 0a 0a 0c', '0c 0b 0b 0c', '1e 18 26 30', '1f 1e 1d 1e', '0c 0b 08 09', '0c 0b 08 09', '0c 0b 08 09', '0c 0b 08 09', '1d 1c 1a 1c', '1d 1c 1a 1c', '4c 4a 5c 5e', '4c 4a 5c 5e', '0a 08 08 0a', '1b 1a 1a 1b', '0c 0b 0b 0c', '1f 1e 1d 1e', '0c 0b 0b 0c', '0c 0b 0b 0c', '1e 18 26 30', '0c 0b 0b 0c', '0c 0b 0b 0c', '0c 0b 0b 0c', '1e 18 26 30', '1f 1e 1d 1e', '0c 0b 08 09', '0c 0b 08 09', '0c 0b 08 09', '0c 0b 08 09', '1d 1c 1a 1c', '1d 1c 1a 1c', '4c 4a 5c 5e', '4c 4a 5c 5e', '0a 08 08 0a', '1b 1a 1a 1b', '0c 0b 0b 0c', '1f 1e 1d 1e', '0c 0b 0b 0c', '0c 0b 0b 0c', '1e 18 26 30', '0c 0b 0b 0c'])
            prase_ses_page_05(page_5_list, 'Enclosure services controller electronics',776, 788, '00 00 00 00', ['00 00 00 00','00 00 00 00','00 00 00 00'])
            prase_ses_page_05(page_5_list, 'Enclosure', 788, 796, '00 00 00 00', ['00 00 00 00', '00 00 00 00'])
            Temperature_Sensor = " ".join([ str(i) for i in page_5_list[248:612]])
            expect_Temperature_Sensor = '00 00 00 00 5a 32 01 01 23 1d 01 01 82 7c 01 01 5a 55 01 01 7a 74 01 01 82 7c 01 01 4b 46 01 01 64 5f 01 01 73 6e 01 01 73 6e 01 01 64 5f 01 01 64 5f 01 01 64 5f 01 01 64 5f 01 01 73 70 01 01 68 66 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 68 66 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 ff ff 01 01 ff ff 01 01 69 67 01 01 4b 46 01 01 64 5f 01 01 73 6e 01 01 73 6e 01 01 64 5f 01 01 64 5f 01 01 64 5f 01 01 64 5f 01 01 73 70 01 01 68 66 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 68 66 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 73 70 01 01 ff ff 01 01 ff ff 01 01 69 67 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 5d 5a 01 01 46 41 14 0f 46 41 14 0f'
        else:
            prase_ses_page_05(page_5_list, 'drive', 4, 368, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'psu', 368, 396, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'cooling', 396, 420, '00 00 00 00', '3c 28 28 3c')
            prase_ses_page_05(page_5_list, 'services controller electronic', 512, 524, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'subenclosure', 524, 532, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'Voltage sensor', 532, 600, '00 00 00 00', '14 10 10 14')
            prase_ses_page_05(page_5_list, 'SAS expander', 600, 628, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'SAS connector', 628, 664, '00 00 00 00', '00 00 00 00')
            prase_ses_page_05(page_5_list, 'Current sensor', 664, 684, '00 00 00 00', '14 10 10 14')
            prase_ses_page_05(page_5_list, 'Display', 684, 692, '00 00 00 00', '00 00 00 00')
            expect_Temperature_Sensor = '00 00 00 00 5a 55 01 01 62 5d 01 01 5a 55 01 01 62 5d 01 01 42 3d 14 0f 42 3d 14 0f 57 52 01 01 57 52 01 01 5a 55 01 01 5a 55 01 01 64 5f 01 01 64 5f 01 01 7d 78 01 01 7d 78 01 01 ff ff 01 01 ff ff 01 01 55 50 01 01 55 50 01 01 64 5f 01 01 64 5f 01 01 ff 73 01 01 ff 73 01 01'
            Temperature_Sensor = " ".join([ str(i) for i in page_5_list[432:512]])

        log.info(Temperature_Sensor)
        if expect_Temperature_Sensor != Temperature_Sensor:
            err_count += 1
            log.fail("The status of Temperature_Sensor is not OK:{}, expect:{}".format(Temperature_Sensor, expect_Temperature_Sensor))
        else:
            log.success("Successfully: the status of Temperature_Sensor is OK:{}".format(Temperature_Sensor))
    if err_count:
        log.fail("verify_ses_page_05 test fail")
        raise RuntimeError("verify_ses_page_05 test fail")

@logThis
def prase_ses_page_05(page_5_list, element_type, range_start, range_end, expect_overall, expect_element):
    log.debug(f"INSIDE prase_ses_page_05    page_5_list         :{page_5_list}")
    log.debug(f"INSIDE prase_ses_page_05    element_type        :{element_type}")
    log.debug(f"INSIDE prase_ses_page_05    range_start         :{range_start}")
    log.debug(f"INSIDE prase_ses_page_05    range_end           :{range_end}")
    log.debug(f"INSIDE prase_ses_page_05    expect_overall      :{expect_overall}")
    log.debug(f"INSIDE prase_ses_page_05    expect_element      :{expect_element}")
    err_count = 0
    tmp_list = []
    for i in range(range_start, range_end, 4):
        tmp_list.append(" ".join(page_5_list[i:(i+4)]))
    print(tmp_list)
    print(len(tmp_list))
    if tmp_list[0] != expect_overall:
        err_count += 1
        log.fail("The overall status of {}s is not OK:{}, expect:{}".format(element_type, tmp_list[0], expect_overall))
    else:
        log.success("Successfully： the overall status of {}s is OK:{}".format(element_type, expect_overall))
    for i in range(1, len(tmp_list)):
        if type(expect_element) is list:
            if tmp_list[i] != expect_element[i]:
                err_count += 1
                log.fail("The {} {} is not OK:{}, expect:{}".format(element_type, i, tmp_list[i], expect_element[i]))
            else:
                log.success("Successfully： the {} {} is OK:{}".format(element_type, i, expect_element[i]))
        else:
            if tmp_list[i] != expect_element:
                err_count += 1
                log.fail("The {} {} is not OK:{}, expect:{}".format(element_type, i, tmp_list[i], expect_element))
            else:
                log.success("Successfully： the {} {} is OK:{}".format(element_type, i, expect_element))
    if err_count:
        log.fail("prase_ses_page_05 {} test fail".format(element_type))
        raise RuntimeError("prase_ses_page_05 {} test fail".format(element_type))

@logThis
def update_whitebox_fw_force(swimage_type, cmd, username, hostip, password, devicename, isUpgrade=True, image_file=None):
    log.debug("Entering update_whitebox_fw_force with args : %s" %(str(locals())))
    imageObj = SwImage.getSwImage(swimage_type)
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    pass_message = 'Complete, no error'
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    if image_file==None:
        if isUpgrade:
            package_file = imageObj.newImage
        else:
            package_file = imageObj.oldImage
    else:
        package_file = image_file
    if ProductNameInfo == "Titan_G2_Kiwi":
        cmd = cmd + ' -i 4' + ' -I ' + imageObj.localImageDir + package_file + ' ' + devicename + ' -v'
    else:
        cmd = cmd + ' -I ' + imageObj.localImageDir + package_file + ' ' + devicename + ' -v'
    log.info(cmd)
    output = get_output_from_ssh_command(username, hostip, password, cmd, timeout=800)
    if ProductTypeInfo == "Nebula_Gen2F":
        CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
                check_output=output, is_negative_test=True)
    else:
        common_check_patern_2(output, pass_message, 'update_whitebox_fw_force')

@logThis
def ses_activitate(username, hostip, password, devicename, active_mode):
    if active_mode == '0xf':
        cmd = 'sg_ses_microcode -m 0xf {} -vv'.format(devicename)
    elif active_mode == '00h':
        cmd = 'sg_senddiag -p -r 04,00,00,04,a0,00,00,00 {} -vv'.format(devicename)
    elif active_mode == '01h':
        cmd = 'sg_senddiag -p -r 04,00,00,04,a0,00,00,01 {} -vv'.format(devicename)
    elif active_mode == '02h':
        cmd = 'sg_senddiag -p -r 04,00,00,04,a0,00,00,02 {} -vv'.format(devicename)
    elif active_mode == '03h':
        cmd = 'sg_senddiag -p -r 04,00,00,04,a0,00,00,03 {} -vv'.format(devicename)
    elif active_mode == '04h':
        cmd = 'sg_senddiag -p -r 04,00,00,04,a0,00,00,04 {} -vv'.format(devicename)
    else:
        log.info("Please input the right mode")
        raise RuntimeError("ses_activitate")
    output = get_output_from_ssh_command(username, hostip, password, cmd)

@logThis
def verify_ses_version_fru_get(device, isUpgrade=True):
    imageObj = SwImage.getSwImage('SES')
    expect_version = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    log.debug(f"expect_version     ==>{expect_version}")
    expect_version_1 = ".".join([i for i in expect_version.strip().split('.')[0:3]])
    log.debug(f"expect_version_1   ==>{expect_version_1}")
    cmd = 'fru get\r'
    #output = run_command_cli(cmd)
    output = run_ESM_command(cmd)
    p1 = ['FW Revision\WSec 1\W+\s+(.+)', 'FW Revision\WSec 2\W+\s+(.+)']
    p2 = ['FW Revision\W?\s+(\S+)']
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    common_check_patern_1(output, p1, expect_version, 'verify_ses_version_fru_get_1')
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        common_check_patern_1(output, p2, expect_version, 'verify_ses_version_fru_get_2')
    else:
        common_check_patern_1(output, p2, expect_version_1, 'verify_ses_version_fru_get_2')

@logThis
def get_fru_info_cli(device, mode='SES'):
    """
    :param mode: SES|CPLD|ALL SES mode will remove ses info, CPLD mode will remove cpld info, all mode will keep all
    """
    cmd ='fru get\r'
    output = run_command_cli(cmd)
    if mode == 'SES':
        p = ['Running Time', 'Built', 'FW Revision']
    elif mode == 'CPLD':
        p = ['Running Time', 'Built', 'CPLD']
    else:
        p = ['Running Time', 'Built']
    for i in p:
        output = '\n'.join([line for line in output.strip().splitlines() if i not in line])
    return output

@logThis
def verify_sbb_mode(username, hostip, password, devicename, expect='2'):
    cmd = 'sg_ses --page=0x2 -I esc,0 --get=2:7:4 {}'.format(devicename)
    log.info(cmd)
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    if ProductNameInfo == "Titan_G2_Lenovo":
        log.debug(f"Product Name :{ProductNameInfo}")
        expect='3'
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    common_check_patern_3(output, expect, 'verify_sbb_mode')

@logThis
def check_ses_version_via_ses_page(username, hostip, password, devicename, isUpgrade=True):
    imageObj = SwImage.getSwImage('SES')
    expect_version = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    expect_version_1 = "".join([i.zfill(2) for i in expect_version.strip().split('.')])
    expect_version_2 = '0' + "".join([i for i in expect_version.strip().split('.')[0:3]])
    log.info(expect_version_1)
    log.info(expect_version_2)
    p1 = ['ESMA Primary.+B0\s+(\S+)', 'ESMA 1.+B0\s+(\S+)', 'ESMA 2.+B0\s+(\S+)']
    p2 = ['CELESTIC\s+TITAN G2-4U90\s+(\S+)']
    cmd1 = 'sg_ses --page=0x7 {}'.format(devicename)
    cmd2 = 'sg_ses --page=0x2 {}'.format(devicename)
    cmd3 = 'sg_ses --page=0xa {}'.format(devicename)
    output = get_output_from_ssh_command(username, hostip, password, cmd1)
    common_check_patern_1(output, p1, expect_version_1, 'check_ses_version in page 7')
    output1 = get_output_from_ssh_command(username, hostip, password, cmd2)
    common_check_patern_1(output1, p2, expect_version_2, 'check_ses_version in page 2')
    output2 = get_output_from_ssh_command(username, hostip, password, cmd3)
    common_check_patern_1(output2, p2, expect_version_2, 'check_ses_version in page a')

@logThis
def check_cpld_version_via_ses_page(username, hostip, password, devicename, isUpgrade=True):
    imageObj = SwImage.getSwImage('CPLD')
    expect_version = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    expect_version_1 = "".join([i.zfill(2) for i in expect_version.strip().split('.')[0:2]])
    expect_version_2 = "".join([i.zfill(2) for i in expect_version.strip().split('.')[2:]])
    p = '{}\s+{}'.format(expect_version_1, expect_version_2)
    log.info(p)
    cmd1 = 'sg_ses --page=0x7 {}'.format(devicename)
    output = get_output_from_ssh_command(username, hostip, password, cmd1)
    common_check_patern_2(output, p, 'check_cpld_version in page 7')

@logThis
def get_cpld_version_ses_page(username, hostip, password, devicename, isUpgrade=True):
    imageObj = SwImage.getSwImage('CPLD')
    expect_version = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    expect_version_1 = "".join([i.zfill(2) for i in expect_version.strip().split('.')[0:2]])
    expect_version_2 = "".join([i.zfill(2) for i in expect_version.strip().split('.')[2:]])
    return expect_version_1

@logThis
def common_check_patern_1(output, p_list, expect, testname):
    err_count = 0
    for p in p_list:
        match = re.search(p, output)
        if match:
            value = match.group(1).strip()
            if value == expect:
                log.success("Successfully {} {}: {}".format(testname, p, expect))
            else:
                log.fail("Fail to {} {} expect {}, actual is {}".format(testname, p, expect, value))
                err_count += 1
        else:
            err_count += 1
            log.fail("can't match patern:{}".format(p))
    if err_count:
        raise RuntimeError("{}".format(testname))

@logThis
def common_check_patern_2(output, p, testname, expect=True):
    if expect:
        match = re.search(p, output)
        if match:
            log.info("Successfully {}: {}".format(testname, p))
        else:
            log.fail("Fail to {}".format(testname))
            raise RuntimeError("{}".format(testname))
    else:
        match = re.search(p, output)
        if match:
            log.fail("Fail to {}".format(testname))
            raise RuntimeError("{}".format(testname))
        else:
            log.info("Successfully {}: {}".format(testname, p))

@logThis
def common_check_patern_3(output, expect, testname):
    if output == expect:
        log.success("Successfully {}: {}".format(testname, expect))
    else:
        log.fail("Fail to {} expect {}, actual is {}".format(testname, expect, output))
        raise RuntimeError("{}".format(testname))

@logThis
def compare_string(str1, str2, testname=''):
    d=difflib.Differ()
    if str1.strip() == str2.strip():
        log.success("Successfully compare_string {}".format(testname))
    else:
        log.fail("compare_string fail {}".format(testname))
        diff=d.compare(str1.strip().splitlines(), str2.strip().splitlines())
        print('\n'.join(list(diff)))
        raise RuntimeError("compare_string {}".format(testname))

@logThis
def powercycle_pdu(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.powerCycleDevice()

@logThis
def powercycle_pdu1(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.powerCycleDevice1()

@logThis
def powercycle_pdu2(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.powerCycleDevice2()

@logThis
def powercycle_pdu3(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.powerCycleDevice3()

@logThis
def poweroff_pdu1(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.poweroffDevice1()

@logThis
def poweron_pdu1(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.poweronDevice1()

@logThis
def poweroff_pdu3(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.poweroffDevice3()

@logThis
def poweron_pdu3(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.poweronDevice3()

@logThis
def power_cycle_JBOD_via_ses_command(username, hostip, password, devicename):
    cmd1 = 'sg_senddiag -p -r 04,00,00,03,a5,0e,ee {}'.format(devicename)
    cmd2 = 'sg_senddiag -p -r 04,00,00,03,a5,0e,01 {}'.format(devicename)
    get_output_from_ssh_command(username, hostip, password, cmd1)
    output = get_output_from_ssh_command(username, hostip, password, cmd2)
    p = 'DRIVER_OK'
    common_check_patern_2(output, p, 'power_on_off_JBOD_via_ses_command', expect=True)

@logThis
def dc_cycle_server(bmcip, bmcusername, bmcpassword):
    cmd = 'ipmitool -I lanplus -H {} -U {} -P {} power cycle'.format(bmcip, bmcusername, bmcpassword)
    p = 'Chassis Power Control\W\s+Cycle'
    output = Device.execute_local_cmd(device_obj, cmd)
    common_check_patern_2(output, p, 'dc_cycle_server', expect=True)

@logThis
def get_devicename(username, hostip, password, expect='Zone1'):
    #platforminfo = get_PlatformType()
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    #cmd = 'sg_scan -ai'
    cmd = 'lsscsi -g'
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    if ProductTypeInfo == "TITAN G2-4U90":
        log.debug(f"Platform type :{ProductTypeInfo}")
#        p1 = re.compile('(/dev/\S+):.*?\n.*?CELESTIC  TITAN G2')
        p1 = re.compile('enclosu CELESTIC TITAN G2.*(/dev/\S+)')
    elif ProductTypeInfo == "LENOVO":
        log.debug(f"Platform type :{ProductTypeInfo}")
        p1 = re.compile('enclosu CELESTIC LENOVO.*(/dev/\S+)')
    elif ProductTypeInfo == "TITAN-4U90":
        log.debug(f"Platform type :{ProductTypeInfo}")
        p1 = re.compile('enclosu CELESTIC TITAN-4U90.*(/dev/\S+)')
    elif ProductTypeInfo == "SD4100":
        log.debug(f"Platform type :{ProductTypeInfo}")
        p1 = re.compile('enclosu CELESTIC SD4100.*(/dev/\S+)')
    else:
        log.debug(f"platform type :{ProductTypeInfo}")
        p1 = re.compile('(/dev/\S+):.*?\n.*?CELESTIC')

    p2 = 'Unsupported'
    devicename_list = p1.findall(output)
    print(devicename_list)
    cmd1 = 'sg_ses -p 2 -I arr,0 {}'.format(devicename_list[0])
    if len(devicename_list) >= 1:
        output = get_output_from_ssh_command(username, hostip, password, cmd1)
        match = re.search(p2, output)
        if match:
            if expect == 'Zone1':
                return devicename_list[1]
            else:
                return devicename_list[0]
        else:
            if expect == 'Zone1':
                return devicename_list[0]
            else:
                return devicename_list[1]
    else:
        log.fail("Please insert more SAS cables")
        raise RuntimeError("get_devicename")

@logThis
def commandExecute(HDDs, read_cmd):
    for HDD in HDDs:
        cmd = "{} {}".format(read_cmd, HDD)
        run_command(cmd)

@logThis
def validateDictPattern(HDDs, get_cmd, check_pattern):
    for HDD in HDDs:
        command = "{} {}".format(get_cmd, HDD)
        CommonLib.execute_check_dict(Const.DUT, command, patterns_dict=check_pattern)

@logThis
def verifyErrorInjectionControl(page_tool_cmd,HDD,el_id,trigger_value,tool_pattern,page_status_cmd,page_pattern):
         run_command('cd Desktop/ses_page_tool/')
         cmd1 = "{} {}".format(page_tool_cmd, HDD)
         device.sendCmd(cmd1)
         device.readUntil('please input elem id')
         device.sendCmd(el_id)
         device.readUntil('q \| exit\!')
         device.sendCmd(trigger_value)
         output=device.readUntil('Page \(17h\): error injection contrl Done')
         device.sendCmd('q')
         log.info(output)
         check_output_with_dict(Const.DUT, patterns_dict=tool_pattern, check_output=output)
         page_command = "{} {}".format(page_status_cmd, HDD)
         CommonLib.execute_check_dict(Const.DUT, page_command, patterns_dict=page_pattern)

@logThis
def check_output_with_dict(device,patterns_dict={}, path=None, timeout=900, line_mode=True,
                       is_negative_test=False, check_output=None, remark=""):
    if not check_output:
        log.debug('Entering procedure execute_check_dict with args : %s' %(str(locals())))
    deviceObj =  Device.getDeviceObject(device)
    passCount = 0
    patternNum = len(patterns_dict)
    pass_p = []
    pattern_all = []
    output = check_output
    for p_name, p_pass in patterns_dict.items():
        pattern_all.append(p_name)
        if line_mode:
            for line in output.splitlines():
                match = re.search(p_pass, line)
                if match:
                    if is_negative_test:
                        passCount -= 1
                    else:
                        passCount += 1
                    pass_p.append(p_name)
                    break
        else:
            match = re.search(p_pass, output, re.M|re.S)
            if match:
                if is_negative_test:
                    passCount -= 1
                else:
                    passCount += 1
                pass_p.append(p_name)
    if is_negative_test:
        passCount += patternNum
    mismatch_key_name = set(pattern_all)-set(pass_p) if not is_negative_test else set(pass_p)
    log.debug('passCount = %s' %passCount)
    log.debug('patternNum = %s' %patternNum)
    if passCount == patternNum:
        log.info('Testcase is PASSED.Pattern matched as expected\n')
    else:
        log.fail('Pattern match failed. Testcase failed')
        raise RuntimeError("Pattern match failed")

@logThis
def temp_lm_upgrade_test(num, pattern,hdd="/dev/sg1"):
    set_cmd = "sg_ses --page=0x02 --index=coo,-1 --set=3:3:1=" + str(num) + " " + hdd
    device.sendMsg(set_cmd + '\r\n')
    time.sleep(10)
    get_cmd = "sg_ses --page=0x02 --index=coo,1 --get=3:3:1 " + hdd
    output = CommonLib.execute_command(get_cmd,timeout=60)
    count = 0
    for line in output.splitlines():
        line = line.strip()
        match = re.search(pattern, line)
        if match:
            count += 1
    if count == 1:
        log.success('Test pass!')
    else:
        raise RuntimeError("Set and get failed!")

@logThis
def lsscsi():
    cmd = 'lsscsi -g | grep -i enc'
    output = CommonLib.execute_command(cmd, timeout=60)
    right_list=[]
    for line in output.splitlines():
        line = line.strip()
        if '/sg' in line:
            right_list.append(line)
    analyze = right_list[0].split('/sg')[1]
    analyze = analyze.strip()
    return analyze

@logThis
def SendingDiagTest(command):
    analyze = lsscsi()
    if command:
        device.sendMsg(command+' /dev/sg'+analyze+'\r\n')
        time.sleep(5)
    else:
        raise RuntimeError("Can not get param.")
    get_cmd = get_pagex_cmd
    out = CommonLib.execute_command(get_cmd+' /dev/sg'+analyze, timeout=60)
    fail_pattern = 'error|fail'
    match = re.search(fail_pattern, out, re.I)
    if match:
        raise RuntimeError("Occur fails, please check output.")
    else:
        log.success("Check pass.")
        reset_expander_0xx_cmd = "sg_senddiag -p -r 10,00,00,09,00,00,72,65,73,65,74,20,31"
        device.sendMsg(reset_expander_0xx_cmd + ' /dev/sg' + analyze + '\r\n')
        time.sleep(60)

@logThis
def SendingDiagResetTest():
    analyze = lsscsi()
    out = CommonLib.execute_command(get_pagex_cmd + ' /dev/sg' + analyze, timeout=60)
    pass_pattern = "sg_ses failed\: Illegal request"
    match = re.search(pass_pattern,out)
    if match:
        log.success("Reset pass.")
    else:
        raise RuntimeError("Occur fails, please check output.")

@logThis
def sg_ses_p_012():
    analyze = lsscsi()
    cmd = 'sg_ses -p 0x12 /dev/sg' + analyze
    output = CommonLib.execute_command(cmd,timeout=60)
    return  output

@logThis
def fru_get_and_compare(value, fru_pattern_string, compare_string, right_cx):
    output = run_ESM_command("fru get\r")
    fru_string=''
    local_string=''
    compare = value
    pattern = fru_pattern_string
    co_pattern = compare_string
    for line in output.splitlines():
        match1 = re.search(pattern, line)
        if match1:
            fru_string = line
    log.info('--------------match=%s' % fru_string)
    for line in compare.splitlines():
        match2 = re.search(co_pattern, line)
        if match2:
            local_string = line
    log.info('--------------match2=%s' % local_string)
    right_match = re.search(right_cx, fru_string)
    right_match2 = re.search(right_cx, local_string)
    if right_match:
        if right_match2:
            log.success("Test Pass")
        else:
            raise RuntimeError("Occur fails, please check output.")
    else:
        raise RuntimeError("Occur fails, please check output.")


@logThis
def FruSnTest(in_cmd, fa_cmd):
    analyze = lsscsi()
    correct_command_list=[]
    for var in in_cmd:
        correct_command_list.append(var)
    incorrect_command_list = []
    for var in fa_cmd:
        incorrect_command_list.append(var)
    device.sendMsg(correct_command_list[0] + analyze +'\r\n')
    fail_pattern = 'error|fail'
    output = sg_ses_p_012()
    match = re.search(fail_pattern, output, re.I)
    if match:
        raise RuntimeError("Occur fails, please check output.")
    device.sendMsg(correct_command_list[1] + analyze + '\r\n')
    time.sleep(5)
    device.sendMsg(correct_command_list[2] + analyze  + '\r\n')
    output2 = sg_ses_p_012()
    match = re.search(fail_pattern, output2, re.I)
    if match:
        raise RuntimeError("Occur fails, please check output.")
    for incorrect in incorrect_command_list:
        fail_output = CommonLib.execute_command(incorrect + analyze, timeout=30)
        incorrect_pattern = 'sg_senddiag failed\: Illegal request'
        match2 = re.search(incorrect_pattern, fail_output)
        if match2:
            log.success('Check pass!')
            return output2
            time.sleep(10)
        else:
            raise RuntimeError("Occur fails, please check output.")

@logThis
def VpdGetAllTest():
    analyze = lsscsi()
    cmd_list=[
        'sg_senddiag -p -r 12,00,00,05,00,0e,00,00,00 /dev/sg' + analyze,
        'sg_senddiag -p -r 12,00,00,05,00,07,00,00,00 /dev/sg' + analyze,
        'sg_senddiag -p -r 12,00,00,05,00,02,00,00,00 /dev/sg' + analyze,
        'sg_senddiag -p -r 12,00,00,05,00,ff,00,00,00 /dev/sg' + analyze
    ]
    for cmd in cmd_list:
        device.sendMsg(cmd+'\r\n')
        time.sleep(5)
        out = sg_ses_p_012()
        fail_pattern = 'error|fail'
        match = re.search(fail_pattern, out, re.I)
        if match:
            raise RuntimeError("Occur fails, please check output.")
        else:
            log.success('Check pass!')

@logThis
def checkLogStatus(device):
     cmd = 'log get' + "\r"
     ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
     if ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
        ESMAConnect(ESMA_IP_1,ESMA_port_1)
     output = run_command_cli(cmd)
     log.info(output)
     pattern1="Event Log.*: 1/510 entries"
     pattern2="Critical: 0/1"
     pattern3="Warning: 0/1"
     pattern4="Info: 1/1"
     common_check_patern_2(output, pattern1, "Event Log Check", expect=True)
     common_check_patern_2(output, pattern2, "Critical Log Check", expect=True)
     common_check_patern_2(output, pattern3, "Warning Log Check", expect=True)
     common_check_patern_2(output, pattern4, "Info Log Check", expect=True)

@logThis
def verifyLog(HDD,cmd,code,pattern):
    cmd1 = "{} {}".format(cmd,HDD)
    output = run_command(cmd1)
    match=re.search(pattern,output)
    if code == "1":
       if not match:
          log.success("Logs entry displayed")
          return
       else:
          log.info("Log got cleared")
          raise RuntimeError("Log got cleared")
    if code == "2":
        if match:
            log.success("Logs got cleared as expected")
            return
        else:
            log.fail("Logs not cleared")
            raise RuntimeError("Logs not cleared")
    if code == "3":
        if match:
            log.success("Logs are in read status as expected")
            return
        else:
            log.fail("Logs are not in read status")
            raise RuntimeError("Logs are not in read status")
    if code == "4":
        if match:
            log.success("Logs are in unread status as expected")
            return
        else:
            log.fail("Logs are not in unread status")
            raise RuntimeError("Logs are not in unread status")
            
@logThis
def checkLogPageStatus(cmd,HDD):
    cmd1 = "{} {}".format(cmd,HDD)
    output = run_command(cmd1)
    pattern= "00     13 [0-9a-f][0-9a-f] [0-9a-f][0-9a-f] [0-9a-f][0-9a-f].*"
    match=re.search(pattern,output)
    if match:
        log.success("Completion code check successful")
    else:
        log.fail("Completion code check failed")
        raise RuntimeError("Completion code check failed")

@logThis
def verifyPSUStatus(cmd, HDD, pattern):
   cmd1 = "{} {}".format(cmd,HDD)
   output = run_command(cmd1)
   match=re.search(pattern,output)
   if match:
     log.success("PSU status of the page check successful")
   else:
     log.fail("PSU status of the page check  Failed")
     raise RuntimeError("Pattern match failed")

@logThis
def checkCLIPSUStatus(device,pattern):
   cmd = 'fru get\r'
   output = run_ESM_command(cmd)
   log.info(output)
   log.info(pattern)
   match = re.search(pattern,output,re.DOTALL)
#   match = re.search(pattern,output)
   if match:
     log.success("PSU status of the page check successful")
   else:
     log.fail("PSU status of the page check  Failed")
     raise RuntimeError("Pattern match failed")

@logThis
def commandrun(cmd,HDD):
    cmd1 = "{} {}".format(cmd,HDD)
    run_command(cmd1)

@logThis
def checkPSUDetailsWithCLI(psu_pattern,cmd,PSU_NO, HDD, device):
    cmd1 = "{} {}".format(cmd,HDD)
    output = run_command(cmd1)
    cli_cmd = 'fru get\r'
    output1 = run_command_cli(cli_cmd)
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

def checkPSUDetailsWithCLI_athena(page_output,psu_cli_pattern,device):
    cli_cmd = 'fru get'
    CommonLib.send_command("$%^0\r",promptStr=None)
    cli_output = run_ESM_command(cli_cmd)
    log.info(cli_output)
    CommonLib.send_command("$%^3\r",promptStr=None)
    psu_page_pattern="\sElement\s\d\sdescriptor:\s(\S+)\s+(\S+.*)\s+(\S+)\s+(\S+)\s+(\S+).*"
    log.info(psu_page_pattern)
    page_op=page_output.splitlines()
    count=0
    for line in page_op:
      match=re.search(psu_page_pattern,line)
      if match:
          PSU_N0_page =match.group(1).strip()
          PS_TYPE_page=match.group(2).strip()
          PS_Serial_Number_page=match.group(3).strip()
          PS_Hardware_Version_page=match.group(4).strip()
          PS_Firmware_Version_page=match.group(5).strip()
          log.info(PSU_N0_page)
          log.info(PS_TYPE_page)
          log.info(PS_Serial_Number_page)
          log.info(PS_Hardware_Version_page)
          log.info(PS_Firmware_Version_page)
          count = 0
          psu_cli_pattern = psu_cli_pattern.format(PS_TYPE_page,PS_Serial_Number_page,PS_TYPE_page,PS_Hardware_Version_page,PS_Firmware_Version_page)
          break
      else:
          count=count+1
    if  count > 0 :
        log.info("Expected pattern not found in page command")
        raise RuntimeError("Pattern match failed")
    log.info(psu_cli_pattern)
    log.info(cli_output)
    match=re.search(psu_cli_pattern,cli_output)
    if match:
        log.info("Expected pattern found in CLI command as expected")
    else:
        log.info("Expected pattern not found in CLI command")
        raise RuntimeError("Pattern match failed")

@logThis
def checkPSUDetailsWithCLI_titan_g2_wb(psu_pattern,cmd,PSU_NO, HDD, device):
    cmd1 = "{} {}".format(cmd,HDD)
    output = run_command(cmd1)
    Disconnect()
    time.sleep(10) 
    ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
    ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cli_cmd = 'fru get'
    output1 = run_ESM_command(cli_cmd)
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
def checkLogDetailsWithCLI(cmd, HDD, device):
    cmd1 = "{} {}".format(cmd,HDD)
    output = run_command(cmd1)
    output=str(output)
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
        ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cli_cmd = 'log get' + "\r"
    output1 = run_command_cli(cli_cmd)
    log.info(output1)
    p='Event Log.*:\s+(\S+)\/+510.*'
    match=re.search(p,output1)
    if match:
       a=match.group(1)
       log.info("The log count in ESM CLI is")
       log.info(a)
    c=output.splitlines()
    for line in c:
       pattern=' 00     13 00 00\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\s+(\S+).*'
       match1=re.search(pattern,line)
       if match1:
         b=match1.group(6)
         log.info("The log count in ses_page_13 is")
         log.info(b)
         e=str(parser_openbmc_lib.parse_hex_to_int(b))
         log.info(e)
    if(a==e):
        log.success("Log Count Matches")
    else:
        log.fail("Log Count Mismatch")
        raise RuntimeError("Log Count Mismatch")

@logThis
def verifyFlagAsInvalid(cmd,index,HDD):
    cmd1="{}{} {}".format(cmd,index,HDD)
    output=run_command(cmd1)
    index=index.split('-')
    start_index=int(index[0]) + 1
    end_index=int(index[1]) + 2
    for i in range(start_index,end_index,1):
        pattern=""".*Element index: {0}  eiioe=1.*
        .*flagged as invalid \(no further information\).*"""
        pattern=pattern.format(i)
        log.info(pattern)
        match=re.search(pattern,output)
        if match:
            log.success("Pattern match passed as expected")
        else:
            log.fail("Pattern match failed as expected")
            raise RuntimeError("Pattern match failed")

@logThis
def verifyFlagAsValid(cmd,index,HDD):
    cmd1="{}{} {}".format(cmd,index,HDD)
    output=run_command(cmd1)
    index=index.split('-')
    start_index=int(index[0]) + 1
    end_index=int(index[1]) + 2
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    for i in range(start_index,end_index,1):
        pattern=""".*Element index: {0}  eiioe=1.*
        .*Transport protocol: SAS.*
        .*number of phys: 1, not all phys: 0, device slot number: {0}.*
        .*phy index: 0.*
          .*SAS device type: no SAS device attached.*
          .*initiator port for:.*
          .*target port for: SATA_device.*
          .*attached SAS address: \\S+.*
          .*SAS address: \\S+.*
          .*phy identifier: 0x0.*"""
        if ProductTypeInfo == "TITAN-4U90":
           pattern=""".*Element index: {0}  eiioe=1.*
        .*Transport protocol: SAS.*
        .*number of phys: 1, not all phys: 0, device slot number: {0}.*
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
def getTheNumberOfDrives(username, hostip, password):
     cmd1="lsscsi -g | grep -i disk  | wc -l"
     output = get_output_from_ssh_command(username, hostip, password, cmd1)
     log.info(output)
     return output

@logThis
def verifyFanSpeed1(drvcout,fanspeedl75,fanspeedg75,device):
    if int(drvcout) <= 76:
       log.info("less or equal to 75")
       verify_fan_speed_cli_command(device,fanspeedl75)
    else:
       log.info("greater than 75")
       verify_fan_speed_cli_command(device,fanspeedg75)

@logThis
def verifyDriverStatus(cmd,HDD,drv_nums,drv_status):
     cmd1 = "{}{} {}".format(cmd,drv_nums,HDD)
     log.info(cmd1)
     runAndCheck(cmd1, checking=drv_status, is_negative=True)

@logThis
def verifyDriverCountAndStatus(cmd,HDD,drv_nums,drv60_status,drv75_status):
    cmd1 = "{}{} {}".format(cmd,drv_nums,HDD)
    log.info(cmd1)
    drv_count_cmd="lsscsi -g | grep -i disk  | wc -l"
    drv_count = run_command(drv_count_cmd)
    log.info(drv_count)
    match=re.search("76",drv_count)
    match1=re.search("61",drv_count)
    if match:
        runAndCheck(cmd1, checking=drv75_status, is_negative=True)
        return
    elif  match1:
        runAndCheck(cmd1, checking=drv60_status, is_negative=True)
    else:
        raise RuntimeError("Drive count Error")

@logThis
def verifySlotNameFormat(cmd,HDD):
    cmd1 = "{} {}".format(cmd,HDD)
    output= run_command(cmd1)
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")

    if ProductTypeInfo == "CELESTIC  P2523":
       for count in range (1,9):
            pattern="{}{}".format("Slot_0",count)
            match=re.search(pattern,output)
            if match :
                log.success("The slot {} is  in expected format".format(pattern))
            else:
                log.fail("The slot {} is not  in expected format".format(pattern))
                raise RuntimeError("The slot  is not  in expected format")
       for count in range (10,23):
            pattern="{}{}".format("Slot_",count)
            match=re.search(pattern,output)
            if match :
                log.success("The slot {} is  in expected format".format(pattern))
            else:
                log.fail("The slot {} is not  in expected format".format(pattern))
                raise RuntimeError("The slot  is not  in expected format")   
    elif ProductTypeInfo == "TITAN-4U90":
       for count in range(1,10):
            pattern="Slot [0-9][0-9]"
            match=re.search(pattern,output)
            if match :
                log.success("The slot {} is  in expected format".format(pattern))
            else:
                log.fail("The slot {} is not  in expected format".format(pattern))
                raise RuntimeError("The slot  is not  in expected format")
       for count in range(10,91):
            pattern="Slot [0-9][0-9]"
            match=re.search(pattern,output)
            if match :
                log.success("The slot {} is  in expected format".format(pattern))
            else:
                log.fail("The slot {} is not  in expected format".format(pattern))
                raise RuntimeError("The slot  is not  in expected format")
    elif ProductTypeInfo == "SD4100":
       for count in range(1,10):
            pattern="Slot [0-9][0-9]"
            match=re.search(pattern,output)
            if match :
                log.success("The slot {} is  in expected format".format(pattern))
            else:
                log.fail("The slot {} is not  in expected format".format(pattern))
                raise RuntimeError("The slot  is not  in expected format")
       for count in range(10,13):
            pattern="Slot [0-9][0-9]"
            match=re.search(pattern,output)
            if match :
                log.success("The slot {} is  in expected format".format(pattern))
            else:
                log.fail("The slot {} is not  in expected format".format(pattern))
                raise RuntimeError("The slot  is not  in expected format")
    else:
       for count in range(1,10):
            pattern="{}{}".format("Slot00",count)
            match=re.search(pattern,output)
            if match :
                log.success("The slot {} is  in expected format".format(pattern))
            else:
                log.fail("The slot {} is not  in expected format".format(pattern))
                raise RuntimeError("The slot  is not  in expected format")
       for count in range(10,91):
            pattern="{}{}".format("Slot00",count)
            match=re.search(pattern,output)
            if match :
                log.success("The slot {} is  in expected format".format(pattern))
            else:
                log.fail("The slot {} is not  in expected format".format(pattern))
                raise RuntimeError("The slot  is not  in expected format")

@logThis
def checkLogInfoWithCLIAthena(output,device):
    pattern3=".*Event Log.*:\s+(\S+)\/510 entries.*"
    pattern4=".*-- Critical:\s+(\S+)\/.*"
    pattern5=".*-- Warning:\s+(\S+)\/.*"
    pattern6=".*-- Info:\s+(\S+)\/.*"
    pattern7=".*ESM\s+(\S+)\s+\$ log get.*"
    cli_cmd = 'log get' + "\r"
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN-4U90" or ProductTypeInfo == "SD4100" :
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
        ESMAConnect(ESMA_IP_1,ESMA_port_1)
        pattern7=".*ESM\s(\S+).*=\>"
        output1 = run_command_cli(cli_cmd)
        log.info(output1)
    elif ProductTypeInfo == "CELESTIC  P2523":
       log.info("Inside Athena")
       CommonLib.send_command("$%^0\r",promptStr=None)
       output1 = run_ESM_command(cli_cmd)
       log.info(output1)
       CommonLib.send_command("$%^3\r",promptStr=None)
       pattern7=".*ESM\s(\S+)_(\d)\s=\>.*"
    else:
       output1 = run_command_cli(cli_cmd)
       log.info(output1)
    pattern1=".* 00     13 00 00\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+).*"
    pattern2=".* 10\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s.*"
    a=output.splitlines()
    for line in a :
        match=re.search(pattern1,line)
        if match:
           completioncode_byte=match.group(2)
           log_rep_id=match.group(3)
           default_value_byte6=match.group(4)
           current_entry_count=match.group(5)+match.group(6)
           Available_entry_count=match.group(7)+match.group(8)
           Current_Critical_log_count=match.group(9)+match.group(10)
           Current_warning_log_count=match.group(11)+match.group(12)
           Current_info_log_count1=match.group(13)
        match1=re.search(pattern2,line)
        if match1:
           Current_info_log_count2=match1.group(1)
           Current_info_log_count=Current_info_log_count1+Current_info_log_count2
           Event_log_count="{}{}".format(match1.group(2),match1.group(3))
           System_operation_log_count="{}{}".format(match1.group(4),match1.group(5))
           Unread_log_entry_count=(match1.group(6)+match1.group(7))
           defaultvaluebyte23=match1.group(8)
           defaultvaluebyte24=match1.group(9)
    b=output1.splitlines()
    for line in b:
        match2=re.search(pattern3,line)
        if match2:
            event_log_enteries_count_cli=match2.group(1)
        match3=re.search(pattern4,line)
        if match3:
            critical_entries_count_cli=match3.group(1)
        match4=re.search(pattern5,line)
        if match4:
            warning_enteries_count_cli=match4.group(1)
        match5=re.search(pattern6,line)
        if match5:
            info_enteries_count_cli=match5.group(1)
        match6=re.search(pattern7,line)
        if match6:
            ESM_name=match6.group(1)
            log.info(ESM_name)
    if completioncode_byte == "00":
       log.success("completion code check is successful")
    else:
       log.fail("completion code check failed")
       raise RuntimeError("completion code check failed")
    if default_value_byte6 == "00":
       log.success("default_value_byte6 check is successful")
    else:
       log.fail("default_value_byte6 check failed")
       raise RuntimeError("default_value_byte6 check failed")
    if defaultvaluebyte23 == "00":
       log.success("default_value_byte23 check is successful")
    else:
       log.fail("default_value_byte23 check failed")
       raise RuntimeError("default_value_byte23 check failed")
    if defaultvaluebyte24 == "00":
       log.success("default_value_byte24 check is successful")
    else:
       log.fail("default_value_byte24 check failed")
       raise RuntimeError("default_value_byte24 check failed")
    if ESM_name == "A" or ESM_name == "B":
       if log_rep_id == "00":
           log.success("log_rep_id check is successful")
       else:
           log.fail("log_rep_id check failed")
           raise RuntimeError("log_rep_id check failed")
    else:
       if log_rep_id == "01":
           log.success("log_rep_id check is successful")
       else:
           log.fail("log_rep_id check failed")
           raise RuntimeError("log_rep_id check failed")
    current_entry_count_int=str(parser_openbmc_lib.parse_hex_to_int(current_entry_count))
    if current_entry_count_int==event_log_enteries_count_cli :
       log.success("current_entry_count check is successful")
    else:
       log.fail("current_entry_count check failed")
       raise RuntimeError("current_entry_count check failed")
    Current_Critical_log_count_int=str(parser_openbmc_lib.parse_hex_to_int(Current_Critical_log_count))
    if Current_Critical_log_count_int == critical_entries_count_cli :
        log.success("Current_Critical_log_count is successful")
    else:
        log.fail("Current_Critical_log_count Failed")
        raise RuntimeError("Current_Critical_log_count Failed")
    Current_warning_log_count_int=str(parser_openbmc_lib.parse_hex_to_int(Current_warning_log_count))
    if Current_warning_log_count_int==warning_enteries_count_cli:
        log.success("Current_warning_log_count check is successful")
    else:
        log.fail("Current_warning_log_count check failed")
        raise RuntimeError("Current_warning_log_count check failed")
    Current_info_log_count_int=str(parser_openbmc_lib.parse_hex_to_int(Current_info_log_count))
    if Current_info_log_count_int == info_enteries_count_cli :
        log.success("Info entries count check is succesful")
    else:
        log.fail("Info entries count check failed")
        raise RuntimeError("Info entries count check failed")
    Unread_log_entry_count_int=str(parser_openbmc_lib.parse_hex_to_int(Unread_log_entry_count))
    if Unread_log_entry_count_int == current_entry_count_int:
        log.success("Unread_log_entry_count matches with current entry count")
    else:
        log.fail("Unread_log_entry_count does not match with current entry count")
        raise RuntimeError("Unread_log_entry_count does not match with current entry count")
    if Unread_log_entry_count_int == event_log_enteries_count_cli:
        log.success("Unread_log_entry_count matches with event log")
    else:
        log.fail("Unread_log_entry_count does not match with event log")
        raise RuntimeError("Unread_log_entry_count does not match with event log")
    Event_system_log=hex(int(Event_log_count,16)+int(System_operation_log_count,16))
    current_entry_count_cmp=hex(int(current_entry_count,16))
    if Event_system_log == current_entry_count_cmp :
       log.success("Event and system operation count matches with current entry count")
    else:
       log.fail("Event and system operation count does not match with current entry count")
       raise RuntimeError("Event and system operation count does not match with current entry count")
    Available_entry_count_int=str(parser_openbmc_lib.parse_hex_to_int(Available_entry_count))
    Available_entry_count_cli=str(510-int(event_log_enteries_count_cli))
    if Available_entry_count_cli == Available_entry_count_int:
      log.success("Available_entry_count check is successful")
    else:
      log.fail("Available_entry_count check Failed")
      raise RuntimeError("Available_entry_count check Failed")


def checkDisplayOfPageOnce(diagcmd, statuscmd, HDD, pattern):
    pgdiagcmd="{} {}".format(diagcmd,HDD)
    pgstatuscmd="{} {}".format(statuscmd,HDD)
    diagcmdpattern="error|fail"
    timeout_pattern= "00     [0-9a-f][0-9a-f] [0-9a-f][0-9a-f] [0-9a-f][0-9a-f] [0-9a-f][0-9a-f] 03.*"
    diag_op=run_command(pgdiagcmd)
    time.sleep(31)
    pgstatus_op1=run_command(pgstatuscmd)
    pgstatus_op2=run_command(pgstatuscmd)
    common_check_patern_2(diag_op, diagcmdpattern, "command execution successful check", expect=False)
    common_check_patern_2(pgstatus_op1,timeout_pattern,"Timeout byte check", expect=True)
    common_check_patern_2(pgstatus_op2,pattern,"Page Execution Fail Check" , expect=True)
    diag_op1=run_command(pgdiagcmd)
    time.sleep(31)
    pgstatus_op3=run_command(pgstatuscmd)
    pgstatus_op4=run_command(pgstatuscmd)
    common_check_patern_2(diag_op1, diagcmdpattern, "command execution successful check", expect=False)
    common_check_patern_2(pgstatus_op3,timeout_pattern,"Timeout byte check", expect=True)
    common_check_patern_2(pgstatus_op4,pattern,"Page Execution Fail Check" , expect=True)

def checkPageWithexpanderLog(diagcmd, statuscmd, HDD, device):
    cutcmd="|cut -c 61-78"
    pgdiagcmd="{} {}".format(diagcmd,HDD)
    pgstatuscmd="{} {}{}".format(statuscmd,HDD,cutcmd)
    diagcmdpattern="error|fail"
    cli_cmd1 = 'log get' + "\r"
    output1 = run_command_cli(cli_cmd1)
    b=output1.splitlines()
    pattern3=".*Event Log \(V.11\):\s+(\S+)\/510 entries.*"
    #pattern3=".*Event Log.*:\s+(\S+)\/510 entries.*"
    pattern4=".*-- Critical:\s+(\S+)\/.*"
    pattern5=".*-- Warning:\s+(\S+)\/.*"
    pattern6=".*-- Info:\s+(\S+)\/.*"
    pattern7=".*ESM\s+(\S+)\s+\$ log get.*"
    for line in b:
        match2=re.search(pattern3,line)
        if match2:
            event_log_enteries_count_cli=match2.group(1)
        match3=re.search(pattern4,line)
        if match3:
            critical_entries_count_cli=match3.group(1)
        match4=re.search(pattern5,line)
        if match4:
            warning_enteries_count_cli=match4.group(1)
        match5=re.search(pattern6,line)
        if match5:
            info_enteries_count_cli=match5.group(1)
    diag_op=run_command(pgdiagcmd)
    common_check_patern_2(diag_op, diagcmdpattern, "command execution successful check", expect=False)
    info_enteries_pattern=".*-- Info:\s+(\S+)\/.*"
    for i in range(1,75):
       pgstatus_op1=run_command(pgstatuscmd)
       a=pgstatus_op1.splitlines()
       mystr = "".join([line.strip('\n') for line in a])
       log.info(mystr)
       match =re.search(info_enteries_pattern,mystr)
       if match:
          log.info("Match Found")
          break
    #event_log_pattern=".Event Log.*:\s+(\S+)\/510 entries.".format(event_log_enteries_count_cli)
    event_log_pattern=".Event Log \(V.11\): {}/510 entries.".format(event_log_enteries_count_cli)
    critical_log_pattern=".-- Critical: {}/{}.".format(critical_entries_count_cli,event_log_enteries_count_cli)
    warning_log_pattern=".-- Warning: {}/{}.".format(warning_enteries_count_cli,event_log_enteries_count_cli)
    info_enteries_pattern=".-- Info: {}/{}.".format(info_enteries_count_cli,event_log_enteries_count_cli)
    common_check_patern_2(mystr,event_log_pattern,"Event log pattern Check_1" , expect=True)
    common_check_patern_2(mystr,critical_log_pattern,"critical_log_pattern Check_1" , expect=True)
    common_check_patern_2(mystr,warning_log_pattern,"warning_log_pattern Check_1" , expect=True)
    common_check_patern_2(mystr,info_enteries_pattern,"info_enteries_pattern Check_1" , expect=True)

def check_logcount_cliwithpage(pageoutput,clioutput):
    pattern1=".Event Log:\s+(\S+)\/510 entries."
    pattern2=".-- Critical:\s+(\S+)\/."
    pattern3=".-- Warning:\s+(\S+)\/."
    pattern4=".-- Info:\s+(\S+)\/."
    a=clioutput.splitlines()
    for line in a:
        match1=re.search(pattern1,line)
        if match1:
            event_log_enteries_count_cli=match1.group(1)
        match2=re.search(pattern2,line)
        if match2:
            critical_entries_count_cli=match2.group(1)
        match3=re.search(pattern3,line)
        if match3:
            warning_enteries_count_cli=match3.group(1)
        match4=re.search(pattern4,line)
        if match4:
            info_enteries_count_cli=match4.group(1)
    event_log_pattern=".Event Log: {}/510 entries.".format(event_log_enteries_count_cli)
    critical_log_pattern=".-- Critical: {}/{}.".format(critical_entries_count_cli,event_log_enteries_count_cli)
    warning_log_pattern=".-- Warning: {}/{}.".format(warning_enteries_count_cli,event_log_enteries_count_cli)
    info_enteries_pattern=".-- Info: {}/{}.".format(info_enteries_count_cli,event_log_enteries_count_cli)
    common_check_patern_2(pageoutput,event_log_pattern,"Event log pattern Check_1" , expect=True)
    common_check_patern_2(pageoutput,critical_log_pattern,"critical_log_pattern Check_1" , expect=True)
    common_check_patern_2(pageoutput,warning_log_pattern,"warning_log_pattern Check_1" , expect=True)
    common_check_patern_2(pageoutput,info_enteries_pattern,"info_enteries_pattern Check_1" , expect=True)

@logThis
def execute_ESM_command(cmd):
    CommonLib.send_command(cmd)

@logThis
def verifyPage0x10And0x17Status(diag_cmd,ses_cmd,pattern,HDD):
    diag_cmd1="{} {}".format(diag_cmd,HDD)
    diag_output = run_command(diag_cmd1)
    page_cmd="{} {}".format(ses_cmd,HDD)
    ses_output=run_command(page_cmd)
    common_check_patern_2(ses_output, pattern, "Output pattern match Check", expect=True)
    pattern = "sg_ses failed: Illegal request"
    for i in range(5):
        ses_output=run_command(page_cmd)
        match=re.search(pattern,ses_output)
        if match:
            log.success("Illegal request Pattern match passed as expected")
            break

@logThis
def verifyPage0x17And0x10Status(diag_cmd,ses_cmd,pattern,HDD):
    diag_cmd1="{} {}".format(diag_cmd,HDD)
    diag_output = run_command(diag_cmd1)
    page_cmd="{} {}".format(ses_cmd,HDD)
    ses_output=run_command(page_cmd)
    common_check_patern_2(ses_output, pattern, "Output pattern match Check", expect=True)
    pattern = "sg_ses failed: Illegal request"
    for i in range(5):
        ses_output=run_command(page_cmd)
        match=re.search(pattern,ses_output)
        if match:
            log.success("Illegal request Pattern match passed as expected")
            break

@logThis
def check_log_filter(diag_cmd,page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(diag_cmd,HDD)
    diag_output = run_command(cmd1)
    truncate= "| cut -c 61-78"
    cmd2 = "{} {} {}".format(page_cmd,HDD,truncate)
    page_output=run_command(cmd2)
    log.info(page_output)
    page_output=page_output.splitlines()
    mystr1 = "".join([line.strip('\n') for line in page_output])
    log.info("to test")
    log.info(mystr1)
    count=0
    output1 = run_command_cli(CLI_cmd)
    log.info(output1)
    for line in output1.splitlines():
        match=re.search(line,mystr1)
        if match:
            log.success("Pattern check passed: {}".format(line))
            count +=1
    if count == 0:
        log.fail("Pattern match failed as expected")
        raise RuntimeError("Pattern match failed")

@logThis
def Check_LED_CLI(diag_cmd,page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(diag_cmd,HDD)
    diag_output = run_command(cmd1)
    truncate= "| cut -c 61-78"
    cmd2 = "{} {} {}".format(page_cmd,HDD,truncate)
    count=0
    for i in range(1,3):
        page_output=run_command(cmd2)
        page_output=page_output.splitlines()
        mystr1 = "".join([line.strip('\n') for line in page_output])
        output1 = run_command_cli(CLI_cmd)
        log.info(mystr1)
        log.info(output1)
        line12=output1.strip().split("\n")[-2]
        pattern1=line12[0]
        log.info(line12)
        line12=line12[0:61]
        match=re.search(line12,mystr1)
        if match:
             log.success("Pattern check passed: {}".format(line12))
             count +=1
             break
    if count == 0:
        log.fail("Pattern match failed")
        raise RuntimeError("Pattern match failed")

@logThis
def checkPageStatus(diag_cmd,page_cmd,HDD):
     cutcmd="|cut -c 61-78"
     pgdiagcmd="{} {}".format(diag_cmd,HDD)
     pgstatuscmd="{} {}{}".format(page_cmd,HDD,cutcmd)
     diagcmdpattern=run_command(pgdiagcmd)
     time.sleep(5)
     pgstatus_op1=run_command(pgstatuscmd)
     a=pgstatus_op1.splitlines()
     output = "".join([line.strip('\n') for line in a])
     diagcmdpattern="error|fail"
     log.info(output)
     pattern1="Event Log: 0/510 entries"
     pattern2="Critical: 0/0"
     pattern3="Warning: 0/0"
     pattern4="Info: 0/0"
     common_check_patern_2(output, pattern1, "Event Log Check", expect=True)
     common_check_patern_2(output, pattern2, "Critical Log Check", expect=True)
     common_check_patern_2(output, pattern3, "Warning Log Check", expect=True)
     common_check_patern_2(output, pattern4, "Info Log Check", expect=True)

@logThis
def CheckCanisterStatus(cmd,HDD,pattern):
   cmd1 = "{} {}".format(cmd,HDD)
   output = run_command(cmd1)
   match=re.search(pattern,output)
   if match:
     log.success("Canister status check successful")
   else:
     log.fail("Canister status check  Failed")
     raise RuntimeError("Pattern match failed")


@logThis
def getFWVersion(device):
    cmd = 'fru get'
    output = run_ESM_command(cmd)
    log.info(output)
    pattern = ".*FW Revision:\s+(\S+).*"
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    match=re.search(pattern,output)
    if match:
        FW_Version=match.group(1)
    else:
        log.info("FW_version is not available")
        raise RuntimeError("FW_version is not available")
    log.info(FW_Version)
    return FW_Version


@logThis
def checkCansiterStatusAndVersion(cmd,HDD,pattern,FW_version):
   cmd1 = "{} {}".format(cmd,HDD)
   output = run_command(cmd1)
   match=re.search(pattern,output)
   if match:
     log.success("Canister status check successful")
   else:
     log.fail("Canister status check  Failed")
     raise RuntimeError("Pattern match failed")
   pattern2=".*CELESTIC\s+TITAN-4U90\s+(\S+).*"
   match2=re.search(pattern2,output)
   if match2:
       ses_version=match2.group(1)
   else:
        log.info("FW_version is not available")
        raise RuntimeError("FW_version is not available")
   log.info("version in ses_page is {}".format(ses_version))
   expect_version = '0' + "".join([i for i in FW_version.strip().split('.')[0:3]])
   log.info("version in CLI is {}".format(expect_version))
   if ses_version == expect_version:
       log.success("FW Version match successful")
   else:
       log.fail("FW Version match fail")
       raise RuntimeError("FW Version match fail")

@logThis
def set_esm_fan_mode_cli_command(device,cmd):
    output = run_command_cli(cmd)
    log.info(output)
    time.sleep(10)
    pattern="Operation success"
    match=re.search(pattern,output)
    if match:
        log.success("Fan mode set successful")
    else:
        log.fail("Fan mode set Fail")
        raise RuntimeError("Fan mode set Fail")

@logThis
def setAndVerifyUW():
    log.info("Inside  UW")
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = run_command_cli(cmd)
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
    modify_value=random.randint(0,int(reading_value)-1)
    clr_cmd="log clear" + "\r"
    run_command_cli(clr_cmd)
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],modify_value,list_threshold[3])  + "\r"
    output2=run_command_cli(cmd2)
    time.sleep(15)
    output3=run_command_cli(cmd)
    log.info(output3)
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
        raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("UW verfication successfull")
    cmd3="log get" + "\r"
    output5=run_command_cli(cmd3)
    output6=output5.splitlines()
    log.info(output5)
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
       raise RuntimeError("Log not updated for UW")
    else:
        log.info("UW verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3])  + "\r"
    output=run_command_cli(cmd2)
    Disconnect()

@logThis
def setAndVerifyUC():
    log.info("Inside  UC")
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = run_command_cli(cmd)
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
    output2=run_command_cli(cmd2)
    time.sleep(15)
    output3=run_command_cli(cmd)
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
        raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("UC verfication successfull")
    cmd3="log get" + "\r"
    output5=run_command_cli(cmd3)
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
       raise RuntimeError("Log not updated for UC")
    else:
        log.info("UC verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3]) + "\r"
    output=run_command_cli(cmd2)
    Disconnect()

@logThis
def setAndVerifyLW():
    log.info("Inside  LW")
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = run_command_cli(cmd)
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
    output2=run_command_cli(cmd2)
    time.sleep(15)
    output3=run_command_cli(cmd)
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
        raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("LW verfication successfull")
    cmd3="log get" + "\r"
    output5=run_command_cli(cmd3)
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
       raise RuntimeError("Log not updated for LW")
    else:
        log.info("LW verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3]) + "\r"
    output=run_command_cli(cmd2)
    Disconnect()

@logThis
def setAndVerifyLC():
    log.info("Inside  LC")
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="temp get" + "\r"
    output = run_command_cli(cmd)
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
    output2=run_command_cli(cmd2)
    time.sleep(15)
    output3=run_command_cli(cmd)
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
        raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("LC verfication successfull")
    cmd3="log get" + "\r"
    output5=run_command_cli(cmd3)
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
       raise RuntimeError("Log not updated for LC")
    else:
        log.info("LC verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3]) + "\r"
    output=run_command_cli(cmd2)
    Disconnect()

@logThis
def CheckCanisterStatus(cmd,HDD,pattern):
   cmd1 = "{} {}".format(cmd,HDD)
   output = run_command(cmd1)
   match=re.search(pattern,output)
   if match:
     log.success("Canister status check successful")
   else:
     log.fail("Canister status check  Failed")
     raise RuntimeError("Pattern match failed")

@logThis
def Verifycanisterdetails(page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(page_cmd,HDD)
    page_output = run_command(cmd1)
    CLI_cmd="fru get\r"
    pattern1="Element 0 descriptor: ESM A"
    pattern2="CAN ASM PN: (\S+)"
    pattern3="CAN ASM SN: (\S+)"
    pattern4="CAN ASM REV: (\S+)"
    pattern5="CPLD 0 Revision Code: (\S+)"
    pattern6="CPLD 1 Revision Code: (\S+)"
    cli_output=run_command_cli(CLI_cmd)
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
    match4=re.search(pattern5,cli_output)
    if match4:
        CPLD_0=match4.group(1)
        CPLD_0=CPLD_0.replace(".","")
        log.info(CPLD_0)
    match5=re.search(pattern6,cli_output)
    if match5:
        CPLD_1=match5.group(1)
        CPLD_1=CPLD_1.replace(".","")
        log.info(CPLD_1)
    pattern_to_check=".*{}.*{}.*{}.*{}.*{}.*{}.*".format(pattern1,ASM_PN,ASM_SN,ASM_REV,CPLD_0,CPLD_1)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,page_output)
    if match:
        log.success("Pattern check got passed as expected")
    else:
        log.fail("Pattern check failed")
        raise RuntimeError("Pattern match failed")

@logThis
def Verifycanisterdetails_titan_g2_wb(page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(page_cmd,HDD)
    page_output = run_command(cmd1)
    pattern1="Element 0 descriptor: ESM A"
    pattern2="CAN ASM PN: (\S+)"
    pattern3="CAN ASM SN: (\S+)"
    pattern4="CAN ASM REV: (\S+)"
    pattern5="CPLD Revision Code: (\S+)"
    pattern6="CPLD 2 Revision Code: (\S+)"
    Disconnect()
    time.sleep(20)
    ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
    ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cli_output=run_ESM_command(CLI_cmd)
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
    match4=re.search(pattern5,cli_output)
    if match4:
        CPLD_0=match4.group(1)
        CPLD_0=CPLD_0.replace(".","")
        log.info(CPLD_0)
    match5=re.search(pattern6,cli_output)
    if match5:
        CPLD_1=match5.group(1)
        CPLD_1=CPLD_1.replace(".","")
        log.info(CPLD_1)
    pattern_to_check=".*{}.*{}.*{}.*{}.*{}.*{}.*".format(pattern1,ASM_PN,ASM_SN,ASM_REV,CPLD_0,CPLD_1)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,page_output)
    if match:
        log.success("Pattern check got passed as expected")
    else:
        log.fail("Pattern check failed")
        raise RuntimeError("Pattern match failed")

@logThis
def verifySesPageLun(ses_cmd,option,pattern,HDD):
    cmd1 = "{} {} {}".format(ses_cmd,HDD,option)
    #page_output = run_command(cmd1)
    CommonLib.execute_check_dict(Const.DUT, cmd1, patterns_dict=pattern)

@logThis
def setvoltageandverifyUW():
    log.info("Inside  UW")
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="power get"
    output = run_ESM_command(cmd)
    output1=output.splitlines()
    count=0
    for line in output1:
        pattern=".*Normal.*"
        match=re.search(pattern,line)
        if match:
            pattern1="^(\S+)\s+(\S+)\s(\S+).*\s(\S+)V.*"
            if ProductTypeInfo == "TITAN-4U90":
                pattern1="^(\S+)\s+(\S+)\s\S+\s(\S+).*\s(\S+)V.*"
            match1=re.search(pattern1,line)
            if match1:
                sensor_ID=match1.group(1)
                sensor_name=match1.group(2)
                sensor_value=match1.group(3)
                read_value=match1.group(4)
                log.info("%s %s %s %s" %(sensor_ID,sensor_name,sensor_value,read_value))
                actual_value=((float(read_value)-float(sensor_value))/float(sensor_value))*100
                if actual_value < 0:
                    log.info("pass")
                    log.info(line)
                    count+=1
                    break
    if count==0:
        log.fail("No Voltage ID available for UW")
        raise RuntimeError("No Voltage ID available for UW")
    clr_cmd="log clear"
    run_ESM_command(clr_cmd)
    cmd1="threshold set {} 3 2 8 10".format(sensor_ID)
    output2=run_ESM_command(cmd1)
    time.sleep(15)
    output3=run_ESM_command(cmd)
    output3=output3.splitlines()
    count=0
    for line in output3:
        pattern="^{}.*Abnormal\s+\[-3%,-2%,\+8%,\+10%\].*".format(sensor_ID)
        match2=re.search(pattern,line)
        if match2:
            log.success("UW check successful")
            count+=1
            break
    if count==0:
        log.fail("UW check not updated")
        raise RuntimeError("UW check not updated")
    cmd3="log get"
    output5=run_ESM_command(cmd3)
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
       raise RuntimeError("Log not updated for UW")
    else:
        log.info("UW verfication in log successfull")
    #Cleanup
    cmd1="threshold set {} 10 8 8 10".format(sensor_ID)
    run_ESM_command(cmd1)
    time.sleep(15)
    Disconnect()

@logThis
def setvoltageandverifyUC():
    log.info("Inside  UC")
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="power get"
    output = run_ESM_command(cmd)
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
                actual_value=((float(read_value)-float(sensor_value))/float(sensor_value))*100
                if actual_value < 0:
                    log.info("pass")
                    log.info(line)
                    count+=1
                    break
    if count==0:
        log.fail("No Voltage ID available for UC")
        raise RuntimeError("No Voltage ID available for UC")
    clr_cmd="log clear"
    run_ESM_command(clr_cmd)
    cmd1="threshold set {} 2 2 8 10".format(sensor_ID)
    output2=run_ESM_command(cmd1)
    time.sleep(15)
    output3=run_ESM_command(cmd)
    output3=output3.splitlines()
    count=0
    for line in output3:
        pattern="^{}.*Abnormal\s+\[-2%,-2%,\+8%,\+10%\].*".format(sensor_ID)
        match2=re.search(pattern,line)
        if match2:
            log.success("UV check successful")
            count+=1
            break
    if count==0:
        log.fail("UV check not updated")
        raise RuntimeError("UV check not updated")
    cmd3="log get"
    output5=run_ESM_command(cmd3)
    output6=output5.splitlines()
    pattern2=".*{} {}.*Vol Failure\s+Assert, UnderThres, c.*".format(sensor_name,sensor_value)
    count2=0
    for line2 in output6:
       match2=re.search(pattern2,line2)
       if match2:
           log.info("Log updated for UV")
           count2+=1
           break
    if count2==0:
       log.info("Log not updated for UV")
       raise RuntimeError("Log not updated for UV")
    else:
        log.info("UW verfication in log successfull")
    #Cleanup
    cmd1="threshold set {} 10 8 8 10".format(sensor_ID)
    run_ESM_command(cmd1)
    time.sleep(15)
    Disconnect()

@logThis
def setvoltageandverifyOW():
    log.info("Inside  OW")
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="power get"
    output = run_ESM_command(cmd)
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
                actual_value=((float(read_value)-float(sensor_value))/float(sensor_value))*100
                if actual_value >= 1:
                    log.info("pass")
                    log.info(line)
                    count+=1
                    break
    if count==0:
        log.fail("No Voltage ID available for OW")
        raise RuntimeError("No Voltage ID available for OW")
    clr_cmd="log clear"
    run_ESM_command(clr_cmd)
    cmd1="threshold set {} 10 8 3 3".format(sensor_ID)
    output2=run_ESM_command(cmd1)
    time.sleep(15)
    output3=run_ESM_command(cmd)
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
        raise RuntimeError("OW check not updated")
    cmd3="log get"
    output5=run_ESM_command(cmd3)
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
       raise RuntimeError("Log not updated for OW")
    else:
        log.info("OW verfication in log successfull")
    #Cleanup
    cmd1="threshold set {} 10 8 8 10".format(sensor_ID)
    run_ESM_command(cmd1)
    time.sleep(15)
    Disconnect()

@logThis
def setvoltageandverifyOC():
    log.info("Inside  OC")
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="power get"
    output = run_ESM_command(cmd)
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
                actual_value=((float(read_value)-float(sensor_value))/float(sensor_value))*100
                if actual_value >= 1:
                    log.info("pass")
                    log.info(line)
                    count+=1
                    break
    if count==0:
        log.fail("No Voltage ID available for OC")
        raise RuntimeError("No Voltage ID available for OC")
    clr_cmd="log clear"
    run_ESM_command(clr_cmd)
    cmd1="threshold set {} 10 8 3 5".format(sensor_ID)
    output2=run_ESM_command(cmd1)
    time.sleep(15)
    output3=run_ESM_command(cmd)
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
        raise RuntimeError("OC check not updated")
    cmd3="log get"
    output5=run_ESM_command(cmd3)
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
       raise RuntimeError("Log not updated for OC")
    else:
        log.info("OC verfication in log successfull")
    #Cleanup
    cmd1="threshold set {} 10 8 8 10".format(sensor_ID)
    run_ESM_command(cmd1)
    time.sleep(15)
    Disconnect()

@logThis
def checkLogWithWrongData(cmd,HDD):
   cmd1 = "{} {}".format(cmd,HDD)
   output = run_command(cmd1)
   pattern="sg_senddiag failed: Illegal request"
   match=re.search(pattern,output)
   if match:
     log.success("Wrong Data check in Log  successful")
   else:
     log.fail("Wrong Data check in Log  Failed")
     raise RuntimeError("Wrong Data check in Log failed")

@logThis
def checkESCEReportBit(cmd,HDD,pattern):
   cmd1 = "{} {}".format(cmd,HDD)
   output = run_command(cmd1)
   common_check_patern_2(output, pattern, "ESCE Report Bit Check", expect=True)

@logThis
def verify_PHY_enable_disable_on_secondaryexpander1():
   log.info("Inside secondary expander1")
   ESMAConnect(ESMA_IP_1,ESMA_port_1)
   cmd="$%^0"
   execute_ESM_command(cmd)
   drv_cmd="drv get"
   disable_cmd="phy disable 30"
   enable_cmd="phy enable 30"
   enable_pattern=".*26\s+Slot027\s+OK.*"
   disable_pattern=".*26\s+Slot027\s+Not Available.*"
   disable_cmd_pattern="PHY 30 disabled"
   enable_cmd_pattern="PHY 30 enabled"
   output=run_command_cli(drv_cmd)
   match=re.search(enable_pattern,output)
   if match:
       log.info("Slot ID 26 is enabled.Verify disable and enable function")
       disable_cmd_output=run_command_cli(disable_cmd)
       common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       time.sleep(20)
       disable_update_output=run_command_cli(drv_cmd)
       common_check_patern_2(disable_update_output,disable_pattern,"PHY Disabled Update check in Slot",expect=True)
       enable_cmd_output=run_command_cli(enable_cmd)
       common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "PHY Enable Check", expect=True)
       time.sleep(60)
       enable_update_output=run_command_cli(drv_cmd)
       common_check_patern_2(enable_update_output,enable_pattern,"PHY Enable Update check in slot",expect=True)
   else :
       log.info("Slot ID 26 is diabled.Verify enable and disable function")
       enable_cmd_output=run_command_cli(enable_cmd)
       common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "PHY Enable Check", expect=True)
       time.sleep(60)
       enable_update_output=run_command_cli(drv_cmd)
       common_check_patern_2(enable_update_output,enable_pattern,"PHY Enable Update check in slot",expect=True)
       disable_cmd_output=run_command_cli(disable_cmd)
       common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       time.sleep(20)
       disable_update_output=run_command_cli(drv_cmd)
       common_check_patern_2(disable_update_output,disable_pattern,"PHY Disabled Update check in Slot",expect=True)
   Disconnect()

@logThis
def verify_PHY_enable_disable_on_secondaryexpander2():
   log.info("Inside seconday expander2")
   ESMAConnect(ESMA_IP_1,ESMA_port_1)
   cmd="$%^2"
   execute_ESM_command(cmd)
   drv_cmd="drv get"
   disable_cmd="phy disable 20"
   enable_cmd="phy enable 20"
   enable_pattern=".*3\s+Slot004\s+OK.*"
   disable_pattern=".*3\s+Slot004\s+Not Available.*"
   disable_cmd_pattern="PHY 20 disabled"
   enable_cmd_pattern="PHY 20 enabled"
   output=run_command_cli(drv_cmd)
   match=re.search(enable_pattern,output)
   if match:
       log.info("Slot ID 3 is enabled.Verify disable and enable function")
       disable_cmd_output=run_command_cli(disable_cmd)
       common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       time.sleep(20)
       disable_update_output=run_command_cli(drv_cmd)
       common_check_patern_2(disable_update_output,disable_pattern,"PHY Disabled Update check in Slot",expect=True)
       enable_cmd_output=run_command_cli(enable_cmd)
       common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "PHY Enable Check", expect=True)
       time.sleep(60)
       enable_update_output=run_command_cli(drv_cmd)
       common_check_patern_2(enable_update_output,enable_pattern,"PHY Enable Update check in slot",expect=True)
   else :
       log.info("Slot ID 3 is diabled.Verify enable and disable function")
       enable_cmd_output=run_command_cli(enable_cmd)
       common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "PHY Enable Check", expect=True)
       time.sleep(60)
       enable_update_output=run_command_cli(drv_cmd)
       common_check_patern_2(enable_update_output,enable_pattern,"PHY Enable Update check in slot",expect=True)
       disable_cmd_output=run_command_cli(disable_cmd)
       common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       time.sleep(20)
       disable_update_output=run_command_cli(drv_cmd)
       common_check_patern_2(disable_update_output,disable_pattern,"PHY Disabled Update check in Slot",expect=True)
   Disconnect()

@logThis
def verifyPHYenable_disableonprimaryexpander():
   log.info("Inside primary expander")
   ESMAConnect(ESMA_IP_1,ESMA_port_1)
   cmd="$%^1"
   execute_ESM_command(cmd)
   phy_info_cmd="phyinfo"
   disable_cmd="phy disable 65"
   enable_cmd="phy enable 65"
   enable_pattern=".*65\s+\w+\s+\w+\s+\w\s+[0-9xa-f]+.*"
   disable_pattern=".*65\s+---+\s+---\s+\w\s+---.*"
   disable_cmd_pattern="PHY 65 disabled"
   enable_cmd_pattern="PHY 65 enabled"
   output=run_command_cli(phy_info_cmd)
   match=re.search(enable_pattern,output)
   if match:
       log.info("PHY ID 65 is enabled.Verify disable and enable function")
       disable_cmd_output=run_command_cli(disable_cmd)
       common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       time.sleep(20)
       disable_update_output=run_command_cli(phy_info_cmd)
       common_check_patern_2(disable_update_output,disable_pattern,"PHY Disabled Update check in Slot",expect=True)
       enable_cmd_output=run_command_cli(enable_cmd)
       common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "PHY Enable Check", expect=True)
       time.sleep(60)
       enable_update_output=run_command_cli(phy_info_cmd)
       common_check_patern_2(enable_update_output,enable_pattern,"PHY Enable Update check in slot",expect=True)
   else :
       log.info("PHY ID 65 is diabled.Verify enable and disable function")
       enable_cmd_output=run_command_cli(enable_cmd)
       common_check_patern_2(enable_cmd_output,enable_cmd_pattern, "PHY Enable Check", expect=True)
       time.sleep(60)
       enable_update_output=run_command_cli(phy_info_cmd)
       common_check_patern_2(enable_update_output,enable_pattern,"PHY Enable Update check in slot",expect=True)
       disable_cmd_output=run_command_cli(disable_cmd)
       common_check_patern_2(disable_cmd_output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       time.sleep(20)
       disable_update_output=run_command_cli(phy_info_cmd)
       common_check_patern_2(disable_update_output,disable_pattern,"PHY Disabled Update check in Slot",expect=True)
   Disconnect()

@logThis
def verifyDriveDiskPowerOn_Off(sec_exp,sec_slot_num,pri_exp,pri_slot_num):
   ESMAConnect(ESMA_IP_1,ESMA_port_1)
   execute_ESM_command(sec_exp)
   drv_cmd="drv get\r"
   off_cmd="drv set {} off\r".format(sec_slot_num)
   on_cmd="drv set {} on\r".format(sec_slot_num)
   sec_on_pattern=".*{}\s+Slot\d+\s+OK.*".format(sec_slot_num)
   sec_off_pattern=".*{}\s+Slot\d+\s+Not Available.*".format(sec_slot_num)
   pri_on_pattern=".*{}\s+Slot\d+\s+OK.*".format(pri_slot_num)
   pri_off_pattern=".*{}\s+Slot\d+\s+Not Available.*".format(pri_slot_num)
   on_off_cmd_pattern="operation done."
   output=run_command_cli(drv_cmd)
   match=re.search(sec_on_pattern,output)
   if match:
       log.info("Slot ID is powereed on .Verify power off function")
       off_cmd_output=run_command_cli(off_cmd)
       common_check_patern_2(off_cmd_output,on_off_cmd_pattern, "Drive Disk Power Off Check", expect=True)
       time.sleep(20)
       off_update_sec=run_command_cli(drv_cmd)
       common_check_patern_2(off_update_sec,sec_off_pattern,"Drive Disk Power Off update check in Slot - secondary",expect=True)
       execute_ESM_command(pri_exp)
       off_update_pri=run_command_cli(drv_cmd)
       common_check_patern_2(off_update_pri,pri_off_pattern,"Drive Disk Power Off update check in Slot - primary",expect=True)
       execute_ESM_command(sec_exp)
       on_cmd_output=run_command_cli(on_cmd)
       common_check_patern_2(on_cmd_output,on_off_cmd_pattern, "Drive Disk Power On Check", expect=True)
       time.sleep(60)
       on_update_sec=run_command_cli(drv_cmd)
       common_check_patern_2(on_update_sec,sec_on_pattern,"Drive Disk Power On update check in slot - secondary",expect=True)
       execute_ESM_command(pri_exp)
       on_update_pri=run_command_cli(drv_cmd)
       common_check_patern_2(on_update_pri,pri_on_pattern,"Drive Disk Power On update check in Slot - primary",expect=True)
   else :
       log.info("Slot ID is powereed off .Verify power on function")
       on_cmd_output=run_command_cli(on_cmd)
       common_check_patern_2(on_cmd_output,on_off_cmd_pattern, "Drive Disk Power On Check", expect=True)
       time.sleep(60)
       on_update_sec=run_command_cli(drv_cmd)
       common_check_patern_2(on_update_sec,sec_on_pattern,"Drive Disk Power On update check in slot - secondary",expect=True)
       execute_ESM_command(pri_exp)
       on_update_pri=run_command_cli(drv_cmd)
       common_check_patern_2(on_update_pri,pri_on_pattern,"Drive Disk Power On update check in Slot - primary",expect=True)
       execute_ESM_command(sec_exp)
       off_cmd_output=run_command_cli(off_cmd)
       common_check_patern_2(off_cmd_output,on_off_cmd_pattern, "Drive Disk Power Off Check", expect=True)
       time.sleep(20)
       off_update_sec=run_command_cli(drv_cmd)
       common_check_patern_2(off_update_sec,sec_off_pattern,"Drive Disk Power Off update check in Slot - secondary",expect=True)
       execute_ESM_command(pri_exp)
       off_update_pri=run_command_cli(drv_cmd)
       common_check_patern_2(off_update_pri,pri_off_pattern,"Drive Disk Power Off update check in Slot - primary",expect=True)
   Disconnect()

@logThis
def execute_in_esm_console_a(cmd):
   ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
   ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
   ESMAConnect(ESMA_IP_1,ESMA_port_1)
   output=run_command_cli("%s \r" %cmd)
   Disconnect()
   return output

@logThis
def execute_in_esm_console_b(cmd):
   ESMB_IP_1 = get_deviceinfo_from_config("UUT","esmbConsoleIP")
   ESMB_port_1 = get_deviceinfo_from_config("UUT","esmbConsolePort")
   ESMBConnect(ESMB_IP_1,ESMB_port_1)
   output=run_command_cli("%s \r" %cmd)
   Disconnect()
   return output

@logThis
def verifyDriveDiskPowerOnOfftitang2wb(sec_exp,sec_slot_num,pri_exp,pri_slot_num):
   ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
   ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
   ESMAConnect(ESMA_IP_1,ESMA_port_1)
   execute_ESM_command(sec_exp + "\r")
   drv_cmd="drv get \r"
   off_cmd="drv set {} off \r".format(sec_slot_num)
   on_cmd="drv set {} on \r".format(sec_slot_num)
   sec_on_pattern="{}\s+Slot {:02d}.*OK".format(sec_slot_num,int(sec_slot_num) + 1)
   sec_off_pattern="{}\s+Slot {:02d}.*Not.*Avaliable".format(sec_slot_num,int(sec_slot_num) + 1)
   pri_on_pattern="{}\s+Slot {:02d}.*OK".format(pri_slot_num,int(pri_slot_num) + 1)
   pri_off_pattern="{}\s+Slot {:02d}.*Not.*Avaliable".format(pri_slot_num,int(pri_slot_num) + 1)
   output=run_command_cli(drv_cmd)
   match=re.search(sec_on_pattern,output)
   if match:
       log.info("Slot ID is powereed on .Verify power off function")
       off_cmd_output=run_command_cli(off_cmd)
       time.sleep(20)
       off_update_sec=run_command_cli(drv_cmd)
       common_check_patern_2(off_update_sec,sec_off_pattern,"Drive Disk Power Off update check in Slot - secondary",expect=True)
       execute_ESM_command(pri_exp + "\r")
       off_update_pri=run_command_cli(drv_cmd)
       common_check_patern_2(off_update_pri,pri_off_pattern,"Drive Disk Power Off update check in Slot - primary",expect=True)
       execute_ESM_command(sec_exp + "\r")
       on_cmd_output=run_command_cli(on_cmd)
       time.sleep(20)
       on_update_sec=run_command_cli(drv_cmd)
       common_check_patern_2(on_update_sec,sec_on_pattern,"Drive Disk Power On update check in slot - secondary",expect=True)
       execute_ESM_command(pri_exp + "\r")
       on_update_pri=run_command_cli(drv_cmd)
       common_check_patern_2(on_update_pri,pri_on_pattern,"Drive Disk Power On update check in Slot - primary",expect=True)
   else :
       log.info("Slot ID is powereed off .Verify power on function")
       on_cmd_output=run_command_cli(on_cmd)
       time.sleep(20)
       on_update_sec=run_command_cli(drv_cmd)
       common_check_patern_2(on_update_sec,sec_on_pattern,"Drive Disk Power On update check in slot - secondary",expect=True)
       execute_ESM_command(pri_exp + "\r")
       on_update_pri=run_command_cli(drv_cmd)
       common_check_patern_2(on_update_pri,pri_on_pattern,"Drive Disk Power On update check in Slot - primary",expect=True)
       execute_ESM_command(sec_exp + "\r")
       off_cmd_output=run_command_cli(off_cmd)
       time.sleep(20)
       off_update_sec=run_command_cli(drv_cmd)
       common_check_patern_2(off_update_sec,sec_off_pattern,"Drive Disk Power Off update check in Slot - secondary",expect=True)
       execute_ESM_command(pri_exp + "\r")
       off_update_pri=run_command_cli(drv_cmd)
       common_check_patern_2(off_update_pri,pri_off_pattern,"Drive Disk Power Off update check in Slot - primary",expect=True)
   Disconnect()



@logThis
def verify_mid_plane_VPD_information(read_cmd,get_cmd,HDD,CLI_output):
    log.info("Inside verify_mid_plane_VPD_information")
    read_cmd1 = "{} {}".format(read_cmd,HDD)
    run_command(read_cmd1)
    truncate= "| cut -c 61-78"
    get_cmd1= "{} {} {}".format(get_cmd,HDD,truncate)
    output=run_command(get_cmd1)
    VPD_output=output.splitlines()
    test_string = "".join([line.strip('\n') for line in VPD_output])
    log.info(test_string)
    log.info(CLI_output)
    pattern1="Midplane Product Name: (\S+)"
    pattern2="Midplane Part Number: (\S+)"
    pattern3="Midplane Serial Number: (\S+)"
    pattern4="Midplane HW EC LVL: (\S+)"
    pattern5="Product Name: (\S+)"
    pattern6="Product Part: (\S+)"
    pattern7="Product Serial Number: (\S+)"
    pattern8="Product Version: (\S+)"
    match1=re.search(pattern1,CLI_output)
    if match1:
        Midplane_Product_Name=match1.group(1)
        log.info(Midplane_Product_Name)
    match2=re.search(pattern2,CLI_output)
    if match2:
        Midplane_Part_Number=match2.group(1)
        log.info(Midplane_Part_Number)
    match3=re.search(pattern3,CLI_output)
    if match3:
        Midplane_Serial_Number=match3.group(1)
        log.info(Midplane_Serial_Number)
    match4=re.search(pattern4,CLI_output)
    if match4:
        Midplane_HW_EC_LVL=match4.group(1)
        log.info(Midplane_HW_EC_LVL)
    match5=re.search(pattern5,CLI_output)
    if match5:
        Product_Name=match5.group(1)
        log.info(Product_Name)
    match6=re.search(pattern6,CLI_output)
    if match6:
        Product_Part=match6.group(1)
        log.info(Product_Part)
    match7=re.search(pattern7,CLI_output)
    if match7:
        Product_Serial_Number=match7.group(1)
        log.info(Product_Serial_Number)
    match8=re.search(pattern8,CLI_output)
    if match8:
        Product_Version=match8.group(1)
        log.info(Product_Version)
    pattern_to_check=".*{}.*{}.*{}.*{}.*{}.*{}.*{}.*{}.*".format(Midplane_Product_Name,Midplane_Part_Number,Midplane_Serial_Number,Midplane_HW_EC_LVL,Product_Name,Product_Part,Product_Serial_Number,Product_Version)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,test_string)
    if match:
        log.success("mid_plane_VPD Pattern check got passed as expected.Match with CLI output success.")
    else:
        log.fail("mid_plane_VPD Pattern check failed")
        raise RuntimeError("mid_plane_VPD Pattern match failed.Does not match with CLI output")

@logThis
def verify_canister_VPD_information(read_cmd,get_cmd,HDD,CLI_output):
    log.info("Inside verify_canister_VPD_information")
    read_cmd1 = "{} {}".format(read_cmd,HDD)
    run_command(read_cmd1)
    truncate= "| cut -c 61-78"
    get_cmd1= "{} {} {}".format(get_cmd,HDD,truncate)
    output=run_command(get_cmd1)
    VPD_output=output.splitlines()
    test_string = "".join([line.strip('\n') for line in VPD_output])
    log.info(test_string)
    log.info(CLI_output)
    pattern=""".*--- ESM A ---.*
.*[General].*
.*Product Name:\s(\S+)\s(\S+).*"""
    match1=re.search(pattern,CLI_output)
    if match1:
        Product_Name_1=match1.group(1)
        Product_Name_2=match1.group(2)
        Product_Name=Product_Name_1+" "+Product_Name_2
        log.info(Product_Name)
    match = test_string.find(Product_Name)
    if match:
        log.info("Product_Name Matches")
    else:
        log.info("canister_VPD Product_Name Match Failed")
        raise RuntimeError("canister_VPD Pattern match failed.Does not match with CLI output")
    pattern2=""".*[Board].*
.*Manufacture Name:.*
.*Part Number: (\S+).*
.*Serial Number: (\S+).*"""
    match2=re.search(pattern2,CLI_output)
    if match2:
        Board_Part_Number=match2.group(1)
        log.info(Board_Part_Number)
        Board_Serial_Number=match2.group(2)
        log.info(Board_Serial_Number)
    match = test_string.find(Board_Part_Number)
    if match:
        log.info("canister_VPD Board_Part_Number Matches")
    else:
        log.info("canister_VPD Board_Part_Number Match Failed")
        raise RuntimeError("canister_VPD Pattern match failed.Does not match with CLI output")
    match = test_string.find(Board_Serial_Number)
    if match:
        log.info("canister_VPD Board_Serial_Number Matches")
    else:
        log.info("canister_VPD Board_Serial_Number Match Failed")
        raise RuntimeError("canister_VPD Pattern match failed.Does not match with CLI output")
    pattern3=""".*[Revision].*
.*FW Revision: (\S+).*
.*FW Revision\(Sec 1\):.*
.*FW Revision\(Sec 2\):.*
.*Built:.*
.*System Configuration Revision:.*
.*CFG Revision: (\S+).*
.*CPLD 0 Revision Code: (\S+).*
.*CPLD 1 Revision Code: (\S+).*
.*HW EC LEVEL: (\s+|\S+)"""
    match3=re.search(pattern3,CLI_output)
    if match3:
        Hardware_EC_Level=match3.group(5)
        log.info(Hardware_EC_Level)
        Firmware_Revision=match3.group(1)
        expect_version = '0' + "".join([i for i in Firmware_Revision.strip().replace('.',' 0')[0:8]])
        log.info(expect_version)
        CPLD_Revision_0=match3.group(3)
        CPLD_Revision_1=match3.group(4)
        CPLD_0=CPLD_Revision_0.replace(".","")
        log.info(CPLD_0)
        CPLD_1=CPLD_Revision_1.replace(".","")
        log.info(CPLD_1)
        Configuration_Revision=match3.group(2)
        log.info(Configuration_Revision)
    common_check_patern_2(test_string,CPLD_0,"canister_VPD CPLD_Revision_0 check",expect=True)
    common_check_patern_2(test_string,CPLD_1,"canister_VPD CPLD_Revision_1 check",expect=True)
    common_check_patern_2(test_string,Configuration_Revision,"canister_VPD Configuration_Revision check",expect=True)
    match = test_string.find(Hardware_EC_Level)
    if match:
        log.info("canister_VPD Hardware_EC_Level Matches")
    else:
        log.info("canister_VPD Hardware_EC_Level Match Failed")
        raise RuntimeError("canister_VPD Pattern match failed.Does not match with CLI output")
    get_cmd= "{} {}".format(get_cmd,HDD)
    output1=run_command(get_cmd)
    a=output1.splitlines()
    for line in a:
       pattern="^ 40     .*"
       match1=re.search(pattern,line)
       if match1:
            match2=re.search(expect_version,line)
            if match2:
                 log.success("canister_VPD Firmware Version check got passed as expected.Match with CLI output success.")
                 break
            else:
                 log.fail("canister_VPD Firmware Version check failed")
                 break

@logThis
def verify_PSU_VPD_information(read_cmd,get_cmd,HDD,CLI_output):
    log.info("Inside verify_PSU_VPD_information")
    read_cmd1 = "{} {}".format(read_cmd,HDD)
    run_command(read_cmd1)
    truncate= "| cut -c 61-78"
    get_cmd1= "{} {} {}".format(get_cmd,HDD,truncate)
    output=run_command(get_cmd1)
    log.info(output)
    VPD_output=output.splitlines()
    test_string = "".join([line.strip('\n') for line in VPD_output])
    log.info(test_string)
    log.info(CLI_output)
    pattern1 =""".*--- PSU 1 ---.*
.*PS Type:.(\S+).*
.*Power Capacity:.(\S+).*
.*PS Manufacturer:.(\S+).*
.*PS Serial Number:.(\S+).*
.*PS Part Number:.(\S+).*
.*PS Firmware Version:.(\S+).*
.*HW EC LEVEL:.(\S+).*"""
    match1=re.search(pattern1,CLI_output)
    if match1:
        Manufacture_Name=match1.group(3)
        Manufacture_PN=match1.group(5)
    log.info(Manufacture_Name)
    log.info(Manufacture_PN)
    pattern_to_check=".*{}.*{}.*".format(Manufacture_Name,Manufacture_PN)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,test_string)
    if match:
        log.success("PSU_VPD Pattern check got passed as expected.Match with CLI output success.")
    else:
        log.fail("PSU_VPD Pattern check failed")
        raise RuntimeError("PSU_VPD Pattern match failed.Does not match with CLI output")



@logThis
def verify_All_VPD_information(read_cmd,get_cmd,HDD,CLI_output):
    log.info("Insde verify_All_VPD_information")
    read_cmd1 = "{} {}".format(read_cmd,HDD)
    run_command(read_cmd1)
    truncate= "| cut -c 61-78"
    get_cmd1= "{} {} {}".format(get_cmd,HDD,truncate)
    output=run_command(get_cmd1)
    log.info(output)
    VPD_output=output.splitlines()
    test_string = "".join([line.strip('\n') for line in VPD_output])
    log.info(test_string)
    log.info(CLI_output)
    log.info("Canister VPD")
    pattern=""".*--- ESM A ---.*
.*[General].*
.*Product Name:\s(\S+)\s(\S+).*"""
    match1=re.search(pattern,CLI_output)
    if match1:
        Product_Name_1=match1.group(1)
        Product_Name_2=match1.group(2)
        Product_Name=Product_Name_1+" "+Product_Name_2
        log.info(Product_Name)
    match = test_string.find(Product_Name)
    if match:
        log.info("Canister VPD Product_Name Matches")
    else:
        log.info("Canister VPD Product_Name Match Failed")
        raise RuntimeError("Canister VPD Pattern match failed.Does not match with CLI output")
    pattern2=""".*[Board].*
.*Manufacture Name:.*
.*Part Number: (\S+).*
.*Serial Number: (\S+).*"""
    match2=re.search(pattern2,CLI_output)
    if match2:
        Board_Part_Number=match2.group(1)
        log.info(Board_Part_Number)
        Board_Serial_Number=match2.group(2)
        log.info(Board_Serial_Number)
    match = test_string.find(Board_Part_Number)
    if match:
        log.info("Canister VPD Board_Part_Number Matches")
    else:
        log.info("Canister VPD Board_Part_Number Match Failed")
        raise RuntimeError("Canister VPD Pattern match failed.Does not match with CLI output")
    match = test_string.find(Board_Serial_Number)
    if match:
        log.info("Canister VPD Board_Serial_Number Matches")
    else:
        log.info("Canister VPD Board_Serial_Number Match Failed")
        raise RuntimeError("Canister VPD Pattern match failed.Does not match with CLI output")
    pattern3=""".*[Revision].*
.*FW Revision: (\S+).*
.*FW Revision\(Sec 1\):.*
.*FW Revision\(Sec 2\):.*
.*Built:.*
.*System Configuration Revision:.*
.*CFG Revision: (\S+).*
.*CPLD 0 Revision Code: (\S+).*
.*CPLD 1 Revision Code: (\S+).*
.*HW EC LEVEL: (\s+|\S+)"""
    match3=re.search(pattern3,CLI_output)
    if match3:
        Hardware_EC_Level=match3.group(5)
        log.info(Hardware_EC_Level)
        Firmware_Revision=match3.group(1)
        expect_version = '0' + "".join([i for i in Firmware_Revision.strip().replace('.',' 0')[0:8]])
        log.info(expect_version)
        CPLD_Revision_0=match3.group(3)
        CPLD_Revision_1=match3.group(4)
        CPLD_0=CPLD_Revision_0.replace(".","")
        log.info(CPLD_0)
        CPLD_1=CPLD_Revision_1.replace(".","")
        log.info(CPLD_1)
        Configuration_Revision=match3.group(2)
        log.info(Configuration_Revision)
    common_check_patern_2(test_string,CPLD_0,"Canister VPD CPLD_Revision_0 check",expect=True)
    common_check_patern_2(test_string,CPLD_1,"Canister VPD CPLD_Revision_1 check",expect=True)
    common_check_patern_2(test_string,Configuration_Revision,"Canister VPD Configuration_Revision check",expect=True)
    match = test_string.find(Hardware_EC_Level)
    if match:
        log.info("Canister VPD Hardware_EC_Level Matches")
    else:
        log.info("Canister VPD Hardware_EC_Level Match Failed")
        raise RuntimeError("Canister VPD Pattern match failed.Does not match with CLI output")
    get_cmd= "{} {}".format(get_cmd,HDD)
    output1=run_command(get_cmd)
    a=output1.splitlines()
    for line in a:
       pattern="^ 40     .*"
       match1=re.search(pattern,line)
       if match1:
            match2=re.search(expect_version,line)
            if match2:
                 log.success("Canister VPD Firmware Version check got passed as expected.Match with CLI output success.")
                 break
            else:
                 log.fail("Canister VPD Firmware Version check failed")
                 break
    log.info("MidPlane VPD")
    pattern1="Midplane Product Name: (\S+)"
    pattern2="Midplane Part Number: (\S+)"
    pattern3="Midplane Serial Number: (\S+)"
    pattern4="Midplane HW EC LVL: (\S+)"
    pattern5="Product Name: (\S+)"
    pattern6="Product Part: (\S+)"
    pattern7="Product Serial Number: (\S+)"
    pattern8="Product Version: (\S+)"
    match1=re.search(pattern1,CLI_output)
    if match1:
        Midplane_Product_Name=match1.group(1)
        log.info(Midplane_Product_Name)
    match2=re.search(pattern2,CLI_output)
    if match2:
        Midplane_Part_Number=match2.group(1)
        log.info(Midplane_Part_Number)
    match3=re.search(pattern3,CLI_output)
    if match3:
        Midplane_Serial_Number=match3.group(1)
        log.info(Midplane_Serial_Number)
    match4=re.search(pattern4,CLI_output)
    if match4:
        Midplane_HW_EC_LVL=match4.group(1)
        log.info(Midplane_HW_EC_LVL)
    match5=re.search(pattern5,CLI_output)
    if match5:
        Product_Name=match5.group(1)
        log.info(Product_Name)
    match6=re.search(pattern6,CLI_output)
    if match6:
        Product_Part=match6.group(1)
        log.info(Product_Part)
    match7=re.search(pattern7,CLI_output)
    if match7:
        Product_Serial_Number=match7.group(1)
        log.info(Product_Serial_Number)
    match8=re.search(pattern8,CLI_output)
    if match8:
        Product_Version=match8.group(1)
        log.info(Product_Version)
    pattern_to_check=".*{}.*{}.*{}.*{}.*{}.*{}.*{}.*{}.*".format(Midplane_Product_Name,Midplane_Part_Number,Midplane_Serial_Number,Midplane_HW_EC_LVL,Product_Name,Product_Part,Product_Serial_Number,Product_Version)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,test_string)
    if match:
        log.success("MidPlane VPD Pattern check got passed as expected.Match with CLI output success.")
    else:
        log.fail("MidPlane VPD Pattern check failed")
        raise RuntimeError("MidPlane VPD Pattern match failed.Does not match with CLI output")
    log.info("PSU 1 VPD")
    pattern1 =""".*--- PSU 1 ---.*
.*PS Type:.(\S+).*
.*Power Capacity:.(\S+).*
.*PS Manufacturer:.(\S+).*
.*PS Serial Number:.(\S+).*
.*PS Part Number:.(\S+).*
.*PS Firmware Version:.(\S+).*
.*HW EC LEVEL:.(\S+).*"""
    match1=re.search(pattern1,CLI_output)
    if match1:
        Manufacture_Name=match1.group(3)
        Manufacture_PN=match1.group(5)
        PS_Serial_Number=match1.group(4)
        HW_EC_LEVEL=match1.group(7)
        PS_Firmware_Version=match1.group(6)
    log.info(Manufacture_Name)
    log.info(Manufacture_PN)
    log.info(PS_Serial_Number)
    log.info(HW_EC_LEVEL)
    log.info(PS_Firmware_Version)
    pattern_to_check=".*{}.*{}.*{}.*{}.*{}.*".format(Manufacture_Name,Manufacture_PN,PS_Serial_Number,HW_EC_LEVEL,PS_Firmware_Version)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,test_string)
    if match:
        log.success("PSU 1 Pattern check got passed as expected.Match with CLI output success.")
    else:
        log.fail("PSU 1 Pattern check failed")
        raise RuntimeError("PSU 1 Pattern match failed.Does not match with CLI output")
    log.info("PSU 4 VPD")
    pattern1 =""".*--- PSU 4 ---.*
.*PS Type:.(\S+).*
.*Power Capacity:.(\S+).*
.*PS Manufacturer:.(\S+).*
.*PS Serial Number:.(\S+).*
.*PS Part Number:.(\S+).*
.*PS Firmware Version:.(\S+).*
.*HW EC LEVEL:.(\S+).*"""
    match1=re.search(pattern1,CLI_output)
    if match1:
        Manufacture_Name=match1.group(3)
        Manufacture_PN=match1.group(5)
        PS_Serial_Number=match1.group(4)
        HW_EC_LEVEL=match1.group(7)
        PS_Firmware_Version=match1.group(6)
    log.info(Manufacture_Name)
    log.info(Manufacture_PN)
    log.info(PS_Serial_Number)
    log.info(HW_EC_LEVEL)
    log.info(PS_Firmware_Version)
    pattern_to_check=".*{}.*{}.*{}.*{}.*{}.*".format(Manufacture_Name,Manufacture_PN,PS_Serial_Number,HW_EC_LEVEL,PS_Firmware_Version)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,test_string)
    if match:
        log.success("PSU 4 Pattern check got passed as expected.Match with CLI output success.")
    else:
        log.fail("PSU 4 Pattern check failed")
        raise RuntimeError("PSU 4 Pattern match failed.Does not match with CLI output")

@logThis
def checkLEDStatus(get_page_cmd, LED1, LED2, LED3, get_LED, LED4, LED_pattern, HDDs):
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType") 
    if ProductTypeInfo == "CELESTIC  P2523":
        log.debug(f"Platform type :{ProductTypeInfo}")
        cmd="{} {} {} {}{}{} {} {}{}{}{}".format(get_page_cmd,HDDs,LED1,"\"",LED2,"\"",LED3,"\"",get_LED,"\"",LED4)
        log.info(cmd)
        pattern= r'^{}$'.format(LED_pattern)
        output=run_command(cmd)
        log.info(output)
        output1=output.splitlines()
        for line in output1:
           match = re.search(pattern, line)
           if match:
              log.success('LED status check Success')
              return
        raise RuntimeError("LED status check failed")
    else:
        for HDD in HDDs:
           cmd="{} {} {} {}{}{} {} {}{}{}{}".format(get_page_cmd,HDD,LED1,"\"",LED2,"\"",LED3,"\"",get_LED,"\"",LED4)
           log.info(cmd)
           pattern= r'^{}$'.format(LED_pattern)
           output=run_command(cmd)
           log.info(output)
           output1=output.splitlines()
           for line in output1:
              match = re.search(pattern, line)
              if match:
                 log.success('LED status check Success')
                 return
           raise RuntimeError("LED status check failed")

@logThis
def checkEnclosureLEDStatus(pg_cmd, get_pg_cmd, HDD, LED_1, encl_LED, LED_4, LED_5, ident_LED, pattern):
    cmd="{} {}".format(pg_cmd,HDD)
    output=run_command(cmd)
    pattern= r'^{}$'.format(pattern)
    output1=output.splitlines()
    count=0
    for line in output1:
       match = re.search(pattern, line)
       if match:
              log.success('enclosure ident bit check Success')
              count+=1
              break
    if count == 0:
       raise RuntimeError("enclosure ident bit check failed")
    cmd="{} {} {} {}{}{} {} {}{}{}{}".format(get_pg_cmd,HDD,LED_1,"\"",encl_LED,"\"",LED_5,"\"",ident_LED,"\"",LED_4)
    output=run_command(cmd)
    pattern= r'^{}$'.format(pattern)
    output1=output.splitlines()
    count=0
    for line in output1:
       match = re.search(pattern, line)
       if match:
              log.success('enclosure ident bit check Success')
              count+=1
              break
    if count == 0:
       raise RuntimeError("enclosure ident bit check failed")

@logThis
def checkCanisterLEDStatus(get_cmd1,get_cmd2,page_cmd,HDD,LED_1,LED_6,LED_7,ident_LED,LED_4,pattern,total_pattern):
    cmd="{} {}".format(get_cmd1,HDD)
    output=run_command(cmd)
    pattern= r'^{}$'.format(pattern)
    output1=output.splitlines()
    count=0
    for line in output1:
       match = re.search(pattern, line)
       if match:
              log.success('canister bit check Success')
              count+=1
              break
    if count == 0:
       raise RuntimeError("canister bit check failed")
    cmd="{} {}".format(get_cmd2,HDD)
    output=run_command(cmd)
    output1=output.splitlines()
    count=0
    for line in output1:
       match = re.search(pattern, line)
       if match:
              log.success('canister bit check Success')
              count+=1
              break
    if count == 0:
       raise RuntimeError("canister bit check failed")
    cmd="{} {} {} {}{}{} {} {}{}{}{}".format(page_cmd,HDD,LED_1,"\"",LED_6,"\"",LED_7,"\"",ident_LED,"\"",LED_4)
    log.info(cmd)
    pattern= r'^{}$'.format(total_pattern)
    output=run_command(cmd)
    output1=output.splitlines()
    count=0
    for line in output1:
       match = re.search(pattern, line)
       if match:
              log.success('canister bit check Success')
              count+=1
              break
    if count == 0:
       raise RuntimeError("canister bit check failed")

@logThis
def checkProductAssetTagWriteReadWithCorrectByteLength(write_cmd, read_cmd, pattern, HDD):
    write_cmd="{} {}".format(write_cmd,HDD)
    run_command(write_cmd)
    read_cmd="{} {}".format(read_cmd,HDD)
    run_command(read_cmd)
 #   log.info(output)
    page_cmd="sg_ses -p 0x12"
    page_cmd="{} {}".format(page_cmd,HDD)
    CommonLib.execute_check_dict(Const.DUT, page_cmd, patterns_dict=pattern)

@logThis
def checkProductAssetTagWriteReadWithInCorrectByteLength(write_cmd, pattern, HDD):
    write_cmd="{} {}".format(write_cmd,HDD)
    output=run_command(write_cmd)
    common_check_patern_2(output,pattern,"Product Asset Tag with Incorrect length Failure",expect=True)

@logThis
def VerifyEnclosureInventorydetails(page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(page_cmd,HDD)
    page_output = run_command(cmd1)
    pattern1="Element 0 descriptor: Enclosure"
    pattern2="Assembly PN: (\S+)"
    pattern3="Assembly SN: (\S+)"
    pattern4="Assembly Rev: (\S+)"
    cli_output=run_command_cli(CLI_cmd)
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
def VerifyEnclosureInventorydetails_titan_g2_wb(page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(page_cmd,HDD)
    page_output = run_command(cmd1)
    pattern1="Element 0 descriptor: Enclosure"
    pattern2="Assembly PN: (\S+)"
    pattern3="Assembly SN: (\S+)"
    pattern4="Assembly Rev: (\S+)"
    ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
    ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
    WhiteboxLibAdapter.OSDisconnect()
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cli_output=run_ESM_command(CLI_cmd)
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
def VerifyIPconfig():
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="ipconfig"
    output = run_command_cli(cmd)
    pattern="DHCP           : (ON|OFF).*"
    pattern1="Local IP       : ((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|0[0-9][0-9]|00[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|0[0-9][0-9]|00[0-9]).*"
    pattern2="Net Mask       : ((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|0[0-9][0-9]|00[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|0[0-9][0-9]|00[0-9]).*"
    pattern3="Default Gateway: ((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|0[0-9][0-9]|00[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|0[0-9][0-9]|00[0-9]).*"
    pattern4="MAC Address    : (([0-9a-fA-F]){2}\-){5}([0-9a-fA-F]){2}.*"
    match=re.search(pattern,output)
    if match:
        log.success("DHCP status validation passed")
    else:
        log.fail("DHCP status validation failed")
        raise RuntimeError("DHCL status validation failed")
    match=re.search(pattern1,output)
    if match:
        log.success("Local IP validation passed")
    else:
        log.fail("Local IP validation failed")
        raise RuntimeError("Local IP validation failed")
    match=re.search(pattern2,output)
    if match:
        log.success("Net mask validation passed")
    else:
        log.fail("Net mask validation failed")
        raise RuntimeError("Net mask validation failed")
    match=re.search(pattern3,output)
    if match:
        log.success("Default gateway validation passed")
    else:
        log.fail("Default gateway validation failed")
        raise RuntimeError("default gateway validation failed")
    match=re.search(pattern4,output)
    if match:
        log.success("MAC address validation passed")
    else:
        log.fail("MAC address validation failed")
        raise RuntimeError("MAC address validation failed")
    Disconnect()

@logThis
def getNumberOfDrives():
     cmd="lsscsi -g | grep -i disk  | wc -l"
     output=run_command(cmd)
     output=output.splitlines()[-2]
     log.info(output)
     return output

@logThis
def verifyDateModification(set_cmd,pattern,DUT):
    run_command_cli(set_cmd)
    reset_cmd="reset 0"
    execute_ESM_command(reset_cmd)
    time.sleep(120)
    Disconnect()
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
#    run_command_cli(Enter)
#    run_command_cli(Enter)
    output_cmd = "fru get"
    CLI_output= run_command_cli(output_cmd)
    common_check_patern_2(CLI_output, pattern, "Verify manufacturer date Check", expect=True)


@logThis
def verifyDateModification_titan_g2_wb(set_cmd,pattern,DUT):
    run_ESM_command(set_cmd)
    reset_cmd="reset 0"
    execute_ESM_command(reset_cmd)
    time.sleep(120)
    output_cmd = "fru get"
    CLI_output= run_ESM_command(output_cmd)
    common_check_patern_2(CLI_output, pattern, "Verify manufacturer date Check", expect=True)


@logThis
def checkDriveDiskPower(set_cmd,get_cmd,HDD1,HDD2,drive_num,device_pattern):
   cmd1="sg_ses -p 2  --index=arr,0"
   cmd1="{} {}".format(cmd1,HDD1)
   output=run_command(cmd1)
   pattern="pattern=.*Element 0 descriptor:\n.*status: Unsupported.*"
   match=re.search(pattern,output)
   if match:
       temp=HDD1
       HDD1=HDD2
       HDD2=temp
   set_cmd="{} {}".format(set_cmd,HDD1)
   run_command(set_cmd)
   get_cmd_0_29="{}{} {}".format(get_cmd,"0-29",HDD1)
   get_cmd_60_66="{}{} {}".format(get_cmd,"60-66",HDD1)
   get_cmd_30_59="{}{} {}".format(get_cmd,"30-59",HDD2)
   get_cmd_67_74="{}{} {}".format(get_cmd,"67-74",HDD2)
   get_0_29_HDD1_output=run_command(get_cmd_0_29)
   log.info(get_0_29_HDD1_output)
   get_60_66_HDD1_output=run_command(get_cmd_60_66)
   log.info(get_60_66_HDD1_output)
   get_30_59_HDD2_output=run_command(get_cmd_30_59)
   log.info(get_30_59_HDD2_output)
   get_67_74_HDD2_output=run_command(get_cmd_67_74)
   log.info(get_67_74_HDD2_output)
   if int(drive_num) <= 60 :
       log.info("Drive num less than 60")
       common_check_patern_2(get_0_29_HDD1_output, device_pattern, "Device off check_0_29", expect=False)
       common_check_patern_2(get_30_59_HDD2_output, device_pattern, "Device off check_30_59", expect=False)
   else:
       log.info("Drive num greater than 60")
       common_check_patern_2(get_0_29_HDD1_output, device_pattern, "Device off check_0_29", expect=False)
       common_check_patern_2(get_60_66_HDD1_output, device_pattern, "Device off check_60_66", expect=False)
       common_check_patern_2(get_30_59_HDD2_output, device_pattern, "Device off check_30_59", expect=False)
       common_check_patern_2(get_67_74_HDD2_output, device_pattern, "Device off check_67_74", expect=False)

@logThis
def ModifyFanSerialAndHWECNumber():
   ESMAConnect(ESMA_IP_1,ESMA_port_1)
   mod_Ser_num="F1015CTH209TJ16N"
   mod_HW_num="05"
   cmd1="fru set -f"
   run_command_cli = partial(CommonLib.run_command, deviceObj=device, prompt='New:')
   run_command_cli(cmd1)
   run_command_cli(mod_Ser_num)
   run_command_cli(mod_HW_num)
   run_command_cli("exit")
   run_command_cli(mod_Ser_num)
   run_command_cli(mod_HW_num)
   run_command_cli("exit")
   run_command_cli(mod_Ser_num)
   run_command_cli(mod_HW_num)
   run_command_cli("exit")
   run_command_cli(mod_Ser_num)
   run_command_cli(mod_HW_num)
   run_command_cli("exit")
   run_command_cli(mod_Ser_num)
   run_command_cli(mod_HW_num)
   run_command_cli = partial(CommonLib.run_command, deviceObj=device, prompt='ESM\s\S\s\$')
   run_command_cli("exit")
   cmd="fru get"
   output=run_command_cli(cmd)
   log.info(output)
   ser_num_pattern="Fan Serial Number: F1015CTH209TJ16N"
   HW_num_pattern="HW EC LEVEL: 05"
   ser_num_count=0
   HW_num_count=0
   output1=output.splitlines()
   for line in output1:
       match_ser_num=re.search(ser_num_pattern,line)
       match_HW_num=re.search(HW_num_pattern,line)
       if match_ser_num:
           ser_num_count=ser_num_count+1
       if match_HW_num:
           HW_num_count=HW_num_count+1
   if ser_num_count == 5:
       log.info("Fan Serial Number updated in all modules")
   else:
       log.info("Fan Serial Number is not updated in all modules")
       raise RuntimeError("Fan Serial Number is not updated in all modules")
   if HW_num_count == 5:
       log.info("HW EC Level  updated in all modules")
   else:
       log.info("HW EC Level is not updated in all modules")
       raise RuntimeError("HW EC Level is not updated in all modules")
   Disconnect()

@logThis
def ModifyFanSerialAndHWECNumber_titan_g2_wb():
   num1="F1015CTH209TJ16N"
   num2="05"
   if getFWVersion("DUT") >= "2.1.4.31":
       num1="05"
       num2="F1015CTH209TJ16N"
   cmd1="fru set -f"
   run_command_cli(cmd1 + '\r', prompt='New:')
   run_command_cli(num1 + '\r', prompt='New:')
   run_command_cli(num2 + '\r', prompt='New:')
   run_command_cli(num1 + '\r', prompt='New:')
   run_command_cli(num2 + '\r', prompt='New:')
   run_command_cli(num1 + '\r', prompt='New:')
   run_command_cli(num2 + '\r', prompt='New:')
   run_command_cli(num1 + '\r', prompt='New:')
   run_command_cli(num2 + '\r', prompt='New:')
   run_command_cli(num1 + '\r', prompt='New:')
   run_command_cli(num2 + '\r', prompt='ESM\s\S\s.*=\>')
   cmd="fru get"
   output=run_command_cli(cmd + '\r', prompt='ESM\s\S\s.*=\>')
   log.info(output)
   ser_num_pattern="F1015CTH209TJ16N"
   HW_num_pattern="05"
   ser_num_count=0
   HW_num_count=0
   output1=output.splitlines()
   for line in output1:
       match_ser_num=re.search(ser_num_pattern,line)
       match_HW_num=re.search(HW_num_pattern,line)
       if match_ser_num:
           ser_num_count=ser_num_count+1
       if match_HW_num:
           HW_num_count=HW_num_count+1
   if ser_num_count == 5:
       log.info("Fan Serial Number updated in all modules")
   else:
       log.info("Fan Serial Number is not updated in all modules")
       raise RuntimeError("Fan Serial Number is not updated in all modules")
   if HW_num_count == 5:
       log.info("HW EC Level  updated in all modules")
   else:
       log.info("HW EC Level is not updated in all modules")
       raise RuntimeError("HW EC Level is not updated in all modules")

@logThis
def checklocalexpanderreset(reset_cmd,HDD):
    reset_cmd="{} {}".format(reset_cmd,HDD)
    output=run_command(reset_cmd)
    pattern="sg_senddiag failed:"
    pattern1="DID_SOFT_ERROR"
    pattern2="DID_NO_CONNECT"
    common_check_patern_2(output,pattern,"Local expander reset diag command check",expect=False)
    common_check_patern_2(output,pattern1,"Local expander reset diag command check",expect=False)
    common_check_patern_2(output,pattern2,"Local expander reset diag command check",expect=False)
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")
        ESMAConnect(ESMA_IP_1,ESMA_port_1)
        Expected_pattern="Enter Shared Mode"
        Expected_pattern2="Done: System POST Passed"
        Expected_pattern3="Done: Compatibility Check Passed"
        output1=device.readUntil(Expected_pattern,180)
        common_check_patern_2(output1,Expected_pattern,"Local expander reset check",expect=True)
        common_check_patern_2(output1,Expected_pattern2,"Local expander reset check",expect=True)
        common_check_patern_2(output1,Expected_pattern3,"Local expander reset check",expect=True)
    else:
       ESMAConnect(ESMA_IP_1,ESMA_port_1)
       Expected_pattern="Done Logical Route Table Dump"
       Expected_pattern2="Start Logical Route Table Dump"
       Expected_pattern3="Max route index"
       Expected_pattern4="Link list length"
       output1=device.readUntil(Expected_pattern,180)
       common_check_patern_2(output1,Expected_pattern,"Local expander reset check",expect=True)
       common_check_patern_2(output1,Expected_pattern2,"Local expander reset check",expect=True)
       common_check_patern_2(output1,Expected_pattern3,"Local expander reset check",expect=True)
       common_check_patern_2(output1,Expected_pattern4,"Local expander reset check",expect=True)
    Disconnect()
    time.sleep(20)

@logThis
def checklocalexpanderresetB(reset_cmd,HDD):
    reset_cmd="{} {}".format(reset_cmd,HDD)
    output=run_command(reset_cmd)
    pattern="sg_senddiag failed:"
    pattern1="DID_SOFT_ERROR"
    pattern2="DID_NO_CONNECT"
    common_check_patern_2(output,pattern,"Local expander reset diag command check",expect=False)
    common_check_patern_2(output,pattern1,"Local expander reset diag command check",expect=False)
    common_check_patern_2(output,pattern2,"Local expander reset diag command check",expect=False)
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMB_IP_1 = get_deviceinfo_from_config("UUT","esmbConsoleIP")
        ESMB_port_1 = get_deviceinfo_from_config("UUT","esmbConsolePort")
        ESMAConnect(ESMB_IP_1,ESMB_port_1)
        Expected_pattern="Enter Shared Mode"
        Expected_pattern2="Done: System POST Passed"
        Expected_pattern3="Done: Compatibility Check Passed"
        output1=device.readUntil(Expected_pattern,180)
        common_check_patern_2(output1,Expected_pattern,"Local expander reset check",expect=True)
        common_check_patern_2(output1,Expected_pattern2,"Local expander reset check",expect=True)
        common_check_patern_2(output1,Expected_pattern3,"Local expander reset check",expect=True)
    Disconnect()

@logThis
def checkEnterSingleModePrint(reset_cmd,HDD):
    reset_cmd="{} {}".format(reset_cmd,HDD)
    output=run_command(reset_cmd)
    pattern="sg_senddiag failed:"
    pattern1="DID_SOFT_ERROR"
    pattern2="DID_NO_CONNECT"
    common_check_patern_2(output,pattern,"Local expander reset diag command check",expect=False)
    common_check_patern_2(output,pattern1,"Local expander reset diag command check",expect=False)
    common_check_patern_2(output,pattern2,"Local expander reset diag command check",expect=False)
    ESMAConnect(ESMA_IP_1,ESMA_port_1)
    expect_prompt="Enter Single Mode"
    output=device.readUntil(expect_prompt)
    pattern=".*ESM A \$ Enter Single Mode.*"
    common_check_patern_2(output,pattern,"Enter Single Mode print check",expect=True)
    Disconnect()

@logThis
def checkSMPPhyEnableDisable(expander):
   smp_discover_cmd="{}{}".format("smp_discover ",expander)
   output=run_command(smp_discover_cmd)
   pattern=".*phy\s+(\S+)\:\S\:attached.*"
   count=0
   output=output.splitlines()
   for line in output:
      match=re.search(pattern,line)
      if match:
          attached_phy=match.group(1)
          count+=1
          break
   if count==0:
       log.info("No attached phy found")
       raise RuntimeError("All vacant phy.Cant verify phy disable")
   phy_disable_cmd="smp_phy_control {} -p {} -o 3".format(expander,attached_phy)
   run_command(phy_disable_cmd)
   disable_check_output=run_command(smp_discover_cmd)
   disable_pattern=".*phy\s+{}\:\S\:disabled".format(attached_phy)
   common_check_patern_2(disable_check_output,disable_pattern,"phy disable check",expect=True)
   phy_enable_cmd="smp_phy_control {} -p {} -o 2".format(expander,attached_phy)
   run_command(phy_enable_cmd)
   time.sleep(10)
   enable_check_output=run_command(smp_discover_cmd)
   log.info(enable_check_output)
   enable_pattern=".*phy\s+{}\:\S\:attached".format(attached_phy)
   common_check_patern_2(enable_check_output,enable_pattern,"phy enable check",expect=True)

@logThis
def queryExpanders(index='0'):
  cmd="ls /dev/bsg/expander-%s\:*" %index
  p_device = "(/dev/bsg/expander\-%s\:\d+).*" %index
  output = run_command(cmd)
  error_msg = "Didn't find available expander."
  device_list = find_matches(p_device, output, error_msg)
  return device_list

@logThis
def checkSMPPhyLinkSpeed(expander,min_rate='9'):
   smp_discover_cmd="{}{}".format("smp_discover ",expander)
   output=run_command(smp_discover_cmd)
   pattern=".*phy\s+(\S+)\:\S\:attached.*12 Gbps.*"
   count=0
   output=output.splitlines()
   for line in output:
      match=re.search(pattern,line)
      if match:
          attached_phy=match.group(1)
          count+=1
          speed_pattern="12 Gbps"
          check_msg="link spped 12 GBPS check for Phys {}".format(attached_phy)
          common_check_patern_2(line,speed_pattern,check_msg,expect=True)
   if count==0:
       log.info("No attached phy found")
       raise RuntimeError("All vacant phy.Cant verify 12 GBPS link speed")
   pattern=".*phy\s+(\S+)\:U\:attached.*"
   for line in output:
      match=re.search(pattern,line)
      if match:
          attached_phy=match.group(1)
          break
   smp_discover_pg_cmd="{}{} -p {}".format("smp_discover ",expander,attached_phy)
   discover_output=run_command(smp_discover_pg_cmd)
   pattern="negotiated logical link rate\: phy enabled\, 12 Gbps"
   pattern1="negotiated physical link rate\: phy enabled\, 12 Gbps"
   common_check_patern_2(discover_output,pattern,"negotiated logical link rate check",expect=True)
   common_check_patern_2(discover_output,pattern1,"negotiated physical link rate check",expect=True)
   phy_control_cmd="smp_phy_control {} -p {} -M 10 -m {} -o 1".format(expander,attached_phy,min_rate)
   output=run_command(phy_control_cmd)
   time.sleep(5)
   updated_discover_output=run_command(smp_discover_pg_cmd)
   restore_cmd="smp_phy_control {} -p {} -M 11 -m {} -o 1".format(expander,attached_phy,min_rate)
   run_command(restore_cmd)
   pattern1="negotiated logical link rate\: phy enabled\, 6 Gbps"
   pattern2="programmed minimum physical link rate\: [36] Gbps"
   pattern3="programmed maximum physical link rate\: 6 Gbps"
   pattern4="negotiated physical link rate\: phy enabled\, 6 Gbps"
   common_check_patern_2(updated_discover_output,pattern1,"negotiated logical link rate check",expect=True)
   common_check_patern_2(updated_discover_output,pattern2,"programmed minimum physical link rate check",expect=True)
   common_check_patern_2(updated_discover_output,pattern3,"programmed maximum physical link rate",expect=True)
   common_check_patern_2(updated_discover_output,pattern4,"negotiated physical link rate check",expect=True)


@logThis
def checkIPConfiguration(diag_cmd,pg_cmd,HDD,pattern):
  diag_cmd="{} {}".format(diag_cmd,HDD)
  output=run_command(diag_cmd)
  pattern1="sg_senddiag failed:"
  common_check_patern_2(output,pattern1,"Diag_cmd_verififcation",expect=False)
  time.sleep(60)
  pg_cmd="{} {} {}".format(pg_cmd,HDD,"-H")
  output=run_command(pg_cmd)
  CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=pattern,check_output=output)

@logThis
def verifyCLISetGetCLICommand():
  ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
  if ProductTypeInfo == "TITAN G2-4U90" or ProductTypeInfo == "LENOVO" or ProductTypeInfo == "TITAN-4U90":
        ESMA_IP_1 = get_deviceinfo_from_config("UUT","consoleIP")
        ESMA_port_1 = get_deviceinfo_from_config("UUT","consolePort")

  ESMAConnect(ESMA_IP_1,ESMA_port_1)
  cmd_list = [ 'about', 'esm get', 'drv get','help','fan get','fan set -m e','fan set -p 35','fan set -l 1','fru get','log get','port get','power get','temp get','threshold get','debug on','errlog get','checklist get','mode get']
  err_count = 0
  fail_info_list = ['command not found', 'No such file or directory', 'cannot read file', 'Unknown command', 'not found', 'no space left on device', 'Command exited with non-zero status',"ERROR","Failure", "No such file","fail","CLI_UNKNOWN_CMD"]
  for cmd in cmd_list:
      output = run_ESM_command(cmd)
      log.info(output)
      for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
      if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format(cmd))
      else:
        log.info("Successfully executed  {} command".format(cmd))

@logThis
def verifySMPCommands():
  cmd="find /dev/bsg/ -name expander-*"
  pattern="/dev/bsg/expander.*"
  output = run_command(cmd)
  expanders_list =[]
  output1=output.splitlines()
  for line in output1:
     line =line.strip()   
     if pattern in line:
         expanders_list.append(line)
  err_count = 0
  fail_info_list = ['command not found', 'No such file or directory', 'cannot read file', 'Unknown command', 'not found', 'no space left on device', 'Command exited with non-zero status',"ERROR","Failure", "No such file","fail","CLI_UNKNOWN_CMD"]
  cmds_list=['smp_rep_general','smp_rep_manufacturer','smp_read_gpio','smp_rep_self_conf_stat','smp_rep_zone_perm_tbl','smp_rep_broadcast -b 3','smp_discover','smp_rep_phy_err_log -p 3','smp_rep_phy_sata','smp_rep_route_info','smp_rep_phy_event  -p 3','smp_discover_list','smp_rep_phy_event_list','smp_rep_exp_route_tbl','smp_ena_dis_zoning','smp_zone_lock','smp_zone_activate','smp_zone_unlock','smp_conf_zone_man_pass -P 1','smp_phy_control -p 3 -P 15','smp_conf_phy_event -p 3 -C']
  for i in range(0,1):
      for cmd in cmds_list:
         expander_cmd="{} {}".format(cmd,expanders_list[i])
         output = run_command(expander_cmd)
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
def SetPartialPathwayTimeout(expander):
   smp_discover_cmd="{}{}".format("smp_discover ",expander)
   log.info(smp_discover_cmd)
   output=run_command(smp_discover_cmd)
   pattern=".phy\s+(\S+)\:\S\:attached."
   count=0
   output=output.splitlines()
   for line in output:
      log.info(line)
      match=re.search(pattern,line)
      if match:
          attached_phy=match.group(1)
          log.info(attached_phy)
          count+=1
          break
   if count==0:
       log.info("No attached phy found")
       raise RuntimeError("All vacant phy")
   Set_Partial_pathway_value="smp_phy_control {} -p {} -P 15".format(expander,attached_phy)
   run_command(Set_Partial_pathway_value)
   show_command="smp_discover {} -p {}".format(expander,attached_phy) 
   Check_page_output=run_command(show_command)
   time.sleep(20)
   pattern=".*partial pathway timeout value\: 15.*"
   common_check_patern_2(Check_page_output,pattern,"Check partial pathway value",expect=True)

@logThis
def verifyI2CReadandWriteCliCommands():
    log.debug("Entering procedure to verifyI2CReadandWriteCliCommands")
    change_to_ESM_mode()
    log.info("Entering Expander 0")
    i2c_read_cmd_exp0=["0 0x05","0 0x06","7 0x56","7 0x64"]
    #"11 0x49","11 0x4A","11 0x64"-Skipping because of known issue
    i2c_write_cmd_exp0=["7 0x56"]
    for i in i2c_read_cmd_exp0:
        read_cmd=f"rd_seeprom {i} 0 1 1"
        output=execute_ESM_command_1(read_cmd)
        log.info(output)
        pattern="error"
        common_check_patern_2(output,pattern,"read_command_execution_check",expect=False)
    for i in i2c_write_cmd_exp0:
        write_cmd=f"wr_seeprom {i} 0 1 1"
        output=execute_ESM_command_1(write_cmd)
        pattern="error"
        common_check_patern_2(output,pattern,"write_command_execution_check",expect=False)
    CommonLib.send_command("$%^1\r",promptStr=None)
    log.info("Entering Expander 1")
    i2c_read_cmd_exp1=["0 0x05","0 0x06","1 0x50","1 0x48","7 0x56", "7 0x64"]
    #"11 0x49","11 0x4A","11 0x64","7 0x55"-Skipping because of known issue
    #"2 0x50","2 0x48"
    i2c_write_cmd_exp1=["1 0x50","7 0x56"]
    #"2 0x50","7 0x55",
    for i in i2c_read_cmd_exp1:
        read_cmd=f"rd_seeprom {i} 0 1 1"
        output=execute_ESM_command_1(read_cmd)
        pattern="error"
        common_check_patern_2(output,pattern,"read_command_execution_check",expect=False)
    for i in i2c_write_cmd_exp1:
        write_cmd=f"wr_seeprom {i} 0 1 1"
        output=execute_ESM_command_1(write_cmd)
        pattern="error"
        common_check_patern_2(output,pattern,"write_command_execution_check",expect=False)
    CommonLib.send_command("$%^3\r",promptStr=None)

@logThis
def verifyI2CReadWriteCliCommands():
    #ESMAConnect(ESMA_IP_1,ESMA_port_1)
    cmd="fru get" + "\r"
    execute_ESM_command(cmd)
    cmd="$%^0" + "\r"
    execute_ESM_command(cmd)
    log.info("Entering Expander 0")
    i2c_read_cmd_exp0=["0 0x05","0 0x06","7 0x56","7 0x64"]
    #"11 0x49","11 0x4A","11 0x64"-Skipping because of known issue
    i2c_write_cmd_exp0=["7 0x56"]
    for i in i2c_read_cmd_exp0:
        read_cmd="rd_seeprom {} 0 1 1".format(i) + '\r'
        output=run_command_cli(read_cmd)
        log.info(output)
        pattern="error"
        common_check_patern_2(output,pattern,"read_command_execution_check",expect=False)
    for i in i2c_write_cmd_exp0:
        write_cmd="wr_seeprom {} 0 1 1".format(i) + '\r'
        output=run_command_cli(write_cmd)
        pattern="error"
        common_check_patern_2(output,pattern,"write_command_execution_check",expect=False)
    cmd="$%^1" + '\r'
    execute_ESM_command(cmd)
    log.info("Entering Expander 1")
    i2c_read_cmd_exp1=["0 0x05","0 0x06","1 0x50","1 0x48","7 0x56", "7 0x64"]
    #"11 0x49","11 0x4A","11 0x64","7 0x55"-Skipping because of known issue
    #"2 0x50","2 0x48"
    i2c_write_cmd_exp1=["1 0x50","7 0x56"]
    #"2 0x50","7 0x55",
    for i in i2c_read_cmd_exp1:
        read_cmd="rd_seeprom {} 0 1 1".format(i) + '\r'
        output=run_command_cli(read_cmd)
        pattern="error"
        common_check_patern_2(output,pattern,"read_command_execution_check",expect=False)
    for i in i2c_write_cmd_exp1:
        write_cmd="wr_seeprom {} 0 1 1".format(i) + '\r'
        output=run_command_cli(write_cmd)
        pattern="error"
        common_check_patern_2(output,pattern,"write_command_execution_check",expect=False)
    cmd="$%^2" + '\r'
    execute_ESM_command(cmd)
    log.info("Entering Expander 2")
    i2c_read_cmd_exp2=["0 0x05","0 0x06","7 0x56","7 0x64"]
    #"11 0x49","11 0x4A","11 0x64","7 0x55",-Skipping because of known issue
    i2c_write_cmd_exp2=["7 0x56"]
    #"7 0x55"
    for i in i2c_read_cmd_exp2:
        read_cmd="rd_seeprom {} 0 1 1".format(i) + '\r'
        output=run_command_cli(read_cmd)
        pattern="error"
        common_check_patern_2(output,pattern,"read_command_execution_check",expect=False)
    for i in i2c_write_cmd_exp2:
        write_cmd="wr_seeprom {} 0 1 1".format(i) + '\r'
        output=run_command_cli(write_cmd)
        pattern="error"
        common_check_patern_2(output,pattern,"write_command_execution_check",expect=False)
    #Disconnect()

@logThis
def set_and_get_fan_mode(set_cmd,get_cmd,pattern):
    log.info("Inside set and get fan mode procedure")
    output = run_command_cli(set_cmd,prompt='ESM\s\S\_0\s=\>')
    log.info(output)
    time.sleep(10)
    pattern="Operation success"
    match=re.search(pattern,output)
    if match:
        log.success("Fan mode set successful")
    else:
        log.fail("Fan mode set Fail")
        raise RuntimeError("Fan mode set Fail")
    output=run_command_cli(get_cmd,prompt='ESM\s\S\_0\s=\>')
    common_check_patern_2(output,pattern,"fan_mode_set_check",expect=False)

@logThis
def change_to_ESM_mode():
    log.info("Inside Change to ESM procedure")
    CommonLib.send_command("$%^0\r",promptStr=None)

@logThis
def set_and_get_fan_speed(dev):
    p=[40,50,60,70,80,90,100]
    l=[1,2,3,4,5,6,7]
    value=["55%","55%","60%","70%","80%","90%","100%"]
    for i in p:
        pattern="ESM{}.*Normal.*{}.*".format(dev,i)
        cmd = "fan set -p {}\r".format(i)
        run_command_cli(cmd,prompt='ESM\s\S\_0\s=\>')
        time.sleep(10)
        get_cmd="fan get\r"
        output=run_command_cli(get_cmd,prompt='ESM\s\S\_0\s=\>')
        common_check_patern_2(output,pattern,"Fan speed check",expect=True)
    for i in l:
        for j in value:
            pattern="ESM{}.*Normal.*{}.*".format(dev,j)
            cmd = "fan set -l {}\r".format(i)
            run_command_cli(cmd,prompt='ESM\s\S\_0\s=\>')
            time.sleep(10)
            get_cmd="fan get\r"
            output=run_command_cli(get_cmd,prompt='ESM\s\S\_0\s=\>')
            common_check_patern_2(output,pattern,"Fan speed check",expect=True)
            value.remove(j)
            break

@logThis
def verifyReadBuffer():
    log.info("Entering read buffer verification procedure")
    hdds = querySGDevices()
    fail_info_list = ['command not found', 'No such file or directory', 'cannot read file', 'Unknown command', 'not found', 'no space left on device', 'Command exited with non-zero status',"ERROR","Failure", "No such file","fail","CLI_UNKNOWN_CMD"]
    for hdd in hdds:
       read_buffer_command="{} {}".format(read_buffer_cmd,hdd)
       output = run_command(read_buffer_command)
       err_count = 0
       for error in fail_info_list:
            match = re.search(error, output)
            if match:
                log.error("fail to get output, error info:{}".format(error))
                err_count += 1
       if err_count:
            raise RuntimeError('{} command execution fail in {}'.format(read_buffer_command,hdd))
       else:
            log.info("Successfully executed  {} command in {}".format(read_buffer_command,hdd))

@logThis
def verifyReportLuns():
    log.info("Entering the procedure to check Luns Report")
    hdds = querySGDevices()
    for hdd in hdds:
        lun_report_command="{} {}".format(lun_report_cmd,hdd)
        CommonLib.execute_check_dict(Const.DUT, lun_report_command, patterns_dict=lun_report_pattern)

@logThis
def ServerConnectESMB():
    DeviceMgr.usingSsh = True
    global device
    device = DeviceMgr.getDevice()
    device.connect(device.rootUserName, device.esmbBmcIP)
    device.loginToDiagOS()
    device.readUntil(device.promptBmc)
    global run_command
    run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
    return

@logThis
def exit_ESM_mode():
    log.info("Inside exit_ESM_mode procedure")
    CommonLib.send_command("$%^3\r",promptStr=None)

@logThis
def execute_ESM_command_1(cmd,error_pattern=some_common_error_patterns):
    log.info("Inside execute_ESM_command_1 procedure")
    output=run_command_cli(cmd + '\r',prompt='ESM\s\S\_[01]\s=\>')
    log.info(output)
    if re.search(error_pattern, output):
        log.fail("Exception Occured")
        raise RuntimeError("ESM Command Failed")
    return output

@logThis
def execute_Linux_command(cmd,error_pattern=some_common_error_patterns):
    log.info("Inside execute_Linux_command procedure")
    output=run_command(cmd,timeout=300)
    log.info(output)
    if re.search(error_pattern, output):
        log.fail("Exception Occured")
        raise RuntimeError("Linux Command Failed")
    return output

@logThis
def compare_fru_get_outputs(op1,op2):
    log.info("Inside compare_fru_get_outputs procedure")
    t1 = re.sub("Running Time: ([0-9][0-9][0-9]|[0-9][0-9]|[0-9]) day ([0-9][0-9]|[0-9]) hours ([0-9][0-9]|[0-9]) minutes ([0-9][0-9]|[0-9]) seconds", '', op1)
    t2 = re.sub("Running Time: ([0-9][0-9][0-9]|[0-9][0-9]|[0-9]) day ([0-9][0-9]|[0-9]) hours ([0-9][0-9]|[0-9]) minutes ([0-9][0-9]|[0-9]) seconds", '', op2)
    if t1 == t2:
        log.success("Outputs are same")
    else:
        log.fail("Outputs are not same")
        raise RuntimeError("FRU Check Failed after reset")

@logThis
def get_primary_device():
    log.info("Inside get_primary_device procedure")
    devices = querySGDevices()
    for i in devices:
        output = run_command("sg_ses -p 1 " + i)
        p1 = 'relative ES process id.*1,'
        p2 = 'relative ES process id.*3,'
        split_output = output.splitlines();
        for line in split_output:
           line = line.strip();
           match1 = re.search(p1,line)
           match2 = re.search(p2,line)
           if match1 or match2:
              prim_device = i
              return prim_device

@logThis
def get_non_primary_device():
    log.info("Inside get_non_primary_device procedure")
    devices = querySGDevices()
    for i in devices:
        output = run_command("sg_ses -p 1 " + i)
        p1 = 'relative ES process id.*2,'
        p2 = 'relative ES process id.*4,'
        split_output = output.splitlines();
        for line in split_output:
           line = line.strip();
           match1 = re.search(p1,line)
           match2 = re.search(p2,line)
           if match1 or match2:
              non_prim_device = i
              return non_prim_device

@logThis
def get_canister_FW():
    log.info("Inside get_canister_FW procedure")
    output=execute_ESM_command_1('about')
    p1 = 'FW Revision.*([0-9]\.[0-9]\.[0-9]\.([0-9][0-9]|[0-9]))'
    split_output = output.splitlines();
    for line in split_output:
       line = line.strip();
       match1 = re.search(p1,line)
       if match1:
          return match1.group(1)


@logThis
def compare_outputs(cmd):
    output1= run_command(cmd)
    Disconnect()
    ServerConnectESMB()
    output2=run_command(cmd)
    Disconnect()
    output1=output1.split('\n',3)[-1]
    log.info(output1)
    output2=output2.split('\n',2)[-1]
    log.info(output2)
    if output1 == output2:
        log.success("Both ESM enclosure status are in sync")
    else:
        log.info("Both ESM enclosure status are not in sync")
        raise RuntimeError("Both ESM enclosure status are not in sync")


@logThis
def checkExecutionOfCLI():
  cmd_list = [ 'about','drv get','esm get','fan get','fru get','log get','log clear','port get','power get','temp get','threshold get','checklist get','mode get','debug on','debug off','led get','vpd get -d 0','vpd get -c 0',' vpd get -d 1','vpd get -c 1','vpd get -p 0','vpd get -p 1','led set 1 on','led set 1 off','threshold set t0 -19 -19 1 70','threshold set t0 -19 -19 65 70','drv set 0 off','drv set 0 on','fan set -p 60']
  err_count = 0
  fail_info_list = ['command not found', 'No such file or directory', 'cannot read file', 'Unknown command', 'not found', 'no space left on device', 'Command exited with non-zero status',"ERROR", "No such file","fail","CLI_UNKNOWN_CMD"]
  for cmd in cmd_list:
      output=run_command_cli(cmd + '\r',prompt='ESM\s\S\_0\s=\>')
      log.info(output)
      for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
      if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format(cmd))
      else:
        log.info("Successfully executed  {} command".format(cmd))
  output=run_command_cli('config reset'+ '\r',prompt='Select \>')
  for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
  if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format('config reset'))
  else:
        log.info("Successfully executed  {} command".format('config reset'))
  run_command_cli('1' + '\r',prompt='ESM\s\S\_0\s=\>')
  output=run_command_cli('fru set -c'+ '\r',prompt='New:')
  for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
  if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format('fru set -c'))
  else:
        log.info("Successfully executed  {} command".format('fru set -c'))
  run_command_cli('exit' + '\r',prompt='ESM\s\S\_0\s=\>')

@logThis
def RemoveAthenaSesFwImage(device,module="Athena_FW"):
    log.debug("Entering RemoveAthenaSesFwImage with args : %s" %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    destinationDir = imageObj.localImageDir
    imgList = list(imageObj.oldImage.values()) + list(imageObj.newImage.values())
    for image in imgList:
       deviceObj.sendCmd("rm %s/%s" %(destinationDir,image)) 

@logThis
def downloadAthenaSesFwImage(device,module="Athena_FW"):
    log.debug("Entering download_Athena_Ses_Fw_Image with args : %s" %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    serverObj = Server.getServer(imageObj.imageServer, needLogin=False)
    imgList = list(imageObj.oldImage.values()) + list(imageObj.newImage.values())

    hostDir = imageObj.hostImageDir
    destinationDir = imageObj.localImageDir

    promptList = ["(y/n)", "(yes/no)", "password:"]
    patternList = re.compile('|'.join(promptList))
    success = False

    for image in imgList:
       deviceObj.sendCmd("scp %s@%s:%s/%s %s" % (serverObj.username, serverObj.managementIP, hostDir, image, destinationDir))
       output1 = deviceObj.read_until_regexp(patternList, 180)
       log.info('output1: ' + str(output1))
       if re.search("(yes/no)",output1):
           deviceObj.transmit("yes")
           deviceObj.receive("password:")
           deviceObj.transmit("%s"%serverObj.password)
       elif re.search("(y/n)",output1):
           deviceObj.transmit("y")
           deviceObj.receive("password:")
           deviceObj.transmit("%s"%serverObj.password)
       elif re.search("password:",output1):
           deviceObj.transmit("%s"%serverObj.password)
       else :
           log.fail("pattern mismatch")

       currentPromptStr = deviceObj.getCurrentPromptStr()
       currentPromptStr = currentPromptStr if currentPromptStr else "100%|No such file"
       output = deviceObj.read_until_regexp(currentPromptStr,timeout=Const.COPYING_TIME)
       p0 = ".*100\%"
       p1 = "No such file or directory"
       if re.search(p0, output):
            log.info("Successfully copy file: %s"%(image))
            success = True
       elif re.search(p1, output):
            log.error("%s"%(p1))
            raise RuntimeError(p1 + ': ' + image)

    if not success:
        raise RuntimeError("Copy file {} through scp failed!".format(fileName))
    return 0

@logThis
def GetCanisterImageName(key,module,upgrade=True):
    log.debug("Entering GetCanisterImageName with args : %s" %(str(locals())))
    imageObj = SwImage.getSwImage(module)
    if upgrade:
       return  imageObj.localImageDir + '/' + imageObj.newImage[key]
    else:
       return  imageObj.localImageDir + '/' + imageObj.oldImage[key]

@logThis
def GetRevFromCanisterImage(image):
    log.debug("Entering GetRevFromImage with args : %s" %(str(locals())))
    p1 = ".*([0-9])\.([0-9])\.([0-9])"
    match = re.search(p1,image)
    if match:
        return match.group(1) + '.*' + match.group(2) + '.*' + match.group(3)

@logThis
def change_to_ESM_mode_1():
    log.info("Inside Change to ESM 1 procedure")
    CommonLib.send_command("$%^1\r",promptStr=None)

@logThis
def verify_CPLD_version(rev_to_Check,ESM):
    CommonLib.send_command("$%^0\r",promptStr=None)
    cmd='fru get'
    output =  run_command_cli(cmd + '\r',prompt='ESM\s\S\_0\s=\>')
    pattern='.*CPLD Revision Code:.*'
    version_list=[]
    output= output.splitlines()
    for line in output:
        match =re.search(pattern,line)
        if match:
            version_list.append(line)
    ESMA_CPLD_Version=version_list[0]
    ESMB_CPLD_version=version_list[1]
    if ESM == 'A':
        common_check_patern_2(ESMA_CPLD_Version,rev_to_Check,"CPLD version check in ESM A",expect=True)
    if ESM == 'B':
        common_check_patern_2(ESMB_CPLD_version,rev_to_Check,"CPLD version check in ESM B",expect=True)

@logThis
def VerifyCommandValidation():
  change_to_ESM_mode()
  cmd_list = ['vpd get -c 0','vpd get -c 1','rd_seeprom 0 0x51 0x00 2 100','rd_seeprom 0 0x51 0x00 2 100','vpd get -d 0','vpd get -d 1','rd_seeprom 1 0x58 0x00 1 1','rd_seeprom 2 0x58 0x00 1 1','rd_seeprom 1 0x51 0x00 1 100','rd_seeprom 2 0x51 0x00 1 100','rd_seeprom 2 0x18 0xf0 1 1','rd_seeprom 3 0x2E 0x00 1 1','temp get','rd_seeprom 4 0x6C 0x00 1 1','rd_seeprom 4 0x6 0x00 1 1']
  err_count = 0
  fail_info_list = ['command not found', 'No such file or directory', 'cannot read file', 'Unknown command', 'not found', 'no space left on device', 'Command exited with non-zero status',"ERROR", "No such file","fail","CLI_UNKNOWN_CMD"]
  for cmd in cmd_list:
      output=run_command_cli(cmd + '\r',prompt='ESM\s\S\_0\s=\>')
      log.info(output)
      for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
      if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format(cmd))
      else:
        log.info("Successfully executed  {} command".format(cmd))
  output=run_command_cli('config reset'+ '\r',prompt='Select \>')
  for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
  if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format('config reset'))
  else:
        log.info("Successfully executed  {} command".format('config reset'))
  run_command_cli('1' + '\r',prompt='ESM\s\S\_0\s=\>')
  output=run_command_cli('fru set -c'+ '\r',prompt='New:')
  for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
  if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format('fru set -c'))
  else:
        log.info("Successfully executed  {} command".format('fru set -c'))
  run_command_cli('exit' + '\r',prompt='ESM\s\S\_0\s=\>')
  exit_ESM_mode()

@logThis
def CLI_Reset_Validation():
    change_to_ESM_mode()
    cmd_list = [ 'reset 0', 'reset 1', 'reset 2', 'reset 3', 'reset 4']
    for cmd in cmd_list:
        clear_log = 'log clear'
        run_command_cli(clear_log + '\r',prompt='ESM\s\S\_0\s=\>')
        output=run_command_cli(cmd + '\r',prompt='ESM\s\S\_0\s=\>')
        time.sleep(200)
        output=run_command_cli('\r',prompt=' ')
        pattern = "ESM Reset"
        cmd = "log get"
        output=run_command_cli(cmd + '\r',prompt='ESM\s\S\_0\s=\>')
        match = re.search(pattern,output)
        if match:
            log.success("ESM reset successfully")
        else:
            log.error("ESM failed to reset")
            raise RuntimeError('ESM failed to reset')
    exit_ESM_mode()

@logThis
def verify_disk_count(installed_disk_count):
   cmd='lsblk |grep nvme |wc -l'
   output=run_command(cmd)
   log.info(output)
   pattern="^{}".format(installed_disk_count)
   log.info(pattern)
   output=output.splitlines()
   count =0
   for line in output:
       match=re.search(pattern,line)
       if match:
           log.success("Installed disk count matches with available disk count")
           count = count + 1
   if count == '0':
       log.fail("Installed disk count does not match with available disk count")
       raise RuntimeError("Installed disk count does not match with available disk count")

@logThis
def get_ps_hardware(fru_output):
    log.debug("Entering procedure to get the ps hardware version")
    ProductNameInfo = get_deviceinfo_from_config("UUT","name")
    output=fru_output.splitlines()
    psu1_HW_EC_Level_pattern=r'.*--- Power Supply 1 ---.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*HW EC LEVEL:\s+(\S+).*'
    psu1_Find_pattern =""".*--- Power Supply 1 ---.*
    .*PS Type: DPS-1300AB-6 J.*
    .*Power Capacity: 1300.*
    .*PS Manufacturer: DELTA.*
    .*PS Serial Number: .*
    .*PS Part Number: .*
    .*PS Firmware Version: .*
    .*HW EC LEVEL:\s+(\S+).*"""
    if ProductNameInfo == "Titan_G2_Lenovo":
        log.debug(f"Inside get_ps_hardware   Product Name :{ProductNameInfo}")
        match = re.search(psu1_HW_EC_Level_pattern,fru_output,re.I|re.M)
        if match:
            ps_hardware_ver=match.group(1)
            log.info(ps_hardware_ver)
            log.debug(f"Inside get_ps_hardware   ps_hardware_ver:{ps_hardware_ver}")
            return ps_hardware_ver
    else:
        pattern=".*PS Hardware Version:\s+(\S+).*"
        for line in output:
            match=re.search(pattern,line)
            if match:
                ps_hardware_ver=match.group(1)
                log.info(ps_hardware_ver)
                break
        return ps_hardware_ver

@logThis
def GetPSUVersion(module,isUpgrade=True):
    log.debug("Enetering procedure to get the PSU version")
    imageObj = SwImage.getSwImage(module)
    expect_version = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    return expect_version

@logThis
def GetCanisterUpdateImageName(key,module,psuversion):
    log.debug("Entering GetCanisterImageName with args : %s" %(str(locals())))
    imageObj = SwImage.getSwImage(module)
    if psuversion == imageObj.oldVersion:
        images = imageObj.localImageDir + '/' + imageObj.newImage[key]
        psu_version_exp = imageObj.newVersion
        return images, psu_version_exp
    else:
        images = imageObj.localImageDir + '/' + imageObj.oldImage[key]
        psu_version_exp = imageObj.oldVersion
        return images, psu_version_exp

@logThis
def execute_linux_command1(cmd):
    log.info("Inside execute_Linux_command procedure")
    cmd= cmd + '\r'
    output=run_command(cmd)
    log.info(output)
    return output

@logThis
def ServerConnect_1():
    log.debug("Entering ServerConnect_1 proc")
    DeviceMgr.usingSsh = True
    global device
    device = DeviceMgr.getDevice()
    device.connect(device.rootUserName, device.bmcIP)
    device.loginToDiagOS()
    device.readUntil(device.promptBmc)
    global run_command
    run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptBmc)
    return

@logThis
def verify_ses_page_04_nebula(username, hostip, password, devicename):
    log.debug("Entering verify_ses_page_04_nebula with args : %s" %(str(locals())))
    err_count = 0
    cmd = 'sg_ses --page=0x04 ' + devicename
    pattern = r'String.+\n\s+00\s+(.+)\s'
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    match = re.search(pattern, output, re.I|re.M)
    if match:
        dynamic_valu_hex=match.group(1).strip()
        dynamic_valu_str=dynamic_valu_hex.replace(" ","")
        if len(dynamic_valu_str) == 8:
            log.success("Successfully verify SES page4 dynamic value is 4 bytes")
        else:
            err_count += 1
            log.fail(f"Fail SES page4 dynamic value is not 4 byte")
            raise RuntimeError("verify_ses_page_04_nebula: SES page4 dynamic value is not 4 bytes")
    else:
        err_count += 1
        log.fail(f"Can't match the patern: {patern}")

@logThis
def verify_ses_page_04_lenovo(username, hostip, password, devicename, expect_ESMA_IP, expect_gateway, expect_ESM_A_DHCP_Mode, expect_ESMA_up_time, \
                        expect_ESMB_up_time, expect_ESM_Zoning_Mode, expect_ESMB_IP, expect_ESM_B_DHCP_Mode, \
                        expect_netmask, expect_LCD_mask='ff', expect_LCD='00'):
    """
    :param devicename:sg_ses use devicename to get ses page
    :param '81':enable '80':disabled, '00':not support
    """
    err_count = 0
    dict_expect = {'esm_a_ip' : expect_ESMA_IP, 'esm_b_ip' : expect_ESMB_IP, 'gateway' : expect_gateway, 'esm_zoning_mode' : expect_ESM_Zoning_Mode, \
                    'esm_a_dpcp_mode' : expect_ESM_A_DHCP_Mode, 'esm_b_dpcp_mode' : expect_ESM_B_DHCP_Mode, 'netmask' : expect_netmask, \
                   'lcd_mask' : expect_LCD_mask, 'lcd' : expect_LCD}
    print(dict_expect)
    cmd = 'sg_ses --page=0x04 ' + devicename
    p = 'String.+\n\s+00\s+(.+)\s+\..+\n\s+10\s+(.+)\s+\.'
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    match = re.search(p, output)
    if match:
        page_4_list = match.group(1).strip().split() + match.group(2).strip().split()
        print(page_4_list)
        ESMA_up_time = parser_openbmc_lib.parse_hex_to_int("".join(page_4_list[0:4]))
        ESMB_up_time = parser_openbmc_lib.parse_hex_to_int("".join(page_4_list[4:8]))
        ESM_Zoning_Mode = page_4_list[9]
        ESM_A_DHCP_Mode = page_4_list[10]
        ESM_B_DHCP_Mode = page_4_list[11]
        ESMA_IP = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[12:16]])
        ESMB_IP = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[16:20]])
        netmask = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[20:24]])
        gateway = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[24:28]])
        LCD_mask = page_4_list[28]
        LCD = page_4_list[29]
        log.info("ESM_A_DHCP_Mode is {}".format(ESM_A_DHCP_Mode))
        log.info("ESM_B_DHCP_Mode is {}".format(ESM_B_DHCP_Mode))
        log.info("ESMA_IP is {}".format(ESMA_IP))
        log.info("ESMB_IP is {}".format(ESMB_IP))
        log.info("gateway is {}".format(gateway))
        log.info("ESMA_up_time is {}".format(ESMA_up_time))
        log.info("ESMB_up_time is {}".format(ESMB_up_time))
        dict_actual = {'esm_a_ip' : ESMA_IP, 'esm_b_ip' : ESMB_IP, 'gateway' : gateway, 'esm_zoning_mode' : ESM_Zoning_Mode, \
                        'esm_a_dpcp_mode' : ESM_A_DHCP_Mode, 'esm_b_dpcp_mode' : ESM_B_DHCP_Mode, 'netmask' : netmask, 'lcd_mask' : LCD_mask, 'lcd' : LCD}
        print(dict_actual)
        for k in dict_expect.keys() & dict_actual.keys():
            if dict_expect[k] == dict_actual[k]:
                log.success("Successfully verify {}: {}".format(k, dict_expect[k]))
            else:
                log.fail("Fail to verify {}: {}, expect: {}".format(k, dict_actual[k], dict_expect[k]))
                err_count += 1
        if (ESMA_up_time - expect_ESMA_up_time) <= 40 and ESMA_up_time >= 0:
            log.success("Successfully verify ESMA_up_time: {}".format(ESMA_up_time))
        else:
            log.fail("Fail to verify ESMA_up_time: {}, expect: {}".format(ESMA_up_time, expect_ESMA_up_time))
            err_count += 1
        if (ESMB_up_time - expect_ESMB_up_time) <= 20 and ESMB_up_time >= 0:
            log.success("Successfully verify ESMB_up_time: {}".format(ESMB_up_time))
        else:
            log.fail("Fail to verify ESMB_up_time: {}, expect: {}".format(ESMB_up_time, expect_ESMB_up_time))
            err_count += 1
    else:
        err_count += 1
        log.fail("Can't match the patern: {}".format(p))

    if err_count:
        raise RuntimeError("verify_ses_page_04_lenovo")

@logThis
def verify_ses_page_04_kiwi(username, hostip, password, devicename, expect_ESMA_IP, expect_gateway, expect_ESM_A_DHCP_Mode, expect_ESMA_up_time, \
                        expect_ESM_Zoning_Mode, expect_netmask, expect_LCD_mask='ff', expect_LCD='00'):
    """
    :param devicename:sg_ses use devicename to get ses page
    :param '81':enable '80':disabled, '00':not support
    """
    err_count = 0
    dict_expect = {'esm_a_ip' : expect_ESMA_IP, 'gateway' : expect_gateway, 'esm_zoning_mode' : expect_ESM_Zoning_Mode, \
                    'esm_a_dpcp_mode' : expect_ESM_A_DHCP_Mode, 'netmask' : expect_netmask, 'lcd_mask' : expect_LCD_mask, 'lcd' : expect_LCD}
    print(dict_expect)
    cmd = 'sg_ses --page=0x04 ' + devicename
    p = 'String.+\n\s+00\s+(.+)\s+\..+\n\s+10\s+(.+)\s+\.'
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    match = re.search(p, output)
    if match:
        page_4_list = match.group(1).strip().split() + match.group(2).strip().split()
        print(page_4_list)
        ESMA_up_time = parser_openbmc_lib.parse_hex_to_int("".join(page_4_list[0:4]))
        ESM_Zoning_Mode = page_4_list[9]
        ESM_A_DHCP_Mode = page_4_list[10]
        ESMA_IP = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[12:16]])
        netmask = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[20:24]])
        gateway = ".".join([(str(parser_openbmc_lib.parse_hex_to_int(i))).zfill(3) for i in page_4_list[24:28]])
        LCD_mask = page_4_list[28]
        LCD = page_4_list[29]
        log.info("ESM_A_DHCP_Mode is {}".format(ESM_A_DHCP_Mode))
        log.info("ESMA_IP is {}".format(ESMA_IP))
        log.info("gateway is {}".format(gateway))
        log.info("ESMA_up_time is {}".format(ESMA_up_time))
        dict_actual = {'esm_a_ip' : ESMA_IP, 'gateway' : gateway, 'esm_zoning_mode' : ESM_Zoning_Mode, \
                        'esm_a_dpcp_mode' : ESM_A_DHCP_Mode, 'netmask' : netmask, 'lcd_mask' : LCD_mask, 'lcd' : LCD}
        print(dict_actual)
        for k in dict_expect.keys() & dict_actual.keys():
            if dict_expect[k] == dict_actual[k]:
                log.success("Successfully verify {}: {}".format(k, dict_expect[k]))
            else:
                log.fail("Fail to verify {}: {}, expect: {}".format(k, dict_actual[k], dict_expect[k]))
                err_count += 1
        if (ESMA_up_time - expect_ESMA_up_time) <= 20 and ESMA_up_time >= 0:
            log.success("Successfully verify ESMA_up_time: {}".format(ESMA_up_time))
        else:
            log.fail("Fail to verify ESMA_up_time: {}, expect: {}".format(ESMA_up_time, expect_ESMA_up_time))
            err_count += 1
    else:
        err_count += 1
        log.fail("Can't match the patern: {}".format(p))

    if err_count:
        raise RuntimeError("verify_ses_page_04_kiwi")

@logThis
def verify_HIC_card_link_speed(slotlist,expect_speed,expect_width):
    log.debug("Entering procedure to verify the speed and width of pcie slots")
    for slot in slotlist:
        cmd="lspci -vvv -s {}".format(slot)
        output=run_command(cmd)
        log.info(output)
        match=re.search(expect_speed,output)
        if match:
            log.success("HIC_card_link_speed check is successful for slot {}".format(slot))
        else:
            log.fail("HIC_card_link_speed check is not successful for slot {}".format(slot))
            raise RuntimeError("HIC_card_link_speed check is not successful for slot {}".format(slot))
        match=re.search(expect_width,output)
        if match:
            log.success("HIC_card_width_check is successful for slot {}".format(slot))
        else:
            log.fail("HIC_card_width_check is not successful for slot {}".format(slot))
            raise RuntimeError("HIC_card_width_check is not successful for slot {}".format(slot))

@logThis
def verifyLAN_Speed_Auto_negotiation(expected_output):
    log.debug("Entering procedure to get the ps hardware version")
    ifconfig_cmd = 'ifconfig'
    tool_cmd = 'ethtool'
    ifconfig_output=run_command(ifconfig_cmd)
    pattern=r'(^eno[0-9a-z]+)'
    lines=ifconfig_output.split('\n')
    res=''
    for i in lines:
        match1=re.search(pattern,i,re.I|re.M)
        if match1:
            res = match1.group(0)
            tmp_cmd=tool_cmd + ' ' + res
            log.debug(f"final command :{tmp_cmd}")
            toolcmd_output=run_command(tmp_cmd)
            match2=re.search("(Supports auto-negotiation:\sYes)",toolcmd_output,re.I|re.M)
            support_value =match2.group(0)
            if support_value == expected_output:
                log.success(f"Successfully:{support_value}")
            else:
                log.fail(f"Failed:{support_value}")
                raise RuntimeError(f"Failed:{support_value}")

@logThis
def downloadPSUFwImage(module="PSU", upgrade=True):
    CommonLib.download_image(Const.SSH_DUT, module, upgrade=upgrade)

@logThis
def getTotalNumberOfDrives():
     cmd="lsscsi -g | wc -l"
     output=run_command(cmd)
     output=output.splitlines()[-2]
     log.info(output)
     return output

@logThis
def getcurrenttime():
    return_dict = {}
    cap_time_output = run_command('timedatectl')
    p1 = 'Universal time:.* (?P<year>\S+)-(?P<month>\S+)-(?P<day>\S+) (?P<hour>\S+):(?P<minute>\S+):(?P<second>\S+).*UTC'
    split_output = cap_time_output.splitlines();
    count = 0
    for line in split_output:
        line = str(line.strip());
        match = re.search(p1,line)
        if match:
            return_dict['Year'] = match.group('year')
            return_dict['Month'] = match.group('month')
            return_dict['Day'] = match.group('day')
            return_dict['Hour'] = match.group('hour')
            return_dict['Minute'] =  match.group('minute')
            return_dict['Sec'] =  match.group('second')
            count=count+1
            current_time=return_dict['Day']+"/"+return_dict['Month']+"/"+return_dict['Year']+" "+return_dict['Hour']+":"+return_dict['Minute']+":"+return_dict['Sec']
            return current_time
    if count == 0 :
        log.fail("could not get universal time from timedatectl")
        raise RuntimeError("could not get universal time from timedatectl")
    else:
        log.info("Got current time and date")

@logThis
def verifyDisk_Temperature():
    log.debug("Entering procedure to verify Disk Temperature")
    cmd = '''lsscsi -g |grep "disk"'''
    DiskDetails_output=run_command(cmd)
    pattern1=r'disk.*\s+([/dev/sg]+[0-9]+)'
    pattern2=r'Current Drive Temperature:\s+([0-9]+)\sC'
    lines=DiskDetails_output.split('\n')
    Disk_list=[]
    for i in lines:
      match1=re.search(pattern1,i,re.I|re.M)
      if match1:
        Disk_list.append(match1.group(1))
    log.debug(f"Disk list :{Disk_list}")
    for j in Disk_list:
      temp_cmd="smartctl -x " + j + " |grep \"Current Drive Temperature\""
      log.debug(f"final cmd :{temp_cmd}")
      Disk_Temp_output=run_command(temp_cmd)
      match2=re.search(pattern2,Disk_Temp_output,re.I|re.M)
      if match2:
        temp_value=match2.group(1)
        log.debug(f"{j} value :{temp_value}")
        if 0 <= int(temp_value) <= 60:
            log.success(f"Disk {j} Temperature value is {temp_value}")
        else:
            log.fail(f"Disk {j} Temperature value is {temp_value}")

@logThis
def getNumberOfPCIEDrives():
    cmd="lspci | wc -l"
    output=run_command(cmd)
    output=output.splitlines()[-2]
    log.info(output)
    return output

@logThis
def checkFwVersionESM(username, hostip, password):
    log.debug("Entering Check wheather same SES FW Vsersion on both ESMs procedure:checkFwVersionESM")
    enclosu_cmd = 'lsscsi -g | grep -i enclosu'
    pattern1=r'CELESTIC  LENOVO\s+(\w+)'
    pattern2=r'CELESTIC LENOVO.*?(/dev/sg\d+)'
    output_enclosu = get_output_from_ssh_command(username, hostip, password, enclosu_cmd)
    lines=output_enclosu.split('\n')
    sg_device_list=[]
    pass_count=0

    for i in lines:
        match=re.search(pattern2,i,re.I|re.M)
        if match:
            sg_device_list.append(match.group(1))
    sg_device_length=len(sg_device_list)
    page7_cmd = 'sg_ses -p 7 ' + sg_device_list[0]
    log.debug(f"page7 command :{page7_cmd}")

    output_page7 = get_output_from_ssh_command(username, hostip, password, page7_cmd)
    match=re.search(pattern1,output_page7,re.I|re.M)
    FW_version = match.group(1)
    log.debug(f"SES FW Version :{FW_version}")
    for i in sg_device_list:
        pattern3=f'CELESTIC LENOVO\s+{FW_version}.*?{i}'
        match=re.search(pattern3,output_enclosu,re.I|re.M)
        if match:
            pass_count += 1
    if pass_count == sg_device_length:
        log.success(f"SES FW version {FW_version} is same on both ESMs")
    else:
        log.fail(f"SES FW version {FW_version} is not same on both ESMs")
        raise RuntimeError(f"SES FW version {FW_version} is not same on both ESMs")

@logThis
def check_PSU_Redundant():
    log.debug("Entering check_PSU_Redundant class procedure: check_PSU_Redundant")
    cmd = 'ipmitool fru'
    output=run_command(cmd)
    #output = get_output_from_ssh_command(username, hostip, password, cmd)
    pattern = r'FRU Device Description.*:\s([PSU0-9_FRU]+)'
    PSU_List = re.findall(pattern, output, re.I|re.M)
    log.debug(f"PSU Devices List :{PSU_List}")
    if len(PSU_List) >= 2:
        log.success(f"PSU Redundant is available in this machine")
    else:
        log.fail("PSU Redundant is not available in this machine")
        raise RuntimeError("check_PSU_Redundant")

@logThis
def get_device_list_nebula(username, hostip, password):
    log.debug("Entering get_device_list_nebula")
    cmd="ls /dev/switch*"
    output = get_output_from_ssh_command(username, hostip, password, cmd)
    log.info(output)
    right_list=[]
    dev_list=[]
    for line in output.splitlines():
        line = line.strip()
        if '/dev/switchtec' in line:
            right_list.append(line)
    for i in right_list:
        log.debug(i)
        cmd="sg_inq {}".format(i)
        cmd_op=get_output_from_ssh_command(username, hostip, password, cmd)
        log.info(cmd_op)
        pattern="Product identification: Nebula_Gen2F"
        if re.search(pattern,cmd_op):
            dev_list.append(i)
    return dev_list

@logThis
def getFWImage(upgrade=True):
    log.debug("Entering getFWImage procedure")
    if upgrade:
        image_file = CommonLib.get_swinfo_dict("SES").get("newImage", "NotFound")
    else:
        image_file = CommonLib.get_swinfo_dict("SES").get("oldImage", "NotFound")
    return image_file

@logThis
def Update_Activate_Ses_Fw_nebula(sg_device_list, Upgrade, image_lists, username, hostip, password):
  log.debug("Entering update_and_activate_nebula procedure with args : %s" %(str(locals())))
  for sg_device in sg_device_list:
    log.debug(f"sg_device ==>{sg_device}")
    for image in image_lists:
      log.debug(f"image ==>{image}")
      ServerConnect_1()
      updateSesFw(sg_device, Upgrade, image)
      #ses_activitate(username, hostip, password, sg_device, 0xf) 
      #command mode 7 will activate the new fw, no need to do the mode 0xf
      #time.sleep(120)
      #whitebox_lib.reboot_os(device)
      Reboot_OS_via_MGMT(username, hostip, password, "reboot")
      ServerDisconnect()
      time.sleep(130)

@logThis
def verify_ses_version_fru_get_nebula(device, isUpgrade=True):
    log.debug("Entering verify_ses_version_fru_get_nebula procedure with args : %s" %(str(locals())))
    imageObj = SwImage.getSwImage('SES')
    expect_version = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    cmd = 'fru get\r'
    output = run_ESM_command(cmd)
    p1 = ['CFG Revision \W?(\S+)\.','FW Revision\W?(\S+)\.']
    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    if ProductTypeInfo == "Nebula_Gen2F":
        log.debug(f"Platform type :{ProductTypeInfo}")
        common_check_patern_4(output, p1, expect_version, 'verify_ses_version_fru_get_nebula_1')

@logThis
def common_check_patern_4(output, p_list, expect, testname):
    log.debug("Entering common_check_patern_4 procedure with args : %s" %(str(locals())))
    err_count = 0
    for p, expect_value in zip(p_list, expect):
        match = re.search(p, output)
        if match:
            value = match.group(1).strip()
            if value == expect_value:
                log.success("Successfully {} {}: {}".format(testname, p, expect_value))
            else:
                log.fail("Fail to {} {} expect {}, actual is {}".format(testname, p, expect_value, value))
                err_count += 1
        else:
            err_count += 1
            log.fail("can't match patern:{}".format(p))
    if err_count:
        raise RuntimeError("{}".format(testname))

@logThis
def check_Ses_Fw_Version_nebula(username, hostip, password, hdd_list, upgrade=True):
    log.debug("Entering check_Ses_Fw_Version_nebulaprocedure with args : %s" %(str(locals())))
    if upgrade:
      version="newVersion"
    else:
      version="oldVersion"
    version =  CommonLib.get_swinfo_dict("SES").get(version, "NotFound")
    version_list = version[1].split(".")
    version_list = map(int, version_list)
    version_format = "{0:0>2d}{1}{2}".format(*version_list)
    for hdd in hdd_list:
        cmd = f"sg_inq {hdd}"
        output=get_output_from_ssh_command(username, hostip, password, cmd)
        pattern="Product revision level:\s(.+)"
        match = re.search(pattern,output,re.I|re.M)
        if match:
            if match.group(1).strip() == version_format:
                log.success(f"Successfully verified SES FW Version: expected {match.group(1).strip()}")
            else:
                log.fail(f"acctual: {match.group(1).strip()} mismatch expected: {version_format}")
        else:
            log.fail(f"acctual: {pattern} mismatach expected version formate: {version_format}")

@logThis
def get_primary_device_nebula(username, hostip, password):
    log.info("Inside get_primary_device_nebula procedure")
    devices =get_device_list_nebula(username, hostip, password)
    for i in devices:
        output = run_command("sg_ses -p 1 " + i)
        p1 = 'relative ES process id.*1, number of ES processes:.*[2|3]'
        #p2 = 'relative ES process id.*3'
        split_output = output.splitlines();
        for line in split_output:
           line = line.strip();
           match1 = re.search(p1,line)
           #match2 = re.search(p2,line)
           if match1:
              prim_device = i
              return prim_device
@logThis
def get_non_primary_device_nebula(username, hostip, password):
    log.info("Inside get_non_primary_device_nebula procedure")
    devices = get_device_list_nebula(username, hostip, password)
    for i in devices:
        output = run_command("sg_ses -p 1 " + i)
        p1 = 'relative ES process id.*2, number of ES processes:.*[2|4]'
        #p2 = 'relative ES process id.*4'
        split_output = output.splitlines();
        for line in split_output:
           line = line.strip();
           match1 = re.search(p1,line)
           #match2 = re.search(p2,line)
           if match1:
              non_prim_device = i
              return non_prim_device


def VerifyEnclosureInventorydetailsAthena(page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(page_cmd,HDD)
    page_output = run_command(cmd1)
    log.info(page_output)
    log.info("123456")
    pattern1="Element 0 descriptor: Athena G2"
    pattern2="Assembly PN: (\S+)"
    pattern3="Assembly SN: (\S+)"
    pattern4="Assembly Rev: (\S+)"
    ASM_PN=ASM_SN=ASM_REV=" "
    change_to_ESM_mode()
    cli_output=run_command_cli(CLI_cmd)
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
    pattern_to_check=".*{}.*{}.*{}{}.*".format(pattern1,ASM_PN,ASM_SN,ASM_REV)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,page_output)
    if match:
        log.success("Pattern check got passed as expected")
    else:
        log.fail("Pattern check failed")
        raise RuntimeError("Pattern match failed")

@logThis
def checkCansiterStatusAndVersionAthena(cmd,HDD,pattern,FW_version):
   cmd1 = "{} {}".format(cmd,HDD)
   output = run_command(cmd1)
   match=re.search(pattern,output)
   if match:
     log.success("Canister status check successful")
   else:
     log.fail("Canister status check  Failed")
     raise RuntimeError("Pattern match failed")
   pattern2=".*CELESTIC\s+P2523\s+(\S+).*"
   match2=re.search(pattern2,output)
   if match2:
       ses_version=match2.group(1)
   else:
        log.info("FW_version is not available")
        raise RuntimeError("FW_version is not available")
   log.info("version in ses_page is {}".format(ses_version))
   expect_version = "".join([i for i in FW_version.strip().split('.')[0:3]]) + '0'
   log.info("version in CLI is {}".format(expect_version))
   if ses_version == expect_version:
       log.success("FW Version match successful")
   else:
       log.fail("FW Version match fail")
       raise RuntimeError("FW Version match fail")
@logThis
def getFWVersionAthena(device):
    cmd = 'fru get'
    output = run_ESM_command(cmd)
    log.info(output)
    pattern = ".*FW Revision\s+(\S+).*"
#    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    match=re.search(pattern,output)
    if match:
        FW_Version=match.group(1)
    else:
        log.info("FW_version is not available")
        raise RuntimeError("FW_version is not available")
    log.info(FW_Version)
    return FW_Version

@logThis
def VerifycanisterdetailsAthena(page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(page_cmd,HDD)
    page_output = run_command(cmd1)
    pattern1="Element 0 descriptor: ESMA"
    pattern2="CAN ASM PN: (\S+)"
    pattern3="CAN ASM SN: (\S+)"
    pattern4="CAN ASM REV: (\S+)"
    pattern5="CPLD Revision Code: (\S+)"
    change_to_ESM_mode()
    cli_output=run_command_cli(CLI_cmd)
    ASM_PN=ASM_SN=ASM_REV=CPLD_0=" "
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
    match4=re.search(pattern5,cli_output)
    if match4:
        CPLD_0=match4.group(1)
        CPLD_0=CPLD_0.replace(".","")
        log.info(CPLD_0)
    pattern_to_check=".*{}.*{}.*{}{}.*{}.*".format(pattern1,ASM_PN,ASM_SN,ASM_REV,CPLD_0)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,page_output)
    if match:
        log.success("Pattern check got passed as expected")
    else:
        log.fail("Pattern check failed")
        raise RuntimeError("Pattern match failed")


@logThis
def verifyCLISetGetCLICommandAthena():
    change_to_ESM_mode()
    cmd_list = [ 'about', 'esm get', 'drv get','help','fan get','fan set -m e','fan set -p 35','fan set -l 1','fru get','log get','port get','power get','temp get','threshold get','debug on','errlog get','checklist get','mode get']
    err_count = 0
    fail_info_list = ['command not found', 'No such file or directory', 'cannot read file', 'Unknown command', 'not found', 'no space left on device', 'Command exited with non-zero status',"ERROR","Failure", "No such file","fail","CLI_UNKNOWN_CMD"]
    for cmd in cmd_list:
        output = run_ESM_command(cmd)
        log.info(output)
        for error in fail_info_list:
          match = re.search(error, output)
          if match:
              log.error("fail to get output, error info:{}".format(error))
              err_count += 1
        if err_count:
           err_count = 0
           raise RuntimeError('{} command execution fail'.format(cmd))
        else:
           log.info("Successfully executed  {} command".format(cmd))
    exit_ESM_mode()

@logThis
def temp_lm_upgrade_test_Athena(num,pattern):
    sg_device_1 = get_primary_device()
    set_cmd = "sg_ses --page=0x02 --index=coo,1 --set=3:3:1=" + str(num) + " " + sg_device_1
    device.sendMsg(set_cmd + '\r\n')
    get_cmd = "sg_ses --page=0x02 --index=coo,1 --get=3:3:1 " + sg_device_1
    output = run_command(get_cmd)
    count = 0
    for line in output.splitlines():
        line = line.strip()
        match = re.search(pattern, line)
        if match:
            count += 1
    if count == 1:
        log.success('Test pass!')
    else:
        raise RuntimeError("Set and get failed!")

@logThis
def savePage7AndPageAInfoAthena(HDD):
    page_info = {"page7" : {}, "pageA" : {}}
    log.info(HDD)
    page7_cmd = "{} {}".format(get_page7_cmd, HDD)
    pageA_cmd = "{} {}".format(get_pageA_cmd, HDD)
    page7_output = runAndCheck(page7_cmd, checking=fail_dict, is_negative=True, timeout=300)
    pageA_output = runAndCheck(pageA_cmd, checking=fail_dict, is_negative=True, timeout=300)
    page_info["page7"].update({ HDD : page7_output })
    page_info["pageA"].update({ HDD : pageA_output})
    return page_info

@logThis
def verify_download_status_without_activate(cmd,image,chk_cmd,status,HDD,device):
    log.info("Download image with mode e and verify status without activate")
    download_cmd = "{} -I {} -i 4 {}".format(cmd,image,HDD)
    log.info(download_cmd)
    chk_cmd = "{} {}".format(chk_cmd,HDD)
    log.info(chk_cmd)
    device_obj = Device.getDeviceObject(device)
    log_op=device_obj.executeCmd(download_cmd,timeout='360')
    #log_op= run_command(download_cmd,prompt='root@localhost',timeout=300)
    log.info(log_op)
    time.sleep(300)
    run_command(chk_cmd,prompt='root@localhost', timeout=300)
    status_op = run_command(chk_cmd,prompt='root@localhost', timeout=300)
    log.info(status_op)
    split_output = status_op.splitlines()
    count =0
    for line in split_output:
        match = re.search(status,line)
        if match:
            log.info("verification of download_status_without_activate is successfull")
            count=0
            break
        else:
            count = count +1
    if count !=0 :
        raise RuntimeError('verification of download_status_without_activate failed')

@logThis
def activate_fw_mode_f_athena(cmd,HDD,device):
    log.info("Activate Fw with mode f")
    cmd = "{} {}".format(cmd,HDD)
    run_command(cmd,prompt='localhost login:', timeout=900)

def VerifyEnclosureInventorydetailsAthena(page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(page_cmd,HDD)
    page_output = run_command(cmd1)
    log.info(page_output)
    log.info("123456")
    pattern1="Element 0 descriptor: Athena G2"
    pattern2="Assembly PN: (\S+)"
    pattern3="Assembly SN: (\S+)"
    pattern4="Assembly Rev: (\S+)"
    ASM_PN=ASM_SN=ASM_REV=" "
    change_to_ESM_mode()
    cli_output=run_command_cli(CLI_cmd)
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
    pattern_to_check=".*{}.*{}.*{}{}.*".format(pattern1,ASM_PN,ASM_SN,ASM_REV)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,page_output)
    if match:
        log.success("Pattern check got passed as expected")
    else:
        log.fail("Pattern check failed")
        raise RuntimeError("Pattern match failed")

@logThis
def checkCansiterStatusAndVersionAthena(cmd,HDD,pattern,FW_version):
   cmd1 = "{} {}".format(cmd,HDD)
   output = run_command(cmd1)
   match=re.search(pattern,output)
   if match:
     log.success("Canister status check successful")
   else:
     log.fail("Canister status check  Failed")
     raise RuntimeError("Pattern match failed")
   pattern2=".*CELESTIC\s+P2523\s+(\S+).*"
   match2=re.search(pattern2,output)
   if match2:
       ses_version=match2.group(1)
   else:
        log.info("FW_version is not available")
        raise RuntimeError("FW_version is not available")
   log.info("version in ses_page is {}".format(ses_version))
   expect_version = "".join([i for i in FW_version.strip().split('.')[0:3]]) + '0'
   log.info("version in CLI is {}".format(expect_version))
   if ses_version == expect_version:
       log.success("FW Version match successful")
   else:
       log.fail("FW Version match fail")
       raise RuntimeError("FW Version match fail")

@logThis
def getFWVersionAthena(device):
    cmd = 'fru get'
    output = run_ESM_command(cmd)
    log.info(output)
    pattern = ".*FW Revision\s+(\S+).*"
#    ProductTypeInfo = get_deviceinfo_from_config("UUT","platformType")
    match=re.search(pattern,output)
    if match:
        FW_Version=match.group(1)
    else:
        log.info("FW_version is not available")
        raise RuntimeError("FW_version is not available")
    log.info(FW_Version)
    return FW_Version

@logThis
def VerifycanisterdetailsAthena(page_cmd,CLI_cmd,HDD,device):
    cmd1 = "{} {}".format(page_cmd,HDD)
    page_output = run_command(cmd1)
    pattern1="Element 0 descriptor: ESMA"
    pattern2="CAN ASM PN: (\S+)"
    pattern3="CAN ASM SN: (\S+)"
    pattern4="CAN ASM REV: (\S+)"
    pattern5="CPLD Revision Code: (\S+)"
    change_to_ESM_mode()
    cli_output=run_command_cli(CLI_cmd)
    ASM_PN=ASM_SN=ASM_REV=CPLD_0=" "
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
    match4=re.search(pattern5,cli_output)
    if match4:
        CPLD_0=match4.group(1)
        CPLD_0=CPLD_0.replace(".","")
        log.info(CPLD_0)
    pattern_to_check=".*{}.*{}.*{}{}.*{}.*".format(pattern1,ASM_PN,ASM_SN,ASM_REV,CPLD_0)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,page_output)
    if match:
        log.success("Pattern check got passed as expected")
    else:
        log.fail("Pattern check failed")
        raise RuntimeError("Pattern match failed")


@logThis
def verifyCLISetGetCLICommandAthena():
    change_to_ESM_mode()
    cmd_list = [ 'about', 'esm get', 'drv get','help','fan get','fan set -m e','fan set -p 35','fan set -l 1','fru get','log get','port get','power get','temp get','threshold get','debug on','errlog get','checklist get','mode get']
    err_count = 0
    fail_info_list = ['command not found', 'No such file or directory', 'cannot read file', 'Unknown command', 'not found', 'no space left on device', 'Command exited with non-zero status',"ERROR","Failure", "No such file","fail","CLI_UNKNOWN_CMD"]
    for cmd in cmd_list:
        output = run_ESM_command(cmd)
        log.info(output)
        for error in fail_info_list:
          match = re.search(error, output)
          if match:
              log.error("fail to get output, error info:{}".format(error))
              err_count += 1
        if err_count:
           err_count = 0
           raise RuntimeError('{} command execution fail'.format(cmd))
        else:
           log.info("Successfully executed  {} command".format(cmd))
    exit_ESM_mode()

@logThis
def temp_lm_upgrade_test_Athena(num,pattern):
    sg_device_1 = get_primary_device()
    set_cmd = "sg_ses --page=0x02 --index=coo,-1 --set=3:3:1=" + str(num) + " " + sg_device_1
    device.sendMsg(set_cmd + '\r\n')
    get_cmd = "sg_ses --page=0x02 --index=coo,-1 --get=3:3:1 " + sg_device_1
    output = run_command(get_cmd)
    count = 0
    for line in output.splitlines():
        line = line.strip()
        match = re.search(pattern, line)
        if match:
            count += 1
    if count == 1:
        log.success('Test pass!')
    else:
        raise RuntimeError("Set and get failed!")

@logThis
def verifyFanCLISetGetCLICommand():
    change_to_ESM_mode()
    cmd_list = [ 'fan get','fan set -m e','fan set -p 55','fan set -l 1']
    err_count = 0
    fail_info_list = ['command not found', 'No such file or directory', 'cannot read file', 'Unknown command', 'not found', 'no space left on device', 'Command exited with non-zero status',"ERROR","Failure", "No such file","fail","CLI_UNKNOWN_CMD"]
    for cmd in cmd_list:
        output = run_ESM_command(cmd)
        log.info(output)
        for error in fail_info_list:
          match = re.search(error, output)
          if match:
              log.error("fail to get output, error info:{}".format(error))
              err_count += 1
        if err_count:
           err_count = 0
           raise RuntimeError('{} command execution fail'.format(cmd))
        else:
           log.info("Successfully executed  {} command".format(cmd))
    exit_ESM_mode()

@logThis
def verifyDriveDiskpowerOnOffAthena():
    change_to_ESM_mode()
    cmd = "drv get"
    output = run_ESM_command(cmd)
    b=output.splitlines()
    count=0
    pattern="(\S+).*Slot_(\d+).*OK"
    for i in b:
        match1=re.search(pattern,i)
        if match1:
            slot_num=match1.group(1)
            count=count+1
            break
    disable_cmd="drv set {} off".format(slot_num)
    enable_cmd="drv set {} on".format(slot_num)
    disable_cmd_pattern="{}.*Not Avaliable.*".format(slot_num)
    enable_cmd_pattern="{}.*OK.*".format(slot_num)
    if count==1:
       disable_cmd_output=run_ESM_command(disable_cmd)
       time.sleep(10)
       output = run_ESM_command(cmd)
       common_check_patern_2(output,disable_cmd_pattern, "PHY Disable Check", expect=True)
       enable_cmd_output=run_ESM_command(enable_cmd)
       time.sleep(30)
       output = run_ESM_command(cmd)
       common_check_patern_2(output,enable_cmd_pattern, "PHY Enable Check", expect=True)
    exit_ESM_mode()

@logThis
def Verify_element_Index_Page_0A(sg_device,page_cmd,output):
    get_cmd = page_cmd + " " + sg_device
    output1 = run_command(get_cmd)
    log.info(output1)
    match=re.search(output,output1)
    if match:
      log.success("Status of the page 0A check successful")
    else:
      log.fail("Status of the page 0A Failed")
      raise RuntimeError("Pattern match failed")

@logThis
def CheckDriverCountAthena():
    drv_count_cmd="lsscsi -g | grep -i disk  | wc -l"
    drv_count = run_command(drv_count_cmd)
    log.info(drv_count)
    match=re.search("12",drv_count)
    if match:
        log.success("Drive count check successful")
    else:
        raise RuntimeError("Drive count Error")

@logThis
def checkLogStatusAthena(device):
     cmd = 'log get' + "\r"
     output = run_command_cli(cmd)
     log.info(output)
     pattern1="Event Log.*: 1/510 entries"
     pattern2="Critical: 0/1"
     pattern3="Warning: 0/1"
     pattern4="Info: 1/1"
     common_check_patern_2(output, pattern1, "Event Log Check", expect=True)
     common_check_patern_2(output, pattern2, "Critical Log Check", expect=True)
     common_check_patern_2(output, pattern3, "Warning Log Check", expect=True)
     common_check_patern_2(output, pattern4, "Info Log Check", expect=True)

@logThis
def checkLogDetailsWithCLIAthena(cmd, HDD, device):
    cmd1 = "{} {}".format(cmd,HDD)
    output = run_command(cmd1)
    output=str(output)
    change_to_ESM_mode()
    cli_cmd = 'log get' + "\r"
    output1 = run_command_cli(cli_cmd)
    log.info(output1)
    p='Event Log.*:\s+(\S+)\/+510.*'
    match=re.search(p,output1)
    if match:
       a=match.group(1)
       log.info("The log count in ESM CLI is")
       log.info(a)
    c=output.splitlines()
    for line in c:
       pattern=' 00     13 00 00\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\s+(\S+).*'
       match1=re.search(pattern,line)
       if match1:
         b=match1.group(6)
         log.info("The log count in ses_page_13 is")
         log.info(b)
         e=str(parser_openbmc_lib.parse_hex_to_int(b))
         log.info(e)
    if(a==e):
        log.success("Log Count Matches")
    else:
        log.fail("Log Count Mismatch")
        raise RuntimeError("Log Count Mismatch")
    exit_ESM_mode()

@logThis
def verifyDevicePowerOffAthena(hdd, idx):
    poweron_status = { "0" : "^0$"}
    poweroff_status = { "1" : "^1$"}
    device_poweron_status = { "status: OK" : "Element \d+ descriptor:.*?\n.*?status: OK"}
    device_poweroff_status = {
            "status: Not available" : "Element \d+ descriptor:.*?\n.*?status: Not available"
            }
    poweroff_disks_cmd = "sg_ses --page=0x02 --index=arr,{} --set=3:4:1=1 {}".format(idx,hdd)
    get_disk_status_cmd = "sg_ses --page=0x02 --index=arr,{} --get=3:4:1 {}".format(idx, hdd)
    poweron_disks_cmd = "sg_ses --page=0x02 --index=arr,{} --clear=3:4:1=0  {}".format(idx,hdd)
    get_device_status_cmd = "sg_ses --page=0x02 {}".format(hdd)
    output = run_command(poweroff_disks_cmd)
    time.sleep(5)
    output1 = run_command([get_disk_status_cmd, get_device_status_cmd])
    output1 += output
    output = run_command(poweron_disks_cmd)
    time.sleep(90)
    output2 = run_command([get_disk_status_cmd, get_device_status_cmd])
    output2 += output
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=poweroff_status, check_output=output1)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=device_poweroff_status,
            check_output=output1, line_mode=False)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=poweron_status, check_output=output2)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=device_poweron_status,
            check_output=output2, line_mode=False)

@logThis
def verify_canister_VPD_information_Athena(read_cmd,get_cmd,HDD,CLI_output):
    log.info("Inside verify_canister_VPD_information")
    read_cmd1 = "{} {}".format(read_cmd,HDD)
    run_command(read_cmd1)
    truncate= "| cut -c 61-78"
    get_cmd1= "{} {} {}".format(get_cmd,HDD,truncate)
    output=run_command(get_cmd1)
    VPD_output=output.splitlines()
    test_string = "".join([line.strip('\n') for line in VPD_output])
    log.info(test_string)
    log.info(CLI_output)
    pattern=""".*--- ESMA ---.*
.*[General].*
.*Product Name:\s(\S+)\s(\S+).*"""
    Product_Name_1=Product_Name_2 =" "
    athena_Product_Name = " "
    match1=re.search(pattern,CLI_output)
    if match1:
        Product_Name_1=match1.group(1)
        log.info(Product_Name_1)
        Product_Name_2=match1.group(2)
        athena_Product_Name=Product_Name_1+" "+Product_Name_2
    match = test_string.find(athena_Product_Name)
    if match:
        log.info("athena_Product_Name Matches")
    else:
        log.info("canister_VPD Product_Name Match Failed")
        raise RuntimeError("canister_VPD Pattern match failed.Does not match with CLI output")
    pattern2=""".*[Board].*
.*Manufacture Name:.*
.*Part Number: (\S+).*
.*Serial Number: (\S+).*"""
    match2=re.search(pattern2,CLI_output)
    if match2:
        Board_Part_Number=match2.group(1)
        log.info(Board_Part_Number)
        Board_Serial_Number=match2.group(2)
        log.info(Board_Serial_Number)
    match = test_string.find(Board_Part_Number)
    if match:
        log.info("canister_VPD Board_Part_Number Matches")
    else:
        log.info("canister_VPD Board_Part_Number Match Failed")
        raise RuntimeError("canister_VPD Pattern match failed.Does not match with CLI output")
    match = test_string.find(Board_Serial_Number)
    if match:
        log.info("canister_VPD Board_Serial_Number Matches")
    else:
        log.info("canister_VPD Board_Serial_Number Match Failed")
        raise RuntimeError("canister_VPD Pattern match failed.Does not match with CLI output")
    pattern3=""".*[Revision].*
.*FW Revision (\S+).*
.*CFG Revision (\S+).*
.*CPLD Revision Code: (\S+).*"""
    match3=re.search(pattern3,CLI_output)
    if match3:
        Firmware_Revision=match3.group(1)
        expect_version = '0' + "".join([i for i in Firmware_Revision.strip().replace('.',' 0')[0:8]])
        log.info(expect_version)
    get_cmd= "{} {}".format(get_cmd,HDD)
    output1=run_command(get_cmd)
    a=output1.splitlines()
    for line in a:
       pattern="^ 40     .*"
       log.info(line)
       match1=re.search(pattern,line)
       if match1:
            match2=re.search(expect_version,line)
            if match2:
                 log.success("canister_VPD Firmware Version check got passed as expected.Match with CLI output success.")
                 break
            else:
                 log.fail("canister_VPD Firmware Version check failed")
                 break

@logThis
def verify_PSU_VPD_information_Athena(read_cmd,get_cmd,HDD,CLI_output):
    log.info("Inside verify_PSU_VPD_information")
    read_cmd1 = "{} {}".format(read_cmd,HDD)
    run_command(read_cmd1)
    truncate= "| cut -c 61-78"
    get_cmd1= "{} {} {}".format(get_cmd,HDD,truncate)
    output=run_command(get_cmd1)
    log.info(output)
    VPD_output=output.splitlines()
    test_string = "".join([line.strip('\n') for line in VPD_output])
    log.info(test_string)
    log.info(CLI_output)
    pattern1 =""".*--- Power Supply 0 ---.*
.*PS Type:.(\S+).*
.*PS Manufacturer:.(\S+).*
.*PS Serial Number:.(\S+).*
.*PS Part Number:.(\S+).*
.*PS Hardware Version: (\S+).*
.*PS Firmware Version:.(\S+).*"""
    match1=re.search(pattern1,CLI_output)
    if match1:
        Manufacture_Name=match1.group(2)
        Manufacture_PN=match1.group(4)
    log.info(Manufacture_Name)
    log.info(Manufacture_PN)
    pattern_to_check=".*{}.*{}.*".format(Manufacture_Name,Manufacture_PN)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,test_string)
    if match:
        log.success("PSU_VPD Pattern check got passed as expected.Match with CLI output success.")
    else:
        log.fail("PSU_VPD Pattern check failed")
        raise RuntimeError("PSU_VPD Pattern match failed.Does not match with CLI output")

@logThis
def verify_All_VPD_information_Athena(read_cmd,get_cmd,HDD,CLI_output):
    log.info("Insde verify_All_VPD_information")
    read_cmd1 = "{} {}".format(read_cmd,HDD)
    run_command(read_cmd1)
    truncate= "| cut -c 61-78"
    get_cmd1= "{} {} {}".format(get_cmd,HDD,truncate)
    output=run_command(get_cmd1)
    log.info(output)
    VPD_output=output.splitlines()
    test_string = "".join([line.strip('\n') for line in VPD_output])
    log.info(test_string)
    log.info(CLI_output)
    log.info("Canister VPD")
    pattern=""".*--- ESMA ---.*
.*[General].*
.*Product Name:\s(\S+)\s(\S+).*"""
    match1=re.search(pattern,CLI_output)
    if match1:
        Product_Name_1=match1.group(1)
        Product_Name_2=match1.group(2)
        Product_Name=Product_Name_1+" "+Product_Name_2
        log.info(Product_Name)
    match = test_string.find(Product_Name)
    if match:
        log.info("Canister VPD Product_Name Matches")
    else:
        log.info("Canister VPD Product_Name Match Failed")
        raise RuntimeError("Canister VPD Pattern match failed.Does not match with CLI output")
    pattern2=""".*[Board].*
.*Manufacture Name:.*
.*Part Number: (\S+).*
.*Serial Number: (\S+).*"""
    match2=re.search(pattern2,CLI_output)
    if match2:
        Board_Part_Number=match2.group(1)
        log.info(Board_Part_Number)
        Board_Serial_Number=match2.group(2)
        log.info(Board_Serial_Number)
    match = test_string.find(Board_Part_Number)
    if match:
        log.info("Canister VPD Board_Part_Number Matches")
    else:
        log.info("Canister VPD Board_Part_Number Match Failed")
        raise RuntimeError("Canister VPD Pattern match failed.Does not match with CLI output")
    match = test_string.find(Board_Serial_Number)
    if match:
        log.info("Canister VPD Board_Serial_Number Matches")
    else:
        log.info("Canister VPD Board_Serial_Number Match Failed")
        raise RuntimeError("Canister VPD Pattern match failed.Does not match with CLI output")
    log.info("MidPlane VPD")
    pattern1="Midplane Product Name: (\S+)"
    pattern2="Midplane Part Number: (\S+)"
    pattern3="Midplane Serial Number: (\S+)"
    pattern4="Midplane HW EC LVL: (\S+)"
    pattern5="Product Name: (\S+)"
    pattern6="Product Part: (\S+)"
    pattern7="Product Serial Number: (\S+)"
    pattern8="Product Version: (\S+)"
    match1=re.search(pattern1,CLI_output)
    if match1:
        Midplane_Product_Name=match1.group(1)
        log.info(Midplane_Product_Name)
    match2=re.search(pattern2,CLI_output)
    if match2:
        Midplane_Part_Number=match2.group(1)
        log.info(Midplane_Part_Number)
    match3=re.search(pattern3,CLI_output)
    if match3:
        Midplane_Serial_Number=match3.group(1)
        log.info(Midplane_Serial_Number)
    match4=re.search(pattern4,CLI_output)
    if match4:
        Midplane_HW_EC_LVL=match4.group(1)
        log.info(Midplane_HW_EC_LVL)
    match5=re.search(pattern5,CLI_output)
    if match5:
        Product_Name=match5.group(1)
        log.info(Product_Name)
    match6=re.search(pattern6,CLI_output)
    if match6:
        Product_Part=match6.group(1)
        log.info(Product_Part)
    match7=re.search(pattern7,CLI_output)
    if match7:
        Product_Serial_Number=match7.group(1)
        log.info(Product_Serial_Number)
    match8=re.search(pattern8,CLI_output)
    if match8:
        Product_Version=match8.group(1)
        log.info(Product_Version)
    pattern_to_check=".*{}.*{}.*{}.*{}.*{}.*{}.*{}.*{}.*".format(Midplane_Product_Name,Midplane_Part_Number,Midplane_Serial_Number,Midplane_HW_EC_LVL,Product_Name,Product_Part,Product_Serial_Number,Product_Version)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,test_string)
    if match:
        log.success("MidPlane VPD Pattern check got passed as expected.Match with CLI output success.")
    else:
        log.fail("MidPlane VPD Pattern check failed")
        raise RuntimeError("MidPlane VPD Pattern match failed.Does not match with CLI output")
    log.info("PSU 0 VPD")
    pattern1 =""".*--- Power Supply 0 ---.*
.*PS Type:.(\S+).*
.*PS Manufacturer:.(\S+).*
.*PS Serial Number:.(\S+).*
.*PS Part Number:.(\S+).*
.*PS Hardware Version:.(\S+).*
.*PS Firmware Version:.(\S+).*"""
    match1=re.search(pattern1,CLI_output)
    if match1:
        Manufacture_Name=match1.group(2)
        Manufacture_PN=match1.group(4)
        PS_Serial_Number=match1.group(3)
        PS_Firmware_Version=match1.group(6)
    log.info(Manufacture_Name)
    log.info(Manufacture_PN)
    log.info(PS_Serial_Number)
    log.info(PS_Firmware_Version)
    pattern_to_check=".*{}.*{}.*{}.*{}.*".format(Manufacture_Name,Manufacture_PN,PS_Serial_Number,PS_Firmware_Version)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,test_string)
    if match:
        log.success("PSU 0 Pattern check got passed as expected.Match with CLI output success.")
    else:
        log.fail("PSU 0 Pattern check failed")
        raise RuntimeError("PSU 0 Pattern match failed.Does not match with CLI output")
    log.info("PSU 1 VPD")
    pattern1 =""".*--- Power Supply 1 ---.*
.*PS Type:.(\S+).*
.*PS Manufacturer:.(\S+).*
.*PS Serial Number:.(\S+).*
.*PS Part Number:.(\S+).*
.*PS Hardware Version:.(\S+).*
.*PS Firmware Version:.(\S+).*"""
    match1=re.search(pattern1,CLI_output)
    if match1:
        Manufacture_Name=match1.group(2)
        Manufacture_PN=match1.group(4)
        PS_Serial_Number=match1.group(3)
        PS_Firmware_Version=match1.group(6)
    log.info(Manufacture_Name)
    log.info(Manufacture_PN)
    log.info(PS_Serial_Number)
    log.info(PS_Firmware_Version)
    pattern_to_check=".*{}.*{}.*{}.*{}.*".format(Manufacture_Name,Manufacture_PN,PS_Serial_Number,PS_Firmware_Version)
    log.info(pattern_to_check)
    match=re.search(pattern_to_check,test_string)
    if match:
        log.success("PSU 1 Pattern check got passed as expected.Match with CLI output success.")
    else:
        log.fail("PSU 1 Pattern check failed")
        raise RuntimeError("PSU 1 Pattern match failed.Does not match with CLI output")


@logThis
def setAndVerifyUWAthena():
    log.info("Inside  UW")
    change_to_ESM_mode()
    cmd="temp get" + "\r"
    output = run_command_cli(cmd)
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
    modify_value=random.randint(0,int(reading_value)-1)
    clr_cmd="log clear" + "\r"
    run_command_cli(clr_cmd)
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],modify_value,list_threshold[3])  + "\r"
    output2=run_command_cli(cmd2)
    time.sleep(15)
    output3=run_command_cli(cmd)
    log.info(output3)
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
        raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("UW verfication successfull")
    cmd3="log get" + "\r"
    output5=run_command_cli(cmd3)
    output6=output5.splitlines()
    log.info(output5)
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
       raise RuntimeError("Log not updated for UW")
    else:
        log.info("UW verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3])  + "\r"
    output=run_command_cli(cmd2)
    exit_ESM_mode()

@logThis
def setAndVerifyUCAthena():
    log.info("Inside  UC")
    change_to_ESM_mode()
    cmd="temp get" + "\r"
    output = run_command_cli(cmd)
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
    output2=run_command_cli(cmd2)
    time.sleep(15)
    output3=run_command_cli(cmd)
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
        raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("UC verfication successfull")
    cmd3="log get" + "\r"
    output5=run_command_cli(cmd3)
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
       raise RuntimeError("Log not updated for UC")
    else:
        log.info("UC verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3]) + "\r"
    output=run_command_cli(cmd2)
    exit_ESM_mode()

@logThis
def setAndVerifyLWAthena():
    log.info("Inside  LW")
    change_to_ESM_mode()
    cmd="temp get" + "\r"
    output = run_command_cli(cmd)
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
    output2=run_command_cli(cmd2)
    time.sleep(15)
    output3=run_command_cli(cmd)
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
        raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("LW verfication successfull")
    cmd3="log get" + "\r"
    output5=run_command_cli(cmd3)
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
       raise RuntimeError("Log not updated for LW")
    else:
        log.info("LW verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3]) + "\r"
    output=run_command_cli(cmd2)
    exit_ESM_mode()

@logThis
def setAndVerifyLCAthena():
    log.info("Inside  LC")
    change_to_ESM_mode()
    cmd="temp get" + "\r"
    output = run_command_cli(cmd)
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
    output2=run_command_cli(cmd2)
    time.sleep(15)
    output3=run_command_cli(cmd)
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
        raise RuntimeError("Threshold  value is not modified as expected")
    else:
        log.info("LC verfication successfull")
    cmd3="log get" + "\r"
    output5=run_command_cli(cmd3)
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
       raise RuntimeError("Log not updated for LC")
    else:
        log.info("LC verfication in log  successfull")
    cmd1="threshold set"
    cmd2="{} {} {} {} {} {}".format(cmd1,temp_id,list_threshold[0],list_threshold[1],list_threshold[2],list_threshold[3]) + "\r"
    output=run_command_cli(cmd2)
    exit_ESM_mode()

@logThis
def verifyCLISetGetCommandWithDelaysAthena(delay_seconds):
    change_to_ESM_mode()
    cmd_list = [
        'help', 'help about', 'about', 'help esm', 'esm get', 'esm get 0', 'esm get 1',
        'help drv', 'drv get', 'drv set 0 off', 'drv get', 'drv set 0 on', 'drv get',
        'help fan', 'fan get', 'fan set -m i', 'fan get', 'fan set -m e', 'fan get',
        'fan set -p 60', 'fan get', 'fan set -l 1', 'fan get', 'help fru', 'fru get',
        'help log', 'log get', 'log get -s i', 'log get -s w', 'log get -s c', 'log get p',
        'log get -s i p', 'log get -s w p', 'log get -s c p', 'log filter get -s',
        'log filter set -s 1', 'log filter set -s 2', 'log filter set -s 2', 'log clear', 'log clear p',
        'help port', 'port get', 'help power', 'power get', 'help temp', 'temp get',
        'help threshold', 'threshold get', 'help debug', 'debug on', 'debug on -l 1',
        'debug on -l 2', 'debug on -l 3', 'debug off', 'help checklist', 'checklist get',
        'help pardrv', 'pardrv get', 'help mode', 'mode get', 'mode set B', 'help led',
        'led get', 'led set 1 on', 'led set 1 fast', 'led set 1 slow', 'led set 1 off',
        'help vpd', 'vpd get -d 0', 'vpd get -d 1', 'vpd get -c 0', 'vpd get -c 1',
        'vpd get -p 0', 'vpd get -p 1', 'help config']
    err_count = 0
    fail_info_list = ['Unknown command', 'not found', "CLI_UNKNOWN_CMD",'unknown_cmd',
        'TAMFW_ERR_INVALID_PARAMETERS','DEV_DRV_ERR_FUNC_NOT_SUPPORT']
    for cmd in cmd_list:
        output = run_ESM_command(cmd)
        time.sleep(int(delay_seconds))
        log.info(output)
        for error in fail_info_list:
          match = re.search(error, output)
          if match:
              log.error("fail to get output, error info:{}".format(error))
              err_count += 1
        if err_count:
           err_count = 0
           raise RuntimeError('{} command execution fail'.format(cmd))
        else:
           log.info("Successfully executed  {} command".format(cmd))
    output = run_command_cli('config get' + '\r', prompt='Select \>')
    time.sleep(int(delay_seconds))
    log.info(output)
    for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
    if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format('config get'))
    else:
        log.info("Successfully executed  {} command".format('config get'))
    run_command_cli('1' + '\r', prompt='ESM\s\S\_0\s=\>')
    time.sleep(int(delay_seconds))
    output = run_command_cli('config reset' + '\r', prompt='Select \>')
    time.sleep(int(delay_seconds))
    log.info(output)
    for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
    if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format('config reset'))
    else:
        log.info("Successfully executed  {} command".format('config reset'))
    run_command_cli('1' + '\r', prompt='ESM\s\S\_0\s=\>')
    time.sleep(int(delay_seconds))
    output = run_command_cli('fru set -encl' + '\r', prompt='New:')
    time.sleep(int(delay_seconds))
    for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
    if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format('fru set -encl'))
    else:
        log.info("Successfully executed  {} command".format('fru set -encl'))
    for i in range(1, 32):
        output = run_command_cli('\r', prompt='New:')
        time.sleep(int(delay_seconds))
        for error in fail_info_list:
            match = re.search(error, output)
            if match:
                log.error("fail to get output, error info:{}".format(error))
                err_count += 1
        if err_count:
            err_count = 0
            raise RuntimeError('{} command execution fail'.format('fru set -encl'))
        else:
            log.info("Successfully executed  {} command".format('fru set -encl'))
    run_command_cli('\r', prompt='ESM\s\S\_0\s=\>')
    time.sleep(int(delay_seconds))
    output = run_command_cli('fru set -c' + '\r', prompt='New:')
    time.sleep(int(delay_seconds))
    for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
    if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format('fru set -c'))
    else:
        log.info("Successfully executed  {} command".format('fru set -c'))
    for i in range(1, 64):
        output = run_command_cli('\r', prompt='New:')
        time.sleep(int(delay_seconds))
        for error in fail_info_list:
            match = re.search(error, output)
            if match:
                log.error("fail to get output, error info:{}".format(error))
                err_count += 1
        if err_count:
            err_count = 0
            raise RuntimeError('{} command execution fail'.format('fru set -c'))
        else:
            log.info("Successfully executed  {} command".format('fru set -c'))
    run_command_cli('\r', prompt='ESM\s\S\_0\s=\>')
    time.sleep(int(delay_seconds))
    output = run_command_cli('fru set -p' + '\r', prompt='New:')
    time.sleep(int(delay_seconds))
    for error in fail_info_list:
        match = re.search(error, output)
        if match:
            log.error("fail to get output, error info:{}".format(error))
            err_count += 1
    if err_count:
        err_count = 0
        raise RuntimeError('{} command execution fail'.format('fru set -p'))
    else:
        log.info("Successfully executed  {} command".format('fru set -p'))
    for i in range(1, 4):
        output = run_command_cli('\r', prompt='New:')
        time.sleep(int(delay_seconds))
        for error in fail_info_list:
            match = re.search(error, output)
            if match:
                log.error("fail to get output, error info:{}".format(error))
                err_count += 1
        if err_count:
            err_count = 0
            raise RuntimeError('{} command execution fail'.format('fru set -p'))
        else:
            log.info("Successfully executed  {} command".format('fru set -p'))
    run_command_cli('\r', prompt='ESM\s\S\_0\s=\>')
    exit_ESM_mode()

@logThis
def verifyCLIInvalidIncorrectCommandAthena():
    change_to_ESM_mode()
    cmd_list = [
        'about help', 'aboutt', 'drv get 90', 'esm get 2', 'fan get -m i', 'fan get i',
        'fan get -l 0', 'fan set', 'fan set -l 8', 'fan set -p 110', 'fan set 50',
        'fru get -encl', 'fru get -c', 'fru get -p', 'fru set -enclosure', 'fru set -can',
        'fru set -ps', 'fru set', 'fru set -encl 0', 'fru set -c 0', 'fru set -p 0', 'log get -s',
        'log filter get', 'log filter get -s 0', 'log filter set -s 3', 'port gfet', 'reset 5',
        'reset 7', 'temp get t0', 'threshold get t0', 'mode set a', 'config get 1',
        'debug on -l 0', 'debug -l i', 'led set 60 on', 'vpd get -d 0 0 257']
    expect_error = 0
    fail_info_list = ["CLI_UNKNOWN_CMD", 'unknown_cmd', 'Bad parameter specified'
        'TAMFW_ERR_INVALID_PARAMETERS','DEV_DRV_ERR_FUNC_NOT_SUPPORT']
    for cmd in cmd_list:
        output = run_ESM_command(cmd)
        log.info(output)
        for error in fail_info_list:
          match = re.search(error, output)
          if match:
              log.info("Successfully rerurn error info:{}".format(error))
              expect_error += 1
        if expect_error == "1":
           log.info("Successfully executed  {} command, rerurn error info:{}".format(cmd, error))
