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
from inspect import getframeinfo, stack
import os.path
import time
import yaml
import Logger as log
#from GoogleCommonLib import powercycle_pdu1
from EDK2CommonLib import powercycle_pdu1
import CommonLib
import random
import Const
import bios_menu_lib
import openbmc_lib
import Const
import YamlParse
import Logger as log
import pexpect
import getpass
import os
import traceback
import parser_openbmc_lib
import json
import CRobot
from BIOS_variable import *
from BMC_variable import *
from datetime import datetime, timedelta
from dataStructure import nestedDict, parser
from errorsModule import noSuchClass, testFailed
import CommonKeywords
from SwImage import SwImage
from Server import Server
from pexpect import pxssh
from functools import partial
import sys
import getpass
import WhiteboxLibAdapter
import whitebox_lib
from crobot.Decorator import logThis
import pexpect
import multiprocessing
from TelnetDevice import TelnetDevice
import pexpect
from crobot.PowerCycler import PowerCycler
import EDK2CommonLib
from  EDK2CommonLib import powercycle_device
from  EDK2CommonLib import exit_the_shell
try:
    import parser_openbmc_lib as parserOpenbmc
    import DeviceMgr
    from Device import Device

except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()
workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
#sys.path.append(os.path.join(workDir, 'platform/edk2'))
sys.path.append(os.path.join(workDir, 'platform', 'edk2'))
sys.path.append(os.path.join(workDir, 'platform', 'edk2','diag'))

from  GoogleDiagLib import rebootToSonic

run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
time.sleep(10)

import Logger as log

@logThis
def powercycle_to_bios(c,d,s):
    deviceObj = Device.getDeviceObject(c)
    deviceObj.powerCycleDevice()
    output1='Corporation'
    j1=deviceObj.read_until_regexp(output1,timeout=50)
    deviceObj.sendCmd('\r')

    out=deviceObj.read_until_regexp('Shell>',timeout=60)
    log.success('Entered the UEFI shell')
    print('The output1 is ',j1)
    deviceObj.sendCmd('exit')
    time.sleep(5)
    deviceObj.sendCmd(s)
    time.sleep(5)
    if not bios_copy in j1:
        log.success('No EVALUATION COPY STRING PRESENT')
    else:
        raise RuntimeError('EVALUATION COPY STRING PRESENT')
    #validate_str(bios_version,j1,'BIOS version as per manual')
    return j1
    enter_bios_with_shell(c,s) 

@logThis
def validate_str(a,b,msg):
    if re.search(a.lower(),b,re.IGNORECASE) :
        msg=msg+ ' Passed'
        log.success(msg)
    else:
        msg=msg+' Failed'
        log.fail(msg)
    c1='PASS : The string  '+ a + ' is being match against output \n' + b
    print(c1)
def execute(device, cmd, mode=None, timeout=60):
    log.debug('Entering Device execute with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if mode != None:
        deviceObj.getPrompt(mode, timeout)
    cmd = 'time ' + cmd
    return deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)


def downloadBIOSImages(device,module="Athena_BIOS_Versions_A"):
    log.debug("Entering download_Athena_BIOS_Fw_Images with args : %s" %(str(locals())))
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
           raise RuntimeError("pattern mismatch")

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

def update_bios_version(device,toolname,package_file):
    log.debug("Entering procedure update_bios_version")
    deviceObj = Device.getDeviceObject(device)
    cmd="./ipmi_drive.sh"
    execute(device, cmd)
    cmd="rmmod ipmi_ssif"
    execute(device, cmd)
    cmd="rmmod acpi_ipmi"
    execute(device, cmd)
    err_count = 0
    timeout = 500
    cmd="{} {}".format(toolname,package_file)
    log.info(cmd)
    msg="Enter your Option :"
    deviceObj.sendCmd(cmd,msg,500)
    cmd1="y"
    pr="#"
    output=deviceObj.sendCmd(cmd1,pr,1200)
    log.info(output)
    pass_message_1="Uploading Image : 100%... done"
    pass_message_2="Flashing  Firmware Image : 100%... done"
    pass_message_3="Verifying Firmware Image : 100%... done"
    pass_message_4="Beginning to Deactive flashMode...end"
    pass_message_5="Resetting the firmware........."
    match1=re.search(pass_message_1,output)
    match2=re.search(pass_message_2,output)
    match3=re.search(pass_message_3,output)
    match4=re.search(pass_message_4,output)
    match5=re.search(pass_message_5,output)
    if match1 and match2 and match3 and match4 and match5:
        log.success("BIOS upgraded successfully")
    else:
        raise RuntimeError("BIOS Upgrade Failed")

def get_image_version_for_upgrade_downgrade(module,version,key):
    log.debug("Entering procedure to  get_image_version_for_upgrade_downgrade")
    imageObj = SwImage.getSwImage(module)
    if version == 'newImage':
      image_name= imageObj.newImage[key]
      log.info(image_name)
    else:
      image_name= imageObj.oldImage[key]
      log.info(image_name)
    return image_name

def GetRevFromImage(image_name):
    log.debug("Entering GetRevFromImage with args : %s" %(str(locals())))
    p1 = ".*([0-9])\.([0-9])\.([0-9][0-9])\.([0-9][0-9])"
    match = re.search(p1,image_name)
    if match:
        return match.group(1) + '.' + match.group(2) + '.' + match.group(3) + '.' + match.group(4)

def verify_me_version_in_os(version,pattern):
    output=version.splitlines()
    ver_pattern="\s(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+).*"
    for line in output:
        match=re.search(ver_pattern,line)
        if match :
           break
    log.info(line)
    version=match.group(3)+' '+ match.group(4)+' '+match.group(13)+' '+match.group(14)
    log.info(version)
    if version == pattern :
       log.info("ME_version check in OS is successful")
    else:
       log.info("ME_version check in OS is unsuccessful")
       raise RuntimeError("ME_version check in OS is unsuccessful")

def compare_pci_op_list(output1,output2):
    log.debug("Entering procedure compare_pci_op_list")
    j=0
    pattern1="Link Capabilities\( C\):.*(\S+).*"
    pattern2="Maximum Link Speed\(3:0\):.*(\S+) GT\/s.*"
    pattern3="Maximum Link Width\(9:4\):.*(\S+).*"
    pattern4="Link Status\(12\):.*(\S+).*"
    pattern5="Current Link Speed\(3:0\):.*(\S+) GT\/s.*"
    pattern6="Negotiated Link Width\(9:4\):.*(\S+)"
    for i in output1:
       i_split=i.splitlines()
       for line in i_split:
            match1=re.search(pattern1,line)
            match2=re.search(pattern2,line)
            match3=re.search(pattern3,line)
            match4=re.search(pattern4,line)
            match5=re.search(pattern5,line)
            match6=re.search(pattern6,line)
            if match1:
               log.info(line)
               Link_Capabilities=match1.group(1)
               log.info(Link_Capabilities)
            if match2:
               log.info(line)
               Maximum_Link_Speed=match2.group(1)
               log.info(Maximum_Link_Speed)
            if match3:
               log.info(line)
               Maximum_Link_Width=match3.group(1)
               log.info(Maximum_Link_Width)
            if match4:
               log.info(line)
               Link_Status=match4.group(1)
               log.info(Link_Status)
            if match5:
               log.info(line)
               Current_Link_Speed=match5.group(1)
               log.info(Current_Link_Speed)
            if match6:
               log.info(line)
               Negotiated_Link_Width=match6.group(1)
               log.info(Negotiated_Link_Width)
       pattern11="Link Capabilities\( C\):.*{}.*".format(Link_Capabilities)
       pattern12="Maximum Link Speed\(3:0\):.*{} GT\/s.*".format(Maximum_Link_Speed)
       pattern13="Maximum Link Width\(9:4\):.*{}.*".format(Maximum_Link_Width)
       pattern14="Link Status\(12\):.*{}.*".format(Link_Status)
       pattern15="Current Link Speed\(3:0\):.*{} GT\/s.*".format(Current_Link_Speed)
       pattern16="Negotiated Link Width\(9:4\):.*{}.*".format(Negotiated_Link_Width)
       match11=re.search(pattern11,output2[j])
       match12=re.search(pattern12,output2[j])
       match13=re.search(pattern13,output2[j])
       match14=re.search(pattern14,output2[j])
       match15=re.search(pattern15,output2[j])
       match16=re.search(pattern16,output2[j])
       if match11 and match12 and match13 and match14 and match15 and match16:
           log.info("All values in pci devices match in both executions")
       else:
           log.info("values in pci devices does not match in both executions")
           raise RuntimeError("values in pci devices does not match in both executions")
       j=j+1

def check_pattern_in_output(output,pattern,message):
    log.debug("Entering procedure to check pattern in an output")
    output1=output.splitlines()
    pattern1="dmesg | grep -i"
    for line in output1:
        if not re.search(pattern1,line):
            if re.search(pattern,line):
                log.info("{} Failed".format(message))
                raise RuntimeError("{} Failed".format(message))
    log.success("{} is successfull".format(message))

def enter_into_bios_setup(device,a):
    log.debug('Entering procedure verify_bios_default_password with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    line1 = 'Enter Password'

    deviceObj.getPrompt("DIAGOS")
    deviceObj.sendCmd("sudo -s")
    deviceObj.sendline("")
    deviceObj.sendCmd("reboot")

    # Enter BIOS Setup Menu
    out=deviceObj.read_until_regexp('Shell>',timeout=300)
    #print('The out is',out)
    deviceObj.sendline('exit')
    time.sleep(5)
    deviceObj.sendline(a)
    time.sleep(5)
    return out
    bios_menu_lib.send_key(device, "KEY_ESC")


##################################################################################################################################################
@logThis
def bios_basic(device,bios_pass):
    deviceObj = Device.getDeviceObject(device)
    str2='Continue'
    str1='stepping'
    k1=deviceObj.read_until_regexp(str2,timeout=10)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 5)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    output=deviceObj.read_until_regexp(str1,timeout=10)
    time.sleep(10)
    bios_menu_lib.send_key(device, "KEY_UP", 2)
    output1=deviceObj.read_until_regexp('Administrator',timeout=10)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ESC")
    validate_str(bios_version,k1,'BIOS version Test')
    if vendor in k1:
        log.success('PASS : Vendor Information Test')
    else:
        raise RuntimeError('FAIL: Vendor Information Test')

    validate_str(bios_version,output,'BIOS version Test on EDKII MAIN  Page')
    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    print('The basic info is : \n',output)
    print('The basic info is : \n',output1)
    return output


@logThis
def check_dmidecode_bios():
    device.sendCmd('sudo -s')
    output=device.executeCmd('dmidecode -t bios')
    s=re.search('Version.*([0-9]\.[0-9]+)',output).group()
    validate_str(bios_version,s,'BIOS Version Test')
    if vendor1 in output:
        log.success('PASS : Vendor Information Test')
    else:
        raise RuntimeError('FAIL: Vendor Information Test')


@logThis
def exit_bios_menu(device):
    deviceObj = Device.getDeviceObject(device)
    output=deviceObj.read_until_regexp('Continue',timeout=10)
    log.success('Bios Main Menu ')
    bios_menu_lib.send_key(device, "KEY_DOWN", 4)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    output1='directly boot'
    deviceObj.read_until_regexp(output1,timeout=50)
    deviceObj.sendCmd('\r')

@logThis
def exit_bios_shelll(device):
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC",5)
    output=deviceObj.read_until_regexp('Continue',timeout=10)
    log.success('Bios Main Menu ')
    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    deviceObj.sendCmd('\r')


################################################################################################################
@logThis
def read_ram_size(device):
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    output=deviceObj.read_until_regexp('Continue',timeout=10)
    s=re.search('[0-9]{5}.*MB RAM',output).group()
    validate_str(ram,s,'Bios ram Test: ')
    bios_menu_lib.send_key(device, "KEY_ESC")
    return output

############################# TC 9  #######################################
@logThis
def checkUnameOperations():
    ver_1= "4.19"
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    a1=device.executeCmd("uname -a")
    r1=device.executeCmd("uname -r")
    v1= device.executeCmd("uname -v")
    run1=run_command("cat /proc/version",timeout=5)
    r2=run_command("dmesg|grep Linux",timeout=5)
    r3=run_command("dmesg|grep -i BIOS",timeout=5)
    run_command('dmidecode -t bios')
    a = re.search(ver_1,a1) and re.search(ver_1,v1) and re.search(ver_1,r1)
    if a:
        log.success('Version is correct')
    else:
        raise RuntimeError('Incorrect version')
    print('a1: ',a1)
    print('ver_1 is : ',ver_1)
    #CommonKeywords.should_match_a_regexp(a1,ver_1)
    #CommonKeywords.should_match_a_regexp(r1,ver_1)
    #CommonKeywords.should_match_a_regexp(v1,ver_1)
    #CommonKeywords.should_match_a_regexp(run1,ver_1)
    #CommonKeywords.should_match_a_regexp(r2,ver_1)
    run_command('exit')

@logThis
def test_me():
   pass 

########################################TC 10 ###########################################################################
@logThis
def check_sonic_boot_via_bios(device):
    s=powercycle_to_bios(device,'no',bios_pass)
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device,"KEY_ESC")
    deviceObj.read_until_regexp('Highlight',timeout=10)
    bios_menu_lib.send_key(device, "KEY_DOWN", 2)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp('Highlight',timeout=10) 
    bios_menu_lib.send_key(device, "KEY_DOWN", 2)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp('Highlight',timeout=10)
    bios_menu_lib.send_key(device, "KEY_ENTER",2)

    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    deviceObj.read_until_regexp('Highlight',timeout=10)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    
    bios_menu_lib.send_key(device, "KEY_DOWN", 2)
    deviceObj.read_until_regexp('Highlight',timeout=10)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    output=deviceObj.read_until_regexp('sonic login',timeout=100)
    deviceObj.loginToDiagOS()
    deviceObj.sendCmd('sudo -s','root@sonic',timeout =20)
   

def checkI2cdetect():
    device.sendCmd('sudo -s')
    c1= device.executeCmd("i2cdetect -l")
    CommonKeywords.should_match_ordered_regexp_list(c1,i2cdetect_list)

@logThis
def checkCpuStats():
    time.sleep(60)    #->Post reboot wait for eth0 to come up
    cmd1= run_command('lscpu',prompt='root@sonic')
    cmd2=run_command('cat /proc/cpuinfo',prompt=None)
    cmd3=run_command('cat /proc/meminfo',prompt=None)
    cmd4=run_command('ifconfig',prompt=None)
    cmd5=run_command('sudo fdisk -l',prompt=None)
    CommonKeywords.should_match_ordered_regexp_list(cmd1,lscpi)
    log.success('Lscpu information matching with bios manual')
    CommonKeywords.should_match_ordered_regexp_list(cmd2,cpu_proc)
    log.success('Cpu info information matching with bios manual')
    CommonKeywords.should_match_ordered_regexp_list(cmd4,ifconfig_list)
    log.success('ifconfig information matching with bios manual')
    CommonKeywords.should_match_ordered_regexp_list(cmd5,fdisk_list)
    log.success('fdisk information matching with bios manual')


@logThis
def  check_network_stats():
    checkI2cdetect()
    checkCpuStats()
################################################################################################################################
@logThis
def check_cpu_microcode(device):
    deviceObj = Device.getDeviceObject(device)
    #output= bios_basic(device,bios_pass)
    #print('The out is :',output)
    #bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ESC")


    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device,"KEY_UP",4)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_ENTER")
    put1 = deviceObj.read_until_regexp('L3 Cache RAM',timeout=10)
    m1=re.search('Microcode Revision.*([0-9A-Za-z]+\s)',put1).group().split()[2]  
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ESC",2)

    output= bios_basic(device,bios_pass)
    print('bios_basic:\n',output)
    m2=re.search('Microcode Revision.*([0-9A-Za-z]+\s)',output).group().split()[2]
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ESC",2)
    j1=deviceObj.read_until_regexp('Continue',timeout=10)
    bios_menu_lib.send_key(device, "KEY_DOWN",3)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    print('j1 : ',j1)
    if m1 == m2:
        log.success('Microcode version is same as in bios manual')
    else:
        raise RuntimeError('Microcode revision different')
    exit_the_shell()
    r3=run_command("dmesg|grep -i microcode",timeout=5)
    m2=[x for x in m2]
    m2.insert(1,'x')
    m2=''.join(m2)
    validate_str(m2,r3,'Microcode test in dmesg: ')

@logThis
def enter_bios_with_shell(device,a):
    deviceObj = Device.getDeviceObject(device)
    out=deviceObj.read_until_regexp('Shell>',timeout=50) 
    deviceObj.sendline('exit')
    deviceObj.sendline(a)

@logThis
def check_eeprom_tlv():
    device.sendCmd('sudo -s','root@sonic')
    j=run_command('cd /usr/local/cls_diag/bin',timeout=10)
    time.sleep(2)
    device.sendCmd('\r')
    output=device.executeCmd('./cel-eeprom-test --read --dev all --type tlv',timeout=10)
    #CommonKeywords.should_match_ordered_regexp_list(output,eeprom_tlv)
    for x in eeprom_tlv:
        if not x in output:
            raise RuntimeError('Error in eeprom data')
            print('Line:',x)
            break
    log.success('Eeprom data check pass')

@logThis
def check_cpu_info(device):
    deviceObj = Device.getDeviceObject(device)
    out=deviceObj.read_until_regexp('Reset',timeout=10)
    print('The out put is ',out)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    exit_the_shell()
    if cpu_info in out and bios_version in out:
        log.success('Cpu info and bios version  matches bios manual')
    else:
        raise RuntimeError('Cpu info and bios version checkfailed')
    for x in bios_list:
        if x not in out:
            raise RuntimeError('Bios menu mismatch')
    log.success('Bios  menu as expected')
   
@logThis
def check_boot_manager_option(device):
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    j1=deviceObj.read_until_regexp('Media',timeout=15)
    print('Boot Manager Menu : Select option 2 ',j1)
    bios_menu_lib.send_key(device, "KEY_ENTER")


    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 2)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp('Shell>',timeout=15)
    log.success('Device successfully booted to shell with option 2 EFI shell')
    deviceObj.sendline("exit")

    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    j2=deviceObj.read_until_regexp('Media',timeout=15)
    print('Boot Manager Menu : Select option 1 is ',j2)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    out=deviceObj.read_until_regexp('Reset',timeout=10)
    print('The out put is ',out)
    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    exit_the_shell()

############################tc 08#######################################################

@logThis
def check_post_info(device):
    m1=''
    log.debug('Power cycing the device . . . . . . . ')
    #s=enter_into_bios_setup(device,bios_pass)
    s=powercycle_to_bios(device,'no',bios_pass)
    print('The value of s is ',s)
    validate_str(ifwi,s,'IFWI version Test')
    if copy_str in s:
        log.success('Copyright info is correct')
    else:
        raise RuntimeError('Copyright info is incorrect')




####################################tc 64 #########################################################
@logThis
def check_boot_manager(device):

    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    deviceObj.read_until_regexp('Continue',timeout=15)
    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    j1=deviceObj.read_until_regexp('key to select',timeout=15)
    for x in boot_list:
        if not re.search(x,j1):
            raise RuntimeError('Boot manager menu does not conform bios manual')
    log.success('The boot manager is in line with bios manual')

    print('Boot Manager Menu',j1)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    exit_the_shell()


#######################tc_27####################################################################################3333
@logThis
def check_pstate_enable(device,a):
    if a == 'KEY_DOWN':
        val = 'Enable'
    else:
        val ='Disable'
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN", 4)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    m1=deviceObj.read_until_regexp('Memory Configuration',timeout=15)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    #print('m1 is ',m1)
    bios_menu_lib.send_key(device, "KEY_DOWN", 7)
    m2=deviceObj.read_until_regexp('Tuning',timeout=15)
    #print('m2 is ',m2)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    m3=deviceObj.read_until_regexp('Limit',timeout=15)
    #print('m3 is ',m3)
    bios_menu_lib.send_key(device, "KEY_DOWN", 5)
    #bios_menu_lib.send_key(device, "KEY_ENTER")
    
    #j2=deviceObj.read_until_regexp('Turbo Mode',timeout=15)
    #print('The value of j2 is ',j2)

    log.debug('Now checking the p state')
    print('########################################################################################')
    print('                            OPERATION :  ',val)
    print('########################################################################################')
    bios_menu_lib.send_key(device, "KEY_ENTER")
    time.sleep(2)
    bios_menu_lib.send_key(device, a, 1)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    #bios_menu_lib.send_key(device, "KEY_F10")
    pass_msg='Energy efficient P-state.*'+val
    bios_menu_lib.send_key(device, "KEY_ESC")
    time.sleep(10)
    deviceObj.sendCmd("Y")
    time.sleep(5)
    deviceObj.sendCmd("\r")
    time.sleep(5)
    bios_menu_lib.send_key(device, "KEY_F10")
    m2=deviceObj.read_until_regexp(pass_msg,timeout=15)
    if m2:
        log.success('P-state status changed')
    #print('m2 is ',m2)
    bios_menu_lib.send_key(device, "KEY_ESC",5)
    log.success('The desired enable/disable operation was successfull')
    exit_bios_menu(device)
    exit_the_shell()



@logThis
def check_lscpu():
    cmd1= run_command('lscpu',prompt='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(cmd1,lscpi)
    log.success('Lscpu info is published irrespective of p-state enable/disable')



###########################################################################################################################################
##TC_28

@logThis
def check_hyper_thread(device,a):
    if a == 'KEY_DOWN':
        val = 'Enable'
    else:
        val ='Disable'
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ENTER") #BIOS menm

    bios_menu_lib.send_key(device, "KEY_DOWN", 4)
    bios_menu_lib.send_key(device, "KEY_ENTER")   #->Advanced
    deviceObj.read_until_regexp('PCH Configuration',timeout=15)

    bios_menu_lib.send_key(device, "KEY_ENTER") #-> Proccess configuration
    deviceObj.read_until_regexp('Highlight',timeout=15)
    

    #bios_menu_lib.send_key(device, "KEY_DOWN", 20)
    #deviceObj.read_until_regexp('Highlight',timeout=15)

    bios_menu_lib.send_key(device, "KEY_DOWN", 15)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, a, 1)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_ESC")
    time.sleep(10)
    deviceObj.sendCmd("Y")
    time.sleep(5)
    deviceObj.sendCmd("\r")
    time.sleep(5)
    bios_menu_lib.send_key(device, "KEY_F10")


    strmsg='Hyper-Threading.*'+val
    m1=deviceObj.read_until_regexp(strmsg,timeout=15)
    
    bios_menu_lib.send_key(device, "KEY_ESC",5)
    exit_bios_menu(device)
    exit_the_shell()



@logThis
def check_cpui_info(a):
    cpu_proc=[]
    cmd2= run_command('cat /proc/cpuinfo',prompt='root@sonic')
    a=int(a)
    for i in range(0,a):
        cpu_proc.append('processor.*:.*'+str(i))
        cpu_proc.append('vendor_id.*:.*GenuineIntel')
        cpu_proc.append('cpu family.*:.*6')
        cpu_proc.append('model.*:.*86')
        cpu_proc.append('model name.*:.*Intel\(R\) Xeon\(R\) CPU D-1649N @ 2.30GHz')
        cpu_proc.append('stepping.*:.*5')
        cpu_proc.append('microcode.*:.*0xe000014')
        cpu_proc.append('cpu cores.*:.*8')
        cpu_proc.append('fpu.*:.*yes')
        cpu_proc.append('fpu_exception.*:.*yes')
        cpu_proc.append('cpuid level.*:.*20')
        cpu_proc.append('wp.*:.*yes')

    CommonKeywords.should_match_ordered_regexp_list(cmd2,cpu_proc) 











############################################################################################################################################


@logThis
def remove_bios_pass(device,a):
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    deviceObj.sendCmd(a)
    time.sleep(10)
    deviceObj.sendCmd("\r")
    time.sleep(10)
    deviceObj.sendCmd("\r")
    time.sleep(10)
    deviceObj.sendCmd("\r")
    log.success('Password has been cleared completely')
    m1=deviceObj.read_until_regexp('Highlight',timeout=15)
    bios_menu_lib.send_key(device, "KEY_ESC",3)
    exit_bios_shelll(device)
    exit_the_shell()


@logThis
def remove_user_pass(device,a):
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    k1=deviceObj.read_until_regexp('Continue',timeout=10)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    deviceObj.sendCmd(a)
    deviceObj.sendCmd("\r")
    time.sleep(10)
    deviceObj.sendCmd("\r")
    time.sleep(10)
    deviceObj.sendCmd("\r")
    log.success('Password has been cleared completely')
    #m1=deviceObj.read_until_regexp('Highlight',timeout=15)
    bios_menu_lib.send_key(device, "KEY_ESC",3)
    exit_bios_shelll(device)
    exit_the_shell()




@logThis
def create_pass(device,user_type,key):
    key=int(key)
    str1='User Password'
    if user_type == 'admin':
        val = bios_pass
    else:
        val=user_pass

    deviceObj = Device.getDeviceObject(device)
    if user_type == 'admin':
        bios_menu_lib.send_key(device, "KEY_ESC")


    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    time.sleep(10)
    bios_menu_lib.send_key(device,'KEY_DOWN',key)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    m1=deviceObj.read_until_regexp(str1,timeout=15)
    deviceObj.sendCmd(val)
    time.sleep(2)
    deviceObj.sendCmd(val)
    time.sleep(10)

    m1=deviceObj.read_until_regexp(str1,timeout=15)

    m1=deviceObj.read_until_regexp('Highlight',timeout=15)
    log.success('Password has been set successful')
    exit_bios_shelll(device)
    exit_the_shell()


@logThis
def change_bios_password(device,user_type,key):
    deviceObj = Device.getDeviceObject(device)
    key=int(key)
    if user_type == 'admin':
        old=bios_pass
        val = new_bios_pass
    else:
        old=user_pass
        val=new_user_pass
    bios_menu_lib.send_key(device, "KEY_ESC") 
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device,'KEY_DOWN',key)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    
    deviceObj.sendCmd(old)
    time.sleep(2)
    deviceObj.sendCmd(val)
    time.sleep(2)
    deviceObj.sendCmd(val)
    time.sleep(10)
    log.success('Password has been changed successfully')
    m1=deviceObj.read_until_regexp('Highlight',timeout=15)
    exit_bios_shelll(device)
    exit_the_shell()



@logThis
def enter_incorrect_password(device):
    wrong='fghlg'
    deviceObj = Device.getDeviceObject(device)


    deviceObj.getPrompt("DIAGOS")
    deviceObj.sendline("")
    deviceObj.sendCmd("sudo reboot")

    # Enter BIOS Setup Menu
    out=deviceObj.read_until_regexp('Shell>',timeout=300)
    #print('The out is',out)
    deviceObj.sendline('exit')
    log.success('Sending incorrect password')
    deviceObj.sendCmd(wrong)
    deviceObj.sendCmd('\r')

    deviceObj.sendCmd('\b \b \b')


    deviceObj.sendCmd(wrong)
    deviceObj.sendCmd('\r')
    log.debug('####SYSTEM HALTED###')
    output1=deviceObj.read_until_regexp('Machine',timeout=10)
    

@logThis
def check_system_halt(device):
    p1= multiprocessing.Process(target=enter_incorrect_password(device))
    p2=multiprocessing.Process(target=powercycle_to_bios(device,'no',new_bios_pass))
    p1.start()
    time.sleep(400)
    p2.start()
    p1.join()
    p2.join()


@logThis
def check_system_halt_user(device):
    p1= multiprocessing.Process(target=enter_incorrect_password(device))
    p2=multiprocessing.Process(target=powercycle_to_bios(device,'no',bios_pass))
    p1.start()
    time.sleep(400)
    p2.start()
    p1.join()
    p2.join()

    
@logThis
def check_access_level(device,a):
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 5)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    time.sleep(10)
    bios_menu_lib.send_key(device, "KEY_UP", 2)
    output1=deviceObj.read_until_regexp(a,timeout=10)
    log.success('User access level test: PASSEED ')
    bios_menu_lib.send_key(device, "KEY_ESC", 3)
    exit_bios_shelll(device)
    exit_the_shell()
    return output1


##################################################################################################################################################################################

def check_cli_bios():
    device.sendCmd('sudo -s')
    x=['dmidecode -t bios','dmidecode -t system','dmidecode -t baseboard','dmidecode -t chassis',\
       'dmidecode -t processor','dmidecode -t memory']
    y=['dmidecode -t 0','dmidecode -t 1','dmidecode -t 2','dmidecode -t 3','dmidecode -t 4','dmidecode -t 17']
    count=0
    for i in range(len(x)):
        j1=device.executeCmd(x[i]).split()
        j2=device.executeCmd(y[i]).split()
        for i in range(0,6):
            j1.pop()
            j2.pop()
            j1.pop(0)
            j2.pop(0)
        for m1 in j2:
            if m1 not in j1:
                count+=1
        print('value of j1 :\n')
        print(j1)
        print('value of j2 :\n')
        print(j2)
        print('The value of count is ',count)
    if count >= 5:
        raise RuntimeError('Dmidecode test failed')






@logThis
def check_port_address(device):

    deviceObj = Device.getDeviceObject(device)
    #bios_menu_lib.send_key(device,'KEY_ESC')
    #out=deviceObj.read_until_regexp('Highlight',timeout=10)
    #bios_menu_lib.send_key(device, "KEY_ENTER")
    #bios_menu_lib.send_key(device, "KEY_UP", 4)
    ##bios_menu_lib.send_key(device, "KEY_ENTER")
    #out=deviceObj.read_until_regexp('Highlight',timeout=10)

    #bios_menu_lib.send_key(device, "KEY_DOWN", 8)
    #bios_menu_lib.send_key(device, "KEY_ENTER")
    #out=deviceObj.read_until_regexp('Legacy OS',timeout=10)
    #com=re.search('COM0.*\(([0-9A-z]+)',out).group(1)
    #bios_menu_lib.send_key(device,'KEY_ESC',4)
    #print('The out is ',out)
    #exit_bios_menu(device)
    #time.sleep(10)
    #exit_the_shell()
    c1=deviceObj.executeCmd('sudo dmesg|grep tty')
    if re.search(com,c1):
        log.success(' port address should be correct as definition in BIOS SPEC/release note')
    else:
        raise RuntimeError('Port address failure')


#################################################################################################################################3
@logThis
def useless_function(sec = 1):
     print(f'Sleeping for {sec} second(s)')
     for _ in range(5):
         time.sleep(sec)
         print(f'sleeping')


########################################TC65#########################################################
@logThis
def check_time_default(device,a='yes'):
    deviceObj = Device.getDeviceObject(device)
    val='40'
    bios_menu_lib.send_key(device,'KEY_ESC')
    out=deviceObj.read_until_regexp('Highlight',timeout=10)
    bios_menu_lib.send_key(device, "KEY_DOWN", 2)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    time.sleep(5)
    out=deviceObj.read_until_regexp('Highlight',timeout=10)


    bios_menu_lib.send_key(device,'KEY_DOWN',4)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    out=deviceObj.read_until_regexp('Highlight',timeout=10)
    if a=='yes':
        bios_menu_lib.send_key(device, "KEY_ENTER")
        deviceObj.sendCmd(val)
    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    out=deviceObj.read_until_regexp('Highlight',timeout=10)
    if not a == 'yes':
        if re.search(val,out):
            log.success('The change was reflected after reset')
        else:
            raise RuntimeError('Value did not reflect after reset')
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device,'KEY_ESC',3)

    exit_bios_menu(device)
    time.sleep(10)
    exit_the_shell()
########################################################################################################


###TCS 70

@logThis 
def check_memory():
     cmd1=run_command('free -h',prompt=None)
     if 'rror' in cmd1:
         raise RuntimeError('Memory free test fail')
     log.success('Memory test pass')
     cmd2=run_command('cat /proc/cpuinfo',prompt=None)
     CommonKeywords.should_match_ordered_regexp_list(cmd2,cpu_proc)
     log.success('Cpu info information matching with bios manual')    
     cmd5=run_command('fdisk -l',prompt=None)
     CommonKeywords.should_match_ordered_regexp_list(cmd5,fdisk_list)
     log.success('fdisk information matching with bios manual')

     
@logThis
def verifyHomePath():
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    output = run_command("cd /home",prompt='root@sonic')
    outputPath = run_command("pwd",prompt='root@sonic')
    if re.search("/home", outputPath):
        log.success("Can find the correct home  path!")
    else:
        raise RuntimeError("Failed to find the home path")


def checkStressHelp():
    flag = 0
    v1=['0 errors','Status: PASS - please verify no corrected errors']

    v2=run_command('stressapptest -s 36000 -M 28800 -m 4 -i 4 -C 8 -W -d /dev/sda3 --pause_delay 40000',prompt='root@sonic',timeout=50000)
    for x in v1:
        if not re.search(x,v2):
            flag = 1
    if flag == 0:
        log.success("No error encountered")
    else:
        raise RuntimeError("Error encountered")

#################################################################################################################3
#tc74
@logThis
def check_system_stress(device):
    deviceObj = Device.getDeviceObject(device)
    str2='Continue'
    str1='stepping'
   
    basic=[bios_version,'Platform.*Capitaine','Microcode Revision.*0E000014',]
    bios_menu_lib.send_key(device, "KEY_ESC")
    k1=deviceObj.read_until_regexp('Highlight',timeout=10)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 5)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    k2=deviceObj.read_until_regexp('Highlight',timeout=10)
    time.sleep(10)
    output2=deviceObj.read_until_regexp(str1,timeout=10)
    bios_menu_lib.send_key(device, "KEY_UP", 2)
    output1=deviceObj.read_until_regexp('Administrator',timeout=10)
    time.sleep(10)
    bios_menu_lib.send_key(device, "KEY_DOWN", 2)
    time.sleep(5)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ESC")
    for x in basic:
        if not re.search(x,output2):
            raise RuntimeError('Bios basic info failed')
    log.success('Bios basic info passed')
    for y in bios_list:
        if not re.search(y,k1):
            raise RuntimeError('Bios menu info failed')
    log.success('Bios menu info passed')

    exit_bios_shelll(device)
    exit_the_shell()
    





###########################################################################################################
##TC66
@logThis
def check_boottime_value(device,b,a='yes'):
    deviceObj=''
    deviceObj = deviceObj = Device.getDeviceObject(device)
    str1='Time-out.*'+b
    time.sleep(5)
    bios_menu_lib.send_key(device, "KEY_ESC")
    deviceObj.read_until_regexp('Highlight',timeout=30)

   
    bios_menu_lib.send_key(device, "KEY_DOWN", 2) 
    bios_menu_lib.send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp('Highlight',timeout=30)

    bios_menu_lib.send_key(device, "KEY_DOWN", 4)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp('Highlight',timeout=30)

    if a == 'yes':
        bios_menu_lib.send_key(device, "KEY_DOWN", 2)
        time.sleep(4)
        j2=deviceObj.read_until_regexp('Discard Changes',timeout=10)
        bios_menu_lib.send_key(device, "KEY_UP", 2)
        bios_menu_lib.send_key(device, "KEY_ENTER")
        deviceObj.sendCmd(b)
        deviceObj.sendCmd("\r")
        bios_menu_lib.send_key(device, "KEY_DOWN", 1)
        time.sleep(10)
        j1=deviceObj.read_until_regexp('Discard Changes',timeout=10)
        bios_menu_lib.send_key(device, "KEY_ENTER")

    else:
        time.sleep(5)
        j1=deviceObj.read_until_regexp('Discard Changes',timeout=10)

        
    if a != "yes":
        if re.search(str1,j1):
            log.success('Auto boot timeout value reflected after reboot/save ')
        else:
            log.fail('Autoboot value didnt reflect after reboot/save')

    

    bios_menu_lib.send_key(device, "KEY_ESC",4)
    exit_bios_menu(device)
    exit_the_shell()


##############################################################################
@logThis
def scan_mgmt():
    c1=device.executeCmd('ifconfig')
    CommonKeywords.should_match_ordered_regexp_list(c1,ifconfig_list)
    if not re.search('inet.*10.208',c1) :
        log.fail('Mgmt ip not found')
    else:
        log.success('mgmt ip present')
    ping_the_dut()


@logThis
def ping_the_dut():
    val1='0% packet loss'
    ip =' ping -c 4 ' + tftp_server_ipv4
    c1=device.executeCmd(ip)
    if val1 in c1:
        log.success('Ping successful')
    else:
        log.fail('Ping Failed')

@logThis
def scan_i2c():
    str1='I2C test all : Passed'
    device.sendCmd('sudo -s')
    j1=device.executeCmd('i2cdetect -l')
    CommonKeywords.should_match_ordered_regexp_list(j1,i2cdetect_list)
    j2=device.executeCmd('i2cdetect -y 0')
    for x,y in i2detect_y0.items():
        if not re.search(y[0],j2):
            print('Failing line',y)
    print('j2',j2)
    log.success('I2c detect for -y 0 passed')


    j3=device.executeCmd('i2cdetect -y 1')
    for x,y in i2detect_y1.items():
        if not re.search(y[0],j3):
            print('Failing line',y)
    log.success('I2c detect for -y 1 passed')

    j4=device.executeCmd('i2cdetect -y 10')
    for x,y in i2detect_y10.items():
        if not re.search(y[0],j4):
            print('Failing line',y)
    log.success('I2c detect for -y 10 passed')

    j5=device.executeCmd('i2cdetect -y 11')
    for x,y in i2detect_y11.items():
        if not re.search(y[0],j5):
            print('Failing line',y)
    log.success('I2c detect for -y 11 passed')

    run_command('cd /usr/local/cls_diag/bin',timeout=10)
    j6=device.executeCmd('./cel-i2c-test --all')
    validate_str(str1,j6,'I2c Test')
@logThis
def scan_disk():
    str1='---> PASSED <<<---'
    j1=device.executeCmd('sudo fdisk -l')
    CommonKeywords.should_match_ordered_regexp_list(j1,fdisk_list)
    log.success('fdisk information matching with bios manual')
 
    j2=device.executeCmd('./cel-storage-test --all')
    validate_str('Storage.*Test.*Passed',j2,'Storage Test')
@logThis
def recheckCpldScratch():
    cmd=run_command("./cel-bb-cpld-test --all",prompt='root@sonic')
    output=cmd.splitlines()
    d1_value=output[-3]
    device.sendCmd('cd /usr/local/cls_diag/tools')
    d2=run_command("./lpc_cpld_x64_64 blu r 0xa1e1",prompt ='root@sonic')
    if re.search(d1_value,d2):
        log.success("Read was successful")
    else:
        raise RuntimeError("Read has failed")
    run_command('exit',prompt='admin@sonic|root@sonic',timeout=5)

@logThis
def scan_come():
    d1_value='0x18'
    str1='sysinfo test all end'
    device.sendCmd('cd /usr/local/cls_diag/tools')
    c1=device.executeCmd('./lpc_cpld_x64_64 blu r 0xa1e0')
    if re.search(d1_value,c1):
        log.success("COMe version is correct")
    else:
        raise RuntimeError("COMe version is incorrect")

    c2=run_command("cd /usr/local/cls_diag/bin", prompt="root@sonic:.*", timeout=5)
    output = run_command("./cel-sysinfo-test --all", prompt="root@sonic:.*", timeout=5)
    validate_str(str1,output,'COme Test')

@logThis
def scan_fpga():
    str1='FPGA Test : Passed'
    c1=device.executeCmd('./cel-fpga-test --all')
    validate_str(str1,c1,'FPGA Test ')


@logThis
def scan_TEMP_CHECK():
    str1='Result:Temp test all --> Passed'
    c1=device.executeCmd('./cel-temp-test --all')
    validate_str(str1,c1,'Temp Test ')
#####################################################################################################################################################################
@logThis
def check_scans(device):
    deviceObj = Device.getDeviceObject(device)
    str1='PCIe Test.*:.*PASSED'
    deviceObj.sendCmd('sudo -s','root@sonic')
    run_command('cd /usr/local/cls_diag/bin',timeout=10)
    log.debug('******************** SCAN PCIE Test    *******************************************')
    j=deviceObj.executeCmd('./cel-pci-test --all -f ../configs/pcis_edk2.yaml')
    validate_str(str1,j,'PCIE Test')


    #scan_i2c()
    check_lpc_interface(device)
    scan_i2c()
    scan_disk()
    scan_come()
    #recheckCpldScratch()
    scan_fpga()
    check_dmidecode_bios()
    scan_TEMP_CHECK()
    check_eeprom_tlv()
    scan_mgmt()




#######################################################################################################
@logThis
def check_power_off():
    device.sendCmd('sudo -s')
    device.sendCmd('poweroff')
    time.sleep(160)
    exit_the_shell()
    time.sleep(160)


@logThis
def check_watch_dog(device):
    device= Device.getDeviceObject(device)
    device.sendCmd('sudo -s')
    j1=device.executeCmd('service gfpga-watchdog restart')
    time.sleep(10)
    j2=device.sendCmd('service gfpga-watchdog status')
    j3=device.read_until_regexp('Started DD3',timeout=10)
    device.sendCmd('q')
    j3=re.search('Main PID.*([0-9]{1,7}\s)',j3).group().split()[2]
    print('Value of j3',j3)
    s='kill -9 '+ j3
    j4=device.executeCmd(s)
    time.sleep(100)
    exit_the_shell()
    

@logThis
def check_diff_reboot(device):
    device=deviceObj = Device.getDeviceObject(device)
    run_command('sudo fast-reboot')
    time.sleep(260)
    device.loginToDiagOS()
    device.sendCmd('sudo -s')
    run_command('echo 0x4449454a > /sys/devices/gfpga-platform/board_powercycle')
    time.sleep(60)
    exit_the_shell()
    run_command('cd /usr/local/cls_diag/tools/')
    device.sendCmd('sudo -s')
    run_command('./lpc_cpld_x64_64 blu w 0xa190 0x0')
    time.sleep(60)
    exit_the_shell()






##############################################################################################################
@logThis
def  check_coverage(a):
    log.success('This testcase has already been covered as a part of exisitng testcases')
    print('Please refer testcase : ',a)



#####################################################################################################################333
@logThis
def check_ospf():
    val='0xde'
    val1='0x55'
    val2='0x13'
    device.executeCmd('cd /usr/local/cls_diag/tools')
    run_command('sudo -s')
    c1=device.executeCmd('./lpc_cpld_x64_64 blu r 0xa1e1')
    c2=device.executeCmd('./lpc_cpld_x64_64 blu r 0xa101')
    c3= device.executeCmd('cat /sys/devices/gfpga-platform/osfp_rst')
  
    m=re.search(val1,c1) and re.search(val,c2)
    if m:
        log.success('CPLD scratch  is correct')
    else:
        raise RuntimeError('CPLD scratch is incorrect')
    if '0' in c3:
        log.success('osfp_rst value is default')
    else:
        raise RuntimeError('osfp_rst value not  default.')


    c1=device.executeCmd('./lpc_cpld_x64_64 blu w 0xa101 0x13')
    c2=device.executeCmd('./lpc_cpld_x64_64 blu w 0xa1e1 0x13')

    m=re.search(val2,c1) and re.search(val2,c2)
    if m:
        log.success('CPLD scratch  is correct')
    else:
        raise RuntimeError('CPLD scratch is incorrect')
    run_command('echo "0x13" > /sys/devices/gfpga-platform/osfp_rst')
    check_power_off()
    device.executeCmd('cd /usr/local/cls_diag/tools')
    run_command('sudo -s')
    c1=device.executeCmd('./lpc_cpld_x64_64 blu r 0xa1e1')
    c2=device.executeCmd('./lpc_cpld_x64_64 blu r 0xa101')
    c3= device.executeCmd('cat /sys/devices/gfpga-platform/osfp_rst')

    m=re.search(val1,c1) and re.search(val,c2)
    if m:
        log.success('CPLD scratch  is correct')
    else:
        raise RuntimeError('CPLD scratch is incorrect')
    if '0' in c3:
        log.success('osfp_rst value is default')
    else:
        raise RuntimeError('osfp_rst value not  default.')


####################################################################################################
##Tcs40/41
@logThis
def check_microsd(device):
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN", 1)
    j1=deviceObj.read_until_regexp('Media',timeout=15)


    bios_menu_lib.send_key(device, "KEY_ESC",5)
    output=deviceObj.read_until_regexp('Continue',timeout=10)
    log.success('Bios Main Menu ')
    bios_menu_lib.send_key(device, "KEY_DOWN", 4)
    time.sleep(5)
    deviceObj.sendCmd('\r')
    j5=deviceObj.read_until_regexp('blk4',timeout=100)
    print('The value of j is',j5)
    print('The value of m is ',j1)
    exit_the_shell()
    if re.search('fs1  :Removable HardDisk',j5):
        log.success('Microsd detected in shell')
    else:
        raise RuntimeError('Microsd not detected in shell')

    if re.search('UEFI USB0:Generic Ultra Fast Media',j1):
        log.success('Microsd detected in BIOS')
    else:
        raise RuntimeError('Microsd not detected in BIOS')
    
    c1=run_command('fdisk -l')
    if re.search('/dev/sdb1.*FAT',c1):
        log.success('Microsd detected in SONIC')
    else:
        raise RuntimeError('Microsd not detected in SONIC')

@logThis
def convert_sd_to_onie():
    run_command('cd /home/admin/')
    c1=run_command('dd if=onie-recovery-x86_64-cel_brixia-r0.iso of=/dev/sdb')
    if not 'copied' in c1:
        raise RuntimeError('MicrSd card issue')






#################################################################################################
#tc06
@logThis
def check_me_config(device):
    val1='Current State.*Recovery'
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")

    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN",4)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN",11)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    j1=deviceObj.read_until_regexp('No Error',timeout=15)
    if re.search(val1,j1):
        log.success('ME default mode is recovery')
    else:
        raise RuntimeError('ME default mode is incorrect')

    exit_bios_shelll(device)
    exit_the_shell()


##################################################################################################3
#tc23
@logThis
def check_fast_boot(device,a,b,c):
    c=int(c)   
    b='KEY_'+b
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")

    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN",4)

    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN",4)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN",23)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device,b,c)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN",1)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device,b,c)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN",1)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device,b,c)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN",1)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device,b,c)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN",1)
    j1=deviceObj.read_until_regexp('BDAT',timeout=15)

    bios_menu_lib.send_key(device, "KEY_ESC")
    time.sleep(10)
    deviceObj.sendCmd("Y")
    time.sleep(5)
    deviceObj.sendCmd("\r")
 
    bios_menu_lib.send_key(device, "KEY_ESC",4)
    str11= 'Attempt Fast Boot.*'+a
    str12='Attempt Fast Cold Boot.*'+a
    str13= 'MemTest On Fast Boot.*'+a
    str14='RMT On Cold Fast Boot.*'+a
    print('values:')
    print(str11,str12,str13,str14)
    m9=re.search(str11,j1) and re.search(str12,j1) and re.search(str12,j1) and re.search(str14,j1)
    if m9:
        log.success('Fast boot operation successfull')
    else:
        raise RuntimeError('Fast boot operation Failed')
    exit_bios_shelll(device)
    exit_the_shell()


######################################################################################################################
##TC40

@logThis
def check_micro_operations(device):
    device= Device.getDeviceObject(device)
    device.sendCmd('sudo -s')
    file1='test.txt'
    file2='final.txt'
    device.sendCmd('touch /home/test.txt')
    c1=device.executeCmd('fdisk -l')
    c2=device.executeCmd('mount /dev/sdb1 /mnt')
    device.sendCmd('touch /mnt/final.txt')
    if  re.search('rror',c2):
        raise RuntimeError('Mount failed')
    else:
        log.success('Mount successful')
    c3=device.executeCmd('ls -la /home/')
    c4=device.executeCmd('ls -la /mnt')
    if not re.search(file1,c3) and not re.search(file2,c4):
        raise RuntimeError('Files not found')

    ##operation
    cmd1='cp /home/'+file1+' /mnt'
    c6=device.executeCmd(cmd1)
    device.executeCmd('sync')

    cmd2='cp /mnt/'+file2+' /home/'
    c7=device.executeCmd(cmd2)
    device.executeCmd('sync')

    c3=device.executeCmd('ls -la /home/')
    c4=device.executeCmd('ls -la /mnt')

    if  not re.search(file2,c3) and not re.search(file1,c4):
        raise RuntimeError('Files not found')
    else:
        log.success('Files copied successfully')

    c8=device.executeCmd('umount /mnt')

    c3=device.executeCmd('ls -la /home/')
    c4=device.executeCmd('ls -la /mnt')

    if  not re.search(file2,c3) and  re.search(file1,c4):
        raise RuntimeError('Files not found')
    else:
        log.success('Files copied successfully')

    device.sendCmd('cd /usr/local/cls_diag/bin')
    c9=device.executeCmd('./cel-storage-test -d 2')
    if 'Storage Test --> Passed' in c9:
        log.success('Storage on /mnt passed')
    else:
        log.fail('Storage test failed')
        
##################################################################################
@logThis
def check_lpc_interface(device):
    device= Device.getDeviceObject(device)
    device.sendCmd('sudo -s')
    device.sendCmd(' cd /usr/local/cls_diag/tools')
    c1=device.executeCmd(' ./lpc_cpld_x64_64 blu r 0xA100')
    c2=device.executeCmd(' ./lpc_cpld_x64_64 blu r 0xA101')
    c3=device.executeCmd('./lpc_cpld_x64_64 blu r 0xA1E0')
    c4=device.executeCmd(' ./lpc_cpld_x64_64 blu r 0xA1E1')
   
    m= re.search(lpca0,c1) and re.search(lpca1,c2) and re.search(lpce0,c3) and re.search(lpce1,c4)
    if m:
        log.success('CPU interface values are correct')
    else:
        raise RuntimeError('LPC values are incorrect')

    j1=device.executeCmd('./lpc_cpld_x64_64 blu w 0xA101 0x21')
    j2=device.executeCmd('./lpc_cpld_x64_64 blu w 0xA1E1 0x21')
    c7=device.executeCmd('./lpc_cpld_x64_64 blu r 0xA101')
    c8=device.executeCmd(' ./lpc_cpld_x64_64 blu r 0xA1E1')
    n= re.search('0x21',c7) and re.search('0x21',c8)
    if n:
        log.success('CPU interface written values are correct')
    else:
        raise RuntimeError('LPC written values are incorrect')

    j1=device.executeCmd('./lpc_cpld_x64_64 blu w 0xA101 0x22')
    j2=device.executeCmd('./lpc_cpld_x64_64 blu w 0xA1E1 0x22')
    c7=device.executeCmd('./lpc_cpld_x64_64 blu r 0xA101')
    c8=device.executeCmd(' ./lpc_cpld_x64_64 blu r 0xA1E1')
    n= re.search('0x22',c7) and re.search('0x22',c8)
    if n:
        log.success('CPU interface written values are correct')
    else:
        raise RuntimeError('LPC written values are incorrect')


    j1=device.executeCmd('./lpc_cpld_x64_64 blu w 0xA101 0x23')
    j2=device.executeCmd('./lpc_cpld_x64_64 blu w 0xA1E1 0x23')
    c7=device.executeCmd('./lpc_cpld_x64_64 blu r 0xA101')
    c8=device.executeCmd(' ./lpc_cpld_x64_64 blu r 0xA1E1')
    n= re.search('0x23',c7) and re.search('0x23',c8)
    if n:
        log.success('CPU interface written values are correct')
    else:
        raise RuntimeError('LPC written values are incorrect') 

    device.sendCmd('cd ../bin')
    c10=device.executeCmd(' ./cel-bb-cpld-test --all ')
    c11=device.executeCmd(' ./cel-cpld-test --all ')

    m = re.search('Test : Passed',c10) and re.search('Test : Passed',c11)
    if m:
        log.success('CPLD and BBLD tests passed')
    else:
        raise RuntimeError('CPLD and BBLD tests failed')


@logThis
def check_cpu_bus(device):
    device= Device.getDeviceObject(device)
    device.sendCmd('sudo -s')
    scan_i2c()
    time.sleep(10)
    c1=device.executeCmd('i2cdetect -q -y 1 0x34 0x34')
    for x,y in i2cdetect_new.items():
        if not re.search(y[0],c1):
            print('Failing line',y)
        else:
            log.success('BUS modified successfully')


    c2=device.executeCmd('i2cdetect -l | grep -i imc')
    #CommonKeywords.should_match_ordered_regexp_list(c2,imc)
    for x in imc:
        if not re.search(x,c2):
            raise RuntimeError('imc bus info failed')
    log.success('imc bus  info passed')

    c3=device.executeCmd(' i2cdetect -F 28')
    c4=device.executeCmd(' i2cdetect -F 29')
    CommonKeywords.should_match_ordered_regexp_list(c3,i2cdetect_28)
    CommonKeywords.should_match_ordered_regexp_list(c4,i2cdetect_28)




##############################################################################################
##tc36

#######################################################################################################
#test31
@logThis
def check_pcie(device):
    str1='PCIe Test.*:.*PASSED'
    deviceObj=''
    deviceObj = Device.getDeviceObject(device)
    deviceObj.sendCmd('sudo -s')
    c1=deviceObj.executeCmd('lspci')
    CommonKeywords.should_match_ordered_regexp_list(c1,lspci)
    deviceObj.sendCmd('cd /usr/local/cls_diag/bin')
    log.debug('******************** SCAN PCIE Test    *******************************************')
    j=deviceObj.executeCmd('./cel-pci-test --all -f ../configs/pcis_edk2.yaml')
    validate_str(str1,j,'PCIE Test')

    deviceObj.sendCmd('cd /usr/local/cls_sdk')
    deviceObj.sendCmd("/etc/init.d/opennsl-modules stop")
    deviceObj.sendCmd(' ./auto_load_user.sh')
    c2=run_command('./bcm.user -y brixiaV2-TH4G-256x1x100.yml',prompt='BCM.0>')
    c3=run_command('ps',prompt='BCM.0>')
    CommonKeywords.should_match_ordered_regexp_list(c3,bcm)
    c4=deviceObj.sendCmd('exit')

#########################################################################################################################
#tc25

@logThis
def check_info_cpu(device,val,a='no'):
    if val == '0':
        key = '16'
        l=25.0
        key1='2' 
    else:
        key= '2'
        l=98.0
        key1='16'
        
    deviceObj=''
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_DOWN",4)
    bios_menu_lib.send_key(device, "KEY_ENTER")
 
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device, "KEY_ENTER")
    if a == 'yes':
        bios_menu_lib.send_key(device, "KEY_ENTER")
        deviceObj.sendCmd(val)
        deviceObj.sendCmd("\r")
        bios_menu_lib.send_key(device, "KEY_ESC")
        time.sleep(15)
        deviceObj.sendCmd("Y")
        time.sleep(5)
        deviceObj.sendCmd("\r")
        bios_menu_lib.send_key(device, "KEY_ESC",4)

        bios_menu_lib.send_key(device, "KEY_ESC")
        bios_menu_lib.send_key(device, "KEY_ENTER")

        bios_menu_lib.send_key(device,"KEY_UP",2)
        bios_menu_lib.send_key(device, "KEY_ENTER")


        c1=deviceObj.read_until_regexp('Stepping',timeout=20)
        c22=re.search('Total CPU Number:.*[0-9]+',c1).group().split()[3]
        if key1 == c22:
            log.success('Cores information correct before reset')
        else:
            log.fail('Cores information incorrect before reset')
        bios_menu_lib.send_key(device, "KEY_ESC",3)
        exit_bios_shelll(device)
        exit_the_shell()
        c100=deviceObj.executeCmd('lscpu')
        m=re.search('CPU\(s\).*[0-9]+',c100).group().split()[1]
        if m == key:
            log.success('Cores information is correct')
        else:
            log.fail('Core information is incorrect')
        c101=deviceObj.executeCmd('cat /proc/cpuinfo')
        if key == '16':
            CommonKeywords.should_match_ordered_regexp_list(c101,cpu_proc)
        else:
            CommonKeywords.should_match_ordered_regexp_list(c101,cpu_new)
        deviceObj.sendCmd('top')
        time.sleep(3)
        deviceObj.sendCmd('q')

        c103=deviceObj.read_until_regexp('#',timeout=20)
        c4=re.search('\%Cpu\(s\)\:.*[0-9]\.?',c103).group().split()[1]
        print('value of c103',c103)
        deviceObj.sendCmd('cd /root/BDX_DE_Linux')
        deviceObj.sendCmd('modprobe msr')
        deviceObj.sendCmd('./BroadwellPwrMon')
        c104=deviceObj.read_until_regexp('Idle',timeout=20)
        print('value of c104',c104)
        print('value of ',c4,l)
        if float(c4) < float(l):
            log.success('Cpu utilization in range')
        else:
            log.fail('Cpu utlization not in range')
        if key == 16:
            CommonKeywords.should_match_ordered_regexp_list(c104,core8)
        else:
            CommonKeywords.should_match_ordered_regexp_list(c104,core0)
        for i in range(3):
            deviceObj.sendMsg(Const.KEY_CTRL_C)
            try:
                d1=device.read_until_regexp('#', timeout=15)
                break
            except Exception:
                continue
    else:
        c2=deviceObj.read_until_regexp('Cfg',timeout=20)
        print('The value of c2',c2)
        bios_menu_lib.send_key(device, "KEY_ESC")
        exit_bios_shelll(device)
        exit_the_shell()

####################################################################################################################3
#test32
@logThis
def check_pcie_conf(device):
    deviceObj=''
    deviceObj = Device.getDeviceObject(device)
    device=deviceObj
    c1=run_command('sudo -s')
    c1=deviceObj.executeCmd('lspci')
    c2=deviceObj.executeCmd('lspci -vvv')
    CommonKeywords.should_match_ordered_regexp_list(c1,lspci)
    CommonKeywords.should_match_ordered_regexp_list(c2,lspci)
    log.success('Lspci devices information is correct')
    o1=device.executeCmd('lspci -s 00:00.0 -vv | grep -i lnkcap')
    o2=device.executeCmd('lspci -s 00:01.0 -vv | grep -i lnkcap')
    o3=device.executeCmd('lspci -s 00:01.1 -vv | grep -i lnkcap')
    o4=device.executeCmd('lspci -s 00:02.0 -vv | grep -i lnkcap')
    o5=device.executeCmd('lspci -s 00:02.2 -vv | grep -i lnkcap')
    o6=device.executeCmd('lspci -s 00:02.3 -vv | grep -i lnkcap')
    o7=device.executeCmd('lspci -s 00:03.0 -vv | grep -i lnkcap')
    o44=re.search('rror',o1) or re.search('rror',o2) or re.search('rror',o3) or \
        re.search('rror',o4) or re.search('rror',o5) or re.search('rror',o6) or \
        re.search('rror',o7)
    if o44:
        raise RuntimeError('Error in displaying speed information')
    else:
        log.success('Speed and width inofrmation displayed without errors')

    v1=device.executeCmd('lspci -s 01:00.0 -vvvxxx')
    CommonKeywords.should_match_ordered_regexp_list(v1,lspci_broad)
    log.success('Information for 01:00 is displayed as per manual')

    v2=device.executeCmd('lspci -s 03:00.0 -vvvxxx')
    CommonKeywords.should_match_ordered_regexp_list(v2,lspci_intel)
    log.success('Information for 03:00 is displayed as per manual')

    v3=device.executeCmd('lspci -s 07:00.0 -vvvxxx')
    CommonKeywords.should_match_ordered_regexp_list(v3,lspci_sfp)
    log.success('Information for 07:00 is displayed as per manual')

    l1=device.executeCmd('lspci -s 05:00.0 -vvvxxx')
    l2=device.executeCmd('lspci -s 05:00.1 -vvvxxx')
    CommonKeywords.should_match_ordered_regexp_list(l1,lspci_sfp)
    CommonKeywords.should_match_ordered_regexp_list(l2,lspci_sfp)
    log.success('Lspci X552 10Gbe SFP+ information : PASS')

    k1=device.executeCmd('lspci -s 0c:00.0 -vvvxxx')
    k2=device.executeCmd('lspci -s 0d:00.0 -vvvxxx')
    CommonKeywords.should_match_ordered_regexp_list(k1,lspci_mgmt)
    CommonKeywords.should_match_ordered_regexp_list(k2,lspci_mgmt)
    log.success('Lspci I210 Gigabit information : PASS')


    m7=device.executeCmd('lspci -vvvxxx | grep -i msi')
    m8=device.executeCmd('lspci -vvvxxx | grep -i bridge')
    m9=device.executeCmd('lspci -vvvxxx | grep -i device')
    s1=device.executeCmd('lspci -vvvxxx | grep -i \"Speed 2.5GT/s\" ')
    s2=device.executeCmd('lspci -vvvxxx | grep -i \"Speed 5GT/s\" ')
    s3=device.executeCmd('lspci -vvvxxx | grep -i \"Speed 8GT/s\" ')
    CommonKeywords.should_match_ordered_regexp_list(m8,lspci_bridge)
    log.success('lspci bridge information : PASS')
    CommonKeywords.should_match_ordered_regexp_list(m9,lspci_device)
    log.success('lspci Device information : PASS')

    s4=re.search('rror',s1) or re.search('rror',s2) or re.search('rror',s3)
    if s4:
        raise RuntimeError('Error in lspci speed grep')
    else:
        log.success('Lspci speeds are in check')

#################################################################################################################################
#tc49
@logThis
def check_acpi_test(device):
    str1='got \r \n'
    deviceObj=''
    deviceObj = Device.getDeviceObject(device)
    deviceObj.sendCmd('sudo -s')
    deviceObj.executeCmd('mount /dev/sdb1 /mnt') 
    deviceObj.executeCmd('cp /home/admin/acpidump.efi /mnt/')
    deviceObj.sendCmd('sudo reboot')
    c2=deviceObj.read_until_regexp('Shell>',timeout=300)
    deviceObj.sendCmd('\r \n')
    time.sleep(5)
    deviceObj.sendCmd('fs1:')
    deviceObj.sendCmd('\r ')
    time.sleep(2)
    deviceObj.sendCmd('cls  \r \n ')
    time.sleep(5)

    deviceObj.sendCmd(str1)
    time.sleep(5)
    deviceObj.sendCmd(' \r \n ')
    device=deviceObj

    device.sendCmd('fs0: \r \n')
    time.sleep(2)
    device.sendCmd('cd EFI \r \n')
    time.sleep(2)
    device.sendCmd('cd SONiC-OS \r \n')
    time.sleep(2)
    device.sendCmd('grubx64.efi \r \n')
    time.sleep(5)
    device.sendCmd('\r')
    device.read_until_regexp('sonic login',timeout=80)
    device.loginToDiagOS()
    device.sendCmd('sudo -s','root@sonic',timeout =20)

    deviceObj.executeCmd('mount /dev/sdb1 /mnt')
    deviceObj.executeCmd('cd  /mnt')

    c1=device.executeCmd('hexdump -C apic.dat')
    c2=device.executeCmd('hexdump -C /sys/firmware/acpi/tables/APIC')
    deviceObj.executeCmd('umount /mnt')
    m = re.search('rror',c1) and re.search('rror',c2)
    if m:
        raise RuntimeError('Error in hexdump')
    else:
        log.success('HexDump successful')


###########################################################################################################333
@logThis
def check_freq(device):
    deviceObj=''
    deviceObj = Device.getDeviceObject(device)
    cmd_list=['1600','1867','2133','Auto']
    for x in cmd_list:
        log.debug('###############################Starting test######################')
        bios_menu_lib.send_key(device, "KEY_ESC")
        bios_menu_lib.send_key(device, "KEY_ENTER")

        bios_menu_lib.send_key(device,"KEY_DOWN",4)
        bios_menu_lib.send_key(device, "KEY_ENTER")
        bios_menu_lib.send_key(device,"KEY_DOWN",4)
        bios_menu_lib.send_key(device, "KEY_ENTER")
        bios_menu_lib.send_key(device,"KEY_DOWN",2)

        bios_menu_lib.send_key(device, "KEY_ENTER")
        if x != 'Auto':
            bios_menu_lib.send_key(device, "KEY_DOWN",1)
        else:
            bios_menu_lib.send_key(device, "KEY_UP",3)
        time.sleep(2) 
        bios_menu_lib.send_key(device, "KEY_ENTER")
        time.sleep(10)
        bios_menu_lib.send_key(device, "KEY_ESC")
        time.sleep(15)
        deviceObj.sendCmd("Y")
        time.sleep(5)
        deviceObj.sendCmd("\r")

        exit_bios_shelll(device)
        exit_the_shell()

        c3=deviceObj.executeCmd('dmidecode --t memory')
        t= re.search('Configured Memory Speed:.*([0-9]{4})',c3).group(1)
        print('Comparing t and x',t,x)
        if t!=x and x!='Auto':
            t=int(t)+1
            t=str(t)
        if t == x or x == 'Auto':
            log.success('Configured memory test passed')
        else:
            log.fail('Configured  memory test failed')
        if x != 'Auto':
            enter_into_bios_setup(device,bios_pass)

#####################################################################################
#tc52
@logThis
def check_sfp_interface(device):
    deviceObj=''
    deviceObj = Device.getDeviceObject(device)
    device=deviceObj
    str1='PCIe Test.*:.*PASSED'
    device.sendCmd('sudo -s','root@sonic')
    run_command('cd /usr/local/cls_diag/bin',timeout=10)
    log.debug('******************** SCAN PCIE Test    *******************************************')
    j=device.executeCmd('./cel-pci-test --all -f ../configs/pcis_edk2.yaml')
    validate_str(str1,j,'PCIE Test')

    run_command('./cel-qsfp-test --all')
    deviceObj.sendCmd('cd /usr/local/cls_sdk')
    deviceObj.sendCmd("/etc/init.d/opennsl-modules stop")
    deviceObj.sendCmd(' ./auto_load_user.sh')
    c2=run_command('./bcm.user -y brixiaV2-TH4G-256x1x100.yml',prompt='BCM.0>')
    c3=run_command('ps',prompt='BCM.0>')
    CommonKeywords.should_match_ordered_regexp_list(c3,bcm)
    c4=deviceObj.sendCmd('exit')
##############################################################################################################

#tc32
@logThis
def check_iio_config(device):
    deviceObj=''
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device,"KEY_DOWN",4)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device,"KEY_DOWN",5)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device,"KEY_DOWN",6)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device,"KEY_DOWN",5)
    for i in range(0,8):
        bios_menu_lib.send_key(device, "KEY_ENTER")
        time.sleep(3)
        c1=deviceObj.read_until_regexp('Payload',timeout=20)
        bios_menu_lib.send_key(device,"KEY_DOWN",20)
        c2=deviceObj.read_until_regexp('Sync',timeout=20)
        bios_menu_lib.send_key(device, "KEY_ESC")
        time.sleep(5)
        bios_menu_lib.send_key(device,"KEY_DOWN",1)


@logThis
def try_pch(device):
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_ESC",6)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device,"KEY_DOWN",4)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device,"KEY_DOWN",6)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device,"KEY_DOWN",1)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    bios_menu_lib.send_key(device,"KEY_DOWN",8)
    for i in range(2,5):
        bios_menu_lib.send_key(device, "KEY_ENTER")
        bios_menu_lib.send_key(device, "KEY_ESC")
        bios_menu_lib.send_key(device, "KEY_ENTER")
        time.sleep(5)
        if i == 11:
            bios_menu_lib.send_key(device,"KEY_DOWN",16)
        else:
            bios_menu_lib.send_key(device,"KEY_UP",3)
        time.sleep(5)
        g1=''
        g1=deviceObj.read_until_regexp('Extra Bus Reserved',timeout=20)
        print('######ITERATION FOR PORT  NO: ',i)
        print(g1)
        if not re.search('MSI.*Enabled',g1):
            log.fail('MSI not enabled or this port')
        bios_menu_lib.send_key(device, "KEY_ESC")
        time.sleep(5)
        bios_menu_lib.send_key(device,"KEY_DOWN",1)
        if i==8:
            bios_menu_lib.send_key(device, "KEY_ESC",8)
            
    exit_bios_shelll(device)
    exit_the_shell()


@logThis
def pch_test(device):
    deviceObj = Device.getDeviceObject(device)
    count=0
    for i in range(0,7):
        bios_menu_lib.send_key(device, "KEY_ESC",3)
        bios_menu_lib.send_key(device, "KEY_ENTER")
        bios_menu_lib.send_key(device,"KEY_DOWN",4)
        bios_menu_lib.send_key(device, "KEY_ENTER")
        bios_menu_lib.send_key(device,"KEY_DOWN",6)
        bios_menu_lib.send_key(device, "KEY_ENTER")
        bios_menu_lib.send_key(device,"KEY_DOWN",1)
        bios_menu_lib.send_key(device, "KEY_ENTER")
        bios_menu_lib.send_key(device,"KEY_DOWN",8)
        if count == 0 :
            bios_menu_lib.send_key(device, "KEY_ENTER")
        else:
            bios_menu_lib.send_key(device, "KEY_DOWN",count)
            bios_menu_lib.send_key(device, "KEY_ENTER")
        time.sleep(5)
        bios_menu_lib.send_key(device,"KEY_DOWN",16)
        time.sleep(5)
        g1=''
        g1=deviceObj.read_until_regexp('Extra Bus Reserved',timeout=20)
        print('The value of g1',g1)
        time.sleep(5)

        bios_menu_lib.send_key(device, "KEY_ESC",5)
        time.sleep(30)
        count+=1
    exit_bios_shelll(device)
    exit_the_shell()


@logThis
def reboot_without_shell():
    device.sendCmd('reboot')
    device.read_until_regexp('sonic login:',timeout=300)
    device.loginToDiagOS()
   


######################################################################################

@logThis
def check_chopper_stress(device):
    deviceObj = Device.getDeviceObject(device)
    str2='Continue'
    str1='stepping'
    basic=['BIOS Revision.*0.0.5','Platform.*Capitaine','Microcode Revision.*0E000014',]
    bios_menu_lib.send_key(device, "KEY_ESC")
    k1=deviceObj.read_until_regexp('Highlight',timeout=10)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    bios_menu_lib.send_key(device, "KEY_DOWN", 5)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    k2=deviceObj.read_until_regexp('Highlight',timeout=10)
    time.sleep(10)
    output2=deviceObj.read_until_regexp(str1,timeout=10)
    bios_menu_lib.send_key(device, "KEY_UP", 2)
    output1=deviceObj.read_until_regexp('Administrator',timeout=10)
    time.sleep(10)
    bios_menu_lib.send_key(device, "KEY_DOWN", 2)
    time.sleep(5)
    bios_menu_lib.send_key(device, "KEY_ESC")
    bios_menu_lib.send_key(device, "KEY_ESC")
    for x in basic:
        if not re.search(x,output2):
            raise RuntimeError('Bios basic info failed')
    log.success('Bios basic info passed')
    for y in bios_list:
        if not re.search(y,k1):
            raise RuntimeError('Bios menu info failed')
    log.success('Bios menu info passed')

    exit_bios_shelll(device)
    exit_the_nerf()



@logThis
def exit_the_nerf():
    device = DeviceMgr.getDevice()
    time.sleep(5)
    out=device.read_until_regexp('Shell>',timeout=200)
    device.sendCmd('fs0: \r \n')
    time.sleep(2)
    device.sendCmd('nerf.x86_64.efi \r \n')
    time.sleep(5)
    device.sendCmd('\r')
    device.read_until_regexp('.*login',timeout=300)
    device.loginToDiagOS()



@logThis
def check_mgmt_info(device):
    deviceObj = Device.getDeviceObject(device)
    deviceObj.sendCmd('sudo -s')
    c1=deviceObj.executeCmd('ifconfig -a')
    c2= deviceObj.executeCmd('lspci -s 0c:00.0')
    time.sleep(5)
    c3= deviceObj.executeCmd('lspci -s 0d:00.0')
    CommonKeywords.should_match_ordered_regexp_list(c2,mgmt_info)
    CommonKeywords.should_match_ordered_regexp_list(c3,mgmt_info)    
    log.success('I210 information is correct')
    if re.search('eth0.*UP',c1):
        log.success('Ifconfig info correct')
    else:
        log.fail('Ifconfig info not correct')
