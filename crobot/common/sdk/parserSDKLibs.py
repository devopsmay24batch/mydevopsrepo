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

import Logger as log
from dataStructure import parser
from SdkLib import *
import re

###############################################################################################
# Function Name: PARSE_sdk_info
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_sdk_info(output):
    outDict = parser()

    p1 = r'## (.+): (.*)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = match.group(1)
            outDict[key] = match.group(2)

    log.info(outDict)
    return outDict


###############################################################################################
# Function Name: PARSE_sdk_version
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_sdk_version(output):
    outDict = parser()
    p1 = r'(.*SDK Version): (.+)'
    p2 = r'(.*SDK Release Version): (.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        match2 = re.search(p2, line)
        if match:
            key = match.group(1).strip()
            outDict[key] = match.group(2).strip()
        elif match2:
            key = match2.group(1).strip()
            outDict[key] = match2.group(2).strip()

    log.info(outDict)
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

    p1 = r'^(OK|FAILED|True|False|GB Initialization Test.*PASS|.*Loopback Test.*?PASS|.*do_reinit_test-.*TEST.*?PASS)'
    match_flag = 0
    outDict['Test Result'] = ""
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['Test Result'] = match.group(1)
            match_flag = 1


    log.info(outDict)
    if match_flag == 0:
        log.info("Didn't get test result in output: ***{}***".format(output))
    return outDict

###############################################################################################
# Function Name: PARSE_test_result_more_keywords
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_test_result_more_keywords(output, keywords, strict_seq=False):
    outDict = parser()

    for line in output.splitlines():
        line = line.strip()
        if strict_seq:
          word = keywords[0]
          if re.search(word, line):
            keywords.remove(word)
            log.info('found keyword %s and remove it' % (word))
        else:
          for word in keywords:
            if re.search(word, line):
              keywords.remove(word)
              log.info('found keyword %s and remove it' % (word))
        if len(keywords) == 0:
          log.info('found all keywords') 
          return 0

    log.info('did not find all keywords, left %s' % (keywords)) 
    return len(keywords)



###############################################################################################
# Function Name: PARSE_port_link_status
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_port_link_status(output):
    outDict = parser()
    outDict['port_number'] = []
    temp_dict = {'link_name':'null_name'}

    p1 = r'Link \[(\d+)\] name (.+G),.+link (\w+), pcs (\w+)'
    link_number = 0
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
          link_number += 1
          outDict['port_number'].extend(temp_dict)

    log.info('parsed out %s ports.' % link_number)

    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            linkNum = int(match.group(1))
            outDict['port_number'][linkNum]= {'link_name': match.group(2)}
            outDict['port_number'][linkNum].update({'link_status': match.group(3)})
            outDict['port_number'][linkNum].update({'pcs_status': match.group(4)})

    log.info(outDict)
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
    port_list = []
    temp = []

    temp_lst = re.findall(r'^Li.*?s True', output, flags=re.M|re.DOTALL)
    for line in temp_lst:
        if line not in temp:
            temp.append(line)
    potential_ports = len(temp)
    log.info('---------------- got potential %d lines.' % potential_ports)

    for line in temp:
        line = line.strip()
        line=line.replace('\r\n', '')
        line=line.replace('\n', '')

        match = re.search(p1, line)
        if match:

            linkNum = int(match.group(1))
            port_list.append(linkNum)
            outDict['port_number'].append(temp_dict)
            outDict['port_number'][link_number]= {'link_name': match.group(2)}
            outDict['port_number'][link_number].update({'link_status': match.group(3)})
            outDict['port_number'][link_number].update({'pcs_status': match.group(4)})
            link_number += 1
    log.info('---------------- parsed out %s ports.' % link_number)
    if link_number != potential_ports:
        abnormal_ports = set(port_list) ^ set(range(potential_ports))
        raise RuntimeError("Abnormal ports: {}".format(abnormal_ports))

    log.info(outDict)
    return outDict


###############################################################################################
# Function Name: PARSE_port_ber_lane_status
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_port_ber_lane_status(output, berThreshold=1e-10):
    p1 = r'^mac_index\s+.*'
    p2 = r'^lane\s+.*\s+lane_ber:\s+(\d\.\d+(e-\d+)?)'

    mac_index_group = []
    lane_count = 0
    error_group = {}

    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            mac_index_group.append({})
            lane_count = 0

        match = re.search(p2, line)
        if match:
            if mac_index_group is not None:
              mac_index_group[len(mac_index_group)-1][lane_count] = line
              ber_value = match.group(1)
              mac_index_group_len = len(mac_index_group)
              if float(ber_value) > berThreshold:  
                error_group[mac_index_group_len - 1] = 1
                log.info('------------- found one lane with unusual BER value %s in the mac group %s'%(ber_value, mac_index_group_len - 1))
              lane_count += 1
            else:
              log.info('------------- operated on the null mac_index_group, wrong.\n')
              return None
    return error_group

###############################################################################################
# Function Name: PARSE_port_ber
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################

def PARSE_port_ber(output, nPort=-1):
    outDict = parser()
    parsed = False

    p1 = r'P\d+\s+mp:(\d+)'
    p2 = r'lane_ber:\s+(\d[\de+-.]+\d)'
    for line in output.splitlines():
      line = line.strip()
      match = re.search(p1, line)
      if match:
        nPort += 1
        outDict[nPort] = []
        parsed = True
        continue
      match = re.search(p2, line)
      if match:
        ber = float(match.group(1).strip())
        outDict[nPort].append(ber)
        parsed = True
        continue

    if parsed:
      log.info(outDict)
      return outDict
    else:
      return None

###############################################################################################
# Function Name: PARSE_port_value_range_check
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_port_value_range_check(output, keywords_to_check, valid_value_range=()):
    outDict = parser()
    parsed = False
    min_value, max_value = valid_value_range
    p1 = keywords_to_check
    failcount = 0

    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            value = float(match.group(1).strip())
            if value <= min_value or value >= max_value:
              log.info('------------- found one with unusual value %s beyond min:%s, max:%s'%(value, min_value, max_value))
              failcount += 1

    return failcount

###############################################################################################
# Function Name: PARSE_port_fec
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_port_fec(output):
    outDict = parser()
    outDict['port_number'] = []
    temp_dict = {'link_name':'null_name'}

    #p1 = r'Link \[(\d+)\] name (.+G),.+, FEC (\d+).+Rx.+Mpps (\d+\.\d+) Gbps (\d+\.\d+), Tx.+Mpps (\d+\.\d+) Gbps (\d+\.\d+)'
    p1 = r'Link \[(\d+)\] name (.+G),.+, FEC (\d+)'

    link_number = 0
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            linkNum = int(match.group(1))
            outDict['port_number'].extend(temp_dict)
            link_number += 1

    log.info('parsed out %s ports.' % link_number)

    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            linkNum = int(match.group(1))
            outDict['port_number'][linkNum]= {'link_name': match.group(2)}
            outDict['port_number'][linkNum].update({'FEC': match.group(3)})
            # outDict['port_number'][linkNum]['Rx Gbps'] = match.group(5)
            # outDict['port_number'][linkNum]['Tx Gbps'] = match.group(7)

    log.info(outDict)
    return outDict

###############################################################################################
# Function Name: PARSE_port_fec_with_unexpected_return
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_port_fec_with_unexpected_return(output):
    outDict = parser()
    outDict['port_number'] = []
    temp_dict = {'link_name':'null_name'}

    #p1 = r'Link \[(\d+)\] name (.+G),.+, FEC (\d+).+Rx.+Mpps (\d+\.\d+) Gbps (\d+\.\d+), Tx.+Mpps (\d+\.\d+) Gbps (\d+\.\d+)'
    p1 = r'^L.* \[(\d+)\] name (.+G),.+FEC (\d+)'

    link_number = 0
    temp = re.findall(r'^L.*?s True', output, flags=re.M|re.DOTALL)
    log.info('---------------- got potential %s lines.' % len(temp))
    for line in temp:
        line = line.strip()
        line=line.replace('\r\n', '')
        line=line.replace('\n', '')
        match = re.search(p1, line)
        if match:
            outDict['port_number'].append(temp_dict)
            linkNum = int(match.group(1))
            outDict['port_number'][link_number]= {'link_name': match.group(2)}
            outDict['port_number'][link_number].update({'FEC': match.group(3)})
            link_number += 1

    log.info('parsed out %s ports.' % link_number)
    log.info(outDict)
    return outDict

###############################################################################################
# Function Name: PARSE_port_traffic
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
def PARSE_port_traffic(output):
    outDict = parser()

    p1 = r'.* Rx (\d+) (\d+),.* Tx (\d+) (\d+), .*'
    match_flag = 0
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['rx_bytes'] = int(match.group(1))
            outDict['tx_bytes'] = int(match.group(3))
            outDict['rx_gbps'] = float(match.group(2))
            outDict['tx_gbps'] = float(match.group(4))
            match_flag = 1

    if match_flag == 0:
        log.info(output)
        log.info("Didn't find traffic data.")
    log.info(outDict)
    return outDict

