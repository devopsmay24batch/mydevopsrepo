# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
# It's better not to call functions in variable files(e.g. BSP_DRIVER = SwImage.getSwImage("BSP_DRIVER")).
# any error during the calling will make all the tests fail.
# We have encountered this type of issue many many times in facebook projects.

import os
from collections import OrderedDict
from SwImage import SwImage
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()
devicename = os.environ.get("deviceName", "")
pc_info = DeviceMgr.getServerInfo('PC')
server_ipv4 = pc_info.managementIP
server_name = pc_info.username
server_passwd = pc_info.password
server_prompt = pc_info.prompt
onieObj = SwImage.getSwImage("ONIE_updater")
onieNewVer = onieObj.newVersion
onieHostDir = onieObj.hostImageDir
onieNewImg = onieObj.newImage
SDK = SwImage.getSwImage("SDK")
sdkname = SDK.newImage
sdk_shell_path = '/root/sdk/{}'.format(sdkname)
cat_sys_eeprom_cmd = "sys_eeprom"
cat_sys_eeprom_cmd_pattern = {"label revision": "Label Revision.*0x27.*R0.*"}
server_tmp_file = "/tmp/dut_output.log"
ifconfig_eth0_cmd = "ifconfig eth0"
ifconfig_a_cmd = "ifconfig -a"
Innovinum_success = "Innovium Switch PCIe Driver opened successfully"
setenvaddr = "d6:4e:4e:ff:4e:03"
envTool = 'fw_printenv'
ubootEnvTool = 'printenv'
testEnv1 = 'testenv1=mytestenv1'
testEnv2 = 'testenv2=mytestenv2'
testEnv3 = 'testenv3=mytestenv3'
testEnv4 = 'testenv4=mytestenv4'
testEnvLst = [testEnv1, testEnv2, testEnv3, testEnv4]
tftp_root_path = '/var/lib/tftpboot'
fail_dict = { "fail":"fail",
              "ERROR":"ERROR",
              "Failure": "Failure",
              "cannot read file":"cannot read file",
              "command not found":"command not found",
              "No such file": "No such file",
              "not found": "not found",
              "Unknown command":"Unknown command",
              "No space left on device": "No space left on device",
              "Command exited with non-zero status": "Command exited with non-zero status"
              }
file_system_utilities_commands = OrderedDict({
    "cd /" : "cd /",
    "fdisk":"fdisk -l",
    "mkfs":"mkfs.ext3 /dev/sda4",
    "fsck":"fsck.ext3 /dev/sda4",
    "mkdir":"mkdir test",
    "mount":"mount /dev/sda3 /test",
    "cd test" : "cd /test",
    "ls" : "ls",
    "cd" : "cd ..",
    "umount" : "umount /dev/sda3",
    "cd1" : "cd /test",
    "ls1" : "ls",
    "wget" : "ls /usr/bin/wget",
    "scp" : "ls /usr/bin/scp"
})
special_characters = {
    '.' : '\.',
    '*' : '\*',
    '(' : '\(',
    ')' : '\)',
    '?' : '\?',
    '|' : '\|'
}
onie_self_update_current_ver_cmd="onie-self-update tftp://192.168.0.5/R3247-J0003-01-v13-cs8260-bsp/celestica_cs8260-release/image/onie/onie-updater-arm64-celestica_cs8260-r0"
onie_self_update_higher_ver_cmd="onie-self-update tftp://192.168.0.5/R3247-J0003-01-v999-cs8260-bsp/celestica_cs8260-release/image/onie/onie-updater-arm64-celestica_cs8260-r0"
onie_self_update_production_ver_cmd="onie-self-update tftp://192.168.0.5/R3247-J0003-01-v13-cs8260-bsp/celestica_cs8260-release/image/onie/onie-updater-arm64-celestica_cs8260-r0"
onie_self_update_customer_ver_cmd="onie-self-update tftp://192.168.0.5/R3247-J0003-01-v14-cs8260-bsp/celestica_cs8260-release/image/onie/onie-updater-arm64-celestica_cs8260-r0"

#### 10.4.1_ONIE_Update_via_Static_IP+TFTP ####
ubootDefaultTool1 = 'env default -a'
ubootDefaultTool2 = 'savee'
ubootDefaultTool3 = 'reset'
#### 10.4.8.1_ONIE_Update_With_Current_Version ####
onieSelfUpdateTool = 'onie-self-update'
onieCurrentImgCmd = onieSelfUpdateTool + ' tftp://' + server_ipv4 + '/' + onieHostDir + '/' + onieNewImg
#### ONIE_10.7.2_ONIE_System_Information ####
TPM_TOOL = 'tpm_getinfo -a'
Tpm_Expect = {
    'version': '2.0',
    'revision': '1.38',
    'manufacturer': 'IFX',
    'part_number': 'SLB9670',
    'firmware_version': '0x70055'
}
initargs_tool = 'print onie_initargs'
bootargs_tool = 'print bootargs'
initargs_res = 'onie_initargs=setenv bootargs console=$consoledev,$baudrate onie_dhcp=eth0 pcie_ports=native pcie_aspm=off'
bootargs_res = 'bootargs=pcie_aspm=off console=ttyAMA0,$baudrate'
#### ONIE_10.7.3_TLV_EEPROM_R/W_Test ####
ONIE_SYSEEPROM_CMD = "onie-syseeprom"
ONIE_WP_ENBLE_VAL = '1'
ONIE_WP_CMD = '/sys/bus/i2c/devices/19-0060/system_eeprom_wp'
ONIE_WRITE_WP_CMD = 'onie-syseeprom -s '
#### ONIE_10.7.22_Check_Driver_Information_in_ONIE ####
onieUbootMode = 'onie_bootcmd'
onieToUpdateMode = 'onie_update'
onieToRescueMode = 'onie_rescue'
onieDriveTool = 'lsmod'
onieDrivePath = '/root/driver'
readDriveVer = 'head releaseNotes | grep Version'
onieInstallDrivePattern = [
    r'ipd\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'sfp_module\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'1pps_fpga\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'march_hare_fpga_core\s+\d+\s+\d+\s+1pps_fpga,\s+Live\s+0xffff\w+\s+\(O\)',
    r'tps53679\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'ltc4286\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'pmbus_core_cus\s+\d+\s+\d+\s+tps53679,\s+Live\s+0xffff\w+\s+\(O\)',
    r'q54sx\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'sitime\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'come_cpld\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'fan_cpld\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'cls_i2c_client\s+\d+\s+\d+\s+come_cpld,\s+Live\s+0xffff\w+\s+\(O\)',
    r'ltc4282\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'asc10\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)'
]
onieUpdateDrivePattern = [
    r'sfp_module\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'1pps_fpga\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'march_hare_fpga_core\s+\d+\s+\d+\s+1pps_fpga,\s+Live\s+0xffff\w+\s+\(O\)',
    r'tps53679\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'ltc4286\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'pmbus_core_cus\s+\d+\s+\d+\s+tps53679,\s+Live\s+0xffff\w+\s+\(O\)',
    r'q54sx\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'sitime\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'come_cpld\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'fan_cpld\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'cls_i2c_client\s+\d+\s+\d+\s+come_cpld,\s+Live\s+0xffff\w+\s+\(O\)',
    r'ltc4282\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)',
    r'asc10\s+\d+\s+\d+\s+\-\s+Live\s+0xffff\w+\s+\(O\)'
]
#### ONIE_10.7.26_SFP_detect_Test ####
sfp_tool = 'sfp_eeprom'
stp_value_pattern = 'AWS'
stp_test_value_pattern = 'AwS'
enable_lpmode_option = ' --lpmode ON'
write_test_stp_option = ' --write 0 130 0x77'
write_stp_option = ' --write 0 130 0x57'

#ssh_connect
username = "root"
exit_ssh = "exit"
tftp_server_ip = "192.168.0.5"
auto_load_user = "./auto_load_user.sh"
check_ports_link_status_cmd = "ifcs show devport"
exit_sdk_shell = 'quit'
tftp_get_onie_file_cmd = "tftp -g {} -r {}"
tftp_get_sys_cpld_file_cmd = "tftp -g {} -r {}"
tftp_get_fan_cpld_file_cmd = "tftp -g {} -r {}"
vmetool_path = "/root/vmetool"
onie_file_local_path = "/tmp"
display_onie_partition_cmd = "cat /proc/mtd"
onie_partition_pattern = '(mtd\d):.*?"onie"'
onie_partition_erase_cmd = "flash_erase /dev/{} 0 0"
onie_erase_pattern = { "Erasing 100% complete": "Erasing.*?100\s*%\s*complete" }
flashcp_upgrade_onie_cmd = "flashcp -v {} /dev/{}"
get_versions_cmd = "get_versions"
diag_bin_path = "/root/diag"
get_sys_info_cmd = "bash -c 'export LD_LIBRARY_PATH=/root/diag/output; export CEL_DIAG_PATH=/root/diag; ./cel-system-test --all' "
sys_info_pass_pattern = {"Sys test : Passed": "Sys\s+test\s+:\s+Passed"}
ACTIVATE_CONSOLE_PROMPT = 'Please press Enter to activate this console'
INSTALLER_MODE_DETECT_PROMPT = 'discover: installer mode detected'
UPDATE_MODE_DETECT_PROMPT = 'discover: ONIE update mode detected'
RESCUE_MODE_DETECT_PROMPT = 'discover: Rescue mode detected'
UNINSTALL_MODE_DETECT_PROMPT = 'discover: Uninstall mode detected'
RECOVERY_DIAG_PATTERN = { "installer mode detected":"installer mode detected"}
switch_onie_mode_cmd = {
    #"installer": "powerCycle",
    "installer": "run onie_bootcmd",
    "update"  : "run onie_update",
    "rescue"   : "run onie_rescue",
    "Uninstall": "run onie_uninstall"
}
TLV_Value_Test1 = { "Product Name"     : ["0x21", "Seastone400"],
                    "Part Number"      : ["0x22", "R1165-F0001-04"],
                    "Serial Number"    : ["0x23", "R1165F2B028731GD00004"],
                    "Base MAC Address" : ["0x24", "00:E0:EC:C9:B1:B4"],
                    "Manufacture Date" : ["0x25", "12/14/2018 03:01:52"],
                    "Device Version"   : ["0x26", "02"],
                    "Label Revision"   : ["0x27", "R0B"],
                    "Platform Name"    : ["0x28", "arm65-celestica_cs8000-r0"],
                    "ONIE Version"     : ["0x29", "2017.110.0.2"],
                    "MAC Addresses"    : ["0x2A", "3"],
                    "Manufacturer"     : ["0x2B", "CSA"],
                    "Country Code"     : ["0x2C", "US"],
                    "Vendor Name"      : ["0x2D", "CSB"],
                    "Diag Version"     : ["0x2E", "1.2"],
                    "Service Tag"      : ["0x2F", "9901000001"],
                    "Vendor Extension" : ["0xFD", "0x0C"],
        }

TLV_Value_Test2 = { "Product Name"     : ["0x21", "XYZ1234A"],
                    "Part Number"      : ["0x22", "ABC1234567890"],
                    "Serial Number"    : ["0x23", "0123456789"],
                    "Base MAC Address" : ["0x24", "00:11:22:33:44:55"],
                    "Manufacture Date" : ["0x25", "01/31/2017 01:02:03"],
                    "Device Version"   : ["0x26", "03"],
                    "Label Revision"   : ["0x27", "R0C"],
                    "Platform Name"    : ["0x28", "powerpc-xyz1234a-r0"],
                    "ONIE Version"     : ["0x29", "onie_version_1.0"],
                    "MAC Addresses"    : ["0x2A", "4"],
                    "Manufacturer"     : ["0x2B", "Manufacturer"],
                    "Country Code"     : ["0x2C", "TW"],
                    "Vendor Name"      : ["0x2D", "Manufacturer"],
                    "Diag Version"     : ["0x2E", "1.1"],
                    "Service Tag"      : ["0x2F", "1"],
                    "Vendor Extension" : ["0xFD", "AssetID=5205005105"],
        }

ONIE_SYSEEPROM_CMD = "onie-syseeprom"
VALUE_PATTERN = "^\w+_VALUE=(.*)"
AUTO_DISCOVERY_PATTERN = { "ONIE: Starting ONIE Service Discovery": "ONIE: Starting ONIE Service Discovery" }
AUTO_DISCOVERY_PATTERN.update(fail_dict)
PRINT_VER_CMD = "print ver"

######TC23 Default file Name Search Order######
INSTALLER_FILE_SEARCH_ORDER = [
        "onie-installer-arm64-celestica_cs8200-r0",
        "onie-installer-arm64-celestica_cs8200-r0.bin",
        "onie-installer-arm64-celestica_cs8200",
        "onie-installer-arm64-celestica_cs8200.bin",
        "onie-installer-celestica_cs8200",
        "onie-installer-celestica_cs8200.bin",
        "onie-installer-arm64-innovium",
        "onie-installer-arm64-innovium.bin",
        "onie-installer-arm64",
        "onie-installer-arm64.bin",
        "onie-installer",
        "onie-installer.bin"
        ]
INSTALLER_SLEEPING_PATTERN = "Info: Sleeping for.*?seconds"
UPDATER_FILE_SEARCH_ORDER = [
        "onie-updater-arm64-celestica_cs8200-r0",
        "onie-updater-arm64-celestica_cs8200-r0.bin",
        "onie-updater-arm64-celestica_cs8200",
        "onie-updater-arm64-celestica_cs8200.bin",
        "onie-updater-celestica_cs8200",
        "onie-updater-celestica_cs8200.bin",
        "onie-updater-arm64-innovium",
        "onie-updater-arm64-innovium.bin",
        "onie-updater-arm64",
        "onie-updater-arm64.bin",
        "onie-updater",
        "onie-updater.bin"
        ]
DISCOVERY_STOP_PATTERN = { "discover: Rescue mode detected. No discover stopped" :
                           "discover: Rescue mode detected\. No discover stopped"
                        }

SSD_INFO_PATTERN = { "Device Model": "(.*?)$", "Serial Number": "(.*?)$", "User Capacity": "(.*?)$", "SATA Version is": "(.*?)$"}
SSD_HEALTH_PATTERN = {"self-assessment test result: PASSED":  "self-assessment test result: PASSED",
                      "No Errors Logged":  "No Errors Logged"
                      }
I2C_BUS_NO_LIST = [37, 38, 35, 36, 41, 40, 50, 39, 47, 46,
                   49, 45, 44, 48, 42, 43, 60, 66, 63, 59,
                   64, 61, 56, 65, 62, 57, 51, 58, 53, 55,
                   54, 52 ]
fhv2_I2C_BUS_NO_LIST = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
                   111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
                   121, 122, 123, 124, 125, 126, 127, 128, 129, 130,
                   131, 132 ]
DRIVER_INFO_IN_BOOTING_PATTERN = {
        "Init dcdc min/max value" : "Init dcdc min/max value",
        "Ethernet controller"     : "Ethernet controller",
        "SATA controller"         : "SATA controller",
        "RAID bus controller"     : "RAID bus controller",
        "/root/driver"            : "/root/driver"
        }
FENGHUANGV2_DRIVER_INFO_IN_BOOTING_PATTERN = {
        "Loading drivers" : "Loading drivers"
        # "/root/sdk"            : "/root/sdk"
        }
LOADED_DRIVER_PATTERN = {
        "ipd"            : "ipd.*?Live",
        "sfp_module"     : "sfp_module.*?Live",
        "pktgen"         : "pktgen.*?Live",
        "mcp3422"        : "mcp3422.*?Live",
        "ir35215"        : "ir35215.*?Live",
        "asc10"          : "asc10.*?Live",
        "i2c_sc18is600"  : "i2c_sc18is600.*?Live",
        "fan_cpld"       : "fan_cpld.*?Live",
        "sys_cpld"       : "sys_cpld[^,]+Live",
        "cls_i2c_client" : "cls_i2c_client.*?i2c_sc18is600,sys_cpld,\s+Live",
        "pmbus_core"     : "pmbus_core.*?Live"
        }
FENGHUANGV2_LOADED_DRIVER_PATTERN = {
        "ipd"            : "ipd.*?Live",
        "cms"            : "cms50216.*?Live",
        "i2c_accel_fpga" : "sfp_module.*?Live",
        "ltc4282"        : "sfp_module.*?Live",
        "psu_dps800"     : "sfp_module.*?Live",
        "asc10"          : "asc10.*?Live",
        "tps53679"       : "sfp_module.*?Live",
        "fan_cpld"       : "fan_cpld.*?Live",
        "sys_cpld"       : "sys_cpld[^,]+Live",
        "cls_i2c_client" : "cls_i2c_client.*?sys_cpld,\s+Live",
        "sfp_module"     : "sfp_module.*?Live",
        }
EXCLUDE_LOAD_DRIVER_PATTERN = { "psu_dps1100" : "psu_dps1100"}
FPP_MODES = [
        "32x400","32x100","32x40",
        "64x100",
        "64x100-1","128x100",
        "128x25","128x10","1-2:4x100G;3-4:40G",
        "1-32:4x100G", "1:4x100G;2-15:100G",
        "1:4x100G;2-15:100G;16-32:4x25G",
        "sfp_detect"
        ]

INTEGRATOR_TEST_MODES = [
        "32x400" , "32x200", "64x100",
        "128x100", "32x100", "32x40",
        "128x25" , "128x10", "sfp_detect"
        ]

sysCpldObj = SwImage.getSwImage("SYS_CPLD")
fanCpldObj = SwImage.getSwImage("FAN_CPLD")
comeCpldObj = SwImage.getSwImage("COME_CPLD")
fpgaObj = SwImage.getSwImage("1PPS_FPGA")
ascObj = SwImage.getSwImage("1PPS_ASC")
localCpldPath = sysCpldObj.localImageDir
sysCpldNewImg = sysCpldObj.newImage
fanCpldNewImg = fanCpldObj.newImage
comeCpldNewImg = comeCpldObj.newImage
fpgaNewImg = fpgaObj.newImage
ascNewImg = ascObj.newImage
sysCpldNewPath = sysCpldObj.hostImageDir + '/' + sysCpldNewImg
fanCpldNewPath = fanCpldObj.hostImageDir + '/' + fanCpldNewImg
comeCpldNewPath = comeCpldObj.hostImageDir + '/' + comeCpldNewImg
fpgaNewPath = fpgaObj.hostImageDir + '/' + fpgaNewImg
sysCpldOption = ' -s '
fanCpldOption = ' -f '
comeCpldOption = ' -c '
comeCpldOption1 = ' -cxfr '
vmetool = "vmetool_arm "

if "fenghuangv2" in devicename.lower():
    cat_onie_platform_cmd = "printenv onie_platform"
    cat_onie_platform_cmd_pattern = {"platform": "CS8270.*"} if device.get('cardType') == "1PPS" else {"platform": "CS8260.*"}
    fsc_check_pattern = {"fan speed control": "fan control.*?fan_ctrl"}
    ps_fsc_check_pattern = {"ps fan speed control": ".*fan_ctrl"}
    ps_fsc_check_percent_pattern = {"ps fan speed percent control": ".*%"}
    QUERY_EEPROM_WRITE_PROTECTION_CMD = "echo WRITE_PROTECT_VALUE=$( i2cget -y -f 8 0x60 0x05 )"
    ENABLE_EEPROM_WRITE_CMD = "i2cset -y -f 8 0x60 0x05 0x0"
    DISABLE_EEPROM_WRITE_CMD = "i2cset -y -f 8 0x60 0x05 {}"
    get_sys_cpld_version_cmd = "i2cget -f -y 8 0x60 0x00"
    get_fan_cpld_version_cmd = "i2cget -f -y 23 0x66 0x00"
    INSTALLER_FILE_SEARCH_ORDER = [
        "onie-installer-arm64-celestica_cs8260-r0",
        "onie-installer-arm64-celestica_cs8260-r0.bin",
        "onie-installer-arm64-celestica_cs8260",
        "onie-installer-arm64-celestica_cs8260.bin",
        "onie-installer-celestica_cs8260",
        "onie-installer-celestica_cs8260.bin",
        "onie-installer-arm64-innovium",
        "onie-installer-arm64-innovium.bin",
        "onie-installer-arm64",
        "onie-installer-arm64.bin",
        "onie-installer",
        "onie-installer.bin"
    ]
    # INSTALLER_SLEEPING_PATTERN = "Info:.*Attempting tftp.*192.168.*"
    UPDATER_FILE_SEARCH_ORDER = [
        "onie-updater-arm64-celestica_cs8260-r0",
        "onie-updater-arm64-celestica_cs8260-r0.bin",
        "onie-updater-arm64-celestica_cs8260",
        "onie-updater-arm64-celestica_cs8260.bin",
        "onie-updater-celestica_cs8260",
        "onie-updater-celestica_cs8260.bin",
        "onie-updater-arm64-innovium",
        "onie-updater-arm64-innovium.bin",
        "onie-updater-arm64",
        "onie-updater-arm64.bin",
        "onie-updater",
        "onie-updater.bin"
    ]
elif "51.2t" in devicename.lower():
    disableFCS = 'pkill az-fan-test'
    comecpld1_img = comeCpldNewImg['CPUCPLD1']
    comecpld2_img = comeCpldNewImg['CPUCPLD2']
    come1_path = comeCpldObj.hostImageDir + '/' + comecpld1_img
    come2_path = comeCpldObj.hostImageDir + '/' + comecpld2_img
    cpldNewImgPathLst = [sysCpldNewPath, fanCpldNewPath, come1_path, come2_path]
    cpldNewImgLst = [sysCpldNewImg, fanCpldNewImg]
    cpldOptionLst = [sysCpldOption, fanCpldOption]
    comeCpldImgLst = [comecpld1_img, comecpld2_img]
    comeOptionLst = [comeCpldOption, comeCpldOption1]
    SYSTEM_INFO_TOOL = 'az-system-info --all'
    SYSTEM_PATTERN = 'Sys test : Passed'
    ONIE_SYSEEPROM_TEST_DICT = {
        '0x21': 'AZ9074-64X-DC-11',
        '0x22': '301-000919-002',
        '0x23': '332404241500073',
        '0x24': 'B4:DB:91:2F:66:70',
        '0x25': '\"08/19/2021 18:20:22\"',
        '0x26': '2',
        '0x27': 'R01',
        '0x28': 'AZ9074-64X-DC-11-R01',
        '0x29': '2017.11.5',
        '0x2a': '3',
        '0x2b': 'SH',
        '0x2c': 'SH',
        '0x2d': 'SH',
        '0x2e': '0.0.9',
        '0xfd': '\"AssetID=4232000057\"'
    }
    INSTALLER_FILE_SEARCH_ORDER = [
        "onie-diagos-installer-arm64-az9074",
        "onie-diagos-installer-arm64-az9074.bin",
        "onie-installer-arm64-az9074-r0",
        "onie-installer-arm64-az9074-r0.bin",
        "onie-installer-arm64-az9074",
        "onie-installer-arm64-az9074.bin",
        "onie-installer-az9074",
        "onie-installer-az9074.bin",
        "onie-installer-arm64-bcm",
        "onie-installer-arm64-bcm.bin",
        "onie-installer-arm64",
        "onie-installer-arm64.bin",
        "onie-installer",
        "onie-installer.bin"
    ]
    UPDATER_FILE_SEARCH_ORDER = [
        "onie-diagos-installer-arm64-az9074",
        "onie-diagos-installer-arm64-az9074.bin",
        "onie-updater-arm64-az9074-r0",
        "onie-updater-arm64-az9074-r0.bin",
        "onie-updater-arm64-az9074",
        "onie-updater-arm64-az9074.bin",
        "onie-updater-az9074",
        "onie-updater-az9074.bin",
        "onie-updater-arm64-bcm",
        "onie-updater-arm64-bcm.bi",
        "onie-updater-arm64",
        "onie-updater-arm64.bin",
        "onie-updater",
        "onie-updater.bin"
    ]
elif "tigrisv2" in devicename.lower():
    disableFCS = 'pkill az-fan-test'
    asc10_0_come_img = ascNewImg['ASC10_0_COME_IMG']
    asc10_1_come_img = ascNewImg['ASC10_1_COME_IMG']
    asc10_0_img = ascNewImg['ASC10_0_IMG']
    asc10_1_img = ascNewImg['ASC10_1_IMG']
    asc10_2_img = ascNewImg['ASC10_2_IMG']
    asc10_0_come_path = ascObj.hostImageDir + '/' + asc10_0_come_img
    asc10_1_come_path = ascObj.hostImageDir + '/' + asc10_1_come_img
    asc10_0_path = ascObj.hostImageDir + '/' + asc10_0_img
    asc10_1_path = ascObj.hostImageDir + '/' + asc10_1_img
    asc10_2_path = ascObj.hostImageDir + '/' + asc10_2_img
    cpldNewImgPathLst = [sysCpldNewPath, fanCpldNewPath, comeCpldNewPath, fpgaNewPath, asc10_0_come_path, asc10_1_come_path, asc10_0_path, asc10_1_path, asc10_2_path]
    cpldNewImgLst = [sysCpldNewImg, fanCpldNewImg, comeCpldNewImg]
    cpldOptionLst = [sysCpldOption, fanCpldOption, comeCpldOption]
    fpgaNewImgLst = [fpgaNewImg, asc10_0_come_img, asc10_1_come_img, asc10_0_img, asc10_1_img, asc10_2_img]
    SYSTEM_INFO_TOOL = 'az-system-info --all'
    SYSTEM_PATTERN = 'Sys test : Passed'
    initargs_res = 'onie_initargs=setenv bootargs console=$consoledev,$baudrate onie_dhcp=eth0,eth1 pcie_ports=native $bootargs'
    bootargs_res = 'bootargs=pcie_aspm=off console=ttyAMA0,$baudrate'
    ONIE_SYSEEPROM_TEST_DICT = {
        '0x21': 'AZ3324-00X-DC-12',
        '0x22': '301-000919-002',
        '0x23': '332404241500073',
        '0x24': 'B4:DB:91:2F:66:70',
        '0x25': '\"08/19/2021 18:20:22\"',
        '0x26': '2',
        '0x27': 'R01',
        '0x28': 'AZ3324-00X-DC-11-R01',
        '0x29': '2017.11.5',
        '0x2a': '3',
        '0x2b': 'SH',
        '0x2c': 'SH',
        '0x2d': 'SH',
        '0x2e': '0.0.9',
        '0xfd': '\"AssetID=4232000058\"'
    }
    INSTALLER_FILE_SEARCH_ORDER = [
        "onie-installer-arm64-az3324-r0",
        "onie-installer-arm64-az3324-r0.bin",
        "onie-installer-arm64-az3324",
        "onie-installer-arm64-az3324.bin",
        "onie-installer-az3324",
        "onie-installer-az3324.bin",
        "onie-installer-arm64-bcm",
        "onie-installer-arm64-bcm.bin",
        "onie-installer-arm64",
        "onie-installer-arm64.bin",
        "onie-installer",
        "onie-installer.bin"
    ]
    UPDATER_FILE_SEARCH_ORDER = [
        "onie-updater-arm64-az3324-r0",
        "onie-updater-arm64-az3324-r0.bin",
        "onie-updater-arm64-az3324",
        "onie-updater-arm64-az3324.bin",
        "onie-updater-az3324",
        "onie-updater-az3324.bin",
        "onie-updater-arm64-bcm",
        "onie-updater-arm64-bcm.bin",
        "onie-updater-arm64",
        "onie-updater-arm64.bin",
        "onie-updater",
        "onie-updater.bin"
    ]
elif "tianhe" in devicename.lower():
    SYSTEM_INFO_TOOL = 'cel-system-test --all'
    SYSTEM_PATTERN = 'Sys test : Passed'
    cat_onie_platform_cmd = "printenv onie_platform"
    cat_onie_platform_cmd_pattern = {"platform": "CS8274.*"}
    fsc_check_pattern = {"fan speed control": "fan control.*?fan_ctrl"}
    ps_fsc_check_pattern = {"ps fan speed control": ".*fan_ctrl"}
    ps_fsc_check_percent_pattern = {"ps fan speed percent control": ".*%"}
    QUERY_EEPROM_WRITE_PROTECTION_CMD = "echo WRITE_PROTECT_VALUE=$( i2cget -y -f 19 0x60 0x05 )"
    ENABLE_EEPROM_WRITE_CMD = "i2cset -y -f 19 0x60 0x05 0x0"
    DISABLE_EEPROM_WRITE_CMD = "i2cset -y -f 19 0x60 0x05 {}"
    get_sys_cpld_version_cmd = "i2cget -f -y 19 0x60 0x00"
    get_fan_cpld_version_cmd = "i2cget -f -y 34 0x66 0x00"
    get_come_cpld_version_cmd = "i2cget -f -y 4 0x60 0x01"
    #unit_name = device.name[-3:]
    #server_tmp_file = "/tmp/dut_output_" + unit_name + ".log"
    ONIE_SYSEEPROM_TEST_DICT = {
        '0x21': 'CS8274-32X-DC-12',
        '0x22': '301-000334-002',
        '0x23': 'CS8274F2B03213419T0002',
        '0x24': '0C:48:C6:98:9F:32',
        '0x25': '\"08/19/2021 18:20:22\"',
        '0x26': '3',
        '0x27': 'R01',
        '0x28': 'CS8274-32X-DC-11-R01',
        '0x29': '2017.11.009',
        '0x2a': '5',
        '0x2b': 'SH',
        '0x2c': 'SH',
        '0x2d': 'SH',
        '0x2e': '0.0.9',
        '0xfd': '\"AssetID=4232000057\"'
    }
    INSTALLER_FILE_SEARCH_ORDER = [
        "onie-installer-arm64-celestica_cs8264-r0",
        "onie-installer-arm64-celestica_cs8264-r0.bin",
        "onie-installer-arm64-celestica_cs8264",
        "onie-installer-arm64-celestica_cs8264.bin",
        "onie-installer-celestica_cs8264",
        "onie-installer-celestica_cs8264.bin",
        "onie-installer-arm64-innovium",
        "onie-installer-arm64-innovium.bin",
        "onie-installer-arm64",
        "onie-installer-arm64.bin",
        "onie-installer",
        "onie-installer.bin"
    ]
    UPDATER_FILE_SEARCH_ORDER = [
        "onie-updater-arm64-celestica_cs8264-r0",
        "onie-updater-arm64-celestica_cs8264-r0.bin",
        "onie-updater-arm64-celestica_cs8264",
        "onie-updater-arm64-celestica_cs8264.bin",
        "onie-updater-celestica_cs8264",
        "onie-updater-celestica_cs8264.bin",
        "onie-updater-arm64-innovium",
        "onie-updater-arm64-innovium.bin",
        "onie-updater-arm64",
        "onie-updater-arm64.bin",
        "onie-updater",
        "onie-updater.bin"
    ]
    #### ONIE_10.7.7_CPLD/FPGA_Updates ####
    cpldNewImgPathLst = [sysCpldNewPath, fanCpldNewPath, comeCpldNewPath]
    cpldNewImgLst = [sysCpldNewImg, fanCpldNewImg, comeCpldNewImg]
    cpldOptionLst = [sysCpldOption, fanCpldOption, comeCpldOption]
    disableFCS = 'pkill cel-fan-test'
    #### ONIE_10.7.8_1pps_Accelerator_FPGA_Update_Test ####
    ppsFpgaObj = SwImage.getSwImage("1PPS_FPGA")
    localFpgaPath = ppsFpgaObj.localImageDir
    ppsFpgaNewImg = ppsFpgaObj.newImage
    ppsFpgaNewPathLst = [ppsFpgaObj.hostImageDir + '/' + ppsFpgaNewImg]
    fpgaFwTool = 'flashcp'
    fpgaOption = ' -v '
    mtdCmd = 'cat /proc/mtd'
    fpgaDevPattern = r'(mtd\d+):.*"i2cfpga"'
    #### ONIE_10.7.24_FPP_Modes_Test ####
    empty_value = ""
    FPP_MODES = [
        "32x400", "32x100", "32x40",
        "64x100",
        "64x100-1", "128x100",
        "128x25", "128x10", "1-2:4x100G;3-4:40G",
        "1-32:4x100G", "1:4x100G;2-15:100G",
        "1:4x100G;2-15:100G;16-32:4x25G",
        "sfp_detect",
        empty_value,
    ]
    FPPS_COUNT_PATTERN = {
        "32x400" : '32',
        "32x100" : '32',
        "32x40" : '32',
        "64x100" : '64',
        "64x100-1" : '64',
        "128x100" : '128',
        "128x25" : '128',
        "128x10" : '128',
        "1-2:4x100G;3-4:40G" : '10',
        "1-32:4x100G" : '128',
        "1:4x100G;2-15:100G" : '18',
        "1:4x100G;2-15:100G;16-32:4x25G" : '86',
        "sfp_detect" : '128',
        "64x100_copper" : '64',
        "32x100_copper" : '32',
        "128x25_copper" : '128',
        "128x10_copper" : '128',
        empty_value : '128',
    }
    INTEGRATOR_TEST_MODES = [
        "32x400", "64x100", "128x100", "32x100", "32x40",
        "128x25", "128x10", "64x100-1", "sfp_detect",
        "64x100_copper", "32x100_copper", "128x25_copper", "128x10_copper"
    ]
######### common:
cat_onie_platform_cmd = "printenv onie_platform"
cat_onie_platform_cmd_pattern = {"platform": "onie_platform=arm64-celestica_.*"}
fsc_check_pattern = {"fan speed control": "fan speed control.*?fan_ctrl"}
QUERY_EEPROM_WRITE_PROTECTION_CMD = "echo WRITE_PROTECT_VALUE=$( i2cget -y -f 15 0x60 0x05 )"
ENABLE_EEPROM_WRITE_CMD = "i2cset -y -f 15 0x60 0x05 0x0"
DISABLE_EEPROM_WRITE_CMD = "i2cset -y -f 15 0x60 0x05 {}"
get_sys_cpld_version_cmd = "i2cget -f -y 15 0x60 0x00"
get_fan_cpld_version_cmd = "i2cget -f -y 10 0x66 0x00"
FW_names = ["SYSCPLD", "SWLEDCPLD1", "FANCPLD", "I2CFPGA", "ASC10-0", "ASC10-1", "ASC10-2"]
FW_CHANGED = {}
DIAG_BOOT_CMD = 'run diag_bootcmd'
ONIE_SN_TOOL = 'onie-sysinfo -s'
ONIE_PN_TOOL = 'onie-sysinfo -P'
ONIE_VER1 = 'onie-sysinfo -v'
ONIE_VER2 = 'cat /etc/os-release'
SYS_INFO_LST = [ONIE_SN_TOOL, ONIE_PN_TOOL, ONIE_VER1, ONIE_VER2]
PSU_INFO_TOOL = 'psu_info'
TEMP_INFO_TOOL = 'thermal_info'
FAN_INFO_TOOL = 'fan_info'
unit_name = device.name
server_tmp_file = "/tmp/dut_output_" + unit_name + ".log"
ONIE_SYSINFO_TOOL = 'onie-sysinfo'
ONIE_SYS_LST = [ONIE_SYSINFO_TOOL, ONIE_VER1, ONIE_VER2]



