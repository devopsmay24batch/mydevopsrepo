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
#import SeastoneConst
import Const
import time
import SEASTONECommonLib 
from collections import OrderedDict
import SeastoneDiagVariable as var
from  SEASTONECommonLib import powercycle_device
from SeastoneDiagVariable import * 
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()
#import openbmc
#import openbmc_lib
workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/seastone'))
#from SeastoneCommonVariable import fail_dict
import SeastoneDiagVariable as var
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
    time.sleep(300)


@logThis
def check_diag_basic(device):
    deviceObj = Device.getDeviceObject(device)
    if deviceObj.getPrompt('DIAGOS'):
        print('Diagos is conencted')
    elif deviceObj.getPrompt('OPENBMC'):
        print('BMC is detected')
    else:
        print('Mothing detected')

@logThis
def goToDiagPath():
    path='/home/cel_diag/seastone2v2/bin \r'
    str1= 'cd ' +path
    c1=run_command(str1)
    device.sendMsg('\n')
    if not re.search('rror', c1):
        log.success('Path changed successfully')
    else:
        raise RuntimeError('Path not changed')


@logThis
def checkStorageStress():
    run_command("cd /home/cel_diag/seastone2v2/tools/stress")
    cmd1=run_command("./SSD_test.sh 300 test_SSD.log",timeout= 600)
    cmd1=run_command('cat test_SSD.log')
    if not re.search('rror',cmd1):
        log.success(" Storage test passed")
    else:
        log.fail("Storage  test failed")



@logThis
def checkDdrStress():
    run_command("cd /home/cel_diag/seastone2v2/tools/stress")
    cmd1=run_command('./DDR_test.sh 300 5 DDR_test.log',timeout=600)
    cmd2=run_command('cat DDR_test.log')
    if  re.search('Status: PASS',cmd2):
        log.success(" DDR test passed")
    else:
        log.fail("DDR  test failed")


@logThis
def checkCpuStress():
    patt='0 errors, 0 warnings'
    run_command("cd /home/cel_diag/seastone2v2/tools/stress")
    cmd1=device.sendMsg('./CPU_test.sh \n')
    time.sleep(1200)
    for i in range(3):
        c3=device.sendMsg(Const.KEY_CTRL_C)
        try:
            c5=device.read_until_regexp('root\@localhost*', timeout=3)
            pass_count += 1
            break
        except Exception:
            continue
    device.executeCmd('ls')
    c1=device.executeCmd('cat CPU_test.log')
    if re.search(patt,c1):
        log.success('Stress passed with 0 errors')
    else:
        log.fail('Stress test failed with errors')
    c1=device.executeCmd('rm  CPU_test.log')

@logThis
def changePartition(val):
    run_command('cd')
    cmd1='ipmitool raw 0x32 0x8f 0x01 '+  val
    device.executeCmd(cmd1)


@logThis
def checkActivePartition(val):
    c1=device.executeCmd('ipmitool raw 0x32 0x8f 0x02')
    if val in c1:
        log.success('Active partion is correct')
    else:
        log.fail('Inactive partition')


@logThis
def checkPartition(val):
    m1=device.executeCmd('ipmitool raw 0x32 0x8f 0x07')
    if val in m1:
        log.success(' partition is set correctly')
    else:
        log.fail('Partition is not set')


@logThis
def check_internal_usb(device):
    device = Device.getDeviceObject(device)
    device.executeCmd('ls')
    time.sleep(5)
    c7=device.sendMsg('ipmitool raw 0x32 0xaa 0x00 \r')
    c11=device.read_until_regexp('sbin',timeout=20)
    time.sleep(3)
    c2=device.executeCmd('lsusb')
    time.sleep(2)
    c3=device.executeCmd('ipmitool raw 0x32 0xaa 0x01')
    time.sleep(5)
    print('The value of c7',c7,'############################################',sep='\n')
    print('The value of c2',c2,'############################################',sep='\n')
    print('The value of c3',c3,'############################################',sep='\n')
    print('The value of c11',c11,'############################################',sep='\n')
    for x in internal_usb:
        if x not in c11:
            print(x+' string not matched')
            raise RuntimeError('Internal device test fail')
    log.success('Internal usb test passed')
    



@logThis
def check_external_usb(devic):
    usb_drive='SanDisk Corp|HP'
    goToDiagPath()
    c1=device.executeCmd('lsusb')
    c2=device.executeCmd('./cel-usb-test -w -d 1 -C 10')
    if re.search(usb_drive,c1) and re.search('PASS',c2):
        log.success('Externla USB test passed')
    else:
        raise RuntimeError('External usb test failed')



@logThis
def checkHelp(mod):
    cmd1 = device.executeCmd("./cel-"+mod+"-test -h")
    cmd2= device.executeCmd("./cel-"+mod+"-test --help")
    pattern= "var."+mod+"_help"
    CommonKeywords.should_match_ordered_regexp_list(cmd1,eval(pattern))
    log.success("The ./cel-"+mod+'-test help options are in-line with manual ')
    CommonKeywords.should_match_ordered_regexp_list(cmd2,eval(pattern))
    log.success("The ./cel-"+mod+'-test help options are in-line with manual ')


@logThis
def checkList(mod):
    cmd1 = run_command("./cel-"+mod+"-test -l",prompt ='root@localhost')
    cmd2= run_command("./cel-"+mod+"-test --list",prompt ='root@localhost')
    pattern = "var."+mod+"_list"
    CommonKeywords.should_match_ordered_regexp_list(cmd1,eval(pattern))
    log.success("The ./cel-"+mod+'-test list options are in-line with manual ')
    CommonKeywords.should_match_ordered_regexp_list(cmd2,eval(pattern))
    log.success("The ./cel-"+mod+'-test list options are in-line with manual ')

@logThis
def checkVersion(modul,ver_1):
    goToDiagPath() 
    cmd1 = run_command('./cel-'+modul+'-test -v',prompt ='root@localhost')
    cmd2 = run_command('./cel-'+modul+'-test --version',prompt ='root@localhost')
    if re.search('icpld',modul):
        pattern_1= ['Current DIAG version:.* '+ver_1]
    else:
        pattern_1 =["The.*./cel-"+modul+"-test version.*: "+ str(ver_1)]
    #CommonKeywords.should_match_paired_regexp_list(cmd1, pattern_1)
    log.success("The ./cel-"+modul+'-test version is : '+ str(ver_1))
    CommonKeywords.should_match_paired_regexp_list(cmd2, pattern_1)
    log.success("The ./cel-"+modul+'-test version.*: '+ str(ver_1))



def checkTest(mod):
    goToDiagPath()
    if mod == 'upgrade':
        time.sleep(60)
        cmd1= run_command("./cel-"+mod+"-test --all",prompt='root@localhost',timeout=1860)
        device.executeCmd('rm CPLD.vme*')
        device.executeCmd('rm BMC.ima*')
        device.executeCmd('rm FPGA.bin*')
        device.executeCmd('rm download.sh*')
        device.executeCmd('rm BIOS.bin*')
    else:
        cmd1 = run_command("./cel-"+mod+"-test --all",prompt ='root@localhost',timeout=300)
    if re.search('sfp|rtc|storage',mod):
        mod=''
    if re.search(mod.upper()+".* PASS",cmd1,re.IGNORECASE):
        log.success(mod + " test passed")
    else:
        log.fail(mod+" test failed")



def check_carrera_test(device):
    device= Device.getDeviceObject(device)
    run_command('minicom -D /dev/ttyUSB7')
    #device.read_until_regexp('',timeout=10)
    device.sendMsg('\n')
    run_command('rd_seeprom 2 0x60 0 1 1',prompt='STG ESM B =>')


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
def check_i2c_read_write():
    goToDiagPath()
    str_1='PASS'
    c1=run_command('./cel-i2c-test -r --bus 13 -A 0x50 -R 0x01 -C 1')
    c2=run_command('./cel-i2c-test -w --bus 13 -A 0x50 -R 0x01 -D 0x77 -C 1')
    c3=run_command('./cel-i2c-test -w --bus 13 -A 0x50 -R 0x01  -D 0x88 -C 1')
    c4=run_command('./cel-i2c-test -r --bus 14 -A 0x50 -R 0x01 -C 1')
    m = re.search(str_1,c1) and re.search(str_1,c2) and re.search(str_1,c3) \
        and re.search(str_1,c4)
    if m:
        log.success('I2c read write operations successful')
    else:
        raise RuntimeError('I2c Read/write failed')

@logThis
def enter_into_bios_setup(device):
    log.debug('Entering procedure verify_bios_default_password with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    deviceObj.getPrompt("DIAGOS")
    deviceObj.sendline("")
    deviceObj.sendCmd("reboot")
    time.sleep(60)
    counter = 70
    while counter >= 0:
         bios_menu_lib.send_key(device, "KEY_DEL")
         counter -= 1
         time.sleep(1)



@logThis
def check_qsfp_temp():
    pat1=' QSFP TEST.*PASS'
    c1=device.executeCmd('./cel-qsfp-test -T')
    if not re.search(pat1,c1):
        raise RuntimeError('Qsfp Temp test failed')
    else:
        log.success('QSFP temp test passed')


@logThis
def check_qsfp_power():
    device.executeCmd('cd /home/cel_diag/seastone2v2/tools')
    #device.executeCmd('./hpmode 200 0xC0')
    c3=run_command('./hpmode 0x7f 0xC0',prompt='root@localhost*',timeout=150)
    c1=device.read_until_regexp('#',timeout=160)
    c2=run_command('ls')
    print('The valueof c2',c2)
    if re.search('error|failed',c3):
        raise RuntimeError('QSFP power mode test failed')
    else:
        log.success('QSFP power mode test Passed')



@logThis
def check_rtc_operation():
    cmd1='./cel-rtc-test -w -D ' + new_date
    c1=run_command(cmd1)
    c2=run_command('./cel-rtc-test -r')
    if re.search(current_date,c2):
        log.success('Successfully set the date')
    else:
        raise RuntimeError('Date set failed')
    print('The value of c2',c2)
    print('The value of output,current_date')



@logThis
def check_usb_test():
    str1='PASS'
    device.sendCmd('umount /mnt/')
    time.sleep(2)
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
def check_chassis(devic):
    device=Device.getDeviceObject(devic)
    log.debug('Sending command: ipmitool chassis power cycle')
    device.sendMsg('ipmitool chassis power cycle \r')
    out=device.read_until_regexp('localhost login:*',timeout=400)
    device.loginToDiagOS()


@logThis
def check_bios_reboot(devic,a,b):
    device=Device.getDeviceObject(devic)
    if b == 'Primary':
        key = '01'
    else:
        key = '03'
    device.executeCmd(a)
    device.sendCmd('reboot \r')
    out=device.read_until_regexp('localhost login:',timeout=400)
    device.loginToDiagOS()


    device.executeCmd('ls')
    c2=device.executeCmd('ipmitool raw 0x3a 0x25 0x02')
    time.sleep(2)
    if re.search(key,c2):
        log.success(b + ' BIOS booted successfully')
    else:
        log.fail(b + ' BIOS booted not as expected')



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
        c1='./cel-cpld-test -d '+ str(i) + ' --dump'
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
    c1=device.executeCmd('./cel-cpld-test –b --all')
    c2=device.executeCmd('./cel-cpld-test –b -d 0 --dump')
    if 'FAIL' in c1 or 'FAIL' in c2:
        raise RuntimeError('Cpld Bmc dump failed')
    else:
        log.success('Cpld bmc dump  passed')

@logThis
def check_upgrade_test(a,b,m=1):
    print('The value of m is ',m)
    print('the type of m',type(m))
    if m == 0:
        log.debug('Downloading the sh file for images')
        ki= 'wget ' +  url
        device.executeCmd(ki)
        device.executeCmd('chmod 777 download.sh')
        device.executeCmd('./download.sh')
        time.sleep(30)

    c='.bin'
    if a == 'cpld':
        c='.vme'
    elif a== 'bmc':
        c='.ima'
        time.sleep(100)
    file_1=a.upper()+c
    path= './cel-upgrade-test --update -d '+ b + ' -f ' + ' ' +file_1
    print('The path is ',path)
    out=device.executeCmd(path,timeout=900)
    if re.search('Passed',out,re.IGNORECASE):
        log.success(a.lower() + ' firmware test passed')
    else:
        raise RuntimeError(a.upper() +' firmware test failed')


@logThis
def modify_bmc_Address(device,a):
    devicea = Device.getDeviceObject(device)
    mac='./cel-eeprom-bmc-test -k -t bmc -A b-6 -D  '+ a
    devicea.executeCmd(mac)

@logThis
def check_bmc_mac_address(device,a):
    match_str=a.upper()+'.*login:'
    device = Device.getDeviceObject(device)
    time.sleep(5)
    device.sendMsg('\r')
    device.switchToBmc()
    device.loginToNEWBMC()
    time.sleep(5)

    c1=device.executeCmd('ifconfig')
    log.debug('Sending reboot command and sleep for 400s')
    device.sendMsg('reboot \r')
    out=device.read_until_regexp(match_str,timeout=400)
    device.sendMsg('\r')
    device.loginToNEWBMC()
    log.success('Succesfully Switched BMC')
    c1=device.executeCmd('ifconfig')
    c2=re.search('[A-Fa-f0-9:?]{17}',c1).group()
    c2=''.join(c2.split(':')).lower()
    print('The mac address is ',c2)
    if c2 == a:
        log.success('Mac address changed after reboot')
    else:
        raise RuntimeError('Mac address didnt change after reboot')
    log.debug('Now switch to Come:')
    device.switchToCpu()
    log.success('Successfully switched to CPU')
    run_command('ls')


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
def check_come_mac(device,a):
    device = Device.getDeviceObject(device)
    time.sleep(5)
    c1=device.executeCmd('./cel-mac-test --all')
    c2=re.search('[A-Fa-f0-9:?]{17}',c1).group()
    c2=''.join(c2.split(':')).lower()
    print('The mac address is ',c2)
    if c2 == a:
        log.success('Mac address is correct')
    else:
        raise RuntimeError('Mac address incorrect')


@logThis
def modify_come_mac(devicea,a):
    #device = Device.getDeviceObject(devicea)
    test='./cel-mac-test  --write --dev 1 --data  ' + a
    time.sleep(5)
    c1=device.executeCmd('./cel-mac-test --read  --dev  1')
    c2=device.executeCmd(test)
    time.sleep(10)
    log.debug('Sending reboot and waiting for 300s')
    device.sendMsg('reboot \r')
    out=device.read_until_regexp('localhost login:*',timeout=230)
    device.loginToDiagOS()

    goToDiagPath()
    time.sleep(10)


@logThis
def check_peci_bus():
    c1=device.executeCmd('ipmitool sensor|grep -i temp')
    if not re.search('rror|NOTOK|NOT OK',c1,re.IGNORECASE):
        log.success('PECI test passed')
    else:
        raise RuntimeError('PECI test failed')

@logThis
def check_eeprom_test():
    c1=device.executeCmd(' ./cel-eeprom-test --dump –t tlv –d 1')
    if re.search('PASS',c1):
        log.success('Dump data successful')
    else:
        raise RuntimeError('dump data error')
    c2=device.executeCmd('./cel-eeprom-test -w -A 21 -D seastone')
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

    powercycle_device(devicea)
    time.sleep(5)
    c6=device.executeCmd('dmidecode -t 1')
    if re.search(st1,c6):
        log.success('Eeprom data write retained after reboot')
    else:
        raise RuntimeError('Eeprom write not retained after reboot')


@logThis
def go_to_fru():
    device.executeCmd('cd /home/cel_diag/seastone2v2/firmware/fru_eeprom/')
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
    str_1='BMC I2C Test All.*PASS'
    data1='0x88'
    data2='0x99'
    c1=device.executeCmd('./cel-i2c-test --all -b')
    if re.search(str_1,c1):
        log.success('BMC I2C TEST PASS')
    else:
        raise RuntimeError('BMC I2C TEST FAIL')

    c2=device.executeCmd('./cel-i2c-test -b -w -p /dev/i2c-0 -A 0x0d -R 1 -D 0x88 -C 1')
    c3=device.executeCmd('./cel-i2c-test -b -r -p /dev/i2c-0 -A 0x0d -R 1 -C 1')
    c4=device.executeCmd('./cel-i2c-test -b -w -p /dev/i2c-0 -A 0x0d -R 1 -D 0x99 -C 1')
    c5=device.executeCmd('./cel-i2c-test -b -r -p /dev/i2c-0 -A 0x0d -R 1 -C 1 ')

    if data1 in c3 and data2 in c5:
        log.success('I2c bus operation successfull')
    else:
        raise RuntimeError('I2c bus operation failed')


@logThis
def check_memory_test():
    data_1='Memory list check.*PASS'
    data_2='MEM memtester.*PASS'
    c1=device.executeCmd('./cel-mem-test -a')
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
    c1=device.executeCmd('./cel-fan-test -b --all',timeout=300)
    if re.search('FAIL',c1,re.IGNORECASE):
        raise RuntimeError('Fan test failed')
    else:
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
def check_psu_ipmi(device):
    str1='PASS'
    device_obj = Device.getDeviceObject(device)
    checkTest(psu)
    c1=run_command('./cel-psu-test -s -d 1 -D C')
    c2= run_command('./cel-psu-test -s -d 1 -D V')
    if re.search(str1,c1) and re.search(str1,c2):
        log.success('PSU test passed')
    else:
        raise RuntimeError('PSU  test failed')

