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
#######################################################################################################################
# Script       : bsp_keywords.robot                                                                               #
# Date         : ##########, 2024                                                                                    #
# Author       : Ishwariya Vetrivel. <ivetrivel@celestica.com>                                                               #
# Description  : This script used as keywords in bsp_test.robot                                                   #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for bsp testing                                                                                 #
#######################################################################################################################

*** Settings ***
Variables         bsp_variable.py
Library           bsp_lib.py
Library           CommonLib.py
Library           OperatingSystem

*** Keywords ***
check kernel version
  test execute command  DUT  ${test_cmd_kernel_test}  ${CENTOS_MODE}  ${expected_kernel}

check Diag Os version
  test execute command  DUT  ${test_cmd_DiagOs_test}  ${CENTOS_MODE}  ${expected_os}

check BSP Structure
  test execute command  DUT  ${test_cmd_BSPlist_test}  ${CENTOS_MODE}  ${expected_bsp_files}

prepare images  ${image_type}
    Step  1  get dhcp ip address  DUT  eth0  ${CENTOS_MODE}
    Step  2  download images  DUT  ${image_type}

downgrade bsp
  [Arguments]  ${bsp_device_folder}
  Independent Step  1  bsp driver update  DUT  remove
  Independent Step  2  reboot come  DUT
  Independent Step  3  check bsp device folder  DUT  remove  ${removed_bsp_device_folder}  False
  Independent Step  4  bsp driver update  DUT  install  False
  Independent Step  5  power reset chassis  DUT
  Independent Step  6  check bsp device folder  DUT  install  ${installed_bsp_device_folder}  False

upgrade bsp
  [Arguments]  ${bsp_device_folder}
  Independent Step  1  bsp driver update  DUT  remove  False
  Independent Step  2  reboot come  DUT
  Independent Step  3  check bsp device folder  DUT  remove  ${removed_bsp_device_folder}  False
  Independent Step  4  bsp driver update  DUT  install  True
  Independent Step  5  power reset chassis  DUT
  Independent Step  6  check bsp device folder  DUT  install  ${installed_bsp_device_folder}

downgrade fpga
  [Arguments]  ${fpga_type}
  IF  '${fb_variant}' == 'minipack3'
     minipack3 online update  DUT  ${fpga_type}  False
  ELSE IF  '${fb_variant}' == 'minerva'
     minerva online update  DUT  ${fpga_type}  False
  END
  power reset chassis  DUT

upgrade fpga
  [Arguments]  ${fpga_type}
  IF  '${fb_variant}' == 'minipack3'
     minipack3 online update  DUT  ${fpga_type}  True
  ELSE IF  '${fb_variant}' == 'minerva'
     minerva online update  DUT  ${fpga_type}  True
  END
  power reset chassis  DUT

downgrade firmware
  [Arguments]  ${fw_type}
  IF  '${fb_variant}' == 'minipack3'
     minipack3 online update  DUT  ${fw_type}  False
  ELSE IF  '${fb_variant}' == 'minerva'
     minerva online update  DUT  ${fw_type}  False
  END
  power reset chassis  DUT

upgrade firmware
  [Arguments]  ${fw_type}
  IF  '${fb_variant}' == 'minipack3'
     minipack3 online update  DUT  ${fw_type}  False
  ELSE IF  '${fb_variant}' == 'minerva'
     minerva online update  DUT  ${fw_type}  False
  END
  power reset chassis  DUT

download cpld images
  download images  DUT  MCB
  download images  DUT  SCM
  download images  DUT  SMB

clean cpld images
  clean images  DUT  MCB
  clean images  DUT  SCM
  clean images  DUT  SMB

make oob firmware writable
  disable write protect  DUT  OOB_EEPROM
  download images  DUT  OOB

clean oob firmware images
  clean images  DUT  OOB
  enable write protect  DUT  OOB_EEPROM

make eeprom ready
  [Arguments]   ${eeprom_type}
  disable write protect  DUT  ${eeprom_type}_EEPROM
  store eeprom  ${eeprom_type}

restore eeprom state
  [Arguments]   ${eeprom_type}
  restore eeprom  ${eeprom_type}
  enable write protect  DUT  ${eeprom_type}_EEPROM

verify cpld version
  [Arguments]   ${fw_type}  ${expected_version}
  verify firmware version  DUT  scm  ${expected_version}
  verify firmware version  DUT  smb  ${expected_version}
  verify firmware version  DUT  mcb  ${expected_version}

downgrade cpld
  [Arguments]   ${fw_type}
  Independent Step  1  minipack3 online update  DUT  scm  False
  Independent Step  2  minipack3 online update  DUT  smb  False
  Independent Step  3  minipack3 online update  DUT  mcb  False
  Step  4  power reset chassis  DUT

upgrade cpld
  [Arguments]   ${fw_type}
  Independent Step  1  minipack3 online update  DUT  scm  True
  Independent Step  2  minipack3 online update  DUT  smb  True
  Independent Step  3  minipack3 online update  DUT  mcb  True
  Step  4  power reset chassis  DUT

update oob switch firmware
  oob firmware update  DUT  True

verify i2scan
  verify i2c buses  DUT  ${i2c_buses}
  verify i2cScan unidiag system test  DUT


ping bmc ipv6 address
  get ipv6 address  DUT  ${OPENBMC_MODE}

set and get fan speed
  [Arguments]   ${speed}
  FOR    ${INDEX}    IN RANGE    1    ${MaxFanNum}+1
        Log    Loop value is ${INDEX}
        Independent Step  1  set fan speed  DUT  ${INDEX}  ${speed}
        sleep  10s
        Independent Step  2  get fan speed  DUT  ${INDEX}  ${speed}
        sleep  1s
        Independent Step  3  verify fan speed  DUT  ${INDEX}  ${speed}
  END

print gpio controllers and lines
  Step  1  verify gpio controllers  DUT  ${gpio_chip}
  Step  2  verify gpio lines  DUT  ${gpio_lines}

set and get gpio lines
  Step  1  get gpio line  DUT  ${gpio_line_number}  0
  Step  2  set gpio line  DUT  ${gpio_line_number}  1
  Step  3  verify gpio line status  DUT  ${gpio_line_number}  output
  Step  4  get gpio line  DUT  ${gpio_line_number}  1
  Step  5  set gpio line  DUT  ${gpio_line_number}  0
  #below step is workaround, need to check
  Step  6  get gpio line  DUT  ${gpio_line_number}  0
  Step  7  verify gpio line status  DUT  ${gpio_line_number}  input

unload and reload gpio driver
  Step  1  unload gpio driver  DUT
  Step  2  load gpio driver  DUT

store eeprom
  [Arguments]   ${eeprom_type}
  store eeprom content  DUT  ${eeprom_type}_EEPROM  ${eeprom_path}  ${eeprom_type}_eeprom_backup.cfg

restore eeprom
  [Arguments]   ${eeprom_type}
  write eeprom  DUT  ${eeprom_type}_EEPROM  ${eeprom_path}  ${eeprom_type}_eeprom_backup.cfg

write eeprom data
  [Arguments]   ${eeprom_type}  ${eeprom_modified}
  generate eeprom cfg  DUT  ${eeprom_path}  ${eeprom_modified}  modified_eeprom.cfg
  write eeprom  DUT  ${eeprom_type}_EEPROM  ${eeprom_path}  modified_eeprom.cfg

verify eeprom content
  [Arguments]   ${eeprom_type}  ${eeprom_modified}
  IF  '${eeprom_modified}' == '${eeprom_path}'
     verify eeprom  DUT  ${eeprom_type}_EEPROM  ${eeprom_path}
  ELSE 
     verify eeprom  DUT  ${eeprom_type}_EEPROM  ${eeprom_path}  ${eeprom_modified}
  END

copy weutil files and make eeprom ready
  copy weutil files  DUT
  IF  '${fb_variant}' == 'minipack3'
     disable write protect  DUT  FCB_EEPROM
     store eeprom content  DUT  SCM_EEPROM  ${eeprom_path}  SCM_eeprom_backup.cfg
     store eeprom content  DUT  SMB_EEPROM  ${eeprom_path}  SMB_eeprom_backup.cfg
     store eeprom content  DUT  MCB_EEPROM  ${eeprom_path}  MCB_eeprom_backup.cfg
     store eeprom content  DUT  FCB_EEPROM  ${eeprom_path}  FCB_eeprom_backup.cfg
  ELSE IF  '${fb_variant}' == 'minerva'
     disable write protect  DUT  COME_EEPROM
     store eeprom content  DUT  COME_EEPROM  ${eeprom_path}  COME_eeprom_backup.cfg
     store eeprom content  DUT  SMB_EEPROM  ${eeprom_path}  SMB_eeprom_backup.cfg
  END

restore eeprom data and state
  IF  '${fb_variant}' == 'minipack3'
     write eeprom  DUT  SCM_EEPROM  ${eeprom_path}  SCM_eeprom_backup.cfg
     write eeprom  DUT  SMB_EEPROM  ${eeprom_path}  SMB_eeprom_backup.cfg
     write eeprom  DUT  MCB_EEPROM  ${eeprom_path}  MCB_eeprom_backup.cfg
     write eeprom  DUT  FCB_EEPROM  ${eeprom_path}  FCB_eeprom_backup.cfg
     enable write protect  DUT  FCB_EEPROM
  ELSE IF  '${fb_variant}' == 'minerva'
     write eeprom  DUT  COME_EEPROM  ${eeprom_path}  COME_eeprom_backup.cfg
     write eeprom  DUT  SMB_EEPROM  ${eeprom_path}  SMB_eeprom_backup.cfg
     enable write protect  DUT  COME_EEPROM
  END

####Below keywords are for Minvera#####################
download smb cpld images
  download images  DUT  SMB1
  download images  DUT  SMB2

clean smb cpld images
  clean images  DUT  SMB1
  clean images  DUT  SMB2

verify smb cpld version
  [Arguments]   ${fw_type}  ${expected_version1}  ${expected_version2}
  verify firmware version  DUT  smb1  ${expected_version1}
  verify firmware version  DUT  smb2  ${expected_version2}

downgrade smb cpld
  [Arguments]   ${fw_type}
  Step  1  minerva online update  DUT  smb1  False
  Step  2  minerva online update  DUT  smb2  False
  Step  3  power reset chassis  DUT

upgrade smb cpld
  [Arguments]   ${fw_type}
  Step  1  minerva online update  DUT  smb1  True
  Step  2  minerva online update  DUT  smb2  True
  Step  3  power reset chassis  DUT

downgrade pwr cpld
  [Arguments]   ${fw_type}
  Step  1  minerva online update  DUT  pwr  False
  Step  2  power reset chassis  DUT

upgrade pwr cpld
  [Arguments]   ${fw_type}
  Step  1  minerva online update  DUT  pwr  True
  Step  2  power reset chassis  DUT


power cycle by pwr cpld
  power reset chassis  DUT  True
