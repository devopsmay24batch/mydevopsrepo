# Script       : midstone100X_sonic.robot
# Date         : 8/4/2021
# Author       : Yagami jiang <yajiang@celestica.com>


*** Settings ***
Variables         midstone100X_sonic_variable.py
Library           midstone100X_sonic_lib.py
Library           CommonLib.py
Library           ../WhiteboxLibAdapter.py
Resource          midstone100X_sonic_keywords.robot
Resource          CommonResource.robot


*** Test Cases ***
SONIC_Image_Upgrade_Test
    [Documentation]  9.11 The purpose of this test is to test SONIC image upgrade.
    [Tags]     SONIC_Image_Upgrade_Test  Midstone100X
    [Setup]  OS Connect Device
    independent_step  1  InstallSonicWithOnie  old
    independent_step  2  RebootToOnieMode  uninstall
    independent_step  3  InstallDiagOS  http  old
    independent_step  4  InstallSonicInSonic  new  1
    independent_step  5  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  RebootToOnieMode  uninstall  AND
    ...  InstallDiagOS  http  old  AND
    ...  InstallSonicInSonic  new  1  AND
    ...  OS Disconnect Device


SONIC_installer_remove_installed_OS
    [Documentation]  9.12 The purpose of this test is to test SONIC_installer remove installed OS.
    [Tags]     SONIC_installer_remove_installed_OS  Midstone100X
    [Setup]  OS Connect Device
    independent_step  1  UninstallSonicInSonic  2
    [Teardown]  OS Disconnect Device


BSP_sysfs_interfaces_check
    [Documentation]  9.1 The purpose of this test is to check BSP sysfs interfaces.
    [Tags]     BSP_sysfs_interfaces_check  Midstone100X
    [Setup]  OS Connect Device
    independent_step  1  CheckBSPSysfsInterfaces
    [Teardown]  OS Disconnect Device


Switch_board_CPLD_register_access
    [Documentation]  9.4 The purpose of this test is to access switch board CPLD register.
    [Tags]     Switch_board_CPLD_register_access  Midstone100X
    [Setup]  OS Connect Device
    FOR  ${index}  IN RANGE  0  4
        independent_step  1  CheckCMDResponse  cat /sys/bus/i2c/devices/10-003${index}/version
                            ...  ${value_of_sys_bus_i2c_devices_10_0030_0033}
        independent_step  2  SendCmdWithoutRule  echo 0x00 > /sys/bus/i2c/devices/10-003${index}/getreg
        independent_step  3  SetWait  10
        independent_step  4  CheckCMDResponse  cat /sys/bus/i2c/devices/10-003${index}/getreg  ${value_of_getreg}
        independent_step  4  CheckCMDResponse  cat /sys/bus/i2c/devices/10-003${index}/scratch  0xde
        independent_step  5  SendCmdWithoutRule  echo 0xdf > /sys/bus/i2c/devices/10-003${index}/scratch
        independent_step  6  SetWait  10
        independent_step  7  CheckCMDResponse  cat /sys/bus/i2c/devices/10-003${index}/scratch  0xdf
        independent_step  8  SendCmdWithoutRule  echo 0x01 0xAA > /sys/bus/i2c/devices/10-003${index}/setreg
        independent_step  9  SetWait  10
        independent_step  10  CheckCMDResponse  cat /sys/bus/i2c/devices/10-003${index}/scratch  0xaa
    END
    END AC And Connect OS
    FOR  ${index}  IN RANGE  0  4
        independent_step  1  CheckCMDResponse  cat /sys/bus/i2c/devices/10-003${index}/scratch  0xde
    END
    independent_step  2  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  END Switch Board CPLD Register Access  AND
    ...  OS Disconnect Device


QSFP_Mode_Test
    [Documentation]  9.6 The purpose of this test is to access switch board CPLD register.
    [Tags]     QSFP_Mode_Test
    [Setup]  OS Connect Device
    FOR  ${index}  IN RANGE  1  65
        independent_step  1  CheckCMDResponse  cat /sys/class/SFF/QSFP${index}/qsfp_modirq  1
        independent_step  2  CheckCMDResponse  cat /sys/class/SFF/QSFP${index}/qsfp_modprs  0
        independent_step  3  CheckCMDResponse  cat /sys/class/SFF/QSFP${index}/qsfp_reset  1
        independent_step  4  SendCmdWithoutRule  echo 0 > /sys/class/SFF/QSFP${index}/qsfp_reset
        independent_step  5  SetWait  10
        independent_step  6  CheckCMDResponse  cat /sys/class/SFF/QSFP${index}/qsfp_reset  0
        independent_step  7  SendCmdWithoutRule  echo 1 > /sys/class/SFF/QSFP${index}/qsfp_reset
        independent_step  8  SetWait  10
        independent_step  9  CheckCMDResponse  cat /sys/class/SFF/QSFP${index}/qsfp_reset  1
        independent_step  10  CheckCMDResponse  cat /sys/class/SFF/QSFP${index}/qsfp_lpmode  0
        independent_step  11  SendCmdWithoutRule  echo 1 > /sys/class/SFF/QSFP${index}/qsfp_lpmode
        independent_step  12  SetWait  10
        independent_step  13  CheckCMDResponse  cat /sys/class/SFF/QSFP${index}/qsfp_lpmode  1
        independent_step  14  SendCmdWithoutRule  echo 0 > /sys/class/SFF/QSFP${index}/qsfp_reset
        independent_step  15  SetWait  10
        independent_step  16  CheckCMDResponse  cat /sys/class/SFF/QSFP${index}/qsfp_reset  0
    END
    [Teardown]  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


SFP_Mode_Test
    [Documentation]  9.7 The purpose of this test is to test QSFP Mode Test.
    [Tags]     SFP_Mode_Test
    [Setup]  OS Connect Device
    FOR  ${index}  IN RANGE  1  3
        independent_step  1  CheckCMDResponse  cat /sys/devices/platform/cls-xcvr/SFP${index}/sfp_absmod  0
        independent_step  2  CheckCMDResponse  cat /sys/devices/platform/cls-xcvr/SFP${index}/sfp_rxlos  0
        independent_step  3  CheckCMDResponse  cat /sys/devices/platform/cls-xcvr/SFP${index}/sfp_txdisable  0
        independent_step  4  SendCmdWithoutRule  echo 1 > /sys/devices/platform/cls-xcvr/SFP${index}/sfp_txdisable
        independent_step  5  SetWait  10
        independent_step  6  CheckCMDResponse  cat /sys/devices/platform/cls-xcvr/SFP${index}/sfp_txdisable  1
        independent_step  7  CheckCMDResponse  cat /sys/devices/platform/cls-xcvr/SFP${index}/sfp_txfault  0

    END
    [Teardown]  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


SONIC_Login_Check_Test
    [Documentation]  9.9 The purpose of this test is to check SONIC login.
    [Tags]     SONIC_Login_Check_Test  Midstone100X
    [Setup]  OS Connect Device
    independent_step  1  CheckNoErrorWhenOSStart
    [Teardown]  OS Disconnect Device


SONIC_Version_Check
    [Documentation]  9.10 The purpose of this test is to check SONIC version.
    [Tags]     SONIC_Version_Check  Midstone100X
    [Setup]  Run Keywords
    ...  SetWait  60  AND
    ...  OS Connect Device
    independent_step  1  CheckShowVersionInfo
    [Teardown]  OS Disconnect Device


Hardware_Interface_Acess_Scan_Check
    [Documentation]  9.15 The purpose of this test is to test hardware interface acess/scan/check.
    [Tags]     Hardware_Interface_Acess_Scan_Check  Midstone100X
    [Setup]  OS Connect Device
    independent_step  1  CheckCpuInfo
    [Teardown]  OS Disconnect Device


TLV_EEPROM_Info_Read
    [Documentation]  9.16 The purpose of this test is to read TLV EEPROM info.
    [Tags]     TLV_EEPROM_Info_Read  Midstone100X
    [Setup]  OS Connect Device
    independent_step  1  CheckTLVEepromInfo
    [Teardown]  OS Disconnect Device


Transceivers_EEPROM_Info_Check
    [Documentation]  9.17 The purpose of this test is to read TLV EEPROM info.
    [Tags]     Transceivers_EEPROM_Info_Check
    [Setup]  OS Connect Device
    independent_step  1  CheckLoopBackPresent
    FOR  ${index}  IN RANGE  16  80
        SendCmdWithoutRule  cd /sys/bus/i2c/devices/${index}-0050
        SendCmdWithoutRule  hexdump -C eeprom  True  ${loopback_manufacturer_name}
    END
    FOR  ${light}  IN RANGE  13  15
        SendCmdWithoutRule  cd /sys/bus/i2c/devices/${light}-0050
        SendCmdWithoutRule  hexdump -C eeprom  True  ${loopback_manufacturer_name}
    END
    [Teardown]  OS Disconnect Device


Power_Command_Test
    [Documentation]  9.21 The purpose of this test is to test power command.
    [Tags]     Power_Command_Test  Midstone100X
    [Setup]  OS Connect Device
    independent_step  1  SendCmdWithoutRule  poweroff
    ${os_status}  SendCmdInBMC  ipmitest chassis power status
    independent_step  2  CheckInfoEqual  ${os_status}  Chassis Power is off
    independent_step  3  SendCmdInBMC  ipmitest chassis power on  switch_cpu=True
    [Teardown]  OS Disconnect Device


Loopback_module_present_stress
    [Documentation]  9.23 Loopback module present stress
    [Tags]     Loopback_module_present_stress  stress
    [Setup]  OS Connect Device
    independent_step  1  RunLoopbackModulePresentStress
    [Teardown]  OS Disconnect Device
