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
import random
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
import GoogleLinuxBootVariable as var
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)

@logThis
def gotoSuperUser():
    output = run_command("pwd", prompt="(root|admin)@sonic:.*")
    if "root@sonic:" in output:
        log.info("Already in super-user mode.")
    else:
        output = run_command("sudo -s", prompt="(root|admin)@sonic:.*")
        log.info("Entered Super-User mode.")

@logThis
def checkUnameOperations():
    ver_1= "4.19"
    gotoSuperUser()
    a1=run_command("uname -a",prompt='root@sonic')
    r1=run_command("uname -r",prompt='root@sonic')
    v1= run_command("uname -v",prompt='root@sonic')
    run1=run_command("cat /proc/version",prompt='root@sonic')
    r2=run_command("dmesg|grep Linux",prompt='root@sonic')
    CommonKeywords.should_match_a_regexp(a1,ver_1)
    CommonKeywords.should_match_a_regexp(r1,ver_1)
    CommonKeywords.should_match_a_regexp(v1,ver_1)
    CommonKeywords.should_match_a_regexp(run1,ver_1)
    CommonKeywords.should_match_a_regexp(r2,ver_1)
    run_command('exit')

def gotoDiagDir():
    gotoSuperUser()
    diag_dir = "/usr/local/cls_diag/bin"
    output = device.sendCmd("cd {}".format(diag_dir),'#',timeout=15)
    if "No such file or directory" in output:
        log.info("File doesn't exist...downloading and installing from server...")
        device.sendCmd("curl -O http://192.168.0.1/R3152-M0025-01_Diag-brixia.v0.1.4.deb",'#',timeout=15)
        device.sendCmd("dpkg -i R3152-M0025-01_Diag-brixia.v0.1.4.deb",'#',timeout=15)
        run_command("cd /usr/local/cls_diag", prompt="root@sonic:.*", timeout=5)
        run_command("./install -p brixia32", prompt="root@sonic:.*", timeout=15)
        output = device.sendCmd("cd {}".format(diag_dir),'#',timeout=15)
    if output:
        log.info("Entered into diag dir..")

@logThis
def checkFlashSize():
    gotoSuperUser()
    a1= run_command("dmidecode -t bios",prompt='root@sonic')
    pat = "ROM Size: 16 MB|ROM Size: 32 MB|ROM Size: 8192 kB"
    if re.search(pat,a1):
        log.success("Flash size is correct")
    else:
        log.fail("Flash size not expected")
    run_command('exit')

##################TCS 06#############################################################################3

@logThis
def bootIntoLinux():
    verifyDiagTool()
    gotoSuperUser()
    device.sendMsg('echo 0x4449454a > /sys/devices/gfpga-platform/board_powercycle \n')
    device.read_until_regexp('.*Hit Ctrl-C to interrupt',timeout=450)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("03", '/#', timeout=100)
    c1=run_command('cat /proc/version',prompt='/#')
    device.sendCmd("exit", "sonic login:", timeout=400)
    m1=c1.splitlines()
    m2=d1.splitlines()

    device.loginToDiagOS()
    if re.search(var.linux_version,c1):
        log.success('Linux version matches')
    else:
        log.fail('Linux version mismatch')
    count=0
    for x in var.linux_menu:
        for y in m2:
            if x == y:
                count=count+1
    if len(var.linux_menu) == count:
        log.success("Test passed")
    else:
        log.fail("Test failed")





############################TCS 08#####################################
@logThis
def boot_into_linuxboots():
    try:
        run_command("ls", prompt="~/#.*root@.*", timeout=2)
        log.info("\nAlready in LinuxBoot shell.\n")
    except Exception as e:
        try:
            run_command("pwd", prompt="(root|admin)@sonic:.*", timeout=2)
            gotoSuperUser()
            device.sendMsg("reboot \r\n")
            output = device.read_until_regexp('.*no modules found matching.*|.*Hit Ctrl-C to interrupt.*',timeout=130)
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
def boot_into_sonic():
    try:
        run_command("ls", prompt="(root|admin)@sonic:.*", timeout=5)
        log.info("Already logged in SONiC OS.")
    except:
        try:
            run_command("ls", prompt="~/#.*root@.*", timeout=5)
            run_command("boot /dev/sda3", prompt=">", timeout=5)
            device.sendCmd("01", "Debian GNU/Linux 10 sonic ttyS0", timeout=35)
            device.sendMsg("\n\n")
            enter_sonic_credentials()
            log.info("Logged into SONiC OS.")

        except:
            device.read_until_regexp('.*Hit Ctrl-C to interrupt',timeout=130)
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

@logThis
def checkI2cdetect():
    c1= run_command("i2cdetect -l",prompt ='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(c1,var.i2c_detect_list_pattern)


@logThis
def checkCpuStats():
    cmd1= run_command('lscpu',prompt='root@sonic')
    cmd2=run_command('cat /proc/cpuinfo',prompt='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(cmd1,var.lscpu)
    CommonKeywords.should_match_ordered_regexp_list(cmd2,var.cpu_proc)

@logThis
def checkFdisk():
    cmd1= run_command('fdisk -l\n',prompt='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(cmd1,var.fdisk)


@logThis
def checkIfconfig():
    cmd1= run_command('ifconfig\n',prompt='root@sonic')
    CommonKeywords.should_match_ordered_regexp_list(cmd1,var.ifconfig)
    run_command('exit')

@logThis
def checkSonicOperation():
    time.sleep(60)        ;# Waiting for device to boot up
    gotoSuperUser()
    checkI2cdetect()
    checkCpuStats()
    checkFdisk()
    checkIfconfig()

#####################################################################


@logThis
def CheckBiosVersionPost(ver=""):
    gotoSuperUser()
    if ver == "new":
        BIOS_ver = CommonLib.get_swinfo_dict("BIOS").get("newVersion", "NotFound")
    else:
        BIOS_ver = CommonLib.get_swinfo_dict("BIOS").get("oldVersion", "NotFound")

    try:
        device.sendCmd('reboot', "BIOS {}".format(BIOS_ver), timeout=40)
    except Exception as e:
        device.sendCmd(Const.KEY_ESC)
        device.read_until_regexp("sonic login:", timeout=250)
        device.loginToDiagOS()
        raise Exception(str(e))
    log.success("BIOS Version matched")
    device.sendCmd(Const.KEY_ESC)
    device.read_until_regexp("sonic login:", timeout=250)
    device.loginToDiagOS()
    gotoSuperUser()
    output = device.sendCmd("dmidecode -t bios", BIOS_ver, timeout=10)
    log.success("BIOS Version matched")
    device.read_until_regexp('#')


# .......... TC_27 PCIE Bus Scan ..........

def checkLinuxbootPcieDevices():
    output = run_command("pci", prompt="~/#.*root@.*", timeout=5)
    for each in var.linuxboot_pci_device_pattern:
        if not re.search(each, output):
            raise Exception("Pattern not found in PCI list.\nConcerned pattern --> " + each)
    log.success("No error in displaying Linuxboot PCIe devices check.")


def checkSonicPcieDevices():
    gotoSuperUser()
    output = device.executeCmd("lspci")
    for each in var.sonic_pci_device_pattern:
        if not re.search(each, output):
            raise Exception(
                "Error in listing the pci device.\nPerticular device not found.\nConcerned pattern is:-> " + each)
    log.success("No error in displaying SONiC PCIe devices check.")


@logThis
def checkPCIeDeviceDetection(os=''):
    if os == "Linuxboot":
        checkLinuxbootPcieDevices()
    elif os == "Sonic":
        checkSonicPcieDevices()

        slots_with_error = []
        for each in var.show_pci_device_with_slot_cmds:
            slot_no = each.split()[2]
            output = device.executeCmd(each)
            # if slot_no not in output:
            if output.count(slot_no) != 2:
                slots_with_error.append(slot_no)
        if len(slots_with_error):
            raise Exception("Below given slots did not print any device info.\n{}".format(" ".join(slots_with_error)))
        log.success("PCIe device detection in Sonic OS successful.")


# .......... TC_28 PCIE Configuration Test ..........

def checkPCIeConfiguration():
    gotoSuperUser()
    cmd = "lspci -s {} -vvvxxx"
    for each in var.pcie_config_cmd1:
        output = run_command(cmd.format(each), prompt="root@sonic:.*", timeout=3)
        if output.count(each) < 2:
            raise Exception("Error in displaying the PCIe devices.\nConcerned command is --> " + cmd.format(each))

    cmd = "lspci -vvvxxx | grep -i "
    for each in var.pcie_config_cmd2:
        output = run_command(cmd + each, prompt="root@sonic:.*", timeout=5)
        if '"' in each:
            each = each[1:-1]
        r = re.findall(".*" + each.upper() + '|' + each + ".*", output)
        if len(r) < 2:
            raise Exception("Error in displaying the PCIe devices.\nConcerned command is --> " + cmd.format(each))


# # .......... TC_029 CPU I2C/SMBus/SMLink Interface Test ..........

def scanI2CBuses():
    gotoSuperUser()
    output = device.executeCmd("i2cdetect -l")
    for each in var.i2c_detect_list_pattern:
        if not re.search(each, output):
            raise Exception("Error in I2C detect.\nConcerned pattern --> " + each)

    output = device.executeCmd("i2cdetect -q -y 1 0x34 0x34")
    for each in var.i2c_detect_y_pattern:
        if not re.search(each, output):
            log.fail("Error in I2C detect. Known issue in Linuxboot\nConcerned pattern --> " + each)
    log.success("I2C Bus scan test passed successfully.")


def check_All_I2C_Device_Scan():
    line = " ----------------------------------------------------------------\n"
    log.info(line + '|Skipping the "./cel-i2c-test -all" check due to LinuxBoot issue.|\n' + line)
    # Skipping the ./cel-i2c-test check due to LinuxBoot issue.

    # device.sendMsg("cd /usr/local/cls_diag/bin \r\n")
    # output = device.executeCmd("./cel-i2c-test --all", timeout=450)

    # if re.search("I2C test all : FAILED <<<---", output):
    #     error_msg = "I2C Scan Test Failed.\nConcerned pattern are as given below.\n\n"
    #     fail_ptn = ".*[|].*[|].*[|].*[|] FAILED <<<---"
    #     r = re.findall(fail_ptn, output)
    #     error_msg += "\n".join(r)
    #     raise Exception(error_msg)
    # else:
    #     log.success("All I2C Scan Test Passed.")


# # .......... TC_030 CPU I2C/SMBus/SMLink Interface Test ..........


def check_ComE_MMC_CPLD_Version():
    gotoSuperUser()
    gotoDiagDir()
    device.sendMsg("cd ../tools  \r\n")
    cpld_cmd = "./lpc_cpld_x64_64 blu r "

    for each in var.come_cpld_ports:
        output = device.executeCmd(cpld_cmd + each)
        if not re.search("port num: " + each, output):
            raise Exception("Error in reading the port {} value.".format(each))

    log.success("Successfully read all four port values.")


def readWriteCPLDScratchRegister():
    cpld_cmd = "./lpc_cpld_x64_64 blu "

    for each in ["0xA101", "0xA1E1"]:
        val = " 0x" + str(random.randint(10, 99))
        cmd = cpld_cmd + "w " + each + val
        device.executeCmd(cmd)
        cmd = cpld_cmd + "r " + each
        output = device.executeCmd(cmd)
        if val not in output:
            raise Exception("Error in writing data to scratch register.\nLinuxBoot known issue same as CPLD version and scratch are ff. ")
    log.success("Read Write Scratch Register Successfull.")


# .......... TC_031 Management Port Information Check ..........

def check_VendorId_DeviceId(os=""):
    if os == "Linuxboot":
        output = run_command("pci", prompt="/#.*root@.*", timeout=5)
        if output.count("Intel Corporation I210 Gigabit Network Connection") != 2:
            raise Exception("Error in printing the PCI.")
    else:
        gotoSuperUser()
        output = run_command("lspci -s 07:00.0 -xxx", prompt="root@sonic:.*", timeout=5)
        output += run_command("lspci -s 08:00.0 -xxx", prompt="root@sonic:.*", timeout=5)
        if output.count("Intel Corporation I210 Gigabit Network Connection") != 2:
            raise Exception("Error in printing the PCI.")
    log.success("Both mgmt port info is detected correct.")


# # .......... TC_021 Read EEPROM Test ..........

def get_version_by_pattern(cmd, pattern, spliter):
    output = device.executeCmd(cmd)
    r = re.findall(pattern, output)[0]
    r = r.split(spliter)[-1].strip()
    return r


@logThis
def check_EEPROM_Option():
    gotoDiagDir()
    eeprom_cmd = "./cel-eeprom-test"

    eeprom_test_version1 = get_version_by_pattern(eeprom_cmd + " -v", "The ./cel-eeprom-test version is :.*", ':')
    eeprom_test_version2 = get_version_by_pattern(eeprom_cmd + " --version", "The ./cel-eeprom-test version is :.*",
                                                  ':')

    if eeprom_test_version1 != eeprom_test_version2 or eeprom_test_version1 != "0.1.4":
        raise Exception("Error in the ./cel-eeprom-test version.\nExpected: 0.1.4\nFound: " + eeprom_test_version1)

    help_op1 = device.executeCmd(eeprom_cmd + " -h")
    help_op2 = device.executeCmd(eeprom_cmd + " --help")

    CommonKeywords.should_match_paired_regexp_list(help_op1, var.eeprom_help_pattern)
    CommonKeywords.should_match_paired_regexp_list(help_op2, var.eeprom_help_pattern)

    list_op1 = device.executeCmd(eeprom_cmd + " -l")
    list_op2 = device.executeCmd(eeprom_cmd + " --list")

    CommonKeywords.should_match_paired_regexp_list(list_op1, var.eeprom_list_pattern)
    CommonKeywords.should_match_paired_regexp_list(list_op2, var.eeprom_list_pattern)

    log.success("Check EEPROM options succesfully completed.")


@logThis
def check_EEPROM_All_Option():
    output = run_command('./cel-eeprom-test -all', prompt="root@sonic:.*", timeout=120)

    failed = []
    dis = "Disable write protect: Failed"
    while re.search(dis, "\n".join(output)):
        index = output.index(dis) - 2
        failed.append(output[index])
        output.remove(dis)

    if len(failed):
        log.fail("==== Error in cel-eeprom-test -all ====\n\n")
        for each in failed:
            log.fail(each + '\n' + dis + '\n')
        raise Exception("Error in printing cel-eeprom-test -all.")

    # Checking for the read/write eeprom data.

    device_sections = output.split("---------------------------------------------------------------")
    for each_section in device_sections:
        writing_data = []
        eeprom_data = []

        #   First half that writes eeprom data
        try:
            r = re.findall("Enable write protect: Done", each_section)[0]
        except:
            break
        r = each_section.split(r)
        first = r[0]
        second = r[1]
        r = re.findall("echo.*", first)
        for each in r:
            each = each.split(">")[0].split('"')[1]
            writing_data.append(each)

        #   Second half that reads eeprom data
        ri = re.findall("Read .* EEPROM information:", second)[0]
        rj = re.findall("Dump .* EEPROM data:", second)[0]
        second = second.splitlines()
        i = second.index(ri)
        j = second.index(rj)
        data = second[i + 1: j - 1]
        for each in data:
            eeprom_data.append(":".join(each.split(':')[1:]).strip())

        for i in range(len(writing_data)):
            if eeprom_data[i] not in writing_data[i]:
                hex_to_int = int(writing_data[i].split('x')[-1], 16)
                if str(hex_to_int) not in eeprom_data[i]:
                    raise Exception(
                        "Error occured in ./cel-eeprom-test -all\nData not matched\n" + eeprom_data[i] + "!=" +
                        writing_data[i])
    log.success("EEPROM check options passed successfully.")


def extractEepromInformation(output):
    array = []
    output = output.split("root@sonic:/usr/local/cls_diag/bin#")
    for each in output:
        r = re.findall("000000.0.*[|].*[|]", each)
        array.append(r)
    return array


@logThis
def dump_And_Read_EEPROM_Via_Diag_And_Hexdump():
    err_linuxboot = "Error in dumping EEPROM data.\nKnown Linuxboot issue. Reported!"
    gotoDiagDir()
    dump_output = ""
    read_output = ""
    hexdump_output = ""
    dump_cmd = "./cel-eeprom-test --dump -d {} -t tlv"
    read_cmd = "./cel-eeprom-test -r -d {} -t tlv"
    check_cmd = "hd /sys/bus/i2c/devices/i2c-{}/eeprom-ro"

    for i in range(1, 9):
        dump_output += "\n\n" + device.executeCmd(dump_cmd.format(i))
        if "No such file or directory" in dump_output:
            raise Exception(err_linuxboot)
    dump_array = extractEepromInformation(dump_output)

    for i in range(1, 9):
        read_output += "\n\n" + device.executeCmd(read_cmd.format(i))
        if "No such file or directory" in read_output:
            raise Exception(err_linuxboot)
    read_array = extractEepromInformation(read_output)

    for each in var.eeprom_hexdump_dirs:
        hexdump_output += "\n\n" + device.executeCmd(check_cmd.format(each))
        if "No such file or directory" in hexdump_output:
            raise Exception(err_linuxboot)
    hexdump_array = extractEepromInformation(hexdump_output)

    if dump_array != read_array and read_array != hexdump_array:
        raise Exception("Error in EEPROM data from dump and read. Some of them not equal.")
    log.success("Both EEPROM data from dump and read command are same.")


def AC_Powercycle_Device():
    gotoSuperUser()
    device.sendCmd(var.powercycle_cmd,'sonic login:',timeout=350)
    device.sendMsg("\n")
    device.loginToDiagOS()


def writeTLVInformation(write_tlf_commands):
    tlv_cmd = "./cel-eeprom-test -w -d {} -t tlv -A {}"
    read_eeprom_cmd = "./cel-eeprom-test -r -d {} -t tlv"
    index = 1

    for each in write_tlf_commands:
        # Write to EEPROM
        eeprom_write_dict = {}
        eeprom_read_dict = {}
        for i in each:
            device.executeCmd(tlv_cmd.format(index, i))
            i = i.split(" -D ")
            eeprom_write_dict[i[0]] = i[1]

        # Read from EEPROM
        output = device.executeCmd(read_eeprom_cmd.format(index))
        r = re.findall(".*EEPROM information:", output)
        output = output.splitlines()
        xi = output.index(r[0])
        xj = output.index(r[1])

        read_data = output[xi + 1: xj - 1]
        for each_data in read_data:
            each_data = each_data.split(": ")
            eeprom_read_dict[each_data[0]] = each_data[1]

        # Check Data
        for key in eeprom_read_dict.keys():
            try:
                x = eeprom_write_dict[key].replace('"', "")
            except:
                continue
            j = eeprom_read_dict[key]
            if j not in x:
                if 'x' not in x:
                    x = hex(int(x)).split('x')[1].upper()
                else:
                    x = x.replace("x", '')
                if x not in j:
                    raise Exception("Error in writing eeprom data.\nConcerned data as below\n" + j + " != " + x)
        index += 1
    log.success("EEPROM data changed and read succesfully.")

# .......... TC_016 Kexe Runtime Kernel Check ..........

@logThis
def AC_Powercycle_Device_Into_Linuxboot():
    device.sendMsg(var.powercycle_cmd + "\r\n")
    device.read_until_regexp('.*no modules found matching.*|.*Hit Ctrl-C to interrupt.*', timeout=130)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)

@logThis
def checkKexeRuntimeKernel():
    gotoSuperUser()
    output = run_command("dmesg  | grep -i -e 'runtime\|kernel'", prompt="root@sonic:.*", timeout=5)
    r = re.findall(".*runtime|kernel.*", output)
    if len(r) == 0:
        raise Exception("Error in Runtime Log.")
    log.success("Kexe Runtime Kernel Log PASSED.")
#TC 24
@logThis
def Cpu_Microcode_ver_check():
    gotoSuperUser()
    output =run_command("dmesg | grep microcode\n", prompt="root@sonic:.*",timeout=50)
    CommonKeywords.should_match_ordered_regexp_list(output,var.cpu_microcode_ver)
    device.read_until_regexp('#')

#TC 14
@logThis
def checkMemoryInfo(os):
    if os == 'Sonic':
        output = run_command('cat /proc/meminfo',prompt='root@sonic:.*')
        CommonKeywords.should_match_ordered_regexp_list(output,var.Memory_info_sonic)
    elif os == 'LinuxBoot':
        output = run_command('cat /proc/meminfo',prompt='/#')
        CommonKeywords.should_match_ordered_regexp_list(output,var.Memory_info_linuxboot)



@logThis
def Check_cpu_and_memory_info(os):
    if os == "LinuxBoot":
        gotoSuperUser()
        device.sendCmd("reboot")
        device.read_until_regexp('.*Hit',timeout=450)
        for i in range(3):
            device.sendMsg(Const.KEY_CTRL_C)
            try:
                d1=device.read_until_regexp('>', timeout=15)
                break
            except Exception:
                continue
        device.sendCmd("03", '/#', timeout=100)
        check_cpu_info()
        checkMemoryInfo('LinuxBoot')
        run_command("boot /dev/sda3",prompt ='sonic login:')
        for i in range(3):
            try:
                d1=device.read_until_regexp('>', timeout=15)
                break
            except Exception:
                continue
        device.sendCmd("01", 'sonic login:', timeout=100)
        device.loginToDiagOS()

    else:
        gotoSuperUser()
        checkCpuStats()
        checkMemoryInfo('Sonic')

@logThis
def check_cpu_info():
     output = run_command('cat /proc/cpuinfo',prompt='/#')
     CommonKeywords.should_match_ordered_regexp_list(output,var.cpu_proc)
################################################################################################################
#TC 04
@logThis
def Check_Post_info():
    gotoSuperUser()
    Check_Post()
    device.loginToDiagOS()
    gotoSuperUser()
    Check_Post()
    device.loginToDiagOS()

@logThis
def Check_Post():
    output = device.sendCmd(var.powercycle_cmd,'Linux version',timeout=200)
    if not "coreboot" in output:
        Reset_type1 = "System Reset Type:Global Reset"
        Reset_type2 = "System Reset Type:Warm Reset"
        Reset_cause = "Reset Cause: Memory Initialize Done Reset"
        Exclude_str = "POST : EVALUATION COPY"
        if not Reset_type1 and Reset_type2 and Reset_cause in output:
            raise Exception("Post info check failed")
        log.info("Reset types verified successfully")
        if Exclude_str in output:
            raise Exception("Post info has " +Exclude_str)
        log.info("Evalution string not present in post")
        log.success("Post info check passed")
    else:
        log.info("Skipping the test case as coreboot is programmed instead of linuxboot")
    device.read_until_regexp("sonic login:",timeout=350)
    device.sendCmd('\n')
#TC19
@logThis
def Check_LinuxBoot_ver(ver = ""):
    gotoSuperUser()
    if ver == "new":
        LinuxBoot_ver = CommonLib.get_swinfo_dict("Linux_Installer").get("newVersion", "NotFound")
    else:
        LinuxBoot_ver = CommonLib.get_swinfo_dict("Linux_Installer").get("oldVersion", "NotFound")

    output = device.sendCmd(var.powercycle_cmd,LinuxBoot_ver,timeout = 80)
    if LinuxBoot_ver in output:
        log.success("Linux Version matched")
    elif "coreboot" in output:
        log.info("Test case skipped")
    else:
        raise Exception("Version checked Failed")

    device.read_until_regexp("sonic login:",timeout= 350)
    device.sendCmd('\n',"sonic login:")
    device.loginToDiagOS()

######################################################################################################################
#TC23
@logThis
def Cpu_Information_check():
    gotoSuperUser()
    checkCpuStats()
    time.sleep(5)
    cmd_lst = [
               "cd /root",
               "ls"
              ]
    output = run_command(cmd_lst,prompt = "root@sonic:~#",timeout=30)
    if "BDX_DE_Linux_2.0" in output:
        log.info("BDX_DE is already present")
    else:
        log.info("BDX_DE_Linux_2.0 file not present..trying to download from server...")
        run_command("curl -O http://192.168.0.1/BDX_DE_Linux_2.0",prompt='#')
    run_command("chmod -R 777 BDX_DE_Linux_2.0 ")
    cmd = run_command("cd BDX_DE_Linux_2.0",prompt="root@sonic:~/BDX_DE_Linux_2.0#",timeout = 5)
    run_command("modprobe msr",prompt = "root@sonic:~/BDX_DE_Linux_2.0#",timeout =3)
    output = run_command("./BroadwellPwrMon",prompt="TCC Status",timeout=40)
    if re.search("Accept License Agreement?[(]Y/y[)]:",output):
        device.sendMsg("Y\n")
    else:
        log.info("Licese Agreement acceptance not seen..")
    for each in var.Cpu_info_check:
        if not each in output:
            raise Exception("CPU_INFO_CHECK_FAILED")
    log.success("CPU Info check passed")
    device.sendCmd(Const.KEY_CTRL_C)
    device.read_until_regexp("root@sonic:~/BDX_DE_Linux_2.0",timeout=100)
    device.sendMsg('exit')
##########################################################################################################################

# .......... TC_025_CPU_Frequency_Check_Under_Full_Loading ..........

def printAndCheckScalingGoverner(flag):
    output = device.executeCmd(var.cat_scaling_gov_cmd)
    if output.count(flag) != 16:
        raise Exception("Error in printing scaling governer.\nIt should be 16 entries of " + flag)


@logThis
def Change_Intel_Power_Saving(flag, power_save_cmds):
    gotoSuperUser()
    for each in power_save_cmds:
        device.executeCmd(each)
    printAndCheckScalingGoverner(flag)


@logThis
def Check_List_Cpu():
    output = device.executeCmd("lscpu")
    for each in var.lscpu_pattern:
        if not re.search(each, output):
            raise Exception("lscpu Failed.\nConcerned pattern is:\n" + each)
    min_fre = float(get_version_by_pattern("lscpu", "CPU min MHz:.*", ':')) - 1
    cpu_fre = float(get_version_by_pattern("lscpu", "CPU MHz:.*", ':'))
    max_fre = float(get_version_by_pattern("lscpu", "CPU max MHz:.*", ':'))

    if min_fre < cpu_fre < max_fre:
        log.success("CPU frequency check passed successfully.")
    else:
        error = "Error in CPU frequency check.\n"
        error += "It should be between {} & {}\nFound {}".format(min_fre, max_fre, cpu_fre)
        raise Exception(error)


@logThis
def Monitor_Cpu_Frequency(time_in_minutes=1):
    fre_msg = "\n--------------------------- FREQUENCY ---------------------------\n"
    error_msg = "ERROR in CPU frequency checking. it's above 3000."
    ok_msg = "\nAll CPU core frequencies are in level.\nThe test will run for {} seconds.\n{} seconds passed.\n"
    device.sendCmd("cd /root/BDX_DE_Linux_2.0")
    device.sendCmd("modprobe msr")

    try:
        device.sendMsg("./BroadwellPwrMon \r\n")
        try:
            device.read_until_regexp("Accept License Agreement?[(]Y/y[)]:", timeout=2)
            device.sendMsg("Y\r\n")
        except:
            pass
        before = time.time()
        while round(time.time() - before) < time_in_minutes * 60:
            current_sec = str(round(time.time() - before))
            output = device.read_until_regexp("Power [(]W[)].*", timeout=2)
            frequency = re.findall("Frequency [(]MHz[)] :.*", output)[0]
            r = re.findall("\d+", frequency)
            log.debug(fre_msg + str(r) + ok_msg.format(time_in_minutes * 60, current_sec) + fre_msg)

            for each in r:
                if int(each) > 3000:
                    raise Exception(error_msg)
        device.sendMsg(Const.KEY_CTRL_C)
        log.success("CPU Core Frequency check test passed successfully.")

    except Exception as e:
        device.sendMsg(Const.KEY_CTRL_C)
        raise Exception(e)
@logThis
def OnieInstallByPxeboot():
    gotoSuperUser()
    output = device.sendCmd(var.powercycle_cmd,timeout=50)
    device.read_until_regexp('.*Hit ',timeout=200)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue

    device.sendCmd("pxeboot \n", '>', timeout=30)
    output1=device.sendCmd("01",timeout=50)
    device.read_until_regexp('.*Hit ',timeout=300)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue

    device.sendCmd("pxeboot \n", '>', timeout=30)

    device.sendCmd("02",'Please press Enter to activate this console.',timeout=100)
    device.sendCmd("\n",'#',timeout=10)
    output2=run_command('onie-sysinfo -v',prompt="ONIE-RECOVERY:/ # ",timeout=5)
    if not var.sysinfo_onie in output2:
        raise Exception("Onie version check failed")
    checkFdisk_onie()
    checkIfconfig_onie()
    output = device.sendCmd("reboot",timeout=50)
    device.read_until_regexp('.*Hit ',timeout=300)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue

    device.sendCmd("pxeboot \n", '>', timeout=30)
    device.sendCmd("02",'Please press Enter to activate this console.',timeout=100)
    device.sendCmd("\n",'#',timeout=10)
    output2=run_command('onie-sysinfo -v',prompt="ONIE-RECOVERY:/ # ",timeout=5)
    if not var.sysinfo_onie  in output2:
        raise Exception("Onie version check failed")

@logThis
def checkFdisk_onie():
    cmd1= run_command('fdisk -l\n',prompt='#')
    CommonKeywords.should_match_ordered_regexp_list(cmd1,var.fdisk_onie)


@logThis
def checkIfconfig_onie():
    cmd1= run_command('ifconfig\n',prompt='#')
    CommonKeywords.should_match_ordered_regexp_list(cmd1,var.ifconfig_onie)

@logThis
def SonicUpdateByPxeboot(Type=''):
     gotoSuperUser()
     output = device.sendCmd("reboot",timeout=50)
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
     device.sendCmd("\n",'#',timeout=10)
     time.sleep(30)
     device.sendCmd('ifconfig')
     device.sendCmd("onie-stop")
     if Type == 'downgrade':
         device.sendCmd("onie-nos-install http://192.168.0.1/onie-installer-x86_64.bin \n")
     else:
         device.sendCmd("onie-nos-install http://192.168.0.1/onie-installer.bin \n")
     device.read_until_regexp("sonic login:.*",timeout=500)
     device.loginToDiagOS()
     gotoSuperUser()
     ver=device.sendCmd("show version","#",timeout=40)
     time.sleep(10)
     if Type == 'downgrade':
         if not var.sonic_ver_old in ver:
             raise Exception("Version check Failed")
     else:
         if not var.sonic_ver_new in ver:
             raise Exception("Version check Failed")
     run_command("lscpu \n",prompt="#",timeout=40)
     run_command("ifconfig \n",prompt="#",timeout=40)

@logThis
def gotoDiagToolDir():
    gotoSuperUser()
    diag_dir = "/usr/local/cls_diag/tools"
    output = device.sendCmd("cd {}".format(diag_dir),'#',timeout=15)
    if "No such file or directory" in output:
        log.info("File doesn't exist...downloading and installing from server...")
        device.sendCmd("curl -O http://192.168.0.1/R3152-M0025-01_Diag-brixia.v0.1.4.deb",'#',timeout=15)
        device.sendCmd("dpkg -i R3152-M0025-01_Diag-brixia.v0.1.4.deb",'#',timeout=15)
        output = device.sendCmd("cd {}".format(diag_dir),'#',timeout=15)
    if output:
        log.info("Entered into diag dir..")

@logThis
def OnlineLinuxBootInstall(Install = ""):
    gotoDiagToolDir()
    Installer_info_dict = CommonLib.get_swinfo_dict("Linux_Installer")
    if Install == "new":
        filename = Installer_info_dict.get("newImage", "NotFound")
    else:
        filename = Installer_info_dict.get("oldImage", "NotFound")
    res = device.sendCmd('ls',filename,timeout=30)
    if filename in res:
        log.info("Image file present in dir")
    else:
        log.info("Image file not present in dir.... trying to download from server......")
        device.sendCmd("curl -O http://192.168.0.1/{}".format(filename),'#',timeout=60)
    Install_cmd = "./afulnx_64 {} /p /b /n /me /x /k".format(filename)
    run_command("insmod amifldrv_mod.o",prompt="#",timeout=40)
    device.sendCmd(Install_cmd,timeout=60)
    try:
        device.read_until_regexp("- Please select one of the options:",timeout=120)
        device.sendCmd('E')
    except:
        log.info("Process selection not seen")
    device.read_until_regexp("Process completed.",timeout=150)

#####TC 41
@logThis
def CPU_Warm_Stress_test():
    
    loop_count = 2  # It's value should be equal to the variable used in CPU_Warm_Stress.sh file

    gotoSuperUser()
    device.sendCmd("cd /home/", '#', timeout=5)
    err_msg = "cat: CPU_Warm_Stress.sh: No such file or directory"
    cmd = device.sendCmd('cat CPU_Warm_Stress.sh', 'root@sonic:/home#', timeout=30)
    if err_msg in cmd:
        log.info("File not present in dir..downloading from server...")
        device.read_until_regexp("root@sonic:/home#", timeout=20)
        device.sendCmd("curl -O http://192.168.0.1/CPU_Warm_Stress.sh", timeout=15)

    log.info("File present in dir...")
    device.read_until_regexp("root@sonic:/home#", timeout=20)
    device.sendCmd("chmod -R 777 CPU_Warm_Stress.sh", '#', timeout=5)

    for i in range(loop_count):
        gotoSuperUser()
        run_command("cd /home", prompt="root@sonic:.*", timeout=5)
        device.sendMsg('./CPU_Warm_Stress.sh \r\n')
        device.read_until_regexp("sonic login:", timeout=450)
        device.sendCmd('\n')
        device.loginToDiagOS()

    gotoSuperUser()
    device.sendCmd("cd /home/", '#', timeout=5)
    output = run_command("cat function_check.log | grep -i fail | wc -l", prompt='root@sonic:.*', timeout=10)
    if "0" not in output:
        raise Exception("Stress Script has error due to LinuxBoot known issue")
    device.sendCmd("cat function_check.log | grep Test Loop | wc -l", '#', timeout=10)
    device.sendCmd("rm -rf count.log function_check.log Check_Bus.txt")

# # .......... TC_09_SONiC_install_by_pxeboot_test ..........

def executeSonicBasic(cmd, ptn_list, fail_msg):
    msg = "Error occured in {} listing.\nConcerned pattern -> {}"
    output = device.executeCmd(cmd)
    for each in ptn_list:
        if not re.search(each, output):
            raise Exception(msg.format(fail_msg, each))


@logThis
def check_Sonic_List(flag='0'):
    gotoSuperUser()
    output = device.executeCmd("sonic-installer list")
    sonic_version = re.findall("SONiC-OS.*", output)[0]
    if "SONiC-OS-202106-brixia.pb" not in sonic_version:
        raise Exception("Error in SONiC version display.")
    if flag == '1':
        log.success("SONiC install by pxeboot test passed successfully.")


@logThis
def install_Sonic_with_rescue_in_Pxeboot():
    l = "\n---------------------------------------\n"
    device.sendCmd("pxeboot", ">", timeout=5)
    device.sendMsg("02")
    for i in range(5):
        try:
            device.sendMsg('\r\n')
            output = device.read_until_regexp("Chosen option rescue.", timeout=5)
            if "Chosen option rescue." in output:
                log.debug("Entered rescue mode successfully.")
                break
        except:
            log.debug("Attempted #{} to rescue mode failed.\nTrying again...".format(str(i + 1)))

    device.read_until_regexp("ONIE: Executing installer:.*", timeout=600)
    log.info(l + "SONiC installation started..." + l)
    device.read_until_regexp("Installed SONiC base image SONiC-OS successfully", timeout=250)
    log.info(l + "SONiC installation successful...\nRestarting device." + l)
    device.read_until_regexp("sonic login:", timeout=150)
    enter_sonic_credentials()
    check_Sonic_List()


@logThis
def check_Sonic_Basic_Functions():
    output = device.executeCmd("i2cdetect -l")
    CommonKeywords.should_match_paired_regexp_list(output, var.pxe_install_i2cdetect_ptn)

    output = device.executeCmd("lspci")
    for each in var.sonic_pci_device_pattern:
        if not re.search(each, output):
            raise Exception(
                "Error in listing the device.\nPerticular device not found.\nConcerned pattern is:-> " + each)

    executeSonicBasic("cat /proc/cpuinfo", var.pxeboot_cpuinfo_pattern, "CPU INFO")
    executeSonicBasic("cat /proc/meminfo", var.pxeboot_meminfo_pattern, "MEM INFO")
    try:
        executeSonicBasic("ifconfig", var.pxeboot_ifconfig_pattern, "IF CONFIG")
    except:
        time.sleep(10)
        executeSonicBasic("ifconfig", var.pxeboot_ifconfig_pattern, "IF CONFIG")
    executeSonicBasic("fdisk -l", var.pxeboot_fdisk_pattern, "FDISK")


def auto_reboot_Into_Sonic():
    # AC Power Reset
    device.sendMsg("reboot \r\n")
    device.read_until_regexp("sonic login:", timeout=150)
    enter_sonic_credentials()

#tc 40 44
@logThis
def Check_Ac_Power_Cycle_stress():
    gotoSuperUser()
    device.sendCmd("cd /home/",'#',timeout=5)
    filename ="AC_Power_StressCap.sh"
    # script_pat = "+ /home/{}".format(filename)
    err_msg = "cat: AC_Power_StressCap.sh: No such file or directory"
    cmd = device.sendCmd('cat AC_Power_StressCap.sh', 'root@sonic:', timeout=15)
    if err_msg in cmd:
        log.info("File not present in dir..downloading from server...")
        device.sendCmd("curl -O http://192.168.0.1/AC_Power_StressCap.sh",'#',timeout=15)

    log.info("File present in dir...")
    device.sendCmd("chmod -R 777 AC_Power_StressCap.sh", 'root@sonic:', timeout=5)
    output = run_command("./"+filename, prompt="root@sonic:" ,timeout=200)
    if "CPLD hang, read 0xa1e1 is 0xff" in output:
        raise Exception("Known Linuxboot Issue. showing value ff.")

@logThis
def SATA_Interface_R_W_stress():
    gotoSuperUser()
    device.sendCmd("cd /home/", 'root@sonic:', timeout=5)
    filename ="Print_df.sh"
    err_msg = "cat: Print_df.sh: No such file or directory"
    cmd = device.sendCmd('cat Print_df.sh', 'root@sonic:', timeout=15)
    if err_msg in cmd:
        log.info("File not present in dir..downloading from server...")
        device.sendCmd("curl -O http://192.168.0.1/Print_df.sh", 'root@sonic:', timeout=15)
    output = device.sendCmd('cat Print_df.sh', 'root@sonic:', timeout=15)
    r = re.findall("\d+", output)[0]
    loop_count = int(r)
    ptn = '------df times={} ------'.format(loop_count)
    log.info(ptn)

    device.sendCmd("chmod -R 777 Print_df.sh", 'root@sonic:', timeout=5)
    device.sendCmd("sed -i -e 's/\r$//' Print_df.sh", 'root@sonic:', timeout=10)
    output = run_command("./Print_df.sh", prompt="root@sonic:.*", timeout=70*loop_count)
    if ptn not in output:
        raise Exception("Error in running Print_df.sh script")

    log.success("SATA Interface R/W Script executed successfully")
    device.sendCmd('\n')
    run_command("ifconfig \n", prompt="root@sonic:", timeout=20)

@logThis
def Check_Memory_stress():
    loop_count = '1' # Change the loop count for more iteration.
    gotoDiagToolDir()
    output = run_command("./memtester 28G " + loop_count,prompt="Loop {}/{}:".format(loop_count,loop_count),timeout=43560)
    if not output:
        raise Exception("Memory Stress test Failed")
    device.read_until_regexp("Done.",timeout=11340)
    log.success("Memory Stress test passed")
    run_command("fdisk -l \n",prompt="#",timeout=20)

# .......... TC_042 CPU Stress Test ..........

def checkCpuUsageCorrect(output, run_time="", remaining_time=""):
    msg = "\n---------------------------------------------\n"
    r = re.findall("%Cpu.*", output)[0]
    r = re.findall("\d+", r)
    cpu_usage = float(r[0] + '.' + r[1])
    if run_time != "":
        time_msg = "\nThe test will run for {} seconds.\n{} seconds remaining.".format(int(run_time), int(remaining_time))
        log.debug(msg+ "CPU Usage %: " + str(cpu_usage) + time_msg +msg)
    return cpu_usage >= 90 and cpu_usage <=99

def checkForStressFile():
    run_command("cd /home", prompt="root@sonic.*", timeout=3)
    output = run_command("ls", prompt="root@sonic.*", timeout=3)

    if 'stress' not in output:
        log.info("Stress file not found on the device.\nFetching the file from the server...")
        run_command(var.fetch_cmd, prompt="root@sonic.*", timeout=10)
        run_command("chmod +x stress", prompt="root@sonic.*", timeout=3)
        log.info("Stress file successfully fetched from the server.")

@logThis
def run_CPU_Stress_Test(time_in_minutes):
    time_in_sec = int(time_in_minutes)*60
    gotoSuperUser()
    checkForStressFile()

    run_command(var.stress_cmd1, prompt="root@sonic.*", timeout=5)
    run_command(var.stress_cmd2, prompt="root@sonic.*", timeout=5)

    output = run_command("top -d 60", prompt="MiB Mem :.*", timeout=3)
    if not checkCpuUsageCorrect(output):
        raise Exception("ERROR")

    before = time.time()
    try:
        while round(time.time() - before) < time_in_sec:
            time.sleep(1)
            device.sendMsg("\n")
            output = device.read_until_regexp("MiB Mem :.*", timeout=3)
            remaining = time_in_sec - int(time.time() - before)
            if not checkCpuUsageCorrect(output, time_in_sec, remaining):
                raise Exception("ERROR")
    except Exception as e:
        device.sendMsg(Const.KEY_CTRL_C)
        if str(e) == "ERROR":
            raise Exception("CPU Usage went out of required range.\n")
        else:
            raise Exception(str(e))
    device.sendMsg(Const.KEY_CTRL_C)
    log.success("CPU stress test successfully executed.")


# # .......... TC_12_SONiC_uninstall_test ..........

def fetchSonicImage():
    run_command("cd /home/admin", prompt="root@sonic:.*", timeout=5)
    output = run_command("ls", prompt="root@sonic:.*", timeout=3)
    if "onie-installer-x86_64.bin" not in output:
        log.info("SONiC pb19 image not found\nFetching from server...\n")
        try:
            run_command(var.fetch_old_sonic, prompt="root@sonic:.*", timeout=80)
            output = run_command("ls", prompt="root@sonic:.*", timeout=3)
            if "onie-installer-x86_64.bin" not in output:
                raise Exception("Error in fetching SONiC image from server.\n" + str(e))
        except Exception as e:
            raise Exception(str(e))
        log.info("Sonic old image succesfully fetched from server.")
    else:
        log.info("Sonic old image already present.")


@logThis
def install_Previous_Sonic_OS():
    gotoSuperUser()
    fetchSonicImage()

    # Install SONiC 19
    device.sendMsg('sonic-installer install onie-installer-x86_64.bin \n')
    device.read_until_regexp("New image will be installed.*")
    device.sendMsg("y \r\n")
    output = device.read_until_regexp("Done", timeout=60)

    if not re.search("Installed SONiC base image SONiC-OS successfully|.*already installed.*", output):
        raise Exception("Error in Installing older SONiC version OS.")
    else:
        log.info("SONiC PB19 installed succesfully.")


@logThis
def boot_Into_Sonic_With_Args(flag="new"):
    boot_id = "pb20" if flag == "new" else "pb19"
    output = run_command("boot /dev/sda3", prompt=">", timeout=3)
    r = re.findall(".*SONiC.*", output)
    index = '1' if boot_id in r[0] else '2'

    device.sendCmd(index, "Debian GNU/Linux 10 sonic ttyS0", timeout=70)
    device.sendMsg("\n\n")
    enter_sonic_credentials()
    log.info("Logged into SONiC OS.")


@logThis
def check_Sonic_Version(flag="new", final=""):
    gotoSuperUser()
    sonic_version = get_version_by_pattern('sonic-installer list', 'Current:.*', ':')
    sonic_required_version = eval("var.sonic_" + flag + '_ptn')
    if sonic_version != sonic_required_version:
        raise Exception("Error in SONiC version.\nExpected:" + sonic_required_version + "\nFound: " + sonic_version)
    else:
        log.success("SONiC Version Correct!")
    if final == "final":
        log.success("SONiC uninstall test successful.")


@logThis
def uninstall_Old_Sonic():
    device.sendMsg("sonic-installer remove {} \n".format(var.sonic_old_ptn))
    device.read_until_regexp("Image will be removed.*", timeout=5)
    device.sendMsg("y \n")
    device.read_until_regexp("root@sonic:.*")


@logThis
def check_Linuxboot_Menu_And_Boot_Into_Sonic():
    output = run_command("boot /dev/sda3", prompt=">", timeout=3)
    if "pb19" in output:
        raise Exception("Old SONiC image not removed\nFound in Linuxboot Menu.")
    device.sendCmd("1", "Debian GNU/Linux 10 sonic ttyS0", timeout=70)
    device.sendMsg("\n\n")
    enter_sonic_credentials()
    log.info("Logged into SONiC OS.")


def edit_File_Replace(filename, replace_text, replace_with_arr):
    output = run_command("cat " + filename, prompt="root@sonic:.*", timeout=20)
    r = re.findall(".*cat myFile.txt.*", output)[0]
    if r.endswith("\r"):
        r = r[:len(r) - 1]

    output = output.splitlines()
    index = output.index(r)
    new_file = output[index + 1: len(output) - 1]
    index = new_file.index(replace_text)
    l = len(new_file)
    new_file = new_file[:index] + replace_with_arr + new_file[index + 1:]

    run_command("rm " + filename, prompt="root@sonic:.*", timeout=20)
    run_command("touch " + filename, prompt="root@sonic:.*", timeout=20)
    for each in new_file:
        run_command("echo {} >> {}".format(each, filename), prompt="root@sonic:.*", timeout=20)

    run_command("cat " + filename, prompt="root@sonic:.*", timeout=20)

########################################################################################################################3
@logThis
def verifyDiagTool():
    gotoSuperUser()
    output = run_command("cd /usr/local/cls_diag/tools",prompt='root@sonic')
    outputPath = run_command("pwd",prompt='root@sonic')
    if re.search("/usr/local/cls_diag/tools", outputPath):
        log.success("Can find the correct diag path!")
    else:
        log.fail("Failed to find the diag path")
##############################################################################################################################
@logThis
def deviceInfoCheck():
    gotoSuperUser()
    device.sendCmd("reboot","Hit ^C within 10 seconds to stop booting",timeout=300)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('#', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("boot /dev/sda1", '>', timeout=60)
    device.sendCmd('03','#',timeout=50)
    output1= run_command('ls -la /dev/',prompt='/#').strip()
    device.sendCmd("boot /dev/sda1",'>',timeout=60)
    device.sendCmd("01", 'sonic login:', timeout=100)
    device.loginToDiagOS()
    gotoSuperUser()
    output2= run_command('ls -la /dev/',prompt='root@sonic:.*').strip()
    pattern='\s*([\S]+)$'
    for each in output1.splitlines():
        out= re.findall(pattern,each)
    for each in output2.splitlines():
        out1= re.findall(pattern,each)
    check = all(item in out for item in out1)
    if check != True:
        raise Exception("This test case validates the device list..\nThe device lists doesnot match...\nNeed manual effort to check the device list")
    log.success("Device List matched")

