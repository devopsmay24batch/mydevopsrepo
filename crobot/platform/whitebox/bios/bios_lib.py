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
from BIOS_variable import *
from BMC_variable import *
from datetime import datetime, timedelta
from dataStructure import nestedDict, parser
from errorsModule import noSuchClass, testFailed
from SwImage import SwImage
from Server import Server
from pexpect import pxssh
import sys
import getpass
import WhiteboxLibAdapter
import whitebox_lib


try:
    import parser_openbmc_lib as parserOpenbmc
    import DeviceMgr
    from Device import Device

except Exception as err:
    log.cprint(str(err))

deviceObj = DeviceMgr.getDevice()


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

def enter_into_bios_setup(device,bios_password):
    log.debug('Entering procedure verify_bios_default_password with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    line1 = 'Enter Password'
    line2 = 'BIOS Version.*(ATHG[0-9]\.[0-9]\.[0-9][0-9]\.[0-9][0-9])'

    deviceObj.getPrompt("centos")
    deviceObj.sendline("")
    deviceObj.sendline("reboot")

    # Enter BIOS Setup Menu

    counter = 30
    while counter >= 0:
        bios_menu_lib.send_key(device, "KEY_DEL")
        counter -= 1
        time.sleep(1)
    output = None
    output = deviceObj.read_until_regexp(line1, timeout=10)
    if output is not None:
       deviceObj.sendline(bios_password)
       time.sleep(5)

    deviceObj = Device.getDeviceObject(device)
    line2 = 'BIOS Version.*(ATHG[0-9]\.[0-9]\.[0-9][0-9]\.[0-9][0-9])'
    output = deviceObj.read_until_regexp(line2, timeout=60)
    match = re.search(line2, output)

    if match:
        log.debug("Found '%s'"%(line2))
        log.success(match.group(1))
        log.success("Successfully entered BIOS with default password")
    else:
        log.fail("Failed to enter BIOS with default password")
        raise testFailed("Failed to enter BIOS with default password")

def set_configuration1_BIOS_setup(device,bios_password='c411ie'):
  log.info("Inside set_configuration1_BIOS_setup procedure")
  deviceObj = Device.getDeviceObject(device)

  bios_menu_lib.send_key(device, "KEY_RIGHT",times=1) #key_strokes_to_reach_Advance_menu
  pass_message_1="Trusted Computing Settings"
  match1=deviceObj.read_until_regexp(pass_message_1, timeout=20)
  bios_menu_lib.send_key(device, "KEY_ENTER")         #key_strokes_to_reach_Trusted Computing
  bios_menu_lib.send_key(device, "KEY_UP", 2)
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)      #Key_strokes_to_reach_Select TPM2.0
  bios_menu_lib.send_key(device, "KEY_UP", 1)         #Device Select                      [TPM 2.0]
  pass_message_2="Device Select.*TPM 2.0"
  match2=deviceObj.read_until_regexp(pass_message_2, timeout=20)
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)      #PH Randomization [Disabled]
  bios_menu_lib.send_key(device, "KEY_UP", 6)         #Select Pending operation
  pass_message_3="PH Randomization.*Disabled"
  match3=deviceObj.read_until_regexp(pass_message_3, timeout=20)
  bios_menu_lib.send_key(device, "KEY_ENTER", 1)
  bios_menu_lib.send_key(device, "KEY_DOWN", 1)
  bios_menu_lib.send_key(device, "KEY_ENTER", 1)      #Select Pending operation [TPM Clear]
  bios_menu_lib.send_key(device, "KEY_UP", 1)        #Pending operation                  [TPM Clear]
  pass_message_4="[Pending operation.*TPM Clear]"
  match4=deviceObj.read_until_regexp(pass_message_4, timeout=20)
  bios_menu_lib.send_key(device, "KEY_ESC")            #Trusted Computing Settings
  pass_message_5="Trusted Computing Settings"
  match5=deviceObj.read_until_regexp(pass_message_5, timeout=20)
  if match2 and match3 and match4 and match5:
    log.success(f"Trusted Computing Settings are successfully")
  else:
    log.fail(f"Trusted Computing Settings are failed")
    raise RuntimeError(f"Trusted Computing Settings are failed")

  bios_menu_lib.send_key(device, "KEY_RIGHT",times=2) #Socket Configuration Menu
  bios_menu_lib.send_key(device, "KEY_ENTER", 1)      #PROCESS CONFIG
  bios_menu_lib.send_key(device, "KEY_UP", 14)        #Select -> Enable Intel(R) TXT
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)      #Enable Intel(R) TXT [Disable]
  bios_menu_lib.send_key(device, "KEY_UP", 1)         #Enable Intel(R) TXT                  [Disable]
  pass_message_6="Intel.*Enable"
  match6=deviceObj.read_until_regexp(pass_message_6, timeout=20)
  bios_menu_lib.send_key(device, "KEY_ESC")           #change the Processor
  pass_message_7="change the Processor"
  match7=deviceObj.read_until_regexp(pass_message_7, timeout=20)  #change the Processor settings is completed
  if match7:
    log.success(f"Change the Processor settings is completed successfully")
  else:
    log.fail(f"Change the Processor settings is failed to set")

  bios_menu_lib.send_key(device, "KEY_RIGHT",times=4) #Save & Exit
  bios_menu_lib.send_key(device, "KEY_DOWN", 4)     #Save changes
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)

def BIOS_BasicTest1_under_UEFI_shell_mode(device,bios_password='c411ie'):
    log.debug('Entering procedure BIOS_BasicTest1_under_UEFI_shell_mode with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_RIGHT",7)
    bios_menu_lib.send_key(device, "KEY_UP",2)
    bios_menu_lib.send_key(device, "KEY_ENTER",2)
    deviceObj.read_until_regexp('Shell>', timeout=60)
    CommonLib.send_command("fs1:",promptStr='FS1:\>')
    CommonLib.send_command("ls",promptStr='FS1:\>')
    cmd1 = f"cd \"Server Security Toolkit Ver1.24\""
    cmd2 = f"cd \"TPM2_0Tools\""
    cmd3 = f"cd \"TPM2ProvFilesCBnT\""
    cmd4 = f"Tpm2_CBnT_Prov.nsh SHA256 Example"
    log.info(cmd1)
    log.info(cmd2)
    log.info(cmd3)
    log.info(cmd4)
    bios_menu_lib.send_str_on_bios(device, cmd1)
    bios_menu_lib.send_str_on_bios(device, cmd2)
    bios_menu_lib.send_str_on_bios(device, cmd3)
    bios_menu_lib.send_str_on_bios(device, cmd4)
    output = deviceObj.read_until_regexp('Provisioning Completed Successfully', timeout=200)
    log.info(output)
    CommonLib.send_command("exit")
    bios_menu_lib.exit_bios_1(device)

def set_configuration2_BIOS_setup(device,bios_password='c411ie'):
  log.info("Inside set_configuration2_BIOS_setup procedure")
  deviceObj = Device.getDeviceObject(device)

  bios_menu_lib.send_key(device, "KEY_RIGHT",times=3) #key_strokes_to_reach_Socket Configuration_menu
  bios_menu_lib.send_key(device, "KEY_ENTER")         #Processor Configuration
  pass_message_1="Processor Configuration"
  match1=deviceObj.read_until_regexp(pass_message_1, timeout=20)
  bios_menu_lib.send_key(device, "KEY_UP", 13)         #key_strokes_to_reach_Enables Intel(R) TXT
  bios_menu_lib.send_key(device, "KEY_ENTER")
  bios_menu_lib.send_key(device, "KEY_UP", 1)
  bios_menu_lib.send_key(device, "KEY_ENTER")          #Intel(R) TXT --> Disabled
  bios_menu_lib.send_key(device, "KEY_DOWN", 1)
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)       #VMX Enabled --> Enabled
  bios_menu_lib.send_key(device, "KEY_DOWN", 1)
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)       #Enable SMX --> Enabled
  bios_menu_lib.send_key(device, "KEY_DOWN", 1)
  pass_message_2="Intel.*Disabled"
  pass_message_3="VMX.*Enable"
  pass_message_4="SMX.*Enable"
  match2=deviceObj.read_until_regexp(pass_message_2, timeout=20)
  match3=deviceObj.read_until_regexp(pass_message_3, timeout=20)
  match4=deviceObj.read_until_regexp(pass_message_4, timeout=20)
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC")            #key_strokes_to_reach_Socket Configuration
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_DOWN", 4)
  bios_menu_lib.send_key(device, "KEY_ENTER")          #IIO Configuration
  bios_menu_lib.send_key(device, "KEY_DOWN", 4)        #Intel. VT for Directed I/O (VT-d)
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)       #Intel. VT for Directed I/O           [Enable]
  bios_menu_lib.send_key(device, "KEY_DOWN", 1)
  pass_message_5="VT.*Enable"
  match5=deviceObj.read_until_regexp(pass_message_5, timeout=20)
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC")
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC")            #key_strokes_to_reach_Socket Configuration_menu
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_UP", 4)
  bios_menu_lib.send_key(device, "KEY_ENTER")          #key_strokes_to_reach_Processor Configuration
  bios_menu_lib.send_key(device, "KEY_UP", 13)
  bios_menu_lib.send_key(device, "KEY_ENTER")
  bios_menu_lib.send_key(device, "KEY_DOWN", 1)
  bios_menu_lib.send_key(device, "KEY_ENTER")          #Enable Intel(R) TXT                  [Enable]
  bios_menu_lib.send_key(device, "KEY_DOWN", 1)
  pass_message_6="Intel.*Enable"
  match6=deviceObj.read_until_regexp(pass_message_6, timeout=20)
  if match1 and match2 and match3 and match4 and match5 and match6:
    log.success(f"SMX, VMX, VT-d Settings are enabled successfully")
  else:
    log.fail(f"SMX, VMX, VT-d Settings are not enabled and failed")
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC")
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_RIGHT", 4)    #key_strokes_to_reach_Save & Exit Menu
  bios_menu_lib.send_key(device, "KEY_DOWN", 3)     #Reset the system after saving
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)    #Save Changes done


def BIOS_BasicTest2_under_UEFI_shell_mode(device,bios_password='c411ie'):
    log.debug('Entering procedure BIOS_BasicTest2_under_UEFI_shell_mode with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    bios_menu_lib.send_key(device, "KEY_RIGHT",7)
    bios_menu_lib.send_key(device, "KEY_UP",2)
    bios_menu_lib.send_key(device, "KEY_ENTER",2)
    deviceObj.read_until_regexp('Shell>', timeout=60)
    CommonLib.send_command("fs1:",promptStr='FS1:\>')
    CommonLib.send_command("ls",promptStr='FS1:\>')
    cmd1 = f"cd \"Server Security Toolkit Ver1.24\""
    cmd2 = f"cd \"CBnTToolkit\""
    cmd3 = f"TxtBtgInfo.efi -c a > before_getsec.txt"
    cmd4 = f"getsec64CBnT.efi -l senter -a"
    cmd5 = f"getsec64CBnT.efi -l sexit"
    log.info(cmd1)
    log.info(cmd2)
    log.info(cmd3)
    log.info(cmd4)
    log.info(cmd5)
    bios_menu_lib.send_str_on_bios(device, cmd1)
    bios_menu_lib.send_str_on_bios(device, cmd2)
    bios_menu_lib.send_str_on_bios(device, cmd3)
    bios_menu_lib.send_str_on_bios(device, cmd4)
    pass_message_1="System is now in TXT Environment"
    match1=deviceObj.read_until_regexp(pass_message_1, timeout=20)
    bios_menu_lib.send_str_on_bios(device, cmd5)
    pass_message_2="System has exited TXT Environment"
    match2=deviceObj.read_until_regexp(pass_message_2, timeout=20)
    if match1 and match2:
      log.success(f"PASSED!! GETSEC[SENTER] complete. System is now in TXT Environment.")
      log.success(f"PASSED!! GETSEC[SEXIT] complete. System has exited TXT Environment.")
    else:
      log.fail(f"FAILED!! Error: SINIT module requires newer MLE version")
      log.fail(f"FAILED!! Error: System is NOT in TXT environment")
      log.fail(f"FAILED!! Demonstrate that a secure launch is not possible")
    CommonLib.send_command("exit")
    bios_menu_lib.exit_bios_1(device)

def Check_DIMMs_GoldConfig_information(device):
  log.debug('Entering procedure Check_DIMMs_information with args : %s\n' % (str(locals())))
  deviceObj = Device.getDeviceObject(device)
  bios_menu_lib.send_key(device, "KEY_RIGHT", 1)   #key_strokes_to_reach_Advanced_menu & Trusted Computing
  bios_menu_lib.send_key(device, "KEY_DOWN", 10)   #key_strokes_to_reach_Intel(R) Optane(TM) Persistent Memory Configuration
  bios_menu_lib.send_key(device, "KEY_ENTER", 1)   #key_strokes_to_reach_Detected PMem modules:
  bios_menu_lib.send_key(device, "KEY_DOWN", 2)   #key_strokes_to_reach_PMem modules
  pass_message_1="Detected PMem modules:.*2"
  match1=deviceObj.read_until_regexp(pass_message_1, timeout=20)
  pass_message_2="All PMem modules are healthy"
  match2=deviceObj.read_until_regexp(pass_message_2, timeout=20)
  bios_menu_lib.send_key(device, "KEY_ENTER",1)   #key_strokes_to_reach_DIMM ID 0x0001
  bios_menu_lib.send_key(device, "KEY_ENTER", 1)    #key_strokes_to_reach_DIMM UID
  bios_menu_lib.send_key(device, "KEY_DOWN", 8)   #key_strokes_to_reach_Firmware API version
  pass_message_3="DIMM UID.*8089-A2-2011-00000E33"
  pass_message_4="DIMM handle"
  pass_message_5="DIMM physical ID"
  pass_message_6="Manageability state.*Manageable"
  pass_message_7="Health state.*Healthy"
  pass_message_8="Health state reason.*None"
  pass_message_9="Capacity.*GiB"
  match3=deviceObj.read_until_regexp(pass_message_3, timeout=20)
  match4=deviceObj.read_until_regexp(pass_message_4, timeout=20)
  match5=deviceObj.read_until_regexp(pass_message_5, timeout=20)
  match6=deviceObj.read_until_regexp(pass_message_6, timeout=20)
  match7=deviceObj.read_until_regexp(pass_message_7, timeout=20)
  match8=deviceObj.read_until_regexp(pass_message_8, timeout=20)
  match9=deviceObj.read_until_regexp(pass_message_9, timeout=20)
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)   #key_strokes_to_reach_DIMM ID 0x0001
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_DOWN",1)    #key_strokes_to_reach_DIMM ID 0x1001
  bios_menu_lib.send_key(device, "KEY_ENTER",1)   #key_strokes_to_reach_DIMM UID
  pass_message_10="DIMM UID.*8089-A2-2011-00000CC4"
  pass_message_11="DIMM handle"
  pass_message_12="DIMM physical ID"
  pass_message_13="Manageability state.*Manageable"
  pass_message_14="Health state.*Healthy"
  pass_message_15="Health state reason.*None"
  pass_message_16="Capacity.*GiB"
  match10=deviceObj.read_until_regexp(pass_message_10, timeout=20)
  match11=deviceObj.read_until_regexp(pass_message_11, timeout=20)
  match12=deviceObj.read_until_regexp(pass_message_12, timeout=20)
  match13=deviceObj.read_until_regexp(pass_message_13, timeout=20)
  match14=deviceObj.read_until_regexp(pass_message_14, timeout=20)
  match15=deviceObj.read_until_regexp(pass_message_15, timeout=20)
  match16=deviceObj.read_until_regexp(pass_message_16, timeout=20)
  if match3 and match10 and pass_message_4 and pass_message_11 and pass_message_5 and pass_message_16:
      log.success(f"PASSED!! no error or any other abnoraml info in DIMM UID/DIMM handle/DIMM physical ID/ Manageability state/Health state/Capacity")
  else:
      log.fail(f"FAILED!! Failed to check DIMM UID/DIMM handle/DIMM physical ID/ Manageability state/Health state/Capacity")

  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)    #key_strokes_to_reach_DIMM ID 0x0001
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)    #key_strokes_to_reach_Detected PMem modules
  time.sleep(5)
  #Intel Optane DC Persistent Memory Configuration -> Provisioning --> Create goal config -->
  bios_menu_lib.send_key(device, "KEY_DOWN", 4)   #key_strokes_to_reach_Provisioning
  bios_menu_lib.send_key(device, "KEY_ENTER", 1)  #key_strokes_to_reach_Create goal config
  bios_menu_lib.send_key(device, "KEY_ENTER", 1)  #key_strokes_to_reach_Create goal config for:        [Platform]
  bios_menu_lib.send_key(device, "KEY_DOWN", 5)   #key_strokes_to_reach_before Create goal config
  pass_message_15="Create goal config for:.*Platform"
  pass_message_16="Reserved.*0"
  pass_message_17="Memory Mode.*0"           #This is mean Appdirect mode is working
  pass_message_18="Persistent memory type.*App Direct"
  pass_message_19="Namespace Label version.*1.2"
  match15=deviceObj.read_until_regexp(pass_message_15, timeout=20)
  match16=deviceObj.read_until_regexp(pass_message_16, timeout=20)
  match17=deviceObj.read_until_regexp(pass_message_17, timeout=20)
  match18=deviceObj.read_until_regexp(pass_message_18, timeout=20)
  match19=deviceObj.read_until_regexp(pass_message_19, timeout=20)
  if match17:
      log.success(f"PASSED!! Appdirect mode is working successfully")
  else:
      log.fail(f"FAILED!! Appdirect mode is working as expected")

  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)    #key_strokes_to_reach_Create goal config
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)    #key_strokes_to_reach_Detected PMem modules
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)    #key_strokes_to_reach_Intel(R) Optane(TM) Persistent Memory Configuration
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_RIGHT", 6)  #key_strokes_to_save_and_exit
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)
  log.debug("Save and Reboot up and Sleeping 150 sec....")
  time.sleep(150)

def Check_Two_Regions_Created_with_Information(device):
  log.debug('Entering procedure Check_Two_Regions_Created_with_Information with args : %s\n' % (str(locals())))
  deviceObj = Device.getDeviceObject(device)
  bios_menu_lib.send_key(device, "KEY_RIGHT",1)   #key_strokes_to_reach_Advanced_menu & Trusted Computing
  bios_menu_lib.send_key(device, "KEY_DOWN",10)   #key_strokes_to_reach_Intel(R) Optane(TM) Persistent Memory Configuration
  bios_menu_lib.send_key(device, "KEY_ENTER",1)   #key_strokes_to_reach_Detected PMem modules:
  bios_menu_lib.send_key(device, "KEY_DOWN",3)    #key_strokes_to_reach_Regions
  bios_menu_lib.send_key(device, "KEY_ENTER",1)   #key_strokes_to_reach_Region ID 1
  bios_menu_lib.send_key(device, "KEY_DOWN",8)   #key_strokes_to_reach_Before-Back to main menu
  time.sleep(5)
  pass_message_1="Region ID 1"
  pass_message_2="Persistent memory type.*App Direct Not"
  pass_message_3="Interleaved"
  pass_message_4="Capacity.*126.000 GiB"
  pass_message_5="Free capacity.*126.000 GiB"
  pass_message_6="Region ID 2"
  pass_message_7="Persistent memory type.*App Direct Not"
  pass_message_8="Interleaved"
  pass_message_9="Capacity.*126.000 GiB"
  pass_message_10="Free capacity.*126.000 GiB"
  match1=deviceObj.read_until_regexp(pass_message_1, timeout=20)
  match2=deviceObj.read_until_regexp(pass_message_2, timeout=20)
  match3=deviceObj.read_until_regexp(pass_message_3, timeout=20)
  match4=deviceObj.read_until_regexp(pass_message_4, timeout=20)
  match5=deviceObj.read_until_regexp(pass_message_5, timeout=20)
  match6=deviceObj.read_until_regexp(pass_message_6, timeout=20)
  match7=deviceObj.read_until_regexp(pass_message_7, timeout=20)
  match8=deviceObj.read_until_regexp(pass_message_8, timeout=20)
  match9=deviceObj.read_until_regexp(pass_message_9, timeout=20)
  match10=deviceObj.read_until_regexp(pass_message_10, timeout=20)
  if match1 and match4 and match6 and match9:
    log.success(f"PASS!! Two Regions are created and each region info shows right")
  else:
    log.fail(f"FAIL!! Two Regions are created and each region info shows right")
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)   #key_strokes_to_reach_Detected PMem modules
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)    #key_strokes_to_reach_Intel(R) Optane(TM) Persistent Memory Configuration
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_RIGHT", 6)  #key_strokes_to_save_and_exit
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)
  log.debug("Save and Reboot up and Sleeping 150 sec....")
  time.sleep(150)

def Check_Namespace_AppDirect_Capacity_Information(device):
  log.debug('Entering procedure Check_Namespace_AppDirect_Capacity_Information with args : %s\n' % (str(locals())))
  deviceObj = Device.getDeviceObject(device)
  bios_menu_lib.send_key(device, "KEY_RIGHT",1)   #key_strokes_to_reach_Advanced_menu & Trusted Computing
  bios_menu_lib.send_key(device, "KEY_DOWN",10)   #key_strokes_to_reach_Intel(R) Optane(TM) Persistent Memory Configuration
  bios_menu_lib.send_key(device, "KEY_ENTER",1)   #key_strokes_to_reach_Detected PMem modules:
  bios_menu_lib.send_key(device, "KEY_DOWN",5)   #key_strokes_to_reach_Namespaces
  bios_menu_lib.send_key(device, "KEY_ENTER",1)   #key_strokes_to_reach_Before-Create namespace
  bios_menu_lib.send_key(device, "KEY_DOWN",1)   #key_strokes_to_reach_Create namespace
  bios_menu_lib.send_key(device, "KEY_ENTER",1)   #key_strokes_to_reach_Name
  bios_menu_lib.send_key(device, "KEY_DOWN",5)   #key_strokes_to_reach_Before-Create namespace
  time.sleep(5)
  pass_message_1="Name"
  pass_message_2="Region ID"
  pass_message_3="Mode.*None"
  pass_message_4="Capacity input.*Remaining"
  pass_message_5="Units.*GiB"
  pass_message_6="Capacity.*126.000"
  match1=deviceObj.read_until_regexp(pass_message_1, timeout=20)
  match2=deviceObj.read_until_regexp(pass_message_2, timeout=20)
  match3=deviceObj.read_until_regexp(pass_message_3, timeout=20)
  match4=deviceObj.read_until_regexp(pass_message_4, timeout=20)
  match5=deviceObj.read_until_regexp(pass_message_5, timeout=20)
  match6=deviceObj.read_until_regexp(pass_message_6, timeout=20)
  if match1 and match2 and match4 and match6:
    log.success(f"PASS!! Namespace Capacity info shows right")
  else:
    log.fail(f"FAIL!! Namespace Capacity info shows right")
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)   #key_strokes_to_reach_Before-Create namespace
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)    #key_strokes_to_Detected PMem modules:
  time.sleep(10)
  bios_menu_lib.send_key(device, "KEY_DOWN",6)   #key_strokes_to_reach_Total capacity
  bios_menu_lib.send_key(device, "KEY_ENTER",1)   #key_strokes_to_reach_Volatile
  bios_menu_lib.send_key(device, "KEY_UP",1)   #key_strokes_to_reach_Back to main menu
  time.sleep(5)
  pass_message_7="Total memory resource allocation across the host server"
  pass_message_8="PMem module Capacities"
  pass_message_9="Volatile:.*0 B"
  pass_message_10="AppDirect:.*252.000 GiB"
  pass_message_11="Inaccessible:.*1.484 GiB"
  pass_message_12="Raw:.*253.484 GiB"
  pass_message_13="DDR Capacities"
  pass_message_14="Volatile:.*1.000 TiB"
  pass_message_15="Cache:.*0 B"
  pass_message_16="Inaccessible:.*0 B"
  pass_message_17="Raw:.*1.000 TiB"
  pass_message_18="Total Memory Capacities"
  pass_message_19="Volatile:.*1.000 TiB"
  pass_message_20="AppDirect:.*252.000 GiB"
  pass_message_21="Cache:.*0 B"
  pass_message_22="Inaccessible:.*1.484 GiB"
  pass_message_23="Raw:.*1.248 TiB"
  match7=deviceObj.read_until_regexp(pass_message_7, timeout=20)
  match8=deviceObj.read_until_regexp(pass_message_8, timeout=20)
  match9=deviceObj.read_until_regexp(pass_message_9, timeout=20)
  match10=deviceObj.read_until_regexp(pass_message_10, timeout=20)
  match11=deviceObj.read_until_regexp(pass_message_11, timeout=20)
  match12=deviceObj.read_until_regexp(pass_message_12, timeout=20)
  match13=deviceObj.read_until_regexp(pass_message_13, timeout=20)
  match14=deviceObj.read_until_regexp(pass_message_14, timeout=20)
  match15=deviceObj.read_until_regexp(pass_message_15, timeout=20)
  match16=deviceObj.read_until_regexp(pass_message_16, timeout=20)
  match17=deviceObj.read_until_regexp(pass_message_17, timeout=20)
  match18=deviceObj.read_until_regexp(pass_message_18, timeout=20)
  match19=deviceObj.read_until_regexp(pass_message_19, timeout=20)
  match20=deviceObj.read_until_regexp(pass_message_20, timeout=20)
  match21=deviceObj.read_until_regexp(pass_message_21, timeout=20)
  match22=deviceObj.read_until_regexp(pass_message_22, timeout=20)
  match23=deviceObj.read_until_regexp(pass_message_23, timeout=20)
  time.sleep(5)
  if match8 and match13 and match18 and match23:
    log.success(f"PASS!! Navigate to Total Capacity page")
    log.success(f"PASS!! Checked App Direct capacity")
    log.success(f"PASS!! Total Memory and Usable Memory in Main Page")
  else:
    log.fail(f"FAIL!! Navigate to Total Capacity page")
    log.fail(f"FAIL!! Checked App Direct capacity")
    log.fail(f"FAIL!! Total Memory and Usable Memory in Main Page")

  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)   #key_strokes_to_reach_Detected PMem modules
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_ESC", 1)    #key_strokes_to_reach_Intel(R) Optane(TM) Persistent Memory Configuration
  time.sleep(5)
  bios_menu_lib.send_key(device, "KEY_LEFT", 1)  #key_strokes_to_reach_Main Menu
  time.sleep(5)
  deviceObj = Device.getDeviceObject(device)
  pass_message_24="Memory Information"
  deviceObj.read_until_regexp(pass_message_24, timeout=60)
  pass_message_25="Total Memory(.*) MB"  #Total Memory                         1306624 MB
  output = deviceObj.read_until_regexp(pass_message_25, timeout=60)

  Total_Memory_match = re.search(pass_message_25, output)
  Total_Memory_match1=Total_Memory_match.group(1).strip()
  if Total_Memory_match:
    log.success(f"BIOS Total Memory :{Total_Memory_match1} MB")
  else:
    log.fail(f"FAIL!! Total Memory is not detected")

  bios_menu_lib.send_key(device, "KEY_RIGHT", 7)  #key_strokes_to_save_and_exit
  bios_menu_lib.send_key(device, "KEY_ENTER", 2)
  log.debug("Save and Reboot up and Sleeping 150 sec....")
  time.sleep(150)
