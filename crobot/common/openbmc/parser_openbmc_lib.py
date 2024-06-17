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
from dataStructure import nestedDict, parser
from SensorCsv import SensorCsv
from pkg_resources import parse_version
import re
import json
import Logger as log
from Device import Device
import DeviceMgr

deviceObj = DeviceMgr.getDevice()

START_GETTY_MSG = r'(\/bin\/start_getty: line\s\d+:\s+\d+ Quit.*{setsid:-}.*{getty}.*\d)|(INIT:.*respawning too fast:\s.+\w)'

def parse_current_boot_flash(output):
    log.debug('Entering procedure parse_current_boot_flash with args : %s\n' %(str(locals())))
    outDict = parser()
    # Current Boot Code Source: Master Flash
    p1 = r'^Current Boot Code Source: (.*) Flash'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['Current Boot'] = match.group(1)
            break
    log.info(outDict)
    return outDict

def parse_current_bios_flash(output):
    log.debug('Entering procedure parse_current_bios_flash with args : %s\n' %(str(locals())))
    outDict = parser()
    # Current Boot Code Source: Master Flash
    p1 = r'(master|slave)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['Current Bios'] = match.group(1)
            break
    log.info(outDict)
    return outDict

def parse_openbmc_version(output):
    log.debug('Entering procedure parse_openbmc_version with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'OpenBMC Release \w+-v?(.*)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['BMC Version'] = match.group(1)
            break
    log.info(outDict)
    return outDict

def parse_fw_version(output):
    log.debug('Entering procedure parse_fw_version with args : %s\n' %(str(locals())))
    outDict = parser()
    output = re.sub(START_GETTY_MSG, '', output)
    # p1 = r'(.*): (v?(.*))'
    p1 = r'(.+): (.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = match.group(1)
            outDict[key] = match.group(2)
    log.info(outDict)
    return outDict

def parse_dmidecode_bios_version(output):
    log.debug('Entering procedure parse_dmidecode_bios_version with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'^(XG1_.*)'
    if 'minipack3' in deviceObj.name or 'minerva' in deviceObj.name:
        p1 = r'^(NL.*)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['BIOS Version'] = match.group(1)
            break
    log.info(outDict)
    return outDict

def parse_th3_version(output):
    log.debug('Entering procedure parse_th3_version with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'PCIe FW loader version: (.+)'
    p2 = r'PCIe FW version: (.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        match2 = re.search(p2, line)
        if match:
            outDict['PCIe FW loader version'] = match.group(1)
        elif match2:
            outDict['PCIe FW version'] = match2.group(1)
    log.info(outDict)
    return outDict

def parse_power_status(output):
    log.debug('Entering procedure parse_power_status with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'Microserver power is (.+)'
    outDict['power status'] = ''
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['power status'] = match.group(1)
            break
    log.info(outDict)
    return outDict

def parse_power_control(output):
    log.debug('Entering procedure parse_power_control with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'Power (.+) microserver.*(Done)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = 'power ' + match.group(1)
            outDict[key] = match.group(2)
            break
    log.info(outDict)
    return outDict

def parse_power_status2(output):
    log.debug('Entering procedure parse_power_status2 with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'Microserver power is\s*(.+)'
    outDict['power status'] = ''
    match = re.search(p1, output)
    if match:
        outDict['power status'] = match.group(1).strip()
    log.info(outDict)
    return outDict

def parse_power_control2(output):
    log.debug('Entering procedure parse_power_control2 with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'Power (.+) microserver\s*...\s*(.+)'
    p2 = r'uServer (.+) already on(.+)'
    p3 = r'Power (.+) x86.*... (.+)'
    outDict['power control'] = ''
    match = re.search(p1, output)
    match2 = re.search(p2, output)
    match3 = re.search(p3, output)
    if match:
        outDict['power control'] = match.group(2).strip()
    if match2:
        outDict['power control'] = match2.group(2).strip()
    if match3:
        outDict['power control'] = match3.group(2).strip()
    log.info(outDict)
    return outDict

def parse_get_fan_speed(output):
    log.debug('Entering procedure parse_get_fan_speed with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'Fan (\d+) RPMs: (\d+), (\d+), \((\d+)\%\)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            fan_name = 'Fan ' + match.group(1)
            outDict[fan_name + ' front'] = match.group(2)
            outDict[fan_name + ' rear'] = match.group(3)
            outDict[fan_name + ' percentage'] = match.group(4)
    log.info(outDict)
    return outDict

def parse_set_fan_speed(output):
    log.debug('Entering procedure parse_set_fan_speed with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'Successfully set fan (\d+) speed to (\d+)\%'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            fan_name = 'Fan ' + match.group(1)
            outDict[fan_name + ' percentage'] = match.group(2)
    log.info(outDict)
    return outDict

def parse_simple_keyword(regex, output):
    log.debug('Entering procedure parse_simple_keyword with args : %s\n' %(str(locals())))
    match = re.search(regex, output)
    if match:
        log.success("Found: %s"%(match.group(0)))
        return match.group(0)
    log.fail("Not found keyword: %s"%(regex))
    return ""

def parse_simple_keyword_cr(regex, output):
    log.debug('Entering procedure parse_simple_keyword_cr with args : %s\n' %(str(locals())))
    match = re.search(regex, output)
    if match:
        log.fail("Found fail keyword: %s" % (regex))
    log.success("Run the command success!")
    return ""

def parse_gpio_data(output):
    log.debug('Entering procedure parse_gpio_data with args : %s\n' %(str(locals())))
    p1 = r'^(0|1)$'
    p2 = r'^(in|out)$'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        match2 = re.search(p2, line)
        if match:
            parsed_data = match.group(1)
            break
        if match2:
            parsed_data = match2.group(1)
            break
        parsed_data = ''
    log.info('gpio data: %s'%(parsed_data))
    return parsed_data

def parse_watchdog_timer(output):
    log.debug('Entering procedure parse_watchdog_timer with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'WDT(\d) Timeout Count:  (\d+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = 'WDT%s'%(match.group(1))
            outDict[key] = int(match.group(2))
    log.info(outDict)
    return outDict

def parse_eeprom(output):
    log.debug('Entering procedure parse_eeprom with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'(\S+)\s+=\s(.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = match.group(1)
            outDict[key] = match.group(2)
    log.info(outDict)
    return outDict

def parse_eeprom_type(output):
    log.debug('Entering procedure parse_eeprom_type with args : %s\n' %(str(locals())))
    p1 = r'(.+) EEPROM ...'
    eeprom_type = None
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            eeprom_type = match.group(1)
            break
    return eeprom_type

def parse_psu_util(output):
    log.debug('Entering procedure parse_psu_util with args : %s\n' %(str(locals())))
    outDict = parser()
    output = re.sub(START_GETTY_MSG, '', output)
    p1 = r'^(\w.+): (.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = match.group(1).strip()
            outDict[key] = match.group(2).strip()
    log.info(outDict)
    return outDict

def parse_json_string(output):
    log.debug('Entering procedure parse_json_string with args : %s\n' %(str(locals())))
    output = re.sub(START_GETTY_MSG, '', output)
    p1 = r'(^{$)'
    p2 = r'(^}$)'
    json_str = ""
    index_i = 0
    index_e = 0
    line_list = output.splitlines()
    for i, line in enumerate(line_list):
        match = re.search(p1, line)
        if match:
            # print(match.group(1))
            index_i = i
            continue
        match2 = re.search(p2, line)
        if match2:
            # print(match2.group(1))
            index_e = i
            continue
    json_str = '\n'.join(line_list[index_i:index_e+1])
    return json_str

def parse_json_string2(output):
    log.debug('Entering procedure parse_json_string2 with args : %s\n' %(str(locals())))
    output = re.sub(START_GETTY_MSG, '', output)
    p1 = r'{'
    p2 = r'}'
    index_i = output.find(p1)
    index_e = output.rfind(p2)
    json_str = output[index_i:index_e+1]
    return json_str


def parse_json_object(json_str):
    log.debug('Entering procedure parse_json_object with args : %s\n' %(str(locals())))
    parsed_json = json.loads(json_str)
    log.debug(json.dumps(parsed_json, indent=4))
    return parsed_json

def parse_util(output):
    log.debug('Entering procedure parse_util with args : %s\n' %(str(locals())))
    outDict = parser()
    output = re.sub(START_GETTY_MSG, '', output)
    p1 = r'(.+): (.+)'
    err_msg = r'([E|e]rror)|(No such file or directory)|(Fail.*)|(command not found)'
    err_match = re.search(err_msg, output)
    if err_match:
        log.fail("Found error: %s"%(err_match.group(0)))
        return outDict
    for line in output.splitlines():
        line = line.strip()
        if '---------------' in line:
            continue
        match = re.search(p1, line)
        if match:
            key = match.group(1).strip()
            outDict[key] = match.group(2).strip()
    log.info(outDict)
    return outDict

def parse_fan_util(output):
    log.debug('Entering procedure parse_fan_util with args : %s\n' %(str(locals())))
    outDict = {}
    output = re.sub(START_GETTY_MSG, '', output)
    p1 = r'(Fan.+eeprom):'
    p2 = r'(.+): (.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            eeprom_name = match.group(1)
            outDict[eeprom_name] = {}
            continue
        match2 = re.search(p2, line)
        if match2 and eeprom_name:
            key = match2.group(1)
            outDict[eeprom_name][key] = match2.group(2).strip()
            continue
    log.info(outDict)
    return outDict

def parse_sensor_util(output):
    log.debug('Entering procedure parse_sensor_util with args : %s\n' %(str(locals())))
    outDict = parser()
    # p1 = r'(\S+).*:\s+(.+) \w+'
    p1 = r'(.+)\s+(\S+)\s:\s+(.+) \w+'
    p2 = r'(\w+) is not present!'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        ##0625 add the judge if the device is not present.
        match2 = re.search(p2, line)
        if match2:
            log.info('%s is not present, so skip the device.'% match2.group(1))
            break
        if match:
            key = match.group(1).strip()
            outDict[key] = match.group(3).strip()
            continue
    log.info(outDict)
    return outDict

def parse_sensor_util_force(output):
    log.debug('Entering procedure parse_sensor_util_force with args : %s\n' %(str(locals())))
    outDict = {}
    # p1 = r'(\S+)\s+(\S+)\s:\s+(.+) (\w+).+\((\w+)\)'
    p1 = r'(.+)\s+(\S+)\s:\s+((.+) (\w+)|(\w+)).+\((\w+)\)'
    p2 = r'(\w+) is not present!'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        match2 = re.search(p2, line)
        if match2:
            log.info('%s is not present, so skip the device.' % match2.group(1))
            break
        if match:
            key = match.group(1).strip()
            outDict[key] = {}
            if match.group(4):
                outDict[key]['value'] = match.group(4).strip()
                outDict[key]['unit'] = match.group(5).strip()
            else:
                outDict[key]['value'] = match.group(3).strip()
                outDict[key]['unit'] = match.group(6).strip()
            outDict[key]['status'] = match.group(7).strip()
    log.info(outDict)
    return outDict

def parse_sensor_util_threshold(output):
    log.debug('Entering procedure parse_sensor_util_threshold with args : %s\n' %(str(locals())))
    outDict = {}
    # p1 = r'(\S+).+ (\w+).+\((\w+)\)'
    p1 = r'(.+)\s+(\S+)\s:\s+((.+) (\w+)|(\w+)).+\((\w+)\)'
    # p1 += r'.+UCR: (\S+).+UNC: (\S+).+UNR: (\S+).+LCR: (\S+).+LNC: (\S+).+LNR: (\S+)'
    p1 += r'(.+UCR: (\S+).+UNC: (\S+).+UNR: (\S+).+LCR: (\S+).+LNC: (\S+).+LNR: (\S+))?'
    p2 = r'(\w+) is not present!'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        match2 = re.search(p2, line)
        if match2:
            log.info('%s is not present, so skip the device.' % match2.group(1))
            break
        if match:
            key = match.group(1).strip()
            outDict[key] = {}
            if match.group(4):
                outDict[key]['value'] = match.group(4).strip()
                outDict[key]['unit'] = match.group(5).strip()
            else:
                outDict[key]['value'] = match.group(3).strip()
                outDict[key]['unit'] = match.group(6).strip()
            outDict[key]['status'] = match.group(7).strip()
            if match.group(8):
                SensorObj = SensorCsv()
                outDict[key]['UCR'] = SensorObj.string_to_float(match.group(9).strip())
                outDict[key]['UNC'] = SensorObj.string_to_float(match.group(10).strip())
                outDict[key]['UNR'] = SensorObj.string_to_float(match.group(11).strip())
                outDict[key]['LCR'] = SensorObj.string_to_float(match.group(12).strip())
                outDict[key]['LNC'] = SensorObj.string_to_float(match.group(13).strip())
                outDict[key]['LNR'] = SensorObj.string_to_float(match.group(14).strip())
            else:
                outDict[key]['UCR'] = ''
                outDict[key]['UNC'] = ''
                outDict[key]['UNR'] = ''
                outDict[key]['LCR'] = ''
                outDict[key]['LNC'] = ''
                outDict[key]['LNR'] = ''
    log.info(outDict)
    return outDict

def parse_sensor_util_history(output):
    log.debug('Entering procedure parse_sensor_util_history with args : %s\n' %(str(locals())))
    outDict = {}
    # p1 = r'(\S+).+min = (\S+),.+average = (\S+),.+max = (\S+)'
    p1 = r'(.+)\s+\(.+min = (\S+),.+average = (\S+),.+max = (\S+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = match.group(1).strip()
            outDict[key] = {}
            outDict[key]['min'] = match.group(2).strip()
            outDict[key]['max'] = match.group(3).strip()
            outDict[key]['average'] = match.group(4).strip()
    log.info(outDict)
    return outDict

def parse_bic_gpio_config_util(output):
    log.debug('Entering procedure parse_bic_gpio_config_util with args : %s\n' %(str(locals())))
    outDict = {}
    p1 = r'gpio_config for pin#(\d+) \((\S+)\):'
    p2 = r'Direction: (.+),\s+Interrupt: (.+),\s+Trigger: (.+),\s+Edge: (.+)'
    line_list = output.splitlines()
    for i in range(0, len(line_list)-1, 2):
        gpio_name_line = line_list[i]
        gpio_info_line = line_list[i+1]
        match1 = re.search(p1, gpio_name_line)
        if match1:
            pin = match1.group(1)
            name = match1.group(2)
            outDict[pin] = {}
            outDict[pin]['name'] = name
        match2 = re.search(p2, gpio_info_line)
        if match2:
            outDict[pin]['Direction'] = match2.group(1)
            outDict[pin]['Interrupt'] = match2.group(2)
            outDict[pin]['Trigger'] = match2.group(3)
            outDict[pin]['Edge'] = match2.group(4)
    log.info(outDict)
    return outDict

def parse_bic_read_sensor(output):
    log.debug('Entering procedure parse_bic_read_sensor with args : %s\n' %(str(locals())))
    outDict = {}
    p1 = r'sensor#(\d+):\s+value: (.+), flags: (.+), status: (.+), ext_status: (.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            num = match.group(1)
            outDict[num] = {}
            outDict[num]['value'] = match.group(2)
            outDict[num]['flags'] = match.group(3)
            outDict[num]['status'] = match.group(4)
            outDict[num]['ext_status'] = match.group(5)
    log.info(outDict)
    return outDict

def parse_ipmitool_mc_info(output):
    log.debug('Entering procedure parse_ipmitool_mc_info with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'^(.+)\s+: (.+)$'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = match.group(1).strip()
            outDict[key] = match.group(2).strip()
            continue
    log.info(outDict)
    return outDict

def parse_oem_rsp_code(output):
    log.debug('Entering procedure parse_oem_rsp_code with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'Unable to send RAW command.+rsp=([\d\w]+)\):\s(.+)'
    p2 = r'.*invalid'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['code'] = match.group(1).strip()
            outDict['message'] = match.group(2).strip()
            continue
        match = re.search(p2, line)
        if match:
            outDict['invalid'] = line
            continue
    if outDict:
        log.info(outDict)
    return outDict

def parse_oem_output(output):
    log.debug('Entering procedure parse_oem_output with args : %s\n' %(str(locals())))
    val_str = ''
    p1 = r'^([0-9a-fA-F]{1,2}\s?[0-9a-fA-F]*)'
    for line in output.splitlines():
        match = re.search(p1, line.strip())
        if match:
            val_str += line
    return val_str.strip()

def parse_pid(output, keyword):
    log.debug('Entering procedure parse_pid with args : %s\n' %(str(locals())))
    pid_list = []
    p1 = r'(\d+).+(\w)\s{2,}(%s)'%(keyword)
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            pid = match.group(1)
            pid_list.append(pid)
    pid_str = ' '.join(pid_list)
    return pid_str

def parse_rsp_to_byte_wdt(output):
    log.debug('Entering procedure parse_rsp_to_byte_wdt with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    if len(rsp_list) >= 6:
        outDict['timer use'] = rsp_list[0]
        outDict['timer action'] = rsp_list[1]
        outDict['pre-timeout'] = rsp_list[2]
        # outDict['timer use expiration'] = rsp_list[3]
        outDict['init countdown lsb'] = rsp_list[4]
        outDict['init countdown msb'] = rsp_list[5]
        if len(rsp_list) >= 8:
            outDict['present countdown lsb'] = rsp_list[6]
            outDict['present countdown msb'] = rsp_list[7]
    else:
        log.info('parse_rsp_to_byte_wdt support only byte count: 6 or 8')
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_sel_info(output):
    log.debug('Entering procedure parse_rsp_to_byte_sel_info with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 14
    if len(rsp_list) == valid_len:
        outDict['sel version'] = rsp_list[0]
        outDict['entries count'] = parse_hex_to_int(rsp_list[2] + rsp_list[1])
        outDict['free space'] = parse_hex_to_int(rsp_list[4] + rsp_list[3])
    else:
        log.info('parse_rsp_to_byte_sel_info support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_sel_entry(output):
    log.debug('Entering procedure parse_rsp_to_byte_sel_entry with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 16
    if len(rsp_list) >= valid_len:
        outDict["Next Record ID"] = parse_hex_to_int(rsp_list[1] + rsp_list[0])
    else:
        log.info('parse_rsp_to_byte_sel_entry support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_bios_bootorder(output):
    log.debug('Entering procedure parse_rsp_to_byte_bios_bootorder with args : %s\n' %(str(locals())))
    boot_mode_dict = {
        0: "Legacy",
        1: "UEFI"
    }
    boot_device_id_dict = {
        0: "USB device",
        1: "Network",
        2: "SATA HDD",
        3: "SATA-CDROM",
        4: "Other"
    }
    ip_dict = {
        0: "IPv4 first",
        1: "IPv6 first"
    }
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 6
    if len(rsp_list) >= 6:
        boot_mode = parse_hex_to_int(rsp_list[0]) & 0x1
        outDict['Boot mode'] = boot_mode_dict[boot_mode]
        for i in range(1, 6):
            boot_dev_id = parse_hex_to_int(rsp_list[i]) & 0x7
            outDict['Boot sequence '+ str(i)] = boot_device_id_dict[boot_dev_id]
            if boot_dev_id == 1:
                ip_order = parse_hex_to_int(rsp_list[i]) >> 3
                outDict['Boot sequence '+ str(i) + ' ip order'] = ip_dict[ip_order]
    else:
        log.fail('parse_rsp_to_byte_bios_bootorder support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_sys_info(output):
    log.debug('Entering procedure parse_rsp_to_byte_sys_info with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 16
    if len(rsp_list) >= valid_len:
        rsp_byte = rsp_list[4:12]
        bios_version = parse_hex_to_string(' '.join(rsp_byte))
        if bios_version:
            log.debug("Convert to string:")
            log.debug(" ".join("{}({})".format(x, y) for x, y in zip(rsp_byte, list(bios_version))))
            outDict['BIOS Version'] = str(bios_version)
    else:
        log.fail('parse_rsp_to_byte_sys_info support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_proc_name(output):
    log.debug('Entering procedure parse_rsp_to_byte_proc_name with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 48
    if len(rsp_list) == valid_len:
        proc_name = parse_hex_to_string(' '.join(rsp_list))
        if proc_name:
            log.debug("Convert to string:")
            log.debug(" ".join("{}({})".format(x, y) for x, y in zip(rsp_list, list(proc_name))))
            outDict['Product Name'] = str(proc_name).rstrip('\x00')
    else:
        log.fail('parse_rsp_to_byte_proc_name support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_proc_basic_info(output):
    log.debug('Entering procedure parse_rsp_to_byte_proc_basic_info with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 7
    if len(rsp_list) == valid_len:
        outDict['Core Number'] = parse_hex_to_int(rsp_list[0])
        outDict['Thread Number'] = parse_hex_to_int(rsp_list[2] + rsp_list[1])
        outDict['Processor frequency MHz'] = parse_hex_to_int(rsp_list[4] + rsp_list[3])
        outDict['Revision'] = ' '.join(rsp_list[5:7])
    else:
        log.fail('parse_rsp_to_byte_proc_basic_info support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict


def parse_rsp_to_byte_board_id(output):
    log.debug('Entering procedure parse_rsp_to_byte_board_id with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 4
    if len(rsp_list) == valid_len:
        outDict['Board SKU ID'] = rsp_list[0]
        outDict['Board Revision ID'] = rsp_list[1]
        outDict['MB Slot ID'] = rsp_list[2]
        outDict['Slot Config ID'] = rsp_list[3]
    else:
        log.fail('parse_rsp_to_byte_board_id support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_dimm_location(output):
    log.debug('Entering procedure parse_rsp_to_byte_dimm_location with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 4
    if len(rsp_list) == valid_len:
        outDict['DIMM Present'] = rsp_list[0]
        outDict['node number'] = rsp_list[1]
        outDict['channel number'] = rsp_list[2]
        outDict['DIMM number'] = rsp_list[3]
    else:
        log.fail('parse_rsp_to_byte_dimm_location support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_dimm_type(output):
    log.debug('Entering procedure parse_rsp_to_byte_dimm_type with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 1
    if len(rsp_list) == valid_len:
        outDict['DIMM type'] = rsp_list[0]
    else:
        log.fail('parse_rsp_to_byte_dimm_type support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_dimm_speed(output):
    log.debug('Entering procedure parse_rsp_to_byte_dimm_speed with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 6
    if len(rsp_list) == valid_len:
        outDict['DIMM speed'] = ' '.join(rsp_list[0:2])
        outDict['DIMM size'] = ' '.join(rsp_list[2:])
    else:
        log.fail('parse_rsp_to_byte_dimm_speed support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_dimm_module_part_num(output):
    log.debug('Entering procedure parse_rsp_to_byte_dimm_module_part_num with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 20
    if len(rsp_list) == valid_len:
        outDict['module part number'] = ' '.join(rsp_list)
    else:
        log.fail('parse_rsp_to_byte_dimm_module_part_num support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_dimm_module_serial_num(output):
    log.debug('Entering procedure parse_rsp_to_byte_dimm_module_serial_num with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 4
    if len(rsp_list) == valid_len:
        outDict['module serial number'] = ' '.join(rsp_list)
    else:
        log.fail('parse_rsp_to_byte_dimm_module_serial_num support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_dimm_module_manu_id(output):
    log.debug('Entering procedure parse_rsp_to_byte_dimm_module_manu_id with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 2
    if len(rsp_list) == valid_len:
        outDict['module manufacture ID'] = ' '.join(rsp_list)
    else:
        log.fail('parse_rsp_to_byte_dimm_module_manu_id support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_read_fru_data(output):
    log.debug('Entering procedure parse_rsp_to_byte_read_fru_data with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    count = parse_hex_to_int(rsp_list[0])
    valid_len = count + 1
    if len(rsp_list) == valid_len:
        outDict['read count'] = parse_hex_to_int(rsp_list[0])
        outDict['fru data'] = ' '.join(rsp_list[1:])
    else:
        log.fail('parse_rsp_to_byte_read_fru_data support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_get_fru_info(output):
    log.debug('Entering procedure parse_rsp_to_byte_get_fru_info with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 3
    if len(rsp_list) == valid_len:
        outDict['FRU Inventory area size'] = parse_hex_to_int(rsp_list[1] + rsp_list[0])
    else:
        log.fail('parse_rsp_to_byte_get_fru_info support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_get_device_id(output):
    log.debug('Entering procedure parse_rsp_to_byte_get_device_id with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 15
    if len(rsp_list) == valid_len:
        outDict['Firmware Revision'] = parse_version(str(rsp_list[2]) + '.' + str(rsp_list[3]))
        outDict['Manufacturer ID'] = str(parse_hex_to_int(rsp_list[8] + rsp_list[7] + rsp_list[6]))
        outDict['Product ID'] = str(parse_hex_to_int(rsp_list[10] + rsp_list[9])) + ' (' + \
                                hex(parse_hex_to_int(rsp_list[10] + rsp_list[9])) + ')'
    else:
        log.fail('parse_rsp_to_byte_get_device_id support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_rsp_to_byte_get_lan_config(output):
    log.debug('Entering procedure parse_rsp_to_byte_get_lan_config with args : %s\n' %(str(locals())))
    outDict = parser()
    rsp_list = str(output).split(' ')
    valid_len = 21
    if len(rsp_list) == valid_len:
        outDict['byte1'] = rsp_list[0]
        outDict['byte2'] = rsp_list[1]
        outDict['byte3'] = rsp_list[2]
        outDict['byte4-21'] = ' '.join(rsp_list[3:])
    else:
        log.fail('parse_rsp_to_byte_get_lan_config support only byte count: %d'%(valid_len))
    log.info(outDict)
    return outDict

def parse_cpu_uart_log(output, test_cmd):
    log.debug('Entering procedure parse_cpu_uart_log with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'(root@localhost.*?#.*reboot)'
    p2 = r'BIOS Date.*Ver: (\w+)'
    p3 = r'(Loading centos-7).*'
    p4 = r'(localhost login:).*'
    p5 = r'.*(%s)'%(test_cmd)
    for line in output.splitlines():
        line = line.strip()
        match1 = re.search(p1, line)
        match2 = re.search(p2, line)
        match3 = re.search(p3, line)
        match4 = re.search(p4, line)
        match5 = re.search(p5, line)
        if match1:
            outDict['CPU console'] = line
            continue
        if match2:
            outDict['BIOS post'] = match2.group(0)
            continue
        if match3:
            outDict['OS loading'] = line
            continue
        if match4:
            outDict['login prompt'] = line
            continue
        if match5:
            outDict['test executed command'] = line
            continue
    log.info(outDict)
    return outDict

def parse_cpu_uart_reboot_log(output):
    p1 = r'.*root@localhost.*?#.*reboot'
    return re.findall(p1, output)

def parse_hex_to_string(hex_str):
    return bytearray.fromhex(hex_str).decode()

def parse_string_to_hex(string):
    return " ".join("0x{:02x}".format(ord(c)) for c in string)

def parse_hex_to_int(hex_str):
    return int(hex_str, 16)

def parse_menu_boot_sequence(output):
    outDict = parser()
    p0 = 'FIXED BOOT ORDER Priorities.*'
    p1 = r'(\d+)\W+\[(.+)'
    p2 = 'Boot Option #'
    boot_option_output = re.search(p0, output).group(0)
    boot_option_list = boot_option_output.split(p2)
    for line in boot_option_list:
        match = re.search(p1, line)
        if match:
            option = 'boot option ' + match.group(1).strip()
            outDict[option] = match.group(2).strip().replace(']', '')[:19].strip()
            continue
    log.info(outDict)
    return outDict

def parse_file_size(output):
    log.debug('Entering procedure parse_file_size with args : %s\n' %(str(locals())))
    file_size = ''
    p1 = r'^(\d+.?\d*\w?)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            file_size = match.group(1).strip()
            break
    return file_size

def parse_disk_size(output, disk_name):
    log.debug('Entering procedure parse_disk_size with args : %s\n' %(str(locals())))
    p1 = 'Disk \/dev\/%s: (\d+.?\d* (GB|GiB|MB|KiB)).*'%(disk_name)
    size = ''
    match = re.search(p1, output)
    if match:
        log.success("Found: %s"%(match.group(0)))
        size = match.group(1)
    else:
        log.fail("Not found keyword: %s"%(p1))
    return size

def parse_board_type_rev(output):
    log.debug('Entering procedure parse_board_type_rev with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'^([A-Z]\w+)-?(\w*)_(.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['project'] = (match.group(1) + match.group(2)).strip()
            outDict['phase'] = match.group(3).strip()
            break
    log.info(outDict)
    return outDict

def parse_read_write_mdio(output):
    log.debug('Entering procedure parse_read_write_mdio with args : %s\n' %(str(locals())))
    val = ''
    p1 = r'(.+)PHY.*[:|value is]\s(.+)'
    match = re.search(p1, output)
    if match:
        val = match.group(2).strip()
    return val

def parse_dir_from_untar(output):
    log.debug('Entering procedure parse_dir_from_untar with args : %s\n' %(str(locals())))
    dir_name = ''
    p1 = r'^(\w+)\/$'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            dir_name = match.group(1)
            break
    return  dir_name

def parse_tpm_result(output):
    log.debug('Entering procedure parse_tpm_result with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'Tests\spassed: (\d+)'
    p2 = r'Tests\sFailed: (\d+)'
    for line in output.splitlines():
        line = line.strip()
        match1 = re.search(p1, line)
        match2 = re.search(p2, line)
        if match1:
            outDict['Tests passed'] = match1.group(1).strip()
        if match2:
            outDict['Tests Failed'] = match2.group(1).strip()
    log.info(outDict)
    return outDict

################################################################################
# Function Name: parse_menu_boot_override
# Date         : 6th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def parse_menu_boot_override(output):
    log.debug('Entering procedure parse_menu_boot_override with args : %s\n' %(str(locals())))
    p0 = 'Boot Override.*'
    p1 = '|'
    p2 = 'Change Opt'
    p3 = 'Connection'
    p4 = 'Select'
    p5 = 'F1:'
    p6 = 'F8:'
    p7 = 'F9:'
    p8 = 'F10:'
    p9 = 'ESC: Exit'
    p10 = 'Boot Override'
    boot_option_output = re.search(p0, output).group(0)
    boot_option_list = boot_option_output.split(p1)
    boot_option_list = [i.strip().strip('-') for i in boot_option_list]
    boot_option_list = [i for i in boot_option_list if len(i) > 2]
    remove_list = []
    for line in boot_option_list:
        match = re.findall(p4, line)
        match1 = re.findall(p9, line)
        match2 = re.findall(p3, line)
        match3 = re.findall(p5, line)
        match4 = re.findall(p2, line)
        match5 = re.findall(p6, line)
        match6 = re.findall(p7, line)
        match7 = re.findall(p8, line)
        match8 = re.findall(p10, line)
        if match:
            remove_list.append(line)
        if match1:
            remove_list.append(line)
        if match2:
            remove_list.append(line)
        if match3:
            remove_list.append(line)
        if match4:
            remove_list.append(line)
        if match5:
            remove_list.append(line)
        if match6:
            remove_list.append(line)
        if match7:
            remove_list.append(line)
        if match8:
            remove_list.append(line)
        else:
            pass
    for i in remove_list:
        boot_option_list.remove(i)
    return boot_option_list

def parse_eeprom2(output):
    log.debug('Entering procedure parse_eeprom2 with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'(.+):\s(.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = match.group(1)
            outDict[key] = match.group(2)
    log.info(outDict)
    return outDict

def parse_eeprom_type2(output):
    log.debug('Entering procedure parse_eeprom_type2 with args : %s\n' %(str(locals())))
    p1 = r'Wedge EEPROM (.+)'
    eeprom_type = None
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            eeprom_type = match.group(1)
            break
    return eeprom_type

def parse_eeprom_from_file(output):
    log.debug('Entering procedure parse_eeprom_from_file with args : %s\n' %(str(locals())))
    outDict = parser()
    p1 = r'(.+) =\s(.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = match.group(1)
            outDict[key] = match.group(2)
    log.info(outDict)
    return outDict

