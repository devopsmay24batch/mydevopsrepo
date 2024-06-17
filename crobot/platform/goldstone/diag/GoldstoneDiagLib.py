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
from functools import partial
from Decorator import *
import re
import Logger as log
import CommonLib
import CommonKeywords
#import GoldstoneConst
import Const
import time
import GOLDSTONECommonLib 
from collections import OrderedDict
import GoldstoneDiagVariable as var
from  GOLDSTONECommonLib import powerCycle

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()
workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/goldstone'))
import GoldstoneDiagVariable as var
import bios_menu_lib

devicename = os.environ.get("deviceName", "")
dummymac=DeviceMgr.getDevice(devicename).get('dummyBmcMac')
realmac=DeviceMgr.getDevice(devicename).get('realBmcMac')


run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
time.sleep(10)

@logThis
def ExportEnvPath(cmd_list):
    it = iter(cmd_list)
    while True:
        try:
            device.executeCmd(next(it))
        except StopIteration:
            break

@logThis
def check_reboot(device):
    device=Device.getDeviceObject(device)
    device.sendMsg('reboot \r')
    out=device.read_until_regexp('localhost login:*',timeout=430)
    device.loginToDiagOS()


@logThis
def check_bmc_reboot(device):
    device=Device.getDeviceObject(device)
    device.executeCmd('ipmitool raw 0x06 0x02')
    time.sleep(200)


@logThis
def check_diag_basic(device):
    deviceObj = Device.getDeviceObject(device)
    if deviceObj.getPrompt('DIAGOS'):
        print('Diagos is conencted')
    elif deviceObj.getPrompt('OPENBMC'):
        print('BMC is detected')
    else:
        print('Nothing detected')

@logThis
def diag_installation(image):
    device.executeCmd('cd',timeout=90)
    run_command('rm *')
    wget_cmd = "wget" + var.http_url + var.image_path + image
    wget_op = device.executeCmd(wget_cmd)
    CommonKeywords.should_match_a_regexp(wget_op, "100%")
    
    cmd2=('dpkg -i ' + image)
    cmd3=device.executeCmd(cmd2)
    if not re.search('rror',cmd3):
        log.success('Diag installed successfully')
    else:
        raise RuntimeError('Diag installation have errors')
    

@logThis
def goToDiagPath(subdir='bin'):
    path='/home/cel_diag/goldstone/' + subdir
    str1= 'cd ' +path
    c1=device.executeCmd(str1,timeout=90)
    if not re.search('rror', c1):
        log.success('Path changed successfully')
    else:
        raise RuntimeError('Path not changed')


@logThis
def checkStress(dev):
    cmd1=device.executeCmd('./stressapptest -s 60 -M 28800 -m 4 -i 4 -C 8 -W -d /dev/%s'%dev,timeout=600)
    if  re.search('Status: PASS',cmd1) and re.search('Found 0 hardware incidents',cmd1):
        log.success("Stress test passed")
    else:
        raise RuntimeError("Stress test failed")

@logThis
def checkHelp(mod,mod_help):
    cmd1 = device.executeCmd("./cel-"+mod+"-test -h")
    cmd2= device.executeCmd("./cel-"+mod+"-test --help")
    #pattern= "var."+mod+"_help"
    #CommonKeywords.should_match_ordered_regexp_list(cmd1,eval(pattern))
    for line in mod_help:
        if not re.search(line,cmd1) or not re.search(line,cmd2):
            raise RuntimeError("Check help failed")
    #CommonKeywords.should_match_ordered_regexp_list(cmd2,eval(pattern))
    log.success("The ./cel-"+mod+'-test help options are in-line with manual ')

@logThis
def checkFru(mod,mod_dump):
    cmd1 = device.executeCmd("./cel-"+mod+"-test --dump")
    for line in mod_dump:
        if not re.search(line,cmd1):
            raise RuntimeError("Check dump fru failed")
    log.success("The ./cel-"+mod+'-test dump options are in-line with manual ')

@logThis
def checkList(mod,mod_list):
    cmd1 = run_command("./cel-"+mod+"-test -l",prompt ='root@localhost')
    if mod == 'i2c':
        if re.search('I2C Test All\s+\|\s+PASS\s+|',cmd1):
            log.success("Check list for i2c passed")
            return
        else:
            raise RuntimeError("I2C check list failed")
    cmd2= run_command("./cel-"+mod+"-test --list",prompt ='root@localhost')
    for line in mod_list:
        if not re.search(line,cmd1) or not re.search(line,cmd2):
            raise RuntimeError("Check list failed")
    log.success("The ./cel-"+mod+'-test list options are in-line with manual ')
    device.executeCmd("cd")
    #pattern = "var."+mod+"_list"
    #CommonKeywords.should_match_ordered_regexp_list(cmd1,eval(pattern))
    #log.success("The ./cel-"+mod+'-test list options are in-line with manual ')
    #CommonKeywords.should_match_ordered_regexp_list(cmd2,eval(pattern))
    #log.success("The ./cel-"+mod+'-test list options are in-line with manual ')

@logThis
def checkVersion(modul,ver_1):
    goToDiagPath() 
    cmd1 = run_command('./cel-'+modul+'-test -v',prompt ='root@localhost')
    cmd2 = run_command('./cel-'+modul+'-test --version',prompt ='root@localhost')
    if re.search('pci|cpu|storage',modul):
        pattern_1= ['Current DIAG version:.* '+ver_1]
    else:
        pattern_1 =["The.*./cel-"+modul+"-test version.*: "+ str(ver_1)]
    CommonKeywords.should_match_paired_regexp_list(cmd1, pattern_1)
    log.success("The ./cel-"+modul+'-test version is : '+ str(ver_1))
    CommonKeywords.should_match_paired_regexp_list(cmd2, pattern_1)
    log.success("The ./cel-"+modul+'-test version.*: '+ str(ver_1))


@logThis
def checkTest(mod,argstr='--all'):
    if mod == 'upgrade':
        timeout = 1860
    else:
        timeout=300
    cmd = "./cel-"+mod+"-test " + argstr
    goToDiagPath()
    #cmd1= run_command(cmd,prompt='root@localhost',timeout=timeout)
    cmd1= device.executeCmd(cmd)
    if re.search('rtc|storage',mod):
        mod=''
    if re.search(mod.upper()+".* PASS",cmd1,re.IGNORECASE):
        log.success(mod + " test passed")
    elif mod =='bbcpld' and re.search("BB_CPLD.* PASS",cmd1,re.IGNORECASE):    
        log.success(mod + " test passed")
    elif mod == 'sfp':
        for num in range(1,65):
            if not re.search("OSFP\s+%s\s+Present"%num,cmd1,re.IGNORECASE):
                log.info(mod+" test failed")
                raise RuntimeError("OSFP port %s not present"%num)
        for num in range(1,3):
            if not re.search("SFP+\s+%s\s+Present"%num,cmd1,re.IGNORECASE):
                log.info(mod+" test failed")
                raise RuntimeError("SFP port %s not present"%num)
        log.success(mod + " test passed")

    else:
        log.fail(mod+" test failed")

@logThis
def checkSfpHpmode():
    cmd = "./cel-sfp-test --hpmode"
    cmd1= run_command(cmd,prompt='root@localhost',timeout=300)
    for line in var.sfp_hpmode_list:
        if not re.search(line,cmd1):
            log.fail("pattern %s not found"%line)
    for num in range(1,65):
        if not re.search("Set OSFP_%s\s+disable\s+lpmode"%num,cmd1,re.IGNORECASE):
            log.fail(mod+" test failed")
            raise RuntimeError("High power mode not enabled for port %s"%num)
    log.success("hpmode test passed")


@logThis
def checkSfpLpmode():
    cmd = "./cel-sfp-test --lpmode"
    cmd1= run_command(cmd,prompt='root@localhost',timeout=300)
    for line in var.sfp_lpmode_list:
        if not re.search(line,cmd1):
            log.fail("pattern %s not found"%line)
    for num in range(1,65):
        if not re.search("Set OSFP_%s\s+enable\s+lpmode"%num,cmd1,re.IGNORECASE):
            log.fail(mod+" test failed")
            raise RuntimeError("Low power mode not enabled for port %s"%num)
    log.success("lpmode test passed")

@logThis
def checkBbcpldTest():
    checkTest(var.cpld) 
    checkTest(var.cpld,argstr='--all -x 10') 
    checkTest(var.cpld,argstr='--dev 1') 
    checkTest(var.cpld,argstr='--dev 10') 

@logThis
def checkFpgaTest():
    checkTest(var.fpga) 
    checkTest(var.fpga,argstr='--all -x 10') 
    checkTest(var.fpga,argstr='--dev 1') 
    checkTest(var.fpga,argstr='--dev 9') 


@logThis
def check_the_uart(device):
    log.debug('Entering test procedure that was just created')
    device_obj = Device.getDeviceObject(device)
    time.sleep(5)
    device_obj.switchToBmc()
    device_obj.loginToNEWBMC()
    log.success('Succesfully Switched BMC')
    log.debug('Now switch to Come:')
    device_obj.switchToCpu()
    log.success('Successfully switched to CPU')
    run_command('ls')


@logThis
def check_rtc_operation():
    cmd1='./cel-rtc-test -w -D ' + var.new_date
    c1=run_command(cmd1)
    c2=run_command('./cel-rtc-test -r')
    if re.search(var.current_date,c2):
        log.success('Successfully set the date')
    else:
        raise RuntimeError('Date set failed')
    print('The value of c2',c2)
    print('The value of output,current_date')



@logThis
def check_usb_test():
    str1='PASS'
    device.sendCmd('umount /mnt/')
    c1=run_command('./cel-usb-test --all')
    c2=run_command('./cel-usb-test -w -d 1 -C 10')
    if re.search(str1,c1) and re.search(str1,c2):
        log.success('Usb test passed')
    else:
        raise RuntimeError('USB info test failed')



@logThis
def check_sysinfo_test():
    str1='PASS'
    c1=run_command('./cel-sysinfo-test --all')
    c2=run_command('./cel-sysinfo-test -b --all')
    if re.search(str1,c1) and re.search(str1,c2):
        log.success('Sys info test passed')
    else:
        raise RuntimeError('Sys info test failed')



@logThis
def check_switch(device):
    log.debug('Entering test procedure that was just created')
    device_obj = Device.getDeviceObject(device)
    time.sleep(5)
    device_obj.switchToBmc()



@logThis
def get_mc_info(device):
    device_obj = Device.getDeviceObject(device)
    mgmt_ip = device_obj.managementIP
    cmd='ipmitool -I lanplus -H '+ mgmt_ip + ' -U admin -P admin {}' 

    promptServer=device_obj.promptServer
    print('The value of server is :',promptServer)
    #c1=device_obj.executeCmd(mc_int,mode=promptServer)
    c1=device_obj.executeCmd(cmd.format('sol activate'))
    c2=device_obj.executeCmd('ls')
    c3=device_obj.sendMsg('~.')
    device_obj.sendMsg('\r')
    #c4=device_obj.executeCmd(cmd.format('chassis power off'))
    #time.sleep(3)
    #c5=device_obj.executeCmd(cmd.format('chassis power status'),promptServer,timeout=30)
    #c6=device_obj.executeCmd(cmd.format('sel list'),promptServer,timeout=10)
    #time.sleep(5)
    #c4=device_obj.executeCmd(cmd.format('chassis power on'))
    #log.debug('Sleeping for 180s for bmc to come up')
    #time.sleep(180)
    #c7=device_obj.executeCmd(cmd.format('mc info'))
    #print('The vale of c1',c1)


@logThis
def check_cpld_dump():
    count=0
    for i in range(1,6):
        c1='./cel-bbcpld-test -d '+ str(i) + ' --dump'
        c2=device.executeCmd(c1)
        if 'PASS' not in c2:
            count+=1
    print('The value of count',count)
    if count <=0:
        log.success('Dump passed')
    else:
        raise RuntimeError('Dump failed')

@logThis
def check_cpld_bmc_test():
    c1=device.executeCmd('./cel-bbcpld-test -b --all')
    c2=device.executeCmd('./cel-bbcpld-test -b -d 0 --dump')
    if 'FAIL' in c1 or 'FAIL' in c2:
        raise RuntimeError('Cpld Bmc dump failed')
    else:
        log.success('Cpld bmc dump  passed')

@logThis
def check_upgrade_test(dev,module,image,img_version,devId):
    if module == 'bbcpld':
        module = 'cpld'
    download = "wget http://" + var.tftp_server_ipv4 + ":" + var.image_path + image
    get_img_path = 'cd /home/cel_diag/goldstone/firmware/' + module
    device = Device.getDeviceObject(dev)
    device.executeCmd(get_img_path)
    cmd1 = device.executeCmd(download)
    CommonKeywords.should_match_a_regexp(cmd1, "100%")
    goToDiagPath()
    cmd= './cel-upgrade-test --update -d '+ devId + ' -f ../firmware/'+ module +'/'+ image
    out=device.executeCmd(cmd,timeout=550)
    if re.search('Passed',out,re.IGNORECASE):
        log.success(module + ' firmware upgrade command passed')
    else:
        raise RuntimeError(module +' firmware upgrade command failed')
    powerCycle(dev)
    if devId == '1':
        cmd = device.executeCmd("dmidecode -t bios | grep Version")
        version = re.search('Version:\s+(\S+)\r',cmd).groups()[0]
    if devId == '2':
        cmd = device.executeCmd("/home/cel_diag/goldstone/tools/lpc_cpld_x86_64 blu r 0xA100")
        version = re.search('\n(0x\S+)\r\s+',cmd)
        version = version.groups()[0] 
    if devId == '3':
        cmd = device.executeCmd("cat /sys/devices/platform/cls_sw_fpga/FPGA/version")
        version = re.search('\n(0x\S+)\r\s+',cmd)
        version = version.groups()[0] 
    if img_version == version:
        log.success(module + 'firmware upgrade passed')
    else:
        log.debug("version is %s and img_version is %s"%(version,img_version))
        raise RuntimeError('firmware upgrade failed')


@logThis
def check_bmc_mac(device,a):
    device = Device.getDeviceObject(device)
    time.sleep(5)
    device.sendMsg('\r')
    device.switchToBmc()
    device.loginToNEWBMC()
    c1=device.executeCmd('ifconfig')
    c2=re.search('[A-Fa-f0-9:?]{17}',c1).group()
    c2=''.join(c2.split(':')).lower()
    print('The mac address is ',c2)
    if c2 == a:
        log.success('Mac address is correct')
    else:
        raise RuntimeError('Mac addresss is incorrect')
    log.debug('Now switch to Come:')
    device.switchToCpu()
    log.success('Successfully switched to CPU')
    run_command('ls')
                                                            


@logThis
def check_come_mac(device,mac=None):
    device = Device.getDeviceObject(device)
    time.sleep(5)
    c1=device.executeCmd('ifconfig %s'%device)
    c2=re.search('[A-Fa-f0-9:?]{17}',c1).group()
    c2=''.join(c2.split(':')).lower()
    print('The mac address is ',c2)
    if not mac:
        return c2
    if c2 == a:
        log.success('Mac address is correct')
    else:
        raise RuntimeError('Mac address incorrect')

@logThis
def check_mac_test():
    goToDiagPath(subdir='tools')
    intf = var.mgmt_intf
    output=device.executeCmd('ifconfig %s'%intf)
    init_mac=re.search('ether ([A-Fa-f0-9:?]{17})',output)[1]
    log.info('Mgmt intf mac is %s'%init_mac)
    cmd = './eeupdate64e /NIC=3 /MAC=%s'%var.dummy_mgmt_intf_mac
    output=device.executeCmd(cmd)
    if re.search('Updating Mac Address to %s...Done.'%var.dummy_mgmt_intf_mac,output,re.I) and \
            re.search('Updating Checksum and CRCs...Done.',output):
                log.success('eeupdate64e command success')
    else:
        raise RuntimeError('eeupdate64e command failed')
    check_come_reboot()
    goToDiagPath(subdir='tools')
    output=device.executeCmd('ifconfig %s'%intf)
    mac=re.search('ether ([A-Fa-f0-9:?]{17})',output)[1]
    log.info('Mgmt intf mac is %s'%mac)
    if ''.join(mac.split(':')) == var.dummy_mgmt_intf_mac:
        log.success('Mac address update success')
    else:
        raise RuntimeError('Mac address programming failed')
    cmd = './eeupdate64e /NIC=3 /MAC=%s'%(''.join(init_mac.split(':')))
    output=device.executeCmd(cmd)
    if re.search('Updating Mac Address to %s...Done.'%(''.join(init_mac.split(':'))),output,re.I) and \
            re.search('Updating Checksum and CRCs...Done.',output):
                log.success('eeupdate64e command success')
    else:
        raise RuntimeError('eeupdate64e command failed')
    check_come_reboot()
    goToDiagPath(subdir='tools')
    output=device.executeCmd('ifconfig %s'%intf)
    mac=re.search('ether ([A-Fa-f0-9:?]{17})',output)[1]
    log.info('Mgmt intf mac is %s'%mac)
    if mac == init_mac:
        log.success('Mac address update success')
    else:
        raise RuntimeError('Mac address programming failed')



@logThis
def check_peci_bus():
    c1=device.executeCmd('ipmitool sensor|grep -i temp')
    if not re.search('rror|NOTOK|NOT OK',c1,re.IGNORECASE):
        log.success('PECI test passed')
    else:
        raise RuntimeError('PECI test failed')

@logThis
def eeprom_write_protect(mode='disable'):
    goToDiagPath(subdir='tools')
    if mode=='disable':
        c1=device.executeCmd('./lpc_cpld_x86_64 blu w 0xA131 0x03')
    else:
        pass
    if not re.search('rror|NOTOK|NOT OK',c1,re.IGNORECASE):
        log.success('eeprom write protect %s'% mode)
    else:
        raise RuntimeError('eeprom write protect %s failed'% mode)
    
@logThis
def write_bbcpld_scratch_reg(val='0x55'):
    goToDiagPath(subdir='tools')
    c1=device.executeCmd('./lpc_cpld_x86_64 blu w 0xA101 %s'%val)

@logThis
def check_eeprom_test():
    eeprom_write_protect()
    goToDiagPath()
    c1=device.executeCmd(' ./cel-eeprom-test --dump -t tlv -d 1')
    if re.search('PASS',c1):
        log.success('Dump data successful')
    else:
        raise RuntimeError('dump data error')
    c2=device.executeCmd('./cel-eeprom-test -w -A 21 -D goldstone')
    if not re.search('Error',c2,re.IGNORECASE):
        log.success('Edit TLV succcess')
    else:
        raise RuntimeError('Edit TLV  error')

@logThis
def check_smbios_burn(devicea):
    st1='Manufacturer: Celestica'
    c1=device.executeCmd('./cel-eeprom-test --fru -r')
    c2=device.executeCmd('./cel-eeprom-test --fru --dump')
    c3=device.executeCmd('./cel-eeprom-test --fru --all')
    c4=device.executeCmd('./cel-eeprom-test --fru -w --item \"Chassis Manufacturer\" -D \"Celestica\"')
    c5=device.executeCmd('./cel-eeprom-test --fru --dump')
    m=re.search('PASS',c1) and re.search('PASS',c2) and re.search('PASS',c3) and re.search('PASS',c4) and \
      re.search('PASS',c5)
    if m:
        log.success('Eerpom data dump and write passed')
    else:
        raise RuntimeError('Eeprom dump failed')

    powerCycle(device)
    device.loginToDiagOS()
    time.sleep(5)
    c6=device.executeCmd('dmidecode -t 1')
    if re.search(st1,c6):
        log.success('Eeprom data write retained after reboot')
    else:
        raise RuntimeError('Eeprom write not retained after reboot')


@logThis
def go_to_fru():
    device.executeCmd('cd /diag/home/cel_diag/goldstone/firmware/fru_eeprom/')
    device.executeCmd('./bin_produce.sh')


@logThis
def write_bmc_fru():
    count=0
    write_lst=['./cel-eeprom-bmc-test -w -t bmc',
            './cel-eeprom-bmc-test -w -t come',
            './cel-eeprom-bmc-test -w -t system',
            './cel-eeprom-bmc-test -w -t switch',
            './cel-eeprom-bmc-test -w -t fan1',
            './cel-eeprom-bmc-test -w -t fan2',
            './cel-eeprom-bmc-test -w -t fan3',
            './cel-eeprom-bmc-test -w -t fan4']
    for x in write_lst:
        c1=''
        c1=device.executeCmd(x)
        if not 'Passed' in c1:
            count+=1
    if count > 0:
        raise RuntimeError('BMC FRU write failed')
    else:
        log.success('BMC FRU writepassed')


@logThis
def check_i2c_operation():
    c1=device.executeCmd('./cel-i2c-test --detect')
    if re.search('Detect I2C Bus\s+\|\s+PASS\s+\|',c1):
        log.success('I2C DETECT TEST PASS')
    else:
        raise RuntimeError('I2C DETECT TEST FAIL')

    c2=device.executeCmd('./cel-i2c-test -u --bus 0 -A 0x50')
    c3=device.executeCmd('./cel-i2c-test --dump --bus 1 --addr 0x64')
    if re.search('I2C Dump Test\s+\|\s+PASS\s+\|',c2) and  re.search('I2C Dump Test\s+\|\s+PASS\s+\|',c3):
        log.success('I2C DUMP TEST PASS')
    else:
        raise RuntimeError('I2C DUMP TEST FAIL')
    c4=device.executeCmd('./cel-i2c-test --read --bus 1 --addr  0x64 --reg 0x00')
    c5=device.executeCmd('./cel-i2c-test -r --bus 0 -A 0x50 --reg 0x00')
    if re.search('I2C Read Test\s+\|\s+PASS\s+\|',c4) and re.search('I2C Read Test\s+\|\s+PASS\s+\|',c5):
        log.success('I2C SCAN TEST PASS')
    else:
        raise RuntimeError('I2C SCAN TEST FAIL')
    c6=device.executeCmd('./cel-i2c-test --scan --dev 1',timeout=90)
    if re.search('I2C Scan Bus\s+\|\s+PASS\s+\|',c6):
        log.success('I2C SCAN TEST PASS')
    else:
        raise RuntimeError('I2C SCAN TEST FAIL')


@logThis
def check_memory_test():
    data_1='Memory list check.*PASS'
    data_2='MEM memtester.*PASS'
    c1=device.executeCmd('./cel-mem-test --all')
    if re.search(data_1,c1) and re.search(data_2,c1):
        log.success('MEMORY TEST PASSED')
    else:
        raise RuntimeError('MEMORY TEST FAILED')


@logThis
def check_pci_test():
    str_1='Status = PASS'
    c1=device.executeCmd('./cel-pci-test --all')
    if re.search(str_1,c1):
        log.success('PCI test passed')
    else:
        raise RuntimeError('PCI test failed')


@logThis
def check_phy_test():
        str_1='PHY.*PASS'
        c1=device.executeCmd('./cel-phy-test --all')
        if re.search(str_1,c1,re.IGNORECASE):
            log.success('PHY test passed')
        else:
            raise RuntimeError('PHy test failed')



@logThis
def check_mc_info():
    c1=device.executeCmd('ipmitool mc info')
    CommonKeywords.should_match_ordered_regexp_list(c1,mcinfo)
    log.success('MC info test passed')

@logThis
def check_mgmt_connect():
    str_1='ma1.*UP'
    str_2='0% packet loss'
    c1=device.executeCmd('ifconfig ma1')
    str1='ping '+come_mgmt+ ' -c 3 -w 3'
    c2=device.executeCmd(str1)
    if re.search(str_1,c1) and re.search(str_2,c2):
        log.success('MGMT port is up and pinagable')
    else:
        raise RuntimeError('Mgmt port not up or pingable')

@logThis
def check_the_uart_test(mod):
    cmd1 = run_command("./cel-"+mod+"-test --all",prompt ='#')
    if re.search('passed',cmd1,re.IGNORECASE) and not re.search('failed',cmd1,re.IGNORECASE):
        log.success('UART test passed')
    else:
        raise RuntimeError('UART test failed') 
    cmd1 = device.executeCmd('reset')



@logThis
def check_come_reboot():
    c1=device.executeCmd('ipmitool chassis power cycle')
    out=device.read_until_regexp('localhost login:*',timeout=400)
    device.loginToDiagOS() 




@logThis
def check_sol_Activate(device):
    deviceObj=Device.getDeviceObject(device)
    mgmt_ip = deviceObj.managementIP
    cmd='ipmitool -I lanplus -H '+ mgmt_ip + ' -U admin -P admin sol activate'
    c1=Device.execute_local_cmd(deviceObj, cmd)
    print('The output of c1 \n', c1)
   
    for i in range(6):
        c3=device.sendMsg('~.')
        try:
            c5=deviceObj.read_until_regexp('terminated ipmitool', timeout=3)
            break
        except Exception:
            continue

@logThis
def check_mole():
    c1=device.executeCmd('ipmitool raw 0x32 0xaa 0x00')
    c2=device.executeCmd('lsusb')
    c3=device.executeCmd('ipmitool raw 0x32 0xaa 0x01')

    print('The value of output is ',c1,c2,c3,sep='\n')

@logThis
def check_come_bios(val_1):
    if val_1=='primary':
        flag = '0x00'
        po = '0x41'
    else:
        flag = '0x01'
        po='0x43'
    str_1= 'echo 0x23 '+ po +'  > /sys/devices/platform/mfd_cpld/baseboard_reg_fields.2.auto/setreg'
    device.executeCmd(str_1)
    device.sendMsg('reboot \r')
    out=device.read_until_regexp('localhost login:*',timeout=430)
    device.loginToDiagOS()
    print('The value of out is :##################################',out)
    c2=device.executeCmd('cat /sys/devices/platform/mfd_cpld/baseboard_reg_fields.2.auto/bios_boot_location')
    if flag in c2:
        log.success(val_1 + '  BIOS partition verified')
    else:
        raise RuntimeError(val_1+ '  BIOS partition not expected')
    print('Comparing flag and c2',flag,c2)
  
@logThis
def check_bmc_cpu(device):
    device_obj = Device.getDeviceObject(device)
    time.sleep(10)
    device_obj.switchToBmc()
    device_obj.loginToNEWBMC()
    log.success('Succesfully Switched BMC')

    c1=device_obj.executeCmd('cat /proc/cpuinfo')

    log.debug('Now switch to Come:')
    device_obj.switchToCpu()
    log.success('Successfully switched to CPU')
    run_command('ls')
    CommonKeywords.should_match_ordered_regexp_list(c1,cpu_proc_info)
    log.success('The cpu proc info output is correct')


@logThis
def check_fan_test():
    device.switchToBmc()
    device.loginToNEWBMC()
    device.executeCmd("systemctl stop monitor-fan-system")
    device.switchToCpu()
    c1=device.executeCmd('./cel-fan-test --all')
    device.switchToBmc()
    device.loginToNEWBMC()
    device.executeCmd("systemctl start monitor-fan-system")
    device.switchToCpu()
    if re.search('FAIL',c1,re.IGNORECASE):
        raise RuntimeError('Fan test failed')
    log.success('FAN Test Passed')


@logThis
def check_fan_speed(a,b):
    str_1= './cel-fan-test -b -w -d '+a+ ' -D '+ b
    c1=device.executeCmd(str_1)
    c2=device.executeCmd('./cel-fan-test -b -r -d --all')
    if re.search('FAIL',c2,re.IGNORECASE):
        raise RuntimeError('Fan test failed for  '+b)
    else:
         log.success('FAN Test Passed for speed '+b)


@logThis
def validate_phy(speed,mode):
    read_cmd = './cel-phy-test -r -d 1'
    phy_info=device.executeCmd(read_cmd)
    init_speed = re.search('Speed:\s+(\d+)',phy_info)[1]
    init_mode = re.search('Duplex:\s+(\S+)\s+',phy_info)[1]
    cmd = "./cel-phy-test -w -d 1 --speed %s --duplex %s"%(speed,mode)
    device.executeCmd(cmd)
    time.sleep(5)
    phy_info=device.executeCmd(read_cmd)
    new_speed = re.search('Speed:\s+(\d+)',phy_info)[1]
    new_mode = re.search('Duplex:\s+(\S+)\s+',phy_info)[1]
    cmd = "./cel-phy-test -w -d 1 --speed %s --duplex %s"%(init_speed,init_mode.lower())
    device.executeCmd(cmd)
    time.sleep(5)
    if new_speed == speed and new_mode.lower() == mode.lower():
        log.success("Speed and mode setting passed")
    else:
        raise RuntimeError('Write phy test failed')
    phy_info=device.executeCmd(read_cmd)
    new_speed = re.search('Speed:\s+(\d+)',phy_info)[1]
    new_mode = re.search('Duplex:\s+(\S+)\s+',phy_info)[1]
    if new_speed == init_speed and new_mode.lower() == init_mode.lower():
        log.success("Speed and mode reverted successfully")
    else:
        raise RuntimeError('Setting speed and mode to init values failed ')

