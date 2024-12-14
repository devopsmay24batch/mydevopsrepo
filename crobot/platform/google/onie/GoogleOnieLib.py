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
import os
import sys
import re
import copy
from collections import OrderedDict
import Logger as log
import CRobot
from crobot import Const
from Decorator import *
from time import sleep
from functools import partial
import GoogleOnieVariable as var

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/Google'))
from GoogleOnieVariable import *
import CommonLib
from common.commonlib import CommonKeywords
import GoogleCommonLib
import GoogleConst
from crobot.SwImage import SwImage

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)





def OnieConnect():
    log.debug("Entering OnieTestCase procedure: OnieConnect")
    device.loginOnie()
    return


def OnieDisconnect():
    global libObj
    log.debug("Entering OnieTestCase procedure: OnieDisconnect")
    device.disconnect()
    return

def bootIntoPxeboot():
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    device.sendMsg('reboot \n')
    device.read_until_regexp('.*Hit ',timeout=450)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue

    device.sendCmd("pxeboot \n", '>', timeout=30)


############### Onie related keywords begin


#TCS 16

#########################################################################################
def checkOnieIdle():
    val='0xF000EC59'
    cd_1='devmem $((offset + 0x40)) 32 0x8'
    cd_2='devmem $((offset + 0x40))'
    cd_3='devmem $((offset + 0x4c))'  #0x0009_27C0
    output=device.sendCmd("02",'Please press Enter to activate this console.',timeout=100)
    device.sendMsg("\n")
    device.sendCmd("echo 1 >  /sys/bus/pci/devices/0000:$(lspci | grep -i 1ae0 | cut -d \' \' -f 1)/enable",'ONIE-RECOVERY:')
    #device.sendMsg('offset=\$(awk \'NR==1{print $1}\' /sys/bus/pci/devices/0000:$(lspci | grep -i 1ae0 | cut -d \' \' -f 1)/resource)',prompt='ONIE-RECOVERY:')
    cd1=run_command(cd_1,prompt='ONIE-RECOVERY:')
    cd2=run_command(cd_2,prompt='ONIE-RECOVERY:')
    cd3=run_command(cd_3,prompt='ONIE-RECOVERY:')
    device.sendCmd('onie-stop')
    print("The value of c1", cd1)
    print("The value of c2", cd2)
    print("The value of c3", cd3)
    if re.search(val,cd3):
        log.success("The value is correct")
    else:
        log.fail("Value is not as expected:0xF000EC59")
    time.sleep(43000)
    out= device.read_until_regexp('ONIE-RECOVERY:', timeout=100)
    print('The value of output is',output)
    if not re.search('rror',out):
        log.success('No error encountered')
    else:
        log.fail('Error encountered')
    device.sendCmd('reboot','sonic login',timeout=300)   ###Switching to sonic
                                                                                
##################################################################################################################
#TCS 12

@logThis
def bootToOnieRescueMode():
   #Note : call function bootintopxeboot before this proc to make it work.
   output1=device.sendCmd("02",'Please press Enter to activate this console.',timeout=100)
   output2=device.sendCmd("\n",'#',timeout=120)
   log.info(output1)
   log.info(output2)
   pat='Chosen option rescue'
   pat1="discover: installer mode detected."
   pat2="Installer Mode Enable"
   pat3="ONIE: Starting ONIE Service Discovery"
   if re.search(pat,output1):
        log.success("Successfully selected onie rescue mode")
   else:
        log.fail("could not select onie rescue mode")
        raise RuntimeError("could not select onie rescue mode")
   if re.search(pat1,output1):
        log.success("successfully  Rescue mode detected.  Installer disabled")
   else:
        log.fail(" Rescue mode detected.  Installer disabled check Failed")
        raise RuntimeError(" Rescue mode detected.  Installer disabled check Failed")
   if re.search(pat2,output2):
        log.success("Rescue Mode Enabled check is successful")
   else:
        log.fail("Rescue Mode Enabled check Failed")
        raise RuntimeError("Rescue Mode Enabled check Failed")

@logThis
def bootIntoAutoRescue():
    pat='discover: installer mode detected'
    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")
    if re.search(var.DHCP_IP,c1):
         log.success("IP Assigned Before the Installation Successfull")
    else:
        log.fail("IP Not Assigned Before Installation")
    output_1 = device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=500)
    device.sendCmd("reboot \n",timeout=200)
    output = device.read_until_regexp('sonic login:',timeout=450)

    if re.search(var.menu_02[2],output):
        log.success("Sonic Image is seen in the Menu")
    else:
        log.fail("Sonic Image not seen in the Menu")
    count=0
    for i in var.menu_02:
        if re.search(i,output):
            count+=1
    log.info("The value of count in Sonic Menu:"+str(count))
    if(count==5):
        log.success("Sonic OS Menu Appeared")
        log.success("Installation Done Successfully")
    else:
        log.fail("Sonic OS Menu Failed")

@logThis
def bootIntoRescueMode():
    pat='discover: installer mode detected'
    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")

    if re.search(var.DHCP_IP,c1):
         log.success("DHCP IP Assigned Before the Installation Successfull")
    else:
        log.fail("DHCP IP Not Assigned Before Installation")
    output = device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=500)
    device.sendMsg("\n")
    m1=device.sendCmd(' onie-stop','ONIE-RECOVERY:/ #',timeout=30)
    sleep(30)
    if not re.search(var.onie_stop,m1):
        log.success("Stopping Onie Done Successfully")
    else:
        log.fail("Onie-Stop Failed")

    m2=device.sendCmd('onie-nos-install http://192.168.0.1/onie-installer.bin','ONIE-RECOVERY:/ #',timeout=320)
    sleep(30)
    if not re.search(var.OS_Install,m2):
        log.success("OS Installed Successfully in http Server")
    else:
        log.fail("OS Installed Failed")
    output=device.sendCmd("reboot",'sonic login:',timeout=450)
    if re.search(var.menu_02[2],output):
        log.success("Sonic Image is seen in the Menu")
    else:
        log.fail("Sonic Image not seen in the Menu")

    count=0
    for i in var.menu_02:
        if re.search(i,output):
            count+=1
    if(count==5):
        log.success("Sonic OS Menu Appeared")
        log.success("Installation Done Successfully")
    else:
        log.fail("Sonic OS Menu Failed")


@logThis
def bootIntoRescueVersion():
    pat='discover: installer mode detected'
    #bootIntoPxeboot()
    #device.sendCmd("reboot",'/#',timeout=250)
    #device.sendCmd("pxeboot \n", '>', timeout=30)
    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")

    lower_version="2020.08.0.0.2"
    upper_version="2020.08.0.0.2"

    #bootIntoPxeboot()
    output = device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=500)
    device.sendMsg("\n")
    device.sendCmd(' onie-sysinfo -v','ONIE-RECOVERY:',timeout=5)

    bootIntoEmbed()

    device.sendMsg('reboot \n')
    device.read_until_regexp('.*Hit ',timeout=450)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue

    device.sendCmd("pxeboot \n", '>', timeout=30)
    device.sendCmd("02",timeout=5)

    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")


    m1=device.sendCmd(' onie-stop','ONIE-RECOVERY:/ #',timeout=30)
    device.sendMsg('ping 192.168.0.1 \n')
    sleep(10)
    device.sendMsg(Const.KEY_CTRL_C)
    device.sendMsg("\n")
    if not re.search(var.onie_stop,m1):
        log.success("Stopping Onie Done Successfully")
    else:
        log.fail("Onie-Stop Failed")

    m2=device.sendCmd('onie-nos-install http://192.168.0.1/onie-installer.bin','ONIE-RECOVERY:/ #',timeout=320)
    device.read_until_regexp('.*Hit ',timeout=450)
    if not re.search(var.OS_Install,m2):
        log.success("OS Installed Successfully in http Server")
    else:
        log.fail("OS Installed Failed")

    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue

    device.sendCmd("03",timeout=5)
    device.sendCmd("pxeboot \n", '>', timeout=30)

    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")

    output = device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=500)
    device.sendMsg("\n")

    device.sendCmd(' onie-sysinfo -v','ONIE-RECOVERY:',timeout=5)
    m3=device.read_until_regexp("2020.08.0.0.2",timeout=10)

    if re.search(upper_version,m3):
        log.success("Onie is Upgrade Upper Version")
    m1=device.sendCmd(' onie-stop','ONIE-RECOVERY:/ #',timeout=30)
    device.sendMsg('ping 192.168.0.1 \n')
    sleep(10)
    device.sendMsg(Const.KEY_CTRL_C)
    device.sendMsg("\n")
    if not re.search(var.onie_stop,m1):
        log.success("Stopping Onie Done Successfully")
    else:
        log.fail("Onie-Stop Failed")

    m3=device.sendCmd('onie-nos-install http://192.168.0.1/onie-installer-x86_64.bin','ONIE-RECOVERY:/ #',timeout=320)
    device.read_until_regexp('.*Hit ',timeout=450)
    if not re.search(var.OS_Install,m3):
        log.success("OS Installed Successfully in http Server")
    else:
        log.fail("OS Installed Failed")

    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("03",timeout=5)
    device.sendCmd("pxeboot \n", '>', timeout=30)

    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")

    output = device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=500)
    device.sendMsg("\n")

    device.sendCmd(' onie-sysinfo -v','ONIE-RECOVERY:',timeout=5)
    m1=device.read_until_regexp("2020.08.0.0.2",timeout=10)
    if re.search(lower_version,m1):
        log.success("Onie is in Lower Version")
    device.sendCmd("reboot",'sonic login:',timeout=450)
    #bootIntoPxeboot()


def checkSystemInformation(sysinfo_pat,sysinfo_ver_pat):
    log.debug('Entering procedure checkSystemInformation: %s\n'%(str(locals())))
    device.executeCmd('onie-stop')
    output_sysinfo=device.executeCmd('onie-sysinfo')
    output_sysinfo_ver=device.executeCmd('onie-sysinfo -v')
    if re.search(sysinfo_pat,output_sysinfo):
       log.success("System information check is successful")
    else:
       log.fail("System information check is not successful")
       raise RuntimeError("System information check is not successful")
    if re.search(sysinfo_ver_pat,output_sysinfo_ver):
       log.success("System information version check is successful")
    else:
       log.fail("System information version check is not successful")
       raise RuntimeError("System information version check is not successful")
    checkFdisk()
    checkIfconfig()
    device.sendCmd("reboot",'sonic login',timeout=500)
    device.loginToDiagOS()


@logThis
def checkFdisk():
    cmd1= run_command('fdisk -l\n',prompt='#')
    CommonKeywords.should_match_ordered_regexp_list(cmd1,var.fdisk)


@logThis
def checkIfconfig():
    cmd1= run_command('ifconfig\n',prompt='#')
    CommonKeywords.should_match_ordered_regexp_list(cmd1,var.ifconfig)

##################################################################################################################3
#tcs 09



@logThis
def checkNewOperation():
    c1=run_command('onie-stop',prompt= 'ONIE-RECOVERY:/ #')
    #c1=device.read_until_regexp('ONIE-RECOVERY:/ #',timeout=20)
    print("The value of c1 is ",c1)
    pat = 'Stopping: discover'
    if re.search(pat,c1):
         log.success("Discover stopped")
    else:
         log.fail("Error:Discovery not stopped")
    checkFdisk()
    checkIfconfig()

@logThis
def bootToSonic():
    device.sendCmd('reboot','sonic login',timeout=450)


####################################################################################################################
@logThis
def checkOnieHttp():
    pat='discover: installer mode detected'
    pat1='The operation has completed successfully'
    pat2='Creating new SONiC-OS partition'
    pat3='ONIE: Executing installer: http://192.168.0.1/onie-installer.*bin'
    pat4='Verifying image checksum.*OK'
    pat5='Preparing image archive.*OK'
    pat6='Successfully installed sonic'
    pat7='Writing superblocks and filesystem accounting information.*done'
    pat8='System Reset Type:Warm Reset'

    device.sendCmd('\n')
    time.sleep(30)
    device.sendCmd('ifconfig')
    device.sendCmd('onie-stop')
    c1=device.sendCmd('onie-nos-install http://192.168.0.1/onie-installer.bin \n')
    c2=device.read_until_regexp('Creating journal',timeout=250)
    c3=device.read_until_regexp('sonic login',timeout=500)
    device.loginToDiagOS()

    if re.search(pat,c2) and re.search(pat1,c2) and re.search(pat2,c2):
        log.success('Installation was successful')
    else:
        log.fail('Installation failed')


    if re.search(pat3,c2) and re.search(pat4,c2) and re.search(pat5,c2):
        log.success('Image fetch was successful')
    else:
        log.fail('Image fetch failed')



    if re.search(pat6,c3) and re.search(pat7,c3) and re.search(pat8,c3):
        log.success('System reboot  was successful')
    else:
        log.fail('System reboot failed')

    CommonKeywords.should_match_ordered_regexp_list(c3,var.new_sonic)
##################################################################################################

@logThis
def checkOnieAutoInstall(update="no"):
    #output1=device.sendCmd("02",'Please press Enter to activate this console.',timeout=100)
    if update == 'yes':
        device.executeCmd('echo 1 >  /sys/bus/pci/devices/0000:$(lspci | grep -i 1ae0 | cut -d \' \' -f 1)/enable')
        device.executeCmd("offset=$(awk 'NR==1{print $1}' /sys/bus/pci/devices/0000:$(lspci | grep -i 1ae0 | cut -d \' \' -f 1)/resource)",timeout=10)
        device.executeCmd('devmem $((offset + 0x40)) 32 0x8')
        device.executeCmd('devmem $((offset + 0x40))')
        device.executeCmd('devmem $((offset + 0x4c))  #0x0009_27C0 ')

    pat='The operation has completed successfully'
    pat1='Creating new SONiC-OS partition'
    pat2='Installing SONiC in ONIE'
    c2=device.sendCmd("\n",'#',timeout=10)
    c1=device.read_until_regexp('sonic login',timeout=500)
    if re.search(pat,c1) and re.search(pat1,c1) and re.search(pat2,c1):
        log.success('Installation was successful')
    else:
        log.fail('Installation failed')
    CommonKeywords.should_match_ordered_regexp_list(c1,var.new_sonic)
#############################################################################################

############################################################################################################


@logThis
def checkOnieUninstall():
    device.executeCmd('echo 1 >  /sys/bus/pci/devices/0000:$(lspci | grep -i 1ae0 | cut -d \' \' -f 1)/enable')
    device.executeCmd("offset=$(awk 'NR==1{print $1}' /sys/bus/pci/devices/0000:$(lspci | grep -i 1ae0 | cut -d \' \' -f 1)/resource)",timeout=10)
    device.executeCmd('devmem $((offset + 0x40)) 32 0x8')
    device.executeCmd('devmem $((offset + 0x40))')
    device.executeCmd('devmem $((offset + 0x4c))  #0x0009_27C0 ')
    output=device.sendCmd('onie-uninstaller \n','done',timeout=800)
    pat1="Erasing internal mass storage device"
    pat2="Erase complete."
    pat3="Uninstall complete.  Rebooting"
    if re.search(pat1,output) and re.search(pat2,output) and re.search(pat3,output):
       log.success("Uninstall complete")
    else:
       log.fail("Uninstall Failed")
       raise RuntimeError("Uninstall Failed")
    print('The value of output',output)
    device.read_until_regexp('.*Hit ',timeout=100)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue

    device.sendCmd("pxeboot \n", '>', timeout=30)

    output1=device.sendCmd("02",'Please press Enter to activate this console.',timeout=100)
    output2=device.sendCmd("\n",'#',timeout=10)
    c1=device.read_until_regexp('sonic login',timeout=500)
    device.loginToDiagOS()

#####################################################################################################################
##################################################################################################
@logThis
def testOnie(sysinfo_pat,sysinfo_ver_pat):
    device.executeCmd('onie-stop')
    output_sysinfo=device.executeCmd('onie-sysinfo')
    output_sysinfo_ver=device.executeCmd('onie-sysinfo -v')
    if re.search(sysinfo_pat,output_sysinfo):
       log.success("System information check is successful")
    else:
       log.fail("System information check is not successful")
       raise RuntimeError("System information check is not successful")
    if re.search(sysinfo_ver_pat,output_sysinfo_ver):
       log.success("System information version check is successful")
    else:
       log.fail("System information version check is not successful")
       raise RuntimeError("System information version check is not successful")
    checkFdisk()
    #checkIfconfig()
    device.executeCmd('onie-start')
    out=device.sendCmd('/n','sonic login',timeout=550)
    device.loginToDiagOS()


@logThis
def bootIntoShell():
    c1=device.sendCmd("05",'#',timeout=30)
    c2=device.sendCmd("pxeboot",'>',timeout=120)
    for x in var.linux_menu:
        if not re.search(x,c2):
            log.fail('Linux menu not as per requirement')
    else:
        log.success('Linuxboot menu is as per requirement ')

@logThis
def bootIntoEmbed():
    pat='Chosen option embed.'
    pat1="discover: ONIE embed mode detected"
    pat3="ONIE: Starting ONIE Service Discovery"

    c1=device.sendCmd("01",'Please press Enter to activate this console.',timeout=100)
    c2=device.sendCmd("\n",'#',timeout=120)
    #c3=device.read_until_regexp('Starting: discover',timeout=120)
    if re.search(pat,c1):
        log.success("Successfully selected embed mode")
    else:
        log.fail("could not select embed mode")
        raise RuntimeError("could not select embed mode")
    if re.search(pat1,c1):
        log.success("successfully  Embed mode detected.  Installer disabled")
    else:
        log.fail(" Embed mode failed to detect")
    c4= device.sendCmd("\n",'~/#',timeout=600)
    c5=device.sendCmd("pxeboot \n",'>',timeout=10)
    c6=device.sendCmd('02 \n')
    print('The value of c5:',c5)
    print('The value of c6:',c6)


@logThis
def bootToRescueOnieMode():
   #Note : call function bootintopxeboot before this proc to make it work.
   output1=device.sendCmd("03",'Please press Enter to activate this console.',timeout=100)
   output2=device.sendCmd("\n",'#',timeout=12)
   log.info(output1)
   log.info(output2)
   pat='ONIE: Using DHCPv4 addr: eth1:.*255.255.255.0'
   if re.search(pat,output1):
         log.success("Got ip address from dhcp")
   else:
         log.fail("Failed to get ip")

####################################################################################################################
#tcs 14

@logThis
def checkRebootOnie():
    device.sendMsg('reboot \n')
    device.read_until_regexp('.*Hit ',timeout=450)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>|root.*', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("pxeboot \n", '>', timeout=10)
    c1=device.sendCmd("02",'Please press Enter to activate this console.',timeout=100)
    c2=device.sendCmd("\n",'#',timeout=120)
    device.executeCmd('onie-stop')



#############################################################################################################################
#Tcs05

@logThis
def bootIntoAutoRescue():
    pat='discover: installer mode detected'
    pat1='The operation has completed successfully'
    pat2='Creating new SONiC-OS partition'
    pat3='ONIE: Executing installer: http://192.168.0.1/onie-installer.*bin'
    pat4='Verifying image checksum.*OK'
    pat5='Preparing image archive.*OK'
    pat6='Allocating group tables:.*done'
    pat7='Writing superblocks and filesystem accounting information.*done'
    pat8='System Reset Type:Warm Reset'

    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")
    if re.search(var.DHCP_IP,c1):
         log.success("IP Assigned Before the Installation Successfull")
    else:
        log.fail("IP Not Assigned Before Installation")
    output_1 = device.read_until_regexp('Please press Enter to activate this console', timeout=500)
    c1 = device.read_until_regexp('sonic login:',timeout=450)
    if re.search(pat1,c1) and re.search(pat2,c1):
        log.success('Installation was successful')
    else:
        log.fail('Installation failed')
    if re.search(pat3,c1) and re.search(pat4,c1) and re.search(pat5,c1):
        log.success('Image fetch was successful')
    else:
        log.fail('Image fetch failed')
    if re.search(pat6,c1) and re.search(pat7,c1) and re.search(pat8,c1):
        log.success('System reboot  was successful')
    else:
        log.fail('System reboot failed')



    if re.search(var.menu_02[2],c1):
        log.success("Sonic Image is seen in the Menu")
    else:
        log.fail("Sonic Image not seen in the Menu")
    count=0
    for i in var.menu_02:
        if re.search(i,c1):
            count+=1
    log.info("The value of count in Sonic Menu:"+str(count))
    if(count==5):
        log.success("Sonic OS Menu Appeared")
        log.success("Installation Done Successfully")
    else:
        log.fail("Sonic OS Menu Failed")
##############################################################################################################
#tc06
@logThis
def bootIntoRescueMode():
    pat='discover: installer mode detected'
    pat1='The operation has completed successfully'
    pat2='Creating new SONiC-OS partition'
    pat3='ONIE: Executing installer: http://192.168.0.1/onie-installer.*bin'
    pat4='Verifying image checksum.*OK'
    pat5='Preparing image archive.*OK'
    pat6='Successfully installed sonic'
    pat7='Writing superblocks and filesystem accounting information.*done'
    pat8='System Reset Type:Warm Reset'

    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")

    if re.search(var.DHCP_IP,c1):
         log.success("DHCP IP Assigned Before the Installation Successfull")
    else:
        log.fail("DHCP IP Not Assigned Before Installation")
    output = device.read_until_regexp('Please press Enter to activate this console', timeout=500)
    device.sendMsg("\n")
    time.sleep(30)
    m1=device.sendCmd(' onie-stop','ONIE-RECOVERY:/ #',timeout=30)
    c1=device.sendCmd('onie-nos-install http://192.168.0.1/onie-installer.bin \n')
    c2=device.read_until_regexp('Creating journal',timeout=250)
    c3=device.read_until_regexp('sonic login',timeout=500)
    device.loginToDiagOS()

    if re.search(pat3,c2) and re.search(pat4,c2) and re.search(pat5,c2):
        log.success('Image fetch was successful')
    else:
        log.fail('Image fetch failed')

    if not re.search(var.onie_stop,m1):
        log.success("Stopping Onie Done Successfully")
    else:
        log.fail("Onie-Stop Failed")

    if not re.search(var.OS_Install,c1):
        log.success("OS Installed Successfully in http Server")
    else:
        log.fail("OS Installed Failed")
    if re.search(pat6,c3) and re.search(pat7,c3) and re.search(pat8,c3):
        log.success('System reboot  was successful')
    else:
        log.fail('System reboot failed')

    if re.search(var.menu_02[2],c3):
        log.success("Sonic Image is seen in the Menu")
    else:
        log.fail("Sonic Image not seen in the Menu")

    count=0
    for i in var.menu_02:
        if re.search(i,c3):
            count+=1
    if(count==5):
        log.success("Sonic OS Menu Appeared")
        log.success("Installation Done Successfully")
    else:
        log.fail("Sonic OS Menu Failed")

################################################################################################################3333
