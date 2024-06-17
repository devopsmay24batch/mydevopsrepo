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
import re
import time
import Logger as log
import CommonLib
import random
import Const
import subprocess
import json
import os
from Decorator import *
from bsp_variable import *
from datetime import datetime
from dataStructure import parser
#from errorsModule import testFailed
#from SensorCsv import SensorCsv
#from pkg_resources import parse_version
from SwImage import SwImage

@logThis
def parse_th5_version(output):
    outDict = parser()
    p1 = r'PCIe FW loader version: (.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['PCIe FW loader version'] = match.group(1)
    log.info(outDict)
    return outDict

@logThis
def parse_ifconfig(output):
    outDict = parser()
    p1 = r'eth0.4088 Link encap:Ethernet'
    p2 = r'inet6 addr: (.+)\/64'
    flag = 0
    for line in output.splitlines():
        line = line.strip()
        if flag:
            match = re.search(p2, line)
            if match:
               outDict['Ipv6_address'] = match.group(1)
               if outDict['Ipv6_address'] == 'fe80::1':
                  continue
            break
        match = re.search(p1, line)
        if match:
           flag = 1
           continue
    log.info(outDict)
    return outDict

@logThis
def parse_fanSensor(fan_num, output):
    fan_rpm = 0
    reg_val = "fan{}.* (\d+) RPM".format(fan_num)
    for line in output.splitlines():
        line = line.strip()
        p1 = re.search(reg_val,line)
        if p1:
           fan_rpm =  int(p1.group(1))
           log.info("Parsed fan rpm value of fan number{} is:{}".format(fan_num,fan_rpm))
           return fan_rpm
    return fan_rpm

def parse_gpioLines(line_num, output, out_status_check=False):
    status = 0
    reg_val = "line .*{}:.*unnamed.*unused.* (\S+) .*active-high".format(line_num)
    for line in output.splitlines():
        line = line.strip()
        if out_status_check:
            p1 = re.search(reg_val,line)
            if p1:
               line_status = p1.group(1)
               return line_status
        else:
            p1 = re.search(reg_val,line)
            if p1:
               status = 1
               return status
    return status

def parse_i2cBuses(bus_num, output):
    status = 0
    reg_val = "i2c-{}.* adapter".format(bus_num)
    for line in output.splitlines():
        line = line.strip()
        p1 = re.search(reg_val,line)
        if p1:
           status = 1
           return status
    return status

def parse_i2cScanOutput(reg_val, output):
    status = 0
    for line in output.splitlines():
        line = line.strip()
        p1 = re.search(reg_val,line)
        if p1:
           status = 1
           return status
    return status


@logThis
def parse_unidiag_output(output):
    outDict = parser()
    if fb_variant == 'minipack3':
       bios_version = re.search('BIOS: *(\S+)',output)
       bmc_version = re.search('BMC: *montblanc-(\S+) .*',output)
       i210_version = re.search('I210: *(\S+), .*',output)
       sdk_version = re.search('SDK: *(\S+)',output)
       bsp_version = re.search('BSP: *(\S+)',output)
       udev_version = re.search('UDEV: *(\S+)',output)
       diag_os_version = re.search(' OS: *(\S+)',output)
       dom1_version = re.search('DOM1 FPGA : *(\S+)',output)
       dom2_version = re.search('DOM2 FPGA : *(\S+)',output)
       iob_version = re.search('IOB  FPGA : *(\S+)',output)
       scm_version = re.search('SCM CPLD : *(\S+)',output)
       smb_version = re.search('SMB CPLD : *(\S+)',output)
       mcb_version = re.search('MCB CPLD : *(\S+)',output)

       outDict['bios'] = bios_version.group(1) if bios_version else ""
       outDict['bmc'] = bmc_version.group(1) if bmc_version else ""
       outDict['i210'] = i210_version.group(1) if i210_version else ""
       outDict['sdk'] = sdk_version.group(1) if sdk_version else ""
       outDict['bsp'] = bsp_version.group(1) if bsp_version else ""
       outDict['udev'] = udev_version.group(1) if udev_version else ""
       outDict['diag_os'] = diag_os_version.group(1) if diag_os_version else ""
       outDict['dom1_fpga'] = dom1_version.group(1) if dom1_version else ""
       outDict['dom2_fpga'] = dom2_version.group(1) if dom2_version else ""
       outDict['iob_fpga'] = iob_version.group(1) if iob_version else ""
       outDict['scm_cpld'] = scm_version.group(1) if scm_version else ""
       outDict['smb_cpld'] = smb_version.group(1) if smb_version else ""
       outDict['mcb_cpld'] = mcb_version.group(1) if mcb_version else ""    
    elif fb_variant == 'minerva':
       bios_version = re.search('BIOS: *(\S+)',output)
       bmc_version = re.search('BMC: *tahan-(\S+) .*',output)
       if not bmc_version:
           bmc_version = re.search('BMC: *janga-(\S+) .*',output)
       i210_version = re.search('I210: *(\S+), .*',output)
       sdk_version = re.search('SDK: *(\S+)',output)
       bsp_version = re.search('BSP: *(\S+)',output)
       udev_version = re.search('UDEV: *(\S+)',output)
       diag_os_version = re.search(' OS: *(\S+)',output)
       dom_version = re.search('DOM FPGA: *(\S+)',output)
       iob_version = re.search('IOB FPGA: *(\S+)',output)
       smb1_version = re.search('SMB CPLD 1: (\S+)',output)
       smb2_version = re.search('SMB CPLD 2: (\S+)',output)
       pwr_version = re.search('PWR CPLD: *(\S+)',output)

       outDict['bios'] = bios_version.group(1) if bios_version else ""
       outDict['bmc'] = bmc_version.group(1) if bmc_version else ""
       outDict['i210'] = i210_version.group(1) if i210_version else ""
       outDict['sdk'] = sdk_version.group(1) if sdk_version else ""
       outDict['bsp'] = bsp_version.group(1) if bsp_version else ""
       outDict['udev'] = udev_version.group(1) if udev_version else ""
       outDict['diag_os'] = diag_os_version.group(1) if diag_os_version else ""
       outDict['dom_fpga'] = dom_version.group(1) if dom_version else ""
       outDict['iob_fpga'] = iob_version.group(1) if iob_version else ""
       outDict['smb1_cpld'] = smb1_version.group(1) if smb1_version else ""
       outDict['smb2_cpld'] = smb2_version.group(1) if smb2_version else ""
       outDict['pwr_cpld'] = pwr_version.group(1) if pwr_version else ""
       
    log.info(outDict)
    return outDict

@logThis
def parse_eepromCfg_output(output):
    outDict = parser()
    if fb_variant == 'minipack3' or fb_variant == 'minerva':
       magic_word = re.search('magic_word=(\S+)',output)
       format_version = re.search('format_version=(\S+)',output)
       product_name = re.search('product_name=(\S+)',output)
       top_level_product_part_number = re.search('top_level_product_part_number=(\S+)',output)
       system_assembly_part_number = re.search('system_assembly_part_number=(\S+)',output)
       facebook_pcba_part_number = re.search('facebook_pcba_part_number=(\S+)',output)
       facebook_pcb_part_number = re.search('facebook_pcb_part_number=(\S+)',output)
       odm_pcba_part_number = re.search('odm_pcba_part_number=(\S+)',output)
       odm_pcba_serial_number = re.search('odm_pcba_serial_number=(\S+)',output)
       product_production_state = re.search('product_production_state=(\S+)',output)
       product_version = re.search('product_version=(\S+)',output)
       product_sub_version = re.search('product_sub_version=(\S+)',output)
       product_serial_number = re.search('product_serial_number=(\S+)',output)
       system_manufacturer = re.search('system_manufacturer=(\S+)',output)
       system_manufacturing_date = re.search('system_manufacturing_date=(\S+)',output)
       pcb_manufacturer = re.search('pcb_manufacturer=(\S+)',output)
       assembled_at = re.search('assembled_at=(\S+)',output)
       local_mac_address = re.search('local_mac_address=(\S+)',output)
       extended_mac_address_base = re.search('extended_mac_address_base=(\S+)',output)
       extended_mac_address_size = re.search('extended_mac_address_size=(\S+)',output)
       eeprom_location_on_fabric = re.search('eeprom_location_on_fabric=(\S+)',output)
    elif fb_variant == 'minerva':
       magic_word = re.search('magic_word = (\S+)',output)
       format_version = re.search('format_version = (\S+)',output)
       product_name = re.search('product_name = (\S+)',output)
       top_level_product_part_number = re.search('top_level_product_part_number = (\S+)',output)
       system_assembly_part_number = re.search('system_assembly_part_number = (\S+)',output)
       facebook_pcba_part_number = re.search('facebook_pcba_part_number = (\S+)',output)
       facebook_pcb_part_number = re.search('facebook_pcb_part_number = (\S+)',output)
       odm_pcba_part_number = re.search('odm_pcba_part_number = (\S+)',output)
       odm_pcba_serial_number = re.search('odm_pcba_serial_number = (\S+)',output)
       product_production_state = re.search('product_production_state = (\S+)',output)
       product_version = re.search('product_version = (\S+)',output)
       product_sub_version = re.search('product_sub_version = (\S+)',output)
       product_serial_number = re.search('product_serial_number = (\S+)',output)
       system_manufacturer = re.search('system_manufacturer = (\S+)',output)
       system_manufacturing_date = re.search('system_manufacturing_date = (\S+)',output)
       pcb_manufacturer = re.search('pcb_manufacturer = (\S+)',output)
       assembled_at = re.search('assembled_at = (\S+)',output)
       local_mac_address = re.search('local_mac_address = (\S+)',output)
       extended_mac_address_base = re.search('extended_mac_address_base = (\S+)',output)
       extended_mac_address_size = re.search('extended_mac_address_size = (\S+)',output)
       eeprom_location_on_fabric = re.search('eeprom_location_on_fabric = (\S+)',output)

    outDict['magic_word'] = magic_word.group(1) if magic_word else ""
    outDict['format_version'] = format_version.group(1) if format_version else ""
    outDict['product_name'] = product_name.group(1) if product_name else ""
    outDict['top_level_product_part_number'] = top_level_product_part_number.group(1)\
            if top_level_product_part_number else ""
    outDict['system_assembly_part_number'] = system_assembly_part_number.group(1)\
            if system_assembly_part_number else ""
    outDict['facebook_pcba_part_number'] = facebook_pcba_part_number.group(1)\
            if facebook_pcba_part_number else ""
    outDict['facebook_pcb_part_number'] = facebook_pcb_part_number.group(1)\
            if facebook_pcb_part_number else ""
    outDict['odm_pcba_part_number'] = odm_pcba_part_number.group(1)\
            if odm_pcba_part_number else ""
    outDict['odm_pcba_serial_number'] = odm_pcba_serial_number.group(1)\
            if odm_pcba_serial_number else ""
    outDict['product_production_state'] = product_production_state.group(1)\
            if product_production_state else ""
    outDict['product_version'] = product_version.group(1) if product_version else ""
    outDict['product_sub_version'] = product_sub_version.group(1)\
            if product_sub_version else ""
    outDict['product_serial_number'] = product_serial_number.group(1)\
            if product_serial_number else ""
    outDict['system_manufacturer'] = system_manufacturer.group(1)\
            if system_manufacturer else ""
    outDict['system_manufacturing_date'] = system_manufacturing_date.group(1)\
            if system_manufacturing_date else ""
    outDict['pcb_manufacturer'] = pcb_manufacturer.group(1) if pcb_manufacturer else ""
    outDict['assembled_at'] = assembled_at.group(1) if assembled_at else ""
    outDict['local_mac_address'] = local_mac_address.group(1) if local_mac_address else ""
    outDict['extended_mac_address_base'] = extended_mac_address_base.group(1)\
            if extended_mac_address_base else ""
    outDict['extended_mac_address_size'] = extended_mac_address_size.group(1)\
            if extended_mac_address_size else ""
    outDict['eeprom_location_on_fabric'] = eeprom_location_on_fabric.group(1)\
            if eeprom_location_on_fabric else ""
    log.info(outDict)
    return outDict

@logThis
def parse_weutil_output(output):
    outDict = parser()
    product_name = re.search('Product Name: *(\S+)',output)
    top_level_product_part_number = re.search('Product Part Number: *(\S+)',output)
    system_assembly_part_number = re.search('System Assembly Part Number: *(\S+)',output)
    facebook_pcba_part_number = re.search('Meta PCBA Part Number: *(\S+)',output)
    facebook_pcb_part_number = re.search('Meta PCB Part Number: *(\S+)',output)
    odm_pcba_part_number = re.search('ODM/JDM PCBA Part Number: *(\S+)',output)
    odm_pcba_serial_number = re.search('ODM/JDM PCBA Serial Number: *(\S+)',output)
    product_production_state = re.search('Product Production State: *(\S+)',output)
    product_version = re.search('Product Version: *(\S+)',output)
    product_sub_version = re.search('Product Sub-Version: *(\S+)',output)
    product_serial_number = re.search('Product Serial Number: *(\S+)',output)
    system_manufacturer = re.search('System Manufacturer: *(\S+)',output)
    system_manufacturing_date = re.search('System Manufacturing Date: *(\S+)',output)
    pcb_manufacturer = re.search('PCB Manufacturer: *(\S+)',output)
    assembled_at = re.search('Assembled at: *(\S+)',output)
    local_mac_address = re.search('Local MAC: *(\S+)',output)
    extended_mac_address_base = re.search('Extended MAC Base: *(\S+)',output)
    extended_mac_address_size = re.search('Extended MAC Address Size: *(\S+)',output)
    eeprom_location_on_fabric = re.search('EEPROM location on Fabric: *(\S+)',output)

    outDict['product_name'] = product_name.group(1) if product_name else ""
    outDict['top_level_product_part_number'] = top_level_product_part_number.group(1)\
            if top_level_product_part_number else ""
    outDict['system_assembly_part_number'] = system_assembly_part_number.group(1)\
            if system_assembly_part_number else ""
    outDict['facebook_pcba_part_number'] = facebook_pcba_part_number.group(1)\
            if facebook_pcba_part_number else ""
    outDict['facebook_pcb_part_number'] = facebook_pcb_part_number.group(1)\
            if facebook_pcb_part_number else ""
    outDict['odm_pcba_part_number'] = odm_pcba_part_number.group(1)\
            if odm_pcba_part_number else ""
    outDict['odm_pcba_serial_number'] = odm_pcba_serial_number.group(1)\
            if odm_pcba_serial_number else ""
    outDict['product_production_state'] = product_production_state.group(1)\
            if product_production_state else ""
    outDict['product_version'] = product_version.group(1) if product_version else ""
    outDict['product_sub_version'] = product_sub_version.group(1)\
            if product_sub_version else ""
    outDict['product_serial_number'] = product_serial_number.group(1)\
            if product_serial_number else ""
    outDict['system_manufacturer'] = system_manufacturer.group(1)\
            if system_manufacturer else ""
    outDict['system_manufacturing_date'] = system_manufacturing_date.group(1)\
            if system_manufacturing_date else ""
    outDict['pcb_manufacturer'] = pcb_manufacturer.group(1) if pcb_manufacturer else ""
    outDict['assembled_at'] = assembled_at.group(1) if assembled_at else ""
    outDict['local_mac_address'] = local_mac_address.group(1) if local_mac_address else ""
    outDict['extended_mac_address_base'] = extended_mac_address_base.group(1)\
            if extended_mac_address_base else ""
    outDict['extended_mac_address_size'] = extended_mac_address_size.group(1)\
            if extended_mac_address_size else ""
    outDict['eeprom_location_on_fabric'] = eeprom_location_on_fabric.group(1)\
            if eeprom_location_on_fabric else ""
    log.info(outDict)
    return outDict

