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
import pexpect
import re
import random
import time
import os
import copy
from subprocess import Popen,PIPE
from robot.libraries.BuiltIn import BuiltIn
from dataStructure import nestedDict, parser

import Const
import Logger as log
from Device import Device
import DeviceMgr
from SwImage import SwImage
from Server import Server
import YamlParse
from crobot.Decorator import logThis


def critical_step(StepNumber, name):
    log.debug('Entering procedure critical_step[%s]\n '%(str(locals())))
    return BuiltIn().run_keyword(name)

def step(StepNumber, name, *args):
    """ when use this api/keyword , if one step fail, the following steps will not be executed """

    log.debug('Entering procedure step[%s]\n '%(str(locals())))
    return BuiltIn().run_keyword(name, *args)

def independent_step(StepNumber, name, *args):
    """ this api/keyword is used in the case all the steps are independent,
    if one step failed, the following steps can be executed one by one   """

    log.debug('Entering procedure independent_step[%s]\n '%(str(locals())))
    return BuiltIn().run_keyword_and_continue_on_failure(name, *args)

def sub_case(case_name, name, *args):
    log.debug('Entering procedure sub_case[%s]\n '%(str(locals())))
    return BuiltIn().run_keyword(name, *args)

def ssh_login_bmc(device):
    log.debug('Entering procedure ssh_login_bmc[%s]\n '%(str(locals())))
    ip = get_ip_address(device, 'eth0', Const.BOOT_MODE_OPENBMC)
    DeviceMgr.usingSsh = True
    deviceObj = DeviceMgr.getDevice(device)
    deviceObj.bmcIP = ip
    time.sleep(30)
    deviceObj.loginBmc()

def ssh_login_cpu(device):
    DeviceMgr.usingSsh = True
    deviceObj = DeviceMgr.getDevice(device)
    deviceObj.loginCpu()

def ssh_disconnect(device):
    log.debug('Entering procedure ssh_disconnect[%s]\n '%(str(locals())))
    deviceObj = DeviceMgr.getDevice(device)
    deviceObj.disconnect()
    DeviceMgr.usingSsh = False

def run_command(cmd, deviceObj=None, prompt=None, timeout=60, CR=True):
    log.debug("Entering procedure: run_command")

    promptStr = prompt
    if not prompt:
        mode = deviceObj.currentBootMode
        prompt_dict = { Const.BOOT_MODE_UBOOT  : deviceObj.promptUboot,
                        Const.BOOT_MODE_ONIE   : deviceObj.promptOnie,
                        Const.BOOT_MODE_DIAGOS : deviceObj.promptDiagOS
                }
        promptStr = prompt_dict.get(mode, "")
    if isinstance(cmd, str):
        cmd_list = [ cmd ]
    elif isinstance(cmd,list):
        cmd_list = cmd
    else:
        raise Exception("run_command not support run {}".format(type(cmd)))
    output = ""
    for cmdx in cmd_list:
        if len(cmdx) > 50:
            due_prompt = escapeString(cmdx.lstrip()[len(cmdx)-50:50-len(cmdx)])
        else:
            due_prompt = escapeString(cmdx.lstrip()[:5])
        #due_prompt = escapeString(cmdx.lstrip()[:5])
        finish_prompt = "{}[\s\S]+{}".format(due_prompt, promptStr)
        if CR:
            cmdx += "\n"
        deviceObj.sendMsg(cmdx)
        output += deviceObj.read_until_regexp(finish_prompt, timeout=timeout)

    return output

def get_file_by_scp(ipaddr, username, password, src_dir, fname, local_dir):
    """ copy file from remote server to local """

    log.debug('Entering procedure get_file_by_scp [%s]\n '%(str(locals())))
    max_retry_cnt = 3
    cur_cnt = 0
    cmd_str1 = ("/usr/bin/scp")
    src_dir_fname = (src_dir + '/' + fname)
    cmd_str2 = (username + '@' + ipaddr + ':' + src_dir_fname)
    cmd = (cmd_str1 + " " + cmd_str2 + " " + local_dir)
    log.debug ("sending network cmd: " + str(cmd))

    rtn_code = 1
    for cur_cnt in range(max_retry_cnt):
        log.cprint ("Loop cnt: " + str(cur_cnt))
        try:
            proc = pexpect.spawn(cmd)
            result = proc.expect(['^.*100\%', 'password:', '(yes/no)', 'ssh.*refused$', '.*denied', pexpect.EOF, pexpect.TIMEOUT], 90)
            if result == 0:
                log.cprint("downloaded successfully")
                break

            if result == 1:
                proc.sendline(password)
                log.cprint("password sent")
            if result == 2: #
                proc.sendline("yes")
                log.cprint("yes sent")
                result = proc.expect(['^.*100\%', 'password:'])
                if result == 0:
                    log.cprint("downloaded successfully")
                    break
                proc.sendline(password)
                log.cprint("password sent")
            proc.expect('^.*100\%', 90)
            log.cprint("downloaded successfully")
            break

        except Exception as e:
            log.cprint ("Unknown error [%s]: " % e)
            execute_local_cmd('ssh-keygen -R ' + ipaddr)

        proc.close()
        cur_cnt += 1

    if cur_cnt == max_retry_cnt:
        log.cprint ("Error downloading file[" + fname + "] from server !\n")
        return 1
    else:
        return 0

###########################################################################################
### Function to copy file from other server into DUT through scp, mode=[openbmc|centos] ###
###########################################################################################
def copy_files_through_scp(device, username, password,server_ip, filelist: list, filepath, destination_path, mode='None', swap=False, ipv6=False, interface='None', timeout=Const.COPYING_TIME, retry=2):
    log.debug("Entering copy_files_through_scp with args : %s" %(str(locals())))
    errCount = 0
    deviceObj = Device.getDeviceObject(device)
    if mode != 'None':
        deviceObj.getPrompt(mode)
    for fileName in filelist:
        if fileName == '':
            continue
        success = False
        for retryCount in range(retry):
            log.debug("retryCount: %d"%(retryCount))
            deviceObj.flush()
            try:
                if swap:
                    if ipv6:
                        cmd = 'scp %s/%s %s@[%s'%(filepath, fileName, username, server_ip)
                        if server_ip.startswith('2001'):
                            cmd += ']:' + destination_path
                        else:
                            cmd += '%' + interface + ']:' + destination_path
                        log.cprint(cmd)
                        deviceObj.sendCmd(cmd)
                    else:
                        deviceObj.sendCmd("scp %s/%s %s@%s://%s" % (filepath, fileName, username, server_ip, destination_path))
                else:
                    if ipv6:
                        if not server_ip.startswith('2001'):
                            cmd = 'scp -6 %s@[%s' % (username, server_ip)
                            cmd += ('%' + interface + ']:' + filepath + '/' + fileName)
                            cmd += (' ' + destination_path + '/')
                        else:
                            cmd = 'scp -6 %s@[%s' % (username, server_ip)
                            cmd += (']:' + filepath + '/' + fileName)
                            cmd += (' ' + destination_path + '/')
                        log.cprint(cmd)
                        deviceObj.sendCmd(cmd)
                    else:
                        deviceObj.sendCmd("scp %s@%s://%s/%s %s" % (username, server_ip, filepath, fileName, destination_path))
                promptList = ["(y/n)", "(yes/no)", "password:"]
                patternList = re.compile('|'.join(promptList))
                output1 = deviceObj.read_until_regexp(patternList, 180)
                log.info('output1: ' + str(output1))

                if re.search("(yes/no)",output1):
                    deviceObj.transmit("yes")
                    deviceObj.receive("password:")
                    deviceObj.transmit("%s"%password)
                elif re.search("(y/n)",output1):
                    deviceObj.transmit("y")
                    deviceObj.receive("password:")
                    deviceObj.transmit("%s"%password)
                elif re.search("password:",output1):
                    deviceObj.transmit("%s"%password)
                else :
                    log.fail("pattern mismatch")

                currentPromptStr = deviceObj.getCurrentPromptStr()
                currentPromptStr = currentPromptStr if currentPromptStr else "100%|No such file"
                output = deviceObj.read_until_regexp(currentPromptStr,timeout=timeout)
                p0 = ".*100\%"
                p1 = "No such file or directory"
                if re.search(p0, output):
                    log.info("Successfully copy file: %s"%(fileName))
                    success = True
                    break    # continue to copy next file
                elif re.search(p1, output):
                    log.error("%s"%(p1))
                    raise RuntimeError(p1 + ': ' + fileName)
            except:
                if ipv6:
                    deviceObj.executeCmd('ssh-keygen -R ' + server_ip + '%' + interface)
                else:
                    execute_local_cmd('ssh-keygen -R ' + server_ip)
                continue   # come to next try

        if not success:
            raise RuntimeError("Copy file {} through scp failed!".format(fileName))
    return 0

def get_current_update_version(imageName):
    return SwImage.getSwImage(imageName).currentUpdateVer

def download_images(device, imageName, ipv6=False, destinationDir = None):
    log.debug("Entering download_images with args : %s" %(str(locals())))
    imageObj = SwImage.getSwImage(imageName)
    serverObj = Server.getServer(imageObj.imageServer, needLogin=False)
    if imageName in ['CPLD', 'PSU']:
        images = list(imageObj.oldImage.values()) + list(imageObj.newImage.values())
    else:
        images = imageObj.getImageList()
    if ipv6:
        serverIP = serverObj.managementIPV6
    else:
        serverIP = serverObj.managementIP
    hostDir = imageObj.hostBaseDir + '/' + imageObj.hostImageDir
    if destinationDir == None:
        destinationDir = imageObj.localImageDir
    copy_files_through_scp(device, serverObj.username, serverObj.password, serverIP, images, hostDir, destinationDir, ipv6=ipv6)

def download_image(device, imageName, ipv6=False, destinationDir = None, upgrade=True, hostBaseDir=''):
    log.debug("Entering download_image with args : %s" %(str(locals())))
    imageObj = SwImage.getSwImage(imageName)
    serverObj = Server.getServer(imageObj.imageServer, needLogin=False)
    if upgrade:
        images = imageObj.newImage
    else:
        images = imageObj.oldImage
    if isinstance(images, str):
        images = [images]
    elif isinstance(images, dict):
        images = images.values()
    elif not isinstance(images, list):
        raise Exception("Images definition is not supported: {}.".format(type(images)))

    if ipv6:
        serverIP = serverObj.managementIPV6
    else:
        serverIP = serverObj.managementIP
    hostDir = os.path.join(hostBaseDir, imageObj.hostImageDir)
    if destinationDir == None:
        destinationDir = imageObj.localImageDir
    copy_files_through_scp(device, serverObj.username, serverObj.password, serverIP, images, hostDir, destinationDir, ipv6=ipv6)

def tftp_get_files(device, server_ip="", file_list=None, renamed_file_list=None, src_path="", dst_path=None, timeout=200, retry=3):
    log.debug("Entering tftp_get_files with args : %s" %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if not server_ip:
        server_ip = get_device_info("PC").get("managementIP","")
    if dst_path:
        deviceObj.sendCmd("cd {}".format(dst_path))
    for i in range(len(file_list)):
        cmd = "tftp -g {} -r {} && echo -e '\nok' || echo -e '\nfail' ".format(server_ip, os.path.join(src_path, file_list[i]))
        if renamed_file_list and i < len(renamed_file_list):
            cmd = "tftp -g {} -r {} -l {} && echo -e '\nok' || echo -e '\nfail' ".format(server_ip,
                    os.path.join(src_path, file_list[i]), renamed_file_list[i])
        prompt = "\nok|\nfail"
        for i in range(retry):
            try:
                output = deviceObj.sendCmdRegexp(cmd, prompt, timeout=timeout)
                if not re.search("^ok", output, re.M):
                    raise Exception("Didn't found successful message")
                break
            except:
                log.info("Download file failed {} times, left retry {} times.".format(i+1, retry-i-1))
                if i+1 == retry:
                    raise Exception("Download {} failed after tried {} times.".format(file_list[i], retry))
                else:
                    continue

def clean_images(device, imageName):
    log.debug("Entering clean_images with args : %s" %(str(locals())))
    imageObj = SwImage.getSwImage(imageName)
    if imageName in ['CPLD', 'PSU']:
        images = list(imageObj.oldImage.values()) + list(imageObj.newImage.values())
    else:
        images = imageObj.getImageList()
    deviceObj = Device.getDeviceObject(device)
    for fileName in images:
        cmd = "rm -f %s/%s"%(imageObj.localImageDir, fileName)
        deviceObj.executeCmd(cmd)
        time.sleep(1)
    cmd1 = "rm -f %s/mpack2_*"%(imageObj.localImageDir)
    if imageName in ['FPGA']:
        deviceObj.executeCmd(cmd1)
        time.sleep(1)
    deviceObj.executeCmd("rmdir %s"%(imageObj.localImageDir))
    time.sleep(1)

def get_ip_address_from_config(device, ipv6=False, staticMode=False):
    log.debug('Entering get_ip_address_from_config with args : %s' %(str(locals())))
    deviceInfo = YamlParse.getDeviceInfo()
    deviceDict = deviceInfo[device]
    if ipv6:
        if staticMode:
            return deviceDict['staticIPV6']
        return deviceDict['managementIPV6']
    return deviceDict['managementIP']

def get_random_ip(device, ipv6=False, staticMode=False):
    log.debug('Entering get_random_ip with args : %s' %(str(locals())))
    ip = get_ip_address_from_config(device, ipv6, staticMode)
    randStr = ''
    if ipv6:
        ip = ip.rstrip(ip.split(':')[-1])
        while randStr == '':
            randStr = "".join(random.sample("0123456789abcdef", 4))
            ### trim leading zeros ###
            randStr = re.sub("^0*", "", randStr)
    else:
        ip = ip.rstrip(ip.split('.')[-1])
        randStr = str(random.randint(20, 160))
    ip = ip + randStr
    log.info("random ip: %s" %ip)
    return ip

def execute_local_cmd(cmd, timeout=10):
    log.debug('\r\nexecute_local_cmd cmd[%s]' %cmd)
    output = ''
    errs = ''
    proc = Popen(cmd, stdout = PIPE, stderr = PIPE, shell = True, encoding='latin-1')
    try:
        # wait for process to complete
        output, errs = proc.communicate(timeout=timeout)
        log.debug(output)
    except Exception as err:
        # clean up if error occurs
        proc.kill()
        log.debug(output)
        raise RuntimeError(str(err))
    log.debug('\r\nSuccessfully execute_local_cmd cmd: [%s]' %cmd)
    return output

# ping it from cap server directly, do not ssh cap server firstly
def exec_local_ping(ipAddress, count, mode=None):
    log.debug("Entering exec_local_ping with args : %s" %(str(locals())))
    cmd = "ping %s -c %s"%(ipAddress, str(count))
    success_msg = str(count) + ' packets transmitted, ' + str(count) + ' (packets )?received, 0% packet loss'
    loss_msg = str(count) + ' packets transmitted, ' + '0 packets received, 100% packet loss'
    output = execute_local_cmd(cmd, 30)
    log.info('output: %s'%(output))
    match = re.search(success_msg, output)
    if match:
        log.success("Found: %s"%(match.group(0)))
        log.success("ping to %s"%ipAddress)
    else:
        log.info("cannot ping to %s"%ipAddress)
        raise RuntimeError("Ping to destination IP address failed")

# ping it from cap server directly, do not ssh cap server firstly
def exec_local_ping6(interface, ipAddress, count, mode):
    ### ping6 -I eth0 fe80::2204:fff:fef0:2ba1 -c 5
    log.debug("Entering exec_local_ping6 with args : %s" %(str(locals())))
    if interface == None:
        cmd = "ping6 %s -c %s" % (ipAddress, str(count))
    else:
        cmd = "ping6 -I %s %s -c %s"%(interface, ipAddress, str(count))
    success_msg = str(count) + ' packets transmitted, ' + str(count) + ' (packets )?received, 0% packet loss'
    output = execute_local_cmd(cmd, 30)
    log.info('output: %s'%(output))
    match=re.search(success_msg, output)
    if match:
        log.success("Found: %s"%(match.group(0)))
        log.success("ping6 to %s"%ipAddress)
    else :
        log.info("cannot ping6 to %s"%ipAddress)
        raise RuntimeError("Ping6 to destination IP address failed")

def config_management_interface(device, interfaceName, ipAddress, netMask, status, mode=None):
    log.debug('Entering config_management_interface with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output1 = deviceObj.executeCmd("ifconfig %s %s netmask %s %s "%(interfaceName, ipAddress, netMask, status),mode=mode)
    output2 = deviceObj.executeCmd ("ifconfig %s"%interfaceName, mode=mode)
    ipformat = '(\d+\.\d+\.\d+\.\d+)'
    l2 = 'inet addr:'+ipformat+' *Bcast:'+ipformat+'  Mask:'+ipformat
    l3 = 'inet ' + ipformat + '.*netmask ' + ipformat + '.*broadcast ' + ipformat
    ip = ''
    mask = ''
    for line in output2.splitlines():
        #print line
        match = re.search(l2, line)
        match2 = re.search(l3, line)
        if match :
            ip = match.group(1)
            mask = match.group(3)
            break
        elif match2:
            ip = match2.group(1)
            mask = match2.group(2)
            break
    if (ip == ipAddress) and (mask == netMask):
        log.success('configuring ip on management interface')
    else:
        log.fail('Failure while configuring ip on management interface')
        raise RuntimeError("Failure while configuring ip on management interface")

def config_management_interface_ipv6(device, interfaceName, ipAddress, prefixlen, status, mode):
    log.debug('Entering config_management_interface_ipv6 with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if mode.lower() == 'openbmc':
        output1 = deviceObj.executeCmd("ifconfig %s %s/%s %s "%(interfaceName, ipAddress, prefixlen, status), mode=mode)
        output2 = deviceObj.executeCmd("ifconfig %s"%interfaceName, mode=mode)
    elif mode.lower() == 'centos' or mode.lower() == 'diagos':
        output1 = deviceObj.executeCmd("ifconfig %s inet6 add %s/%s %s "%(interfaceName, ipAddress, prefixlen, status), mode=mode)
        output2 = deviceObj.executeCmd("ifconfig %s"%interfaceName, mode=mode)
    else:
        log.fail('Failure while configuring mode')
        raise RuntimeError("Failure while configuring mode")
    ipformat = ipAddress
    log.cprint(output2)
    match = re.search(ipformat, output2)
    if match:
        log.success('configuring ipv6 on management interface')
    else:
        log.fail('Failure while configuring ipv6 on management interface')
        raise RuntimeError("Failure while configuring ipv6 on management interface")

def get_ip_address_list(device, interfaceName, mode, ipv6=False):
    log.debug('Entering get_ip_address_list with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    # for some machines, ethx is not up by default.
    set_interface_link(interfaceName, 'up', mode)

    if ipv6:
        ipformat = r'inet6 (addr:\s?)?(.+)(\/|prefixlen)'
    else:
        ipformat = r'inet (addr:)?(\d+\.\d+\.\d+\.\d+)'
    ipList = []
    ip = ''
    output = deviceObj.executeCmd("ifconfig %s"%interfaceName, mode=mode, timeout=30)
    for line in output.splitlines():
        line = line.strip()
        match = re.search(ipformat, line)
        if match:
            ip = match.group(2).strip()
            ipList.append(ip)
            log.success('Successfully get ip address: %s'%(ip))
    return ipList

def get_ip_address(device, interfaceName, mode=None, ipv6=False):
    log.debug('Entering get_ip_address with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    # for some machines, ethx is not up by default.
    set_interface_link(interfaceName, 'up', mode)

    if ipv6:
        if interfaceName == 'eth0':
            ipformat = r'inet6 (addr:\s?)?(.+)(\/|prefixlen).*(Scope:Global|scopeid.*Global)'
        else:
            ipformat = r'inet6 (addr:\s?)?(.+)(\/|prefixlen).*(Scope:Link|scopeid.*link)'
    else:
        ipformat = r'inet (addr:)?(\d+\.\d+\.\d+\.\d+)'
    ip = ''
    output = deviceObj.executeCmd("ifconfig %s"%interfaceName, mode=mode, timeout=30)
    for line in output.splitlines():
        line = line.strip()
        match = re.search(ipformat, line)
        if match:
            if ipv6:
                if '::' in line:
                    ip = match.group(2).strip()
                    log.success('Successfully get dhcp ipv6 address: %s' % (ip))
                    break
            else:
                ip = match.group(2).strip()
                log.success('Successfully get ip address: %s'%(ip))
                break
    return ip

def check_ip_address(device, interfaceName, mode=None, ipv6=False):
    log.debug('Entering check_ip_address with args : %s' %(str(locals())))
    ip = get_ip_address(device, interfaceName, mode, ipv6)
    if ip != '':
        return ip

    if ipv6:
        option = '6'
    else:
        option = '4'
    cmd = 'dhclient -%s %s'%(option, interfaceName)
    if ipv6:
        cmd += ' --address-prefix-len 64'
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.executeCmd(cmd, mode=mode, timeout=200)
    time.sleep(8)
    ip = get_ip_address(device, interfaceName, mode, ipv6)
    if ip != '':
        return ip

    for i in range(0, 6):
        ip = get_random_ip('PC', ipv6)
        try:
            if ipv6:
                exec_local_ping6(None, ip, 5, 'None')
            else:
                exec_local_ping(ip, 5, 'None')
        except RuntimeError:  ## ping failed, so this IP should not be used, can use it
            break

    if ip != '':
        if ipv6:
            config_management_interface_ipv6(device, interfaceName, ip, 64, 'up', mode)
        else:
            config_management_interface(device, interfaceName, ip, '255.255.255.0', 'up', mode)
    time.sleep(8)
    return get_ip_address(device, interfaceName, mode, ipv6)

def check_ip_address_list(device, interfaceName, mode, preferred_network='None', ipv6=False, staticMode=False):
    log.debug('Entering check_ip_address_list with args : %s' %(str(locals())))
    ipList = get_ip_address_list(device, interfaceName, mode, ipv6)
    if ipList:
        if preferred_network != 'None':
            for ipAddress in ipList:
                match = re.search(preferred_network, ipAddress)
                if match:
                    log.info('using dhcp ip address: %s'%(ipAddress))
                    return ipAddress
        else:
            for ipAddress in ipList:
                ip = ipAddress
            return ip

    if not staticMode:
        ### run dhclient to get ip address
        if ipv6:
            option = '6'
        else:
            option = '4'
        cmd = 'dhclient -%s %s'%(option, interfaceName)
        if ipv6:
            cmd += ' --address-prefix-len 64'
        deviceObj = Device.getDeviceObject(device)
        output = deviceObj.executeCmd(cmd, mode=mode, timeout=300)
        time.sleep(8)
        ipList = get_ip_address_list(device, interfaceName, mode, ipv6)
        if ipList:
            if preferred_network != 'None':
                for ipAddress in ipList:
                    match = re.search(preferred_network, ipAddress)
                    if match:
                        log.info('using dhcp ip address: %s'%(ipAddress))
                        return ipAddress
            else:
                for ipAddress in ipList:
                    ip = ipAddress
                return ip

    ### if still cannot get ip address, set static random ip
    for i in range(0, 6):
        ip = get_random_ip('PC', ipv6, staticMode)
        try:
            if ipv6:
                exec_local_ping6(None, ip, 5, 'None')
            else:
                exec_local_ping(ip, 5, 'None')
        except RuntimeError:  ## ping failed, so this IP should not be used, can use it
            break

    if ip != '':
        if ipv6:
            config_management_interface_ipv6(device, interfaceName, ip, 64, 'up', mode)
        else:
            config_management_interface(device, interfaceName, ip, '255.255.255.0', 'up', mode)
    time.sleep(8)
    ipList = get_ip_address_list(device, interfaceName, mode, ipv6)
    if ipList:
        if preferred_network != 'None':
            for ipAddress in ipList:
                match = re.search(preferred_network, ipAddress)
                if match:
                    log.info('using ip address: %s'%(ipAddress))
                    return ipAddress
        else:
            for ipAddress in ipList:
                ip = ipAddress
            return ip

def get_readable_strings(patterns):
    replace_dict = {".*?":" ", r'\t':"", "[":"", "]": "", "^":"", "$":"", "\\":"", "*":"", r'\d':"", "+":""}
    if isinstance(patterns, list) or isinstance(patterns, set):
        printout_str = ", ".join(patterns)
    else:
        printout_str = patterns

    for key, value in replace_dict.items():
        printout_str = printout_str.replace(key, value)
    return printout_str


def escapeString(string):
    special_characters = {
        '.' : '\.',
        '*' : '\*',
        '(' : '\(',
        ')' : '\)',
        '?' : '\?',
        '|' : '\|',
        '+' : '\+',
        '$' : '\$',
        '[' : '\[',
        ']' : '\]'
    }
    for key, value in special_characters.items():
        string = string.replace(key, value)

    return string


#########################################################################################################
### parse pattern conposed with key and value in pattern dict,  get the string in value capture group ###
### and return a dict with same keys of pattern dict and captured strings as value.                   ###
### Log example: "Device Model:     HBS3A1912A4M4B1", pattern dict: {"Device Model": "(.*?)$"}        ###
### return dict {"Device Model": "HBS3A1912A4M4B1" }                                                  ###
#########################################################################################################
def parseDict(output=None, pattern_dict={}, sep_field=":", use_value_pattern=False, line_mode=True):
    log.debug("Entering parseDict.")

    result_dict = copy.deepcopy(pattern_dict)
    for key in result_dict.keys():
        result_dict[key] = ""
    match_flag = 0
    for key, value in pattern_dict.items():
        pattern = "{}\s*{}\s*{}".format(escapeString(key),escapeString(sep_field), value)
        if use_value_pattern:
            pattern = value
        if line_mode:
            match = re.search(pattern, output, re.M)
        else:
            match = re.search(pattern, output, re.S)
        if match:
            result_dict[key] = match.group(1).strip()
            match_flag = 1
        else:
            log.info("Not find value for item: {}".format(key))
    if  match_flag:
        return result_dict
    else:
        log.info("No any value found in parsing.")
        return {}


#######################################################
### Function to execute ping, mode=[openbmc|centos] ###
#######################################################
def exec_ping(device, ipAddress, count, mode=None, expected='None'):
    log.debug("Entering exec_ping with args : %s" %(str(locals())))
    log.debug("Execute the ping from Device:%s to ip:%s"%(device, ipAddress))
    deviceObj = Device.getDeviceObject(device)
    cmd = "ping %s -c %s"%(ipAddress, str(count))
    success_msg = str(count) + ' packets transmitted, ' + str(count) + ' (packets )?received, 0% packet loss'
    loss_msg = str(count) + ' packets transmitted, ' + '0 packets received, 100% packet loss'

    output = deviceObj.executeCmd(cmd, mode=mode, timeout=30)
    log.info('output: %s'%(output))
    if expected == 'None':
        match = re.search(success_msg, output)
        if match:
            log.success("Found: %s"%(match.group(0)))
            log.success("ping to %s"%ipAddress)
        else:
            log.fail("ping to %s"%ipAddress)
            raise RuntimeError("Ping to destination IP address failed")
    elif expected == 'loss':
        match = re.search(loss_msg, output)
        if match:
            log.success("Found: %s"%(match.group(0)))
            log.success("ping to " + ipAddress + " get 100% packet loss")
        else:
            log.fail("ping to " + ipAddress + " did not get 100% packet loss")
            raise RuntimeError("Ping to destination IP address with loss expected failed")

############################################################
### Function to execute ping ipv6, mode=[openbmc|centos] ###
############################################################
def exec_ping6(device, interface, ipAddress, count, mode):
    ### ping6 -I eth0 fe80::2204:fff:fef0:2ba1 -c 5
    log.debug("Entering exec_ping6 with args : %s" %(str(locals())))
    log.debug("Execute the ping6 from Device:%s to ipv6:%s"%(device, ipAddress))
    deviceObj =  Device.getDeviceObject(device)
    if deviceObj.deviceType == 'server':
        cmd = "ping6 %s -c %s" % (ipAddress, str(count))
    else:
        cmd = "ping6 -I %s %s -c %s"%(interface, ipAddress, str(count))
    success_msg = str(count) + ' packets transmitted, ' + str(count) + ' (packets )?received, 0% packet loss'

    output = deviceObj.executeCmd(cmd, mode=mode, timeout=30)
    log.info('output: %s'%(output))
    match=re.search(success_msg, output)
    if match:
        log.success("Found: %s"%(match.group(0)))
        log.success("ping6 to %s"%ipAddress)
    else :
        log.fail("ping6 to %s"%ipAddress)
        raise RuntimeError("Ping6 to destination IP address failed")

###########################################################################################
### Usage: execute command and check output or check output only, match pattern is dict ###
###########################################################################################
def execute_check_dict(device, cmd, mode=None, patterns_dict={}, path=None, timeout=900, line_mode=True,
                       is_negative_test=False, check_output=None, remark=""):
    if not check_output:
        log.debug('Entering procedure execute_check_dict with args : %s' %(str(locals())))
    deviceObj =  Device.getDeviceObject(device)
    passCount = 0
    patternNum = len(patterns_dict)
    log.debug('path:**{}**, cmd:**{}** '.format(path, cmd))
    if path:
        deviceObj.sendMsg('cd ' + path)
    if check_output:
        output = check_output
    else:
        output = deviceObj.executeCmd(cmd, mode=mode, timeout=timeout)

    pass_p = []
    pattern_all = []
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
    cmd = cmd.strip("\n")
    if remark:
        description = remark + ":" + cmd
    else:
        description = "commands:{}".format(cmd)
    if passCount == patternNum:
        log.info('%s is PASSED\n' %description)
    else:
        cmd_str = cmd
        if cmd:
            cmd_str = "while execute '{}' ".format(cmd)
        log.fail('Exiting execute_check_cmd with result FAIL. {}'.format(remark))
        raise Exception("Failure {}with  items: {}".format(cmd_str, mismatch_key_name))

    return output

###########################################################
###  Get one not occupied IP in the same subnet of PC   ###
###########################################################
def Get_Not_Occupied_IP():
    log.debug("Entering OnieLib class procedure: Get_Not_Occupied_IP")

    server_ip = get_device_info("PC").get("managementIP","")
    if not server_ip:
        raise Exception("Server ip is not found in config file")
    device_ip = ""
    for host_ip in range(2, 255):
        ip_array = server_ip.split(".")
        ip_array[3] = str(host_ip)
        ip = ".".join(ip_array)
        try:
            exec_local_ping(ip, 3, None)
            continue
        except:
            device_ip = ip
            break

    return device_ip

#######################################
###  Get device info in Device.yml  ###
#######################################
def get_device_info(device_name):
    log.debug("Entering get_device_info with args : %s" %(str(locals())))

    return YamlParse.getDeviceInfo().get(device_name, {})

####################################################
###  Get software info dict from SwImages.yml    ###
####################################################
def get_swinfo_dict(item_name):
    log.debug("Entering get_swinfo_dict with args : %s" %(str(locals())))

    return SwImage.getSwImage(item_name).imageDict


#############################################################################################
# Function Name: get_dhcp_ip_address
# Date         : 10th July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def get_dhcp_ip_address(device, interfaceName, mode, ipv6=False):
    log.debug('Entering get_dhcp_ip_address with args : %s' %(str(locals())))
    log.info('get dhcp ip address')
    preferred_network = 'None'
    if ipv6:
        server_ip = get_ip_address_from_config('PC', ipv6)
        if re.search(':', server_ip):
            slist = server_ip.split(':')
            preferred_network = slist[0]
    return check_ip_address_list(device, interfaceName, mode, preferred_network, ipv6)

#######################################################################################################################
# Function Name: compare_input_dict_to_parsed
# Date         : 18th December 2020
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def compare_input_dict_to_parsed(parsed_dict, input_array, highlight_fail=True):
    log.debug('Entering procedure compare_input_dict_to_parsed with args : %s\n' %(str(locals())))
    fail_count = 0
    log.cprint("input_array: " + str(type(input_array)))
    if str(type(input_array)) == "<class 'str'>":
        input_array = YamlParse.stringToDict(input_array)

    for key, value in zip(dict(input_array).keys(), input_array.values()):
        log.debug("Searching for %s = %s in parsed output" % (key, value))
        dict_value = parsed_dict.get(key)
        log.info("printing value %s" % dict_value)
        if dict_value is None:
            if highlight_fail:
                log.fail('For key = %s, Value %s not found in parsed output\n' %(key, value))
            else:
                log.info('For key = %s, Value %s not found in parsed output\n' %(key, value))
            fail_count += 1
        elif value == dict_value:
            log.success('For key = %s, Values match %s, %s\n' %(key, value, dict_value))
            continue
        # elif dict_value == '0':
        #     log.error('Value 0 found for Key = %s\n' %key)
        #     fail_count += 1
        elif value == 'ANY':
            log.success('Valid value is present for the key = %s\n' %key)
            continue
        else:
            if highlight_fail:
                log.fail('For key = %s, Values do not match: Found \'%s\' Expected \'%s\'\n'
                        %(key, dict_value, value))
            else:
                log.info('For key = %s, Values do not match: Found \'%s\' Expected \'%s\'\n'
                        %(key, dict_value, value))
            fail_count += 1
    return fail_count

#######################################################################################################################
# Function Name: set_interface_link
# Date         : 22nd December 2020
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def set_interface_link(interface_name, status, mode):
    ### ifconfig eth0 [down|up]
    log.debug("Entering set_interface_link with args : %s" %(str(locals())))
    cmd = 'ifconfig %s %s'%(interface_name, status)
    execute_command(cmd, mode=mode)
    time.sleep(5)

#######################################################################################################################
# Function Name: create_dir
# Date         : 25th December 2020
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def create_dir(path, mode):
    log.debug('Entering procedure create_dir with args : %s\n' %(str(locals())))
    if check_file_exist(path, mode):
        log.info("%s exists"%(path))
        return 0
    else:
        mkdir_cmd = 'mkdir -p ' + path
        execute_command(mkdir_cmd, mode=mode)
        return 1

#######################################################################################################################
# Function Name: check_file_exist
# Date         : 25th December 2020
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def check_file_exist(path, mode=None, test_flag=False):
    log.debug('Entering procedure check_file_exist with args : %s\n' %(str(locals())))

    # check whether file exists
    p1 = 'No such file or directory'
    cmd = ('ls %s' %path)
    output = execute_command(cmd, mode=mode, timeout=300)
    errCount = 0
    if len(output) == 0:
        errCount = 1
    else:
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1,line)
            if match:
                errCount+=1
                break
    if errCount:
        # file not exist
        if test_flag:
            log.fail("%s does not exist"%(path))
            raise RuntimeError("check_file_exist")
        else:
            log.info("%s does not exist"%(path))
            return False
    else:
        # file exists
        log.success("%s exists"%(path))
        return True

#######################################################################################################################
# Function Name: mount_data
# Date         : 4th January 2021
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def mount_data(dev, path, mode):
    ### mkdir /mnt/data1
    ### mount /dev/mmcblk0 /mnt/data1
    log.debug('Entering procedure mount_data with args : %s\n' %(str(locals())))
    ret = create_dir(path, mode)
    if ret:
        mount_cmd = 'mount ' + dev + ' ' + path
        execute(mount_cmd, mode)
    else:
        log.info("%s exists, no need to mount data"%(path))

#######################################################################################################################
# Function Name: reboot
# Date         : 4th January 2021
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def reboot(mode, log_File='None'):
    log.debug('Entering procedure reboot : %s\n '%(str(locals())))
    prompt(mode)
    transmit("reboot")
    booting_msg = r'Restarting|U-Boot'
    #output = receive(booting_msg, timeout=600)
    output = read_until_regexp(booting_msg, timeout=600)
    if log_File != 'None':
        send_output_to_log_file(output, log_File)
    time.sleep(200)
    prompt(mode, timeout=800, idleTimeout=800, logFile=log_File)
    time.sleep(35)

    deviceObj = DeviceMgr.getDevice()
    sendline('\n')
    # this command caused read eeprom file failed
    #if mode == 'openbmc' and ('minipack2' in deviceObj.name or 'cloudripper' in deviceObj.name):
        ### need to run this command to link the driver when BMC boot up
     #   execute('ln -s ld-2.29.so /lib/ld-linux.so.3', mode=mode)

#######################################################################################################################
# Function Name: switch_to_centos
# Date         : 4th January 2021
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def switch_to_centos(logFilename='None'):
    log.debug('Entering procedure switch_to_centos : %s\n '%(str(locals())))
    deviceObj = DeviceMgr.getDevice()
    deviceObj.switchToCpu()
    prompt(Const.BOOT_MODE_CENTOS, timeout=Const.BOOTING_TIME, idleTimeout=Const.BOOTING_TIME, logFile=logFilename)

#######################################################################################################################
# Function Name: switch_to_openbmc
# Date         : 4th January 2021
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def switch_to_openbmc(logFilename='None'):
    log.debug('Entering procedure switch_to_openbmc : %s\n '%(str(locals())))
    deviceObj = DeviceMgr.getDevice()
    deviceObj.trySwitchToBmc()   # just switch to bmc side, let getPrompt() to enter correct status.
    prompt(Const.BOOT_MODE_OPENBMC, timeout=Const.BOOTING_TIME, idleTimeout=Const.BOOTING_TIME, logFile=logFilename)

#######################################################################################################################
# Function Name: change_dir
# Date         : 7th January 2021
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def change_dir(path="", mode=None):
    ## cd [path]
    log.debug('Entering procedure change_dir with args : %s\n' %(str(locals())))
    cmd = "cd " + path
    output = execute_command(cmd, mode=mode)
    p1 = 'No such file or directory'
    match = re.search(p1, output, re.IGNORECASE)
    if match:
        log.fail("%s"%(p1))
        raise RuntimeError("Fail to change directory")
    else:
        log.success('Successfully change directory %s'%(path))

#######################################################################################################################
# Function Name: get_eeprom_cfg_dict
# Date         : 8th January 2021
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def get_eeprom_cfg_dict(eeprom_name):
    log.debug('Entering procedure get_eeprom_cfg_dict : %s\n '%(str(locals())))
    eeprom_config_dict = YamlParse.getEepromConfig()
    if eeprom_name in eeprom_config_dict:
        return eeprom_config_dict[eeprom_name]
    else:
        log.fail('"%s" cannot be found in EepromConfig.yaml'%(eeprom_name))
        raise RuntimeError("Fail to get_eeprom_cfg_dict")


#######################################################################################################################
# Function Name: fb_generate_eeprom_cfg
# Date         : 11th January 2021
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def fb_generate_eeprom_cfg(eeprom_name):
    log.debug('Entering procedure fb_generate_eeprom_cfg : %s\n '%(str(locals())))
    eeprom_config_dict = get_eeprom_cfg_dict(eeprom_name)

    if 'HOTSWAP' in eeprom_name.upper():
        #### example of hotswap_eeprom.cfg format for Facebook device:
        ### 0x20 : 0x3f
        ### 0x31 : 0x56
        last_key = list(eeprom_config_dict.keys())[-1]
        eeprom_str = ''
        for key, value in eeprom_config_dict.items():
            if key == last_key:
                eeprom_str += key + ' : ' + value
            else:
                eeprom_str += key + ' : ' + value + '\n'
    else:
        #### example of eeprom.cfg format for Facebook device:
        ### [fb]
        ### magic_word                      = 0xFBFB
        ### format_version                  = 0x3
        eeprom_str = '[fb]'
        for key, value in eeprom_config_dict.items():
            eeprom_str += '\n' + pad_with_tabs(key, 32) + '= ' + value
    log.debug('eeprom_str: ' + eeprom_str)
    return eeprom_str

#######################################################################################################################
# Function Name: pad_with_tabs
# Date         : 11th January 2021
# Author       : Prapatsorn W. <pwsutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
#######################################################################################################################
def pad_with_tabs(s, maxlen):
    log.debug('Entering procedure pad_with_tabs : %s\n '%(str(locals())))
    n_pad = int((maxlen-len(s)-1)/Const.TABWIDTH+1)
    return s + "\\t"*n_pad

# Pass-through APIs to proceed on top-level robot script for more convenient
def prompt(mode=None, timeout=60, idleTimeout=60, logFile='None'):
    log.debug("Entering procedure prompt.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.getPrompt(mode, timeout, idleTimeout, logFile)

def transmit(cmd, CR=True):
    log.debug("Entering procedure transmit.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.transmit(cmd, CR)

def execute(cmd, mode=None, timeout=60):
    log.debug("Entering procedure execute.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.execute(cmd, mode, timeout)

def sendline(cmd, CR=True):
    log.debug("Entering procedure sendline.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.sendline(cmd, CR)

def receive(rcv_str, timeout=60):
    log.debug("Entering procedure receive.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.receive(rcv_str, timeout)


def send_msg(msg):
    log.debug("Entering procedure send_msg.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.sendMsg(msg)


# frequently used send/read command/message related functions begin
def execute_command(cmd, mode=None, timeout=60):
    log.debug("Entering procedure executeCmd.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.executeCmd(cmd, mode, timeout)


def send_command(cmd, promptStr=None, timeout=10):
    log.debug("Entering procedure send_command.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.sendCmd(cmd, promptStr, timeout)


def send_cmd_regexp(cmd, promptRegexp, timeout):
    log.debug("Entering procedure send_cmd_regexp.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.sendCmdRegexp(cmd, promptRegexp, timeout)


@logThis
def run_cmd(cmd, prompt, mode=None, timeout=60):
    """ this api will check the exit code after execute it;
     this api can be used in the mode do not support time operation
     :param prompt: the prompt after executing the cmd
    """
    deviceObj = DeviceMgr.getDevice()
    return deviceObj.runCmd(cmd, prompt, mode, timeout)


@logThis
def exec_cmd(cmd, mode=None, timeout=60):
    """ this api will check the exit code after execute it, can be used in the mode support time operation """
    deviceObj = DeviceMgr.getDevice()
    return deviceObj.execCmd(cmd, mode, timeout)


def read_until_regexp(patterns, timeout):
    log.debug("Entering procedure read_until_regexp.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.read_until_regexp(patterns, timeout)
# frequently used send/read command/message related functions end


def power_cycle_to_mode(mode):
    log.debug("Entering procedure power_cycle_to_mode.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.powerCycleToMode(mode)

# End of pass-through APIs

def send_output_to_log_file(output, logFile=Const.UART_LOG):
    log.debug("Entering procedure receive.\n")
    deviceObj = DeviceMgr.getDevice()

    return deviceObj.send_output_to_log_file(output, logFile)


@logThis
def prepare_images(image_name, mode=None, host_base_dir = ''):
    image = SwImage.getSwImage(image_name)
    image.hostBaseDir = host_base_dir
    create_dir(image.localImageDir, mode)
    get_dhcp_ip_address(Const.DUT, 'eth0', mode)
    download_images(Const.DUT, image_name)


@logThis
def check_cmd_no_output(cmd, output=None):
    deviceObj = DeviceMgr.getDevice()
    error_list = ['No such file or directory', 'command not found', 'Permission denied']
    if not output:
        output = deviceObj.executeCmd(cmd)
    count = 0
    for line in output.splitlines():
        for err in error_list:
            if re.search(err, line):
                count += 1
            else:
                continue
    if count:
        log.fail("verify output is failed")
        deviceObj.raiseException("Failure while checking output")
    else:
        return True

@logThis
def get_mac_address(device, interface, keyword='HWaddr'):
    deviceObj = DeviceMgr.getDevice(device)
    output = deviceObj.executeCmd('ifconfig ' + interface)
    pattern = keyword + ' (\S+)'
    match = re.search(pattern, output)
    if match:
        mac_addr = match.group(1).strip()
        log.cprint(mac_addr)
        return mac_addr
    else:
        raise RuntimeError('Can not get mac address')


@logThis
def check_exit_code(prompt):
    """ this api can be used in the mode do not support time operation
     :param prompt: the prompt after executing the cmd
    """
    deviceObj = DeviceMgr.getDevice()
    out = deviceObj.executeCommand('echo $?', prompt)
    for line in out.splitlines():
        if re.search(r'^0$', line):
            log.success('check exit code successfully.')
            return
    raise RuntimeError('check exit code failed!')

@logThis
def parse_fw_version(output):
    outDict = parser()
    # output = re.sub(START_GETTY_MSG, '', output)
    # p1 = r'(.*): (v?(.*))'
    p1 = r'(.+): (.+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            key = match.group(1)
            outDict[key] = match.group(2)
    log.debug(str(outDict))
    return outDict

@logThis
def get_key_list(tc_number):
    return YamlParse.getKeyListConfig().get(tc_number, {})

@logThis
def filter_passpattern(tc_number, fail_dict={}, fail_list=[]):
    white_list = get_key_list(tc_number).get('white_list')
    length = len(fail_dict)
    pattern_name = []
    pattern_all = []
    filter_key = []
    if fail_dict:
        for p_key, p_value in fail_dict.items():
            pattern_all.append(p_value)
            pattern_name.append(p_key)
        for i in range(length):
            for pattern in white_list:
                if re.search(pattern_all[i], pattern):
                #if pattern_all[i] in pattern:
                    filter_key.append(pattern_name[i])
                    break
        for i in filter_key:
            del fail_dict[i]
        return fail_dict
    if fail_list:
        for i in range(len(fail_list)):
            for pattern in white_list:
                if re.search(fail_list[i], pattern):
                    filter_key.append(fail_list[i])
        return list(set(fail_list) - set(filter_key))


def download_image_tftp(image_name, upgrade=True):
    image = SwImage.getSwImage(image_name)
    file_name = image.newImage if upgrade else image.oldImage
    files = ["{}/{}".format(image.hostImageDir,file_name)]
    tftp_get_files(Const.DUT, file_list=files, dst_path=image.localImageDir, timeout=400)

#### Procedure to change the directory in the CAP server
@logThis
def change_local_dir(path="", mode=None):
    log.debug("Entering procedure to change the directory in the CPA server")
    os.chdir(path)
    os.system('pwd')
    log.info("Directory changed")
