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
import JuniperConst
import Const
import time
from errorsModule import *
from collections import OrderedDict

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/Juniper'))
from JuniperCommonVariable import fail_dict
import JuniperCommonLib
import JuniperDiagLagavulinVariablesLatest as var
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)

@logThis
def verifyDiagToolPath():
    output = run_command("cd /root/Diag/lagavulin")
    outputPath = run_command("pwd") 
    if re.search("/root/Diag/lagavulin", outputPath):
        log.success("Can find the correct diag path")
    else:
        log.fail("Failed to find the diag path")
        raise testFailed("Failed to find the diag path")


@logThis
def checkHelpInfo():
    cmdOutput = run_command('bin/cel-cpu-test -h')
    Patternlist = [ '-l, --list      List the config info.',
            '--all       Test all configure options',
        '-v, --version    Display the version and exit',
        '-h, --help      Display this help text and exit',
        '-r, --readmsr   Read Operation',
        '-w, --writemsr  Write Operation',
        '-n, --cpu       CPU Number',
        '-R, --reg       Register Address',
        '-D, --data      Register value']
    CommonKeywords.should_match_paired_regexp_list(cmdOutput, Patternlist)

@logThis
def checkTheListOfConfigInfo():
    cmdOutput1 = run_command('bin/cel-cpu-test -l')
    cmdOutput2 = run_command('bin/cel-cpu-test --list')
    cmdOutput3 = run_command('bin/cel-cpu-test --all')
    PatternList1 =['stepping 1',
                   'model 15',
                   'family 6',
                   'processor type 0',
                   'extended model 5',
                   'extended family 0',
                   'serial number 0x0000000000000000']
    CommonKeywords.should_match_paired_regexp_list(cmdOutput1, PatternList1)
    CommonKeywords.should_match_paired_regexp_list(cmdOutput2, PatternList1)
    CommonKeywords.should_match_a_regexp(cmdOutput3, "CPU test : Passed")


@logThis
def checktheToolVersion():
    Output1 = run_command('./bin/cel-cpu-test -v')
    Output2 = run_command('./bin/cel-cpu-test --version')
    pattern = "The ./bin/cel-cpu-test version is : 1.0.0"
    CommonKeywords.should_match_a_regexp(Output1, pattern)
    CommonKeywords.should_match_a_regexp(Output2, pattern)

@logThis
def readandWriteRegisterOperation():
    Output1 = run_command('./bin/cel-cpu-test -r -n 0 -R 0x186')
    Output2 = run_command('./bin/cel-cpu-test --readmsr --cpu 0 --reg 0x186')
    run_command('./bin/cel-cpu-test -w -n 0 -R 0x186 -D 0x1')
    Output3 = run_command('./bin/cel-cpu-test -r -n 0 -R 0x186')
    run_command('./bin/cel-cpu-test --writemsr --cpu 0 --reg 0x186 --data 0x0')
    Output4 = run_command('./bin/cel-cpu-test --readmsr --cpu 0 --reg 0x186')
    
    CommonKeywords.should_match_a_regexp(Output1, "0")
    CommonKeywords.should_match_a_regexp(Output2, "0")
    CommonKeywords.should_match_a_regexp(Output3, "1")
    CommonKeywords.should_match_a_regexp(Output3, "0")

@logThis
def  AutochecktheCPUinfo():
    output1 = run_command('dmidecode -t bios')
    output2 = run_command('dmidecode -t system')
    output3 = run_command('dmidecode -t baseboard')
    output4 = run_command('dmidecode -t chassis')
    CommonKeywords.should_match_a_regexp(output1, "BIOS boot specification is supported")
    CommonKeywords.should_match_a_regexp(output2, "No errors detected")
    CommonKeywords.should_match_a_regexp(output3, "Board is a hosting board")
    CommonKeywords.should_match_a_regexp(output4, "Chassis Asset Tag")

@logThis
def cpuLinuxCommand():
    origin_dict = {
            "CPU Cores:" : "(.*?)$",
            "CPU Vendor:" : "(.*?)$",
            }
    linux_dict = {
            "Core(s) per socket:" : "(.*?)$",
            "Vendor ID:" : "(.*?)$",
            }
    origin_output = run_command('./bin/cel-cpu-test --all')
    linux_output = run_command('lscpu')
    linux_result = CommonLib.parseDict(output=linux_output, pattern_dict=linux_dict, sep_field=" ")
    origin_result = CommonLib.parseDict(output=origin_output, pattern_dict=origin_dict, sep_field=" ")
    log.cprint(linux_result)
    log.cprint(origin_result)
    for key, value in origin_result.items():
       if value not in linux_result.values():
           print(linux_result)
           print(key ,  value)
           log.fail("The value of {} is not as expected.".format(key))
           raise testFailed("The value of {} is not as expected.".format(key))

@logThis
def memoryHelpInfo():
    cmdOutput1 = run_command('bin/cel-mem-test -h')
    cmdOutput2 = run_command('bin/cel-mem-test --help')
    Patternlist = ['-r, --read       Read mem data',
        '-w, --write      Use the config to test write',
        '-C, --count      Data count',
        '-W, --width      Data width <8,16,32,64>',
           ' --all        Test all configure options',
        '-v, --version    Display the version and exit',
        '-h, --help       Display this help text and exit']
    CommonKeywords.should_match_paired_regexp_list(cmdOutput1, Patternlist)
    CommonKeywords.should_match_paired_regexp_list(cmdOutput2, Patternlist)

@logThis
def memoryToolVersion():
    Output1 = run_command('bin/cel-mem-test -v')
    Output2 = run_command('bin/cel-mem-test --version')
    pattern = "The bin/cel-mem-test version is : 1.0.0"
    CommonKeywords.should_match_a_regexp(Output1, pattern)
    CommonKeywords.should_match_a_regexp(Output2, pattern)


@logThis
def readWriteDataWidthandCount():
    run_command('bin/cel-mem-test --write --width 8 --count 1')
    Output1 = run_command('bin/cel-mem-test --read --width 8 --count 1')

    run_command('bin/cel-mem-test -w -W 16 -C 1')
    Output2 = run_command('bin/cel-mem-test -r -W 16 -C 1')

    run_command('bin/cel-mem-test -w -W 32 -C 1')
    Output3 = run_command('bin/cel-mem-test -r -W 32 -C 1')

    run_command('bin/cel-mem-test --write --width 64 --count 1')
    Output4 = run_command('bin/cel-mem-test --read --width 64 --count 1')

    CommonKeywords.should_match_a_regexp(Output1, "MEM read: Passed")
    CommonKeywords.should_match_a_regexp(Output2, "MEM read: Passed")
    CommonKeywords.should_match_a_regexp(Output3, "MEM read: Passed")
    CommonKeywords.should_match_a_regexp(Output4, "MEM read: Passed")
@logThis
def i2cListParameter():
    output1=run_command('./bin/cel-i2c-test -l')
    list_pattern=["0*51.*switch_eeprom.*0051",
                  "0*57.*CPU_eeprom.*0057",
                  "0*70.*board_PCA9548_1.*0070",
                  "0*72.*COME_PCA9548.*0072",
                  "0*73.*board_PCA9548.*0073",
                  "0*18.*ddr_tempsensor.*0018",
                  "0*50.*SPD.*0050",
                  "0*56.*PSU_eeprom.*0056",
                  "0*5e.*PSU_control.*005e",
                  "0*49.*swboard_tempsensor.*0049",
                  "0*4a.*swboard_tempsensor.*004a",
                  "0*4c.*swboard_tempsensor.*004c",
                  "0*4d.*swboard_tempsensor.*004d",
#                  "0*71.*uplink_PCA9548.*0071",
                  "0*54.*uplink_eeprom.*0054",
                  "0*50.*QSFP .*0050",
                  "0*36.*CPU_PXE.*0036",
                  "0*3a.*CPU_PXE.*003a",
                  "0*34.*power_monitor.*0034",
                  "0*4e.*cpu_tempsensor.*004e"]
#                  "0*50.*SFP eeprom.*0050"
    #CommonKeywords.should_match_paired_regexp_list(output1,list_pattern)
    pass_count = 0
    fail_count = 0
    cmd = output1
    for param in list_pattern:
        if re.search(param, cmd):
            pass_count += 1
            print("pass:" , param)
        else:
            fail_count += 1
            print("fail:" , param)

    if (pass_count != 0 and fail_count == 0):
        log.success("i2c list test passed")
    elif (fail_count != 0 and passcount != 0):
        log.fail("one of the list parameter failed")
        raise testFailed("one of the list parameter failed")
    elif (pass_count == 0 and fail_count != 0):
        log.fail("Both the i2c list command failed")
        raise testFailed("Both the i2c list command failed")

@logThis
def i2cScanParameter(scan_pattern):
    output=run_command('./bin/cel-i2c-test -s')
    CommonKeywords.should_match_paired_regexp_list(output, scan_pattern)

@logThis
def i2cScanBusParameter(single_scan_bus_pattern):
    output=run_command('./bin/cel-i2c-test -s --bus 1')
    CommonKeywords.should_match_paired_regexp_list(output, single_scan_bus_pattern)

@logThis
def i2cAllParameter():
    output=run_command('./bin/cel-i2c-test --all')
    if re.search("FAILED", output):
        log.fail("i2c 'all' command  have failures")
        raise testFailed("i2c 'all' command  have failures")
    else:
        log.success("i2c 'all' cmd ran successfully")

@logThis
def i2cDumpTestParameter(dump_test_pattern):
    output=run_command('./bin/cel-i2c-test --dump --bus 2 -A 0x56')
    CommonKeywords.should_match_paired_regexp_list(output, dump_test_pattern)

@logThis
def i2cDetectParameter(i2c_detect_pattern):
    output=run_command('./bin/cel-i2c-test --detect')
    #CommonKeywords.should_match_paired_regexp_list(output, i2c_detect_pattern)
    pass_count = 0
    fail_count = 0
    cmd = output
    for param in i2c_detect_pattern:
        if re.search(param, cmd):
            pass_count += 1
            
        else:
            fail_count += 1
            

    if (pass_count != 0 and fail_count == 0):
        log.success("i2c detect test parameter passed")
    elif (fail_count != 0 and pass_count != 0):
        log.fail("one of the detect test parameter failed")
        raise testFailed("one of the detect test parameter failed")
    elif (pass_count == 0 and fail_count != 0):
        log.fail("Both the i2c detect parameter failed")
        raise testFailed("Both the i2c detect parameter failed")

@logThis
def i2c_Read_Write_Parameter():
    output1 = run_command('./bin/cel-i2c-test -r --bus 2 -A 0x56 -R 0x00 -C 1')
    output2 = run_command('./bin/cel-i2c-test --read --bus 2 --addr 0x56 --reg 0x00 --count 1')
    if re.search("rror | Failed | Warning", output1) and re.search("rror | Failed | Warning", output2):
        log.fail("Error in i2c read command")
        raise testFailed("Error in i2c read command")
    else:
        log.success("i2c read cmd ran successfully")
    
    w_output= run_command('./bin/cel-i2c-test -w --bus 2 -A 0x56 -R 0x00 -C 1 -D  0x76')
    r_output= run_command('./bin/cel-i2c-test -r --bus 2 -A 0x56 -R 0x00 -C 1')
    w_pattern=["i2c tool: write val 0 = 0x76"]
    r_pattern=["0x76"]
    CommonKeywords.should_match_paired_regexp_list(w_output, w_pattern)
    CommonKeywords.should_match_paired_regexp_list(r_output, r_pattern)

    w_output=run_command('./bin/cel-i2c-test --write --bus 2 --addr 0x56 --reg 0x00 --count 1 --data 0x77')
    r_output=run_command('./bin/cel-i2c-test --read --bus 2 --addr 0x56 --reg 0x00 --count 1')
    w_pattern=["i2c tool: write val 0 = 0x77"]
    r_pattern=["0x77"]
    CommonKeywords.should_match_paired_regexp_list(w_output, w_pattern)
    CommonKeywords.should_match_paired_regexp_list(r_output, r_pattern)


@logThis
def autoChecktheMemoryInfo():
    Output = run_command('bin/cel-mem-test --all')
    if re.search("Failed", Output):
        log.fail("The Memory info test failed")
        raise testFailed("The Memory info test failed")
    else:
        log.success("The Memory info test passed")

@logThis
def memoryLinuxCmd():
    origin_dict = {
            "Data width" : "(.*?)$",
            "Size" : "(.*?)$",
            "Type" : "(.*?)$",
            "Speed" : "(.*?)$"
            }

    linux_dict = {
            "Data Width" : "(.*?)$",
            "Size" : "(.*?)$",
            "Type" : "(.*?)$",
            "Speed" : "(.*?)$"
            }

    linux_output = run_command('dmidecode -t 17')
    linux_output = linux_output.replace("bits", "")
    linux_output = linux_output.replace("MT/s", "")
    linux_output = linux_output.replace("MB", "")
    log.cprint(linux_output)

    origin_output = run_command('bin/cel-mem-test --all')
    origin_output = origin_output.replace("Passed", "")
    log.cprint(origin_output)
    
    linux_result = CommonLib.parseDict(output=linux_output, pattern_dict=linux_dict, sep_field=":")
    log.cprint(linux_result)
    
    origin_result = CommonLib.parseDict(output=origin_output, pattern_dict=origin_dict, sep_field=":")
    log.cprint(origin_result)
    
    for key, value in origin_result.items():
       if value not in linux_result.values():
           log.fail("The value of {} is not as expected.".format(key))
           raise testFailed("The value of {} is not as expected.".format(key))

@logThis
def verifyToolPath():
    output = run_command("cd /root/Diag/lagavulin/tools")
    outputPath = run_command("pwd")
    if re.search("/root/Diag/lagavulin/tools", outputPath):
        log.success("Can find the correct diag tool path")
    else:
        log.fail("Failed to find the diag tool path")
        raise testFailed("Failed to find the diag tool path")
    return outputPath

@logThis
def verifyI210Adapter():
    output = run_command("./eeupdate64e")
    if re.search("I210", output):
        log.success("Found the I210 adapter")
    else:
        log.fail("I210 adapater not found")
        raise testFailed("I210 adapater not found")

@logThis
def defaultMacAddr():
    output = CommonLib.get_mac_address("DUT", "eth0", keyword ='ether')
    defaultMac = output.replace(":" , "")
    print(defaultMac)
    return defaultMac


@logThis
def modifyMacAddr(write_mac=None):
    if not write_mac:
        import random
        random_mac = random.sample("0123456789ABCDEF", 10)
        write_mac = [ random_mac[i] if i%2==1 else random_mac[i] for i in range(len(random_mac)) ]
        write_mac = "".join(write_mac).rstrip("")
        write_mac = '00' + write_mac
        log.info("Setting randome MAC: {}".format(write_mac))

    output = run_command("./eeupdate64e /NIC= 1 /MAC=" + write_mac)
    if re.search("Error", output):
        log.fail("mac is not configured")
        raise testFailed("mac is not configured")
    else:
        log.success("mac is configured")

    device.rebootToDiag()
    verifyToolPath()

    resultout = CommonLib.get_mac_address("DUT", "eth0", keyword ='ether')
    resultout = resultout.replace(":" , "")
    resultout = resultout.upper()
    print("1:" , resultout)
    print("2:" , write_mac)
    if re.search(resultout , write_mac):
        log.success("The modified Mac address is reflected in DUT")
    else:
        log.fail("The modified Mac Address is not refelected in DUT")
        raise testFailed("The modified Mac Address is not refelected in DUT")
    

@logThis
def tpmHelpParameter():
    output1 = run_command('./bin/cel-tpm-test -h')
    output2 = run_command('./bin/cel-tpm-test --help')

    help_pattern = ["--all           Test all configure options",
         "-h, --help          Display this help text and exit",
         "-l, --list          List yaml info"]
    

    CommonKeywords.should_match_paired_regexp_list(output1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(output2, help_pattern)


@logThis
def tpmListParameter():
    output1 = run_command('./bin/cel-tpm-test -l')
    output2 = run_command('./bin/cel-tpm-test --list')
    list_pattern =["name : tpm",
            "get restart command:",
            "get command: tpm2_getcap properties-fixed",
            "tpm vendor: SLB9670"]
    CommonKeywords.should_match_paired_regexp_list(output1, list_pattern)
    CommonKeywords.should_match_paired_regexp_list(output2, list_pattern)

@logThis
def tpmAllParameter():
    output= run_command('./bin/cel-tpm-test --all')
    all_pattern=["tpm match:SLB9670",
            "TPM test : Passed"]
    CommonKeywords.should_match_paired_regexp_list(output, all_pattern)

@logThis
def pciHelpParameter():
    output1 = run_command('./bin/cel-pci-test -h')
    output2 = run_command('./bin/cel-pci-test --help')

    help_pattern = ["-l, --list .* list config",
            "-v, --version .*Display the version and exit",
            "-r, --read .*Read the PCIe Configuration Register",
            "-w, --write .*Write the PCIe Configuration Register",
            "-d, --dev .*the BDF of the device",
            "-R, --reg .*Register address",
            "-W, --width .*The width of data",
            "-D, --data .*The value of data",
            "--all .*Test all configure options",
            "-h, --help .*Display this help text and exit"]
    CommonKeywords.should_match_paired_regexp_list(output1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(output2, help_pattern)

@logThis
def pciAllParameter():
    output = run_command('./bin/cel-pci-test --all')
    all_pattern =["PCIe test : Passed"]
    CommonKeywords.should_match_paired_regexp_list(output, all_pattern)

@logThis
def pciVersionParameter():
    output1 = run_command('./bin/cel-pci-test --version')
    output2 = run_command('./bin/cel-pci-test -v')
    ver_pattern = ["1.0.0"]
    CommonKeywords.should_match_paired_regexp_list(output1, ver_pattern)
    CommonKeywords.should_match_paired_regexp_list(output2, ver_pattern)

@logThis
def pciListParameter():
    output1 = run_command('./bin/cel-pci-test -l')
    output2 = run_command('./bin/cel-pci-test --list')
    list_pattern =["BCM\d+ Switch ASIC", "I210 Gigabit Network Connection"]
    CommonKeywords.should_match_paired_regexp_list(output1, list_pattern)
    pass_count = 0
    fail_count = 0
    cmd = output1
    for param in list_pattern:
        if re.search(param, cmd):
            pass_count += 1
            print("pass:" , param)
        else:
            fail_count += 1
            print("fail:" , param)

    if (pass_count != 0 and fail_count == 0):
        log.success("pci list test passed")
    elif (fail_count != 0 and passcount != 0):
        log.fail("one of the list parameter failed")
        raise testFailed("one of the list parameter failed")
    elif (pass_count == 0 and fail_count != 0):
        log.fail("Both the pci list command failed")
        raise testFailed("Both the pci list command failed")

@logThis
def pciLinuxCommand():
    output2 = run_command('lspci -s 02:00.0 -xxxvvv')
    output3 = run_command('lspci -s 04:00.0 -xxxvvv')
    output1 = run_command('lspci')
    output = run_command('./bin/cel-pci-test --list')
    
    list_pattern =["BCM\d+ Switch ASIC", "I210 Gigabit Network Connection"]
    pattern2 = ["BCM\d+ Switch ASIC", "Switch", "8GT/s"]
    temp_list = list(map(lambda x: str(x[2:]) + '0:\s+\w+\s+.*', list(hex(a) for a in range(0, 16))))
    pattern2.extend(temp_list)
    pattern4 = ["I210 Gigabit Network Connection" , "Eth" , "04:00.0"]
    pattern4.extend(temp_list)

    for item in pattern2: 
        if re.search(item, output2):
            log.success("diag info {} matches with linux command".format(item))
        else:
            log.fail("diag info {} doesnot match with linux command".format(item))
            raise testFailed("diag info {} doesnot match with linux command".format(item))
    
    for item in pattern4:
        if re.search(item, output3):
            log.success("diag info {} matches with linux command".format(item))
        else:
            log.fail("diag info {} doesnot match with linux command".format(item))
            raise testFailed("diag info {} doesnot match with linux command".format(item))

    CommonKeywords.should_match_paired_regexp_list(output1, list_pattern)

@logThis
def pciReadWriteOperation():
    read_output1 = run_command('bin/cel-pci-test -r -d 02:00.0 -R 0x0 -W w')
    read_output2 = run_command('bin/cel-pci-test --read --dev 02:00.0 --reg 0x0 --width w')
    write_output1 = run_command('bin/cel-pci-test -w -d 02:00.0 -R 0x1C -W w -D 0x0')
    read_output3 = run_command('bin/cel-pci-test -r -d 02:00.0 -R 0x1C -W w ')
    write_output2 = run_command('bin/cel-pci-test --write --dev 02:00.0 --reg 0x1C --width w --data 0x1')
    read_output4 = run_command('bin/cel-pci-test --read --dev 02:00.0 --reg 0x1C --width w')
    pattern1= ['0000']
    pattern2=['0001']
    CommonKeywords.should_match_paired_regexp_list(read_output3, pattern1)
    CommonKeywords.should_match_paired_regexp_list(read_output4, pattern2)

    if re.search("Error", write_output1):
        log.fail("write operation with data 0x0 failed")
        raise testFailed("write operation with data 0x0 failed")
        print("write_output1:" , write_output1)
    else:
        log.success("write operation with data 0x0 is successful")

    if re.search("Error", write_output2):
        log.fail("write operation with data 0x1 failed")
        raise testFailed("write operation with data 0x1 failed")
        print("write_output2:" , write_output2)
    else:
        log.success("write operation with data 0x1 is successful")
        

@logThis
def ethHelpParameter():
    outPut1 = run_command('./bin/cel-eth-test -h')
    outPut2 = run_command('./bin/cel-eth-test --help')
    help_pattern = ["-v, --version.*Display the version and exit",
            "-h, --help.*Display this help text and exit" ,
            "-i, --interloop.*Internal loopback test" ,
            "-e, --exterloop.*External loopback test",
            "-S, --speed.* Change speed"]
    CommonKeywords.should_match_paired_regexp_list(outPut1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, help_pattern)

@logThis
def ethVersionParameter():
    output1 = run_command('./bin/cel-eth-test --version')
    output2 = run_command('./bin/cel-eth-test -v')
    ver_pattern = ["The ./bin/cel-eth-test version is : 1.0.0"]
    CommonKeywords.should_match_paired_regexp_list(output1, ver_pattern)
    CommonKeywords.should_match_paired_regexp_list(output2, ver_pattern)

@logThis
def checkRemotePcConnected():
    ip = CommonLib.check_ip_address(Const.DUT, 'eth0','DIAGOS')
    outPut = run_command('ifconfig eth0 {} up'.format(ip))
    if re.search("Error" , outPut):
        log.fail("eth0 ip is not configured")
        raise testFailed("eth0 ip is not configured")
    else:
        log.success("eth0 ip is configured")
    CommonLib.exec_local_ping("192.168.0.1" , 4)

@logThis
def ethSpeedParameter():
    interLoop1 = run_command('./bin/cel-eth-test -p eth0 -i')
    interLoop2 = run_command('./bin/cel-eth-test --port eth0 --interloop')
    getSpeed1 = run_command('./bin/cel-eth-test -p eth0 -g')
    getSpeed2 = run_command('./bin/cel-eth-test --port eth0 --get_speed')
 
    chgSpeed1 = run_command('./bin/cel-eth-test -p eth0 -S 100')
    time.sleep(10)
    getSpeed3 = run_command('./bin/cel-eth-test -p eth0 -g')
  
    chgSpeed2 = run_command('./bin/cel-eth-test --port eth0 --speed 10')
    time.sleep(10)
    getSpeed4 = run_command('./bin/cel-eth-test --port eth0 --get_speed')
   
    chgSpeed3 = run_command('./bin/cel-eth-test -p eth0 -S 1000')
    time.sleep(10)
    getSpeed5 = run_command('./bin/cel-eth-test -p eth0 -g')
   
    interloop = "The test result is PASS"
    if re.search(interloop, interLoop1) and re.search(interloop, interLoop2):
        log.success("interloop parameter passed")
    else:
        log.fail("The interloop parameter  have error")
        raise testFailed("The interloop parameter  have error")

    if re.search("100Mb/s", getSpeed3) and re.search("10Mb/s", getSpeed4) and re.search("1000Mb/s", getSpeed5):
        log.success("Modified speed is returned")
    else:
        log.fail("Modified speed is not set in the get output")
        raise testFailed("Modified speed is not set in the get output")


@logThis
def cpldHelpParameter():
    outPut1 = run_command('./bin/cel-cpld-test --help')
    outPut2 = run_command('./bin/cel-cpld-test -h')
    help_pattern=["-r, --read .*Read the data",
            "-w, --write.*Write the data",
            "-D, --data.*Input data",
            "-d, --dev.*Device id <1 is system cpld,2 is cpu cpld>",
            "-R, --reg.*Register id 1..x",
            "-A, --addr.*Register address",
            "-l, --list.*List yaml config",
            "-V .* Show cpld version",
            "--all.* Test all configure options",
            "-v, --version.*Display the test tool version and exit",
            "-h, --help.*Display this help text and exit"]
    CommonKeywords.should_match_paired_regexp_list(outPut1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, help_pattern)

@logThis
def cpldListParameter():
    outPut1 = run_command('./bin/cel-cpld-test -l')
    outPut2 = run_command('./bin/cel-cpld-test --list')
    list_pattern=["Device: sys_cpld, Reg_num: 48, Dev_path: /sys/devices/platform/sys_cpld",
            "Device: cpu_cpld, Reg_num: 6, Dev_path: /sys/devices/platform/CPU_cpld"]
    for item in list_pattern:
        if re.search(item, outPut1) and re.search(item, outPut2):
            log.success("cpld list parameter test success")
        else:
            log.fail("cpld list parameter test {} failed".format(item))
            raise testFailed("cpld list parameter test {} failed".format(item))
            
        
@logThis
def cpldVersionParameter():
    outPut_1 = run_command('./bin/cel-cpld-test -v')
    outPut_2 = run_command('./bin/cel-cpld-test --version')
    outPut_3 = run_command('./bin/cel-cpld-test -V -d 1')
    outPut_4 = run_command('./bin/cel-cpld-test -V --dev 1')
    outPut_5 = run_command('./bin/cel-cpld-test -V -d 2')
    outPut_6 = run_command('./bin/cel-cpld-test -V --dev 2')

    ver_pattern =["The ./bin/cel-cpld-test version is : .*"]
    sys_cpld_version = CommonLib.get_swinfo_dict("SYS_CPLD").get("newVersion", "NotFound")
    log.debug("sys_cpld:{}".format(sys_cpld_version))

    cpu_cpld_version = CommonLib.get_swinfo_dict("CPU_CPLD").get("newVersion", "NotFound")
    log.debug("cpu_cpld:{}".format(cpu_cpld_version))

    pattern_d1 = ["sys_cpld version is: {}".format(sys_cpld_version)]
    pattern_d2 = ["cpu_cpld version is: {}".format(cpu_cpld_version)]

    outPut = [outPut_1, outPut_2]
    for val in outPut:
        CommonKeywords.should_match_paired_regexp_list(val, ver_pattern)
    outPut = [outPut_3, outPut_4]
    for val in outPut:
        CommonKeywords.should_match_paired_regexp_list(val, pattern_d1)
    outPut = [outPut_5, outPut_6]
    for val in outPut:
        CommonKeywords.should_match_paired_regexp_list(val, pattern_d2)

@logThis
def cpldAllParameter():
    outPut = run_command('./bin/cel-cpld-test --all')
    pattern = ["sys_cpld r/w Passd", "cpu_cpld r/w Passd", "CPLD test : Passed"]
    for val in pattern:
        if re.search(val, outPut):
            log.success("cpld all parameter {} test verified".format(val))
        else:
            log.fail("cpld all parameter {} test failed".format(val))
            raise testFailed("cpld all parameter {} test failed".format(val))

@logThis
def cpldReadWriteDatabyRegisterAddress():
    outPut_1 = run_command('./bin/cel-cpld-test -r -d 1 -A 0x02')
    outPut_2 = run_command('./bin/cel-cpld-test --read --dev 1 --addr 0x02')
    outPut_3 = run_command('./bin/cel-cpld-test -r -d 2 -A 0x02')
    outPut_4 = run_command('./bin/cel-cpld-test --read --dev 2 --addr 0x02')

    writeSys_1 = run_command('./bin/cel-cpld-test -w -d 1 -A 0x02 -D 0x04')
    readSys_1 = run_command('./bin/cel-cpld-test -r -d 1 -A 0x02')

    writeSys_2 = run_command('./bin/cel-cpld-test --write --dev 1 --addr 0x02 --data 0x03')
    readSys_2 = run_command('./bin/cel-cpld-test --read --dev 1 --addr 0x02')

    writeCpu_1 = run_command('./bin/cel-cpld-test -w -d 2 -A 0x02 -D 0x04')
    readCpu_1 = run_command('./bin/cel-cpld-test -r -d 2 -A 0x02')

    writeCpu_2 = run_command('./bin/cel-cpld-test --write --dev 2 --addr 0x02 --data 0x03')
    readCpu_2 = run_command('./bin/cel-cpld-test --read --dev 2 --addr 0x02')
   
    Pattern = "sys_cpld Reg \\[0x02\\] data: 0x03"
    outPut = [outPut_1, outPut_2]
    pass_count = 0
    for val in outPut:
        if re.search(Pattern, val):
            pass_count +=1
        else:
            log.fail("Sys cpld read operation {} failed".format(val))
            raise testFailed("Sys cpld read operation {} failed".format(val))
    if (pass_count == 2):
        log.success("Sys cpld read operation is success")
   
    Pattern = "cpu_cpld Reg \\[0x02\\] data: 0x03"
    outPut = [outPut_3, outPut_4]
    pass_count = 0
    for val in outPut:
        if re.search(Pattern, val):
            pass_count +=1
        else:
            log.fail("cpu cpld read operation {} failed".format(val))
            raise testFailed("cpu cpld read operation {} failed".format(val))
    if (pass_count == 2):
        log.success("cpu cpld read operation is success")

    if re.search("sys_cpld write reg: 0x02 0x04", writeSys_1):
        log.success("Sys cpld data \'0x04\' write opration by register addr is success")
    else:
        log.fail("Sys cpld data \'0x04\' write opration by register addr is failed")
        raise testFailed("Sys cpld data \'0x04\' write opration by register addr is failed")
    
    if re.search("sys_cpld write reg: 0x02 0x03", writeSys_2):
        log.success("Sys cpld data \'0x03\' write opration by register addr is success")
    else:
        log.fail("Sys cpld data \'0x03\' write opration by register addr is failed")
        raise testFailed("Sys cpld data \'0x03\' write opration by register addr is failed")
    
    if re.search("cpu_cpld write reg: 0x02 0x04", writeCpu_1):
        log.success("Cpu cpld data \'0x04\' write opration by register addr is success")
    else:
        log.fail("Cpu cpld data \'0x04\' write opration by register addr is failed")
        raise testFailed("Cpu cpld data \'0x04\' write opration by register addr is failed")
    
    if re.search("cpu_cpld write reg: 0x02 0x03", writeCpu_2):
        log.success("Cpu cpld data \'0x03\' write opration by register addr is success")
    else:
        log.fail("Cpu cpld data \'0x03\' write opration by register addr is failed")
        raise testFailed("Cpu cpld data \'0x03\' write opration by register addr is failed")

    if re.search("sys_cpld Reg \\[0x02\\] data: 0x04", readSys_1):
        log.success("Sys cpld data \'0x04\' read opration by register addr is success")
    else:
        log.fail("Sys cpld data \'0x04\' read opration by register addr is failed")
        raise testFailed("Sys cpld data \'0x04\' read opration by register addr is failed")
    
    if re.search("sys_cpld Reg \\[0x02\\] data: 0x03", readSys_2):
        log.success("Sys cpld data \'0x03\' read opration by register addr is success")
    else:
        log.fail("Sys cpld data \'0x03\' read opration by register addr is failed")
        raise testFailed("Sys cpld data \'0x03\' read opration by register addr is failed")
    
    if re.search("cpu_cpld Reg \\[0x02\\] data: 0x04", readCpu_1):
        log.success("Cpu cpld data \'0x04\' read opration by register addr is success")
    else:
        log.fail("Cpu cpld data \'0x04\' read opration by register addr is failed")
        raise testFailed("Cpu cpld data \'0x04\' read opration by register addr is failed")
    
    if re.search("cpu_cpld Reg \\[0x02\\] data: 0x03", readCpu_2):
        log.success("Cpu cpld data \'0x03\' read opration by register addr is success")
    else:
        log.fail("Cpu cpld data \'0x03\' read opration by register addr is failed")
        raise testFailed("Cpu cpld data \'0x03\' read opration by register addr is failed")


@logThis
def cpldReadWriteDatabyRegisterId():
    outPut_1 = run_command('./bin/cel-cpld-test -r -d 1 -R 44')
    outPut_2 = run_command('./bin/cel-cpld-test --read --dev 1 --reg 44')
    
    Pattern = "sys_cpld Reg \\[Software_Scratch:0x02\\] data: 0x03"
    for item in [outPut_1, outPut_2]:
        if re.search(Pattern, item):
            log.success("read operation is success for the command{}".format(item))
        else:
            log.fail("read operation is failed for the command{}".format(item))
            raise testFailed("read operation is failed for the command{}".format(item))

    write_1 = run_command('./bin/cel-cpld-test -w -d 1 -R 44 -D 0xdd')
    read_1 = run_command('./bin/cel-cpld-test -r -d 1 -R 44')
    if re.search("sys_cpld write Reg Software_Scratch: 0x02 0xdd", write_1):
        log.success("write operation for data 0xdd is success")
    else:
        log.fail("write operation for data 0xdd is failed")
        raise testFailed("write operation for data 0xdd is failed")

    if re.search("sys_cpld Reg \\[Software_Scratch:0x02\\] data: 0xdd", read_1):
        log.success("read operation for data 0xdd is success")
    else:
        log.fail("read operation for data 0xdd is failed")
        raise testFailed("read operation for data 0xdd is failed")

    write_2 = run_command('./bin/cel-cpld-test --write --dev 1 --reg 44 --data 0x03')
    read_2 = run_command('./bin/cel-cpld-test --read --dev 1 --reg 44')

    if re.search("sys_cpld write Reg Software_Scratch: 0x02 0x03", write_2):
        log.success("write operation for data 0x03 is success")
    else:
        log.fail("write operation for data 0x03 is failed")
        raise testFailed("write operation for data 0x03 is failed")

    if re.search("sys_cpld Reg \\[Software_Scratch:0x02\\] data: 0x03", read_2):
        log.success("read operation for data 0x03 is success")
    else:
        log.fail("read operation for data 0x03 is failed")
        raise testFailed("read operation for data 0x03 is failed")


@logThis
def rtcHelpParameter():
    outPut1 = run_command('./bin/cel-rtc-test --help')
    outPut2 = run_command('./bin/cel-rtc-test -h')
    help_pattern =["-r, --read.*Read rtc data",
            "-w, --write.*Use the config to test write",
            "-D, --data.*Input the date and time '20181231 235959'",
            "--all.*Test all configure options",
            "-v, --version.*Display the version and exit",
            "-h, --help.*Display this help text and exit"]
    CommonKeywords.should_match_paired_regexp_list(outPut1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, help_pattern)

@logThis
def rtcVersionParameter():
    outPut1 = run_command('./bin/cel-rtc-test -v')
    outPut2 = run_command('./bin/cel-rtc-test --version')
    ver_pattern = ["The ./bin/cel-rtc-test version is : 1.0.0"]
    CommonKeywords.should_match_paired_regexp_list(outPut1, ver_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, ver_pattern)

@logThis
def setandReadRtcTime():
    from datetime import datetime
    now = datetime.now()
    date_time = now.strftime("'%Y%m%d %H%M%S'")
    read_time = now.strftime("%Y-%m-%d %H:%M")
    log.debug("Time:{}".format(date_time))
    #read rtc before set
    r_output1=run_command('./bin/cel-rtc-test -r')
    r_output2=run_command('./bin/cel-rtc-test --read')
    if re.search("Error" , r_output1) and re.search("Error" , r_output2):
        log.fail("error in reading date-time")
        raise testFailed("error in reading date-time")
    else:
        log.success("reading date-time before setting it, is successful")

    write_1 = run_command("./bin/cel-rtc-test -w -D '20191118 110310'")
    read_1 = run_command('./bin/cel-rtc-test -r')
    if re.search("Error" , write_1):
        log.fail("error in setting date-time")
        raise testFailed("error in setting date-time")
    else:
        log.success("setting date-time is successful")

    if re.search("2019-11-18 11:03", read_1):
        log.success("reading date-time is successful")
    else:
        log.fail("Error in reading date-time")
        raise testFailed("Error in reading date-time")

    write_2 = run_command("./bin/cel-rtc-test --write --data {}".format(date_time))
    read_2 = run_command("./bin/cel-rtc-test --read")
    if re.search("Error", write_2):
        log.fail("error in setting current date-time")
        raise testFailed("error in setting current date-time")
    else:
        log.success("setting current date-time is successful")
    if re.search(read_time, read_2):
        log.success("reading current date-time is successful")
    else:
        log.fail("Error in reading current date-time")
        raise testFailed("Error in reading current date-time")

@logThis
def pwmonHelpParameter():
    outPut1 = run_command('./bin/cel-pwmon-test -h')
    outPut2 = run_command('./bin/cel-pwmon-test --help')
    help_pattern =[ "-a, --all.*Test all configure options",
            "-v, --version.*Display the version and exit",
            "-h, --help.*Display this help text and exit",
            "-l, --list.*List yaml info",
            "-d, --dev.*[dev id such as 0.1..x]",
            "-c, --channel.*[channel id such as 0.1..x]",
            "-r, --read.*read operation",
            "-g, --get.*Get the margin property",
            "-s, --set.*Set the margin property",
            "-V, --image_version Get the version of the image of power monitor module"]

    CommonKeywords.should_match_paired_regexp_list(outPut1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, help_pattern)

@logThis
def pwmonVersionParameter():
    outPut1 = run_command('./bin/cel-pwmon-test -v')
    outPut2 = run_command('./bin/cel-pwmon-test --version')
    outPut_1 = run_command('./bin/cel-pwmon-test -d 1 -V')
    outPut_2 = run_command('./bin/cel-pwmon-test --dev 1 --image_version')
    outPut_3 = run_command('./bin/cel-pwmon-test -d 2 -V')
    outPut_4 = run_command('./bin/cel-pwmon-test --dev 2 --image_version')

    ver_pattern =["The ./bin/cel-pwmon-test version is : .*"]
    pattern_d1 = ["ucd90120_sys image version : .*"]
    pattern_d2 = ["ucd90120_cpu image version : .*"]

    outPut = [outPut1, outPut2]
    for val in outPut:
        CommonKeywords.should_match_paired_regexp_list(val, ver_pattern)
    outPut = [outPut_1, outPut_2]
    for val in outPut:
        CommonKeywords.should_match_paired_regexp_list(val, pattern_d1)
    outPut = [outPut_3, outPut_4]
    for val in outPut:
        CommonKeywords.should_match_paired_regexp_list(val, pattern_d2)

@logThis
def getPlatformType():
    verifyToolPath()
    outPut = run_command('./eeprom -p /sys/bus/i2c/devices/0-0051/eeprom -d 1')
    if re.search("model_number.*48F|model_number.*48T|model_number.*48P|model_number.*24T|model_number.*24P", outPut):
            log.success("DUT is 48F/48T/24T/48P/24P chipset")
            return "1"
    else:
        log.success("DUT is 24MP/48MP chipset")
        return "2"

@logThis
def pwmonListandAllParameter():
    outPut_list = run_command('./bin/cel-pwmon-test -l')
    outPut = run_command('./bin/cel-pwmon-test --list')
    outPut_all = run_command('./bin/cel-pwmon-test --all')
    val =getPlatformType()
    verifyDiagToolPath()
    chl_num = 11
    if re.search("dev_1 chl: 12", outPut):
        chl_num = 12
    list_pattern1 = ["dev_1 name: ucd90120_sys", "dev_1 path: /dev/", "dev_1 type: PWMON", "dev_1 margin_cpld_id: 1",
                     "dev_1 margin_control_register: 43", "dev_1 margin_control_normal: 0x0",
                     "dev_1 margin_control_high: 0x12",
                     "dev_1 margin_control_low: 0x11"]
    temp_line = 'dev_1 chl: ' + str(chl_num)
    list_pattern1.append(temp_line)
    list_pattern2 = ["dev_2 name: ucd90120_cpu", "dev_2 path: /dev/", "dev_2 type: PWMON", "dev_2 margin_cpld_id: 2",
                     "dev_2 margin_control_register: 4", "dev_2 margin_control_normal: 0x0",
                     "dev_2 margin_control_high: 0x3",
                     "dev_2 margin_control_low: 0x2", "dev_2 chl: 12"]

    for j in range(1, 3):
        if j == 2:
            chl_num = 12
            list_pattern1.extend(list_pattern2)
        for i in range(1, chl_num+1):
            temp_list = []
            line1 = 'dev_' + str(j) + ' chl_' + str(i) + '\stype:\s.*'
            temp_list.append(line1)
            line2 = 'dev_' + str(j) + ' chl_' + str(i) + '\smax:\s.*'
            temp_list.append(line2)
            line3 = 'dev_' + str(j) + ' chl_' + str(i) + '\smin:\s.*'
            temp_list.append(line3)
            line4 = 'dev_' + str(j) + ' chl_' + str(i) + '\svalue:\s.*'
            temp_list.append(line4)
            list_pattern1.extend(temp_list)
    pass_count1 = 0
    pass_count2 = 0
    for line in outPut_list.splitlines():
        for pattern in list_pattern1:
            if re.search(pattern, line):
                pass_count1 += 1

    for line in outPut.splitlines():
        for pattern in list_pattern1:
            if re.search(pattern, line):
                pass_count2 += 1
    if pass_count1 == pass_count2 == len(list_pattern1):
        log.info('get list is PASSED')
    else:
        raise Exception("Find errors when execute")

    if re.search("PWMON test : Passed", outPut_all):
        log.success("power monitor all paramerter verified")
    else:
        log.fail("power monitor all paramerter failed")
        raise testFailed("power monitor all paramerter failed")

@logThis
def pwmonSetandGetMarginValue():
    d1_s1_outPut = run_command('./bin/cel-pwmon-test -d 1 -s high')
    d1_g1_outPut = run_command('./bin/cel-pwmon-test -d 1 -g')
    d1_s2_outPut = run_command('./bin/cel-pwmon-test -d 1 -s low')
    d1_g2_outPut = run_command('./bin/cel-pwmon-test -d 1 -g')
    d1_s3_outPut = run_command('./bin/cel-pwmon-test -d 1 -s normal')
    d1_g3_outPut = run_command('./bin/cel-pwmon-test -d 1 -g')
    d1_S1_outPut = run_command('./bin/cel-pwmon-test --dev 1 --set_margin high')
    d1_G1_outPut = run_command('./bin/cel-pwmon-test --dev 1 --get_margin')
    d1_S2_outPut = run_command('./bin/cel-pwmon-test --dev 1 --set_margin low')
    d1_G2_outPut = run_command('./bin/cel-pwmon-test --dev 1 --get_margin')
    d1_S3_outPut = run_command('./bin/cel-pwmon-test --dev 1 --set_margin normal')
    d1_G3_outPut = run_command('./bin/cel-pwmon-test --dev 1 --get_margin')

    d2_s1_outPut = run_command('./bin/cel-pwmon-test -d 2 -s high')
    d2_g1_outPut = run_command('./bin/cel-pwmon-test -d 2 -g')
    d2_s2_outPut = run_command('./bin/cel-pwmon-test -d 2 -s low')
    d2_g2_outPut = run_command('./bin/cel-pwmon-test -d 2 -g')
    d2_s3_outPut = run_command('./bin/cel-pwmon-test -d 2 -s normal')
    d2_g3_outPut = run_command('./bin/cel-pwmon-test -d 2 -g')
    d2_S1_outPut = run_command('./bin/cel-pwmon-test --dev 2 --set_margin high')
    d2_G1_outPut = run_command('./bin/cel-pwmon-test --dev 2 --get_margin')
    d2_S2_outPut = run_command('./bin/cel-pwmon-test --dev 2 --set_margin low')
    d2_G2_outPut = run_command('./bin/cel-pwmon-test --dev 2 --get_margin')
    d2_S3_outPut = run_command('./bin/cel-pwmon-test --dev 2 --set_margin normal')
    d2_G3_outPut = run_command('./bin/cel-pwmon-test --dev 2 --get_margin')
    high = [d1_g1_outPut, d1_G1_outPut, d2_g1_outPut, d2_G1_outPut]
    low = [d1_g2_outPut, d1_G2_outPut, d2_g2_outPut, d2_G2_outPut]
    normal = [d1_g3_outPut, d1_G3_outPut, d2_g3_outPut, d2_G3_outPut]
    pass_count = 0
    fail_count = 0 
    for val in high:
        if re.search("high", val):
            pass_count += 1
        else:
            fail_count += 1
    if (fail_count == 0):
        log.success("set and get of pwmod margin HIGH is verified")
    else:
        log.fail("set and get of pwmod margin HIGH failed")
        raise testFailed("set and get of pwmod margin HIGH failed")
    pass_count = 0
    fail_count = 0
    for val in low:
        if re.search("low", val):
            pass_count += 1
        else:
            fail_count += 1
    if (fail_count == 0):
        log.success("set and get of pwmod margin LOW is verified")
    else:
        log.fail("set and get of pwmod margin LOW failed")
        raise testFailed("set and get of pwmod margin LOW failed")
    pass_count = 0
    fail_count = 0
    for val in normal:
        if re.search("normal", val):
            pass_count += 1
        else:
            fail_count += 1
    if (fail_count == 0):
        log.success("set and get of pwmod margin NORMAL is verified")
    else:
        log.fail("set and get of pwmod margin NORMAL failed")
        raise testFailed("set and get of pwmod margin NORMAL failed")


@logThis
def pwmonReadtheChannelVoltage():
    outPut_1 = run_command('./bin/cel-pwmon-test -r -d 1 -c 1')
    outPut_2 = run_command('./bin/cel-pwmon-test --read --dev 1 --channel 2')
    outPut_3 = run_command('./bin/cel-pwmon-test -r -d 1 -c 3')
    outPut_4 = run_command('./bin/cel-pwmon-test --read --dev 2 --channel 1')
    outPut_5 = run_command('./bin/cel-pwmon-test -r -d 2 -c 2')
    outPut_6 = run_command('./bin/cel-pwmon-test -r -d 2 -c 3')
    if re.search("3.*", outPut_1):
        log.success("d1 channel 1 voltage read is successful")
    else:
        log.fail("d1 channel 1 voltage read failed")
        raise testFailed("d1 channel 1 voltage read failed")
    if re.search("0.8.*", outPut_2):
        log.success("d1 channel2 voltage read is successful")
    else:
        log.fail("d1 ch2 voltage read failed")
        raise testFailed("d1 ch2 voltage read failed")
    if re.search("1.*", outPut_3):
        log.success("d1 channel3 voltage read is successful")
    else:
        log.fail("d1 ch3 voltage read failed")
        raise testFailed("d1 ch3 voltage read failed")
    if re.search("1.*", outPut_4):
        log.success("d2 ch 1 voltage read is successful")
    else:
        log.fail("d2 ch1 voltage read failed")
        raise testFailed("d2 ch1 voltage read failed")
    if re.search("1.*", outPut_5):
        log.success("d2 ch 2 voltage read is successful")
    else:
        log.fail("d2 ch2 voltage read failed")
        raise testFailed("d2 ch2 voltage read failed")
    if re.search("1.*", outPut_6):
         log.success("d2 ch 3 voltage read is successful")
    else:
        log.fail("d2 ch3 voltage read failed")
        raise testFailed("d2 ch3 voltage read failed")


@logThis
def checkDutSupportSFPtest():
    verifyToolPath()
    outPut = run_command('./eeprom -p /sys/bus/i2c/devices/0-0051/eeprom -d 1')
    if re.search("model_number.*48F", outPut):
            log.success("DUT is 48F variant and support SFP Test")
            return "48F"
    else:
        log.debug("DUT is not 48F variant so skipping the test case")
        return "other"

@logThis
def sfpToolPath():
    outPut = run_command('cd /root/Diag/lagavulin/SDK')
    path = run_command('pwd')
    if re.search("/root/Diag/lagavulin/SDK", path):
        log.success("In the sdk path")
    else:
        log.fail("Not in sdk path")
        raise testFailed("Not in sdk path")

@logThis
def downSFPtest():
    model = checkDutSupportSFPtest()
    sfpToolPath()
    if (model == '48F'):
        outPut = run_command('./auto_load_user.sh -a -d >  ../tools/sfp.log')
        run_command('cd ../tools')
        for port in range(0, 48):
            sfp = run_command('./parse_down_sfp {}'.format(port))
            if (re.search("Port Name:.*", sfp) and re.search("Vendor:.*", sfp) and re.search("Type:.*", sfp) and re.search("Part:.*", sfp)  and re.search("Serial:.*", sfp)):
                log.success("parse down sfp {} ".format(port))
            else:
                log.fail("parse down sfp {} ".format(port))
                raise testFailed('Failure in downsfp test')
            
                

    else:
        log.info("Skipping this test steps since the DUT doesnot support SFP test")



@logThis
def versionHelpParameter():
    outPut1 = run_command('./bin/cel-version-test -h')
    outPut2 = run_command('./bin/cel-version-test --help')
    help_pattern =["-S, --show *Show FW info.",
            "-v, --version *Display the version and exit", 
            "-h, --help *Display this help text and exit"]
    CommonKeywords.should_match_paired_regexp_list(outPut1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, help_pattern)


@logThis
def versionParameter():
    outPut1 = run_command('./bin/cel-version-test -v')
    outPut2 = run_command('./bin/cel-version-test --version')
    ver_pattern = ["The ./bin/cel-version-test version is :.*"]
    CommonKeywords.should_match_paired_regexp_list(outPut1, ver_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, ver_pattern)

@logThis
def versionShowParameter():
    outPut1 = run_command('./bin/cel-version-test -S')
    outPut2 = run_command('./bin/cel-version-test --show')

    Diag_version =  CommonLib.get_swinfo_dict("DIAG").get("newVersion", "NotFound")
    log.debug("Diag_version:{}".format(Diag_version))
    
    CentOS_Version = CommonLib.get_swinfo_dict("OS").get("newVersion", "NotFound")
    log.debug("CentOS_Version:{}".format(CentOS_Version))
    CentOS_Version = CentOS_Version.replace(")", "")
    os = CentOS_Version.split("(")
    os_version = os[-1]
    centos_version = os[0]
    centos_version = centos_version.strip()
    log.debug("CentOS_Version:{}".format(centos_version))
    log.debug("os_version:{}".format(os_version))

    kernal_version = CommonLib.get_swinfo_dict("KERNEL").get("newVersion", "NotFound")
    log.debug("kernal_version:{}".format(kernal_version))
    
    BIOS_Version = CommonLib.get_swinfo_dict("BIOS").get("newVersion", "NotFound")
    log.debug("BIOS_Version:{}".format(BIOS_Version))
    
    sys_cpld_version = CommonLib.get_swinfo_dict("SYS_CPLD").get("newVersion", "NotFound") 
    log.debug("sys_cpld:{}".format(sys_cpld_version))
    
    cpu_cpld_version = CommonLib.get_swinfo_dict("CPU_CPLD").get("newVersion", "NotFound")
    log.debug("cpu_cpld:{}".format(cpu_cpld_version))
    
    I210_version = CommonLib.get_swinfo_dict("I210").get("newVersion", "NotFound")
    log.debug("I210_version:{}".format(I210_version))
    
    sdk_version = CommonLib.get_swinfo_dict("SDK").get("newVersion", "NotFound")
    log.debug("sdk_version:{}".format(sdk_version))
    Image_dict={
            "Diag Version" : Diag_version,
            "CentOS Version" : centos_version,
            "OS Version" : os_version,
            "Kernel Version" : kernal_version,
            "BIOS Version" : BIOS_Version,
            "SYS CPLD Version" : sys_cpld_version,
            "CPU CPLD Version" : cpu_cpld_version,
            "I210 FW Version" : I210_version,
            "SDK Version" : sdk_version
            }
    CommonLib.execute_check_dict('DUT', cmd="", mode=None, patterns_dict=Image_dict, timeout=60, line_mode=True, check_output=outPut1)
    CommonLib.execute_check_dict('DUT', cmd="", mode=None, patterns_dict=Image_dict, timeout=60, line_mode=True, check_output=outPut2)


@logThis
def osVersion():
    Centos_version = run_command('cat /etc/redhat-release')
    Os_version = run_command('cat /etc/product/VERSION')
    linux_version = run_command('cat /proc/version')
    bios_version = run_command('dmidecode -t bios')
    CentOS_Version = CommonLib.get_swinfo_dict("OS").get("newVersion", "NotFound")
    log.debug("CentOS_Version:{}".format(CentOS_Version))
    CentOS_Version = CentOS_Version.replace(")", "")
    os = CentOS_Version.split("(")
    os_version = os[-1]
    centos_version = os[0]
    centos_version = centos_version.strip()
    log.debug("CentOS_Version:{}".format(centos_version))
    log.debug("os_version:{}".format(os_version))

    kernal_version = CommonLib.get_swinfo_dict("KERNEL").get("newVersion", "NotFound")
    log.debug("kernal_version:{}".format(kernal_version))

    BIOS_Version = CommonLib.get_swinfo_dict("BIOS").get("newVersion", "NotFound")
    log.debug("BIOS_Version:{}".format(BIOS_Version))
    if re.search(centos_version, Centos_version) and re.search(os_version, Os_version) and re.search(kernal_version, linux_version) and re.search (BIOS_Version, bios_version):
        log.success("All os version command output contains correct version")
    else:
        log.fail("OS version command output version is not correct")
        raise testFailed("OS version command output version is not correct")


@logThis
def lpcHelpParameter():
    outPut1 = run_command('./bin/cel-lpc-test -h')
    outPut2 = run_command('./bin/cel-lpc-test --help')
    help_pattern = ["-h, --h *Show the help text", 
            "-w, --write *Write operation",
            "-r, --read *Read operation",
            "-C, --count= *Count",
            "-a, --addr= *Address",
            "-V, --val= *Value to be set",
            "-o, --offset= *Register offset to read"]
    CommonKeywords.should_match_paired_regexp_list(outPut1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, help_pattern)

@logThis
def lpcReadwriteOperation():
    outPut_1 = run_command('./bin/cel-lpc-test -r -a 0xfc800000 -o 0x00 -C 2')
    outPut_2 = run_command('./bin/cel-lpc-test --read --addr 0xfc800000 --offset 0x00 --count 2')
    outPut_3 = run_command('./bin/cel-lpc-test -r -a 0xfc800000 -o 0x00 -C 1')
    outPut_4 = run_command('./bin/cel-lpc-test --read --addr 0xfc800000 --offset 0x00 --count 1')
    outPut_5 = run_command('./bin/cel-lpc-test -r -a 0xfc800000 -o 0x01 -C 1')
    outPut_6 = run_command('./bin/cel-lpc-test --read --addr 0xfc800000 --offset 0x01 --count 1')
    outPut_7 = run_command('./bin/cel-lpc-test -r -a 0xfc800000 -o 0x00 -C 5')
    outPut_8 = run_command('./bin/cel-lpc-test --read --addr 0xfc800000 --offset 0x00 --count 5')
    outPut_9 = run_command('./bin/cel-lpc-test -r -a 0xfc800000 -o 0x02 -C 1')
    outPut_10 = run_command('./bin/cel-lpc-test --read --addr 0xfc800000 --offset 0x02 --count 1')
    read = [outPut_1, outPut_2, outPut_3, outPut_4, outPut_5, outPut_6, outPut_7, outPut_8, outPut_9, outPut_10]
    pass_count = 0
    fail_count = 0 
    for item in read:
        if re.search("read lpc passed", item):
            pass_count +=1
        else: 
            fail_count += 1
            failed_item = [item.append]

    if (pass_count == 10):
        log.success("lpc address read operation passed")
    elif (pass_count != 0 and fail_count != 0):
        log.fail("some of lpc read address operation failed:\n{}".format(failed_item))
        raise testFailed("some of lpc read address operation failed:\n{}".format(failed_item))
    elif (fail_count == 10):
        log.fail("All the lpc read address opertaion failed:\n{}".format(failed_item))
        raise testFailed("All the lpc read address opertaion failed:\n{}".format(failed_item))


    outPut1 = run_command('./bin/cel-lpc-test -w -a 0xfc800000 -o 0x02 -C 1 -V 05')
    outPut2 = run_command('./bin/cel-lpc-test -r -a 0xfc800000 -o 0x02 -C 1')
    if re.search("05", outPut1) and re.search("05", outPut2):
        log.success("lpc address write and read operation passed")
    else:
        log.fail("lpc address write and read operation failed")
        raise testFailed("lpc address write and read operation failed")
    outPut3 = run_command('./bin/cel-lpc-test --write --addr 0xfc800000 --offset 0x02 --count 1 --val 04')
    outPut4 = run_command('./bin/cel-lpc-test --read --addr 0xfc800000 --offset 0x02 --count 1')
    outPut5 = run_command('./bin/cel-lpc-test -r -a 0xfc800000 -o 0x00 -C 3')
    outPut6 = run_command('./bin/cel-lpc-test --read --addr 0xfc800000 --offset 0x00 --count 3')
    outPut7 = run_command('./bin/cel-lpc-test -r -a 0xfc805000 -o 0x00 -C 2')
    outPut8 = run_command('./bin/cel-lpc-test --read --addr 0xfc805000 --offset 0x00 --count 2')
    if re.search("04", outPut3) and re.search("04", outPut4) and re.search(".*04", outPut5) and re.search(".*04", outPut6) and ("04" not in outPut7) and ("04" not in outPut8):
        log.success("lpc address write and read operation passed")
    else:
        log.fail("lpc address write and read operation failed")
        raise testFailed("lpc address write and read operation failed")

@logThis
def getDiagOs():
    device.read_until_regexp(device.loginPromptDiagOS, timeout=480)
    device.getPrompt(Const.BOOT_MODE_DIAGOS)

@logThis
def resetHelpParameter():
    outPut1 = run_command('./bin/cel-reset-test -h')
    outPut2 = run_command('./bin/cel-reset-test --help')
    help_pattern = [
            "-r, --read *Read the last reset reason",
            "-t, --type *Reset type <cold|warm>",
            "-l, --list *List yaml info",
            "-v, --version *Display the version and exit",
            "-h, --help *Display this help text and exit"
            ]
    CommonKeywords.should_match_paired_regexp_list(outPut1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, help_pattern)

@logThis
def resetVersionParameter():
    outPut1 = run_command('./bin/cel-reset-test -v')
    outPut2 = run_command('./bin/cel-reset-test --version')
    ver_pattern = ["The ./bin/cel-reset-test version is :.*"]
    CommonKeywords.should_match_paired_regexp_list(outPut1, ver_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, ver_pattern)

@logThis
def resetListParameter():
    outPut1 = run_command('./bin/cel-reset-test -l')
    outPut2 = run_command('./bin/cel-reset-test --list')
    list_pattern = ["CPLD id : *2",
            "1 .* Reset_Reason_1 .* 5 .* /tmp/reset_reason.txt",
            "2 .* Reset_Reason_2 .* 6 .* /tmp/reset_reason.txt"]
    for item in list_pattern:
        if re.search(item, outPut1) and re.search(item, outPut2):
            log.success("list pattern {} is correct for \' -r option \'".format(item))
        else:
            log.fail("list pattern {} is wrong\' -r option \'".format(item))
            raise testFailed("list pattern {} is wrong\' -r option \'".format(item))
    

@logThis
def resetReadParameter():
    outPut1 = run_command('./bin/cel-reset-test -r')
    outPut2 = run_command('./bin/cel-reset-test --read')
    read_pattern =["The last reset is PCH .* Reset",
            "Reset test : Passed"]
    CommonKeywords.should_match_paired_regexp_list(outPut1, read_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, read_pattern)

@logThis
def resetSetParameter():
    device.sendCmd('./bin/cel-reset-test -t cold', 'Booting' , timeout=30)
    getDiagOs()
    verifyDiagToolPath()
    read_value = run_command('./bin/cel-reset-test -r')
    read_pattern =["The last reset is PCH Cold Reset",
            "Reset test : Passed"]
    CommonKeywords.should_match_paired_regexp_list(read_value, read_pattern)

    device.sendCmd('./bin/cel-reset-test --type warm', 'Booting' , timeout=30)
    getDiagOs()
    verifyDiagToolPath()
    read_value = run_command('./bin/cel-reset-test --read')
    read_pattern =["The last reset is PCH Warm Reset",
            "Reset test : Passed"]
    CommonKeywords.should_match_paired_regexp_list(read_value, read_pattern)

    device.sendCmd('./bin/cel-reset-test --type cold', 'Booting' , timeout=30)
    getDiagOs()
    verifyDiagToolPath()
    read_value = run_command('./bin/cel-reset-test -r')
    read_pattern =["The last reset is PCH Cold Reset",
            "Reset test : Passed"]
    CommonKeywords.should_match_paired_regexp_list(read_value, read_pattern)

    device.sendCmd('./bin/cel-reset-test -t warm', 'Booting' , timeout=30)
    getDiagOs()
    verifyDiagToolPath()
    read_value = run_command('./bin/cel-reset-test --read')
    read_pattern =["The last reset is PCH Warm Reset",
            "Reset test : Passed"]
    CommonKeywords.should_match_paired_regexp_list(read_value, read_pattern)

@logThis
def logindevice():
    getDiagOs()

@logThis
def enableRelaxSecurity(device='DUT'):
    import bios_menu_lib
    log.debug("Entering procedure reboot_and_enable_relax_security.\n")
    CommonLib.send_command('reboot', 'Press Esc for boot options' , timeout=30)
    
    bios_menu_lib.send_key(device, 'KEY_ESC')
    time.sleep(30)
    bios_menu_lib.send_key(device, 'KEY_DOWN', 3, 5)
    bios_menu_lib.send_key(device, 'KEY_ENTER',1, 5)
    time.sleep(20)
    bios_menu_lib.send_key(device, 'KEY_RIGHT',1 ,20)
    bios_menu_lib.send_key(device, 'KEY_DOWN', 3, 20)
    bios_menu_lib.send_key(device, 'KEY_ENTER',1 ,10)
    bios_menu_lib.send_key(device, 'KEY_DOWN', 3, 20)
    bios_menu_lib.send_key(device, 'KEY_ENTER', 1, 10)

    bios_menu_lib.send_key(device, 'KEY_DOWN',1,20)
    bios_menu_lib.send_key(device, 'KEY_ENTER',1,10)
    bios_menu_lib.send_key(device, 'KEY_F10',1,20)
    bios_menu_lib.send_key(device, 'KEY_ENTER',1, 30)
    
    getDiagOs()
    verifyToolPath()
    result=run_command('lspci')
    if re.search('00:1f.1 .*', result):
        log.success("The relax security option is set in BIOS")
    else:
        raise testFailed("Unable to set relax Security option in BIOS")

@logThis
def disableRelaxSecurity(device='DUT'):
    import bios_menu_lib
    log.debug("Entering procedure reboot_and_disable_relax_security.\n")
    CommonLib.send_command('reboot', 'Press Esc for boot options' , timeout=30)

    bios_menu_lib.send_key(device, 'KEY_ESC')
    time.sleep(30)
    bios_menu_lib.send_key(device, 'KEY_DOWN', 3, 5)
    bios_menu_lib.send_key(device, 'KEY_ENTER',1, 5)
    time.sleep(20)
    bios_menu_lib.send_key(device, 'KEY_RIGHT',1 ,20)
    bios_menu_lib.send_key(device, 'KEY_DOWN', 3, 20)
    bios_menu_lib.send_key(device, 'KEY_ENTER',1 ,10)
    bios_menu_lib.send_key(device, 'KEY_DOWN', 3, 20)
    bios_menu_lib.send_key(device, 'KEY_ENTER', 1, 10)

    bios_menu_lib.send_key(device, 'KEY_UP',1,20)
    bios_menu_lib.send_key(device, 'KEY_ENTER',1,10)
    bios_menu_lib.send_key(device, 'KEY_F10',1,20)
    bios_menu_lib.send_key(device, 'KEY_ENTER',1, 30)

    getDiagOs()
    verifyToolPath()
    result=run_command('lspci')
    output="'00:1f.1 .*"
    if (output not in result):
        log.success("The relax security option is disabled in BIOS")
    else:
        log.fail("Unable to disable relax Security option in BIOS")
        raise testFailed("Unable to disable relax Security option in BIOS")

@logThis
def getAndSetUsbRegisterValue():
    get_1=device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:1f.1/resource0 0xA74100')
    set_1=device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:1f.1/resource0 0xA74100 w 0xFC05D811')
    get_2=device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:1f.1/resource0 0xA74100')

    get_3=device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:1f.1/resource0 0xA74126')
    set_2=device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:1f.1/resource0 0xA74126 w 0xFFFFFFFF')
    get_4=device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:1f.1/resource0 0xA74126')
    if ('Error' not in get_1) and ('Error' not in set_1) and ('Error' not in set_2) and ('Error' not in get_3):
        log.success("set and get opertion executed successfully")
    else:
        log.fail("Error in usb set operation")
        raise testFailed("Error in set operation")
    if re.search('0xFC05D811', get_2) and re.search('0xFFFFFFFF', get_4):
        log.success("get and set of register value is done ")
    else:
        log.fail("get and set of usb register value is not happend")
        raise testFailed("get and set of register value is not happend")

@logThis
def setAndRead_Sata3_Dword6_RegisterValue():
    set_output=device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:1f.1/resource0 0xba1098 w 0x152D2800')
    get_output=device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:1f.1/resource0 0xba1098')
    if ('Error' not in set_output):
        log.success("set operation for sata3 dword6 register value is success")
    else:
        log.fail("unable to set operation for sata3 dword6 register value")
        raise testFailed("unable to set operation for sata3 dword6 register value")

    if re.search('0x152D2800', get_output):
        log.success('get operation for sata3 dword6 register value is successful')
    else:
        log.fail('get operation failed for sata3 dword6 register value')
        raise testFailed('get operation failed for sata3 dword6 register value')

@logThis
def getandSet_SMBus_Clk_Value():
    set_clk = device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:12.0/resource0 0x300 w 0x40000005')
    get_clk = device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:12.0/resource0 0x300')
    if ('Error' not in set_clk) and ('Error' not in get_clk):
        log.success('Set and Get command of SMBus clk values executed successfully')
    else:
        log.fail('Set and Get command of SMBus clk values execution failed')
        raise testFailed('Set and Get command of SMBus clk values execution failed')
    if re.search('0x40000005' , get_clk):
        log.success('user set value is received in get SMBus operation')
    else:
        log.fail('user set value is not received in Get operation')
        raise testFailed('user set value is not received in Get operation')
    set_clk = device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:12.0/resource0 0x304 w 0x8087007')
    get_clk = device.executeCmd('./pcimem /sys/bus/pci/devices/0000\:00\:12.0/resource0 0x304')
    if re.search('0x08087007' , get_clk):
        log.success('user set value is received in get SMBus operation')
    else:
        log.fail('user set value is not received in Get operation')
        raise testFailed('user set value is not received in Get operation')


@logThis
def setFanSpeed(D,p1,p2):
    p1= str(p1) +"%"
    p2 = str(p2) + "%"
    for i in range(1,3):
        str1 = "./bin/cel-fan-test -S -d " + str(i) + " -D " +str(D)
        str2 = "./bin/cel-fan-test --speed --dev " + str(i) + " --data " +str(D)
        output1 = run_command(str1)
        pattern_1 = ['Set FAN{} pwm {}'.format(i,p1),'FAN{} pwm is {}'.format(i,p2),'set fan{} speed Passed'.format(i)]
        
        output2 = run_command(str2)
        pattern_2 = ["Set FAN{} pwm {}".format(i,p1),"FAN{} pwm is {}".format(i,p2),"set fan{} speed Passed".format(i)]
        
        CommonKeywords.should_match_paired_regexp_list(output1, pattern_1)
        CommonKeywords.should_match_paired_regexp_list(output2, pattern_2)

@logThis
def checkCardHelp():
    cmd1=run_command('./bin/cel-cards-test -h')
    cmd2=run_command('./bin/cel-cards-test --help')
    pattern_1 = [       'Options are:',
                   '-s, --status  Show status',
                   '-l, --list    List yaml info',
                   '-v, --version  Display the version and exit',
                   '-h, --help    Display this help text and exit']
    CommonKeywords.should_match_paired_regexp_list(cmd1, pattern_1)
    CommonKeywords.should_match_paired_regexp_list(cmd2, pattern_1)



@logThis
def checkCardTest():
    cmd1 = run_command('./bin/cel-cards-test -v')
    cmd2 = run_command('./bin/cel-cards-test --version')
    ver_1 = "1.0.0"
    pattern_1 =["The ./bin/cel-cards-test version is : "+ str(ver_1)]
    CommonKeywords.should_match_paired_regexp_list(cmd1, pattern_1)
    CommonKeywords.should_match_paired_regexp_list(cmd2, pattern_1)



@logThis
def checkTypeAndMode():
    cmd1 = run_command('./bin/cel-cards-test -s')
    cmd2 = run_command('./bin/cel-cards-test --status')
    if re.search("24MP|24T|24P|48MP|48T|48P|48F",cmd1) and re.search("10G|25G|100G",cmd1):
        log.success("Type and mode matched")
    else:
        log.fail("Type and mode mismatch")
        raise testFailed("Type and mode mismatch")

    if re.search("24MP|24T|24P|48MP|48T|48P|48F",cmd2) and re.search("10G|25G|100G",cmd2):
        log.success("Type and mode matched")
    else:
        log.fail("Type and mode mismatch")
        raise testFailed("Type and mode mismatch")


@logThis
def runTpmManufactureTest():
    output = run_command('sh tools/tpm_manufacture_test.sh', timeout='120')
    pass_pattern = ["TPM Test Result: success!"]
    CommonKeywords.should_match_paired_regexp_list(output, pass_pattern)

@logThis
def systemCpldUpdate():
    output = run_command('bin/cel-vmetools2-test firmware/systemcpld_v000f_20210302.vme', timeout=110)
    pass_pattern = ["| PASS! |"]
    CommonKeywords.should_match_paired_regexp_list(output, pass_pattern)

@logThis
def checkDdrTest():
    run_command("cd /usr/bin")
    #output = run_command("stressapptest  -M 1200 -s 43200",timeout = 43250)
    output = run_command("stressapptest  -M 1200 -s 350",timeout = 370)
    CommonKeywords.should_match_a_regexp(output, 'Status: PASS')

@logThis
def eccHelpParameter():
    outPut1= run_command('./bin/cel-ecc-test -h')
    outPut2=run_command('./bin/cel-ecc-test --help')
    help_pattern=['-s, --status  ecc information status',
            '-l, --list    List yaml info',
            '-v, --version  Display the version and exit',
            '-h, --help    Display this help text and exit']
    CommonKeywords.should_match_paired_regexp_list(outPut1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, help_pattern)

@logThis
def eccVersionParameter():
    outPut1=run_command('./bin/cel-ecc-test -v')
    outPut2=run_command('./bin/cel-ecc-test --version')
    ver_pattern=['The ./bin/cel-ecc-test version is :.*']
    CommonKeywords.should_match_paired_regexp_list(outPut1, ver_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, ver_pattern)

@logThis
def eccListParameter():
    outPut1=run_command('./bin/cel-ecc-test -l')
    outPut2=run_command('./bin/cel-ecc-test --list')
    list_pattern=['1 .* IA32_MC7_STATUS .* 0x041d',
            '2 .* IA32_MC8_STATUS .* 0x0421']
    for item in list_pattern:
        if re.search(item, outPut1) and re.search(item, outPut2):
            log.success("list pattern {} is correct".format(item))
        else:
            log.fail("list pattern {} is wrong".format(item))
            raise testFailed("list pattern {} is wrong".format(item))

@logThis
def eccStatusParameter():
    outPut1=run_command('./bin/cel-ecc-test -s')
    outPut2=run_command('./bin/cel-ecc-test --status')
    status_pattern=['Memory\\(Channel 0\\)',
            'IA32_MC7_STATUS: 0x0',
            'Uncorrected Error: NO',
            'Corrected Error Count: 0x0',
            'Memory\\(Channel 1\\)',
            'IA32_MC8_STATUS: 0x0',
            'Uncorrected Error: NO',
            'Corrected Error Count: 0x0']
    pass_count = 0
    for item in status_pattern:
        if re.search(item, outPut1) and re.search(item, outPut2):
            pass_count+=1
        else:
            print("Failed due to the value:", item)
    if (pass_count == 8):
        log.success("ecc status parameter check passed")
    else:
        log.fail('Failure in ecc status parameter')
        raise testFailed('Failure in ecc status parameter')


@logThis
def marginHelpParameter():
    outPut=run_command('./bin/cel-margin-test -h')
    help_pattern=['-h, help information',
        '-m, <high,normal,low> configure the margin function']
    CommonKeywords.should_match_paired_regexp_list(outPut, help_pattern)

@logThis 
def pwmon_dcdc_all_test():
    pw_output=run_command('./bin/cel-pwmon-test --all')
    dc_output=run_command('./bin/cel-dcdc-test --all')
    pw_pattern=["PWMON test : Passed"]
    CommonKeywords.should_match_paired_regexp_list(pw_output, pw_pattern)
    dc_pattern=["DCDC test : Passed"]
    CommonKeywords.should_match_paired_regexp_list(dc_output, dc_pattern)

@logThis
def setMarginFunction():
    CommonLib.send_command('./bin/cel-margin-test -m high', 'Configure device to margin high')
    pwmon_dcdc_all_test()

    CommonLib.send_command('./bin/cel-margin-test -m low', 'Configure device to margin low')
    pwmon_dcdc_all_test()

    CommonLib.send_command('./bin/cel-margin-test -m normal', 'Configure device to margin normal')
    pwmon_dcdc_all_test()
    
@logThis
def checkDcdcVersion(modul,ver_1):
    cmd1 = run_command('./bin/cel-'+modul+'-test -v')
    cmd2 = run_command('./bin/cel-'+modul+'-test --version')
    pattern_1 =["The ./bin/cel-"+modul+"-test version is : "+ str(ver_1)]
    CommonKeywords.should_match_paired_regexp_list(cmd1, pattern_1)
    CommonKeywords.should_match_paired_regexp_list(cmd2, pattern_1)

@logThis
def CheckHelpInformationTool():
    log.debug('''help information of the tool should be got correctly via "-h" and "--help" option''')
    cmd1_output = run_command('./bin/cel-temp-test -h')
    cmd2_output = run_command('./bin/cel-temp-test --help')
    pattern1 = ["Options are:", "-r, --read          Read temp",
            "    --all           Test all configure options",
            "-v, --version        Display the version and exit",
            "-h, --help          Display this help text and exit",
            "-l, --list          List yaml info",
            "-m, --mode          change the test all mode <high/normal/low>",
            "-d, --dev           dev id"]
    CommonKeywords.should_match_paired_regexp_list(cmd1_output, pattern1)
    CommonKeywords.should_match_paired_regexp_list(cmd2_output, pattern1)

@logThis
def verifytheToolVersion(cmd1, cmd2):
    cmd1_output = run_command(cmd1)
    cmd2_output = run_command(cmd2)
    pattern1 = "The ./bin/cel-cpu-test version is : 1.0.0"
    log.debug("Verify the tool version")
    result1 = CommonKeywords.should_match_a_regexp(cmd1_output, pattern1)
    result2 = CommonKeywords.should_match_a_regexp(cmd2_output, pattern1)
    if result1 and result2 == 'does not match':
        log.fail("The tool version mismatch and should be correct in the release note")
        raise testFailed("The tool version mismatch and should be correct in the release note")
@logThis
def CheckYamlinformation(ymalinfocmd1, ymalinfocmd2):
    cmd1_output = run_command(ymalinfocmd1)
    cmd2_output = run_command(ymalinfocmd2)

    pattern1 = str([1, "Inlet1_AFI_sys", 0.0, 46.0, "U111", "/dev/Inlet1_AFI_sys",
        2, "onboard_AFO_sys", 0.0, 55.0, "U110", "/dev/onboard_AFO_sys",
        3, "onboard_AFI_sys", 0.0, 60.0, "U112", "/dev/onboard_AFI_sys",
        4, "Inlet1_AFO_sys", 0.0, 46.0, "U108", "/dev/Inlet1_AFO_sys",
        5, "Inlet2_AFO_sys", 0.0, 50.0, "U168", "/dev/Inlet2_AFO_sys",
        6, "Inlet3_AFO_system", 0.0, 49.0, "U26", "/dev/Inlet3_AFO_system",
        7, "temp_cpu_board", 0.0, 55.0, "U2039", "/dev/temp_cpu_board",
        8, "temp_CPU", 0.0, 70.0, "CPU", "/dev/temp_CPU",
        9, "temp_DIMM", 0.0, 70.0, "DIMM", "/dev/temp_DIMM"])

    log.debug("verify yaml information status and the result should be correct")
    CommonKeywords.should_match_a_regexp(cmd1_output, pattern1)
    CommonKeywords.should_match_a_regexp(cmd2_output, pattern1)

@logThis
def checkAutoTestrun(sensor_cmdlist):
    log.debug("Auto test for all sensor with all the configure options")
    pattern1 = str([1, "Inlet1_AFI_sys", "U111", 0.0, 46.0, "temp1_input", 24.00, "Passed",
        2, "onboard_AFO_sys", "U110", 0.0, 55.0, "temp1_input", 28.00, "Passed",
        3, "onboard_AFI_sys", "U112", 0.0, 60.0, "temp1_input", 26.50, "Passed",
        4, "Inlet1_AFO_sys" , "U108", 0.0, 46.0, "temp1_input", 23.50, "Passed",
        5, "Inlet2_AFO_sys" , "U168", 0.0, 50.0, "temp1_input", 23.50, "Passed",
        6, "Inlet3_AFO_system", "U26", 0.0, 49.0, "temp1_input", 23.50, "Passed",
        7, "temp_cpu_board", "U2039", 0.0, 55.0, "temp1_input", 26.50, "Passed",
        8, "temp_CPU", "CPU", 0.0, 70.0, "temp1_input", 25.00, "Passed",
        9, "temp_DIMM", "DIMM", 0.0, 70.0, "temp1_input", 27.06, "Passed"])

    for sensor_cmd in sensor_cmdlist:
        time.sleep(2)
        cmd_output = run_command(sensor_cmd)
        if not(re.search('rror|FAILED', cmd_output)):
                CommonKeywords.should_match_a_regexp(cmd_output, pattern1)
        else:
            log.info(cmd_output)
            log.fail(f"Error message is seen and TEMP test : FAILED via {sensor_cmd} cmd output")
            raise testFailed(f"Error message is seen and TEMP test : FAILED via {sensor_cmd} cmd output")



@logThis
def checkTempRangeValue(Tempoutput, allTempOutput):
    log.debug("Getting the sensor type and value")
    allTempOutput = allTempOutput.split("\n")
    sendsorName=re.search("([a-z0-9]+\_[a-z]+|\_[a-z]+)", Tempoutput, re.I|re.M)
    currentTemValue=re.search("(\d+\.\d+)", Tempoutput, re.I|re.M)
    sendsorName = sendsorName.group()
    currentTemValue = currentTemValue.group()
    for line in allTempOutput:
        if re.search(sendsorName, line):
            m = re.search("(0.0.*\S\d\.\d)", line)
            m = m.group(1).split("|")
            mim_value = m[0]
            max_value = m[1].replace(" ", "")
            if (mim_value <= str(currentTemValue) <= max_value):
                log.success(f"{sendsorName} temp value is {currentTemValue} in range between {mim_value} and {max_value}")
            else:
                raise testFailed(f"{sendsorName} temp value is {currentTemValue} NOT in range between {mim_value} and {max_value}")

@logThis
def checkthetempvalues(tempvaluecmd1, tempvaluecmd2, yamlinfo_cmd1):
    log.debug("Read the temp value in the device")
    allTempOutput = run_command(yamlinfo_cmd1)
    for i in range(1,10):
        time.sleep(2)
        cmd3_output = run_command(tempvaluecmd1 + str(i))
        time.sleep(2)
        cmd4_output = run_command(tempvaluecmd2 + str(i))
        if not(re.search('rror|FAILED', cmd3_output) and re.search('rror|FAILED', cmd4_output)):
            checkTempRangeValue(cmd3_output, allTempOutput)
            checkTempRangeValue(cmd4_output, allTempOutput)
        else:
            log.info(cmd3_output)
            log.info(cmd4_output)

@logThis
def checkI210Update():
    eeupdate = "./eeupdate64e"
    eeupdate_bin = "./eeupdate64e /NIC 1 /D " + var.bin_file
    read_word = "./eeupdate64e /NIC 1 /rw 0x1c"
    write_word = "./eeupdate64e /NIC 1 /ww 0x1c 0007"
    write_value = '0x0007'

    device.sendMsg("cd tools")
    device.executeCmd(eeupdate)

    output = device.executeCmd(eeupdate_bin)
    if not re.search("NIC Bus Dev Fun Vendor-Device  Branding string",output):
        log.fail("Error in Flash image update.")
        raise testFailed("Error in Flash image update.")
    
    output = device.executeCmd(read_word)

    output = device.executeCmd(write_word)

    output = device.executeCmd(read_word)
    read_value_after = re.findall("1: Word 0x1C =.*", output)[0].split('=')[-1].strip()
    
    if write_value == read_value_after and read_value_after.endswith("0007"):
        log.success("Diag tool Firmware upgrade function works correctly.")
    else:
        log.fail("Error in reading-writing value.")
        raise testFailed("Error in reading-writing value.")


@logThis
def checkFirmwareVersion(ver_1):
    cmd1 = run_command('./bin/cel-pwmon-test -d 2 -V')
    pattern_1 =["ucd90120_cpu image version : "+ str(ver_1)]
    CommonKeywords.should_match_paired_regexp_list(cmd1, pattern_1)


@logThis
def updatePwmonFirmware(firm):
    str1 = "./bin/cel-pwmon-upgrade -s CPU -f firmware/" + firm + "\n"
    device.sendMsg(str1)
    device.read_until_regexp('Need to write the system cpld*',timeout=120)
    device.sendCmd('reboot', 'Booting',timeout=30)
    getDiagOs()
    verifyDiagToolPath()

@logThis
def writeCPLDRegister_and_BootGoldenBios():
    BIOS_Version = CommonLib.get_swinfo_dict("BIOS").get("newVersion", "NotFound")
    Golden_BIOS_Version = BIOS_Version.replace('P', 'G')
    CommonLib.send_command('./bin/cel-cpld-test -w -d 2 -A 0x20b -D 0x5', 'cpu_cpld write reg: 0x20B 0x5')
    device.sendCmd('reboot', 'Golden BIOS version {}'.format(Golden_BIOS_Version) , timeout=45)
    CommonLib.send_command('none', 'Primary BIOS version {}'.format(BIOS_Version), timeout=280)
    getDiagOs()
    verifyDiagToolPath()
    CommonLib.send_command('./bin/cel-cpld-test --write --dev 2 --addr 0x20b --data 0x5', 'cpu_cpld write reg: 0x20B 0x5')
    device.sendCmd('reboot', 'Golden BIOS version {}'.format(Golden_BIOS_Version) , timeout=45)
    CommonLib.send_command('none', 'Primary BIOS version {}'.format(BIOS_Version), timeout=280)
    getDiagOs()


@logThis
def emmcHelpParameter():
    outPut1= run_command('./bin/cel-emmc-test -h')
    outPut2= run_command('./bin/cel-emmc-test --help')
    help_pattern=['--all *Test all configure options',
            '-i, --info *Show all EMMC information',
            '-v, --version *Display the version and exit',
            '-h, --help *Display this help text and exit',
            '-l, --list *List the setting in the configuration file']
    CommonKeywords.should_match_paired_regexp_list(outPut1, help_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, help_pattern)

@logThis
def emmcListParameter():
    diag_EMMC_Manufacturer= "SMART Modular"
    diag_EMMC_Product= "CGR1A "
    diag_EMMC_Capacity= "20.6"

    outPut1= run_command('./bin/cel-emmc-test -l')
    outPut2= run_command('./bin/cel-emmc-test --list')
    list_pattern=['.* emmc list cfg .*',
            'Total Device : 1, Test Size: 10, loop count: 1000','.*',
            'Id  :    1 , Name: emmc',
            'Type: emmc',
            'Dev Path : /sys/class/mmc_host/mmc0/mmc0\\\:0001/',
            f'Manufacturer : {diag_EMMC_Manufacturer} | SanDisk | Swissbit',
            f'Product : {diag_EMMC_Product}| ATPBG2 | 00020G',
            f'Capacity : {diag_EMMC_Capacity}']
    CommonKeywords.should_match_paired_regexp_list(outPut1, list_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, list_pattern)

@logThis
def emmcVersionParameter():
    CommonLib.send_command('./bin/cel-emmc-test -v', 'The ./bin/cel-emmc-test version is : 1.3.0')
    CommonLib.send_command('./bin/cel-emmc-test --version', 'The ./bin/cel-emmc-test version is : 1.3.0')

@logThis
def emmcInfoParamater():
    diag_EMMC_Manufacturer= "'SMART Modular' || 'SanDisk' || 'Swissbit'"
    diag_EMMC_Product= "'CGR1A ' || 'ATPBG2' || '00020G'"

    outPut1= run_command('./bin/cel-emmc-test -i')
    outPut2= run_command('./bin/cel-emmc-test --info')
    info_pattern=[".*sh.* drop_caches: 3",
            "type: 'MMC'",
            f"manufacturer: {diag_EMMC_Manufacturer} .*",
            f"product: {diag_EMMC_Product}.*",
            "serial: 0x0000000.*",
            "manfacturing date: .*",
            " done."]
    CommonKeywords.should_match_paired_regexp_list(outPut1, info_pattern)
    CommonKeywords.should_match_paired_regexp_list(outPut2, info_pattern)
    
@logThis
def emmcAll_LinuxInfoParameter():
    diag_EMMC_Manufacturer= "'SMART Modular' || 'SanDisk' || 'Swissbit'"
    diag_EMMC_Product= "'CGR1A ' || 'ATPBG2' || '00020G'"
    diag_EMMC_Capacity_all_pattern= "20.6 GB, 20635975680 bytes, 40304640 sectors"

    outPut =run_command('./bin/cel-emmc-test --all')
    linux_ouput=run_command('fdisk -l')

    all_pattern=[f"Manufacturer:  '{diag_EMMC_Manufacturer}' \' ---> Passed",
            f"Product:  '{diag_EMMC_Product}' .*---> Passed",
            f"Capacity:  {diag_EMMC_Capacity_all_pattern} ---> Passed"]
    pass_count =0
    if not(re.search ('rror|Failed|Warning', outPut) and re.search ('rror|Failed|Warning', linux_ouput)):
        for item in all_pattern:
            if re.search(item, outPut):
                pass_count += 1
            else:
                log.fail(f"Failure occured in the value {item}")
                raise testFailed(f"Failure occured in the value {item}")

        if (pass_count == 3) and re.search(diag_EMMC_Capacity_all_pattern, linux_ouput):
            log.success("linux and all parameter of EMMC command passed")
        else:
            log.fail(f'Failure occurred since the value {diag_EMMC_Capacity_all_pattern} and pass_count ={pass_count}is not same')
            raise testFailed (f'Failure occurred since the value {diag_EMMC_Capacity_all_pattern} and pass_count ={pass_count}is not same')


@logThis
def checkHelpWithCmdAndPattern(cmd, pattern):
    help_output1 = run_command( cmd + " -h")
    help_output2 = run_command( cmd + " -help")
    CommonKeywords.should_match_paired_regexp_list(help_output1, pattern)
    CommonKeywords.should_match_paired_regexp_list(help_output2, pattern)

def getVersionByCmdAndPattern(get_versions_cmd, pattern, split_by):
    output = run_command(get_versions_cmd)
    version = re.findall(pattern, output)[0].split(split_by)[-1].strip()
    return version

def checkWriteReadRegisterFunction(cmds, pattern):
    output = run_command(cmds)
    for each in pattern:
        if not re.search(each, output):
            return False
    return True

@logThis
def executeEepromTest():
    tool_version = getVersionByCmdAndPattern("./bin/cel-cpld-test -v", "The ./bin/cel-cpld-test version is :.*", ":")
    if not tool_version == "1.0.0":
        log.fail("The Tool Version is {}. Mismatched from the release note's version (1.0.0).".format(tool_version))
        raise testFailed("The tool version is mismatched.")
    
    # 4. Load the driver
    output = run_command(var.load_drivers_cmd)
    load_driver_pattern = [
        ".*delete_device: Deleting device.*at 0x54",
        ".*new_device: Instantiated device.*at 0x54",
    ]

    for each in load_driver_pattern:
        if not re.search(each, output):
            log.fail("Failed to load the driver.")
            raise testFailed("Failed to load the driver.")

    # Write and read the register data by 
    # 5. Register address.
    pattern = [
        "sys_cpld Reg .* data: 0x81",
        "sys_cpld Reg .* data: 0x80"
        ]
    if not checkWriteReadRegisterFunction(var.write_read_by_reg_add_cmd, pattern):
        log.fail("Failed to read write.")
        raise testFailed("Failed to read write data by reg address")

    # 6. Register No ID.
    pattern = [
        "sys_cpld Reg .* data: 0x81",
        "sys_cpld Reg .* data: 0x80"
        ]
    if not checkWriteReadRegisterFunction(var.write_read_by_reg_id_cmd, pattern):
        log.fail("Failed to read write.")
        raise testFailed("Failed to read write data by reg ID")

    # 7. Set model number as EX4400-48P
    run_command(["cd tools", "./crudini --set eeprom.cfg SYS_EEPROM model_number EX4400-48P"])
    
    # 8. Eeprom Flash
    output = run_command(var.eeprom_flash_cmd)
    if not re.search("model_number.*= EX4400-48P", output):
        log.fail("Setting Model Number Failed.")
        raise testFailed("Setting Model Number Failed.")
    
    run_command("cd ..")

    pattern = [
        "sys_cpld Reg .* data: 0x81",
        "sys_cpld Reg .* data: 0x80"
        ]
    if not checkWriteReadRegisterFunction(var.write_read_by_reg_add_cmd, pattern):
        log.fail("Failed to read write.")
        raise testFailed("Failed to read write data by reg address")
    else:
        log.success("Uplink module EEPROM Test Successful.")
   
@logThis
def emmcFWrevision():
    outPut = run_command('./fw_version_check /dev/mmcblk0')
    pattern = ['/dev/mmcblk0',
            'Vendor ID read from CID file \\(/sys/class/mmc_host/mmc0/mmc0:0001/cid\\)',
            'Verified to be valid eMMC part',
            'FW_VERSION\\[00\\]: .*',
            'Formatted Firmware Version: .*']
    CommonKeywords.should_match_ordered_regexp_list(outPut, pattern)
    if re.search(var.emmc_fw_revision_pattern, outPut):
        log.success("emmc fw revision is correct!")
    else:
        log.fail("wrong emmc fw version!")
        raise testFailed("wrong emmc fw version!")


@logThis
def emmcInfo():
    outPut = run_command('fdisk -l')
    info_pattern ='Disk /dev/mmcblk0: 20.6 GB, 20635975680 bytes, 40304640 sectors'
    if not(re.search ('rror|Failed|Warning', outPut)) and re.search(info_pattern, outPut):
        log.success("emmc info in cmd \'fdisk -l\' executed successfully")
    else:
        log.fail(f'Failure is due the pattern mismatch: {info_pattern}')
        raise testFailed (f'Failure is due the pattern mismatch: {info_pattern}')

@logThis
def poeFirmwareUpdate():
    
    card_type = getVersionByCmdAndPattern(var.card_type_cmd, var.card_type_pattern, ' ')
    if card_type not in "24P|48P|24MP|48MP":
        log.info("Card Type {} not supported for this test case.".format(card_type))
        return

    tool_version = getVersionByCmdAndPattern(var.tool_ver_cmd, var.tool_ver_ptn, ":")
    if tool_version != "1.0.0":
        log.fail("The Tool Version is {}. Mismatched from the release note's version (1.0.0).".format(tool_version))
        raise testFailed("The tool version is mismatched.")
    
    run_command(var.poe_fw_update_cmd, timeout=100)
    poe_sw_version = getVersionByCmdAndPattern(var.poe_ver_cmd, var.poe_ver_ptn, ":").split(' ')[0]
    if poe_sw_version == "0354":
        log.success("The update was completed successfully.")
    else:
        log.fail("Error in updating the PoE firmware.")
        raise testFailed("Error in updating the PoE firmware.")



@logThis
def checkPcieOperation():
    str1 = run_command("./auto_load_user.sh  -da",timeout =100)
#    pattern_1 =  ['Firmware download success',
#                 'Init load FW internally SUCCESS',
#                 'PASSED: broadfin Mode Config API passed']
 #   CommonKeywords.should_match_ordered_regexp_list(str1,pattern_1)
    if 'Failed' not in str1:
        log.success('cmd successfully boot into SDK system')
    else:
        log.fail('Cmd failed to boot into sdk system!')
        raise testFailed('cmd successfully boot into SDK system')
    device.sendMsg('./cls_shell attach \n')
    str2 = device.read_until_regexp('.*Attach: Unit 0.*')
    time.sleep(10)
    str3 = run_command("./cls_shell exit \n")
    time.sleep(10)


    if re.search("rror",str1):
         device.sendCmd('./cls_shell exit \n')
         exit
    if len(re.findall(".*Attach: Unit 0.*",str2)) != 0:
        log.success("Attach passed")
    else:
        log.fail("Error encountered.Non-expected output")
        raise testFailed("Error encountered.Non-expected output ")
        exit



@logThis
def verifySDKPath():
    output = run_command("cd /root/Diag/lagavulin/SDK")
    outputPath = run_command("pwd")
    if re.search("/root/Diag/lagavulin/SDK", outputPath):
        log.success("Can find the correct diag tool path")
    else:
        log.fail("Failed to find the diag SDK path")
        raise testFailed("Failed to find the diag SDK path")
    return outputPath


@logThis
def checkDeviceType():
    outPut = run_command('fdisk -l')
    if not re.search('sda.*', outPut) and not re.search('mmcblk.*', outPut):
        log.fail("Disk type is not USB|emmc")
        raise testFailed("\'sdax\ or emmc' for usb/emmc disk is not found in the cmd output")

    outPut = outPut.splitlines()
    disk =[]
    for line in outPut:
        if re.search('Disk', line):
            val = line.partition('/dev/')[-1]
            if val.strip() != '':
                disk.append(val)
    dtype=[]
    for item in disk:
        dtype.append((item.split()[0]).replace(':',""))

    return dtype

@logThis
def fioStressTestandLogVerification(stresstime, timeout):
    import logging
    logger = logging.getLogger()
    handler = logging.FileHandler('disk_stress_test.log')
    logger.addHandler(handler)
    disktype= checkDeviceType()
    log.debug(f'received : {disktype}')
    list_len = len(disktype)
    
    for item in disktype:
        cmd= f'fio fiocfg --name=job2 --filename=/dev/{item} --runtime={stresstime} --time_based'
        time=timeout
        output= run_command(cmd, timeout=time)
        
        logging.info(output)
        if re.search('rrror|warning|Failed', output):
            log.fail(f"Failure in the stress test with the disk :\'{item}\'")
            raise testFailed (f"Failure in the stress test with the disk :\'{item}\'")
        else:
            item = item +":"
            str1= output.split('READ:')[1]
            str2= output.split(item)[1]
            print("Run status group 0 (all jobs): \n READ:", str1)

    if not re.search('mmcblk', str(disktype)):
        log.fail('EMMC device is not present!')
    if not re.search('sda',str(disktype)):
        log.fail("USB device not present!")


@logThis
def checkFanTest():
    cmd1=run_command('./bin/cel-fan-test -h')
    cmd2=run_command('./bin/cel-fan-test --help')
    CommonKeywords.should_match_paired_regexp_list(cmd1, var.fan_help)
    CommonKeywords.should_match_paired_regexp_list(cmd2, var.fan_help)

@logThis
def checkFanList():

    cmd1 = run_command('./bin/cel-fan-test -l')
    cmd2 = run_command('./bin/cel-fan-test --list')
    pattern_1 = ['CPLD ID : 1, Device: FAN1, Reg_num: 3 , Fan_Status_Regid: 26, FAN_LED_Regid: 27',
            'Function |    PWM       |   FrontSpeed  |   RearSpeed  ',
            'Reg ID   |     16        |      17       |     18',
            'CPLD ID : 1, Device: FAN2, Reg_num: 3 , Fan_Status_Regid: 26, FAN_LED_Regid: 27',
            'Reg ID   |     22        |      23       |     24']
    CommonKeywords.should_match_ordered_regexp_list(cmd1,pattern_1)
    CommonKeywords.should_match_ordered_regexp_list(cmd2,pattern_1)



@logThis
def checkFanOperations():
    r1= run_command('./bin/cel-fan-test -r -R 19')
    r2 =run_command ('./bin/cel-fan-test --read --reg 19')
    r3 =run_command('./bin/cel-fan-test -r -R 22')
    w1 =run_command('./bin/cel-fan-test -w -R 22 -D ff')
    r4 =run_command('./bin/cel-fan-test --read --reg 22')
    w2 =run_command('./bin/cel-fan-test --write --reg 22 --data 7f')
    r5 =run_command('./bin/cel-fan-test --read --reg 22')

    if re.search("data: 0x7f",r1) and re.search("data: 0x7f",r2):
        log.success("The data is correct: \"data: 0x7f\"")
    else:
        log.fail("The expected data is incorrect.Expected : \"data: 0x7f\"")
        raise testFailed("The expected data is incorrect.Expected : \"data: 0x7f\"")

    if 'Error' not in r3:
        log.success("The data read for reg 22 is success!")
    else:
        log.fail("The data is incorrect!")
        raise testFailed("The Error string found in reg 22!")
    if re.search('data: ff',w1):
        log.success('Write success.New value: data: ff')
    else:
        log.fail("write failed : ff")
        raise testFailed("write failed : ff")
    if re.search('data: 0xff',r4):
        log.success("read is successful.Date: 0xff")
    else:
        log.fail("Expected read: 0xff ")
        raise testFailed("Expected read: 0xff ")
    if re.search('data: 7f',w2) and re.search('data: 0x7f',r5):
        log.success("Write was succesful: data: 7f")
    else:
        log.fail("Read/Write error.Expected : 7f")
        raise testFailed("Read/Write error.Expected : 7f")


@logThis
def fanOnOff(fan,val):
    str1 = run_command("./bin/cel-fan-test -L -d " + str(fan) + " -D " +str(val))
    str2 = run_command("./bin/cel-fan-test --led --dev " + str(fan) + " --data " +str(val))
    pattern_1= 'set FAN{} led {}'.format(fan,val)
    CommonKeywords.should_match_a_regexp(str1, pattern_1)
    CommonKeywords.should_match_a_regexp(str2, pattern_1)

@logThis
def fanLedStatus():
    fanOnOff(1,'off')
    fanOnOff(1,'on')
    fanOnOff(2,'off')
    fanOnOff(2,'on')



@logThis
def checkFanAll():
    cmd1 = run_command("./bin/cel-fan-test --all")
    pattern_1= ['FAN1:',
            'FAN1 is present',
            'FAN1 type is F2B',
            'FAN1 led is on',
            #'FAN1 front speed is 6900 RPM',
            #'FAN1 rear speed is 5850 RPM',

            'Set FAN1 pwm 50%',
            'FAN1 pwm is 49%',


            'Set FAN1 pwm 100%',
            'FAN1 pwm is 100%',

            'Set FAN1 pwm 30%',
            'FAN1 pwm is 29%',


            'FAN2:',
            'FAN2 is present',
            'FAN2 type is F2B',
            'FAN2 led is on',
            #'FAN2 front speed is 6900 RPM',
            #'FAN2 rear speed is 5700 RPM',

            'Set FAN2 pwm 50%',
            'FAN2 pwm is 49%',

            'Set FAN2 pwm 100%',
            'FAN2 pwm is 100%',

            'Set FAN2 pwm 30%',
            'FAN2 pwm is 29%',

            'FAN test : Passed']
    CommonKeywords.should_match_ordered_regexp_list(cmd1,pattern_1)


@logThis
def checkFanStatus():
    cmd1= run_command("./bin/cel-fan-test -s")
    cmd2= run_command("./bin/cel-fan-test --status")
    pattern_1 = ['FAN1:',
                'FAN1 is present',
                'FAN1 type is F2B',
                'FAN1 led is on',
                'FAN2:',
                'FAN2 is present',
                'FAN2 type is F2B',
                'FAN2 led is on']
    CommonKeywords.should_match_ordered_regexp_list(cmd1,pattern_1)
    CommonKeywords.should_match_ordered_regexp_list(cmd2,pattern_1)


@logThis
def checkFanSpeed(D,check = "no"):
    d1= str(D) +"%"
    if D == "100":
        d2 = str(D) +"%"
    else:
        d2 = str(int(D)-1) + "%"

    #Fan1
    str1 = "./bin/cel-fan-test -S -d 1 -D " +str(D)
    str2 = "./bin/cel-fan-test --speed --dev 1  --data " +str(D)
    output1 = run_command(str1)
    pattern_1 = ['Set FAN1 pwm {}'.format(d1),'FAN1 pwm is {}'.format(d2),'set fan1 speed Passed']
    checkFanStatus()
    output2 = run_command(str2)
    pattern_2 = ["Set FAN1 pwm {}".format(d1),"FAN1 pwm is {}".format(d2),"set fan1 speed Passed"]
    checkFanStatus()
    CommonKeywords.should_match_paired_regexp_list(output1, pattern_1)
    CommonKeywords.should_match_paired_regexp_list(output2, pattern_2)
    if check == "yes":
        checkFanAll()

    #Fan2
    str1 = "./bin/cel-fan-test -S -d 2 -D " +str(D)
    str2 = "./bin/cel-fan-test --speed --dev 2  --data " +str(D)
    output1 = run_command(str1)
    pattern_1 = ['Set FAN2 pwm {}'.format(d1),'FAN2 pwm is {}'.format(d2),'set fan2 speed Passed']
    checkFanStatus()
    output2 = run_command(str2)
    pattern_2 = ["Set FAN2 pwm {}".format(d1),"FAN2 pwm is {}".format(d2),"set fan2 speed Passed"]
    checkFanStatus()
    CommonKeywords.should_match_paired_regexp_list(output1, pattern_1)
    CommonKeywords.should_match_paired_regexp_list(output2, pattern_2)
    if check == "yes":
        checkFanAll()


@logThis
def updateDeviceImage(a):
    start = "rpm -ivh " + a
    out =  run_command('cd /home\r')
    output = run_command("pwd")
    if re.search("/home", out):
        log.success("Entered home directory")
    else:
        log.fail("Failed to enter home directory")
        raise testFailed("Failed to enter home directory")
    str_1 = run_command("rpm -qa|grep Diag")
    str_1 = "rpm -e " + str_1.split()[-2]
    deletion = run_command(str_1)
    run_command(start)
    device.sendCmd('reboot', 'Booting',timeout=30)
    getDiagOs()
    verifyDiagToolPath()
    val_1 = run_command("rpm -qa|grep Diag")
    val_1 = val_1.split()[-2] + ".rpm"
    if val_1 == a:
        log.success("Package installed successfully")
    else:
        log.fail("Package installtion failed")
        raise testFailed("Package installtion failed")




@logThis
def warmRebootTest():
    str1= run_command('./bin/cel-all-test --all')
    log.info(str1)
    if 'FAILED' in str1:
        log.fail("FAILED msg seen in './bin/cel-all-test --all'")
        raise testFailed("Failures found in Test app list cfg!")
    x= ['cpld','cpu','dcdc','fan','i2c','mem','emmc','pci','psu','pwmon','temp','tpm','usb','eeprom','eeprom','eth','cards','version','rtc','python','eeprom','eeprom']
    lst1=[]
    for i in range(0,len(x)):
        if i ==len(x)-3:
            lst1.append('{}.*Passed'.format(x[i]))
        elif i>=len(x)-2:
            lst1.append('./tools/{}.*Passed'.format(x[i]))
        elif x[i] == 'emmc' or x[i] == 'usb':
            lst1.append('./bin/cel-{}-test.*drop_caches: 3'.format(x[i]))
        else:
            lst1.append('./bin/cel-{}-test.*Passed'.format(x[i]))

    lst1.append("Total:{}, Failed: 0, Passed:{}".format(len(x),len(x)))
    CommonKeywords.should_match_ordered_regexp_list(str1,lst1)
    

@logThis
def get_sw_image(update  = "new"):
     updater_info_dict = CommonLib.get_swinfo_dict("IMAGE")
     if update == "new":
         filename = updater_info_dict.get("newImage", "NotFound")
     else:
         filename = updater_info_dict.get("oldImage", "NotFound")

     return filename

@logThis
def copyDiagImageTool():
    var_username = var.server_username
    var_password = var.server_password
    var_server_ip = var.tftp_server_ipv4
    var_filelist = var.diag_image_copy_list
    var_filepath = var.diag_image_server_path
    var_destination_path = var.diag_image_unit_path
    # var_mode = centos_mode

    return CommonLib.copy_files_through_scp(Const.DUT, var_username, var_password, var_server_ip, var_filelist, var_filepath, var_destination_path, 'None')

def tempSensorTest():
    output = run_command("./bin/cel-temp-test --all")
    if re.search("TEMP test : Passed", output):
        log.success("Temp Sensor Test PASSED.")
    else:
        log.fail("Failed to get the temp.")
        raise testFailed("Failed to get the temp.")

def LedTest10G_25G():
    output = run_command("./bin/cel-led-test --all -t port")
    if re.search("led test :Passed", output):
        log.success("LED Test PASSED.")
    else:
        log.fail("LED Test FAILED.")
        raise testFailed("LED Test FAILED.")

def runEepromTest():
    output = run_command(var.eeprom_cmds)
    for each in var.eeprom_test_pattern:
        if not re.search(each, output):
            log.fail("EEPROM Test Failed because of the pattern: \n\n--->" + each + "\n\n")
            raise testFailed("EEPROM Test Failed")

def SFPTest():
    output = run_command(var.sfp_cmds)
    for each in var.sfp_test_pattern:
        if not re.search(each, output):
            log.fail("SFP Test Failed.")
            raise testFailed("SFP Test Failed at cmd no. 6/8.")
    
    supply_voltage1 = float(re.findall("SUPPLY_VOLTAGE:.*", output)[0].split(':')[-1].strip())
    supply_voltage2 = float(re.findall("SUPPLY_VOLTAGE:.*", output)[1].split(':')[-1].strip())

    high_voltage1 = float(re.findall("VOLTAGE_HIGH_ALARM:.*", output)[0].split(':')[-1].strip())
    high_voltage2 = float(re.findall("VOLTAGE_HIGH_ALARM:.*", output)[1].split(':')[-1].strip())

    low_voltage1 = float(re.findall("VOLTAGE_LOW_ALARM:.*", output)[0].split(':')[-1].strip())
    low_voltage2 = float(re.findall("VOLTAGE_LOW_ALARM:.*", output)[1].split(':')[-1].strip())

    condition1 = low_voltage1 < supply_voltage1 < high_voltage1
    condition2 = low_voltage2 < supply_voltage2 < high_voltage2

    if not condition1 and condition2:
        log.fail("Error in Supply Voltage.")
        raise testFailed("Error in Supply Voltage.")

def executeMarginTest(value):
    margin_cmd = "./bin/cel-margin-test -m"

    device.sendMsg(margin_cmd + " {} \n\n".format(value))
    output = device.executeCmd("./bin/cel-pwmon-test --all")
    time.sleep(2)
    pwmon = re.search("PWMON test : Passed", output)
    output = device.executeCmd("./bin/cel-dcdc-test --all")
    time.sleep(2)
    dcdc = re.search("DCDC test : Passed", output)

    if not pwmon and dcdc:
        return False
    return True

def marginTest():
    device.sendMsg("cd /root/Diag/lagavulin \n\n")
    # At HIGH
    if not executeMarginTest("high"):
        log.fail("Margin Test failed at high.")
        raise testFailed("Margin Test failed at high.")

    # At LOW
    if not executeMarginTest("low"):
        log.fail("Margin Test failed at low.")
        raise testFailed("Margin Test failed at low.")
    else:
        device.executeCmd("./bin/cel-margin-test -m normal")
        log.success("Margin Test Passed Successfully.")

def upgrade_downgrade_cpu_cpld_version(cpld_bin_file, flag="upgrading"):
    run_command("cd /root/Diag/lagavulin")
    scp(cpld_bin_file)
    run_command("cp " + cpld_bin_file + " firmware/")
    old_version = getVersionByCmdAndPattern("./bin/cel-version-test -S", "CPU CPLD Version     :.*", ":")
    output = run_command("./bin/cel-update-test firmware/" + cpld_bin_file, timeout='120')
    for each in var.cpld_update_pattern:
        if not re.search(each, output):
            log.fail("ERROR in "+ flag +" the CPLD version.")
            raise testFailed("ERROR in "+ flag +" the CPLD version.")
    
    # --------------------- AC POWER CYCLE FUNCTION HERE. ---------------------

    new_version = getVersionByCmdAndPattern("./bin/cel-version-test -S", "CPU CPLD Version     :.*", ":")

    if old_version != new_version:
        log.success("The CPU CPLD "+ flag +" successfull.")
    else:
        log.fail("Error in CPU CPLD "+ flag +".")
        raise testFailed("Error in CPU CPLD "+ flag +".")


def checkSwitchCardHelp():
    help1 = run_command("./bin/cel-pwmon-upgrade -h")
    help2 = run_command("./bin/cel-pwmon-upgrade -help")

    CommonKeywords.should_match_paired_regexp_list(help1, var.switch_card_help_pattern)
    CommonKeywords.should_match_paired_regexp_list(help2, var.switch_card_help_pattern)

def checkSwitchCardVersion():
    output1 = run_command("./bin/cel-pwmon-test -d 1 -V")
    output2 = run_command("./bin/cel-pwmon-test --dev 1 --image_version")
    ver_pattern=["ucd90120_sys image version :.*"]
    CommonKeywords.should_match_paired_regexp_list(output1, ver_pattern)
    CommonKeywords.should_match_paired_regexp_list(output2, ver_pattern)

def updateImageByPwon():
    card_type = getVersionByCmdAndPattern("./bin/cel-cards-test -s", "Card type is .*", " ")
    
    update_txt_file = "U109_48X_05-26-14_46_V5_online.txt" if card_type in "24T/48T/24P/48P/48F" else "UCD_Lagavulin_MP_V03_0118.txt"
    old_version = getVersionByCmdAndPattern("./bin/cel-pwmon-test -d 1 -V", "ucd90120_sys image version :.*", ':')

    output = run_command("./bin/cel-pwmon-upgrade -s SYS -f firmware/" + update_txt_file)
    for each in var.switch_update_pattern:
        if not re.search(each, output):
            log.fail("Error in Updating the image file.")
            raise testFailed("Error in Updating the image file.")
    
    # --------------------- AC POWER CYCLE FUNCTION HERE. ---------------------

    new_version = getVersionByCmdAndPattern("./bin/cel-pwmon-test -d 1 -V", "ucd90120_sys image version :.*", ':')
    
    if old_version != new_version and new_version == "V05":
        log.success("Update Switch Card Power Monitor successfull.")
    else:
        log.fail("Update Switch Card Power Monitor FAILED.")
        raise testFailed("Update Switch Card Power Monitor FAILED.")


def upgradeEmmcFfu():
    device.sendMsg("cd /root/Diag/lagavulin/tools \n\n")
    fw_old_version = getVersionByCmdAndPattern("./fw_version_check /dev/mmcblk0", "Formatted Firmware Version:.*", ':')

    output = run_command("./mmc cid read /sys/bus/mmc/devices/mmc0\:0001/")
    manufacturer = re.findall("manufacturer:.*", output)[0]
    if "SMART Modular" in manufacturer:
        bin_file = "ISP-TTC29(R96-103164).bin"
    elif "Swissbit" in manufacturer:
        bin_file = "FW_SFEM020GB1ED1TO-I-6F-11P-JUN.bin"
    else:
        bin_file = "T0812.bin"

    run_command("cd ffu")
    device.sendMsg("./ffu_utility /dev/mmcblk0 \n\n")

    try:
        output = device.read_until_regexp(".*root@localhost ffu.*", timeout=5)
        if "No such file or directory" in output:
            raise Exception("SW_ERR")
    except Exception as E:
        if str(E) == "SW_ERR":
            raise Exception("SW error occured. Can not input the file name.")
        else:
            device.sendMsg(bin_file + " \r\n")
            device.read_until_regexp(".*root@localhost ffu.*", timeout=50)

    device.rebootToDiag()
    verifyToolPath()

    
    device.sendMsg("cd /root/Diag/lagavulin/tools \n\n")
    run = run_command("./fw_version_check /dev/mmcblk0")
    fw_new_version = getVersionByCmdAndPattern("./fw_version_check /dev/mmcblk0", "Formatted Firmware Version:.*", ':')
    
    err_msg = "eMMC FFU Upgrade Failed.\nVersion not changed\n"
    
    if 'SanDisk'  in manufacturer:
        if fw_new_version == fw_old_version:
            log.success("eMMC FFU Upgrade Successful.")
        else:
            log.fail(err_msg)
            raise testFailed(err_msg)
    else:
        if re.search(var.emmc_fw_revision_pattern, run):
            log.success("eMMC FFU Upgrade Successful.")
        else:
            log.fail(err_msg)
            raise testFailed(err_msg)
    
def executeCableVoltageDropTest():
    device.sendMsg("cd tools \n\n")
    output = run_command("./cable_test_new.sh")
    if re.search("-bash: ./cable_test_new.sh: No such file or directory", output):
        log.info("Only PZCOM-F0002-03 QSFP28 is supported.")
    elif re.search("Please insert PZCOM-F0002-03 QSFP28 into Port1#!", output):
        log.fail("Error in Cable Test. Please insert PZCOM-F0002-03 QSFP28 into Port1#!")
        raise testFailed("Error in Cable Test. Please insert PZCOM-F0002-03 QSFP28 into Port1#!")
    else:
        CommonKeywords.should_match_paired_regexp_list(output, var.fly_back_pass_pattern)


def downgrade_Upgrade_System_Cpld_Version(sys_cpld_vme_image, flag="Upgrading"):
    version_before = getVersionByCmdAndPattern("./bin/cel-version-test -S", "CPU CPLD Version.*", ':')
    scp(sys_cpld_vme_image) 
    output = run_command("./bin/cel-vmetools2-test " + sys_cpld_vme_image, timeout ='120')
    if re.search("| PASS! |", output):
        log.success("System CPLD {} successful.".format(flag))
    else:
        log.fail("ERROR in {} System CPLD Version".format(flag))
        raise testFailed("ERROR in {} System CPLD Version".format(flag))

    # --------------------- AC POWER CYCLE FUNCTION HERE. ---------------------

    version_after = getVersionByCmdAndPattern("./bin/cel-version-test -S", "CPU CPLD Version.*", ':')
    if version_before != version_after:
        log.success("System CPLD Update successful.")
    else:
        log.fail("Error in updating System CPLD Version.")
        raise testFailed("Error in updating System CPLD Version.")


@logThis
def dcdcHelpInfo():
    cmd1 = run_command('./bin/cel-dcdc-test -h')
    cmd2 = run_command('./bin/cel-dcdc-test --help')

    pattern_2 = ['Options are:',
             '--all           Test all configure options',
         '-v, --version        Display the version and exit',
         '-h, --help          Display this help text and exit',
         '-r, --read          Read the voltage value',
        '-l, --list          List yaml info',
        '-d, --dev           \[dev id such as 1..x], 1 is pxe1110_cpu_1, 2 is pxe1110_cpu_2, 3 is pxe1331',
         '-c, --channel       \[channel id such as 1..x\]',
         '-g, --get_margin    Get the property of margin',
         '-s, --set_margin    Set the property of margin']
    CommonKeywords.should_match_paired_regexp_list(cmd1, pattern_2)
    CommonKeywords.should_match_paired_regexp_list(cmd2, pattern_2)

@logThis
def listTheConfigYaml():
    cmd1 = run_command('./bin/cel-dcdc-test -l')
    cmd2 = run_command('./bin/cel-dcdc-test --list')
    if re.search("rror|Warning|Failed|Invalid", cmd1) and re.search("rror|Warning|Failed|Invalid", cmd2):
        log.fail("Error Encountered while executing list cmd 'cel-dcdc-test'")
        raise testFailed("Error Encountered while executing list cmd 'cel-dcdc-test'")
    else:
        log.success("dcdc-test list commands executed successfully")



@logThis
def checkDcdcVersion(modul,ver_1):
    cmd1 = run_command('./bin/cel-'+modul+'-test -v')
    cmd2 = run_command('./bin/cel-'+modul+'-test --version')
    pattern_1 =["The ./bin/cel-"+modul+"-test version is : "+ str(ver_1)]
    CommonKeywords.should_match_paired_regexp_list(cmd1, pattern_1)
    CommonKeywords.should_match_paired_regexp_list(cmd2, pattern_1)



@logThis
def checkDcdcVoltage():
    check= [1,2,5]
    for i in range(1,4):
        for j in range(1,4):
            if re.search('rror',run_command("./bin/cel-dcdc-test -r -d {} -c {}".format(i,j))):
                log.fail('Error Encountered in read dcdc cmd')
                raise testFailed('Error Encountered')
            if re.search('rror',run_command("./bin/cel-dcdc-test --read --dev {} --channel {}".format(i,j))):
                log.fail('Error Encountered in read dcdc cmd')
                raise testFailed('Error Encountered')

    for i in check:
        if i == 5:
            condition = not re.search('Not Supported',run_command("./bin/cel-dcdc-test  -d {} -s high" .format(i))) and \
                     re.search('Not Supported',run_command("./bin/cel-dcdc-test  -d {} -g" .format(i))) and \
                     not re.search('Not Supported',run_command("./bin/cel-dcdc-test  -d {} -s high" .format(i))) and \
                     not re.search('Not Supported',run_command("./bin/cel-dcdc-test  --dev {} --set_margin high".format(i))) and \
                     re.search('Not Supported',run_command("./bin/cel-dcdc-test  --dev {} --get_margin" .format(i)))
        else:
            condition = re.search('Not Supported',run_command("./bin/cel-dcdc-test  -d {} -s high" .format(i))) and \
                     re.search('Not Supported',run_command("./bin/cel-dcdc-test  -d {} -g" .format(i))) and \
                     re.search('Not Supported',run_command("./bin/cel-dcdc-test  -d {} -s high" .format(i))) and \
                     re.search('Not Supported',run_command("./bin/cel-dcdc-test  --dev {} --set_margin high".format(i))) and \
                     re.search('Not Supported',run_command("./bin/cel-dcdc-test  --dev {} --get_margin" .format(i)))
    if not condition:
        log.fail("Error encountered in Dcdc voltage")
        raise testFailed("Error encountered")


@logThis
def setAvsVoltage(arg,volt):
    cmd = "./avs_voltage_set.sh -" + arg
    cmd1 = run_command(cmd)
    if re.search(var.volt, cmd1):
        log.success(f'cpld register is correct!')
    else:
        log.fail('cpld register have unknown value!')
        raise testFailed('cpld register have unknown value!')

    if "inconsistent" in cmd1 or "Error" in cmd1:
        log.fail("AVS Voltage is inconsistent with CPLD register!!")
        raise testFailed("AVS Voltage is inconsistent with CPLD register!!")
    else:
        log.success("AVS Voltage set is successful!")

    if arg == "s":
         #device.sendCmd('reboot', 'Booting',timeout=30)
         #getDiagOs()
         #verifyDiagToolPath()
         log.info("Do power cycle manually to get the set AVS voltage value!")
    #JuniperCommonLib.powerCycleToDiagOS()
    if arg == "h":
        pattern=["Usage:",
                "-h: help information",
                "-s: set the avs voltage",
                "-c: compare the avs voltage with the register of CPLD"]
        CommonKeywords.should_match_paired_regexp_list(cmd1, pattern)

@logThis
def dcdcTestAll():
    cmd1 = run_command("./bin/cel-dcdc-test --all")
    pattern_1= ["DCDC test : Passed"]
    CommonKeywords.should_match_paired_regexp_list(cmd1, pattern_1)



@logThis
def checkEepromList():

    cmd1 = run_command('./eeprom -p /sys/bus/i2c/devices/0-0057/eeprom -d 2 ')
    run_command('./eeprom -c eeprom.cfg -o /sys/bus/i2c/devices/0-0057/eeprom -d 2')
    cmd2 = run_command('./eeprom -p /sys/bus/i2c/devices/0-0057/eeprom -d 2')
    CommonKeywords.should_match_paired_regexp_list(cmd1, var.cpu_list)
    CommonKeywords.should_match_paired_regexp_list(cmd2, var.cpu_list)

    cmd1 = run_command('./eeprom -p /sys/bus/i2c/devices/0-0051/eeprom -d 1')
    run_command('./eeprom -c eeprom.cfg -o /sys/bus/i2c/devices/0-0051/eeprom -d 1')
    cmd2 = run_command('./eeprom -p /sys/bus/i2c/devices/0-0051/eeprom -d 1')

    CommonKeywords.should_match_ordered_regexp_list(cmd1, var.sys_list)
    CommonKeywords.should_match_ordered_regexp_list(cmd2, var.sys_list)

@logThis
def checkSetModel():
    run_command('./crudini --set eeprom.cfg SYS_EEPROM model_number EX4400-48F-S')
    run_command('./eeprom -c eeprom.cfg -o /sys/bus/i2c/devices/0-0051/eeprom -d 1')
    cmd1 = run_command('./eeprom -p /sys/bus/i2c/devices/0-0051/eeprom -d 1')
    CommonKeywords.should_match_ordered_regexp_list(cmd1, var.sys_list1)

@logThis
def resetList():
        #(a = "no"):
#    if a == "yes":
#        pass
        #JuniperCommonLib.powerCycleToDiagOS()
    device.rebootToDiag()
    verifyToolPath()

    cmd1 = run_command('./eeprom -p /sys/bus/i2c/devices/0-0057/eeprom -d 2 ')
    cmd2 = run_command('./eeprom -p /sys/bus/i2c/devices/0-0051/eeprom -d 1')
    CommonKeywords.should_match_paired_regexp_list(cmd1, var.cpu_list)
    CommonKeywords.should_match_ordered_regexp_list(cmd2, var.sys_list1)

@logThis
def scp(filename):
    password = 'intel@1234'
    device.sendCmd(f'scp root@192.168.0.152:/home/tyrconnell_image/{filename} .')
    promptList = ["(y/n)", "(yes/no)", "password:"]
    patternList = re.compile('|'.join(promptList))
    output1 = device.read_until_regexp(patternList, timeout= '180')
    log.info('output1: ' + str(output1))

    if re.search("(yes/no)",output1):
        device.transmit("yes")
        device.receive("password:")
        device.transmit("%s"%password)
    elif re.search("(y/n)",output1):
        device.transmit("y")
        device.receive("password:")
        device.transmit("%s"%password)
    elif re.search("password:",output1):
        device.transmit("%s"%password)
    else:
        log.fail("pattern mismatch")

    device.read_until_regexp('root@localhost', timeout='140')
    device.sendCmd('\n\n')
    output = run_command('ls -la', prompt='root@localhost')
    if filename in output:
        log.success(f"file {filename} successfully fetched!")
    else:
        raise RuntimeError(f"Please add the file {filename} in 10.204.82.253/192.168.0.152, root server or add the file to the unit and run the test!")

@logThis
def iperfStressTest():
    serverip = CommonLib.get_device_info("PC").get("managementIP", "NotFound")
    log.debug("server ip: {}".format(serverip))
    scp('iperf')
    run_command("cd /home/")
    tool=run_command("ls")
    iperfversion = CommonLib.get_swinfo_dict("IPERF").get("newImage", "NotFound")
    pass_count=0
#    if re.search(iperfversion, tool):
#        log.success("iperf tool is present in lagavulin device")
#        pass_count +=1
#        CommonLib.exec_local_ping(serverip , 4)
#    else:
#        log.fail("please install iperf in the test unit for the test execution")
#        raise testFailed("please install iperf in the test unit for the test execution")

    pxhandle = jenkinServerLogin()

    data_rate=0
    if (pass_count!='0'):
        output= run_command("./"+iperfversion + " -c " + serverip + " -i 1 -t " + var.stress_count, timeout = var.cmd_timeout)
        output = output.splitlines()
        for item in output:
            if re.search(".*Mbits/sec", item):
                data= item.partition('Mbits/sec')[0]
                data = data.split()
                data = int(data[-1])
                if (data >= 900):
                    data_rate+=1
                else:
                    log.fail("The data rate is less than 90% = {}".format(data))
                    raise testFailed("The data rate is less than 90% = {}".format(data))
                if (data_rate == var.stress_count):
                    log.success("iperf data rate is 90% and above")

    else:
        log.fail("please install iperf in the test unit for the test execution")
        raise testFailed("please install iperf in the test unit for the test execution")
    pxhandle.close()

@logThis
def jenkinServerLogin():
    import pexpect
    import sys
    serverip = CommonLib.get_device_info("PC").get("managementIP", "NotFound")
    log.debug("server ip: {}".format(serverip))
    usr=  CommonLib.get_device_info("PC").get("rootUserName", "NotFound")

    #child = pexpect.spawn(f"ssh {usr}@{serverip}")
    child = pexpect.spawn(f"ssh -o StrictHostKeyChecking=no -l {usr} {serverip}")
    child.expect(f"{usr}@{serverip}'s password:")
    child.sendline(f"{var.server_pwd}")
    child.expect(f"{usr}.*#")
    child.sendline(f"{var.server_path}")
    child.expect(f"{usr}.*#")
    child.sendline(f"{var.server_cmd}")
    child.expect("Server listening on TCP port .*")
    return child


