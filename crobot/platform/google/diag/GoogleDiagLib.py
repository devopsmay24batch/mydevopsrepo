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
import GoogleConst
import Const
import time
from collections import OrderedDict

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/Google'))
from GoogleCommonVariable import fail_dict
import GoogleCommonLib
import GoogleDiagVariable as var
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)

@logThis
def ExportEnvPath(cmd_list):
    it = iter(cmd_list)
    while True:
        try:
            device.executeCmd(next(it))
        except StopIteration:
            break

@logThis
def gotoSuperUser():
    output = run_command("pwd", prompt="(root|admin)@sonic:.*")
    if "root@sonic:" in output:
        log.info("Already in super-user mode.")
    else:
        output = run_command("sudo -s", prompt="(root|admin)@sonic:.*")
        log.info("Entered Super-User mode.")

@logThis
def WaitForExecute(timestamp):
    time.sleep(timestamp)

@logThis
def systemResetToDiag(cmd):
    CommonLib.transmit(cmd)
    device.read_until_regexp(GoogleConst.STOP_AUTOBOOT_PROMPT, 200)
    device.sendMsg(GoogleConst.STOP_AUTOBOOT_KEY)
    device.getPrompt(Const.BOOT_MODE_DIAGOS)

@logThis
def upgradeCoreboot():
    log.info("Upgrading Brixia Coreboot Device")
    cmd=run_command("./cel-upgrade-test --update -d 5 -f ../tools/firmware/Coreboot.bios",prompt='root@sonic')
    log.info("Upgrading Capitaine Coreboot Device")
    cmd=run_command("./cel-upgrade-test --update -d 3 -f ../tools/firmware/Coreboot.bios",prompt='root@sonic')

@logThis
def upgradeCpld():
    log.info("Upgrading COMe CPLD Device")
    cmd=run_command("./cel-upgrade-test --update --dev 2 --file ../tools/firmware/COMe_CPLD_V16_20210901.vme",prompt='root@sonic')
    log.info("Upgrading Baseboard CPLD Device")
    cmd=run_command("./cel-upgrade-test --update --dev 4 --file ../tools/firmware/Brixia_baseboard_ucd_rev1.2.csv",prompt='root@sonic')

@logThis
def verifyDiagTool():
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    output = run_command("cd /usr/local/cls_diag/tools",prompt='root@sonic')
    outputPath = run_command("pwd",prompt='root@sonic')
    if re.search("/usr/local/cls_diag/tools", outputPath):
        log.success("Can find the correct diag path!")
    else:
        log.fail("Failed to find the diag path")

@logThis
def verifyDiagToolPath():
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    output = run_command("cd /usr/local/cls_diag/bin",prompt='root@sonic')
    outputPath = run_command("pwd",prompt='root@sonic')
    if re.search("/usr/local/cls_diag/bin", outputPath):
        log.success("Can find the correct diag path!")
    else:
        log.fail("Failed to find the diag path")


@logThis
def verifyHomePath():
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    output = run_command("cd /home",prompt='root@sonic')
    outputPath = run_command("pwd",prompt='root@sonic')
    if re.search("/home", outputPath):
        log.success("Can find the correct home  path!")
    else:
        log.fail("Failed to find the home path")

##############################COMMON##################################

@logThis
def checkHelp(mod):
    cmd1 = run_command("./cel-"+mod+"-test -h",prompt ='root@sonic')
    cmd2= run_command("./cel-"+mod+"-test --help",prompt='root@sonic')
    pattern= "var."+mod+"_help"
    CommonKeywords.should_match_ordered_regexp_list(cmd1,eval(pattern))
    log.success("The ./cel-"+mod+'-test help options are in-line with manual ')
    CommonKeywords.should_match_ordered_regexp_list(cmd2,eval(pattern))
    log.success("The ./cel-"+mod+'-test help options are in-line with manual ')

@logThis
def checkList(mod):
    cmd1 = run_command("./cel-"+mod+"-test -l",prompt ='root@sonic')
    cmd2= run_command("./cel-"+mod+"-test --list",prompt ='root@sonic')
    pattern = "var."+mod+"_list"
    CommonKeywords.should_match_ordered_regexp_list(cmd1,eval(pattern))
    log.success("The ./cel-"+mod+'-test list options are in-line with manual ')
    CommonKeywords.should_match_ordered_regexp_list(cmd2,eval(pattern))
    log.success("The ./cel-"+mod+'-test list options are in-line with manual ')

@logThis
def checkVersion(modul,ver_1):
    cmd1 = run_command('./cel-'+modul+'-test -v',prompt ='root@sonic')
    cmd2 = run_command('./cel-'+modul+'-test --version',prompt ='root@sonic')
    pattern_1 =["The.* ./cel-"+modul+"-test version is : "+ str(ver_1)]
    CommonKeywords.should_match_paired_regexp_list(cmd1, pattern_1)
    log.success("The ./cel-"+modul+'-test version is : '+ str(ver_1))
    CommonKeywords.should_match_paired_regexp_list(cmd2, pattern_1)
    log.success("The ./cel-"+modul+'-test version is : '+ str(ver_1))


@logThis
def checkTest(mod):
    if mod == 'pci':
        cmd1= run_command("./cel-"+mod+"-test --all --file ../configs/pcis_coreboot.yaml",prompt ='root@sonic')
    else:
        cmd1 = run_command("./cel-"+mod+"-test --all",prompt ='root@sonic')
    if re.search(mod.upper()+".*test.*: Passed",cmd1,re.IGNORECASE):
        log.success(mod + " test passed")
    else:
        log.fail(mod+" test failed")


@logThis
def boot_into_linuxboot():
    try:
        run_command("ls", prompt="~/#.*root@.*", timeout=2)
        log.info("\nAlready in LinuxBoot shell.\n")
    except Exception as e:
        try:
            run_command("pwd", prompt="(root|admin)@sonic:.*", timeout=2)
            gotoSuperUser()
            device.sendMsg("reboot \r\n")
            output = device.read_until_regexp('.*no modules found matching.*|.*Hit Ctrl-C to interrupt.*', timeout=130)
            if "Hit Ctrl-C to interrupt" in output:
                for i in range(3):
                    device.sendMsg(Const.KEY_CTRL_C)
                    try:
                        device.read_until_regexp('03. Enter a LinuxBoot shell', timeout=15)
                        device.sendMsg("3 \r\n")
                        break
                    except Exception:
                        continue
            else:
                for i in range(3):
                    device.sendMsg(Const.KEY_CTRL_C)
                    try:
                        device.read_until_regexp('>', timeout=15)
                        break
                    except Exception:
                        continue
            log.info("Logged into LinuxBoot Shell.")
        except Exception as e:
            log.info(str(e))


def enter_sonic_credentials():
    device.sendCmd(device.userName, "Password:", timeout=3)
    device.sendCmd(device.password, timeout=5)


@logThis
def boot_into_sonics():
    try:
        run_command("ls", prompt="(root|admin)@sonic:.*", timeout=2)
        log.info("Already logged in SONiC OS.")
    except:
        try:
            run_command("ls", prompt="~/#.*root@.*", timeout=2)
            run_command("boot /dev/sda3", prompt=">", timeout=3)
            device.sendCmd("01", "Debian GNU/Linux 10 sonic ttyS0", timeout=35)
            device.sendMsg("\n\n")
            enter_sonic_credentials()
            log.info("Logged into SONiC OS.")

        except:
            device.read_until_regexp('.*Hit Ctrl-C to interrupt', timeout=130)
            for i in range(3):
                device.sendMsg(Const.KEY_CTRL_C)
                try:
                    device.read_until_regexp('>', timeout=15)
                    break
                except Exception:
                    continue
            device.sendCmd("01", "Debian GNU/Linux 10 sonic ttyS0", timeout=50)
            enter_sonic_credentials()
            log.info("Logged into SONiC OS.")


#################################### TC_01 Install Diag Test  ############################################

def checkDiagVersion(flag):
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    device.sendCmd("cd /usr/local/cls_diag/bin", "root@sonic:", timeout=3)
    output = run_command("./cel-sysinfo-test --all", prompt="root@sonic:.*", timeout=3)
    version = re.findall("Diag Version:.*", output)[0].split(':')[1].strip()

    compare_version = var.brixia_diag_version if flag == "new" else var.brixia_old_diag_version
    if version != compare_version:
        raise Exception(
            "Diag version is not as required\nRequired version: " + compare_version + "\nFound version: " + version)
    else:
        print('PASS : The Diag version is correct :',version)



@logThis
def fetch_Image_From_Server(image):
    gotoSuperUser()
    run_command("cd /home/admin", prompt="root@sonic:.*", timeout=5)
    output = device.sendCmd("ls", "root@sonic:", timeout=5)
    if image in output:
        log.info("Image " + image + " already present on the device.")
        return
    log.info("Fetching diag image from server...")
    output = run_command("curl -O http://192.168.0.1/" + image, prompt="root@sonic:.*", timeout=60)
    if "Failed to connect" in output:
        log.info("Falied to fetch the image {} from the server.".format(image))


@logThis
def install_Diag_Package(diag_image):
    run_command("dpkg -i " + diag_image, prompt="root@sonic:.*", timeout=30)
    run_command("cd /usr/local/cls_diag", prompt="root@sonic:.*", timeout=3)

    # For Brixia Only
    run_command("./install -p brixia32", prompt="root@sonic:.*", timeout=15)
    run_command("sync;sync;sync", prompt="root@sonic:.*", timeout=15)
    cmd=run_command('reboot',prompt='sonic login:',timeout=300)
    device.loginToDiagOS()
    device.sendCmd('sudo -s','root@sonic',timeout =20)
 

@logThis
def check_Basic_Diag_Functions(flag=''):
    gotoSuperUser()

    # Check Structure
    device.sendCmd("cd /usr/local/cls_diag/bin", "root@sonic:", timeout=3)
    output = run_command("ls -la *", prompt="root@sonic:.*", timeout=3)
    for each in var.structure_ptn:
        if each not in output:
            raise Exception("Error in listing diag structure.\nConcerned Pattern -> " + each)
    log.success('The basic ls -la commands are displayed correctly')
    # Check Diag Version
    checkDiagVersion('new')

    c12= run_command('dpkg -l | grep cel-diag',prompt="root@sonic:", timeout=3)
    if re.search('ii  cel-diag',c12):
        log.success('Diag package present')
    else:
        log.fail('Diag package error')
    # Check Diag Export Line
    output = run_command("cat /root/.bashrc", prompt="root@sonic:.*", timeout=3)
    r = re.findall(".*export.*", output)
    r = [i for i in r if not i.startswith('#')]
    if len(r) > 1:
        raise Exception("More than one export statement found.\n" + str(r))
    log.success("Install Diag Test Successfully Passed.")

    if flag != 'final':
        cmd=run_command('reboot',prompt='sonic login:',timeout=300)
        device.loginToDiagOS()
        device.sendCmd('sudo -s','root@sonic',timeout =20)



#################################### TC_02 Update Diag Test  ############################################

def install_Old_Diag_Version():
    fetch_Image_From_Server(var.old_diag_image)
    install_Diag_Package(var.old_diag_image)


def remove_Old_Diag():
    output = ""
    for each in var.remove_diag_cmds:
        output += run_command(each, prompt="root@sonic:.*", timeout=10)
    for ptn in var.remove_diag_ptn:
        if ptn not in output:
            raise Exception("Error in removing old Diag version.")
    c1= run_command('cd /usr/local/cls_diag/',prompt='admin@sonic|root@sonic')
    if re.search('No such file or directory',c1):
        log.success('Diag package successfully removed from the system')
    else:
        log.fail('Diag package not purged')

#################################### TC_03 Upgrade BIOS/Coreboot  ############################################

def check_Coreboot_Version(flag="new"):
    bios_ver = eval("var.bios_" + flag + "_version")
    gotoSuperUser()
    run_command("cd /usr/local/cls_diag/bin", prompt="root@sonic:.*", timeout=5)

    output = run_command("./cel-sysinfo-test --all", prompt="root@sonic:.*", timeout=5)
    version = re.findall("BIOS Version:.*", output)[0].split(':')[1].strip()
    if version != bios_ver:
        raise Exception("BIOS version is not latest.\nFound version: " + version)
    else:
        log.success('BIOS version  is correct')

    output = run_command("dmidecode -t bios", prompt="root@sonic:.*", timeout=5)
    version = re.findall(".*Version:.*", output)[0].split(':')[1].strip()
    if version != bios_ver: 
        raise Exception("BIOS version is not latest.\nFound version: " + version)
    else:
        log.success('BIOS version is correct')
        print(bios_ver)

def change_Bios_version(cmd):
    if var.bios_new_image in cmd:
        run_command("flash_erase /dev/mtd0 0x3f0000 16", prompt="root@sonic:.*", timeout=10)
        run_command('yes "_HVNMAIL" | tr -d \'\\n\' | dd conv=notrunc bs=4096 seek=1008 count=16 of=/dev/mtd0',
                    prompt="root@sonic:.*", timeout=10)
        time.sleep(130)
        powerCycleDevice()
        gotoSuperUser()
    run_command("cd /usr/local/cls_diag/bin", prompt="root@sonic:.*", timeout=5)
    output = run_command(cmd, prompt="root@sonic:.*", timeout=300)
    if "Result: Upgrade Firmware --> Passed" not in output:
        raise Exception("Error in upgrading the BIOS/Coreboot version.")
    log.success('Firmware upgrade/downgrade operation successful')

def check_Other_Options():
    # --HELP option
    output = run_command("./cel-upgrade-test -h", prompt="root@sonic:", timeout=5)
    output += run_command("./cel-upgrade-test --help", prompt="root@sonic:", timeout=5)
    for each in var.option_help_ptn:
        if output.count(each) != 2:
            raise Exception("Error in cel-upgrade-test help pattern.\nConcerned pattern: " + each)
    log.success('The diag ./cel-upgrade-test options -h and --help are in-line with manual')
    # --VERSION option
    output = run_command("./cel-upgrade-test -v", prompt="root@sonic:", timeout=5)
    msg = "The diag ./cel-upgrade-test version is : " + var.brixia_diag_version
    if msg not in output:
        raise Exception("Error in cel-upgrade-test version pattern")
    else:
        log.success('The diag ./cel-upgrade-test version is correct')
    output = run_command("./cel-upgrade-test --version", prompt="root@sonic:", timeout=5)
    if msg not in output:
        raise Exception("Error in cel-upgrade-test version pattern.\nConcerned pattern: " + each)
    else:
        log.success('The diag ./cel-upgrade-test version is correct')
    # --LIST option
    output = run_command("./cel-upgrade-test -l", prompt="root@sonic:", timeout=5)
    output += run_command("./cel-upgrade-test --list", prompt="root@sonic:", timeout=5)
    for each in var.option_list_ptn:
        if output.count(each) != 2:
            raise Exception("Error in cel-upgrade-test list pattern.\nConcerned pattern: " + each)
    log.success('The diag ./cel-upgrade-test options -l and --list are in-line with manual')

#################################### TC_04 Upgrade CPLD Test   ############################################

def check_baseboard_CPLD_Version(flag="new"):
    if flag == 'new':
        fr_v1='0xb'
    else:
        fr_v1='0xa'
    cpld_baseboard_ver = eval("var.cpld_baseboard_" + flag + "_ver")
    gotoSuperUser()
    verifyDiagTool()
    c1=run_command('./lpc_cpld_x64_64 blu r 0xa100',prompt="root@sonic:.*", timeout=5)
    if re.search(fr_v1,c1):
        log.success("Baseboard cpld version is correct")
    else:
        log.fail("Baseboard CPLD version is incorrect")

    run_command("cd /usr/local/cls_diag/bin", prompt="root@sonic:.*", timeout=5)
    output = run_command("./cel-sysinfo-test --all", prompt="root@sonic:.*", timeout=5)
    # Baseboard Check
    baseboard = re.findall("Baseboard CPLD Version:.*", output)[0].split(':')[1].strip()
    if baseboard != cpld_baseboard_ver:
        raise Exception(
            "Error in Baseboard CPLD verison check.\nExpected: {}\nFound: {}".format(cpld_baseboard_ver, baseboard))


def check_come_CPLD_Version(flag="new"):
    if flag == 'new':
        d1_value='0x17'
    else:
        d1_value='0x16'
    cpld_come_ver = eval("var.cpld_come_" + flag + "_ver")
    gotoSuperUser()
    verifyDiagTool()
    c1=run_command('./lpc_cpld_x64_64 blu r 0xa1e0',prompt="root@sonic:.*", timeout=5)
    if re.search(d1_value,c1):
        log.success("COMe version is correct")
    else:
        log.fail("COMe version is incorrect")

    run_command("cd /usr/local/cls_diag/bin", prompt="root@sonic:.*", timeout=5)
    output = run_command("./cel-sysinfo-test --all", prompt="root@sonic:.*", timeout=5)
    # Come Check
    come = re.findall("COMe_CPLD Version:.*", output)[0].split(':')[1].strip()
    if come != cpld_come_ver:
        raise Exception("Error in COMe CPLD verison check.\nExpected: {}\nFound: {}".format(cpld_come_ver, come))
    else:
        log.success('Operation is successful')


def change_cpld_version(mode, flag="new"):
    image = eval("var.cpld_" + mode + "_" + flag + "_image")
    arg = "2" if mode == "come" else "4"
    cmd = var.change_cpld_cmd.format(arg, image)
    device.sendMsg(cmd + "\r\n")
    output = device.read_until_regexp("root@sonic:.*", timeout=310)
    if "Result: Upgrade Firmware --> Passed" not in output:
        raise Exception("Error in changing CPLD " + mode + " verison.")
    else:
        log.success('Downgrade/Upgrade operation successful')

#################################### tcs 10  ############################################
@logThis
def checkLspci():
    cmd1= run_command("lspci",prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(cmd1,var.lspci)

@logThis
def checkPciFile():
    c1=run_command("./cel-pci-test -l --file ../configs/pcis_linuxboot.yaml",prompt ='root@sonic')
    c2=run_command("./cel-pci-test --all -f ../configs/pcis_linuxboot.yaml",prompt ='root@sonic')
    if re.search("PCIe.*test.*: Failed",c2,re.IGNORECASE):
        log.success(" Test failed as expected")
    else:
        log.fail(" Test passed but expected fail")
    run_command('exit')    ###Exit root privilege



###########################################tcs 14###################################################################
@logThis
def operate(a):
    a= run_command(a,prompt ='root@sonic')
    a=a.split(" ")
    return a[-5]


@logThis
def checkCpldOperations():
    global d1_value
    val = ['Read value: 0x17','cpld test : Passed']
    val1=['cpld test : Passed']
    d1_value="0x17"
    c1=run_command("./cel-cpld-test -d 1",prompt ='root@sonic')
    c2=run_command("./cel-cpld-test --dev 1 ",prompt ='root@sonic')

    #operate("./cel-cpld-test -all")

    CommonKeywords.should_match_ordered_regexp_list(c1,val)
    log.success('The Cpld version is correct')
    CommonKeywords.should_match_ordered_regexp_list(c2,val)
    log.success('The Cpld version is correct')

    c3 = run_command("./cel-cpld-test -d 2",prompt ='root@sonic')
    c4=run_command("./cel-cpld-test --dev 2",prompt ='root@sonic')
  
    CommonKeywords.should_match_ordered_regexp_list(c3,val1)
    log.success('The Cpld scratch value is correct')
    CommonKeywords.should_match_ordered_regexp_list(c4,val1)
    log.success('The Cpld scratch value is correct')


    c5=operate("./cel-cpld-test -d 2")

    verifytool()
    #print("The value of c5 is ",c5)
    d1=run_command("./lpc_cpld_x64_64 blu r 0xa1e0",prompt ='root@sonic')
    d2=run_command("./lpc_cpld_x64_64 blu r 0xa1e1",prompt ='root@sonic')

    if re.search(d1_value,d1)  and re.search(c5,d2):
        log.success("Read was successful")
    else:
        log.fail("Read has failed")


    verifyDiagToolPath()
    run_command('exit',prompt ='root@sonic')
    run_command('exit',prompt ='root@sonic')



@logThis
def recheckCpldScratch():
    cmd=run_command("./cel-bb-cpld-test --all",prompt='root@sonic')
    output=cmd.splitlines()
    d1_value=output[-3]
    verifyDiagTool()
    d2=run_command("./lpc_cpld_x64_64 blu r 0xa1e1",prompt ='root@sonic')
    if re.search(d1_value,d2):
        log.success("Read was successful")
    else:
        log.fail("Read has failed")
    run_command('exit',prompt='admin@sonic|root@sonic',timeout=5)

##########################Tcs 44#############################################
@logThis
def checkStressHelp():
    flag = 0
    v1=['0 errors','Status: PASS - please verify no corrected errors']

    c1=run_command("stressapptest -h",prompt ='root@sonic')
    v2=run_command('stressapptest -s 600 -M 28800 -m 4 -i 4 -C 8 -W -d /dev/sda3 --pause_delay 700',timeout=700,prompt='root@sonic')

    CommonKeywords.should_match_ordered_regexp_list(c1,var.stress_help)
    for x in v1:
        if not re.search(x,v2):
            flag = 1
    if flag == 0:
        log.success("No error encountered")
    else:
        log.fail("Error encountered")

@logThis
def coverMfgIssue():
    c1=run_command('for i in {1..10}; do echo -e \"--- Test Loop $i ---\n\"; stressapptest -s 60 -M 28800 -m 4 -i 4 -C 8 -W -d /dev/sda3; sleep 30; done',timeout=2000)
    device.sendMsg('\n')
    if re.search('STATUS: FAIL',c1):
        log.fail('Error in Mfg loop')
    c9=len(re.findall('Status: PASS',c1))
    if c9 == 10:
        log.success('Test loops passed')
    else:
        log.fail('Test Loops failed')


############################################POWER CYCLER   ##########################

@logThis
def  powerCycleDevice():
    verifytool()
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    device.sendCmd('echo 0x4449454a > /sys/devices/gfpga-platform/board_powercycle', 'sonic login:',timeout=450)
    device.loginToDiagOS()
    time.sleep(60)

#########################################TCS 9 ####################################



@logThis
def checkFpgaOperations():
   c4=run_command("./cel-fpga-test -d 1",prompt='root@sonic')
   c5=run_command("./cel-fpga-test --dev 2",prompt='root@sonic')
   c6=run_command("./cel-fpga-test --dev 3",prompt='root@sonic')
   c7=run_command("./cel-fpga-test -d 4",prompt='root@sonic')
   c8=run_command("cat /sys/devices/gfpga-platform/scratch",prompt='root@sonic')
   c9=run_command("./cel-fpga-test --all",prompt='root@sonic')
   for x in [c4,c5,c6,c7]:
       if re.search("FPGA.*test.*: Passed",x,re.IGNORECASE):
           log.success("Test passed")
       else:
           log.fail(" test failed")
   if var.scratch != c8:
       log.success("Scratch value expected as non zero")
   else:
       log.fail("Scratch value is 0")

   if re.search("FPGA.*test.*: Passed",c9,re.IGNORECASE):
           log.success("Test passed")
   else:
           log.fail(" test failed")
@logThis
def verifySdk():
    output = run_command("cd /usr/local/cls_sdk",prompt="root@sonic")
    outputPath = run_command("pwd",prompt="root@sonic")
    if re.search("/usr/local/cls_sdk", outputPath):
        log.success("Correct sdk path")
    else:
        log.fail("Failed to find the sdk path")

@logThis
def quitSdk():
    run_command("quit",prompt="root@sonic")


@logThis
def verifytool():
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    output = run_command("cd /usr/local/cls_diag/tools",prompt="root@sonic")
    outputPath = run_command("pwd",prompt="root@sonic")
    if re.search("/usr/local/cls_diag/tools", outputPath):
        log.success("Correct tool path")
    else:
        log.fail("Failed to find the tool path")

@logThis
def checkFpgaSdk():
    verifySdk()
    d6=run_command("./auto_load_user.sh",prompt ='root@sonic')
    d7=run_command('./bcm.user -y brixiaV2-TH4G-256x1x100.yml',prompt='BCM.0>',timeout= 30)
    d3=run_command('version',prompt='BCM.0>',timeout=30)
    quitSdk()
    run_command('exit')

   # CommonKeywords.should_match_a_regexp(d7,var.fpga_sdk)
    CommonKeywords.should_match_ordered_regexp_list(d3,var.fpga_sdk)

    verifyDiagToolPath()
    d9=run_command("./cel-fpga-test --all --loop 3",prompt ='root@sonic')
    if re.search("FPGA.*test.*: Passed",d9,re.IGNORECASE):
        log.success(" Test passed")
    else:
        log.fail(" Test failed")

    checkI2cdetect()


    verifySdk()
    m1=run_command("./auto_load_user.sh",prompt ='root@sonic')
    m2=run_command('./bcm.user -y brixiaV2-TH4G-256x1x100.yml',prompt='BCM.0>',timeout= 30)
    m3=run_command('version',timeout=30,prompt ='BCM.0>')
    quitSdk()


@logThis
def checkMajorMinor():
    c1= run_command("cat /sys/devices/gfpga-platform/majorrevision",prompt ='root@sonic')
    c2= run_command("cat /sys/devices/gfpga-platform/minorrevision",prompt ='root@sonic')
    c3= run_command("cat /sys/devices/gfpga-platform/scratch",prompt ='root@sonic')
    print("c1- {} :major{}".format(c1,var.major))
    print("c2-{} : minor{}".format(c2,var.minor))
    reg = re.search(var.major,c1) and re.search(var.minor,c2) and re.search(var.scratch,c3)
    if reg:
        log.success("Values are expected")
        log.success('The scratch value is 0')
    else:
        log.fail("Values not correct")
@logThis
def checkI2cdetect():
    c1= run_command("i2cdetect -l",prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(c1,var.i2cdetect_list)

###############################tcs 33 #####################################################################

@logThis
def checkTh4Operations():
    ##Help:
    typ1 = ['01:00.0 0200: 14e4:b996 \(rev 11\)']

    c1=run_command('./cel-detect-th4-test -h',prompt ='root@sonic')
    c2=run_command('./cel-detect-th4-test --help',prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(c1,var.th4_help)
    log.success('Th4g help options are in-line with manual')
    CommonKeywords.should_match_ordered_regexp_list(c2,var.th4_help)
    log.success('Th4g help options are in-line with manual')

    pattern1=  ['The ./cel-detect-th4-test version is : '  + str(var.th4_version)]
    c3=run_command('./cel-detect-th4-test -v',prompt ='root@sonic')
    c4=run_command('./cel-detect-th4-test --version',prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(c3,pattern1)
    log.success('Th4g version is correct')
    CommonKeywords.should_match_ordered_regexp_list(c4,pattern1)
    log.success('Th4g version is correct')

    c5=run_command('./cel-detect-th4-test -l',prompt ='root@sonic')
    c6=run_command('./cel-detect-th4-test --list --file ../configs/detect_th4_b0.yaml',prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(c5,var.th4_list)
    log.success('Th4g list options are in-line with manual')
    CommonKeywords.should_match_ordered_regexp_list(c6,var.th4_list)
    log.success('Th4g list options are in-line with manual')

    c7=run_command('lspci -s 01:00.0 -n',prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(c7,typ1)
    log.success('Th4g lspci rev is correct')

    c8=run_command('./cel-detect-th4-test --dev 1',prompt ='root@sonic')
    c9=run_command('./cel-detect-th4-test -d 2',prompt ='root@sonic')
    c10=run_command('./cel-detect-th4-test -d 3 -f ../configs/detect_th4_b0.yaml',prompt ='root@sonic')
    c11=run_command('./cel-detect-th4-test --all -f ../configs/detect_th4_b0.yaml',prompt ='root@sonic')
    reg = re.search('detect-th4 test : Passed',c8) and \
          re.search('detect-th4 test : Passed',c9) and \
          re.search('detect-th4 test : Passed',c10) and \
          re.search('detect_th4 Test : Passed',c11)
    if reg:
        log.success("\nTh4g dev 1  passed\nTh4g dev 2  passed\nTh4g dev 3  passed\nTh4g All Test  passed\n")
    else:
        log.fail("Th4g Test failed")

    c12= run_command(' ./cel-detect-th4-test --all',prompt ='root@sonic')
    c13=run_command('./cel-detect-th4-test --all --file ../configs/detect_th4.yaml',prompt ='root@sonic')

    reg1= re.search('detect_th4 Test : FAILED',c12)  and re.search('detect_th4 Test : FAILED',c12)
    if reg1:
        log.success("Th4G Test Failed as expected")
    else:
        log.fail("Expect Th4g to fail but test passed")
    run_command('exit')     ####exiting root

@logThis
def checkTempList():
    c1=run_command("./cel-temp-test --list  --file ../configs/second_source/temp_flex.yaml",prompt ='root@sonic')
    c2=run_command("./cel-temp-test -l  --file ../configs/second_source/temp_flex.yaml",prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(c1,var.temp_list) 
    CommonKeywords.should_match_ordered_regexp_list(c2,var.temp_list)
    log.success('Temp list in-line with manual')

@logThis
def checkTempTest(mod):
    cmd1 = run_command("./cel-"+mod+"-test --all",prompt ='root@sonic')
    if re.search(mod.upper()+".*test.* Passed",cmd1,re.IGNORECASE):
        log.success(" Temp test All passed.")
    else:
        log.fail("Temp test All failed.")
    output = run_command("sensors", prompt="root@sonic:.*", timeout=10)
    for each in var.adapter_list:
        if each not in output:
            raise Exception("Error in sensor list.\nConcerned pattern: "+each)
    c11=run_command(' ./cel-temp-test --all --file ../configs/second_source/temp_flex.yaml',prompt="root@sonic")
    if re.search('Result:Temp test all --> FAILED <<<',c11):
        log.success('Test Failed as expected')
    else:
        log.fail('Test passed but expected fail')

    c12=run_command('./cel-temp-test --all --file ../configs/second_source/temp_astersyn.yaml',prompt="root@sonic")
    if re.search('Result:Temp test all --> FAILED <<<',c11):
        log.success('Test Failed as expected')
    else:
        log.fail('Test passed but expected fail')


@logThis
def checkPsuTest(mod):
    cmd1 = run_command("./cel-"+mod+"-test --all",prompt ='root@sonic')
    if re.search("POWER test : Passed",cmd1,re.IGNORECASE):
        log.success(" test passed")
    else:
        log.fail(" test failed")

@logThis
def checkPsuRead(mod):
    cmd1=run_command("./cel-"+mod+"-test --read --dev 1",prompt ='root@sonic')
    if not  re.search("Power read dc dev_id 1 Passed",cmd1,re.IGNORECASE):
        raise Exception("psu read passed")
    for i in range(2,17):
        cmd=run_command("./cel-"+mod+"-test -r -d {}".format(i),prompt ='root@sonic')
        if re.search("Power read dc dev_id {} Passed".format(i),cmd,re.IGNORECASE):
            log.success("psu read passed")
        else:
            raise Exception("psu read failed")

@logThis
def checkTempRead(mod):
    run_command('docker ps | grep pmon',prompt ='root@sonic')
    time.sleep(60)   ;#For docker to come up
    c1=run_command("./cel-"+mod+"-test --read  --dev 1")
    if not re.search("Result:Temp read Temp_id: "+ str(1) +" --> Passed",c1,re.IGNORECASE):
        log.fail('Temp test failed for dev 1 ')
    for i in range(2,27):
        cmd=run_command("./cel-"+mod+"-test -r -d " + str(i), prompt ='root@sonic')
        if re.search("Result:Temp read Temp_id: "+ str(i) +" --> Passed",cmd,re.IGNORECASE):
            log.success("temp read passed")
        else:
            log.fail("temp read failed")

@logThis
def checkQsfpHelp():
    cmd=run_command("./cel-qsfp-test -h",prompt='root@sonic')
    count=0
    for i in var.qsfp_help:
        if re.search(i,cmd,re.IGNORECASE):
            count+=1
    if count==len(var.qsfp_help):
        log.success("qsfp help parameter passed")
    else:
        log.fail("qsfp help parameter failed")


@logThis
def checkQsfpList():
    cmd=run_command("./cel-qsfp-test -l",prompt='root@sonic')
    count=0
    for i in var.qsfp_list:
        if re.search(i,cmd,re.IGNORECASE):
            count+=1
    if count==len(var.qsfp_list):
        log.success("qsfp list parameter passed")
    else:
        log.fail("qsfp list parameter failed")


@logThis
def verifyAdminPath():
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    output = run_command("cd /home/admin",prompt='root@sonic')
    outputPath = run_command("pwd",prompt='root@sonic')
    if re.search("/home/admin", outputPath):
        log.success("Can find the correct admin path!")
    else:
        log.fail("Failed to find the admin path")

@logThis
def showMemorySpdInformation():
    cmd=run_command("dmidecode -t memory",prompt='root@sonic')

    count=0
    for i in var.memory_spd_list:
        if re.search(i,cmd,re.IGNORECASE):
            count+=1
    if count==len(var.memory_spd_list):
        log.success("memory spd information passed")
    else:
        log.fail("memory spd information failed")

@logThis
def checkLowAndHighPowerMode():
    cmd1=run_command("./cel-qsfp-test --lpmode",prompt='root@sonic')
    cmd2=run_command("./cel-qsfp-test --hpmode",prompt='root@sonic')
    count1=0
    count2=0
    for i in var.lp_mode_pattern:
        if re.search(i,cmd1,re.IGNORECASE):
            count1+=1
    for i in var.hp_mode_pattern:
        if re.search(i,cmd2,re.IGNORECASE):
            count2+=1
    if count1==2 and count2==2:
        log.success("low and high power osfp mode passed")
    elif count1==2 and count2!=2:
        log.fail("high power mode failed")
    elif count1!=2 and count2==2:
        log.fail("low power mode failed")
    else:
        log.fail("both low and high power modes failed")

@logThis
def checkQsfpTest():
    cmd=run_command("./cel-qsfp-test --all",prompt='root@sonic')

    if re.search(var.qsfp_all_pattern,cmd,re.IGNORECASE):
        log.success("qsfp test all parameter passed")
    else:
        log.fail("qsfp all parameter failed")
@logThis
def checkSysHelp():
    cmd=run_command("./cel-sysinfo-test -h",prompt='root@sonic')
    cmd1=cmd=run_command("./cel-sysinfo-test --help",prompt='root@sonic')
    count=0
    for i in var.sysinfo_help:
        if re.search(i,cmd,re.IGNORECASE):
            count+=1
    if count==len(var.sysinfo_help):
        log.success("sysinfo help parameter passed")
    else:
        log.fail("sysinfo help parameter failed")
    count=0
    for i in var.sysinfo_help:
        if re.search(i,cmd1,re.IGNORECASE):
            count+=1
    if count==len(var.sysinfo_help):
        log.success("sysinfo help parameter passed")
    else:
        log.fail("sysinfo help parameter failed")


@logThis
def checkSysList():
    cmd=run_command("./cel-sysinfo-test -l",prompt='root@sonic')
    cmd1=run_command("./cel-sysinfo-test --list",prompt='root@sonic')
    count=0
    for i in var.sysinfo_list:
        if re.search(i,cmd,re.IGNORECASE):
            count+=1
    if count==len(var.sysinfo_list):
        log.success("sysinfo list parameter passed")
    else:
        log.fail("sysinfo list parameter failed")

    count=0
    for i in var.sysinfo_list:
        if re.search(i,cmd1,re.IGNORECASE):
            count+=1
    if count==len(var.sysinfo_list):
        log.success("sysinfo list parameter passed")
    else:
        log.fail("sysinfo list parameter failed")

@logThis
def checkbaseboardHelp():
    cmd=run_command("./cel-bb-cpld-test -h",prompt='root@sonic')
    count=0
    for i in var.bb_cpld_help:
        if re.search(i,cmd,re.IGNORECASE):
            count+=1
    if count==len(var.bb_cpld_help):
        log.success("baseboard cpld help parameter passed")
    else:
        log.fail("baseboard cpld help parameter failed")
    
    cmd=run_command("./cel-bb-cpld-test --help",prompt='root@sonic')
    count=0
    for i in var.bb_cpld_help:
        if re.search(i,cmd,re.IGNORECASE):
            count+=1
    if count==len(var.bb_cpld_help):
        log.success("baseboard cpld help parameter passed")
    else:
        log.fail("baseboard cpld help parameter failed")


@logThis
def checkBaseboardList():
    cmd=run_command("./cel-bb-cpld-test -l",prompt='root@sonic')
    count=0
    for i in var.bb_cpld_list:
        if re.search(i,cmd,re.IGNORECASE):
            count+=1
    if count==len(var.bb_cpld_list):
        log.success("baseboard list parameter passed")
    else:
        log.fail("baseboard list parameter failed")

    cmd=run_command("./cel-bb-cpld-test --list",prompt='root@sonic')
    count=0
    for i in var.bb_cpld_list:
        if re.search(i,cmd,re.IGNORECASE):
            count+=1
    if count==len(var.bb_cpld_list):
        log.success("baseboard list parameter passed")
    else:
        log.fail("baseboard list parameter failed")
 

@logThis
def checkSysInfoTest():
    cmd=run_command("./cel-sysinfo-test --all",prompt='root@sonic')
    if re.search("sysinfo test all end",cmd,re.IGNORECASE):
        log.success("sysinfo all parameter passed")
    else:
        log.fail("sysinfo all parameter failed")

@logThis
def checkSysInfoDevTest():
    cmd=run_command("./cel-sysinfo-test -r -d 1",prompt='root@sonic')
    if re.search("get dev.*fw info Passed",cmd,re.IGNORECASE):
        log.success("sysinfo dev test parameter passed")
    else:
        log.fail("sysinfo dev test parameter failed")



@logThis
def checkBaseboardTest():
    cmd=run_command("./cel-bb-cpld-test --all",prompt='root@sonic')
    if cmd.count('Passed')==123:
        log.success("baseboard all test passed")
    else:
        log.fail("baseboard all test failed")
    output=cmd.splitlines()
    last_wr=output[-3]
    verifyDiagTool()
    cmd4= run_command('./lpc_cpld_x64_64 blu r 0xa100',prompt='#')
    if not var.cpld_version1 in cmd4:
        raise Exception("scratch version check failed on port number 100")
    cmd5= run_command('./lpc_cpld_x64_64 blu r 0xa101',prompt='#')
    if not re.search(last_wr,cmd5,re.IGNORECASE):
        raise Exception("scratch version check failed on port 101")
    log.success("Scratch version matched")
    cmd6= run_command('./lpc_cpld_x64_64 blu r 0xa183',prompt='#')
    if not var.cpld_version3 in cmd6:
        raise Exception("scratch version check failed on port number 183")
    log.success('cpld version check passed')

@logThis
def checkBaseboardDevTest():
    cmd=run_command("./cel-bb-cpld-test -d 1",prompt='#')
    if re.search("cpld test : Passed",cmd,re.IGNORECASE):
        log.success('CPLD test passed for -d 1')
    else:
        raise Exception("Baseboard dev test failed")
    cmd1=run_command("./cel-bb-cpld-test --dev 2",prompt='#')
    if re.search("cpld test : Passed",cmd1,re.IGNORECASE):
        log.success('CPLD test passed for -d 2')
    else:
        raise Exception("Baseboard dev test failed")
    valo=re.search(r"0x\w?\w",cmd1).group()
    cmd2=run_command("./cel-bb-cpld-test -d 26",prompt='#')
    if  re.search("cpld test : Passed",cmd2,re.IGNORECASE):
        log.success('CPLD test passed for -d 26')
    else:
        raise Exception("Baseboard dev test failed")
    output=cmd2.splitlines()
    last_wr=output[-3]
    cmd3=run_command("./cel-bb-cpld-test -d 23",prompt='#')
    if  re.search("cpld test : Passed",cmd3,re.IGNORECASE):
        log.success('CPLD test passed for -d 23')
    else:
        raise Exception("Baseboard dev test failed")
    verifyDiagTool()
    print('The val0 is ',valo)
    cmd4= run_command('./lpc_cpld_x64_64 blu r 0xa100',prompt='#')
    val1=cmd4.split()
    val1=val1[-2]
    print('The val1 is ',val1)
    val9=eval(val1)
    val10=eval(valo)
    verifyDiagTool()
    if val9 == val10:
        log.success('Version is same as linux command')
    else:
        raise Exception("scratch version check failed on port number 100")
    cmd5= run_command('./lpc_cpld_x64_64 blu r 0xa101',prompt='#')
    if re.search(last_wr,cmd5,re.IGNORECASE):
        log.success("Scratch version  matched with linux command")
    else:
        raise Exception("scratch version check failed on port 101")
    cmd6= run_command('./lpc_cpld_x64_64 blu r 0xa183',prompt='#')
    if  val1 in cmd6:
        log.success('Cpld type and linux command output is same')
        
        raise Exception("Cpld type check failed on port number 183")




#################################################################################################################

@logThis
def checkDdrTest(a,b):
    ddr_stress=['pagesize is 4096']
       # 'want 164MB',
       # 'got  164MB'
    verifytool()
    if re.search("164",a):
        j = 1
    else:
        j=5
    print("The value of j is ",j)
    for i in range(1,j+1):
        ddr_stress.append('Loop 1/'+str(j)+':')
        ddr_stress.append('Stuck Address.*:.*ok')
        ddr_stress.append('Random Value        : ok')
        ddr_stress.append('Compare XOR         : ok')
        ddr_stress.append('Compare SUB         : ok')
        ddr_stress.append('Compare MUL         : ok')
        ddr_stress.append('Compare DIV         : ok')
        ddr_stress.append('Compare OR          : ok')
        ddr_stress.append('Compare AND         : ok')
        ddr_stress.append('Sequential Increment: ok')
        ddr_stress.append('Solid Bits          : ok')
        ddr_stress.append('Block Sequential    : ok')
        ddr_stress.append('Checkerboard        : ok')
        ddr_stress.append('Bit Spread          : ok')
        ddr_stress.append('Bit Flip            : ok')
        ddr_stress.append('Walking Ones        : ok')
        ddr_stress.append('Walking Zeroes      : ok')
        ddr_stress.append('8-bit Writes        : ok')
        ddr_stress.append('16-bit Writes       : ok')

    ddr_stress.append('Done')
    print("The value of ddr list is",ddr_stress)
    c1=run_command(a,timeout=str(b),prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(c1,ddr_stress)

@logThis
def ChangetoAdmin():
        run_command("exit")


###########################################################################################################

@logThis
def checkFpgaUpper():
    result=[]
    updater_info_dict = CommonLib.get_swinfo_dict("BRIXIA_DIAG")
    ver1= updater_info_dict.get("fpga_version").get("NEW_VER","")
    c1=run_command('cat /sys/devices/gfpga-platform/majorrevision',prompt ='root@sonic')
    c2=run_command('cat /sys/devices/gfpga-platform/minorrevision',prompt ='root@sonic')
    result.extend(re.findall(r'[0-9]+',c1))
    result.extend(re.findall(r'[0-9]+',c2))
    final='.'.join(result)
    patt = 'FPGA Version: '+final
    c4=run_command('./cel-sysinfo-test --all',prompt ='root@sonic')
    if re.search(patt,c4):
        log.success('Version is correct')
    else:
        log.fail('Version is incorrect')



@logThis
def checkDowngradeUpgrade(val):
    run_command('cp /home/admin/*.bin ../tools/firmware/',prompt='admin@sonic|root@sonic')
    run_command('cp /home/admin/*.vme ../tools/firmware/',prompt='admin@sonic|root@sonic')
    run_command('ls ../tools/firmware',prompt='admin@sonic|root@sonic')
    updater_info_dict = CommonLib.get_swinfo_dict("BRIXIA_DIAG")
    filename = updater_info_dict.get("fpga_version").get(val+"_IMAGE","")
    ver = updater_info_dict.get("fpga_version").get(val+"_VER","")
    patt = 'FPGA Version: '+ver
    print("The version is ",filename)
    c1=run_command('./cel-upgrade-test --update --dev 3 --file ../tools/firmware/'+filename,prompt ='root@sonic')
    if re.search('Result: Upgrade Firmware --> Passed',c1):
        log.success("Firmware upgrade successful")
    else:
        log.fail("Firmware failed...Aborting...........")
        exit
    log.info('Check if fpga is correct after upgrade/downgrade')
    powerCycleDevice()   ;#Powercycle after operation
    verifyDiagToolPath()
    c2=run_command('./cel-sysinfo-test --d 7',prompt ='root@sonic') ;#Check if fpga is correct after upgrade/downgrade
    if re.search(patt,c2):
        log.success("Correct version installed") 
    else:
        log.fail("The version is incorrect")



@logThis
def checkSystemInfoTest():
    m2=run_command(' ./cel-upgrade-test --list',prompt ='root@sonic')
    m3=m2.splitlines()
    l1=len(var.upgrade_list)
    print('the type of m2',type(m2))
    #print('the type of',type(var.upgrade_list))
    count=0
    for x in var.upgrade_list:
        for y in m3:
            if x == y:
                count=count+1
                print("match",x)
    if l1 == count:
        log.success("Test passed")
    else:
        log.fail("Test failed")
    print("Count:",count)
    print("length:",l1)
    run_command("exit",prompt="root@sonic")
    run_command("exit",prompt="root@sonic")



#################################################################################################

##################################################################################################################################
##TCS 34

@logThis
def checkAllTests():
    cmd_lst= ['./cel-eeprom-test -w -d 5 -t tlv -A fan_pn -D \"GFM0848VW\"', 
             './cel-eeprom-test -w -d 6 -t tlv -A fan_pn -D \"GFM0848VW\"', 
             './cel-eeprom-test -w -d 7 -t tlv -A fan_pn -D \"GFM0848VW\"',
             './cel-eeprom-test -w -d 8 -t tlv -A fan_pn -D \"GFM0848VW\"', 
             './cel-eeprom-test -w -d 5 -t tlv -A fan_maxspeed -D \"15400\"',  
             './cel-eeprom-test -w -d 6 -t tlv -A fan_maxspeed -D \"15400\"', 
             './cel-eeprom-test -w -d 7 -t tlv -A fan_maxspeed -D \"15400\"',
             './cel-eeprom-test -w -d 8 -t tlv -A fan_maxspeed -D \"15400\"']
    for x in cmd_lst:
        cmd1=run_command(x,prompt='root@sonic')
        time.sleep(3)
    run_command('docker exec -ti pmon supervisorctl stop thermalctld',prompt ='root@sonic',timeout=10)
    run_command('cp /home/all.yaml /usr/local/cls_diag/configs/.',prompt ='root@sonic') 
    run_command('ls -la log/',prompt ='root@sonic')
    c1=run_command('./cel-all-test --all',prompt ='root@sonic',timeout=1800)
    device.sendMsg('reset \n')
    device.read_until_regexp('root@sonic',timeout=20)
    patt = ['Failed.*0.*Passed:18.*Total.*18']
    CommonKeywords.should_match_ordered_regexp_list(c1,patt)
    c2=run_command('ls -la log/',prompt ='root@sonic')
    if re.search(r'[a-z]+\_[0-9]{4}\-[0-9]{2}\-[0-9]{2}\-[0-9]{2}\-[0-9]{2}\-[0-9]{2}',c2):
        log.success('Test log found')
    else:
        log.fail('Test log missing')
    run_command('exit')
################################################################################################################################

#Tcs35

@logThis
def checkStructure():
    #val='find . | sed -e \"s/[^-][^\/]*\// |/g\" -e \"s/|\([^ ]\)/|-\1/\" '
    val='find . | sed -e "s/[^-][^\/]*\// |/g" '
    run_command('cd /usr/local/cls_diag')
    c1=run_command(val)
    CommonKeywords.should_match_ordered_regexp_list(c1,var.struct)
    log.success('Structure of diagnostic package is same as user manual')


@logThis
def checkDiagOperations():
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    flag=0
    run_command('cd /usr/local/cls_diag',prompt ='root@sonic')

    c2=run_command('ls -la',prompt ='root@sonic')
    if not re.search('README.txt',c2):
        log.success('README.txt not available as expected')
    else:
        log.fail("Didnt expect README.txt")

    run_command('cd configs',prompt ='root@sonic')
    c3=run_command('cat *.yaml',prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(c3,var.config_var)
    log.success('All information in the yaml file shows correct information')

    run_command('cd /usr/local/cls_diag/tools',prompt ='root@sonic')
    c4=run_command('ls -la | grep -i margin',prompt ='root@sonic')
    for x in var.power_margin:
        if x not in c4:
            flag=1
    if flag == 1:
        log.fail("Certain files  not found")
    else:
        log.success("All files are intact")

    c5=run_command('ls -la | grep -i fusion',prompt ='root@sonic')
    if var.fusion not in c5:
        log.fail("Certain files  not found")
    else:
        log.success("All files are intact")

    c6=run_command('cat pmbus_margin.py|grep -i SCRIPT_VERSION',prompt ='root@sonic')
    if re.search(var.scr_pat,c6):
        log.success("Script version is correct")
    else:
        log.fail('Script version is incorrect')
    run_command('exit')


########################################################################################################################################

#tcs 36
@logThis
def checkStorageStress():
    run_command(" cd /usr/local/cls_diag/tools/stress")
    cmd1=run_command("./SSD_test.sh 300 test_SSD.log",timeout= 600)
    if re.search(".*SSD test done",cmd1,re.IGNORECASE) and not re.search('rror',cmd1):
        log.success(" Storage test passed")
    else:
        log.fail("Storage  test failed")
    c2=run_command('cat test_SSD.log')
    m= re.search('util\=[0-9]+\.[0-9]+',c2)
    j =m.group().split('=')[1]
    if float(j) > 70.0:
        log.success('Disk stats utilization more than 70%')
    else:
        log.fail('Disk stats utilization is less than 70%')
    run_command("rm -rf test_SSD.log")
    c3=run_command('ls -la')
    if "test_SSD" not in c3:
        log.success('File test_SSD has been deleted successfully')
    else:
        log.fail("test_SSD not deleted")


######################################################################################################################################
#tcs 37

@logThis
def checkCpuStress():
    patt='0 errors, 0 warnings'
    device.sendMsg('sudo -s \n')
    run_command(" cd /usr/local/cls_diag/tools/stress",prompt='root@sonic',timeout=5)
    cmd = "./CPU_test.sh  \n"
    c1=device.sendMsg(cmd)
    time.sleep(600)
    #c2=device.read_until_regexp('.*Please read stress.txt',timeout=120)
    pass_count = 0
    for i in range(3):
        c3=device.sendMsg(Const.KEY_CTRL_C)
        try:
            c5=device.read_until_regexp('admin\@sonic.*|root\@sonic.*', timeout=3)
            pass_count += 1
            break
        except Exception:
            continue
    if pass_count:
        log.success('cpu stress test passed')
    else:
        raise Exception('cpu stress test failed')
    time.sleep(5)
    #c2=run_command('cat test.log \n')
    time.sleep(2)
    print('The value os c2 is :',c5)
    if re.search(patt,c5):
        log.success('Stress passed with 0 errors')
    else:
        log.fail('Stress test failed with errors')
    run_command('cat CPU_test.sh')
    device.sendMsg('rm -rf test.log')
    device.sendMsg('exit')

#########################################################################################################################

@logThis
def checkRtcNew():
#The output of date,hwclock and dmidecode are different and hence not checking
    #device.sendCmd('sudo -s','root@sonic',timeout =20)
    #device.sendCmd('reboot', 'sonic login:',timeout=450)
    #device.loginToDiagOS()
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    verifyDiagToolPath()

    c1=run_command('dmidecode -t bios',prompt='root@sonic')
    c2=run_command('date',prompt='root@sonic')
    c4=run_command('./cel-rtc-test -r',prompt ='root@sonic')
    c3=run_command('hwclock',prompt ='root@sonic')
    c3=c3.split()[0]
    if re.search(c3,c4):
        log.success('RTC time is correct')
    else:
        log.fail('RTC time failed to display correct time ')

    if re.search('rror',c3):
        log.fail('Error is time read')

@logThis
def checkRtcStat():
    time.sleep(30)
    c1=run_command('./cel-rtc-test --read',prompt ='root@sonic')
    run_command('cp /usr/local/cls_diag/configs/rtc.yaml /home/',prompt ='root@sonic')
    c2=run_command('./cel-rtc-test -r -f /home/rtc.yaml',prompt ='root@sonic')
    c3=run_command('hwclock',prompt ='root@sonic')
    c1=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c1).group()
    c2=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c2).group()
    c3=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c3).group()
    if c1 == c2  ==  c3:
        log.success('Values are correct for -r and -r -f /home/rtc.yaml')
    else:
        log.fail('Values are incorrect for -r and -r -f /home/rtc.yaml')





@logThis
def checkRtcFile():
    c2=run_command('./cel-rtc-test --read',prompt ='root@sonic')
    c1=run_command('./cel-rtc-test -l --f /home/rtc.yaml',prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(c1,var.rtc_list)
    c3=run_command('hwclock',prompt ='root@sonic')
    c2=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c2).group()
    c4=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c3).group()
    print('The value os c2 is ',c2)
    print('The value of c4:',c4)
    if c2 == c4:
        log.success('Values are correct')
    else:
        log.fail('Values are incorrect')

    c5=run_command('./cel-rtc-test -w -D "20300430 235959"',prompt ='root@sonic')
    c6=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c5).group()
    c3=run_command('./cel-rtc-test -r',prompt ='root@sonic')
    c4=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c3).group()

    if c6 == c4:
        log.success('Values are correct')
    else:
        log.fail('Values are incorrect')

    c7=run_command('./cel-rtc-test --write --data "20211231 235959" --file /home/rtc.yaml',prompt ='root@sonic')
    c8=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c7).group()
    c3=run_command('hwclock',prompt ='root@sonic')
    c4=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c3).group()
    if c8 == c4:
        log.success('Values are correct')
    else:
        log.fail('Values are incorrect')
    c9= run_command('./cel-rtc-test -r',prompt ='root@sonic')
    c10=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c9).group()
    #c4=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c10).group()
    if c10 == c4:
         log.success('Values are correct')
    else:
         log.fail('Values are incorrect')

@logThis
def checkRtcOperation():
    c1=run_command('./cel-rtc-test -r',prompt='root@sonic')
    c2=run_command('./cel-rtc-test -r --file /home/rtc.yaml',prompt='root@sonic')
    c3=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c1).group()
    c4=re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',c2).group()
    if c3==c4:
        log.success('RTC test passed')
    else:
        log.fail('RTC test failed')
    cmd=run_command('reboot',prompt='sonic login:',timeout=300)
    device.loginToDiagOS()
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    run_command('hwclock',prompt='root@sonic')
############################################################################################################
@logThis
def checkCpuStats():
    cmd1= run_command('lscpu',prompt='root@sonic')
    cmd2=run_command('cat /proc/cpuinfo',prompt='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(cmd1,var.lscpu)
    CommonKeywords.should_match_ordered_regexp_list(cmd2,var.cpu_proc)
    cmd3=''.join(cmd2)
    z=re.findall('MHz[:][\s]+[0-9]+',cmd2)
    flag=0
    for x in z:
        if int(x.split()[1]) >= 3000:
            flag=1
    if flag == 0:
        log.success('The Cpu mhz is under 3000 MHz')
    else:
        log.fail('The Cpu mhz is above 3000 MHz')

    c2=run_command('./cel-cpu-test --all',prompt='root@sonic')
    c3=[]
    c3.append(re.search('CPU Thread[:][\s]+[0-9]+',c2).group().split()[2])
    c3.append(re.search('CPU Vendor[:][\s]+[0-9A-Za-z]+',c2).group().split()[2])
    c3.append(re.search('CPU Model[:][\s]+\w+\W+?\w+\W+?\w+\W+\w+\W+\w+\W+\w+\W+\w+\.?\w+',c2).group().split()[2])
    print(c3)
    cmd3=cmd1.splitlines()
    c4=[]
    c4.append(cmd3[5].split()[1])
    c4.append(cmd3[11].split()[2])
    c4.append(cmd3[14].split()[2]+cmd3[14].split()[3]+cmd3[14].split()[4]+cmd3[14].split()[5]+cmd3[14].split()[6]+cmd3[14].split()[7])
    print(c4)
    if c3 == c4:
        log.success("Result between linux command and diag tools are same")
    else:
        log.fail("Result between linux command and diag tools are different")

@logThis
def checkCpuFileOperation():
    run_command('cp /usr/local/cls_diag/configs/cpu.yaml  /home/',prompt='root@sonic')
    run_command('cd /home',prompt='root@sonic')
    time.sleep(2)
    run_command('sed -i \'s/cpu_cores:  16/cpu_cores:  8/g\' cpu.yaml',prompt='root@sonic')
    run_command('cd /usr/local/cls_diag/bin',prompt='root@sonic')
    run_command('./cel-cpu-test -l --file /home/cpu.yaml',prompt='root@sonic')
    c1=run_command('./cel-cpu-test --all -f /home/cpu.yaml',prompt='root@sonic')
    if re.search('CPU test : FAILED',c1,re.IGNORECASE):
        log.success("Test failed as expected")
    else:
        log.fail("Test passed but expected to fail")

    run_command('exit')
###########################################################################################################

#########################################################################################################################
#BRIXIA_DIAG_TC_08_I2C_Test
@logThis
def verifyi2cport(mod,i2cbus_port):
    log.debug('Entering procedure verifyi2cport: %s\n' % (str(locals())))
    for key, value in i2cbus_port.items():
        if len(key) == 1 and key == '0':
            cmd_output = run_command('./cel-' + mod + '-test --scan --bus ' + key, prompt='root@sonic')
            continue
        cmd_output = run_command('./cel-' + mod + '-test --s --bus ' + key, prompt='root@sonic')
        for i in value:
            if re.search(i, cmd_output):
                log.success(f"Successfully verified I2C port on bus {key}")
            else:
                log.fail(f"FAIL!! verified I2C port on bus {key}")
                raise RuntimeError(f"FAIL!! verified I2C port on bus {key}")

@logThis
def Checki2cdevice(detectdevice_lst):
    log.debug('Entering procedure Checki2cdevice: %s\n' % (str(locals())))
    for key, value in detectdevice_lst.items():
        cmd_output = run_command('i2cdetect -y ' + key, prompt='root@sonic')
        for i in value:
            if re.search(i, cmd_output):
                log.success(f"Successfully I2C detect on bus {key}")
            else:
                log.fail(f"FAIL!! verified I2C detect on bus {key}")
                raise RuntimeError(f"FAIL!! verified I2C detect on bus {key}")

@logThis
def Readi2cdeviceviaDiagcommand(mod,i2cdiagcmd):
    log.debug('Entering procedure Readi2cdeviceviaDiagcommand: %s\n' % (str(locals())))
    log.debug("111111111111")
    c1=run_command('./cel-i2c-test --read --bus 0 --addr 0x48 --reg16 0x00',prompt='root@sonic')
    if not re.search('0xff',c1) and re.search('I2C read : Passed',c1):
        log.fail('I2c read failed for bus 0')
    for listvalue in i2cdiagcmd:
        cmd_output = run_command('./cel-' + mod + '-test --read --bus ' + listvalue[0] + ' --addr ' + listvalue[1] + ' --reg ' + listvalue[2],prompt='root@sonic')
        pattern_result1 = listvalue[3]
        pattern_result2 = "PASSED"
        if not (re.search(pattern_result1, cmd_output) and re.search(pattern_result1, cmd_output) and re.search(r"ERROR", cmd_output)):
            log.success(f"Successfully Read i2c device bus {listvalue[0]} via Diag command")
        else:
            log.fail(f"FAIL!! Read i2c device bus {listvalue[0]} via Diag command")
            #raise RuntimeError(f"FAIL!! Read i2c device bus {listvalue[0]} via Diag command")

@logThis
def verifyi2cdetect(mod,i2cbus_device):
    log.debug('Entering procedure verifyi2cdetect: %s\n' % (str(locals())))
    for key, value in i2cbus_device.items():
        cmd_output = run_command("i2cdetect -r -y " + key, prompt='root@sonic')
        for i in value:
            if re.search(i, cmd_output):
                log.success(f"Successfully I2C detect by using option on bus {key}")
            else:
                log.fail(f"FAIL!! verified I2C detect by using option on bus {key}")
                raise RuntimeError(f"FAIL!! verified I2C detect by using option on bus {key}")

########################################################################################################################

#TC13
@logThis
def checkPsuSensorAndPsuFile():
    cmd=run_command("sensors",prompt='#',timeout=100)
    if re.search("Error.*",cmd):
        raise Exception("PSU Sensor check failed")
    cmd1=run_command("./cel-psu-test --list --file ../configs/psu_B0.yaml",prompt='#')
    cmd2=run_command("./cel-psu-test --all -f ../configs/psu_B0.yaml",prompt='#')
    if not re.search("POWER test : Passed",cmd2,re.IGNORECASE):
        raise Exception("Sensor test failed")
    log.success("sensor test passed")
    cmd3=run_command("./cel-psu-test --all --file ../configs/second_source/psu_B0_flex.yaml",prompt='#',timeout=60)
    if  re.search("POWER test : FAILED",cmd3,re.IGNORECASE):
        log.success('Power test failed as expected')
    else:
        raise Exception("Sensor test failed")
    cmd4=run_command("./cel-psu-test --all --file ../configs/second_source/psu_B0_astersyn.yaml",prompt='#',timeout=60)
    if  re.search("POWER test : FAILED",cmd4,re.IGNORECASE):
        log.success('Sensor test failed as expected')
    else:
        raise Exception("Sensor test failed")
    run_command("cd /",prompt="root@sonic.*",timeout=5)


########################################################################################################################33333
#tcs30




@logThis
def checkBasic():
    global fr_v1
    fr_v1='0xb'
    fr_v2='0x17'
    device.sendCmd('sudo -s','root@sonic',timeout =20)
    a1=run_command("uname -a",prompt='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(a1,var.ver_1)
    j1= var.brixia_ver.replace('-OS-','.')
    a2=run_command('show version',prompt='root@sonic',timeout =20)
    print('The brixia is ',j1)
    if re.search(j1,a2):
        log.success('Image is correct')
    else:
        log.fail('Image is incorrect')
    verifyDiagTool()
    a3=run_command('./lpc_cpld_x64_64 blu r 0xa100',prompt='root@sonic')
    a4=run_command('./lpc_cpld_x64_64 blu r 0xa1e0',prompt='root@sonic')
    print('The value of a3',a3)
    print('The value of a4',a4)
    if re.search(fr_v1,a3) and re.search(fr_v2,a4):
        log.success('Values are correct:')
    else:
        log.fail('Values are incorrect')


@logThis
def checkSoftwareInfo():
    updater_info_dict = CommonLib.get_swinfo_dict("BRIXIA_DIAG")
    ver1= updater_info_dict.get("fpga_version").get("NEW_VER","")
    j1= var.brixia_ver.replace('-OS-','.')
    verifyDiagToolPath()
    s1=run_command('./cel-sysinfo-test -d 1',prompt='root@sonic')
    s2=run_command('./cel-sysinfo-test -d 2',prompt='root@sonic')
    s3=run_command('./cel-sysinfo-test -d 3',prompt='root@sonic')
    s4=run_command('./cel-sysinfo-test -d 4',prompt='root@sonic')
    s5=run_command('./cel-sysinfo-test --dev 5',prompt='root@sonic')
    s6=run_command('./cel-sysinfo-test --dev 6',prompt='root@sonic')
    s7=run_command('./cel-sysinfo-test --dev 7',prompt='root@sonic')
    s8=run_command('./cel-sysinfo-test --dev 8',prompt='root@sonic')
    s9=run_command('./cel-sysinfo-test --dev 9',prompt='root@sonic')

    CommonKeywords.should_match_ordered_regexp_list(s4,var.ver_1)

    if re.search(ver1,s7):
        log.success('version is correct')
    else:
        log.fail('Version is incorrect')

    if re.search(var.sys_version,s5):
        log.success('Diag version is correct')
    else:
        log.fail('Diag Version is incorrect')

    if re.search(j1,s6):
        log.success('Image is correct')
    else:
        log.fail('Image not correct')

    run_command('exit',prompt='root@sonic')
    run_command('exit')
#####################################################################################################################
#TC 19
@logThis
def checkEepromDump():
    cmd=run_command('./cel-eeprom-test --dump --dev all --type tlv',prompt='root@sonic')
    for i in range(1,9):
        cmd=run_command("./cel-eeprom-test --dump -d {} -t tlv".format(i),prompt='root@sonic')
    eepromDataCheck()

@logThis
def checkEepromRead():
    run_command('./cel-eeprom-test --read --dev all --type tlv',prompt='root@sonic')
    for i in range(1,9):
        cmd=run_command("./cel-eeprom-test -r -d {} -t tlv".format(i),prompt='root@sonic')
    eepromDataCheck()

@logThis
def eepromDataCheck():
    eepat1=var.eeprom_mod4+var.eeprom_data1
    eepat2=var.eeprom_mod1 +  var.eeprom_data3
    eepat3=var.eeprom_mod1 + var.eeprom_data2
    eepat4=var.eeprom_mod2 + var.eeprom_data1
    eepat5=var.eeprom_mod3 + var.eeprom_data2
    if not eepat1 and eepat2 and eepat3 and eepat4 and eepat5 in cmd:
        raise Exception("EEPROM data test failed!!")
    log.success("EEPROM data test passed")

@logThis
def checkEepromTest():
    cmd=run_command("./cel-eeprom-test --all",prompt='root@sonic',timeout=200)
    eepromDataCheck()

@logThis
def checkEepromData():
    flag = 0 
    cmd=run_command('./cel-eeprom-test --dump --dev all --type tlv',prompt='root@sonic')
    cmd_lst=['hd /sys/bus/i2c/devices/i2c-1/1-0050/eeprom-ro',
             'hd /sys/bus/i2c/devices/i2c-1/1-0051/eeprom-ro',
             'hd /sys/bus/i2c/devices/i2c-19/19-0051/eeprom-ro',
             'hd /sys/bus/i2c/devices/i2c-10001/10001-0050/eeprom-ro',
             'hd /sys/bus/i2c/devices/i2c-12/12-0050/eeprom-ro',
             'hd /sys/bus/i2c/devices/i2c-13/13-0050/eeprom-ro',
             'hd /sys/bus/i2c/devices/i2c-14/14-0050/eeprom-ro',
             'hd /sys/bus/i2c/devices/i2c-15/15-0050/eeprom-ro'
            ]
    #output=run_command(cmd_lst,prompt='root@sonic:/usr/local/cls_diag/bin#')
    for x in cmd_lst:
        cmd1=run_command(x,prompt='root@sonic')
        if re.search(cmd1,cmd):
            flag =1
    if flag == 1 :
        log.success('Eeprom dumpdata same as output of hd data')
    else:
        log.fail('Eeprom dumpdata is not same as output of hd data')

@logThis
def removeEepromData():
    cmd_lst=[
            'echo 0 > /sys/bus/i2c/devices/i2c-1/1-0050/write_p',
            'echo 1 > /sys/bus/i2c/devices/i2c-1/1-0050/eeprom_erase',
            'echo 0 > /sys/bus/i2c/devices/i2c-1/1-0051/write_p',
            'echo 1 > /sys/bus/i2c/devices/i2c-1/1-0051/eeprom_erase',
            'echo 0 > /sys/bus/i2c/devices/i2c-19/19-0051/write_p',
            'echo 1 > /sys/bus/i2c/devices/i2c-19/19-0051/eeprom_erase',
            'echo 0 > /sys/bus/i2c/devices/i2c-10001/10001-0050/write_p',
            'echo 1 > /sys/bus/i2c/devices/i2c-10001/10001-0050/eeprom_erase',
            'echo 0 > /sys/bus/i2c/devices/i2c-12/12-0050/write_p',
            'echo 1 > /sys/bus/i2c/devices/i2c-12/12-0050/eeprom_erase',
            'echo 0 > /sys/bus/i2c/devices/i2c-13/13-0050/write_p',
            'echo 1 > /sys/bus/i2c/devices/i2c-13/13-0050/eeprom_erase',
            'echo 0 > /sys/bus/i2c/devices/i2c-14/14-0050/write_p',
            'echo 1 > /sys/bus/i2c/devices/i2c-14/14-0050/eeprom_erase',
            'echo 0 > /sys/bus/i2c/devices/i2c-15/15-0050/write_p',
            'echo 1 > /sys/bus/i2c/devices/i2c-15/15-0050/eeprom_erase'
            ]
    output=run_command(cmd_lst,prompt='root@sonic:/usr/local/cls_diag/bin#',timeout=50)
    cmd=run_command('./cel-eeprom-test --dump -d all --type tlv',prompt='root@sonic:/usr/local/cls_diag/bin#',timeout=60)
    pat1=var.eeprom_mod1 + var.eeprom_rdata1
    pat2=var.eeprom_mod1 + var.eeprom_rdata2
    pat3=var.eeprom_mod2 + var.eeprom_rdata2
    pat4=var.eeprom_mod3 + var.eeprom_rdata2
    pat5=var.eeprom_mod4 + var.eeprom_rdata2
    if not pat1 and pat2 and pat3 and pat4 and pat5 in cmd:
        raise Exception("Failed to remove eeprom data")
    log.success("Removed Eeprom data successfully")
    checkAllEepromData()
@logThis
def writeTlvInfo():
    for i in range (1,3):
        cmd_lst=[
            './cel-eeprom-test -w -d {} -t tlv -A pn -D "R3152-M0001-01"'.format(i),
            './cel-eeprom-test -w -d {} -t tlv -A sn -D "R1207-G0002-01XXXXXXXX"'.format(i),
            './cel-eeprom-test -w -d {} -t tlv -A mac_address -D "00:1A:11:01:02:03"'.format(i),
            './cel-eeprom-test -w -d {} -t tlv -A mfg_date -D "2042"'.format(i),
            './cel-eeprom-test -w -d {} -t tlv -A card_type -D "0x54"'.format(i),
            './cel-eeprom-test -w -d {} -t tlv -A hw_revision -D "0x01"'.format(i),
            './cel-eeprom-test -w -d {} -t tlv -A board_pn -D "ABC1234567-01"'.format(i),
            './cel-eeprom-test -w -d {} -t tlv -A board_sn -D "161812345678901"'.format(i),
            './cel-eeprom-test -w -d {} -t tlv -A mac_count -D "128"'.format(i),
            './cel-eeprom-test -w -d {} -t tlv -A psu_type -D "0xDC"'.format(i)]
        output=run_command(cmd_lst,prompt='root@sonic:/usr/local/cls_diag/bin#')
        if "Error" in output:
            raise Exception("cmd failed")
    cmd_lst2=[
            './cel-eeprom-test -w -d 3 -t tlv -A product_name -D "BX"',
            './cel-eeprom-test -w -d 3 -t tlv -A pn -D "1075455-02"',
            './cel-eeprom-test -w -d 3 -t tlv -A sn -D "TMBCTH194201434"',
            './cel-eeprom-test -w -d 3 -t tlv -A mac_address -D "00:1A:11:44:55:66"',
            './cel-eeprom-test -w -d 3 -t tlv -A mfg_date -D "2042"',
            './cel-eeprom-test -w -d 3 -t tlv -A card_type -D "0x60"',
            './cel-eeprom-test -w -d 3 -t tlv -A hw_revision -D "0x01"',
            './cel-eeprom-test -w -d 3 -t tlv -A board_pn -D "1075637-02"',
            './cel-eeprom-test -w -d 3 -t tlv -A board_sn -D "abc123456"',
            './cel-eeprom-test -w -d 3 -t tlv -A mac_count -D "CBX07248404"',
            './cel-eeprom-test -w -d 3 -t tlv -A psu_type -D "0xDC"']
    output=run_command(cmd_lst2,prompt='root@sonic:/usr/local/cls_diag/bin#')
    if "Error" in output:
            raise Exception("cmd failed")
    cmd_lst3=[
            './cel-eeprom-test -w -d 4 -t tlv -A mfg_date -D "2042"',
            './cel-eeprom-test -w -d 4 -t tlv -A card_type -D "0x61"',
            './cel-eeprom-test -w -d 4 -t tlv -A hw_revision -D "0x01"',
            './cel-eeprom-test -w -d 4 -t tlv -A board_pn -D "R3152-M0001-01"',
            './cel-eeprom-test -w -d 4 -t tlv -A board_sn -D "12345678"',
            './cel-eeprom-test -w -d 4 -t tlv -A psu_type -D "0xDC"',
            './cel-eeprom-test -w -d 4 -t tlv -A subassy_pn -D "ABC1234567-01"',
            './cel-eeprom-test -w -d 4 -t tlv -A subassy_sn -D "161812345678901"'
            ]
    output=run_command(cmd_lst3,prompt='root@sonic:/usr/local/cls_diag/bin#')
    if "Error" in output:
            raise Exception("cmd failed")
    for i in range(5,9):
        cmd_lst4=[
                './cel-eeprom-test -w -d {} -t tlv -A pn -D "R1257-F0002-01"'.format(i),
                './cel-eeprom-test -w -d {} -t tlv -A sn -D "12345678"'.format(i),
                './cel-eeprom-test -w -d {} -t tlv -A mfg_date -D "2042"'.format(i),
                './cel-eeprom-test -w -d {} -t tlv -A card_type -D "0x64"'.format(i),
                './cel-eeprom-test -w -d {} -t tlv -A hw_revision -D "0x01"'.format(i),
                './cel-eeprom-test -w -d {} -t tlv -A board_pn -D "112233-44"'.format(i),
                './cel-eeprom-test -w -d {} -t tlv -A board_sn -D "abc123456"'.format(i),
                './cel-eeprom-test -w -d {} -t tlv -A psu_type -D "0xDC"'.format(i),
                './cel-eeprom-test -w -d {} -t tlv -A fan_maxspeed -D "22000"'.format(i),
                './cel-eeprom-test -w -d {}  -t tlv -A fan_pn -D "R40W12BGNL9"'.format(i)
            ]
        output=run_command(cmd_lst4,prompt='root@sonic:/usr/local/cls_diag/bin#')
        if "Error" in output:
            raise Exception("cmd failed")
    cmd1= run_command('./cel-eeprom-test -r -d all --type tlv',prompt='root@sonic:/usr/local/cls_diag/bin#',timeout=100)
    time.sleep(30)
    powerCycleDevice()
    verifyDiagToolPath()
    time.sleep(30)
    cmd2= run_command('./cel-eeprom-test -r -d all --type tlv',prompt='root@sonic:/usr/local/cls_diag/bin#',timeout=100)
    time.sleep(30)
    for each in cmd1.splitlines():
        if not re.search(each,cmd2):
            raise Exception("EEprom data not matching")
    log.success("EEprom data matched")

@logThis
def checkAllEepromData():
    cmd= run_command('./cel-eeprom-test -r -d all --type tlv',prompt='root@sonic:/usr/local/cls_diag/bin#',timeout=100)

@logThis
def programEeprom():
    cmd_lst=[
            './cel-eeprom-test --list --file ../configs/eeprom.yaml',
            './cel-eeprom-test --all -f ../configs/eeprom.yaml']
    output=run_command(cmd_lst,prompt='root@sonic:/usr/local/cls_diag/bin#',timeout=100)
    time.sleep(30)
    cmd1= run_command('./cel-eeprom-test -r -d all --type tlv',prompt='root@sonic:/usr/local/cls_diag/bin#',timeout=100)
    time.sleep(30)
    cmd=run_command('reboot',prompt='sonic login:',timeout=300)
    device.loginToDiagOS()
    verifyDiagToolPath()
    time.sleep(30)
    cmd2= run_command('./cel-eeprom-test -r -d all --type tlv',prompt='root@sonic:/usr/local/cls_diag/bin#',timeout=100)
    time.sleep(30)
    for each in cmd1.splitlines():
        if not re.search(each,cmd2):
            raise Exception("EEprom data not matching")
    log.success("EEprom data matched")
################################################################################################################################################
#TC23
@logThis
def ReadMacId():
    run_command('ifconfig -a',prompt='#',timeout=10)
    cmd1=run_command("./eeupdate64e /ALL",prompt='root@sonic')
@logThis
def readAllMac():
    fail=0
    c1=run_command('ifconfig -a',prompt='#',timeout=10)
    c2=re.findall('([A-Fa-f0-9:]{17})',c1)
    c3=[x.replace(":",'').upper() for x in c2]
    for i in range(1,7):
        cmd2=run_command("./eeupdate64e /NIC={} /MAC_DUMP".format(i),prompt='root@sonic')
        m=re.search('[A-Fa-f0-9]{12}',cmd2).group()
        if m not in c3:
            fail=1
        if "Error" in cmd2:
            raise Exception("Read Mac failed!!")
    if fail == 0:
        log.success('MAC address from diag tools is same as ifconfig interface')
    else:
        log.fail('MAC address from diag tools is not same as ifconfig interface')
@logThis
def WriteMacId():
    cmd_lst=[
           './eeupdate64e /NIC=1 /MAC=00A0C9112211',
           './eeupdate64e /NIC=2 /MAC=00A0C9112212',
           './eeupdate64e /NIC=3 /MAC=00A0C9112213',
           './eeupdate64e /NIC=4 /MAC=00A0C9112214',
           './eeupdate64e /NIC=5 /MAC=E45E1B00AABB',
           './eeupdate64e /NIC=6 /MAC=E45E1B001122'
            ]
    cmd1=run_command(cmd_lst,prompt='root@sonic',timeout=80)
    for i in range (1,7):
        pat="{}: Updating Checksum and CRCs...Done.".format(i)
        if not re.search(pat,cmd1):
            raise Exception("Modify Mac address failed")
    log.success("Write MAC Pattern Successfull")
    powerCycleDevice()

@logThis
def WriteNewMacId():
    cmd_lst=[
           './eeupdate64e /NIC=1 /MAC=00A0C7112211',
           './eeupdate64e /NIC=2 /MAC=00A0C7112212',
           './eeupdate64e /NIC=3 /MAC=00A0C7112213',
           './eeupdate64e /NIC=4 /MAC=00A0C7112214',
           './eeupdate64e /NIC=5 /MAC=E45E1B00AACC',
           './eeupdate64e /NIC=6 /MAC=E45E1B002233'
            ]
    cmd1=run_command(cmd_lst,prompt='root@sonic',timeout=80)
    for i in range (1,7):
        pat="{}: Updating Checksum and CRCs...Done.".format(i)
        if not re.search(pat,cmd1):
            raise Exception("Modify Mac address failed")
    log.success("Write MAC Pattern Successfull")
    powerCycleDevice()


@logThis
def getMacAdd():
    cmd2=run_command("./eeupdate64e /NIC=1 /MAC_DUMP",prompt='root@sonic')
    pat="1: LAN MAC Address is (.+)"
    mat1=re.search(pat,cmd2).group().split()[-1].strip('.')
    if not mat1:
        raise Exception("Failed")
    cmd2=run_command("./eeupdate64e /NIC=2 /MAC_DUMP",prompt='root@sonic')
    pat="2: LAN MAC Address is (.+)"
    mat2=re.search(pat,cmd2).group().split()[-1].strip('.')
    if not mat2:
        raise Exception("Failed")
    cmd2=run_command("./eeupdate64e /NIC=3 /MAC_DUMP",prompt='root@sonic')
    pat="3: LAN MAC Address is (.+)"
    mat3=re.search(pat,cmd2).group().split()[-1].strip('.')
    if not mat3:
        raise Exception("Failed")
    cmd2=run_command("./eeupdate64e /NIC=4 /MAC_DUMP",prompt='root@sonic')
    pat="4: LAN MAC Address is (.+)"
    mat4=re.search(pat,cmd2).group().split()[-1].strip('.')
    if not mat4:
        raise Exception("Failed")
    cmd2=run_command("./eeupdate64e /NIC=5 /MAC_DUMP",prompt='root@sonic')
    pat="5: LAN MAC Address is (.+)"
    mat5=re.search(pat,cmd2).group().split()[-1].strip('.')
    if not mat5:
        raise Exception("Failed")
    cmd2=run_command("./eeupdate64e /NIC=6 /MAC_DUMP",prompt='root@sonic')
    pat="6: LAN MAC Address is (.+)"
    mat6=re.search(pat,cmd2).group().split()[-1].strip('.')
    if not mat6:
        raise Exception("Failed")
    pat2 = "ether (.+)"
    output= run_command('ifconfig eth0',prompt='#',timeout=10)
    mac=re.search(pat2,output).group().split()[1].replace(':','')
    if not (mat5.lower()==mac.lower()):
        raise Exception("NIC 5 MAC Address mismatched")
    output= run_command('ifconfig eth1',prompt='#',timeout=10)
    mac=re.search(pat2,output).group().split()[1].replace(':','')
    if not (mat6.lower()==mac.lower()):
        raise Exception("NIC 6 MAC Address mismatched")
    output= run_command('ifconfig eth2',prompt='#',timeout=10)
    mac=re.search(pat2,output).group().split()[1].replace(':','')
    if not (mat1.lower()==mac.lower()):
        raise Exception("NIC 1 MAC Address mismatched")
    output= run_command('ifconfig eth3',prompt='#',timeout=10)
    mac=re.search(pat2,output).group().split()[1].replace(':','')
    if not (mat2.lower()==mac.lower()):
        raise Exception("NIC 2 MAC Address mismatched")
    output= run_command('ifconfig eth4',prompt='#',timeout=10)
    mac=re.search(pat2,output).group().split()[1].replace(':','')
    if not (mat3.lower()==mac.lower()):
        raise Exception("NIC 3 MAC Address mismatched")
    output= run_command('ifconfig eth5',prompt='#',timeout=10)
    mac=re.search(pat2,output).group().split()[1].replace(':','')
    if not (mat4.lower()==mac.lower()):
        raise Exception("NIC 4 MAC Address mismatched")
    log.success("MAC Address check passed")

@logThis
def checkFWVersion():
    cmd_lst=['./eeupdate64e /bus=9 /dev=0 /fun=0 /eepromver',
             './eeupdate64e /bus=10 /dev=0 /fun=0 /eepromver']
    output=run_command(cmd_lst,prompt='#',timeout=100)
    for i in range(0,2):
        if not "3.25" in output:
            raise Exception("FW Version mismatch")
    log.success("FW Version is latest")

@logThis
def upgradei210FW():
    cmd_lst=['./eeupdate64e /bus=9 /dev=0 /fun=0 /d /home/Dev_Start_I210_Copper_NOMNG_16Mb_A2_3.25_0.03.bin',
            './eeupdate64e /bus=10 /dev=0 /fun=0 /d /home/Dev_Start_I210_Copper_NOMNG_16Mb_A2_3.25_0.03.bin']
    output=run_command(cmd_lst,prompt='#',timeout=150)
    for i in range(0,2):
        if not "Shared Flash image updated successfully." in output:
            raise Exception("Downgrade Failed")
    log.success('Flash image updated successfully.')
    powerCycleDevice()
    verifyDiagTool()
    #cmd_lst=["./eeupdate64e /bus=9 /dev=0 /fun=0 /eepromver","./eeupdate64e /bus=10 /dev=0 /fun=0 /eepromver"]
    #output=run_command(cmd_lst,prompt='#',timeout=150)
    for i in range(0,2):
        if not "Shared Flash image updated successfully" in output:
            raise Exception("Upgrade Failed")
    log.success("FW Version is upgraded")


@logThis
def downgradei210FW():
    cmd_lst=['./eeupdate64e /bus=9 /dev=0 /fun=0 /d /home/Dev_Start_I210_Copper_NOMNG_16Mb_A2_1.0__Rev10.bin',
             './eeupdate64e /bus=10 /dev=0 /fun=0 /d /home/Dev_Start_I210_Copper_NOMNG_16Mb_A2_1.0__Rev10.bin']
    output=run_command(cmd_lst,prompt='#',timeout=150)
    for i in range(0,2):
        if not "Shared Flash image updated successfully." in output:
            raise Exception("Upgrade Failed")
    log.success('Flash image updated successfully.')
    powerCycleDevice()
    verifyDiagTool()
    #checkFWVersion()


