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
import InitFrameworkLib
from dataStructure import nestedDict, parser
import re
from DiagLib import *
import CommonLib


#######################################################################################################################
# Function Name: PARSE_raw_output
# Date         : 30th January 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
def PARSE_raw_output(output):
    val_str = ''
    p1 = '^([0-9a-fA-F]{2}\s*)+'
    for line in output.splitlines():
        line = line.strip()
        log.debug('line = %s'%(line))
        match = re.search(p1,line)
        if match:
            val_str = line
            break
    return val_str


#######################################################################################################################
# Function Name: PARSE_diagtool_help
# Date         : 27th January 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
def PARSE_diagtool_help(output):
    outDict = parser()
    #p1='usage: [\w+,\-,\/]+\/(cel\-[\w,\-]+)+ \[OPTIONS\]'
    p1='usage: [\w+,\-,\/]+\/(cel\-[\w,\-]+)+ \[.*\]'
    p2='-a[\,\s]+--all\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p3='-h[\,\s]+--help\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p4='-K[\,\s]+--check\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p5='-i[\,\s]+--info\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p6='-r[\,\s]+--read\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p7='-w[\,\s]+--write\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p8='-D[\,\s]+--data\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p9='-S[\,\s]+--show\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p10='-p[\,\s]+--port\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p11='-u[\,\s]+--color\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p12='-F[\,\s]+--off\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p13='-H[\,\s]+--flash\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    p14='-l[\,\s]+--list\s+([\[,\],\(,\~,\),\w,\d,\s,\.]+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            outDict['bin_tool'] = match.group(1)
        else:
            match = re.search('cel-tpm-test', line)
            if match:
                outDict['bin_tool'] = match.group()
        match = re.search(p2,line)
        if match:
            outDict['all_option'] = match.group(1)
        match = re.search(p3,line)
        if match:
            outDict['help_option'] = match.group(1)
        match = re.search(p4,line)
        if match:
            outDict['check_option'] = match.group(1)
        match = re.search(p5,line)
        if match:
            outDict['info_option'] = match.group(1)
        match = re.search(p6,line)
        if match:
            outDict['read_option'] = match.group(1)
        match = re.search(p7,line)
        if match:
            outDict['write_option'] = match.group(1)
        match = re.search(p8,line)
        if match:
            outDict['data_option'] = match.group(1)
        match = re.search(p9,line)
        if match:
            outDict['show_option'] = match.group(1)
        match = re.search(p10,line)
        if match:
            outDict['port_option'] = match.group(1)
        match = re.search(p11,line)
        if match:
            outDict['color_option'] = match.group(1)
        match = re.search(p12,line)
        if match:
            outDict['off_option'] = match.group(1)
        match = re.search(p13,line)
        if match:
            outDict['flash_option'] = match.group(1)
        match = re.search(p14,line)
        if match:
            outDict['list_option'] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)
    return outDict


#######################################################################################################################
# Function Name: PARSE_diagtool_info
# Date         : 27th January 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
def PARSE_diagtool_info(output):
    outDict = parser()
    p1='Vendor:\s*(.+)'
    p2='Product:\s*(.+)'
    p3='Revision:\s*(.+)'
    p4='Compliance:\s*(.+)'
    p5='User Capacity:\s*(.+)'
    p6='Logical block size:\s*(.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            outDict['Vendor'] = match.group(1)
        match = re.search(p2,line)
        if match:
            outDict['Product'] = match.group(1)
        match = re.search(p3,line)
        if match:
            outDict['Revision'] = match.group(1)
        match = re.search(p4,line)
        if match:
            outDict['Compliance'] = match.group(1)
        match = re.search(p5,line)
        if match:
            outDict['User Capacity'] = match.group(1)
        match = re.search(p6,line)
        if match:
            outDict['Logical block size'] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)
    return outDict


#######################################################################################################################
# Function Name: PARSE_diagtool_show
# Date         : 28th January 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
def PARSE_diagtool_show(output):
    outDict = parser()
    p1='Diag Version: (\d+\.\d+\.\d+)'
    p2='OS Version: (\d+\.\d+\.\d+)'
    p3='Kernel Version: (\d+\.\d+\.\d+)'
    p4='BMC Version: (\d+\.\d+)'
    p5='BIOS Version: ([\w,\d]+\_[\w,\d]+)'
    p6='FPGA1 Version: (\d+\.\d+)'
    p7='FPGA2 Version: (\d+\.\d+)'
    p8='SCM CPLD Version: (\d+\.\d+)'
    p9='SMB CPLD Version: (\d+\.\d+)'
    p10='I210 FW Version: (\d+\.\d+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            outDict['diag_version'] = match.group(1)
        match = re.search(p2,line)
        if match:
            outDict['os_version'] = match.group(1)
        match = re.search(p3,line)
        if match:
            outDict['kernel_version'] = match.group(1)
        match = re.search(p4,line)
        if match:
            outDict['bmc_version'] = match.group(1)
        match = re.search(p5,line)
        if match:
            outDict['bios_version'] = match.group(1)
        match = re.search(p6,line)
        if match:
            outDict['fpga1_version'] = match.group(1)
        match = re.search(p7,line)
        if match:
            outDict['fpga2_version'] = match.group(1)
        match = re.search(p8,line)
        if match:
            outDict['scm_cpld_version'] = match.group(1)
        match = re.search(p9,line)
        if match:
            outDict['smb_cpld_version'] = match.group(1)
        match = re.search(p10,line)
        if match:
            outDict['i2c_fw_version'] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)
    return outDict


#######################################################################################################################
# Function Name: PARSE_diagtool_list
# Date         : 30th January 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
def PARSE_diagtool_list(output):
    outDict = parser()
    p1='chip_type:\s+([\w,\d]+)'
    p2='vendor_id:\s+([\w,\d]+)'
    p3='bus_id\s+:\s+([\w,\d]+)'
    p4='dev_addr\s+:\s+([\w,\d]+)'
    p5='dev_path\s+:\s+([\/,\w,\d]+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            outDict['chip_type'] = match.group(1)
        match = re.search(p2,line)
        if match:
            outDict['vendor_id'] = match.group(1)
        match = re.search(p3,line)
        if match:
            outDict['bus_id'] = match.group(1)
        match = re.search(p4,line)
        if match:
            outDict['dev_addr'] = match.group(1)
        match = re.search(p5,line)
        if match:
            outDict['dev_path'] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)
    return outDict


#######################################################################################################################
# Function Name: PARSE_get_cpld_output
# Date         : 30th January 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
def PARSE_get_cpld_output(output):
    val_str = ''
    p1 = '^[0-9a-fA-F]{6}:\s+([0-9a-fA-F]+)'
    for line in output.splitlines():
        line = line.strip()
        # log.debug('line = %s'%(line))
        match = re.search(p1,line)
        if match:
            val_str = match.group(1)
            break
    return val_str


#######################################################################################################################
# Function Name: PARSE_bmc_diagtool_help
# Date         : 25th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
def PARSE_bmc_diagtool_help(output):
    outDict = parser()
    p1='Usage\:\s+\.\/(cel-[\w\-]+)\s+options\s+\([\-\w\|]+\)'
    p2='-a\s+([\w\s]+)'
    p3='-h\s+([\w\s]+)'
    p4='-i\s+([\w\s]+)'

    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            outDict['bin_tool'] = match.group(1)
        match = re.search(p2,line)
        if match:
            outDict['all_option'] = match.group(1)
        match = re.search(p3,line)
        if match:
            outDict['help_option'] = match.group(1)
        match = re.search(p4,line)
        if match:
            outDict['info_option'] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)
    return outDict


#######################################################################################################################
# Function Name: PARSE_bmc_diagtool_info
# Date         : 28th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
def PARSE_bmc_diagtool_info(output,pattern,inputArray):
    outDict = parser()
    new_inputArray = inputArray
    for line in output.splitlines():
        line = line.strip()
        # log.debug('line=%s' % line)
        for i in pattern:
            match = re.search(i,line)
            if match:
                for attr in new_inputArray:
                    if match.group(1) == new_inputArray[attr]:
                        outDict[attr] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)
    return outDict


#######################################################################################################################
# Function Name: PARSE_FW_Version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com> 
#######################################################################################################################
def PARSE_FW_Version(output):
    outDict = parser()
    p1='Bridge-IC Version:\s+([\w,\d]+\.[\d]+)'
    p2='Bridge-IC Bootloader Version:\s+([\w,\d]+\.[\d]+)'
    p3='BIOS Version:\s+([\w,\d]+)'
    p4='CPLD Version:\s+([\w,\d]+)'
    p5='ME Version:\s+([\d]+\.[\d]+\.[\d]+\.[\d]+)'
    p6='PVCCIN VR Version:\s+([\w,\d]+\,\s+[\w,\d]+)'
    p7='DDRAB VR Version:\s+([\w,\d]+\,\s+[\w,\d]+)'
    p8='P1V05 VR Version:\s+([\w,\d]+\,\s+[\w,\d]+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            outDict['BRIDGE_VER'] = match.group(1)
        match = re.search(p2,line)
        if match:
            outDict['BRIDGE_BOOTLOADER_VER'] = match.group(1)
        match = re.search(p3,line)
        if match:
            outDict['BIOS_VER'] = match.group(1)
        match = re.search(p4,line)
        if match:
            outDict['CPLD_VER'] = match.group(1)
        match = re.search(p5,line)
        if match:
            outDict['ME_VER'] = match.group(1)
        match = re.search(p6,line)
        if match:
            outDict['PVCCIN_VER'] = match.group(1)
        match = re.search(p7,line)
        if match:
            outDict['DDRAB_VER'] = match.group(1)
        match = re.search(p8,line)
        if match:
            outDict['P1V05_VER'] = match.group(1)

    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)
    return outDict


#######################################################################################################################
# Function Name: PARSE_pattern_value
# Date         : 27th July 2020
# Author       : Yang Xuecun<yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang Xuecun<yxcun@celestica.com> 
#######################################################################################################################
def PARSE_pattern_value(output, patterns, patterns_is_dict=True, line_mode=True):
    dLibObj = InitFrameworkLib.getDiagLibObj()
    outDict = parser()
    outList = []
    match_p_list = []
    pattern_sum = len(patterns)
    pass_num = 0
    if line_mode:
        for line in output.splitlines():
            line = line.strip()
            if patterns_is_dict:
                for key, pattern in patterns.items():
                    match = re.search(pattern, line)
                    if match:
                        match_p_list.append(pattern)
                        outDict[key] = match.group(1)
                        break
            else:
                for pattern in patterns:
                    match = re.search(pattern, line)
                    if match:
                        match_p_list.append(pattern)
                        outList.append( match.group(1))
    else:
        if patterns_is_dict:
            for key, pattern in patterns.items():
                match = re.search(pattern, output, re.M|re.S)
                if match:
                    match_p_list.append(pattern)
                    outDict[key] = match.group(1)
                    break
        else:
            for pattern in patterns:
                match = re.search(pattern, output, re.M|re.S)
                if match:
                    match_p_list.append(pattern)
                    outList.append( match.group(0))

    if patterns_is_dict:
        outObj = outDict
    else:
        outObj = outList
    pass_num = len(set(match_p_list))
    if pass_num < pattern_sum:
        dLibObj.wpl_log_fail("Error: pattern_sum:{}, pass_num:{}".format(pattern_sum, pass_num))
        if not patterns_is_dict:
            mismatch_list = list(set(patterns) - set(match_p_list))
        else:
            mismatch_list = list(set(patterns.values()) - set(match_p_list))
        dLibObj.wpl_log_info("mismatch items: [{}]".format(CommonLib.get_readable_strings(mismatch_list)))
    dLibObj.wpl_log_info("{}".format(outObj))
    return outObj
