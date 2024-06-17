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
    found = 0
    p1='usage: [\w+,\-,\/]+\/(cel\-[\w,\-]+)+ \[OPTIONS\]'
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
            found += 1
            outDict['bin_tool'] = match.group(1)
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['all_option'] = match.group(1)
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['help_option'] = match.group(1)
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['check_option'] = match.group(1)
        match = re.search(p5,line)
        if match:
            found += 1
            outDict['info_option'] = match.group(1)
        match = re.search(p6,line)
        if match:
            found += 1
            outDict['read_option'] = match.group(1)
        match = re.search(p7,line)
        if match:
            found += 1
            outDict['write_option'] = match.group(1)
        match = re.search(p8,line)
        if match:
            found += 1
            outDict['data_option'] = match.group(1)
        match = re.search(p9,line)
        if match:
            found += 1
            outDict['show_option'] = match.group(1)
        match = re.search(p10,line)
        if match:
            found += 1
            outDict['port_option'] = match.group(1)
        match = re.search(p11,line)
        if match:
            found += 1
            outDict['color_option'] = match.group(1)
        match = re.search(p12,line)
        if match:
            found += 1
            outDict['off_option'] = match.group(1)
        match = re.search(p13,line)
        if match:
            found += 1
            outDict['flash_option'] = match.group(1)
        match = re.search(p14,line)
        if match:
            found += 1
            outDict['list_option'] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
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
    found = 0
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
            found += 1
            outDict['Vendor'] = match.group(1)
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['Product'] = match.group(1)
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['Revision'] = match.group(1)
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['Compliance'] = match.group(1)
        match = re.search(p5,line)
        if match:
            found += 1
            outDict['User Capacity'] = match.group(1)
        match = re.search(p6,line)
        if match:
            found += 1
            outDict['Logical block size'] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
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
    found = 0
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
            found += 1
            outDict['diag_version'] = match.group(1)
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['os_version'] = match.group(1)
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['kernel_version'] = match.group(1)
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['bmc_version'] = match.group(1)
        match = re.search(p5,line)
        if match:
            found += 1
            outDict['bios_version'] = match.group(1)
        match = re.search(p6,line)
        if match:
            found += 1
            outDict['fpga1_version'] = match.group(1)
        match = re.search(p7,line)
        if match:
            found += 1
            outDict['fpga2_version'] = match.group(1)
        match = re.search(p8,line)
        if match:
            found += 1
            outDict['scm_cpld_version'] = match.group(1)
        match = re.search(p9,line)
        if match:
            found += 1
            outDict['smb_cpld_version'] = match.group(1)
        match = re.search(p10,line)
        if match:
            found += 1
            outDict['i2c_fw_version'] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
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
    found = 0
    p1='chip_type:\s+([\w,\d]+)'
    p2='vendor_id:\s+([\w,\d]+)'
    p3='bus_id\s+:\s+([\w,\d]+)'
    p4='dev_addr\s+:\s+([\w,\d]+)'
    p5='dev_path\s+:\s+([\/,\w,\d]+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            found += 1
            outDict['chip_type'] = match.group(1)
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['vendor_id'] = match.group(1)
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['bus_id'] = match.group(1)
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['dev_addr'] = match.group(1)
        match = re.search(p5,line)
        if match:
            found += 1
            outDict['dev_path'] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
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
    found = 0
    p1='Usage\:\s+\.\/(cel-[\w\-]+)\s+options\s+\([\-\w\|]+\)'
    p2='-a\s+([\w\s]+)'
    p3='-h\s+([\w\s]+)'
    p4='-i\s+([\w\s]+)'

    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            found += 1
            outDict['bin_tool'] = match.group(1)
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['all_option'] = match.group(1)
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['help_option'] = match.group(1)
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['info_option'] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
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
    found = 0
    new_inputArray = inputArray
    for line in output.splitlines():
        line = line.strip()
        # log.debug('line=%s' % line)
        for i in pattern:
            match = re.search(i,line)
            if match:
                for attr in new_inputArray:
                    if match.group(1) == new_inputArray[attr]:
                        found += 1
                        outDict[attr] = match.group(1)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
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
    found = 0
    p1='Bridge-IC Version:\s+v([\d]+\.[\d]+)'
    p2='Bridge-IC Bootloader Version:\s+v([\d]+\.[\d]+)'
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
            found += 1
            outDict['BRIDGE_VER'] = match.group(1)
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['BRIDGE_BOOTLOADER_VER'] = match.group(1)
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['BIOS_VER'] = match.group(1)
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['CPLD_VER'] = match.group(1)
        match = re.search(p5,line)
        if match:
            found += 1
            outDict['ME_VER'] = match.group(1)
        match = re.search(p6,line)
        if match:
            found += 1
            outDict['PVCCIN_VER'] = (match.group(1) + ', ' + match.group(2))
        match = re.search(p7,line)
        if match:
            found += 1
            outDict['DDRAB_VER'] = (match.group(1) + ', ' + match.group(2))
        match = re.search(p8,line)
        if match:
            found += 1
            outDict['P1V05_VER'] = (match.group(1) + ', ' + match.group(2))

    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
        return outDict


#######################################################################################################################
# Function Name: PARSE_CPLD_Versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
def PARSE_CPLD_Versions(output):
    outDict = parser()
    found = 0
    p1='SMB_SYSCPLD:\s+([\d]+\.[\d]+)'
    p2='SMB_PWRCPLD:\s+([\d]+\.[\d]+)'
    p3='SCMCPLD:\s+([\d]+\.[\d]+)'
    p4='FCMCPLD:\s+([\d]+\.[\d]+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            found += 1
            outDict['SYSCPLD_VER'] = match.group(1)
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['PWRCPLD_VER'] = match.group(1)
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['SCMCPLD_VER'] = match.group(1)
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['FCMCPLD_VER'] = match.group(1)

    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
        return outDict


#######################################################################################################################
# Function Name: PARSE_CPLD_FPGA_BIC_Versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
def PARSE_CPLD_FPGA_BIC_Versions(output):
    outDict = parser()
    found = 0
    p1='FCMCPLD:\s+([\d]+\.[\d]+)'
    p2='PWRCPLD:\s+([\d]+\.[\d]+)'
    p3='SCMCPLD:\s+([\d]+\.[\d]+)'
    p4='SMBCPLD:\s+([\d]+\.[\d]+)'
    p5='DOMFPGA1:\s+([\d]+\.[\d]+)'
    p6='DOMFPGA2:\s+([\d]+\.[\d]+)'
    p7='Bridge-IC Version:\s+v([\d]+\.[\d]+)'
    p8='Bridge-IC Bootloader Version:\s+v([\d]+\.[\d]+)'
    p9='CPLD Version:\s+([\w,\d]+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            found += 1
            outDict['FCMCPLD_VER'] = match.group(1)
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['PWRCPLD_VER'] = match.group(1)
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['SCMCPLD_VER'] = match.group(1)
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['SMBCPLD_VER'] = match.group(1)
        match = re.search(p5,line)
        if match:
            found += 1
            outDict['FPGA1_VER'] = match.group(1)
        match = re.search(p6,line)
        if match:
            found += 1
            outDict['FPGA2_VER'] = match.group(1)
        match = re.search(p7,line)
        if match:
            found += 1
            outDict['BRIDGE_VER'] = match.group(1)
        match = re.search(p8,line)
        if match:
            found += 1
            outDict['BRIDGE_BOOTLOADER_VER'] = match.group(1)
        match = re.search(p9,line)
        if match:
            found += 1
            outDict['CPLD_VER'] = match.group(1)

    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
        return outDict


#######################################################################################################################
# Function Name: WEDGE400C_PARSE_FW_UTIL_Versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
def WEDGE400C_PARSE_FW_UTIL_Versions(output):
    outDict = parser()
    found = 0

    p0='BMC\s+Version:\s+([\w,\d]+)-([\w,\d]+-dirty)'
    p1='BMC\s+Version:\s+([\w,\d]+)-v([\d]+\.[\d]+)'
    p2='BMC\s+Version:\s+([\w,\d]+)-([\w,\d]+)'
    p3='TPM\s+Version:\s+([\d]+\.[\d]+)'
    p4='FCMCPLD:\s+([\d]+\.[\d]+)'
    p5='PWRCPLD:\s+([\d]+\.[\d]+)'
    p6='SCMCPLD:\s+([\d]+\.[\d]+)'
    p7='SMBCPLD:\s+([\d]+\.[\d]+)'
    p8='DOMFPGA1:\s+([\d]+\.[\d]+)'
    p9='DOMFPGA2:\s+([\d]+\.[\d]+)'
    p10='Bridge-IC\s+Version:\s+v([\d]+\.[\d]+)'
    p11='Bridge-IC\s+Bootloader\s+Version:\s+v([\d]+\.[\d]+)'
    p12='BIOS\s+Version:\s+([\w,\d]+_[\w,\d]+)'
    p13='CPLD\s+Version:\s+([\w,\d]+)'
    p14='ME\s+Version:\s+([\d]+\.[\d]+\.[\d]+\.[\d]+)'
    p15='PVCCIN\s+VR\s+Version:\s+([\w,\d]+),\s([\w,\d]+)'
    p16='DDRAB\s+VR\s+Version:\s+([\w,\d]+),\s([\w,\d]+)'
    p17='P1V05\s+VR\s+Version:\s+([\w,\d]+),\s([\w,\d]+)'

    outDict['BMC_VER'] = 'NA'
    outDict['TPM_VER'] = 'NA'
    outDict['FCMCPLD_VER'] = 'NA'
    outDict['PWRCPLD_VER'] = 'NA'
    outDict['SCMCPLD_VER'] = 'NA'
    outDict['SMBCPLD_VER'] = 'NA'
    outDict['FPGA1_VER'] = 'NA'
    outDict['FPGA2_VER'] = 'NA'
    outDict['BRIDGE_VER'] = 'NA'
    outDict['BRIDGE_BOOTLOADER_VER'] = 'NA'
    outDict['BIOS_VER'] = 'NA'
    outDict['CPLD_VER'] = 'NA'
    outDict['ME_VER'] = 'NA'
    outDict['PVCCIN_VER'] = 'NA'
    outDict['DDRAB_VER'] = 'NA'
    outDict['P1V05_VER'] = 'NA'

    for line in output.splitlines():
        line = line.strip()

        # if daily built BMC version
        match = re.search(p0,line)
        if match:
            found += 1
            outDict['BMC_VER'] = match.group(2)
            continue
        else:
            # if official BMC version
            match = re.search(p1,line)
            if match:
                found += 1
                outDict['BMC_VER'] = match.group(2)
                continue

            match = re.search(p2,line)
            if match:
                found += 1
                outDict['BMC_VER'] = match.group(2)
                continue

        # TPM
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['TPM_VER'] = match.group(1)
            continue

        # FCMCPLD
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['FCMCPLD_VER'] = match.group(1)
            continue

        # PWRCPLD
        match = re.search(p5,line)
        if match:
            found += 1
            outDict['PWRCPLD_VER'] = match.group(1)
            continue

        # SCMCPLD
        match = re.search(p6,line)
        if match:
            found += 1
            outDict['SCMCPLD_VER'] = match.group(1)
            continue

        # SMBCPLD
        match = re.search(p7,line)
        if match:
            found += 1
            outDict['SMBCPLD_VER'] = match.group(1)
            continue

        # FPGA1
        match = re.search(p8,line)
        if match:
            found += 1
            outDict['FPGA1_VER'] = match.group(1)
            continue

        # FPGA2
        match = re.search(p9,line)
        if match:
            found += 1
            outDict['FPGA2_VER'] = match.group(1)
            continue

        # BRIDGE
        match = re.search(p10,line)
        if match:
            found += 1
            outDict['BRIDGE_VER'] = match.group(1)
            continue

        # BRIDGE BOOTLOADER
        match = re.search(p11,line)
        if match:
            found += 1
            outDict['BRIDGE_BOOTLOADER_VER'] = match.group(1)
            continue

        # BIOS
        match = re.search(p12,line)
        if match:
            found += 1
            outDict['BIOS_VER'] = match.group(1)
            continue

        # CPLD
        match = re.search(p13,line)
        if match:
            found += 1
            outDict['CPLD_VER'] = match.group(1)
            continue

        # ME
        match = re.search(p14,line)
        if match:
            found += 1
            outDict['ME_VER'] = match.group(1)
            continue

        # PVCCIN
        match = re.search(p15,line)
        if match:
            found += 1
            outDict['PVCCIN_VER'] = (match.group(1) + ', ' + match.group(2))
            continue

        # DDRAB
        match = re.search(p16,line)
        if match:
            found += 1
            outDict['DDRAB_VER'] = (match.group(1) + ', ' + match.group(2))
            continue

        # P1V05
        match = re.search(p17,line)
        if match:
            found += 1
            outDict['P1V05_VER'] = (match.group(1) + ', ' + match.group(2))
            continue

    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
        return outDict


#######################################################################################################################
# Function Name: PARSE_FPGA_Versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
def PARSE_FPGA_Versions(output):
    outDict = parser()
    found = 0
    p1='DOM_FPGA_1\s+:\s+([\d]+\.[\d]+)'
    p2='DOM_FPGA_2\s+:\s+([\d]+\.[\d]+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            found += 1
            outDict['FPGA1_VER'] = match.group(1)
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['FPGA2_VER'] = match.group(1)

    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
        return outDict


#######################################################################################################################
# Function Name: PARSE_Temp_Volt_Limits
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
def PARSE_Temp_Volt_Limits(output):
    outDict = parser()
    found = 0
    p1='Min_temperature_limit:([ \t])+(\d+)C'
    p2='Max_temperature_limit:([ \t])+(\d+)C'
    p3='Low_Voltage_limit:([ \t])+(\d+)mV'
    p4='Max_Voltage_limit:([ \t])+(\d+)mV'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1,line)
        if match:
            found += 1
            outDict['MIN_TEMP'] = match.group(1)
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['MAX_TEMP'] = match.group(1)
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['MIN_VOLT'] = match.group(1)
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['MAX_VOLT'] = match.group(1)

    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
        return outDict


###############################################################################################
# Function Name: PARSE_port_link_status_with_unexpected_return
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_port_link_status_with_unexpected_return(output):
    outDict = parser()
    outDict['port_number'] = []
    temp_dict = {'link_name':'null_name'}

    p1 = r'^Link \[(\d+)\] name (.+G), .*\s*.+link (\w+), pcs (\w+)'
    link_number = 0

    temp = re.findall(r'^Li.*?s True', output, flags=re.M|re.DOTALL)
    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info('---------------- got potential %s lines.' % len(temp))
    for line in temp:
        line = line.strip()
        line=line.replace('\r\n', '')
        line=line.replace('\n', '')

        match = re.search(p1, line)
        if match:
          link_number += 1
          outDict['port_number'].extend(temp_dict)

    dLibObj.wpl_log_info('---------------- parsed out %s ports.' % link_number)

    temp = re.findall(r'Link .*?s True', output, flags=re.M|re.DOTALL)
    for line in temp:
        line = line.strip()
        line=line.replace('\r\n', '')
        line=line.replace('\n', '')

        match = re.search(p1, line)
        if match:
            linkNum = int(match.group(1))
            outDict['port_number'][linkNum]= {'link_name': match.group(2)}
            outDict['port_number'][linkNum].update({'link_status': match.group(3)})
            outDict['port_number'][linkNum].update({'pcs_status': match.group(4)})

    dLibObj.wpl_log_info(outDict)
    return outDict


###############################################################################################
# Function Name: PARSE_test_result
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_test_result(output):
    outDict = parser()

    p1 = r'^(OK|FAILED|True|False|GB Initialization Test.*PASS|.*Loopback Test ---------- PASS)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['Test Result'] = match.group(1)

    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)
    return outDict


#######################################################################################################################
# Function Name: MINIPACK2_PARSE_FW_UTIL_Versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
def MINIPACK2_PARSE_FW_UTIL_Versions(output):
    outDict = parser()
    found = 0

    p0='BMC\s+Version:\s+fuji-([\w,\d]+-dirty)'
    p1='BMC\s+Version:\s+fuji-v([\d]+\.[\d]+)'
    p2='TPM\s+Version:\s+([\d]+\.[\d]+)'
    p3='FCMCPLD\s+B:\s+([\d]+\.[\d]+\.[\d]+)'
    p4='FCMCPLD\s+T:\s+([\d]+\.[\d]+\.[\d]+)'
    p5='PWRCPLD\s+L:\s+([\d]+\.[\d]+\.[\d]+)'
    p6='PWRCPLD\s+R:\s+([\d]+\.[\d]+\.[\d]+)'
    p7='SCMCPLD:\s+([\d]+\.[\d]+\.[\d]+)'
    p8='SMBCPLD:\s+([\d]+\.[\d]+\.[\d]+)'
    p9='IOB\s+FPGA:\s+([\d]+\.[\d]+)'
    p10='PIM1\s+DOMFPGA:\s+([\d]+\.[\d]+)'
    p11='PIM2\s+DOMFPGA:\s+([\d]+\.[\d]+)'
    p12='PIM3\s+DOMFPGA:\s+([\d]+\.[\d]+)'
    p13='PIM4\s+DOMFPGA:\s+([\d]+\.[\d]+)'
    p14='PIM5\s+DOMFPGA:\s+([\d]+\.[\d]+)'
    p15='PIM6\s+DOMFPGA:\s+([\d]+\.[\d]+)'
    p16='PIM7\s+DOMFPGA:\s+([\d]+\.[\d]+)'
    p17='PIM8\s+DOMFPGA:\s+([\d]+\.[\d]+)'
    p18='Bridge-IC\s+Version:\s+v([\d]+\.[\d]+)'
    p19='Bridge-IC\s+Bootloader\s+Version:\s+v([\d]+\.[\d]+)'
    p20='BIOS\s+Version:\s+([\w,\d]+_[\w,\d]+)'
    p21='CPLD\s+Version:\s+([\w,\d]+)'
    p22='ME\s+Version:\s+([\d]+\.[\d]+\.[\d]+\.[\d]+)'
    p23='PVCCIN\s+VR\s+Version:\s+([\w,\d]+),\s+([\w,\d]+)'
    p24='DDRAB\s+VR\s+Version:\s+([\w,\d]+),\s+([\w,\d]+)'
    p25='P1V05\s+VR\s+Version:\s+([\w,\d]+),\s+([\w,\d]+)'

    outDict['BMC_VER'] = 'NA'
    outDict['TPM_VER'] = 'NA'
    outDict['FCMCPLD_B_VER'] = 'NA'
    outDict['FCMCPLD_T_VER'] = 'NA'
    outDict['PWRCPLD_L_VER'] = 'NA'
    outDict['PWRCPLD_R_VER'] = 'NA'
    outDict['SCMCPLD_VER'] = 'NA'
    outDict['SMBCPLD_VER'] = 'NA'
    outDict['IOB_FPGA_VER'] = 'NA'
    outDict['PIM1_FPGA_VER'] = 'NA'
    outDict['PIM2_FPGA_VER'] = 'NA'
    outDict['PIM3_FPGA_VER'] = 'NA'
    outDict['PIM4_FPGA_VER'] = 'NA'
    outDict['PIM5_FPGA_VER'] = 'NA'
    outDict['PIM6_FPGA_VER'] = 'NA'
    outDict['PIM7_FPGA_VER'] = 'NA'
    outDict['PIM8_FPGA_VER'] = 'NA'
    outDict['BRIDGE_VER'] = 'NA'
    outDict['BRIDGE_BOOTLOADER_VER'] = 'NA'
    outDict['BIOS_VER'] = 'NA'
    outDict['CPLD_VER'] = 'NA'
    outDict['ME_VER'] = 'NA'
    outDict['PVCCIN_VER'] = 'NA'
    outDict['DDRAB_VER'] = 'NA'
    outDict['P1V05_VER'] = 'NA'

    for line in output.splitlines():
        line = line.strip()

        # BMC
        match = re.search(p0,line)
        if match:
            found += 1
            outDict['BMC_VER'] = match.group(1)
            continue
        else:
            match = re.search(p1,line)
            if match:
                found += 1
                outDict['BMC_VER'] = match.group(1)
                continue

        # TPM
        match = re.search(p2,line)
        if match:
            found += 1
            outDict['TPM_VER'] = match.group(1)
            continue

        # FCMCPLD B
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['FCMCPLD_B_VER'] = match.group(1)
            continue

        # FCMCPLD T
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['FCMCPLD_T_VER'] = match.group(1)
            continue

        # PWRCPLD L
        match = re.search(p5,line)
        if match:
            found += 1
            outDict['PWRCPLD_L_VER'] = match.group(1)
            continue

        # PWRCPLD R
        match = re.search(p6,line)
        if match:
            found += 1
            outDict['PWRCPLD_R_VER'] = match.group(1)
            continue

        # SCMCPLD
        match = re.search(p7,line)
        if match:
            found += 1
            outDict['SCMCPLD_VER'] = match.group(1)
            continue

        # SMBCPLD
        match = re.search(p8,line)
        if match:
            found += 1
            outDict['SMBCPLD_VER'] = match.group(1)
            continue

        # IOB FPGA
        match = re.search(p9,line)
        if match:
            found += 1
            outDict['IOB_FPGA_VER'] = match.group(1)
            continue

        # PIM1 DOMFPGA
        match = re.search(p10,line)
        if match:
            found += 1
            outDict['PIM1_FPGA_VER'] = match.group(1)
            continue

        # PIM2 DOMFPGA
        match = re.search(p11,line)
        if match:
            found += 1
            outDict['PIM2_FPGA_VER'] = match.group(1)
            continue

        # PIM3 DOMFPGA
        match = re.search(p12,line)
        if match:
            found += 1
            outDict['PIM3_FPGA_VER'] = match.group(1)
            continue

        # PIM4 DOMFPGA
        match = re.search(p13,line)
        if match:
            found += 1
            outDict['PIM4_FPGA_VER'] = match.group(1)
            continue

        # PIM5 DOMFPGA
        match = re.search(p14,line)
        if match:
            found += 1
            outDict['PIM5_FPGA_VER'] = match.group(1)
            continue

        # PIM6 DOMFPGA
        match = re.search(p15,line)
        if match:
            found += 1
            outDict['PIM6_FPGA_VER'] = match.group(1)
            continue

        # PIM7 DOMFPGA
        match = re.search(p16,line)
        if match:
            found += 1
            outDict['PIM7_FPGA_VER'] = match.group(1)
            continue

        # PIM8 DOMFPGA
        match = re.search(p17,line)
        if match:
            found += 1
            outDict['PIM8_FPGA_VER'] = match.group(1)
            continue

        # BRIDGE
        match = re.search(p18,line)
        if match:
            found += 1
            outDict['BRIDGE_VER'] = match.group(1)
            continue

        # BRIDGE BOOTLOADER
        match = re.search(p19,line)
        if match:
            found += 1
            outDict['BRIDGE_BOOTLOADER_VER'] = match.group(1)
            continue

        # BIOS
        match = re.search(p20,line)
        if match:
            found += 1
            outDict['BIOS_VER'] = match.group(1)
            continue

        # CPLD
        match = re.search(p21,line)
        if match:
            found += 1
            outDict['CPLD_VER'] = match.group(1)
            continue

        # ME
        match = re.search(p22,line)
        if match:
            found += 1
            outDict['ME_VER'] = match.group(1)
            continue

        # PVCCIN
        match = re.search(p23,line)
        if match:
            found += 1
            outDict['PVCCIN_VER'] = (match.group(1) + ', ' + match.group(2))
            continue

        # DDRAB
        match = re.search(p24,line)
        if match:
            found += 1
            outDict['DDRAB_VER'] = (match.group(1) + ', ' + match.group(2))
            continue

        # P1V05
        match = re.search(p25,line)
        if match:
            found += 1
            outDict['P1V05_VER'] = (match.group(1) + ', ' + match.group(2))
            continue

    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
        return outDict


######################################################################################################################
# Function Name: CLOUDRIPPER_PARSE_FW_UTIL_Versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
def CLOUDRIPPER_PARSE_FW_UTIL_Versions(output):
    outDict = parser()
    found = 0

    p0='BMC\s+Version:\s+([\w,\d]+)-([\w,\d]+-dirty)'
    p1='BMC\s+Version:\s+([\w,\d]+)-v([\d]+\.[\d]+)'
    p2='BMC\s+Version:\s+([\w,\d]+)-([\w,\d]+)'
    p3='TPM\s+Version:\s+([\d]+\.[\d]+)'
    p4='FCMCPLD:\s+([\d]+\.[\d]+)'
    p5='PWRCPLD:\s+([\d]+\.[\d]+)'
    p6='SCMCPLD:\s+([\d]+\.[\d]+)'
    p7='SMBCPLD:\s+([\d]+\.[\d]+)'
    p8='DOMFPGA1:\s+([\d]+\.[\d]+)'
    p9='DOMFPGA2:\s+([\d]+\.[\d]+)'
    p10='Bridge-IC\s+Version:\s+v([\d]+\.[\d]+)'
    p11='Bridge-IC\s+Bootloader\s+Version:\s+v([\d]+\.[\d]+)'
    p12='BIOS\s+Version:\s+([\w,\d]+_[\w,\d]+)'
    p13='CPLD\s+Version:\s+([\w,\d]+)'
    p14='ME\s+Version:\s+([\d]+\.[\d]+\.[\d]+\.[\d]+)'
    p15='PVCCIN\s+VR\s+Version:\s+([\w,\d]+),\s([\w,\d]+)'
    p16='DDRAB\s+VR\s+Version:\s+([\w,\d]+),\s([\w,\d]+)'
    p17='P1V05\s+VR\s+Version:\s+([\w,\d]+),\s([\w,\d]+)'

    outDict['BMC_VER'] = 'NA'
    outDict['TPM_VER'] = 'NA'
    outDict['FCMCPLD_VER'] = 'NA'
    outDict['PWRCPLD_VER'] = 'NA'
    outDict['SCMCPLD_VER'] = 'NA'
    outDict['SMBCPLD_VER'] = 'NA'
    outDict['FPGA1_VER'] = 'NA'
    outDict['FPGA2_VER'] = 'NA'
    outDict['BRIDGE_VER'] = 'NA'
    outDict['BRIDGE_BOOTLOADER_VER'] = 'NA'
    outDict['BIOS_VER'] = 'NA'
    outDict['CPLD_VER'] = 'NA'
    outDict['ME_VER'] = 'NA'
    outDict['PVCCIN_VER'] = 'NA'
    outDict['DDRAB_VER'] = 'NA'
    outDict['P1V05_VER'] = 'NA'

    for line in output.splitlines():
        line = line.strip()

        # if daily built BMC version
        match = re.search(p0,line)
        if match:
            found += 1
            outDict['BMC_VER'] = match.group(2)
            continue
        else:
            # if official BMC version
            match = re.search(p1,line)
            if match:
                found += 1
                outDict['BMC_VER'] = match.group(2)
                continue

            match = re.search(p2,line)
            if match:
                found += 1
                outDict['BMC_VER'] = match.group(2)
                continue

        # TPM
        match = re.search(p3,line)
        if match:
            found += 1
            outDict['TPM_VER'] = match.group(1)
            continue

        # FCMCPLD
        match = re.search(p4,line)
        if match:
            found += 1
            outDict['FCMCPLD_VER'] = match.group(1)
            continue

        # PWRCPLD
        match = re.search(p5,line)
        if match:
            found += 1
            outDict['PWRCPLD_VER'] = match.group(1)
            continue

        # SCMCPLD
        match = re.search(p6,line)
        if match:
            found += 1
            outDict['SCMCPLD_VER'] = match.group(1)
            continue
        # SMBCPLD
        match = re.search(p7,line)
        if match:
            found += 1
            outDict['SMBCPLD_VER'] = match.group(1)
            continue

        # FPGA1
        match = re.search(p8,line)
        if match:
            found += 1
            outDict['FPGA1_VER'] = match.group(1)
            continue

        # FPGA2
        match = re.search(p9,line)
        if match:
            found += 1
            outDict['FPGA2_VER'] = match.group(1)
            continue

        # BRIDGE
        match = re.search(p10,line)
        if match:
            found += 1
            outDict['BRIDGE_VER'] = match.group(1)
            continue

        # BRIDGE BOOTLOADER
        match = re.search(p11,line)
        if match:
            found += 1
            outDict['BRIDGE_BOOTLOADER_VER'] = match.group(1)
            continue

        # BIOS
        match = re.search(p12,line)
        if match:
            found += 1
            outDict['BIOS_VER'] = match.group(1)
            continue

        # CPLD
        match = re.search(p13,line)
        if match:
            found += 1
            outDict['CPLD_VER'] = match.group(1)
            continue

        # ME
        match = re.search(p14,line)
        if match:
            found += 1
            outDict['ME_VER'] = match.group(1)
            continue

        # PVCCIN
        match = re.search(p15,line)
        if match:
            found += 1
            outDict['PVCCIN_VER'] = (match.group(1) + ', ' + match.group(2))
            continue

        # DDRAB
        match = re.search(p16,line)
        if match:
            found += 1
            outDict['DDRAB_VER'] = (match.group(1) + ', ' + match.group(2))
            continue

        # P1V05
        match = re.search(p17,line)
        if match:
            found += 1
            outDict['P1V05_VER'] = (match.group(1) + ', ' + match.group(2))
            continue

    dLibObj = InitFrameworkLib.getDiagLibObj()
    dLibObj.wpl_log_info(outDict)

    if found:
        return outDict


