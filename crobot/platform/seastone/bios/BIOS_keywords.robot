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
# Script       : BIOS_keywords.robot                                                                                  #
# Date         : July 29, 2020                                                                                        #
# Author       : James Shi <jameshi@celestica.com>                                                                    #
# Description  : This script used as keywords in bios.robot                                                           #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for BIOS testing                                                                                    #
#######################################################################################################################

*** Settings ***
Variables         BIOS_variable.py

#Library           whitebox_lib.py
#Library           openbmc_lib.py
#Library           common_lib.py
Library           bios_menu_lib.py
Library           CommonLib.py
Library           OperatingSystem
#Library           ../WhiteboxLibAdapter.py
#Library           ../ses/ses_lib.py
#Library           ../bmc/bmc_lib.py
Library           bios_lib.py

Resource          BIOS_keywords.robot
Resource          CommonResource.robot
#Resource          BMC_keywords.robot

*** Keywords ***
Enter bios now
  enter_into_bios_setup_now  DUT  


check random test
   random_test  DUT

Enter bios as user
  enter_into_bios_setup  DUT  ${user_pass}


leave bios
   exit bios menu  DUT

boot sonic via bios
    check sonic boot via bios  DUT

check the cpu microcode
   ${microcode_cmd_ouput}=   getting_cpu_microcode  DUT
   ${microcode_rev_cmd}=  Convert To Hex   ${microcode_cmd_ouput}  base=16
   enter_into_bios_setup_now  DUT
   ${microcode_bios_output}=   get_microcode_revision_from_bios  DUT
   exit_bios_now  DUT
   ${microcode_rev_bios}=  Convert To Hex  ${microcode_bios_output}   base=16
   Should Be Equal  ${microcode_rev_cmd}   ${microcode_rev_bios}

check memory frequency
   enter_into_bios_setup_now  DUT
   change_the_frequency  DUT  1600
   save_and_exit_bios_now  DUT
   checking memory frequency  DUT  1600
   enter_into_bios_setup_now  DUT
   change_the_frequency  DUT  2400
   save_and_exit_bios_now  DUT
   checking memory frequency  DUT  2400
   
   

boot onie test
   enter_into_bios_setup_now  DUT
   set_boot_onie  DUT
   save_and_exit_onie_boot_now  DUT
   set_default_boot_setup_from_onie_and_uefi  DUT
   

main menu test
   enter_into_bios_setup_now  DUT
   ${date_and_time}=  check_main_menu  DUT
   save_and_exit_bios_now  DUT 
   enter_into_bios_setup_now  DUT
   ${updated_date_and_time}=  check_changed_date_and_time  DUT  ${date_and_time}  true
   save_and_exit_bios_now  DUT
   enter_into_bios_setup_now  DUT
   check_changed_date_and_time  DUT  ${updated_date_and_time}  false
   save_and_exit_bios_now  DUT

boot UEFI OS test
   enter_into_bios_setup_now  DUT
   set_boot_uefi  DUT
   boot_uefi_test  DUT
   
   

boot UEFI shell check
   enter_into_bios_setup_now  DUT
   set_boot_uefi  DUT
   boot_uefi_shell_test  DUT
   
   
   



administrator password test
   enter_into_bios_setup_now  DUT
   change_bios_password  DUT  default  1234  admin
   save_and_exit_bios_now  DUT 
   enter_into_bios_setup_now  DUT
   login_to_device  DUT  1234
   change_bios_password  DUT  1234  default  admin
   save_and_exit_bios_now  DUT 
   
user password test
   enter_into_bios_setup_now  DUT
   change_bios_password  DUT  default  1234  user
   save_and_exit_bios_now  DUT 
   enter_into_bios_setup_now  DUT
   login_to_device  DUT  1234
   change_bios_password  DUT  1234  default  user
   save_and_exit_bios_now  DUT


bios information check
   enter_into_bios_setup_now  DUT
   ${bios_setup_output}=  check_bios_information_from_bios_setup  DUT
   exit_bios_now  DUT
   ${bios_post_output}=  checking_bios_information_from_post_log  DUT
   Should Be Equal  ${bios_setup_output}  ${bios_post_output}
   checking_bios_information_from_dmidecode  DUT  ${bios_setup_output}
   


save and exit check
   enter_into_bios_setup_now  DUT
   save_and_exit_menu  DUT

accesslevel test
   enter_into_bios_setup_now  DUT
   change_bios_password  DUT  default  1234  admin
   change password  DUT  default  4321  user
   save_and_exit_bios_now  DUT
   enter_into_bios_setup_now  DUT
   login_to_device  DUT  4321
   check_accesslevel  DUT  User
   change_bios_password  DUT  4321  default  user
   save_and_exit_bios_now  DUT
   enter_into_bios_setup_now  DUT
   login_to_device  DUT  1234
   check_accesslevel  DUT  Administrator
   change_bios_password  DUT  1234  default  admin
   save_and_exit_bios_now  DUT	

ipmi_bmc_test
   enter_into_bios_setup_now  DUT
   ${setup_bmc_info}=  read_bmc_information_from_setup  DUT
   exit_bios_now  DUT
   ${os_bmc_info}=  read_bmc_information_from_os  DUT
   Should Be Equal  ${setup_bmc_info}   ${os_bmc_info}
   update_bmc_firmware  DUT
   enter_into_bios_setup_now  DUT
   ${setup_bmc_info}=  read_bmc_information_from_setup  DUT
   exit_bios_now  DUT
   ${os_bmc_info}=  read_bmc_information_from_os  DUT
   Should Be Equal  ${setup_bmc_info}   ${os_bmc_info}
   

management_port_information_check
   enter_into_bios_setup_now  DUT
   check_for_management_information_in_setup  DUT
   set_boot_uefi  DUT
   check_management_port_information  DUT

boot_menu_check
   enter_into_bios_setup_now  DUT
   boot_menu_onl  DUT
   enter_into_bios_setup_now  DUT
   boot_menu_onie  DUT
   set_default_boot_setup_from_onie_and_uefi  DUT
   
   

uefi_pxe_functional_test
   enter_into_bios_setup_now  DUT
   set_ipv4_pxe_support_status_bios  DUT
   save_and_exit_bios_now  DUT
   enter_into_bios_setup_now  DUT
   set_boot_pxe  DUT
   check_exit_from_pxe  DUT
   enter_into_bios_setup_from_pxe  DUT
   set_ipv4_pxe_support_status_bios  DUT  disabled
   save_and_exit_bios_now  DUT

non_bios_boot_messages_test
   enter_into_bios_setup_now  DUT
   set_ipv4_pxe_support_status_bios  DUT
   save_and_exit_bios_now  DUT
   enter_into_bios_setup_now  DUT
   set_boot_pxe  DUT
   check_non_bios_messages  DUT
   enter_into_bios_setup_from_pxe  DUT
   set_ipv4_pxe_support_status_bios  DUT  disabled
   save_and_exit_bios_now  DUT

memtest86_test_check
   memtest86_usg_image_to_executable  DUT
   enter_into_bios_setup_now  DUT
   set_usb_partition_1  DUT
   check_memtest86  DUT
   set_default_boot_order  DUT
   enter_into_bios_setup_now  DUT
   set_default_boot_setup_from_onie_and_uefi  DUT
   clean_up_memtest86  DUT


online_programming_under_uefi_shell_check
   online_programming_under_uefi_shell_onl  DUT
   enter_into_bios_setup_now  DUT
   set_boot_uefi  DUT
   online_programming_under_uefi_shell  DUT
   
   

power_reset_cause_test
   ${ip}=  get_ip_address_from_ipmitool_device  DUT
   check_power_reset_cause  DUT  ${ip}
  

access bios via shell
   enter bios with shell

AC power device
   Step  1  EDK2CommonLib.Powercycle Device   DUT   no


chuck it
   Step  1  exit bios shelll  DUT
   Step  2  exit the shell


Power me up
   Step  1   EDK2CommonLib.Powercycle Device   DUT   yes

exit the shell
    EDK2CommonLib.exit the shell

downgrade primary bios image through lan
    update_bios_image  DUT  ${old_bios_image}  0  lanplus=True
    bios_boot  DUT  0
    verify_the_bios_version  DUT  ${old_bios_image}

upgrade primary bios image through lan
    update_bios_image  DUT  ${new_bios_image}  0  lanplus=True
    bios_boot  DUT  0
    verify_the_bios_version  DUT  ${new_bios_image}

downgrade backup bios image through lan
    bios_boot  DUT  1
    update_bios_image  DUT  ${old_bios_image}  0  lanplus=True
    bios_boot  DUT  1
    verify_the_bios_version  DUT  ${old_bios_image}

upgrade backup bios image through lan
    bios_boot  DUT  1
    update_bios_image  DUT  ${new_bios_image}  0  lanplus=True
    bios_boot  DUT  1
    verify_the_bios_version  DUT  ${new_bios_image}

downgrade primary bios image through usb
    mount_disk_on_device  DUT
    update_bios_image_through_usb  DUT  ${old_bios_image}  0
    bios_boot  DUT  0
    verify_the_bios_version  DUT  ${old_bios_image}
    umount_disk_from_device  DUT

upgrade primary bios image through usb
    mount_disk_on_device  DUT
    update_bios_image_through_usb  DUT  ${new_bios_image}  0
    bios_boot  DUT  0
    verify_the_bios_version  DUT  ${new_bios_image}
    umount_disk_from_device  DUT

downgrade backup bios image through usb
    mount_disk_on_device  DUT
    bios_boot  DUT  1
    update_bios_image_through_usb  DUT  ${old_bios_image}  1
    bios_boot  DUT  1
    verify_the_bios_version  DUT  ${old_bios_image}
    umount_disk_from_device  DUT

upgrade backup bios image through usb
    mount_disk_on_device  DUT
    bios_boot  DUT  1
    update_bios_image_through_usb  DUT  ${new_bios_image}  1
    bios_boot  DUT  1
    verify_the_bios_version  DUT  ${new_bios_image}
    umount_disk_from_device  DUT
downgrade primary bios image through afulnx
    download_files_in_device  DUT
    update_bios_through_afulnx  DUT  ${old_bios_image}
    bios_boot  DUT  0
    verify_the_bios_version  DUT  ${old_bios_image}


upgrade primary bios image through afulnx
    download_files_in_device  DUT
    update_bios_through_afulnx  DUT  ${new_bios_image}
    bios_boot  DUT  0
    verify_the_bios_version  DUT  ${new_bios_image}

End CPU LPC Interface Test
    Step  1  write baseboard cpld register  0xa101  0xde
    Step  2  read baseboard cpld register  DUT  0xa101  de
    Step  3  write baseboard cpld register  0xa1e1  0xde
    Step  4  read baseboard cpld register  DUT  0xa1e1  de


check bmc and sel setup
   Step  1  enter into bios setup now  DUT
   Step  2  check bmc enable  DUT
   Step  3  check sel setup  DUT  1  True
   Step  4  exit bios now  DUT

check and clear sel os
   Step  1  check sel os  DUT
   Step  2  clear sel os  DUT

check sel clear setup
   Step  1  enter into bios setup now  DUT
   Step  2  check sel setup  DUT  2
   Step  3  exit bios now  DUT

check sel update setup
   Step  1  enter into bios setup now  DUT
   Step  2  check sel setup  DUT  3
   Step  3  exit bios now  DUT

validate static ip config
   Step  1  enter into bios setup now  DUT
   Step  2  configure network setup  DUT  1
   Step  3  check network setup  DUT  1  soft
   Step  4  exit bios now  DUT
   Step  5  check network os  DUT  1
   Step  6  enter into bios setup now  DUT
   Step  7  check network setup  DUT  1  hard
   Step  8  exit bios now  DUT
   Step  8  configure network os  DUT  1
   Step  9  enter into bios setup now  DUT
   Step  10  check network setup  DUT  1  soft

validate dhcp ip config
   Step  1  configure network setup  DUT  2
   Step  2  check network setup  DUT  2  soft
   Step  3  exit bios now  DUT
   Step  3  check network os  DUT  2
   Step  4  enter into bios setup now  DUT
   Step  5  check network setup  DUT  2  soft
   Step  6  exit bios now  DUT

config fastboot image
   Step  1  import from remote  DUT  5
   Step  2  import from remote  DUT  8
   Step  3  import from remote  DUT  7
   Step  4  set bios version  DUT  1
   Step  5  enter into bios setup now  DUT
   Step  6  set boot one  DUT  Shell

validate fastboot image
   Step  1  run amiprd tool  DUT  1
   Step  2  configure fastboot setup  DUT  1
   Step  3  run amiprd tool  DUT  2  True
   #Step  4  configure fastboot setup  DUT  2
   #Step  5  run amiprd tool  DUT  1  True

cleanup fastboot image
   #Step  1  exit shell to onl  DUT
   Step  2  enter into bios setup now  DUT
   Step  3  set boot one  DUT  ONL
   Step  4  import from remote  DUT  6
   Step  5  set bios version  DUT  2