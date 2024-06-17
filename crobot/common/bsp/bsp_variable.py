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
##### Variable file used for bmc.robot #####
import os
import re
import logging
import DeviceMgr
from SwImage import SwImage
from dataStructure import parser

OPENBMC_MODE = 'openbmc'
CENTOS_MODE = 'centos'

devicename = os.environ.get("deviceName", "")

if "minerva" in devicename.lower():
    fb_variant = 'minerva'
    #### Meta_Minerva_BSP_TC_002 Structure of BSP Package ####
    test_cmd_kernel_test = 'uname -a'
    expected_kernel = ['Linux localhost.localdomain 5']
    test_cmd_DiagOs_test = 'cat /etc/os-release'
    expected_os = ['CentOS Stream 9']
    test_cmd_BSPlist_test = 'ls /usr/lib/modules/5.19.0/kernel/fboss/'
    expected_bsp_files = ['fbiob-pci.ko', 'janga_smbcpld.ko', 'mp3_smbcpld.ko', 'regbit-sysfs.ko', 'fpga-info.ko' , 'mcbcpld.ko', 'mtia_pwrcpld.ko', 'spi-fbiob.ko', 'gpio-fbiob.ko', 'mp3_fancpld.ko', 'mtia_smbcpld.ko', 'tahan_smbcpld.ko', 'i2c-fbiob.ko', 'mp3_scmcpld.ko', 'port-led.ko', 'xcvr-ctrl.ko']

    #####BSP_TC_002_BSP_Driver_Install_Uninstall_Test ######
    removed_bsp_device_folder = ['cplds', 'eeprom', 'gpio', 'leds', 'xcvrs']
    installed_bsp_device_folder = ['cplds', 'eeprom', 'fpgas', 'gpio', 'i2c-busses', 'leds', 'sensors', 'xcvrs']
    old_installed_bsp_device_folder = ['fpgas', 'i2c-busses', 'leds', 'sensors']
    cplds_folder = ['FAN_CPLD', 'MCB_CPLD','SCM_CPLD', 'SMB_CPLD']
    eeprom_folder = ['MCB_EEPROM', 'SCM_EEPROM']
    fpgas_folder = ['IOB_FPGA']
    gpio_folder = ['IOB_GPIO_CHIP_0']
    i2c_busses_folder = ['DOM1_I2C_BUS_33', 'DOM1_I2C_BUS_34', 'DOM2_I2C_BUS_33', 'DOM2_I2C_BUS_34', 'I801_I2C_BUS', 'ISMT_I2C_BUS', 'IOB0_PCA9548_CH0', 'IOB0_PCA9548_CH1', 'IOB0_PCA9548_CH2', 'IOB0_PCA9548_CH3', 'IOB0_PCA9548_CH4', 'IOB0_PCA9548_CH5', 'IOB0_PCA9548_CH6', 'IOB0_PCA9548_CH7', 'IOB1_PCA9546_CH0', 'IOB1_PCA9546_CH1', 'IOB1_PCA9546_CH2', 'IOB1_PCA9546_CH3', 'IOB_I2C_BUS_1', 'IOB_I2C_BUS_2', 'IOB_I2C_BUS_3', 'IOB_I2C_BUS_4', 'IOB_I2C_BUS_5', 'IOB_I2C_BUS_6', 'IOB_I2C_BUS_7', 'IOB_I2C_BUS_8', 'IOB_I2C_BUS_9', 'IOB_I2C_BUS_10', 'IOB_I2C_BUS_11', 'IOB_I2C_BUS_12', 'IOB_I2C_BUS_13', 'IOB_I2C_BUS_14', 'IOB_I2C_BUS_15', 'IOB_I2C_BUS_16', 'IOB_I2C_BUS_17', 'IOB_I2C_BUS_18', 'IOB_I2C_BUS_19', 'IOB_I2C_BUS_20', 'IOB_I2C_BUS_21', 'IOB_I2C_BUS_22', 'IOB_I2C_BUS_23', 'IOB_I2C_BUS_24', 'IOB_I2C_BUS_25', 'IOB_I2C_BUS_26', 'IOB_I2C_BUS_27', 'XCVR_1', 'XCVR_2', 'XCVR_3', 'XCVR_4', 'XCVR_5', 'XCVR_6', 'XCVR_7', 'XCVR_8', 'XCVR_9', 'XCVR_10', 'XCVR_11', 'XCVR_12', 'XCVR_13', 'XCVR_14', 'XCVR_15', 'XCVR_16', 'XCVR_17', 'XCVR_18', 'XCVR_19', 'XCVR_20', 'XCVR_21', 'XCVR_22', 'XCVR_23', 'XCVR_24', 'XCVR_25', 'XCVR_26', 'XCVR_27', 'XCVR_28', 'XCVR_29', 'XCVR_30', 'XCVR_31', 'XCVR_32', 'XCVR_33', 'XCVR_34', 'XCVR_35', 'XCVR_36', 'XCVR_37', 'XCVR_38', 'XCVR_39', 'XCVR_40', 'XCVR_41', 'XCVR_42', 'XCVR_43', 'XCVR_44', 'XCVR_45', 'XCVR_46', 'XCVR_47', 'XCVR_48', 'XCVR_49', 'XCVR_50', 'XCVR_51', 'XCVR_52', 'XCVR_53', 'XCVR_54', 'XCVR_55', 'XCVR_56', 'XCVR_57', 'XCVR_58', 'XCVR_59', 'XCVR_60',  'XCVR_61', 'XCVR_62', 'XCVR_63', 'XCVR_64']
    leds_folder = ['FAN_STATUS_LED' , 'SCM_FRU_LED' , 'SMB_FRU_LED', 'POWER_STATUS_LED' , 'SCM_STATUS_LED' , 'SYSTEM_STATUS_LED']
    sensors_folder = ['CPU_CORE_TEMP']
    xcvrs_folder = ['xcvr_1', 'xcvr_2', 'xcvr_3', 'xcvr_4', 'xcvr_5', 'xcvr_6', 'xcvr_7', 'xcvr_8', 'xcvr_9', 'xcvr_10', 'xcvr_11', 'xcvr_12', 'xcvr_13', 'xcvr_14', 'xcvr_15', 'xcvr_16', 'xcvr_17', 'xcvr_18', 'xcvr_19', 'xcvr_20', 'xcvr_21', 'xcvr_22', 'xcvr_23', 'xcvr_24', 'xcvr_25', 'xcvr_26', 'xcvr_27', 'xcvr_28', 'xcvr_29', 'xcvr_30', 'xcvr_31', 'xcvr_32', 'xcvr_33', 'xcvr_34', 'xcvr_35', 'xcvr_36', 'xcvr_37', 'xcvr_38', 'xcvr_39', 'xcvr_40', 'xcvr_41', 'xcvr_42', 'xcvr_43', 'xcvr_44', 'xcvr_45', 'xcvr_46', 'xcvr_47', 'xcvr_48', 'xcvr_49', 'xcvr_50', 'xcvr_51', 'xcvr_52', 'xcvr_53', 'xcvr_54', 'xcvr_55', 'xcvr_56', 'xcvr_57', 'xcvr_58', 'xcvr_59', 'xcvr_60',  'xcvr_61', 'xcvr_62', 'xcvr_63', 'xcvr_64']


    ######## upgrade/downgrade cases ########
    bsp_ver1 = [SwImage.getSwImage(SwImage.BSP).oldVersion]
    bsp_ver2 = [SwImage.getSwImage(SwImage.BSP).newVersion]

    bsp_folder = SwImage.getSwImage(SwImage.BSP).localImageDir
    bsp_package_file_path1 = SwImage.getSwImage(SwImage.BSP).oldlocalImageDir
    bsp_package_file_path2 = SwImage.getSwImage(SwImage.BSP).newlocalImageDir
    bsp_package_file1 = SwImage.getSwImage(SwImage.BSP).oldImage
    bsp_package_file1_zip = SwImage.getSwImage(SwImage.BSP).oldImageZip
    bsp_package_file2 = SwImage.getSwImage(SwImage.BSP).newImage
    bsp_package_file2_zip = SwImage.getSwImage(SwImage.BSP).newImageZip

    '''
    ver1 = SwImage.getSwImage(SwImage.FPGA).oldVersion['DOMFPGA1']
    flag = re.search('v.(\d+)',ver1)
    dom_ver1 = [hex(int(flag.group(1)))] if flag else ""
    ver2 = SwImage.getSwImage(SwImage.FPGA).newVersion['DOMFPGA1']
    flag = re.search('v.(\d+)',ver2)
    dom_ver2 = [hex(int(flag.group(1)))] if flag else ""
    '''
    dom_ver1 = [SwImage.getSwImage(SwImage.FPGA).oldVersion['DOMFPGA1']]
    dom_ver2 = [SwImage.getSwImage(SwImage.FPGA).newVersion['DOMFPGA1']]


    cpld1_ver1 = [SwImage.getSwImage(SwImage.SMB1).oldVersion]
    cpld1_ver2 = [SwImage.getSwImage(SwImage.SMB1).newVersion]
    cpld2_ver1 = [SwImage.getSwImage(SwImage.SMB2).oldVersion]
    cpld2_ver2 = [SwImage.getSwImage(SwImage.SMB2).newVersion]
    pwr_ver1   = [SwImage.getSwImage(SwImage.PWR).oldVersion]
    pwr_ver2   = [SwImage.getSwImage(SwImage.PWR).newVersion]

    '''
    ver1 = SwImage.getSwImage(SwImage.IOB).oldVersion
    flag = re.search('v.(\d+)',ver1)
    iob_ver1 = [hex(int(flag.group(1)))] if flag else ""
    ver2 = SwImage.getSwImage(SwImage.IOB).newVersion
    flag = re.search('v.(\d+)',ver2)
    iob_ver2 = [hex(int(flag.group(1)))] if flag else ""
    '''

    iob_ver1 = [SwImage.getSwImage(SwImage.IOB).oldVersion]
    iob_ver2 = [SwImage.getSwImage(SwImage.IOB).newVersion]
    th5_version = parser()
    th5_version['PCIe FW loader version'] = SwImage.getSwImage(SwImage.TH5).newVersion['PCIe FW loader version']

    #########unidiag system version##########
    unidiag_version = parser()
    unidiag_version['bios'] = SwImage.getSwImage(SwImage.BIOS).newVersion
    unidiag_version['bmc'] = SwImage.getSwImage(SwImage.BMC).newVersion
    unidiag_version['i210'] = SwImage.getSwImage(SwImage.I210).newVersion
    unidiag_version['sdk'] = SwImage.getSwImage(SwImage.SDK).newVersion
    unidiag_version['bsp'] = SwImage.getSwImage(SwImage.BSP).newVersion
    unidiag_version['udev'] = SwImage.getSwImage(SwImage.UDEV).newVersion
    unidiag_version['diag_os'] = SwImage.getSwImage(SwImage.DIAG_OS).newVersion
    unidiag_version['iob_fpga'] = SwImage.getSwImage(SwImage.IOB).newVersion
    unidiag_version['dom_fpga'] = SwImage.getSwImage(SwImage.FPGA).newVersion['DOMFPGA1']
    unidiag_version['smb1_cpld'] = SwImage.getSwImage(SwImage.SMB1).newVersion
    unidiag_version['smb2_cpld'] = SwImage.getSwImage(SwImage.SMB2).newVersion
    unidiag_version['pwr_cpld'] = SwImage.getSwImage(SwImage.PWR).newVersion

    ################I2C bus number, Address, Register Address or Value##############
    scm_reg_addr = '0x4'
    scm_reg_val = '0xde'
    smb_cpld_bus_no = '11'
    smb_cpld_addr = '0x33'
    smb_reg_addr = '0x4'
    smb_reg_val = '0xde'
    mcb_cpld_bus_no = '15'
    mcb_cpld_addr = '0x60'
    mcb_reg_addr = '0x4'
    mcb_reg_val = '0xde'
    cpld_write_val = '0xee'
    oob_reg_addr = '0xb1'
    oob_reg_val1 = '0x0' #Enabling write protect
    oob_reg_val2 = '0x2' #Disabling write protect
    smb_cpld_bus_no = '4'
    smb_cpld_addr = '0x35'
    smb_reg_addr = '0x42'
    smb_reg_val1 = '0x1'
    smb_reg_val2 = '0x0'
    ###Below needed####
    scm_cpld_bus_no = '4'
    scm_cpld_addr = '0x35'
    come_reg_addr = '0x42'
    come_reg_val1 = '0x1'
    come_reg_val2 = '0x0'
    come_eeprom_addr = '0x53'
    come_eeprom_addr2 = '0053'
    come_eeprom_bus_no = '1'
    gpio_line = '55=1'
    eeprom_chip_type = '24c02'
    pwr_cpld_bus_no = '17' # del
    pwr_cpld_addr = '0x60' # del
    pwr_reset_reg_addr = '0xf'
    pwr_reset_reg_val = '1'
    ###
    smb1_cpld_bus_no = '4'
    smb1_cpld_addr = '0x35'
    smb1_reg_addr = '0x4'
    smb1_reg_val = '0xde'
    smb2_cpld_bus_no = '11'
    smb2_cpld_addr = '0x33'
    smb2_reg_addr = '0x4'
    smb2_reg_val = '0xde'
    pwr_cpld_bus_no = '17'
    pwr_cpld_addr = '0x60'
    pwr_reg_addr = '0x4'
    pwr_reg_val = '0xde'

    ######Fan speed testcase#####
    MaxFanNum = 8
    fan_sensor_name = 'fancpld-i2c-15-33'
    fan_max_rpm = 13200
    fan_min_rpm = 1500
    speed_deviation = 2.5 # percentage

    ########GPIO testcase#######
    gpio_chip = 'gpiochip0'
    gpio_lines = 256
    gpio_line_number = 11
    gpio_bus_number = 2

    #######SPI driver testcase######
    spi_line_number = 'spi0.0'
    spi_dev_path = '/dev/spidev0.0'


    ####EEPROM related variables#####
    eeprom_path = "/var/unidiag/firmware/"
    smb_eeprom_modified = 'SMB_EEPROM_TEST'
    come_eeprom_modified = 'COME_EEPROM_TEST'

    #########I2C test #############
    i2c_buses = 74
    i2c_system_scan_pattern=[
	  "TH5 BRD EEPROM\s+I801 CH1\s+1\s+0x53\s+PASS",
      "SMB_CPLD_1\s+IOB CH2\s+4\s+0x35\s+PASS",
      "XDPE1A2G5B\(VDD_CORE\)\s+IOB CH3\s+5\s+0x76\s+PASS",
      "EEPROM\(OOB Switch\)\s+IOB CH5\s+7\s+0x50\s+PASS",
      "COME_CPLD\s+IOB CH6\s+8\s+0x40\s+PASS",
      "TH5\s+IOB CH7\s+9\s+0x44\s+PASS",
      "EEPROM\(SMB FRU#1\)\s+IOB CH8\s+10\s+0x56\s+PASS",
      "SMB_CPLD_2\s+IOB CH9\s+11\s+0x33\s+PASS",
      "SMB_CPLD_2_OSFP\s+IOB CH9\s+11\s+0x3e\s+PASS",
      "XP0R75V_TRVDD_1\(MP2975\)\s+IOB CH10\s+12\s+0x7d\s+PASS",
      "VRM_OSFP_3R3V_RIGHT\(MP2975\)\s+IOB CH10\s+12\s+0x7e\s+PASS",
      "VRM_OSFP_3R3V_LEFT\(MP2975\)\s+IOB CH11\s+13\s+0x7a\s+PASS",
      "XP0R75V_TRVDD_0\(MP2975\)\s+IOB CH11\s+13\s+0x7b\s+PASS",
      "LM75B\(U67\)_RIGHT_TOP_INLET\s+IOB CH12\s+14\s+0x49\s+PASS",
      "LM75B\(U69\)_RIGHT_BOT_INLET\s+IOB CH12\s+14\s+0x48\s+PASS",
      "PWR CPLD\s+IOB CH15\s+17\s+0x60\s+PASS",
      "LM75B\(U51\)_TOP_OUTLET\s+IOB CH16\s+18\s+0x48\s+PASS",
      "LM75B \(U57\)_BOT_PWR STAGE\s+IOB CH16\s+18\s+0x49\s+PASS",
      "LM75B\(U77\)_LEFT_BOT_INLET\s+IOB CH20\s+22\s+0x48\s+PASS",
      "ADM1272\(48V Hotswap\)\s+IOB CH21\s+23\s+0x10\s+PASS",
      "RC19004\(PCIe CLK Buffer Gen4\)\s+IOB CH22\s+24\s+0x6f\s+PASS",
      "LM75B\(U39\)_TOP_TH5\s+IOB CH24\s+26\s+0x48\s+PASS",
      "LM75B\(U182\)_BOT_TH5\s+IOB CH24\s+26\s+0x49\s+PASS",
      "ADC128D8 #4\s+IOB CH25\s+27\s+0x1d\s+PASS",
      "ADC128D8 #5\s+IOB CH25\s+27\s+0x35\s+PASS",
      "ADC128D8 #6\s+IOB CH25\s+27\s+0x37\s+PASS",
      "ADC128D818 #1\s+IOB CH26\s+28\s+0x1d\s+PASS",
      "ADC128D818 #2\s+IOB CH26\s+28\s+0x35\s+PASS",
      "ADC128D818 #3\s+IOB CH26\s+28\s+0x37\s+PASS",
      "test_scan_i2c_smb: Scanned 29 i2c devices, 0 failed",

      "LM75B\(U1\)_PDB\s+IOB CH21\s+23\s+0x48\s+PASS",
      "Q50SN120A4\(Brick1\)\s+IOB CH21\s+23\s+0x60\s+PASS",
      "Q50SN120A4\(Brick2\)\s+IOB CH21\s+23\s+0x61\s+PASS",
      "test_scan_i2c_pdb: Scanned 3 i2c devices, 0 failed",

      "COMe EEPROM\s+IOB CH14\s+16\s+0x56\s+PASS",
      "OUTLET Sensor\s+IOB CH14\s+16\s+0x4a\s+PASS",
      "INLET Sensor\s+IOB CH14\s+16\s+0x48\s+PASS",
      "COMe_CPLD\s+IOB CH14\s+16\s+0x0f\s+PASS",
      "COMe_CPLD_2\s+IOB CH14\s+16\s+0x1f\s+PASS",
      "VNN_PCH\s+IOB CH23\s+25\s+0x11\s+PASS",
      "1V05_STBY\s+IOB CH23\s+25\s+0x22\s+PASS",
      "1V8_STBY\s+IOB CH23\s+25\s+0x76\s+PASS",
      "VDDQ\s+IOB CH23\s+25\s+0x45\s+PASS",
      "VCCANA\s+IOB CH23\s+25\s+0x66\s+PASS",
      "test_scan_i2c_come: Scanned 10 i2c devices, 0 failed",

      "COMe FRU EEPROM\s+BMC CH0\s+0\s+0x56\s+PASS",
      "COMe Inlet Temp\s+BMC CH0\s+0\s+0x48\s+PASS",
      "COMe Outlet Temp\s+BMC CH0\s+0\s+0x4a\s+PASS",
      "COMe CPLD ADC\s+BMC CH0\s+0\s+0x0f\s+PASS",
      "COMe CPLD Misc Control\s+BMC CH0\s+0\s+0x1f\s+PASS",
      "SMB_CPLD_1\s+BMC CH1\s+1\s+0x35\s+PASS",
      "SMB_FRU#2\s+BMC CH3\s+3\s+0x56\s+PASS",
      "PCA9555\s+BMC CH4\s+4\s+0x27\s+PASS",
      "COMe SML0\s+BMC CH5\s+5\s+0x16\s+PASS",
      "BMC Thermal sensor\s+BMC CH8\s+8\s+0x4a\s+PASS",
      "BMC EEPROM\s+BMC CH8\s+8\s+0x51\s+PASS",
      "PWR_CPLD\s+BMC CH12\s+12\s+0x60\s+PASS",
      "IOBFPGA\s+BMC CH13\s+13\s+0x35\s+PASS",
      "test_scan_i2c_bmc: Scanned 13 i2c devices, 0 failed"
    ]

    ####Version utility######
    flashrom_version = 'flashrom 1.4'
    ddtool_version = '8.32'

if "minipack3" in devicename.lower():
    fb_variant = 'minipack3'
    #### BSP_TC_001_BSP Structure of FBOSS ####
    test_cmd_kernel_test = 'uname -a'
    expected_kernel = ['Linux localhost.localdomain 5']
    test_cmd_DiagOs_test = 'cat /etc/os-release'
    expected_os = ['CentOS Stream 9']
    test_cmd_BSPlist_test = 'ls /usr/lib/modules/5.19.0/kernel/fboss/'
    expected_bsp_files = ['fbiob-pci.ko', 'janga_smbcpld.ko', 'mp3_smbcpld.ko', 'regbit-sysfs.ko', 'fpga-info.ko' , 'mcbcpld.ko', 'mtia_pwrcpld.ko', 'spi-fbiob.ko', 'gpio-fbiob.ko', 'mp3_fancpld.ko', 'mtia_smbcpld.ko', 'tahan_smbcpld.ko', 'i2c-fbiob.ko', 'mp3_scmcpld.ko', 'port-led.ko', 'xcvr-ctrl.ko']

    #####BSP_TC_002_BSP_Driver_Install_Uninstall_Test ######
    #removed_bsp_device_folder = ['cplds', 'eeprom', 'gpio', 'leds', 'xcvrs']
    removed_bsp_device_folder = ['cplds', 'eeprom', 'gpio', 'flashes', 'xcvrs']
    #installed_bsp_device_folder = ['cplds', 'eeprom', 'fpgas', 'gpio', 'i2c-busses', 'leds', 'sensors', 'xcvrs']

    installed_bsp_device_folder = ['cplds', 'eeprom', 'flashes', 'fpgas', 'gpio', 'i2c-busses', 'sensors', 'watchdogs']
    #old_installed_bsp_device_folder = ['fpgas', 'i2c-busses', 'leds', 'sensors']
    old_installed_bsp_device_folder = ['cplds', 'eeprom', 'flashes', 'fpgas', 'gpio', 'i2c-busses', 'sensors', 'xcvrs']
    cplds_folder = ['FAN_CPLD', 'MCB_CPLD','SCM_CPLD', 'SMB_CPLD']
    eeprom_folder = ['MCB_EEPROM', 'SCM_EEPROM', 'SMB_EEPROM', 'FCB_EEPROM']
    fpgas_folder = ['IOB_FPGA']
    flashes_folder = ['DOM1_FLASH','DOM2_FLASH','I210_SCMCPLD_FLASH','IOB_FLASH','MCBCPLD_FLASH','SMBCPLD_FLASH','TH5_FLASH']
    gpio_folder = ['IOB_GPIO_CHIP_0']
    watchdogs_folder = ['FAN_WATCHDOG']
    #i2c_busses_folder = ['DOM1_I2C_BUS_33', 'DOM1_I2C_BUS_34', 'DOM2_I2C_BUS_33', 'DOM2_I2C_BUS_34', 'I801_I2C_BUS', 'ISMT_I2C_BUS', 'IOB0_PCA9548_CH0', 'IOB0_PCA9548_CH1', 'IOB0_PCA9548_CH2', 'IOB0_PCA9548_CH3', 'IOB0_PCA9548_CH4', 'IOB0_PCA9548_CH5', 'IOB0_PCA9548_CH6', 'IOB0_PCA9548_CH7', 'IOB1_PCA9546_CH0', 'IOB1_PCA9546_CH1', 'IOB1_PCA9546_CH2', 'IOB1_PCA9546_CH3', 'IOB_I2C_BUS_1', 'IOB_I2C_BUS_2', 'IOB_I2C_BUS_3', 'IOB_I2C_BUS_4', 'IOB_I2C_BUS_5', 'IOB_I2C_BUS_6', 'IOB_I2C_BUS_7', 'IOB_I2C_BUS_8', 'IOB_I2C_BUS_9', 'IOB_I2C_BUS_10', 'IOB_I2C_BUS_11', 'IOB_I2C_BUS_12', 'IOB_I2C_BUS_13', 'IOB_I2C_BUS_14', 'IOB_I2C_BUS_15', 'IOB_I2C_BUS_16', 'IOB_I2C_BUS_17', 'IOB_I2C_BUS_18', 'IOB_I2C_BUS_19', 'IOB_I2C_BUS_20', 'IOB_I2C_BUS_21', 'IOB_I2C_BUS_22', 'IOB_I2C_BUS_23', 'IOB_I2C_BUS_24', 'IOB_I2C_BUS_25', 'IOB_I2C_BUS_26', 'IOB_I2C_BUS_27', 'XCVR_1', 'XCVR_2', 'XCVR_3', 'XCVR_4', 'XCVR_5', 'XCVR_6', 'XCVR_7', 'XCVR_8', 'XCVR_9', 'XCVR_10', 'XCVR_11', 'XCVR_12', 'XCVR_13', 'XCVR_14', 'XCVR_15', 'XCVR_16', 'XCVR_17', 'XCVR_18', 'XCVR_19', 'XCVR_20', 'XCVR_21', 'XCVR_22', 'XCVR_23', 'XCVR_24', 'XCVR_25', 'XCVR_26', 'XCVR_27', 'XCVR_28', 'XCVR_29', 'XCVR_30', 'XCVR_31', 'XCVR_32', 'XCVR_33', 'XCVR_34', 'XCVR_35', 'XCVR_36', 'XCVR_37', 'XCVR_38', 'XCVR_39', 'XCVR_40', 'XCVR_41', 'XCVR_42', 'XCVR_43', 'XCVR_44', 'XCVR_45', 'XCVR_46', 'XCVR_47', 'XCVR_48', 'XCVR_49', 'XCVR_50', 'XCVR_51', 'XCVR_52', 'XCVR_53', 'XCVR_54', 'XCVR_55', 'XCVR_56', 'XCVR_57', 'XCVR_58', 'XCVR_59', 'XCVR_60',  'XCVR_61', 'XCVR_62', 'XCVR_63', 'XCVR_64']
    i2c_busses_folder = ['DOM1_I2C_BUS_33', 'DOM1_I2C_BUS_34', 'DOM2_I2C_BUS_33', 'DOM2_I2C_BUS_34', 'I801_I2C_BUS', 'ISMT_I2C_BUS',  'IOB0_PCA9548_CH1', 'IOB0_PCA9548_CH2', 'IOB0_PCA9548_CH3', 'IOB0_PCA9548_CH4', 'IOB0_PCA9548_CH5', 'IOB0_PCA9548_CH6', 'IOB0_PCA9548_CH7', 'IOB0_PCA9548_CH8',  'IOB1_PCA9546_CH1', 'IOB1_PCA9546_CH2', 'IOB1_PCA9546_CH3', 'IOB1_PCA9546_CH4', 'IOB_I2C_BUS_1', 'IOB_I2C_BUS_2', 'IOB_I2C_BUS_3', 'IOB_I2C_BUS_4', 'IOB_I2C_BUS_5', 'IOB_I2C_BUS_6', 'IOB_I2C_BUS_7', 'IOB_I2C_BUS_8', 'IOB_I2C_BUS_9', 'IOB_I2C_BUS_10', 'IOB_I2C_BUS_11', 'IOB_I2C_BUS_12', 'IOB_I2C_BUS_13', 'IOB_I2C_BUS_14', 'IOB_I2C_BUS_15', 'IOB_I2C_BUS_16', 'IOB_I2C_BUS_17', 'IOB_I2C_BUS_18', 'IOB_I2C_BUS_19', 'IOB_I2C_BUS_20', 'IOB_I2C_BUS_21', 'IOB_I2C_BUS_22', 'IOB_I2C_BUS_23', 'IOB_I2C_BUS_24', 'IOB_I2C_BUS_25', 'IOB_I2C_BUS_26', 'IOB_I2C_BUS_27', 'XCVR_1', 'XCVR_2', 'XCVR_3', 'XCVR_4', 'XCVR_5', 'XCVR_6', 'XCVR_7', 'XCVR_8', 'XCVR_9', 'XCVR_10', 'XCVR_11', 'XCVR_12', 'XCVR_13', 'XCVR_14', 'XCVR_15', 'XCVR_16', 'XCVR_17', 'XCVR_18', 'XCVR_19', 'XCVR_20', 'XCVR_21', 'XCVR_22', 'XCVR_23', 'XCVR_24', 'XCVR_25', 'XCVR_26', 'XCVR_27', 'XCVR_28', 'XCVR_29', 'XCVR_30', 'XCVR_31', 'XCVR_32', 'XCVR_33', 'XCVR_34', 'XCVR_35', 'XCVR_36', 'XCVR_37', 'XCVR_38', 'XCVR_39', 'XCVR_40', 'XCVR_41', 'XCVR_42', 'XCVR_43', 'XCVR_44', 'XCVR_45', 'XCVR_46', 'XCVR_47', 'XCVR_48', 'XCVR_49', 'XCVR_50', 'XCVR_51', 'XCVR_52', 'XCVR_53', 'XCVR_54', 'XCVR_55', 'XCVR_56', 'XCVR_57', 'XCVR_58', 'XCVR_59', 'XCVR_60',  'XCVR_61', 'XCVR_62', 'XCVR_63', 'XCVR_64']
    leds_folder = ['FAN_STATUS_LED' , 'SCM_FRU_LED' , 'SMB_FRU_LED', 'POWER_STATUS_LED' , 'SCM_STATUS_LED' , 'SYSTEM_STATUS_LED']
    sensors_folder = ['3V3_L_U1_MP2891_1', '3V3_L_U8_TMP1075_1', '3V3_R_U1_MP2891_1', '3V3_R_U8_TMP1075_1', 'BMC_UXX_LM75_3', 'CPU_CORE_TEMP', 'FAN_PRESENT_1', 'FAN_PRESENT_2', 'FAN_PRESENT_3', 'FAN_PRESENT_4', 'FAN_PRESENT_5', 'FAN_PRESENT_6', 'FAN_PRESENT_7', 'FAN_PRESENT_8', 'FAN_PWM_1', 'FAN_PWM_2', 'FAN_PWM_3', 'FAN_PWM_3', 'FAN_PWM_4', 'FAN_PWM_5', 'FAN_PWM_6', 'FAN_PWM_7', 'FAN_PWM_8', 'PWM_ENABLE_1', 'PWM_ENABLE_2', 'PWM_ENABLE_3', 'PWM_ENABLE_4', 'PWM_ENABLE_5', 'PWM_ENABLE_6','PWM_ENABLE_7', 'PWM_ENABLE_8', 'SCM_U10_ADM1278_1', 'SCM_U36_LM75_1', 'FCB_B_U1_TMP1075_1', 'SCM_U37_LM75_2', 'FCB_B_U5_TMP1075_2','SCM_U59_ADC128D818_1', 'FCB_T_U1_TMP1075_1', 'SMB_U122_PMBUS_1', 'FCB_T_U5_TMP1075_2', 'SMB_U182_TMP1075_2', 'MCB_U25_TMP1075_1', 'SMB_U206_ADC128D818_1', 'MCB_U35_ADC128D818_1', 'SMB_U207_ADC128D818_2', 'PDB_L_U1_TMP1075_1', 'SMB_U208_ADC128D818_1', 'PDB_R_U1_TMP1075_1', 'SMB_U39_TMP1075_1', 'SMB_U51_TMP1075_1', 'SMB_U57_TMP1075_2', 'SMB_U86_MP2975_1', 'SMB_U92_MP2975_1']

    xcvrs_folder_check = 0
    if xcvrs_folder_check:
       installed_bsp_device_folder = ['cplds', 'eeprom', 'flashes', 'fpgas', 'gpio', 'i2c-busses', 'sensors', 'xcvrs', 'watchdogs']
    xcvrs_folder = ['xcvr_1', 'xcvr_2', 'xcvr_3', 'xcvr_4', 'xcvr_5', 'xcvr_6', 'xcvr_7', 'xcvr_8', 'xcvr_9', 'xcvr_10', 'xcvr_11', 'xcvr_12', 'xcvr_13', 'xcvr_14', 'xcvr_15', 'xcvr_16', 'xcvr_17', 'xcvr_18', 'xcvr_19', 'xcvr_20', 'xcvr_21', 'xcvr_22', 'xcvr_23', 'xcvr_24', 'xcvr_25', 'xcvr_26', 'xcvr_27', 'xcvr_28', 'xcvr_29', 'xcvr_30', 'xcvr_31', 'xcvr_32', 'xcvr_33', 'xcvr_34', 'xcvr_35', 'xcvr_36', 'xcvr_37', 'xcvr_38', 'xcvr_39', 'xcvr_40', 'xcvr_41', 'xcvr_42', 'xcvr_43', 'xcvr_44', 'xcvr_45', 'xcvr_46', 'xcvr_47', 'xcvr_48', 'xcvr_49', 'xcvr_50', 'xcvr_51', 'xcvr_52', 'xcvr_53', 'xcvr_54', 'xcvr_55', 'xcvr_56', 'xcvr_57', 'xcvr_58', 'xcvr_59', 'xcvr_60',  'xcvr_61', 'xcvr_62', 'xcvr_63', 'xcvr_64']


    ######## upgrade/downgrade cases ########
    bsp_ver1 = [SwImage.getSwImage(SwImage.BSP).oldVersion]
    bsp_ver2 = [SwImage.getSwImage(SwImage.BSP).newVersion]
    bsp_zip_file = [SwImage.getSwImage(SwImage.BSP).newImageZip]

    bsp_folder = SwImage.getSwImage(SwImage.BSP).localImageDir
    bsp_package_file_path1 = SwImage.getSwImage(SwImage.BSP).oldlocalImageDir
    bsp_package_file_path2 = SwImage.getSwImage(SwImage.BSP).newlocalImageDir
    bsp_package_file1 = SwImage.getSwImage(SwImage.BSP).oldImage
    bsp_package_file1_zip = SwImage.getSwImage(SwImage.BSP).oldImageZip
    bsp_package_file2 = SwImage.getSwImage(SwImage.BSP).newImage
    bsp_package_file2_zip = SwImage.getSwImage(SwImage.BSP).newImageZip

    '''
    ver1 = SwImage.getSwImage(SwImage.FPGA).oldVersion['DOMFPGA1']
    flag = re.search('v.(\d+)',ver1)
    dom1_ver1 = [hex(int(flag.group(1)))] if flag else ""
    ver2 = SwImage.getSwImage(SwImage.FPGA).newVersion['DOMFPGA1']
    flag = re.search('v.(\d+)',ver2)
    dom1_ver2 = [hex(int(flag.group(1)))] if flag else ""

    ver1 = SwImage.getSwImage(SwImage.FPGA).oldVersion['DOMFPGA2']
    flag = re.search('v.(\d+)',ver1)
    dom2_ver1 = [hex(int(flag.group(1)))] if flag else ""
    ver2 = SwImage.getSwImage(SwImage.FPGA).newVersion['DOMFPGA2']
    flag = re.search('v.(\d+)',ver2)
    dom2_ver2 = [hex(int(flag.group(1)))] if flag else ""
    '''
    dom1_ver1 = [SwImage.getSwImage(SwImage.FPGA).oldVersion['DOMFPGA1']]
    dom1_ver2 = [SwImage.getSwImage(SwImage.FPGA).newVersion['DOMFPGA1']]
    dom2_ver1 = [SwImage.getSwImage(SwImage.FPGA).oldVersion['DOMFPGA2']]
    dom2_ver2 = [SwImage.getSwImage(SwImage.FPGA).newVersion['DOMFPGA2']]
    cpld_ver1 = [SwImage.getSwImage(SwImage.MCB).oldVersion]
    cpld_ver2 = [SwImage.getSwImage(SwImage.MCB).newVersion]

    '''
    ver1 = SwImage.getSwImage(SwImage.IOB).oldVersion
    flag = re.search('v.(\d+)',ver1)
    iob_ver1 = [hex(int(flag.group(1)))] if flag else ""
    ver2 = SwImage.getSwImage(SwImage.IOB).newVersion
    flag = re.search('v.(\d+)',ver2)
    iob_ver2 = [hex(int(flag.group(1)))] if flag else ""
    '''
    iob_ver1 = [SwImage.getSwImage(SwImage.IOB).oldVersion]
    iob_ver2 = [SwImage.getSwImage(SwImage.IOB).newVersion]
    th5_version = parser()
    th5_version['PCIe FW loader version'] = SwImage.getSwImage(SwImage.TH5).newVersion['PCIe FW loader version']

    #########unidiag system version##########
    unidiag_version = parser()
    unidiag_version['bios'] = SwImage.getSwImage(SwImage.BIOS).newVersion
    unidiag_version['bmc'] = SwImage.getSwImage(SwImage.BMC).newVersion
    unidiag_version['i210'] = SwImage.getSwImage(SwImage.I210).newVersion
    unidiag_version['sdk'] = SwImage.getSwImage(SwImage.SDK).newVersion
    unidiag_version['bsp'] = SwImage.getSwImage(SwImage.BSP).newVersion
    unidiag_version['udev'] = SwImage.getSwImage(SwImage.UDEV).newVersion
    unidiag_version['diag_os'] = SwImage.getSwImage(SwImage.DIAG_OS).newVersion
    unidiag_version['iob_fpga'] = SwImage.getSwImage(SwImage.IOB).newVersion
    unidiag_version['dom1_fpga'] = SwImage.getSwImage(SwImage.FPGA).newVersion['DOMFPGA1']
    unidiag_version['dom2_fpga'] = SwImage.getSwImage(SwImage.FPGA).newVersion['DOMFPGA2']
    unidiag_version['scm_cpld'] = SwImage.getSwImage(SwImage.SCM).newVersion['CPLD Version']
    unidiag_version['smb_cpld'] = SwImage.getSwImage(SwImage.SMB).newVersion
    unidiag_version['mcb_cpld'] = SwImage.getSwImage(SwImage.MCB).newVersion

    ################I2C bus number, Address, Register Address or Value##############
    scm_cpld_bus_no = '4'
    scm_cpld_addr = '0x35'
    scm_reg_addr = '0x4'
    scm_reg_val = '0xde'
    smb_cpld_bus_no = '11'
    smb_cpld_addr = '0x33'
    smb_reg_addr = '0x4'
    smb_reg_val = '0xde'
    mcb_cpld_bus_no = '15'
    mcb_cpld_addr = '0x60'
    mcb_reg_addr = '0x4'
    mcb_reg_val = '0xde'
    cpld_write_val = '0xee'
    oob_reg_addr = '0xb1'
    oob_reg_val1 = '0x0' #Enabling write protect
    oob_reg_val2 = '0x2' #Disabling write protect
    fcb_reg_addr = '0x05'
    fcb_reg_val1 = '0xf0'
    fcb_reg_val2 = '0x03'
    gpio_line = '55=1'
    eeprom_chip_type = '24c02'
    scm_eeprom_bus_no = '102'
    scm_eeprom_addr = '0x50'
    scm_eeprom_addr2 = '0050'

    ######Fan speed testcase#####
    MaxFanNum = 8
    fan_sensor_name = 'mp3_fancpld-i2c-15-33'
    fan_max_rpm1 = 12200
    fan_max_rpm2 = 11400
    speed_deviation = 2.5 # percentage
    hw_monitor = 'hwmon13'
    fan_speen_cpld_max = 40

    ########GPIO testcase#######
    gpio_chip = 'gpiochip0'
    gpio_lines = 256
    gpio_line_number = 11
    gpio_bus_number = 2

    #######SPI driver testcase######
    spi_line_number = 'spi0.0'
    spi_dev_path = '/dev/spidev0.0'

    #########I2C test #############
    i2c_buses = 108
    i2c_system_scan_pattern=[
     "TMP1075 Thermal sensor.*IOB CH12.*14.*0x4e.*PASS",
     "MCB EEPROM\s+IOB CH12\s+14\s+0x53.*PASS",
     "MCB CPLD FAN Control\s+IOB CH13\s+15\s+0x33.*PASS",
     "MCB CPLD MCB Control\s+IOB CH13\s+15\s+0x60.*PASS",
     "Fan1_HSC PTPS25990\s+IOB CH18\s+20\s+0x4c.*PASS",
     "Fan2_HSC PTPS25990\s+IOB CH19\s+21\s+0x4c.*PASS",
     "Fan3_HSC PTPS25990\s+IOB CH20\s+22\s+0x4c.*PASS",
     "Fan4_HSC PTPS25990\s+IOB CH21\s+23\s+0x4c.*PASS",
     "Fan5_HSC PTPS25990\s+IOB CH22\s+24\s+0x4c.*PASS",
     "Fan6_HSC PTPS25990\s+IOB CH23\s+25\s+0x4c.*PASS",
     "Fan7_HSC PTPS25990\s+IOB CH24\s+26\s+0x4c.*PASS",
     "Fan8_HSC PTPS25990\s+IOB CH25\s+27\s+0x4c.*PASS",
     "MCB ADC ADC128D818\s+IOB CH26\s+28\s+0x37.*PASS",
     "detect_mcb_i2c_device: Scanned 13 i2c devices, 0 failed.",

     "XDPE1A2G5B VDD_CORE\s+IOB CH3\s+5\s+0x76.*PASS",
     "SMB ADC1 ADC128D818\s+IOB CH6\s+8\s+0x1d.*PASS",
     "SMB ADC2 ADC128D818\s+IOB CH6\s+8\s+0x1f.*PASS",
     "TH5 SW ASIC\s+IOB CH7\s+9\s+0x44.*PASS",
     "SMB ADC3 ADC128D818\s+IOB CH8\s+10\s+0x35\s+PASS",
     "SMB CPLD\s+IOB CH9\s+11\s+0x33\s+PASS",
     "SMB CPLD OSFP\s+IOB CH9\s+11\s+0x3e\s+PASS",
     "SMB EEPROM\s+IOB CH9\s+11\s+0x50\s+PASS",
     "TRVDD_1 MP2975\s+IOB CH10\s+12\s+0x7d\s+PASS",
     "TRVDD_0 MP2975\s+IOB CH11\s+13\s+0x7b\s+PASS",
     "TMP1075 Thermal Sensor#1\s+DOM1 CH33\s+62\s+0x48\s+PASS",
     "TMP1075 Thermal Sensor#2\s+DOM1 CH33\s+62\s+0x49\s+PASS",
     "TMP1075 Thermal Sensor#3\s+DOM2 CH33\s+96\s+0x4a\s+PASS",
     "TMP1075 Thermal Sensor#4\s+DOM2 CH33\s+96\s+0x4b\s+PASS",
     "detect_smb_i2c_device: Scanned 14 i2c devices, 0 failed",

     "PCA9548\s+IOB CH0\s+2\s+0x70\s+PASS",
     "PCA9546\s+IOB CH1\s+3\s+0x70\s+PASS",
     "SCM CPLD\s+IOB CH2\s+4\s+0x35\s+PASS",
     "ADM1278 Hot Swap\s+PCA9548 CH0\s+98\s+0x10\s+PASS",
     "LM75_#1 Thermal sensor\s+PCA9548 CH1\s+99\s+0x4c\s+PASS",
     "LM75_#2 Thermal sensor\s+PCA9548 CH1\s+99\s+0x4d\s+PASS",
     "SCM_ADC ADC128D818\s+PCA9548 CH2\s+100\s+0x37\s+PASS",
     "SCM FRU E2PROM#1\s+PCA9548 CH3\s+101\s+0x54\s+PASS",
     "88E6321 E2PROM\s+PCA9548 CH4\s+102\s+0x50\s+PASS",
     "PCIe Clk buffer #1 RC19004\s+PCA9548 CH6\s+104\s+0x6c\s+PASS",
     "PCIe Clk buffer #2 RC19004\s+PCA9548 CH6\s+104\s+0x6f\s+PASS",
     "detect_scm_i2c_device: Scanned 11 i2c devices, 0 failed.",
     
     "FCB_T EEPROM\s+IOB CH14\s+16\s+0x53\s+PASS",
     "FCB_T TMP1075#1\s+IOB CH15\s+17\s+0x49\s+PASS",
     "FCB_T TMP1075#2\s+IOB CH15\s+17\s+0x4b\s+PASS",
     "FCB_B TMP1075#1\s+IOB CH16\s+18\s+0x49\s+PASS",
     "FCB_B TMP1075#2\s+IOB CH16\s+18\s+0x4b\s+PASS",
     "detect_fcb_i2c_device: Scanned 5 i2c devices, 0 failed.",

     "TMP1075 Thermal Sensor \s+IOB CH4\s+6\s+0x48\s+PASS",
     "PSU 1 FRU\s+IOB CH4\s+6\s+0x51\s+PASS",
     "PSU 1 MCU\s+IOB CH4\s+6\s+0x59\s+PASS",
     "TMP1075 Thermal Sensor\s+IOB CH5\s+7\s+0x48\s+PASS",
     "PSU 2 FRU\s+IOB CH5\s+7\s+0x51\s+PASS",
     "PSU 2 MCU\s+IOB CH5\s+7\s+0x59\s+PASS",
     "detect_pdb_i2c_device: Scanned 6 i2c devices, 0 failed.",

     "XP3R3V_LEFT MPS - MP2891 \s+DOM1 CH32\s+61\s+0x23\s+PASS",
     "TMP1075 Thermal Sensor   \s+DOM1 CH32\s+61\s+0x48\s+PASS",
     "XP3R3V_RIGHT MPS - MP2891\s+DOM2 CH32\s+95\s+0x23\s+PASS",
     "TMP1075 Thermal Sensor   \s+DOM2 CH32\s+95\s+0x48\s+PASS",
     "detect_3v3_card_i2c_device: Scanned 4 i2c devices, 0 failed.",

     "VNN_PCH\s+PCA9546 CH1\s+107\s+0x11\s+PASS",
     "1V05_STBY\s+PCA9546 CH1\s+107\s+0x22\s+PASS",
     "1V8_STBY\s+PCA9546 CH1\s+107\s+0x76\s+PASS",
     "VDDQ\s+PCA9546 CH1\s+107\s+0x45\s+PASS",
     "VCCANA_CPU\s+PCA9546 CH1\s+107\s+0x66\s+PASS",
     "FRU\s+PCA9546 CH2\s+108\s+0x56\s+PASS",
     "OUTLET Sensor\s+PCA9546 CH2\s+108\s+0x4a\s+PASS",
     "INLET Sensor\s+PCA9546 CH2\s+108\s+0x48\s+PASS",
     "detect_come_i2c_device: Scanned 8 i2c devices, 0 failed.",

     "SCM FRU EEPROM#2\s+BMC CH3\s+3\s+0x56\s+PASS",
     "PCA9555\s+BMC CH4\s+4\s+0x27\s+PASS",
     "COMe CPU\s+BMC CH5\s+5\s+0x16\s+PASS",
     "FCB_B EEPROM\s+BMC CH6\s+6\s+0x53\s+PASS",
     "BMC EEPROM\s+BMC CH8\s+8\s+0x51\s+PASS",
     "LM75 Thermal Sensor \s+BMC CH8\s+8\s+0x51\s+PASS",
     "MCB CPLD MCB Control\s+BMC CH12\s+12\s+ 0x60\s+PASS",
     "IOB FPGA\s+BMC CH13\s+13\s+ 0x35\s+PASS",
     "detect_bmc_i2c_device: Scanned 8 i2c devices, 0 failed."
    ]



    ####Version utility######
    flashrom_version = 'flashrom v1.2'
    ddtool_version = '8.32'

    ####EEPROM related variables#####
    eeprom_path = "/var/unidiag/firmware/"
    scm_eeprom_modified = 'SCM_EEPROM_TEST'
    smb_eeprom_modified = 'SMB_EEPROM_TEST'
    mcb_eeprom_modified = 'MCB_EEPROM_TEST'
    fcb_eeprom_modified = 'FCB_EEPROM_TEST'
