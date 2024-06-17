###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

*** Settings ***
Documentation   Alibaba common diagnostic suite
Resource        CommonKeywords.resource
Resource        AliCommonKeywords.resource
Resource        AliDiagKeywords.resource

Library         AliCommonLib.py
Library         AliDiagLib.py
Library         String

Suite Setup     Detect hardware loopback module

*** Test Cases ***

# sonic already packed the latest diag
#ALI_DIAG_TC001_UPGRADE_AND_INSTALL_DIAG_TOOL_VIA_SONIC
#    [Tags]  ALI_DIAG_TC001_UPGRADE_AND_INSTALL_DIAG_TOOL_VIA_SONIC
#    ...  migaloo
#    ...  shamu
#
#    [Setup]  Run Keywords
#    ...  open prompt and login to root user  console=${diagos_mode}  AND
#    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
#    ...  Sleep  45s  # Wait for some terrible I2C bus add messages
#
#    Log  >>Manual Install DIAG Tools on SONiC<<
#    Step   1  open prompt and login to root user  console=${diagos_mode}
#    Step   2  renew IP using DHCP  console=${diagos_mode}  interface=${dhcp_interface}
#    Step   3  ping to IP  console=${diagos_mode}  ip=${tftp_server_ipv4}
#    ...  msg=Not found the TFTP server!${\n}Can not download the diag package to install!
#    Step   4  secure copy file
#    ...  console=${diagos_mode}
#    ...  username=${scp_username}
#    ...  password=${scp_password}
#    ...  source_ip=${ssh_server_ipv4}
#    ...  source_path=${diag_deb_path}
#    ...  source_file=${diag_deb_new_package}
#    ...  destination=${diag_deb_save_to}
#    Step   5  Run Keyword And Ignore Error
#    ...  show software version
#    ...  console=${diagos_mode}
#    ...  path=${diagos_cpu_diag_path}
#    Step   6  remove file/folder  console=${diagos_mode}  file=/usr/local/migaloo
#    Step   7  install diagtool debian package
#    Step   8  show software version
#    ...  console=${openbmc_mode}
#    ...  command=${openbmc_show_diag_version_command}
#    ...  path=${openbmc_diag_bin_path}

    #
    # This part of the code is does not work and can not run it,
    # due to, the rest of the test-cases is going to fail.
    #

    # Log  >>SONiC Automatic Install DIAG Tools<<
    # Step   9  remove file/folder  console=${diagos_mode}  file=/usr/local/migaloo/
    # Step  10  remove file/folder  console=${openbmc_mode}  file=/var/log/BMC_Diag/
    # Step  11  power cycle to mode  mode=${diagos_mode}
    # Step  12  Sleep  8min  # Just wait then it is going to install by automatic (typically 5min)
    # Step  13  Wait for OpenBMC Info
    # Step  14  verify installed DIAG package
    # ...  console=${diagos_mode}
    # ...  command=${diagos_show_diag_version_command}
    # ...  path=${diagos_cpu_diag_path}
    # ...  patterns=${diagos_version_show_patterns}
    # ...  version=${diag_new_version}
    # Step  15  show software version
    # ...  console=${openbmc_mode}
    # ...  command=${openbmc_show_diag_version_command}
    # ...  path=${openbmc_diag_bin_path}


ALI_DIAG_TC003_ONLINE_UPDATE_BMC_IN_COME
    [Tags]  ALI_DIAG_TC003_ONLINE_UPDATE_BMC_IN_COME
    ...  migaloo  long_time

    [Setup]  Run Keywords
    ...  power cycle to mode  mode=${diagos_mode}  AND  # OpenBMC always boot from master
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3

    Log  >>Show the current boot source and OpenBMC version<<  console=${TRUE}
    Step   1  find current boot source
    Step   2  Wait for OpenBMC Info
    Step   3  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=${diagos_show_diag_version_command}
    ...  patterns=${diagos_version_show_patterns}
    ...  msg=Failed to verify -S/show option!
    ...  sec=${5 * 60}

    Log  >>Downgrade SLAVE OpenBMC<<  console=${TRUE}
    Step   4  Update OpenBMC on COMe
    ...  where_to_download=${bmc_path}
    ...  image_name=${bmc_old_image}
    ...  save_to=${bmc_save_to}
    ...  image_version=${bmc_old_version}
    ...  switch_pattern=Slave Flash
    ...  boot_from=slave
    ...  flash_cs=1

    Log  >>Upgrade SLAVE OpenBMC<<  console=${TRUE}
    Step   5  Update OpenBMC on COMe
    ...  where_to_download=${bmc_path}
    ...  image_name=${bmc_new_image}
    ...  save_to=${bmc_save_to}
    ...  image_version=${bmc_new_version}
    ...  switch_pattern=Slave Flash
    ...  boot_from=slave
    ...  flash_cs=1

    Log  >>Downgrade MASTER OpenBMC<<  console=${TRUE}
    Step   6  Update OpenBMC on COMe
    ...  where_to_download=${bmc_path}
    ...  image_name=${bmc_old_image}
    ...  save_to=${bmc_save_to}
    ...  image_version=${bmc_old_version}
    ...  switch_pattern=Master Flash
    ...  boot_from=master
    ...  flash_cs=0

    Log  >>Upgrade MASTER OpenBMC<<  console=${TRUE}
    Step   7  Update OpenBMC on COMe
    ...  where_to_download=${bmc_path}
    ...  image_name=${bmc_new_image}
    ...  save_to=${bmc_save_to}
    ...  image_version=${bmc_new_version}
    ...  switch_pattern=Master Flash
    ...  boot_from=master
    ...  flash_cs=0


####  Remove ALI_DIAG_TC004_ONLINE_UPDATE_BIOS_IN_BMC_OS, covered by ALI_BMC_COMM_TC_005_ONLINE_UPDATE_BIOS_IN_BMC_OS
   # [Tags]  ALI_DIAG_TC004_ONLINE_UPDATE_BIOS_IN_BMC_OS
   # ...  migaloo
   # ...  SHAMU_DIAG_TC047_BIOS_UPDATE
   # ...  shamu


ALI_DIAG_TC005_ONLINE_UPDATE_FPGA_IN_SONIC
    [Tags]  ALI_DIAG_TC005_ONLINE_UPDATE_FPGA_IN_SONIC
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Log  >>Downgrade FPGA on SONiC console<<  console=${TRUE}
    Step   1  force to switch boot source
    ...  switch_to_pattern=Master Flash
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && boot_from master)
    open prompt and login to root user  console=${openbmc_mode}
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    Sleep  45s  # Wait for some terrible I2C bus add messages
    Step   2  show software version
    Step   3  DiagOS renew IP using DHCP and set variable
    Step   4  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${diagos_fpga_path}
    ...  source_file=${diagos_fpga_old_image}
    ...  destination=${diagos_fpga_save_to}
    ...  sec=${6 * 60}
    ...  always_copy=${TRUE}
    Step   5  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=fpga_prog ${diagos_fpga_save_to}/${diagos_fpga_old_image}
    ...  sec=${3 * 60}
    Step   6  OpenBMC wedge power script
    Step   7  show software version
    Step   8  search for a pattern
    ...  text=${text}
    ...  pattern=(?mi)^[ \\\\t]*FPGA Version[ \\\\t]+:[ \\\\t]*(?P<fpga>${diagos_fpga_old_version})
    ...  msg=The FPGA version does not downgrade!

    [Teardown]  Run Keywords
    ...  Log  >>Upgrade FPGA on SONiC console<<  console=${TRUE}  AND
    ...  force to switch boot source
    ...  switch_to_pattern=Master Flash
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && boot_from master)  AND
    ...  open prompt and login to root user  console=${openbmc_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3  AND
    ...  Sleep  45s  AND  # Wait for some terrible I2C bus add messages
    ...  show software version  AND
    ...  DiagOS renew IP using DHCP and set variable  AND
    ...  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${diagos_fpga_path}
    ...  source_file=${diagos_fpga_new_image}
    ...  destination=${diagos_fpga_save_to}
    ...  sec=${6 * 60}
    ...  always_copy=${TRUE}  AND
    ...  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=fpga_prog ${diagos_fpga_save_to}/${diagos_fpga_new_image}
    ...  sec=${3 * 60}  AND
    ...  OpenBMC wedge power script  AND
    ...  show software version  AND
    ...  search for a pattern
    ...  text=${text}
    ...  pattern=(?mi)^[ \\\\t]*FPGA Version[ \\\\t]+:[ \\\\t]*(?P<fpga>${diagos_fpga_new_version})
    ...  msg=The FPGA version does not upgrade!


ALI_DIAG_TC006_ONLINE_UPDATE_FPGA_IN_BMC
    [Tags]  ALI_DIAG_TC006_ONLINE_UPDATE_FPGA_IN_BMC
    ...  migaloo
    ...  SHAMU_DIAG_TC046_UPDATE_FPGA_IMAGE
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Log  >>Downgrade FPGA on BMC console<<  console=${TRUE}
    Step   1  show software version
    ...  command=${diagos_show_fpga_version_command}
    Step   2  OpenBMC renew IP using DHCP and set variable
    Step   3  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${fpga_multboot_path}
    ...  source_file=${fpga_multboot_old_image}
    ...  destination=${fpga_multboot_save_to}
    ...  sec=${6 * 60}
    ...  always_copy=${TRUE}
    Step   4  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=(source /usr/local/bin/openbmc-utils.sh && spi_upgrade FPGA -w ${fpga_multboot_save_to}/${fpga_multboot_old_image})
    ...  sec=${3 * 60}
    Step   5  OpenBMC wedge power script
    Step   6  show software version
    ...  command=${diagos_show_fpga_version_command}
    Step   7  search for a pattern
    ...  text=${text}
    ...  pattern=(?mi)^[ \\\\t]*FPGA Version[ \\\\t]*:[ \\\\t]*(?P<fpga>${fpga_multboot_old_version})
    ...  msg=The FPGA version does not downgrade!

    [Teardown]  Run Keywords
    ...  Log  >>Upgrade FPGA on BMC console<<  console=${TRUE}  AND
    ...  show software version
    ...  command=${diagos_show_fpga_version_command}  AND
    ...  OpenBMC renew IP using DHCP and set variable  AND
    ...  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${fpga_multboot_path}
    ...  source_file=${fpga_multboot_new_image}
    ...  destination=${fpga_multboot_save_to}
    ...  sec=${6 * 60}
    ...  always_copy=${TRUE}  AND
    ...  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=(source /usr/local/bin/openbmc-utils.sh && spi_upgrade FPGA -w ${fpga_multboot_save_to}/${fpga_multboot_new_image})
    ...  sec=${3 * 60}  AND
    ...  OpenBMC wedge power script  AND
    ...  show software version
    ...  command=${diagos_show_fpga_version_command}  AND
    ...  search for a pattern
    ...  text=${text}
    ...  pattern=(?mi)^[ \\t]*FPGA Version[ \\t]*:[ \\t]*(?P<fpga>${fpga_multboot_new_version})
    ...  msg=The FPGA version does not upgrade!

ALI_DIAG_TC007_CPLD_UPDATE_VIA_COME
    [Tags]  ALI_DIAG_TC007_CPLD_UPDATE_VIA_COME
    ...  migaloo

    # Downgrade
    Step   1  DiagOS renew IP using DHCP and set variable
    Step   2  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${base_cpld_path}    ## The CPLDs all in same path.
    ...  source_file=*    ## Copy all CPLDs to DUT.
    ...  destination=/home/STRESS
    ...  sec=${15 * 60}

    # FAN CPLD
    Step   3  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 2 ${fan_cpld_old_image}
    ...  console=${diagos_mode}
    ...  sec=${3 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # SWITCH CPLD
    Step   5  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 3 ${switch_cpld_old_image}
    ...  console=${diagos_mode}
    ...  sec=${5 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # TOP CPLD
    Step   6  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 4 ${switch_cpld_old_image}
    ...  console=${diagos_mode}
    ...  sec=${5 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!
    # BOTTOM CPLD
    Step   7  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 5 ${switch_cpld_old_image}
    ...  console=${diagos_mode}
    ...  sec=${5 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # BASE CPLD
    Step  9  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 0 ${base_cpld_old_image}
    ...  console=${diagos_mode}
    ...  sec=${5 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # COMe CPLD
    Step  11  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 1 ${come_cpld_old_image}
    ...  console=${diagos_mode}
    ...  sec=${5 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # BASE CPLD Refresh (reboot)
    Step  13  send a line
    ...  command=ispvm -i 0 /home/STRESS/${base_cpld_refresh_new_image}
    Step  14  read until pattern  pattern= login:  sec=${20 * 60}

    # FAN CPLD Refresh
    Step  15  DiagOS renew IP using DHCP and set variable
    Step  17  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 2 ${fan_cpld_refresh_new_image}
    ...  console=${diagos_mode}
    ...  sec=${20 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!
    Step  18  verify software version
    Step  19  search for ordered pattern list
    ...  text=${text}
    ...  patterns=${old_cpld_version_patterns}
    ...  msg=The CPLD version does not match!

    #
    # Upgrade
    #
    # FAN CPLD
    Step   20  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 2 ${fan_cpld_new_image}
    ...  console=${diagos_mode}
    ...  sec=${3 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # SWITCH CPLD
    Step   21  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 3 ${switch_cpld_new_image}
    ...  console=${diagos_mode}
    ...  sec=${5 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # TOP CPLD
    Step   22  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 4 ${switch_cpld_new_image}
    ...  console=${diagos_mode}
    ...  sec=${5 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!
    # BOTTOM CPLD
    Step   23  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 5 ${switch_cpld_new_image}
    ...  console=${diagos_mode}
    ...  sec=${5 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # BASE CPLD
    Step  24  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 0 ${base_cpld_new_image}
    ...  console=${diagos_mode}
    ...  sec=${5 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # COMe CPLD
    Step  25  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 1 ${come_cpld_new_image}
    ...  console=${diagos_mode}
    ...  sec=${5 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # BASE CPLD Refresh (reboot)
    Step  26  send a line
    ...  command=ispvm -i 0 /home/STRESS/${base_cpld_refresh_new_image}
    Step  27  read until pattern  pattern= login:  sec=${20 * 60}

    # FAN CPLD Refresh
    Step  28  DiagOS renew IP using DHCP and set variable
    Step  29  execute command and verify with a pattern
    ...  path=/home/STRESS
    ...  command=ispvm -i 2 ${fan_cpld_refresh_new_image}
    ...  console=${diagos_mode}
    ...  sec=${20 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!
    Step  30  verify software version
    Step  31  search for ordered pattern list
    ...  text=${text}
    ...  patterns=${new_cpld_version_patterns}
    ...  msg=The CPLD version does not match!

    # In case fail to reboot (refresh), It does not boot up at all
    [Teardown]  Run Keyword If Test Failed  power cycle to mode  mode=${diagos_mode}

ALI_DIAG_TC008_CPLD_UPDATE_VIA_BMC
    [Tags]  ALI_DIAG_TC008_CPLD_UPDATE_VIA_BMC
    ...  migaloo  long_time

    Step   1  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=source /usr/local/bin/openbmc-utils.sh

    #
    # Downgrade
    #
    # FAN CPLD
    Step   2  OpenBMC renew IP using DHCP and set variable
    Step   3  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${base_cpld_path}    ## The CPLDs all in same path.
    ...  source_file=*
    ...  destination=/var/log/cpld
    ...  sec=${6 * 60}
    ...  always_copy=${TRUE}

    Step   4  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld FAN_CPLD ${fan_cpld_old_image}
    ...  console=${openbmc_mode}
    ...  sec=${10 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # SWITCH CPLD
    Step   5  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld SW_CPLD1 ${switch_cpld_old_image}
    ...  console=${openbmc_mode}
    ...  sec=${20 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # TOP CPLD
    Step   6  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command= program_cpld TOP_LC_CPLD ${switch_cpld_old_image}
    ...  console=${openbmc_mode}
    ...  sec=${20 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!
    # BOTTOM CPLD
    Step  7  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld BOT_LC_CPLD ${switch_cpld_old_image}
    ...  console=${openbmc_mode}
    ...  sec=${20 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # BASE CPLD
    Step  8  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld BASE_CPLD ${base_cpld_old_image}
    ...  console=${openbmc_mode}
    ...  sec=${20 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # COMe CPLD
    Step  9  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld CPU_CPLD ${come_cpld_old_image}
    ...  console=${openbmc_mode}
    ...  sec=${10 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # BASE CPLD Refresh (reboot)
    Step  10  send a line
    ...  command=program_cpld BASE_CPLD /var/log/cpld/${base_cpld_refresh_new_image}
    Step  11  read until pattern  pattern= login:  sec=${20 * 60}
    Step  12  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=source /usr/local/bin/openbmc-utils.sh

    # FAN CPLD
    Step  13  execute command and verify with a pattern
    ...  path=/var/log/cpld/
    ...  command=program_cpld FAN_CPLD ${fan_cpld_refresh_new_image}
    ...  console=${openbmc_mode}
    ...  sec=${10 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!
    Step  14  verify software version
    Step  15  search for ordered pattern list
    ...  text=${text}
    ...  patterns=${old_cpld_version_patterns}
    ...  msg=The CPLD version does not match!

    #
    # Upgrade
    #
    # FAN CPLD
    Step  16  OpenBMC renew IP using DHCP and set variable
    Step  17  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld FAN_CPLD ${fan_cpld_new_image}
    ...  console=${openbmc_mode}
    ...  sec=${10 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # SWITCH CPLD
    Step  18  OpenBMC renew IP using DHCP and set variable
    Step  19  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld SW_CPLD1 ${switch_cpld_new_image}
    ...  console=${openbmc_mode}
    ...  sec=${20 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # TOP CPLD
    Step  20  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command= program_cpld TOP_LC_CPLD ${switch_cpld_new_image}
    ...  console=${openbmc_mode}
    ...  sec=${20 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!
    # BOTTOM CPLD
    Step  21  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld BOT_LC_CPLD ${switch_cpld_new_image}
    ...  console=${openbmc_mode}
    ...  sec=${20 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # BASE CPLD
    Step  22  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld BASE_CPLD ${base_cpld_new_image}
    ...  console=${openbmc_mode}
    ...  sec=${20 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # COMe CPLD
    Step  23  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld CPU_CPLD ${come_cpld_new_image}
    ...  console=${openbmc_mode}
    ...  sec=${10 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!

    # BASE CPLD Refresh (reboot)
    Step  24  send a line
    ...  command=program_cpld BASE_CPLD /var/log/cpld/${base_cpld_refresh_new_image}
    Step  25  read until pattern  pattern= login:  sec=${20 * 60}
    Step  26  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=source /usr/local/bin/openbmc-utils.sh

    # FAN CPLD
    Step  27  OpenBMC renew IP using DHCP and set variable
    Step  28  execute command and verify with a pattern
    ...  path=/var/log/cpld
    ...  command=program_cpld FAN_CPLD ${fan_cpld_refresh_new_image}
    ...  console=${openbmc_mode}
    ...  sec=${10 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!
    Step  29  verify software version
    Step  30  search for ordered pattern list
    ...  text=${text}
    ...  patterns=${new_cpld_version_patterns}
    ...  msg=The CPLD version does not match!
    [Teardown]  Run Keyword If Test Failed  power cycle to mode  mode=${diagos_mode}


# ALI_DIAG_TC009_BMC_UPDATE_TH4_PCIE_FIRMWARE_TEST
#     [Tags]  ALI_DIAG_TC009_BMC_UPDATE_TH4_PCIE_FIRMWARE_TEST
#     ...  migaloo

#     # Reboot first to make for what PCIe TH4 firmware load current
#     [Setup]  Run Keywords
#     ...  OpenBMC renew IP using DHCP and set variable  AND
#     ...  secure copy file
#     ...  console=${openbmc_mode}
#     ...  username=${scp_username}
#     ...  password=${scp_password}
#     ...  source_ip=${ssh_server_ipv4}
#     ...  source_path=${openbmc_th4_path}
#     ...  source_file=${openbmc_th4_new_image}
#     ...  destination=${openbmc_th4_save_to}
#     ...  sec=${6 * 60}
#     # ...  always_copy=${TRUE}

#     # Just show for current version
#     Step   1  Execute command on SDK Prompt (sdklt.0>)
#     ...  command=pciephy fwinfo
#     ...  pattern=(?mi)[ \\\\t]*PCIe FW loader version:[ \\\\t]*(?P<pcie_fw_loader_version>.*)$
#     # To make sure the console is not hangup
#     set test variable  ${original_pcie_loader_version}  ${match}
#     Step   2  execute command and verify exit code
#     ...  console=${openbmc_mode}
#     ...  command=source /usr/local/bin/openbmc-utils.sh
#     Step   3  execute command and verify with a pattern
#     ...  console=${openbmc_mode}
#     ...  command=spi_upgrade -h
#     ...  pattern=spi_upgrade
#     ...  is_check_exit_code=${FALSE}  # Do not know why, it is not return zero!
#     Step   4  execute command and verify with a pattern
#     ...  console=${openbmc_mode}
#     ...  command=spi_upgrade TH4 -w ${openbmc_th4_save_to}/${openbmc_th4_new_image}
#     ...  pattern=Erase/write (?P<result>done)
#     ...  msg=Failed not found done pattern!
#     ...  sec=${3 * 60}
#     Step   5  Execute command on SDK Prompt (sdklt.0>)
#     ...  command=pciephy fwinfo
#     ...  pattern=(?mi)[ \\\\t]*PCIe FW loader version:[ \\\\t]*(?P<pcie_fw_loader_version>.*)$
#    To make sure the console is not hangup
#    set test variable  ${loaded_pcie_loader_version}  ${match}
#    Step   6  power cycle to mode  mode=${openbmc_mode}
#    Step   7  Execute command on SDK Prompt (sdklt.0>)
#    ...  command=pciephy fwinfo
#    ...  pattern=(?mi)[ \\\\t]*PCIe FW loader version:[ \\\\t]*(?P<pcie_fw_loader_version>.*)$
#    # To make sure the console is not hangup
#    set test variable  ${reboot_pcie_loader_version}  ${match}
#    Step   8  Should Be Equal As Strings
#    ...  ${loaded_pcie_loader_version}[pcie_fw_loader_version]  ${reboot_pcie_loader_version}[pcie_fw_loader_version]
#    ...  msg=Failed, the PCIe Loader version should be treated equally as before reboot!

#    Restore to the latest version
#    [Teardown]  Run Keywords
#    ...  Execute command on SDK Prompt (sdklt.0>)  command=pciephy fwload ${diagos_th4_pcie_new_image}  pattern=(?mi)[ \\\\t]*PCIE firmware updated (?P<result>successfully)  AND
#    ...  power cycle to mode  mode=${openbmc_mode}


ALI_DIAG_TC010_CPU_UPDATE_TH4_PCIE_FIRMWARE_TEST
    [Tags]  ALI_DIAG_TC010_CPU_UPDATE_TH4_PCIE_FIRMWARE_TEST
    ...  migaloo  long_time

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  AND  # Wait for some terrible I2C bus add messages
    ...  Execute command on SDK Prompt (sdklt.0>)
    ...  command=pciephy fwload ${diagos_th4_pcie_new_image}
    ...  pattern=(?mi)[ \\\\t]*PCIE firmware updated (?P<result>successfully)

    Step   1  Execute command on SDK Prompt (sdklt.0>)
    ...  command=pciephy fwinfo
    ...  pattern=(?mi)[ \\\\t]*PCIe FW loader version:[ \\\\t]*(?P<pcie_fw_loader_version>.*)$
    set test variable  ${original_pcie_loader_version}  ${match}
    Step   2  Execute command on SDK Prompt (sdklt.0>)
    ...  command=pciephy fwload ${diagos_th4_pcie_old_image}
    ...  pattern=(?mi)[ \\\\t]*PCIE firmware updated (?P<result>successfully)
    set test variable  ${pcie_loader_downgrade_result}  ${match}
    Step   3  Execute command on SDK Prompt (sdklt.0>)
    ...  command=pciephy fwinfo
    ...  pattern=(?mi)[ \\\\t]*PCIe FW loader version:[ \\\\t]*(?P<pcie_fw_loader_version>.*)$
    set test variable  ${pcie_loader_downgrade_version}  ${match}
    Step   4  power cycle to mode  mode=${diagos_mode}
    Step   5  open prompt and login to root user  console=${diagos_mode}
    Step   6  Execute command on SDK Prompt (sdklt.0>)
    ...  command=pciephy fwinfo
    ...  pattern=(?mi)[ \\\\t]*PCIe FW loader version:[ \\\\t]*(?P<pcie_fw_loader_version>.*)$
    set test variable  ${pcie_loader_downgrade_reboot_version}  ${match}
    Step   7  Should Be Equal As Strings
    ...  ${pcie_loader_downgrade_version}[pcie_fw_loader_version]  ${pcie_loader_downgrade_reboot_version}[pcie_fw_loader_version]
    ...  msg=Failed, PCIe loader Version used to update does not match after reboot!

    [Teardown]  Run Keywords
    ...  Execute command on SDK Prompt (sdklt.0>)  command=pciephy fwload ${diagos_th4_pcie_new_image}  pattern=(?mi)[ \\\\t]*PCIE firmware updated (?P<result>successfully)  AND
    ...  set test variable  ${teardown_pcie_loader_update_result}  ${match}  AND
    ...  execute command on SDK Prompt (sdklt.0>)  command=pciephy fwinfo  pattern=(?mi)[ \\\\t]*PCIe FW loader version:[ \\\\t]*(?P<pcie_fw_loader_version>.*)$  AND
    ...  set test variable  ${teardown_pcie_loader_update_version}  ${match}  AND
    ...  Should Be Equal As Strings  ${original_pcie_loader_version}[pcie_fw_loader_version]  ${teardown_pcie_loader_update_version}[pcie_fw_loader_version]  msg=Failed to update/restore PCIe loader Version to latest version!  AND
    ...  power cycle to mode  mode=${diagos_mode}


ALI_DIAG_TC011_I210_10GKR_FIRMWARE_UPDATE
    [Tags]  ALI_DIAG_TC011_I210_10GKR_FIRMWARE_UPDATE
    ...  migaloo

    [Setup]  Run Keywords
    # Read & save the original MAC
    ...  power cycle to mode  mode=${diagos_mode}  AND
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  AND  # Wait for some terrible I2C bus add messages
    ...  show network interface IP  console=${diagos_mode}  interface=eth0  pattern=(?m)^ +link\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})  AND
    ...  set test variable  &{eth0_nic5_mac_original}  &{matches}  AND
    ...  show network interface IP  console=${diagos_mode}  interface=eth1  pattern=(?m)^ +link\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})  AND
    ...  set test variable  &{eth1_nic1_mac_original}  &{matches}  AND
    ...  show network interface IP  console=${diagos_mode}  interface=eth2  pattern=(?m)^ +link\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})  AND
    ...  set test variable  &{eth2_nic2_mac_original}  &{matches}

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e
    ...  patterns=${diagos_nic_list_patterns}
    ...  msg=Failed to run "eeupdate64e"!
    ...  is_check_exit_code=${FALSE}

    Log  >>First MAC used to test<<  console=${TRUE}

    # Write it and read it to check
    Step  2   execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=5 /MAC=${diagos_eeupdate64e_mac}[base]
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to write MAC for NIC=5!
    ...  is_check_exit_code=${FALSE}

    # Reboot
    Step  3   reboot UNIX-like OS  console=${diagos_mode}

    Step  4   show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth0
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth0_mac_written}  &{matches}
    Step  5   show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth1
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth1_mac_written}  &{matches}
    Step  6   show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth2
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth2_mac_written}  &{matches}

    # Compare before & after write it
    ${eth0_mac_written_str}=  Replace String
    ...  string=${eth0_mac_written}[mac_1]
    ...  search_for=:
    ...  replace_with=
    Step  7   Should Be Equal As Strings
    ...  first=${diagos_eeupdate64e_mac}[base]
    ...  second=${eth0_mac_written_str}
    ...  msg=Failed, the written MAC/eth0 does not match with read out!
    ...  ignore_case=${TRUE}

    # Reboot by power terminal
    Step  8   power cycle to mode  mode=${diagos_mode}
    Step  9   open prompt and login to root user  console=${diagos_mode}

    # Check the MAC address after reboot
    Step  10  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth0
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth0_mac_cycle}  &{matches}
    Step  11  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth1
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth1_mac_cycle}  &{matches}
    Step  12  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth2
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth2_mac_cycle}  &{matches}

    # Compare after reboot
    ${eth0_mac_cycle_str}=  Replace String
    ...  string=${eth0_mac_cycle}[mac_1]
    ...  search_for=:
    ...  replace_with=
    Step  13  Should Be Equal As Strings
    ...  first=${diagos_eeupdate64e_mac}[base]
    ...  second=${eth0_mac_cycle_str}
    ...  msg=Failed, the written MAC/eth0 does not match with read out!
    ...  ignore_case=${TRUE}

    Log  >>Second MAC used to test<<  console=${TRUE}

    # Write it and read it to check
    Step  14  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=5 /MAC=001122334455
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to write MAC for NIC=5!
    ...  is_check_exit_code=${FALSE}

    # Reboot
    Step  15  reboot UNIX-like OS  console=${diagos_mode}

    Step  16  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth0
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth0_mac_written}  &{matches}
    Step  17  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth1
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth1_mac_written}  &{matches}
    Step  18  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth2
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth2_mac_written}  &{matches}

    # Compare before & after write it
    ${eth0_mac_written_str}=  Replace String
    ...  string=${eth0_mac_written}[mac_1]
    ...  search_for=:
    ...  replace_with=
    Step  19  Should Be Equal As Strings
    ...  first=001122334455
    ...  second=${eth0_mac_written_str}
    ...  msg=Failed, the written MAC/eth0 does not match with read out!
    ...  ignore_case=${TRUE}

    # Reboot by power terminal
    Step  20  power cycle to mode  mode=${diagos_mode}
    Step  21  open prompt and login to root user  console=${diagos_mode}

    # Check the MAC address after reboot
    Step  22  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth0
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth0_mac_cycle}  &{matches}
    Step  23  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth1
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth1_mac_cycle}  &{matches}
    Step  24  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth2
    ...  pattern=(?m)^ +link\\\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  &{eth2_mac_cycle}  &{matches}

    # Compare after reboot
    ${eth0_mac_cycle_str}=  Replace String
    ...  string=${eth0_mac_cycle}[mac_1]
    ...  search_for=:
    ...  replace_with=
    Step  25  Should Be Equal As Strings
    ...  first=001122334455
    ...  second=${eth0_mac_cycle_str}
    ...  msg=Failed, the written MAC/eth0 does not match with read out!
    ...  ignore_case=${TRUE}

    ${eth0_nic5_mac_original_str}=  Replace String
    ...  string=${eth0_nic5_mac_original}[mac_1]
    ...  search_for=:
    ...  replace_with=

    [Teardown]  Run Keywords
    # Restore the original MAC
    ...  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=5 /MAC=${eth0_nic5_mac_original_str}
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to restore original/write MAC for NIC=5!
    ...  is_check_exit_code=${FALSE}  AND
    ...  power cycle to mode  mode=${diagos_mode}  AND
    ...  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth0
    ...  pattern=(?m)^ +link\\/ether (?P<mac>${eth0_nic5_mac_original}[mac_1])
    ...  msg=Failed to restore for the original MAC address on eth0/nic5!


ALI_DIAG_TC012_OOB_SWITCH_FIRMWARE_UPDATE
    [Tags]  ALI_DIAG_TC012_OOB_SWITCH_FIRMWARE_UPDATE
    ...  migaloo

    [Setup]  Run Keywords
    ...  OpenBMC renew IP using DHCP and set variable  AND
    ...  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${diagos_bcm5387_path}
    ...  source_file=${diagos_bcm5387_new_image}
    ...  destination=${diagos_bcm5387_save_to}

    Step  1   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=source /usr/local/bin/openbmc-utils.sh
    ...  msg=Failed to source the shell file!
    Step  2   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=gpio_set F2 1
    ...  msg=Failed to source the shell file!
    Step  3   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=at93cx6_util_py3.py --cs 43 --miso 44 --mosi 45 --clk 46 --mode at93c46 chip write --file ${diagos_bcm5387_save_to}/${diagos_bcm5387_new_image}
    ...  msg=Failed to update OOB Switch Firmware!
    ...  sec=${5 * 60}
    Step  4   powerCycleToOpenbmc


ALI_DIAG_TC013_TLV_EEPROM_UPDATE
    [Tags]  ALI_DIAG_TC013_TLV_EEPROM_UPDATE
    ...  migaloo

    # Save the TLV EEPROM default to restore it later
    # Step x is used to share the pattern
    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Step  x  execute command and verify with unordered pattern list  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -r  patterns=${eeprom_tlv_patterns}  msg=Failed to dump TLV eeprom by diagtool!  AND
    ...  set test variable  &{diagtool_tlv_info}  &{matches}  AND
    ...  Step  x  execute command and verify with unordered pattern list  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=show platform syseeprom  patterns=${eeprom_tlv_patterns}  msg=Failed to dump TLV eeprom by diagtool!  AND
    ...  set test variable  &{sonic_tlv_info}  &{matches}

    Step  1   execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -h
    ...  patterns=${diagos_eeprom_test_patterns}
    ...  msg=Failed to verify -h/help option!
    Step  2   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -v
    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
    ...  msg=Failed, not found version!
    Step  3  execute command and verify exit code    # close Write protection, be able to write all eeprom.
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeprom_lock_and_unlock_migaloo -c
    ...  msg=Failed to close Write protection!${\n}Non zero exit code!

    # Write some stuff to TLV EEPROM
    Step  4   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 --dump
    ...  msg=Failed to dump TLV info!${\n}Non zero exit code!
    Step  5   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -l
    ...  msg=Failed to list TLV eeprom!${\n}Non zero exit code!


    Step  6   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x21 -D "${eeprom_tlv_dummy}[product_name]"
    ...  msg=Failed to write Product Name!${\n}Non zero exit code!
    Step  7   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x22 -D "${eeprom_tlv_dummy}[part_number]"
    ...  msg=Failed to write Part Number!${\n}Non zero exit code!
    Step  8   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x23 -D "${eeprom_tlv_dummy}[serial_number]"
    ...  msg=Failed to write Serial Number!${\n}Non zero exit code!
    Step  9   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x24 -D "${eeprom_tlv_dummy}[base_mac]"
    ...  msg=Failed to write Base MAC Address!${\n}Non zero exit code!
    Step  10   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x25 -D "${eeprom_tlv_dummy}[mfg_date]"
    ...  msg=Failed to write Manufacture Date!${\n}Non zero exit code!
    Step  11  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x26 -D "${eeprom_tlv_dummy}[device_version]"
    ...  msg=Failed to write Device Version!${\n}Non zero exit code!
    Step  12  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x27 -D "${eeprom_tlv_dummy}[label_revision]"
    ...  msg=Failed to write Label Revision!${\n}Non zero exit code!
    Step  13  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x28 -D "${eeprom_tlv_dummy}[platform_name]"
    ...  msg=Failed to write Platform Name!${\n}Non zero exit code!
    Step  14  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x29 -D "${eeprom_tlv_dummy}[onie_version]"
    ...  msg=Failed to write ONIE Version!${\n}Non zero exit code!
    Step  15  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2A -D "${eeprom_tlv_dummy}[mac_addr]"
    ...  msg=Failed to write MAC Addresses!${\n}Non zero exit code!
    Step  16  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2B -D "${eeprom_tlv_dummy}[mfg]"
    ...  msg=Failed to write Manufacturer!${\n}Non zero exit code!
    Step  17  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2C -D "${eeprom_tlv_dummy}[mfg_country]"
    ...  msg=Failed to write Manufacture Country!${\n}Non zero exit code!
    Step  18  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2D -D "${eeprom_tlv_dummy}[vendor_name]"
    ...  msg=Failed to write Vendor Name!${\n}Non zero exit code!
    Step  19  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2E -D "${eeprom_tlv_dummy}[diag_version]"
    ...  msg=Failed to write Diag Version!${\n}Non zero exit code!
    Step  20  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2F -D "${eeprom_tlv_dummy}[service_tag]"
    ...  msg=Failed to write Service Tag!${\n}Non zero exit code!
    Step  21  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0xFD -D "${eeprom_tlv_dummy}[vendor_ext]"
    ...  msg=Failed to write Vendor Extension!${\n}Non zero exit code!

    # Now, try to turn off/on the AC power and expected the all variables to not changed
    # 2rd dump TLV EEPROM
    Step  22  power cycle to mode  mode=${diagos_mode}
    Step  23  open prompt and login to root user  console=${diagos_mode}
    Step  24  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -t tlv -d 1 -C 256 -r
    ...  patterns=${eeprom_tlv_patterns}
    ...  msg=Failed to dump TLV eeprom by diagtool!
    set test variable  &{diagtool_tlv_info_2rd}  &{matches}
    Step  25  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=show platform syseeprom
    ...  patterns=${eeprom_tlv_patterns}
    ...  msg=Failed to dump TLV eeprom by diagtool!
    set test variable  &{sonic_tlv_info_2rd}  &{matches}

    # It should equal for each stage...
    Step  26  compare two dictionaries with matched key
    ...  original=${diagtool_tlv_info}
    ...  compare=${sonic_tlv_info}
    ...  msg=Default TLV EEPROM compare${\n}The diagtool and SONiC command is not matched for one or more TLV EEPROM variable(s)
    Step  27  compare two dictionaries with matched key
    ...  original=${diagtool_tlv_info_2rd}
    ...  compare=${sonic_tlv_info_2rd}
    ...  msg=The device already turn off/on${\n}The diagtool and SONiC command is not matched for one or more TLV EEPROM variable(s)
    Step  28  execute command and verify exit code    # close Write protection, be able to write all eeprom.
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeprom_lock_and_unlock_migaloo -c
    ...  msg=Failed to close Write protection!${\n}Non zero exit code!

    [Teardown]  Run Keywords
    # Write the default to TLV EEPROM
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x21 -D "${diagtool_tlv_info}[product_name]"  msg=Failed to write or not found Product Name!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x22 -D "${diagtool_tlv_info}[part_number]"  msg=Failed to write or not found Part Number!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x23 -D "${diagtool_tlv_info}[serial_number]"  msg=Failed to write or not found Serial Number!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x24 -D "${diagtool_tlv_info}[base_mac]"  msg=Failed to write or not found Base MAC Address!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x25 -D "${diagtool_tlv_info}[mfg_date]"  msg=Failed to write or not found Manufacture Date!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x26 -D "${diagtool_tlv_info}[device_version]"  msg=Failed to write or not found Device Version!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x27 -D "${diagtool_tlv_info}[label_device]"  msg=Failed to write or not found Label Revision!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x28 -D "${diagtool_tlv_info}[platform_name]"  msg=Failed to write or not found Platform Name!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x29 -D "${diagtool_tlv_info}[onie_version]"  msg=Failed to write or not found ONIE Version!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2A -D "${diagtool_tlv_info}[mac_addr]"  msg=Failed to write or not found MAC Addresses!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2B -D "${diagtool_tlv_info}[mfg]"  msg=Failed to write or not found Manufacturer!${\n}Non zero exit code!  AND
    # diagtool does not provide Manufacture Country, take it from SONiC tool!
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2C -D "${sonic_tlv_info}[mfg_country]"  msg=Failed to write or not found Manufacture Country!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2D -D "${diagtool_tlv_info}[vendor_name]"  msg=Failed to write or not found Vendor Name!${\n}Non zero exit code!  AND
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2E -D "${diagtool_tlv_info}[diag_version]"  msg=Failed to write or not found Diag Version!${\n}Non zero exit code!  AND
    # diagtool does not provide Service Tag, take it from SONiC tool!
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0x2F -D "${sonic_tlv_info}[service_tag]"  msg=Failed to write or not found Service Tag!${\n}Non zero exit code!  AND
    # Take dummy!
    ...  execute command and verify exit code  console=${diagos_mode}  path=${diagos_cpu_diag_path}  command=./cel-eeprom-test -t tlv -d 1 -C 256 -w -A 0xFD -D "${eeprom_tlv_dummy}[vendor_ext]"  msg=Failed to write or not found Vendor Extension!${\n}Non zero exit code!


ALI_DIAG_TC014_SMBIOS_FRU_EEPROM_UPDATE
    [Tags]  ALI_DIAG_TC014_SMBIOS_FRU_EEPROM_UPDATE
    ...  migaloo
    ...  SHAMU_DIAG_TC006_SMBIOS_FRU_BURNING
    ...  shamu

    [Setup]  Run Keywords
    # Open prompt for root user
    ...  power cycle to mode  mode=${diagos_mode}
    ...  AND  open prompt and login to root user  console=${diagos_mode}
    ...  AND  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3
    ...  AND  Sleep  45s  # Wait for some terrible I2C bus add messages
    ...  AND  Step  x  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -d
    ...  patterns=${diagos_eeprom_tool_d_patterns}
    ...  msg=Failed to show EEPROM/SMBIOS FRU!
    ...  AND  set test variable  &{eeprom_tool_d}  &{matches}
    # dmidecode
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 0
    ...  AND  Step  x  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 1
    ...  patterns=${diagos_dmidecode_t1_patterns}
    ...  msg=Failed to show dmidecode/system info!
    ...  AND  set test variable  &{dmidecode_t1}  &{matches}
    ...  AND  Step  x  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 2
    ...  patterns=${diagos_dmidecode_t2_patterns}
    ...  msg=Failed to show dmidecode/board info!
    ...  AND  set test variable  &{dmidecode_t2}  &{matches}
    ...  AND  Step  x  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 3
    ...  patterns=${diagos_dmidecode_t3_patterns}
    ...  msg=Failed to show dmidecode/board info!
    ...  AND  set test variable  &{dmidecode_t3}  &{matches}

    Step   1  Log  >>EEPROM test help option (if migaloo)<<
    Run Keyword If  '${PLATFORM}' == 'migaloo'
    ...  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-eeprom-test -h
    ...  patterns=${diagos_eeprom_help_patterns}
    ...  msg=Failed to verify -h option!

    # Re-boot before compare EEPROM
    Step   2  power cycle to mode  mode=${diagos_mode}

    # Compare system, board and chassis info
    # dmidecode -t 1
    Step   3  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[pd_name]  ${dmidecode_t1}[dmi_name]
    ...  msg=Failed, board name does not match for eeprom_tool and dmidecode!
    Step   4  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[pd_version]  ${dmidecode_t1}[dmi_version]
    ...  msg=Failed, board version does not match for eeprom_tool and dmidecode!
    Step   5  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[pd_sku]  ${dmidecode_t1}[dmi_sku]
    ...  msg=Failed, SKU does not match for eeprom_tool and dmidecode!
    Step   6  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[pd_family]  ${dmidecode_t1}[dmi_family]
    ...  msg=Failed, product family does not match for eeprom_tool and dmidecode!

    # dmidecode -t 2
    Step   7  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[brd_mfg]  ${dmidecode_t2}[dmi_mfg]
    ...  msg=Failed, Manufacturer does not match for eeprom_tool and dmidecode!
    Step   8  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[brd_revision]  ${dmidecode_t2}[dmi_version]
    ...  msg=Failed, board revision does not match for eeprom_tool and dmidecode!
    Step   9  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[brd_serial]  ${dmidecode_t2}[dmi_serial]
    ...  msg=Failed, board serial number does not match for eeprom_tool and dmidecode!
    Step  10  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[brd_asset_tag]  ${dmidecode_t2}[dmi_asset_tag]
    ...  msg=Failed, board asset tag does not match for eeprom_tool and dmidecode!

    # dmidecode -t 3
    Step  11  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[cs_serial]  ${dmidecode_t3}[dmi_serial]
    ...  msg=Failed, chassis serial number does not match for eeprom_tool and dmidecode!
    Step  12  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[cs_mfg]  ${dmidecode_t3}[dmi_mfg]
    ...  msg=Failed, chassis manufacture does not match for eeprom_tool and dmidecode!
    Step  13  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[cs_version]  ${dmidecode_t3}[dmi_version]
    ...  msg=Failed, chassis version does not match for eeprom_tool and dmidecode!
    Step  14  Should Be Equal As Strings
    ...  ${eeprom_tool_d}[cs_asset_tag]  ${dmidecode_t3}[dmi_asset_tag]
    ...  msg=Failed, chassis asset tag does not match for eeprom_tool and dmidecode!

    # Update SMBIOS EEPROM
    Log  >>Close eeprom write protection!<<
    execute command and verify exit code    # close Write protection, be able to write all eeprom.
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeprom_lock_and_unlock_migaloo -c
    ...  msg=Failed to close Write protection!${\n}Non zero exit code!
    Step  15  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "chassis_type" -v "A"
    ...  msg=Failed to write chassis type!
    Step  16  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "chassis_serial_number" -v "CLR3174FCL03090410015"
    ...  msg=Failed to write chassis serial number!
    Step  17  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "chassis_manufacture" -v "Celestica"
    ...  msg=Failed to write chassis manufacture!
    Step  18  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "chassis_version" -v "01"
    ...  msg=Failed to write chassis version!
    Step  19  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "chassis_asset_tag" -v "PLEASE-UPDATE"
    ...  msg=Failed to write chassis asset tag!
    Step  20  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_manufacture" -v "Celestica"
    ...  msg=Failed to write board manufacture!
    Step  21  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_product_name" -v "R3130-G0002-01"
    ...  msg=Failed to write board product name!
    Step  22  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_serial_number" -v "SN12345678"
    ...  msg=Failed to write board serial number!
    Step  23  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_revision" -v "02"
    ...  msg=Failed to write board revision!
    Step  24  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_asset_tag" -v "R3130-G0002-01"
    ...  msg=Failed to write board asset tag!
    Step  25  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_location" -v "CHN"
    ...  msg=Failed to write board location!
    Step  26  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_manufecture" -v "Celestica"
    ...  msg=Failed to write product manufecture!
    Step  27  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_name" -v "AS14-40D-F"
    ...  msg=Failed to write product name!
    Step  28  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_version" -v "03"
    ...  msg=Failed to write product version!
    Step  29  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_serial_number" -v "SN12345678"
    ...  msg=Failed to write product serial number!

    # No verify, just check the return code
    Run Keyword If  '${PLATFORM}' == 'shamu'
    ...  RUN KEYWORDS
    ...  Log  >>Step 30 and 31<<
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_asset_tag" -v "R3130-M0112-01"
    ...  msg=Failed to write product asset tag!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_FRU_ID" -v "0x0001"
    ...  msg=Failed to write product FRU ID!

    Step  32  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_system_UUID" -v "0x0102030405060708090a0b0c0d0e0f"
    ...  msg=Failed to write product system UUID!
    Step  33  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_SKU_number" -v "R3130-G0002-01"
    ...  msg=Failed to write product SKU number!

    Log  >>Step 34<<
    Run Keyword If  '${PLATFORM}' == 'migaloo'
    ...  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_family_name" -v "migaloo"
    ...  msg=Failed to write product family name!
    ...  ELSE IF  '${PLATFORM}' == 'shamu'
    ...  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_family_name" -v "shamu"
    ...  msg=Failed to write product family name!

    Step  35  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -u
    ...  patterns=${regularly_unexpected_patterns}
    ...  msg=Failed to update!

    RUN KEYWORD IF  '${PLATFORM}' == 'migaloo'
    ...  RUN KEYWORDS
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  DiagOS renew IP using DHCP and set variable
    ...  AND  Log  >>Step 35.2<<
    ...  AND  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${diagos_image_bios_path}
    ...  source_file=${diagos_bios_fru_eeprom_internal_new_image}
    ...  destination=${diagos_bios_fru_eeprom_internal_save_to}
    ...  AND  Log  >>Step 35.3<<
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -i ${diagos_bios_fru_eeprom_internal_save_to}/${diagos_bios_fru_eeprom_internal_new_image}
    ...  msg=Failed to update fru eeprom internal area!

    Step  36  power cycle to mode  mode=${diagos_mode}

    Log  >>Close eeprom write protection!<<
    execute command and verify exit code    # close Write protection, be able to write all eeprom.
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeprom_lock_and_unlock_migaloo -c
    ...  msg=Failed to close Write protection!${\n}Non zero exit code!

    # Re-check all it again
    Step  37  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -d
    ...  patterns=${diagos_eeprom_tool_d_patterns}
    ...  msg=Failed to show EEPROM/SMBIOS FRU!
    set test variable  &{eeprom_tool_d_2nd}  &{matches}

    # dmidecode
    Step  38  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 0
    Step  39  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 1
    ...  patterns=${diagos_dmidecode_t1_patterns}
    ...  msg=Failed to show dmidecode/system info!
    set test variable  &{dmidecode_t1_2nd}  &{matches}
    Step  40  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 2
    ...  patterns=${diagos_dmidecode_t2_patterns}
    ...  msg=Failed to show dmidecode/board info!
    set test variable  &{dmidecode_t2_2nd}  &{matches}
    Step  41  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 3
    ...  patterns=${diagos_dmidecode_t3_patterns}
    ...  msg=Failed to show dmidecode/board info!
    set test variable  &{dmidecode_t3_2nd}  &{matches}

    # Re-compare system, board and chassis info again
    # dmidecode -t 1
    Step  42  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[pd_name]  ${dmidecode_t1_2nd}[dmi_name]
    ...  msg=Failed, board name does not match for eeprom_tool and dmidecode!
    Step  43  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[pd_version]  ${dmidecode_t1_2nd}[dmi_version]
    ...  msg=Failed, board version does not match for eeprom_tool and dmidecode!
    Step  44  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[pd_sku]  ${dmidecode_t1_2nd}[dmi_sku]
    ...  msg=Failed, SKU does not match for eeprom_tool and dmidecode!
    Step  45  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[pd_family]  ${dmidecode_t1_2nd}[dmi_family]
    ...  msg=Failed, product family does not match for eeprom_tool and dmidecode!

    # dmidecode -t 2
    Step  46  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[brd_mfg]  ${dmidecode_t2_2nd}[dmi_mfg]
    ...  msg=Failed, Manufacturer does not match for eeprom_tool and dmidecode!
    Step  47  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[brd_revision]  ${dmidecode_t2_2nd}[dmi_version]
    ...  msg=Failed, board revision does not match for eeprom_tool and dmidecode!
    Step  48  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[brd_serial]  ${dmidecode_t2_2nd}[dmi_serial]
    ...  msg=Failed, board serial number does not match for eeprom_tool and dmidecode!
    Step  49  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[brd_asset_tag]  ${dmidecode_t2_2nd}[dmi_asset_tag]
    ...  msg=Failed, board asset tag does not match for eeprom_tool and dmidecode!

    # dmidecode -t 3
    Step  50  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[cs_serial]  ${dmidecode_t3_2nd}[dmi_serial]
    ...  msg=Failed, chassis serial number does not match for eeprom_tool and dmidecode!
    Step  51  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[cs_mfg]  ${dmidecode_t3_2nd}[dmi_mfg]
    ...  msg=Failed, chassis manufacture does not match for eeprom_tool and dmidecode!
    Step  52  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[cs_version]  ${dmidecode_t3_2nd}[dmi_version]
    ...  msg=Failed, chassis version does not match for eeprom_tool and dmidecode!
    Step  53  Should Be Equal As Strings
    ...  ${eeprom_tool_d_2nd}[cs_asset_tag]  ${dmidecode_t3_2nd}[dmi_asset_tag]
    ...  msg=Failed, chassis asset tag does not match for eeprom_tool and dmidecode!

    # Finally, restore to default value
    # Update SMBIOS EEPROM
    [Teardown]  Run Keywords
    ...  Run Keyword If  '${PLATFORM}' == 'migaloo'  # Run "chassis_type" only for migaloo
    ...  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "chassis_type" -v "${eeprom_tool_d}[cs_type]"
    ...  msg=Failed to write chassis type!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "chassis_serial_number" -v "${eeprom_tool_d}[cs_serial]"
    ...  msg=Failed to write chassis serial number!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "chassis_manufacture" -v "${eeprom_tool_d}[cs_mfg]"
    ...  msg=Failed to write chassis manufacture!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "chassis_version" -v "${eeprom_tool_d}[cs_version]"
    ...  msg=Failed to write chassis version!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "chassis_asset_tag" -v "${eeprom_tool_d}[cs_asset_tag]"
    ...  msg=Failed to write chassis asset tag!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_manufacture" -v "${eeprom_tool_d}[brd_mfg]"
    ...  msg=Failed to write board manufacture!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_product_name" -v "${eeprom_tool_d}[brd_product_name]"
    ...  msg=Failed to write board product name!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_serial_number" -v "${eeprom_tool_d}[brd_serial]"
    ...  msg=Failed to write board serial number!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_revision" -v "${eeprom_tool_d}[brd_revision]"
    ...  msg=Failed to write board revision!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_asset_tag" -v "${eeprom_tool_d}[brd_asset_tag]"
    ...  msg=Failed to write board asset tag!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "board_location" -v "${eeprom_tool_d}[brd_location]"
    ...  msg=Failed to write board location!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_manufecture" -v "${eeprom_tool_d}[pd_mfg]"
    ...  msg=Failed to write product manufecture!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_name" -v "${eeprom_tool_d}[pd_name]"
    ...  msg=Failed to write product name!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_version" -v "${eeprom_tool_d}[pd_version]"
    ...  msg=Failed to write product version!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_serial_number" -v "${eeprom_tool_d}[pd_serial]"
    ...  msg=Failed to write product serial number!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_system_UUID" -v "${eeprom_tool_d}[pd_system_uuid]"
    ...  msg=Failed to write product system UUID!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_SKU_number" -v "${eeprom_tool_d}[pd_sku]"
    ...  msg=Failed to write product SKU number!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -w "product_family_name" -v "${eeprom_tool_d}[pd_family]"
    ...  msg=Failed to write product family name!
    ...  AND  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_smbios_fru_eeprom_path}
    ...  command=./eeprom_tool -u
    ...  patterns=${regularly_unexpected_patterns}
    ...  msg=Failed to update!
    ...  AND  power cycle to mode  mode=${diagos_mode}


# ALI_DIAG_TC015_BMC_SIDE_FRU_EEPROM_UPDATE  ## Covered by OpenBMC Test Cases.
#    [Tags]  ALI_DIAG_TC015_BMC_SIDE_FRU_EEPROM_UPDATE
#    ...  migaloo  long_time
#
#    # Typically total run time is 75 minutes
#
#    [Setup]  Run Keywords
#    ...  open prompt and login to root user  console=${diagos_mode}  AND
#    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
#    ...  Sleep  45s  # Wait for some terrible I2C bus add messages
#
#    Step   1  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> COMe <<
#    ...  path=${openbmc_come_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d
#    ...  eeprom_tool_write=./eeprom_tool -w
#    ...  eeprom_tool_update=./eeprom_tool -u
#    ...  fru_util_dump=fru-util come
#    Step   2  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> FCB <<
#    ...  path=${openbmc_fcb_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d
#    ...  eeprom_tool_write=./eeprom_tool -w
#    ...  eeprom_tool_update=./eeprom_tool -u
#    ...  fru_util_dump=fru-util fb
#    Step   3  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> Linecard 1 <<
#    ...  path=${openbmc_linecard_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d -l 1
#    ...  eeprom_tool_write=./eeprom_tool -w -l 1
#    ...  eeprom_tool_update=./eeprom_tool -u -l 1
#    Step   4  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> Linecard 2 <<
#    ...  path=${openbmc_linecard_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d -l 2
#    ...  eeprom_tool_write=./eeprom_tool -w -l 2
#    ...  eeprom_tool_update=./eeprom_tool -u -l 2
#    Step   5  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> System <<
#    ...  path=${openbmc_system_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d
#    ...  eeprom_tool_write=./eeprom_tool -w
#    ...  eeprom_tool_update=./eeprom_tool -u
#    ...  fru_util_dump=fru-util sys
#    Step   6  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> Fan 1 <<
#    ...  path=${openbmc_fan_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d -f 1
#    ...  eeprom_tool_write=./eeprom_tool -w -f 1
#    ...  eeprom_tool_update=./eeprom_tool -u -f 1
#    ...  fru_util_dump=fru-util fan 1
#    Step   7  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> Fan 2 <<
#    ...  path=${openbmc_fan_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d -f 2
#    ...  eeprom_tool_write=./eeprom_tool -w -f 2
#    ...  eeprom_tool_update=./eeprom_tool -u -f 2
#    ...  fru_util_dump=fru-util fan 2
#    Step   8  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> Fan 3 <<
#    ...  path=${openbmc_fan_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d -f 3
#    ...  eeprom_tool_write=./eeprom_tool -w -f 3
#    ...  eeprom_tool_update=./eeprom_tool -u -f 3
#    ...  fru_util_dump=fru-util fan 3
#    Step   9  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> Fan 4 <<
#    ...  path=${openbmc_fan_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d -f 4
#    ...  eeprom_tool_write=./eeprom_tool -w -f 4
#    ...  eeprom_tool_update=./eeprom_tool -u -f 4
#    ...  fru_util_dump=fru-util fan 4
#    Step  10  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> Fan 5 <<
#    ...  path=${openbmc_fan_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d -f 5
#    ...  eeprom_tool_write=./eeprom_tool -w -f 5
#    ...  eeprom_tool_update=./eeprom_tool -u -f 5
#    ...  fru_util_dump=fru-util fan 5
#    Step   11  Edit eeprom.cfg, write, update and dump to verify
#    ...  log_msg_header=>> BMC <<
#    ...  path=${openbmc_bmc_fru_eeprom_path}
#    ...  eeprom_tool_dump=./eeprom_tool -d
#    ...  eeprom_tool_write=./eeprom_tool -w
#    ...  eeprom_tool_update=./eeprom_tool -u
#    ...  fru_util_dump=fru-util bmc


# All the steps below are working fine, and the only one unfinished is how to compare it!
ALI_DIAG_TC016_I2C_DEVICE_SCAN
    [Tags]  ALI_DIAG_TC016_I2C_DEVICE_SCAN
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    # SONiC/Diag OS
    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-i2c-test -h
    ...  patterns=${diagos_i2c_test_help_patterns}
    ...  msg=Failed to verify -h/help option!
    # SONiC/Diag OS: Find a list of I2C bus
    Step  2   execute command and verify with a pattern for table
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-i2c-test -l
    ...  pattern=\\\\/sys\\\\/bus\\\\/i2c\\\\/devices\\\\/(?P<bus>\\\\d+)-\\\\d+
    ...  msg=Failed, not found any I2C bus pattern!
    set test variable  &{diag_bus_list}  &{matches}
    # SONiC/Diag OS: Find a list of I2C address
    Step  3   search for a regexp for table
    ...  text=${text}
    ...  pattern=\\\\/sys\\\\/bus\\\\/i2c\\\\/devices\\\\/\\\\d+-(?P<addr>\\\\d+)
    ...  msg=Failed, not found any I2C address pattern!
    set test variable  &{diag_addr_list}  &{matches}

    Step  4   execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-i2c-test -s
    ...  patterns=${regularly_unexpected_patterns}
    ...  sec=${10 * 60}
    ...  msg=Failed!
    Step  5   execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-i2c-test -r --bus 0 -A 0x56 -R 0x00 -C 2
    ...  patterns=${regularly_unexpected_patterns}
    ...  msg=Failed to read the data on the bus!${\n}!
    Step  6   execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-i2c-test --dump --bus 0 -A 0x56
    ...  patterns=${regularly_unexpected_patterns}
    ...  msg=Failed to dump all data on the bus!${\n}The command is return non-zero exit code!
    Step  7   execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-i2c-test -s --bus 0
    ...  patterns=${regularly_unexpected_patterns}
    ...  msg=Failed to scan the device on the bus!${\n}The command is return non-zero exit code!
    Step  8   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-i2c-test --detect
    ...  msg=Failed to check/detect all the device on the bus!${\n}The command is return non-zero exit code!
    Step  9   execute command and verify with a pattern for table
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=i2cdetect -l
    ...  pattern=(?m)^i2c-(?P<bus>\\\\d+)
    ...  msg=Failed to list all the device on the bus!
    set test variable  &{i2cdetect_bus_list}  &{matches}
    Step  10   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-i2c-test --all
    ...  pattern=(?mi)^[ \\\\t]*I2C test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed to test all!
    Step  11  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-i2c-test -v
    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
    ...  msg=Failed, not found version!

    # OpenBMC
    Step  12  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  path=${openbmc_diag_bin_path}
    ...  command=./cel-i2c-test -h
    ...  patterns=${openbmc_i2c_test_help_patterns}
    ...  msg=Failed to verify -h/help option!
    Step  13  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  path=${openbmc_diag_bin_path}
    ...  command=./cel-i2c-test -s
    ...  pattern=[ \\\\t]*All the I2C devices test.*(?P<result>PASS)
    ...  msg=Failed to scan all the device on the bus, not found the pass pattern!
    ...  sec=${3 * 60}
    Step  14  execute command and verify with a pattern for table
    ...  console=${openbmc_mode}
    ...  path=${openbmc_diag_bin_path}
    ...  command=./cel-i2c-test -l
    ...  pattern=(?m)^[ \\\\t]+.*?[ \\\\t]+(?P<bus>\\\\d+)[ \\\\t]+0x[0-9a-fA-F]{2}
    ...  msg=Failed to list all the device on the bus!
    set test variable  &{openbmc_bus_list}  &{matches}
    Step  15  search for a regexp for table
    ...  text=${text}
    ...  pattern=(?m)^[ \\\\t]+.*?[ \\\\t]+\\\\d+[ \\\\t]+(?P<addr>0x[0-9a-fA-F]{2})
    ...  msg=Failed, not found any I2C address pattern!
    set test variable  &{openbmc_addr_list}  &{matches}
    Step  16  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  path=${openbmc_diag_bin_path}
    ...  command=./cel-i2c-test -a
    ...  pattern=(?mi)^[ \\\\t]*All the I2C devices test.*(?P<result>PASS)
    ...  msg=Failed to test all!
    ...  sec=${3 * 60}


ALI_DIAG_TC017_PCIE_DEVICE_SCAN
    [Tags]  ALI_DIAG_TC017_PCIE_DEVICE_SCAN
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-pci-test -h
    ...  patterns=${pci_help_patterns}
    ...  msg=Failed to verify -h option!
    Step  2   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-pci-test -l
    Step  3   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-pci-test -v
    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
    ...  msg=Failed, not found version!
    Step  4   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-pci-test -a
    ...  pattern=(?mi)^[ \\\\t]*PCIe test[ \\\\t]+.*(?P<result>PASS)


ALI_DIAG_TC018_FPGA_ACCESS_TEST
    [Tags]  ALI_DIAG_TC018_FPGA_ACCESS_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    # TC_018_1
    Step   1  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-fpga-test -h
    ...  patterns=${diagos_fpga_help_patterns}
    ...  msg=Failed to verify -h/help option!
    Step   2  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -l
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?i)fpga.*?(?P<path>/.*/FPGA)
    set test variable  ${fpga_device_path}  ${match}
    Step   3  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -v
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
    ...  msg=Failed, not found the version!
    Step   4  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -a
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*fpga test[ \\\\t\\\\.]*.*(?P<result>PASS)
    ...  msg=Failed, not found pass result!
    Step   5  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -r -d 1 -A 0x00
    ...  path=${diagos_cpu_diag_path}
    Step   6  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -r -d 1 -A 0x04
    ...  path=${diagos_cpu_diag_path}
    Step   7  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -w -d 1 -A 0x04 -D 0x05
    ...  path=${diagos_cpu_diag_path}
    Step   8  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -r -d 1 -A 0x04
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*fpga Reg \\\\[0x04\\\\] data: (?P<reg>0x00000005)
    ...  msg=Failed, should be read as wrote as 0x05!
    Step   9  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -d 1 -V
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*fpga Reg \\\\[0x00\\\\] data: (?P<reg>0x[0-9a-fA-F]+)
    ...  msg=Failed, not found the FPGA version!
    set test variable  ${diagtool_fpga_version}  ${match}

    # TC_018_2
    Step  10  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=echo 0x00 > /sys/devices/platform/AS24128D.switchboard/FPGA/getreg
    ...  path=${diagos_cpu_diag_path}
    Step  11  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=cat /sys/devices/platform/AS24128D.switchboard/FPGA/getreg
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^(?P<reg>0x[0-9a-fA-F]+)$
    ...  msg=Failed, not found the FPGA version!
    set test variable  ${sysfs_fpga_version}  ${match}

    Step  12  Should Be Equal As Strings
    ...  first=${diagtool_fpga_version}[reg]
    ...  second=${sysfs_fpga_version}[reg]
    ...  msg=Failed, the FPGA read by diagtool != sysfs${\n * 2}

    # TC_018_3
    Step  13  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=cat /usr/local/migaloo/configs/fpgas.yaml
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi)^[ \\\\t]*dev_path.*?\\\\"(?P<path>.*/FPGA)\\\\"
    ...  msg=Failed, not found the device path!
    set test variable  ${yaml_dev_path}  ${match}

    Step  14  Should Be Equal As Strings
    ...  first=${fpga_device_path}[path]
    ...  second=${yaml_dev_path}[path]
    ...  msg=Failed, the FPGA path read by yaml != diagtool${\n * 2}


ALI_DIAG_TC019_CPLD_ACCESS_TEST
    [Tags]  ALI_DIAG_TC019_CPLD_ACCESS_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -h
    ...  patterns=${cpld_help_patterns}
    ...  msg=Failed to verify -h option!
    Step  2   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -v
    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
    ...  msg=Failed, not found version!
    Step  3   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-cpld-test -l
    ...  path=${diagos_cpu_diag_path}
    Step  4   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -a
    ...  pattern=(?m)^[ \\\\t]*CPLD test[ \\\\t\\\\.]*.*(?P<result>PASS)
    ...  msg=Failed to verify -a option!

    Step  5   Read CPLD register  command=./cel-cpld-test -r -d 1 -A 0xa101
    Step  6   Write CPLD register  command=./cel-cpld-test -w -d 1 -A 0xa101 -D 0xee
    Step  7   Read CPLD register
    ...  command=./cel-cpld-test -r -d 1 -A 0xa101
    ...  pattern=data: (?P<data>0xee)
    ...  msg=Failed to verify CPLD read & write, expected to get 0xee!

    Step  8   Read CPLD register  command=./cel-cpld-test -r -d 2 -A 0x01
    Step  9   Write CPLD register  command=./cel-cpld-test -w -d 2 -A 0x01 -D 0xee
    Step  10  Read CPLD register
    ...  command=./cel-cpld-test -r -d 2 -A 0x01
    ...  pattern=data: (?P<data>0xee)
    ...  msg=Failed to verify CPLD read & write, expected to get 0xee!

    Step  11  Read CPLD register
    ...  command=./cel-cpld-test -d 1 -V
    ...  msg=Failed to read CPLD!
    Step  12  Read CPLD register
    ...  command=./cel-cpld-test -d 2 -V
    ...  msg=Failed to read CPLD!
    Step  13  Read CPLD register
    ...  command=./cel-cpld-test -d 3 -V
    ...  msg=Failed to read CPLD!
    Step  14  Read CPLD register
    ...  command=./cel-cpld-test -d 4 -V
    ...  msg=Failed to read CPLD!
    Step  15  Read CPLD register
    ...  command=./cel-cpld-test -d 5 -V
    ...  msg=Failed to read CPLD!
    Step  16  Read CPLD register
    ...  command=./cel-cpld-test -d 6 -V
    ...  msg=Failed to read CPLD!
    Step  17  Read CPLD register
    ...  command=./cel-cpld-test -d 7 -V
    ...  msg=Failed to read CPLD!


ALI_DIAG_TC021_PSU_PRESENT_TEST
    [Tags]  ALI_DIAG_TC021_PSU_PRESENT_TEST
    ...  migaloo

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  path=${openbmc_diag_bin_path}
    ...  command=./cel-psu-test -h
    ...  patterns=${psu_help_patterns}
    ...  msg=Failed to verify help option, may not found some option(s)!
    Step  2   verify all PSU status
    # Below step needed manual, unplug & plug for PSU 1 & 2, as such comment here!
    # ./cel-psu-test -s
    # Unplug
    Step  3   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  path=${openbmc_diag_bin_path}
    ...  command=./cel-psu-test -a
    ...  pattern=(?m)^[ \\\\t]+PSU Test[ \\\\.]+.*(?P<result>PASS)
    ...  msg=Failed for PSU Test All


ALI_DIAG_TC022_LPC_ACCESS_TEST
    [Tags]  ALI_DIAG_TC022_LPC_ACCESS_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step   1  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-lpc-test -h
    ...  patterns=${diagos_lpc_help_patterns}
    ...  msg=Failed to verify help option, may not found some option(s)!
    Step   2  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-lpc-test -a
    ...  pattern=(?mi)[ \\\\t]*CPU-?BMC LPC.*(?P<result>PASS)
    ...  msg=Failed for LPC Access Test All
    ...  sec=${5 * 60}


ALI_DIAG_TC023_SATA_ACCESS_TEST
    [Tags]  ALI_DIAG_TC023_SATA_ACCESS_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-sata-test -h
    ...  patterns=${sata_test_help_patterns}
    ...  msg=Failed to verify -h option!
    Step  2   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-sata-test -i
    ...  path=${diagos_cpu_diag_path}
    Step  3   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-sata-test -l
    ...  path=${diagos_cpu_diag_path}
    Step  4   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-sata-test -v
    ...  pattern=${sata_test_version_pattern}
    ...  msg=Failed to verify -v option!
    Step  5   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-sata-test --all
    ...  patterns=[r'Device Model.*?Passed', r'User Capacity.*?Passed']
    ...  is_check_exit_code=${FALSE}
    ...  msg=Failed to verify --all option!


# ALI_DIAG_TC024_TPM_ACCESS_TEST
#     [Tags]  ALI_DIAG_TC024_TPM_ACCESS_TEST
#     ...  migaloo

#     Step  1   execute command and verify with paired pattern list
#     ...  console=${openbmc_mode}
#     ...  path=${openbmc_diag_bin_path}
#     ...  command=./cel-tpm-test -h
#     ...  patterns=${openbmc_mdio_help_patterns}
#     ...  msg=Failed to verify -h/help option!


ALI_DIAG_TC025_MDIO_ACCESS_TEST
    [Tags]  ALI_DIAG_TC025_MDIO_ACCESS_TEST
    ...  migaloo

    # TC_025_1
    Step  1   execute command and verify with paired pattern list
    ...  console=${openbmc_mode}
    ...  path=${openbmc_diag_bin_path}
    ...  command=./cel-mdio-test -h
    ...  patterns=${openbmc_mdio_help_patterns}
    ...  msg=Failed to verify -h/help option!

    Step  2   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  path=${openbmc_diag_bin_path}
    ...  command=./cel-mdio-test -a
    Step  3   search for a pattern
    ...  text=${text}
    ...  pattern=(?mi)^[ \\\\t]*management phy BCM54616 mdio Test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed not found MGMT/BCM54616 pass pattern!
    Step  4   search for a pattern
    ...  text=${text}
    ...  pattern=(?mi)^[ \\\\t]*opemBMC phy BCM54616 mdio Test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed not found OpenBMC/BCM54616 pass pattern!

    Step  5   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=(printf "y\n" | bcm5387.sh --mode mdio)

    Step  6   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=mdio-util -s read 0x1e 0x34 0x00
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?mi)^(?P<default>0x[0-9a-fA-F]{2})$
    ...  msg=Failed to read from MDIO!
    set test variable  ${mdio_default}  ${match}
    Step  7   execute command and verify with unexpected patterns
    ...  console=${openbmc_mode}
    ...  command=mdio-util -s write 0x1e 0x34 0x00 0xaa
    ...  patterns=${openbmc_mdio_write_unexpected_patterns}
    ...  msg=Failed to write 0xaa to MDIO!
    Step  8   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=mdio-util -s read 0x1e 0x34 0x00
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?mi)^(?P<read>0xaa)$
    ...  msg=Failed to read from MDIO, expected to get 0xaa!

    # TC_025_2
    Step  9   execute command and verify with unexpected patterns
    ...  console=${openbmc_mode}
    ...  command=mdio-util -s write 0x1e 0x34 0x00 ${mdio_default}[default]
    ...  patterns=${openbmc_mdio_write_unexpected_patterns}
    ...  msg=Failed to write ${mdio_default}[default] to MDIO!
    Step  10  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=mdio-util -s read 0x1e 0x34 0x00
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?mi)^(?P<read>${mdio_default}[default])$
    ...  msg=Failed to read from MDIO, expected to get ${mdio_default}[default]!


ALI_DIAG_TC026_CPU_INFORMATION_TEST
    [Tags]  ALI_DIAG_TC026_CPU_INFORMATION_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpu-test -h
    ...  patterns=${cpu_test_help_patters}
    ...  msg=Failed to verify -h option!
    ...  is_check_exit_code=${FALSE}
    Step  2   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpu-test -a
    ...  patterns=${cpu_test_all_patterns}
    ...  msg=Failed to verify -a option!
    Step  3   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpu-test --all
    ...  patterns=${cpu_test_all_patterns}
    ...  msg=Failed to verify --all option!
    Step  4   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpu-test -v
    ...  pattern=${cpu_test_version_pattern}
    ...  msg=Failed to verify -v option!
    Step  5   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=lscpu
    ...  pattern=${lscpu_model_name_pattern}
    ...  msg=Failed, not found the CPU Model Name!
    Step  6   Should Be Equal As Strings
    ...  first=${matches}[cpu_model_name]
    ...  second=${match}[cpu_model_name]
    ...  msg=Failed to compare for CPU Model Name!


ALI_DIAG_TC027_MEMORY_TEST
    [Tags]  ALI_DIAG_TC027_MEMORY_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-mem-test -h
    ...  patterns=${diagos_mem_help_patterns}
    ...  msg=Failed to verify -h option!
    Step  2   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-mem-test -l
    ...  path=${diagos_cpu_diag_path}
    ...  msg=Failed to list the memory device!${\n}The command is return non-zero exit code!
    Step  3   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-mem-test -K
    ...  pattern=(?mi)[ \\\\t]*MEM memtester[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed to run memory test!${\n}Not found the pass pattern!
    ...  sec=${10 * 60}
    Step  4   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-mem-test -a
    ...  pattern=(?mi)[ \\\\t]*MEM test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed to run test-all memory!${\n}Not found the pass pattern!
    ...  sec=${10 * 60}
    Step  5   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-mem-test --all
    ...  pattern=(?mi)[ \\\\t]*MEM test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed to run test-all memory!${\n}Not found the pass pattern!
    ...  sec=${10 * 60}


ALI_DIAG_TC028_MANAGEMENT_ETHER_PORT_MAC_CHECK_TEST
    [Tags]   ALI_DIAG_TC028_MANAGEMENT_ETHER_PORT_MAC_CHECK_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-mac-test -h
    ...  patterns=${diagos_mac_help_patterns}
    ...  msg=Failed to verify -h option!
    Step  2   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-mac-test -v
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
    ...  msg=Failed, not found version!
    Step  3   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-mac-test -a
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi)^[ \\\\t]*MAC test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed, not found pass pattern!
    Step  4   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-mac-test --all
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi)^[ \\\\t]*MAC test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed, not found pass pattern!


ALI_DIAG_TC029_OOB_TEST
    [Tags]  ALI_DIAG_TC029_OOB_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-oob-test -h
    ...  patterns=${diagos_oob_help_patterns}
    ...  msg=Failed to verify -h option!
    Step  2   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-oob-test -v
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
    ...  msg=Failed, not found version!
    Step  3   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-oob-test -a
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi)^[ \\\\t]*OOB test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed, not found pass pattern!
    Step  4   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-oob-test --all
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi)^[ \\\\t]*OOB test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed, not found pass pattern!


ALI_DIAG_TC030_RTC_TEST
    [Tags]  ALI_DIAG_TC030_RTC_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-rtc-test -h
    ...  patterns=${diagos_rtc_help_patterns}
    ...  msg=Failed to verify -h option!
    Step  2   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-rtc-test -v
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
    ...  msg=Failed, not found version!

    # Start to test the time!
    Step  3   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-rtc-test -r
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*Current Date info :[ \\\\t]*(?P<date>.*\\\\d)
    ...  msg=Failed, not found date/time!
    set test variable  ${rtc}  ${match}
    Step  4   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=hwclock
    ...  pattern=(?m)^[ \\\\t]*(?P<date>\\\\d{4}.*?)\\\\.
    ...  msg=Failed, not found date/time!
    set test variable  ${hwclock}  ${match}
    Step  5   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=date --rfc-3339=seconds
    ...  pattern=(?m)^[ \\\\t]*(?P<date>\\\\d{4}.*?)\\\\+
    ...  msg=Failed, not found date/time!
    set test variable  ${date}  ${match}

    #  Diff it!
    Step  6   date/time difference
    ...  ${rtc}[date]  ${hwclock}[date]
    ...  diff=3
    ...  msg=Failed, the date is not the same for "cel-rtc-test -r" and "hwclock"${\n}, the diff is more than 3 seconds!
    Step  7   date/time difference
    ...  ${rtc}[date]  ${date}[date]
    ...  diff=5
    ...  msg=Failed, the date is not the same for "cel-rtc-test -r" and "date"${\n}, the diff is more than 5 seconds!

    # Add offset, write and read to verify
    ${offset}=  Add Time To Date
    ...  ${rtc}[date]  1 minute
    ...  exclude_millis=${TRUE}
    ${offset_formatted}=  Convert Date
    ...  ${offset}
    ...  result_format=%Y%m%d %H%M%S

    Step  8   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-rtc-test -w -D '${offset_formatted}'
    ...  path=${diagos_cpu_diag_path}
    Step  9   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-rtc-test -r
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*Current Date info :[ \\\\t]*(?P<date>.*\\\\d)
    ...  msg=Failed, not found date/time!
    set test variable  ${rtc_2nd}  ${match}
    Step  10  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=hwclock
    ...  pattern=(?m)^[ \\\\t]*(?P<date>\\\\d{4}.*?)\\\\.
    ...  msg=Failed, not found date/time!
    set test variable  ${hwclock_2nd}  ${match}
    Step  11  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=date --rfc-3339=seconds
    ...  pattern=(?m)^[ \\\\t]*(?P<date>\\\\d{4}.*?)\\\\+
    ...  msg=Failed, not found date/time!
    set test variable  ${date_2nd}  ${match}

    # Adjust time back to correct it!
    ${offset}=  Subtract Time From Date
    ...  ${rtc_2nd}[date]  1 minute
    ...  exclude_millis=${TRUE}
    ${offset_formatted}=  Convert Date
    ...  ${offset}
    ...  result_format=%Y%m%d %H%M%S
    Step  12  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-rtc-test -w -D '${offset_formatted}'
    ...  path=${diagos_cpu_diag_path}


    #  Diff it!
    Step  13   date/time difference
    ...  ${rtc_2nd}[date]  ${hwclock_2nd}[date]
    ...  diff=3
    ...  msg=Failed, the date is not the same for "cel-rtc-test -r" and "hwclock"${\n}, the diff is more than 3 seconds!
    Step  14   date/time difference
    ...  ${rtc_2nd}[date]  ${date_2nd}[date]
    ...  diff=5
    ...  msg=Failed, the date is not the same for "cel-rtc-test -r" and "date"${\n}, the diff is more than 5 seconds!

    # Reboot and check it again!
    Step  15  reboot UNIX-like OS  console=${diagos_mode}
    Step  16  open prompt and login to root user  console=${diagos_mode}

    Step  17  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-rtc-test -r
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*Current Date info :[ \\\\t]*(?P<date>.*\\\\d)
    ...  msg=Failed, not found date/time!
    set test variable  ${rtc_3nd}  ${match}
    Step  18  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=hwclock
    ...  pattern=(?m)^[ \\\\t]*(?P<date>\\\\d{4}.*?)\\\\.
    ...  msg=Failed, not found date/time!
    set test variable  ${hwclock_3nd}  ${match}
    Step  19  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=date --rfc-3339=seconds
    ...  pattern=(?m)^[ \\\\t]*(?P<date>\\\\d{4}.*?)\\\\+
    ...  msg=Failed, not found date/time!
    set test variable  ${date_3nd}  ${match}

    #  Diff it!
    Step  20   date/time difference
    ...  ${rtc_3nd}[date]  ${hwclock_3nd}[date]
    ...  diff=3
    ...  msg=Failed, the date is not the same for "cel-rtc-test -r" and "hwclock"${\n}, the diff is more than 3 seconds!
    Step  21   date/time difference
    ...  ${rtc_3nd}[date]  ${date_3nd}[date]
    ...  diff=5
    ...  msg=Failed, the date is not the same for "cel-rtc-test -r" and "date"${\n}, the diff is more than 5 seconds!

    # Finally, run test all!
    Step  22  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-rtc-test -a
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi)^[ \\\\t]*RTC test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed, not found pass pattern!
    Step  23  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-rtc-test --all
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi)^[ \\\\t]*RTC test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed, not found pass pattern!


ALI_DIAG_TC031_SOFTWARE_FIRMWARE_INFORMATION_INFO
    [Tags]  ALI_DIAG_TC031_SOFTWARE_FIRMWARE_INFORMATION_INFO
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-version-test -h
    ...  patterns=${diagos_version_help_patterns}
    ...  msg=Failed to verify -h option!
    Step  2   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-version-test -v
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
    ...  msg=Failed, not found version!
    Step  3   Wait for OpenBMC Info
    Step  4   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=${diagos_show_diag_version_command}
    ...  patterns=${diagos_version_show_patterns}
    ...  msg=Failed to verify -S/show option!
    ...  sec=${5 * 60}


ALI_DIAG_TC032_INTERNAL_USB_TEST
    [Tags]  ALI_DIAG_TC032_INTERNAL_USB_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-internal-usb-test -h
    ...  patterns=${diagos_int_usb_help_patterns}
    ...  msg=Failed to verify -h option!
    Step  2   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-internal-usb-test -a
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi).*usb test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed, not found the pass pattern!
    Step  3   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-internal-usb-test --all
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi).*usb test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed, not found the pass pattern!


ALI_DIAG_TC033_EXTERNAL_USB_TEST
    [Tags]  ALI_DIAG_TC033_EXTERNAL_USB_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-usb-test -h
    ...  patterns=${diagos_usb_help_patterns}
    ...  msg=Failed to verify help option!
    Step  2   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-usb-test -a
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi)^[ \\\\t]*usb test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed, not found the pass pattern!
    Step  3   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-usb-test --all
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?mi)^[ \\\\t]*usb test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed, not found the pass pattern!
    Step  4   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-usb-test -i
    ...  path=${diagos_cpu_diag_path}
    ...  is_check_exit_code=${FALSE}


# ALI_DIAG_TC034_I2C_DEVICE_TEST    ## Covered by ALI_DIAG_TC016_I2C_DEVICE_SCAN
#    [Tags]  ALI_DIAG_TC034_I2C_DEVICE_TEST
#    ...  migaloo
#
#    [Setup]  Run Keywords
#    ...  open prompt and login to root user  console=${diagos_mode}  AND
#    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
#    ...  Sleep  45s  # Wait for some terrible I2C bus add messages
#
#    Pass Execution If  '${loopback module?}' == 'FAIL'  This test case is skipped, it requires a loopback module on all ports!
#
#    # DIAG OS
#    Step  1   execute command and verify exit code
#    ...  console=${diagos_mode}
#    ...  command=i2cdetect -l
#    ...  path=${diagos_cpu_diag_path}
#    Step  2   find I2C device number by i2cdetect
#    Step  3   execute command and verify with ordered pattern list
#    ...  console=${diagos_mode}
#    ...  path=${diagos_cpu_diag_path}
#    ...  command=./cel-i2c-test -h
#    ...  patterns=${diagos_i2c_device_patterns}
#    ...  msg=Failed to verify help option!
#    Step  4   find I2C device number by diagtool
#    Step  5   execute command and verify exit code
#    ...  console=${diagos_mode}
#    ...  command=./cel-i2c-test -s
#    ...  path=${diagos_cpu_diag_path}
#    ...  sec=90
#    Step  6   execute command and verify exit code
#    ...  console=${diagos_mode}
#    ...  command=./cel-i2c-test -r --bus 0 -A 0x56 -R 0x00 -C 2
#    ...  path=${diagos_cpu_diag_path}
#    Step  7   execute command and verify exit code
#    ...  console=${diagos_mode}
#    ...  command=./cel-i2c-test -s --bus 0
#    ...  path=${diagos_cpu_diag_path}
#    Step  8   execute command and verify exit code
#    ...  console=${diagos_mode}
#    ...  command=./cel-i2c-test --dump --bus 0 -A 0x56
#    ...  path=${diagos_cpu_diag_path}
#    Step  9   find I2C device number by diagtool
#    ...  command=./cel-i2c-test --detect
#    ...  pattern=(?m)^(?P<dev>i2c.*? +.*? {2,}.*? {2,}.*)
#    Step  10  Should Be Equal As Integers
#    ...  ${i2cdetect_dev}[number]  ${diagtool_dev_number}
#    ...  Failed, the I2C devices detected by "i2cdetect -l" and "cel-i2c-test -l" are not the same!
#    Step  11  execute command and verify with a pattern
#    ...  console=${diagos_mode}
#    ...  path=${diagos_cpu_diag_path}
#    ...  command=./cel-i2c-test --all
#    ...  pattern=(?m)^[ \\\\t]*I2C test[ \\\\t]+.*(?P<result>PASS)
#    ...  msg=Failed to verify --all option!
#    ...  sec=90
#    Step  12  execute command and verify with a pattern
#    ...  console=${diagos_mode}
#    ...  command=./cel-i2c-test -v
#    ...  path=${diagos_cpu_diag_path}
#    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
#    ...  msg=Failed, not found version!
#
#    # OpenBMC
#    Step  13  execute command and verify with ordered pattern list
#    ...  console=${openbmc_mode}
#    ...  path=${openbmc_diag_bin_path}
#    ...  command=./cel-i2c-test -h
#    ...  patterns=${openbmc_i2c_help_patterns}
#    ...  msg=Failed to verify help option!
#    Step  14  execute command and verify with a pattern
#    ...  console=${openbmc_mode}
#    ...  command=./cel-i2c-test -s
#    ...  path=${openbmc_diag_bin_path}
#    ...  pattern=(?m)^[ \\\\t]*All the I2C devices test[ \\\\t]+.*(?P<result>PASS)
#    ...  msg=Failed, not found the pass pattern!
#    ...  sec=90s
#    Step  15  execute command and verify exit code
#    ...  console=${openbmc_mode}
#    ...  command=./cel-i2c-test -l
#    ...  path=${openbmc_diag_bin_path}
#    Step  16  execute command and verify exit code
#    ...  console=${openbmc_mode}
#    ...  command=i2cdetect -l
#    Step  17  find I2C device number by i2cdetect
#    ...  console=${openbmc_mode}


ALI_DIAG_TC035_10G_KG_TEST
    [Tags]  ALI_DIAG_TC035_10G_KG_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-10KR-test -h
    ...  patterns=${diagos_10kg_help_patterns}
    ...  msg=Failed to verify -h option!
    Step  2   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-10KR-test -a
    ...  pattern=(?m)^[ \\\\t]*10G KR test[ \\\\t]*.*(?P<result>PASS)
    ...  msg=Failed, not found the pass pattern!
    Step  3   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-10KR-test -v
    ...  pattern=(?m)^[ \\\\t]*.*version is : (?P<version>[\\\\d\\\\.]+)
    ...  msg=Failed, not found version!


ALI_DIAG_TC036_CHANGE_QSFP_POWER
    [Tags]  ALI_DIAG_TC036_CHANGE_QSFP_POWER
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step   1  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./luxshare_power_config.sh -h
    ...  msg=Failed to configuration all QSFP for high power!
    ...  sec=90
    Step   2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./luxshare_power_config.sh -n
    ...  msg=Failed to configuration all QSFP for low power!
    ...  sec=90


ALI_DIAG_TC039_MANAGEMENT_UART_SWITC_TEST
    [Tags]  ALI_DIAG_TC039_MANAGEMENT_UART_SWITC_TEST
    ...  migaloo

    Step  1   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=ifconfig
    ...  msg=Failed to execute ifconfig!
    Step  2   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=cat /etc/issue
    ...  msg=Failed to execute "cat /etc/issue"!
    Step  3   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=ifconfig
    ...  msg=Failed to execute ifconfig!
    Step  4   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=lscpu
    ...  msg=Failed to execute lscpu!


ALI_DIAG_TC040_QSFP_LOWER_SPEED_SIGNEL_TEST
    [Tags]  ALI_DIAG_TC040_QSFP_LOWER_SPEED_SIGNEL_TEST
    ...  migaloo  long_time

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    # TC_040_1
    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -h
    ...  patterns=${diagos_port_help_patterns}
    ...  path=${diagos_cpu_diag_path}
    ...  msg=Failed to verify port help option!

    # TC_040_2
    Step  2   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -s
    ...  path=${diagos_cpu_diag_path}
    Step  3   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -s -d 1
    ...  path=${diagos_cpu_diag_path}

    # All QSFPs
    # "in reset"
    Step  4   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -c -t reset -D 0
    ...  path=${diagos_cpu_diag_path}
    Step  5   Verify QSFP specific status
    ...  command=./cel-port-test -s
    ...  pattern=(?mi)^[ \\\\t]+(?P<number>\\\\d+)[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>in reset)[ \\\\t]+(?P<modsel>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>\\\\w[\\\\w ]+)
    ...  number_of_qsfp=${128*6}
    ...  msg=Failed, some of QSFP Port does not "in reset" status!${\n}Please check with the log for more detail!
    # "not in reset"
    Step  6   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -c -t reset -D 1
    ...  path=${diagos_cpu_diag_path}
    Step  7   Verify QSFP specific status
    ...  command=./cel-port-test -s
    ...  pattern=(?mi)^[ \\\\t]+(?P<number>\\\\d+)[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>not in reset)[ \\\\t]+(?P<modsel>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>\\\\w[\\\\w ]+)
    ...  number_of_qsfp=${128*6}
    ...  msg=Failed, some of QSFP Port does not "not in reset" status!${\n}Please check with the log for more detail!
    # One-by-one QSFP
    # "in reset"
    Step  8   Verify all QSFP one-by-one port specific status
    ...  pattern=[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>in reset)[ \\\\t]+(?P<modsel>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>\\\\w[\\\\w ]+)
    ...  command=./cel-port-test -c -t reset -D 0 -d
    ...  msg=Failed to verify one-by-one set "in reset"!
    # "not in reset"
    Step  9   Verify all QSFP one-by-one port specific status
    ...  pattern=[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>not in reset)[ \\\\t]+(?P<modsel>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>\\\\w[\\\\w ]+)
    ...  command=./cel-port-test -c -t reset -D 1 -d
    ...  msg=Failed to verify one-by-one set "not in reset"!

    # All QSFPs
    # "enable modsel"
    Step  10  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -c -t modsel -D 0
    ...  path=${diagos_cpu_diag_path}
    Step  11  Verify QSFP specific status
    ...  command=./cel-port-test -s
    ...  pattern=(?mi)^[ \\\\t]+(?P<number>\\\\d+)[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modsel>enable modsel)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>\\\\w[\\\\w ]+)
    ...  number_of_qsfp=${128*6}
    ...  msg=Failed, some of QSFP Port does not "enable modsel" status!${\n}Please check with the log for more detail!
    # "disable modsel"
    Step  12  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -c -t modsel -D 1
    ...  path=${diagos_cpu_diag_path}
    Step  13  Verify QSFP specific status
    ...  command=./cel-port-test -s
    ...  pattern=(?mi)^[ \\\\t]+(?P<number>\\\\d+)[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modsel>disable modsel)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>\\\\w[\\\\w ]+)
    ...  number_of_qsfp=${128*6}
    ...  msg=Failed, some of QSFP Port does not "disable modsel" status!${\n}Please check with the log for more detail!
    # One-by-one QSFP
    # "enable modsel"
    Step  14  Verify all QSFP one-by-one port specific status
    ...  pattern=[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modsel>enable modsel)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>\\\\w[\\\\w ]+)
    ...  command=./cel-port-test -c -t modsel -D 0 -d
    ...  msg=Failed to verify one-by-one set "enable modsel"!
    # "disable modsel"
    Step  15  Verify all QSFP one-by-one port specific status
    ...  pattern=[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modsel>disable modsel)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>\\\\w[\\\\w ]+)
    ...  command=./cel-port-test -c -t modsel -D 1 -d
    ...  msg=Failed to verify one-by-one set "disable modsel"!

    # All QSFPs
    # "low mode"
    Step  16  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -c -t lpmod -D 0
    ...  path=${diagos_cpu_diag_path}
    Step  17  Verify QSFP specific status
    ...  command=./cel-port-test -s
    ...  pattern=(?mi)^[ \\\\t]+(?P<number>\\\\d+)[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modsel>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>low mode)
    ...  number_of_qsfp=${128*6}
    ...  msg=Failed, some of QSFP Port does not "low mode" status!${\n}Please check with the log for more detail!
    # "high mode"
    Step  18  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -c -t lpmod -D 1
    ...  path=${diagos_cpu_diag_path}
    Step  19  Verify QSFP specific status
    ...  command=./cel-port-test -s
    ...  pattern=(?mi)^[ \\\\t]+(?P<number>\\\\d+)[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modsel>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>high mode)
    ...  number_of_qsfp=${128*6}
    ...  msg=Failed, some of QSFP Port does not "high mode" status!${\n}Please check with the log for more detail!
    # One-by-one QSFP
    # "low mode"
    Step  20  Verify all QSFP one-by-one port specific status
    ...  pattern=[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modsel>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>low mode)
    ...  command=./cel-port-test -c -t lpmod -D 0 -d
    ...  msg=Failed to verify one-by-one set "low mode"!
    # "high mode"
    Step  21  Verify all QSFP one-by-one port specific status
    ...  pattern=[ \\\\t]+(?P<present>\\\\w[\\\\w ]+)[ \\\\t]+(?P<reset>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modsel>\\\\w[\\\\w ]+)[ \\\\t]+(?P<modirq>\\\\w[\\\\w ]+)[ \\\\t]+(?P<lpmod>high mode)
    ...  command=./cel-port-test -c -t lpmod -D 1 -d
    ...  msg=Failed to verify one-by-one set "high mode"!


ALI_DIAG_TC041_GET_QSFP_TEMPERATURE
    [Tags]  ALI_DIAG_TC041_GET_QSFP_TEMPERATURE
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  5s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-qsfptemp-test
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=Get QSFP Temp.*?PASS
    ...  sec=420
    ...  msg=Failed, get QSFP temp failed!
    ...  is_check_exit_code=${FALSE}


## ALI_DIAG_TC042_SSD_TEST  ## Covered by ALI_DIAG_TC023_SATA_ACCESS_TEST


ALI_DIAG_TC043_TEST_ALL
    [Tags]    ALI_DIAG_TC043_TEST_ALL
    ...  migaloo

    Step  1   open prompt and login to root user  console=${openbmc_mode}
    Step  2   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=./check_info_tool.sh create
    ...  path=${openbmc_diag_utility_path}
    ...  msg=Failed to create the configuration!
    ...  sec=30
    Step  3   execute command and verify with unexpected patterns
    ...  console=${openbmc_mode}
    ...  command=./check_info_tool.sh
    ...  path=${openbmc_diag_utility_path}
    ...  patterns=${regularly_unexpected_patterns}
    ...  msg=Failed to check EEPROM configulation!
    ...  sec=30
    Step  4   open prompt and login to root user  console=${diagos_mode}
    Step  5   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./test_all.sh -m normal -f EVT1_cpu_test_all.cfg -M both
    ...  path=${diagos_diag_utility_path}
    ...  pattern=[ \\\\t]*Test all items[ \\\\t.\\\\[]+(?P<test_all_result>PASS)
    ...  sec=${25 * 60}  # 25 mins (typical 17 mins)


# ALI_DIAG_TC044_PRIMARY_FPGA_AND_GOLDEN_FPGA_FUNCTION_TEST Change to manual test


ALI_DIAG_TC045_INSIDE_CPLD_AND_OUTSIDE_CPLD_FUNCTION_TEST
    [Tags]  ALI_DIAG_TC045_INSIDE_CPLD_AND_OUTSIDE_CPLD_FUNCTION_TEST
    ...  migaloo
    ...  SHAMU_DIAG_TC041_INSIDE_CPLD_AND_OUTSIDE_CPLD_FUNCTION_TEST
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  ${diagos_mode}  AND
    ...  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  5s  AND  # Wait for some terrible I2C bus add messages
    ...  DiagOS renew IP using DHCP and set variable

    # TC_045_1
    Step  1   Wait for OpenBMC Info

    RUN KEYWORD IF  '${PLATFORM}' == 'migaloo'
    ...  Run Keywords  Step  2A   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=${diagos_show_diag_version_command}
    ...  patterns=${diagos_version_show_patterns}
    ...  msg=Failed to verify -S/show option!
    ...  sec=${5 * 60}  AND
    ...  search for a pattern
    ...  text=${text}
    ...  pattern=BaseBoard CPLD.*?${base_cpld_new_version}
    ...  msg=Failed, not found the basecpld version!

    ...  ELSE IF  '${PLATFORM}' == 'shamu'
    ...  Run Keywords  Step  2B   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -v
    ...  patterns=${cpld_v_patterns}
    ...  msg=Failed to verify -v/version option!
    ...  sec=${5 * 60}  AND
    ...  search for a pattern
    ...  text=${text}
    ...  pattern=Base.*?${base_cpld_new_version}
    ...  msg=Failed, not found the basecpld version!

    ...  ELSE
    ...  Log  Not to show base board CPLD for your platform!

    Step  2   secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${base_cpld_path}
    ...  source_file=${base_cpld_new_image}
    ...  destination=${base_cpld_save_to}
    Step  3  update_basecpld_flash
    # TC_045_2
    Step  4   power cycle to mode  mode=${diagos_mode}
    Sleep  120
    Step  5   Wait for OpenBMC Info

    RUN KEYWORD IF  '${PLATFORM}' == 'migaloo'
    ...  Run Keywords  Step  9A   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=${diagos_show_diag_version_command}
    ...  patterns=${diagos_version_show_patterns}
    ...  msg=Failed to verify -S/show option!
    ...  sec=${5 * 60}  AND
    ...  search for a pattern
    ...  text=${text}
    ...  pattern=Base.*?(0x06|0x0c)  # 0x06 is the golden version on earlier machines.
    ...  msg=Failed, not found the basecpld version!

    ...  ELSE IF  '${PLATFORM}' == 'shamu'
    ...  Run Keywords  Step  9B   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -v
    ...  patterns=${cpld_v_patterns}
    ...  msg=Failed to verify -v/version option!
    ...  sec=${5 * 60}  AND
    ...  search for a pattern
    ...  text=${text}
    ...  pattern=Base.*?0x5a
    ...  msg=Failed, not found the basecpld version!

    # TC_045_3
    Step  6  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${base_cpld_path}
    ...  source_file=${base_cpld_new_image}
    ...  destination=${base_cpld_save_to}
    Step  7  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${base_cpld_save_to}
    ...  command=ispvm -i 0 ${base_cpld_new_image}
    ...  pattern=(?P<result>PASS)
    ...  msg=Failed to program CPLD!
    Step  8  power cycle to mode  mode=${diagos_mode}
    Sleep  120
    Step  9  Wait for OpenBMC Info
    RUN KEYWORD IF  '${PLATFORM}' == 'migaloo'
    ...  Step  9A   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=${diagos_show_diag_version_command}
    ...  patterns=${diagos_version_show_patterns}
    ...  msg=Failed to verify -S/show option!
    ...  sec=${5 * 60}
    ...  ELSE IF  '${PLATFORM}' == 'shamu'
    ...  Step  9B   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -v
    ...  patterns=${cpld_v_patterns}
    ...  msg=Failed to verify -v/version option!
    ...  sec=${5 * 60}
    ...  ELSE
    ...  Log  Not to show base board CPLD for your platform!

    Step  10  Should Be Equal As Strings  ${matches}[baseboard_cpld]  ${diagos_base_cpld_new_version}
    ...  msg=Failed, after issued "wedge power script" for cycle the unit, the base board CPLD version does not matched new version!

    [Teardown]  Run Keywords
    ...  Run Keyword If Test Failed  powerCycleToOpenbmc  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=7


ALI_DIAG_TC046_CPU_FREQUENCY_TEST
    [Tags]  ALI_DIAG_TC046_CPU_FREQUENCY_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  5s  # Wait for some terrible I2C bus add messages

    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=./cel-cpu-frequency-test -h
    ...  patterns=${diagos_cpu_freq_help_patterns}
    ...  path=${diagos_cpu_diag_path}
    ...  msg=Failed to verify CPU frequency help option!
    Step  2   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-cpu-frequency-test -a
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=[ \\\\t]*CPU Frequency.*?(?P<result>PASS)


ALI_DIAG_TC047_RACK_TEST
    [Tags]  ALI_DIAG_TC047_RACK_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  5s  # Wait for some terrible I2C bus add messages

    Step  1   Verify all fan eeproms by eeprom tool
    Step  2   Verify all fan eeproms by FRU tool
    Step  3   execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -s
    ...  patterns=${regularly_unexpected_patterns}
    ...  path=${diagos_cpu_diag_path}
    ...  msg=Failed to verify by run the command!
    # Below step has comment for some needed manual step and found it be able run by automatic
    Step  4   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=Ali_Diag -m rack
    ...  path=${diagos_diag_utility_path}
    ...  pattern=[ \\\\t]*Test all items[ \\\\t.\\\\[]+(?P<test_all_result>PASS)
    ...  sec=108000  # 30 mins
    Step  5   EFI find boot order  console=${diagos_mode}  pattern=${efi_boot_order_pattern}
    Step  6   EFI whereof boot priority  console=${diagos_mode}  patterns=${efi_boot_whereof_patterns}
    Step  7   EFI compare boot order
    ...  boot_priority_higher=${efi_whereof}[sonic]
    ...  boot_priority_lower=${efi_whereof}[onie]
    ...  msg=Failed, SONiC boot priority is less than ONiE priority!


ALI_DIAG_TC048_BMC_I2C_DEVICE_TEST
    [Tags]  ALI_DIAG_TC048_BMC_I2C_DEVICE_TEST
    ...  migaloo

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-i2c-test -h
    ...  patterns=${openbmc_i2c_help_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify I2C help option!
    Step  2   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=./cel-i2c-test -s
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?m)^[ \\\\t]*All the I2C devices test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed to scan I2C device!
    ...  sec=90
    Step  3   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=./cel-i2c-test -l
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to list I2C device, the exit code is not zero!
    Step  4   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=./cel-i2c-test -a
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?m)^[ \\\\t]*All the I2C devices test[ \\\\t]+.*(?P<result>PASS)
    ...  msg=Failed to test all I2C device!
    ...  sec=90


ALI_DIAG_TC049_BMC_CPU_TEST
    [Tags]  ALI_DIAG_TC049_BMC_CPU_TEST
    ...  migaloo

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-CPU-test -h
    ...  patterns=${openbmc_cpu_help_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify CPU help option!
    Step  2   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=./cel-CPU-test -i
    ...  path=${openbmc_diag_bin_path}
    Step  3   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-CPU-test -a
    ...  patterns=${openbmc_cpu_i_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify -a option!


ALI_DIAG_TC050_MEMORY_TEST
    [Tags]  ALI_DIAG_TC050_MEMORY_TEST
    ...  migaloo
    ...  SHAMU_DIAG_TC059_MEMORY_TEST
    ...  shamu

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-memory-test -h
    ...  patterns=${memory_help_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify help option!
    Step  2   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=./cel-memory-test -i
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify -i option!
    Step  3   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${openbmc_mem_test_command}
    ...  pattern=${memory_a_pattern}
    ...  path=${openbmc_diag_bin_path}
    ...  sec=1200  # 20 mins (typically 11 mins)
    ...  msg=Failed to verify -a option or not found some pattern!


ALI_DIAG_TC051_EMMC_INFO_TEST
    [Tags]  ALI_DIAG_TC051_EMMC_INFO_TEST
    ...  migaloo

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-emmc-test -h
    ...  patterns=${emmc_help_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify help option!
    Step  2   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=./cel-emmc-test -i
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?m)[ \\\\t]*\\\\/dev\\\\/(?P<emmc_device0>\\\\w+): (?P<emmc_device0_mbytes>.*), (?P<emmc_device0_bytes>\\\\d+) bytes
    ...  msg=Failed not found the eMMC device and its size!
    Step  3   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=fdisk -l
    ...  pattern=(?m)[ \\\\t]*\\\\/dev\\\\/(?P<fdisk_device0>${match}[emmc_device0]):.*, (?P<fdisk_device0_bytes>${match}[emmc_device0_bytes]) bytes
    ...  msg=Failed not found the eMMC device or does not match for its name/size!
    Step  4   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=./cel-emmc-test -s
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?m)(?P<emmc_device0_mbytes>\\\\d+ \\\\wB)
    ...  msg=Failed, the size does not match!
    Step  5   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=./cel-emmc-test -a
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?m)^[ \\\\t]*check_emmc_size[ \\\\.]+.*(?P<result>PASS)
    ...  msg=Failed, the size does not match!


ALI_DIAG_TC052_BMC_CONTROL_COME_REBOOT_TEST
    [Tags]  ALI_DIAG_TC052_BMC_CONTROL_COME_REBOOT_TEST
    ...  migaloo
    [Setup]  change kernel log level  console=${openbmc_mode}  level=3

    # TC052-1
    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh --help
    ...  patterns=${diagos_wedge_power_patterns}
    ...  msg=Failed to verify help option!
    ...  is_check_exit_code=${FALSE}
    Step  2   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh status
    ...  pattern=Microserver power is (?P<microserver_status>.*)
    ...  msg=Failed, not found the current Microserver Power status!
    ...  is_check_exit_code=${FALSE}

    # TC052-2
    Step  3   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh off
    ...  pattern=(?i)Power.*?microserver.*?(?P<result>Done)
    ...  msg=Failed, not success to turn off the Microserver Power!
    ...  is_check_exit_code=${FALSE}
    Step  4   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh status
    ...  pattern=(?i)Microserver power is (?P<result>off)
    ...  msg=Failed, the Microserver Power is not off!
    ...  is_check_exit_code=${FALSE}
    Step  5   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh on
    ...  pattern=(?i)Power.*?microserver.*?(?P<result>Done)
    ...  msg=Failed, not success to turn on the Microserver Power!
    ...  is_check_exit_code=${FALSE}
    Step  6   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh status
    ...  pattern=(?i)Microserver power is (?P<result>on)
    ...  msg=Failed, the Microserver Power is not on!
    ...  is_check_exit_code=${FALSE}

    # TC052-3
    Step  7   OpenBMC wedge power script  action=cycle
    Step  8   open prompt  ${openbmc_mode}  sec=10

    # TC052-4
    Step  9   OpenBMC wedge power script  action=reset
    Step  10  open prompt  ${openbmc_mode}  sec=10
    [Teardown]  Run Keywords
    ...  recover cpu  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7

ALI_DIAG_TC053_RTC_TEST
    [Tags]  ALI_DIAG_TC053_RTC_TEST
    ...  migaloo

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-RTC-test -h
    ...  patterns=${option_h_and_a_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify help option!
    Step  2   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=./cel-RTC-test -a
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=^[ \\\\t]*RTC Test[ \\\\.]+.*(?P<result>PASS)
    ...  msg=Failed to test RTC!


ALI_DIAG_TC054_BMC_SWITCH_MASTER_SLAVE_BIOS_TEST
    [Tags]  ALI_DIAG_TC054_BMC_SWITCH_MASTER_SLAVE_BIOS_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  force to switch BIOS boot source
    ...  switch_to_pattern=Master flash
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && come_reset master)  AND
    ...  open prompt and login to root user  console=${openbmc_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   force to switch BIOS boot source
    ...  switch_to_pattern=Slave flash
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && come_reset slave)
    open prompt and login to root user  console=${openbmc_mode}
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    Sleep  45s  # Wait for some terrible I2C bus add messages
    Step  2   force to switch BIOS boot source
    ...  switch_to_pattern=Master flash
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && come_reset master)
    open prompt and login to root user  console=${openbmc_mode}
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    Sleep  45s  # Wait for some terrible I2C bus add messages

    [Teardown]  force to switch BIOS boot source
    ...  switch_to_pattern=Master flash
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && come_reset master)


ALI_DIAG_TC055_BMC_SWITCH_MASTER_SLAVE_BMC_TEST
    [Tags]  ALI_DIAG_TC055_BMC_SWITCH_MASTER_SLAVE_BMC_TEST
    ...  migaloo

    # Awlays start with master boot
    [Setup]  Run Keywords
    ...  force to switch boot source
    ...  switch_to_pattern=Master Flash
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && boot_from master)  AND
    ...  open prompt and login to root user  console=${openbmc_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1   force to switch boot source
    ...  switch_to_pattern=Slave Flash
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && boot_from slave)
    open prompt and login to root user  console=${openbmc_mode}
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    Sleep  45s  # Wait for some terrible I2C bus add messages
    Step  2   force to switch boot source
    ...  switch_to_pattern=Master Flash
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && boot_from master)
    open prompt and login to root user  console=${openbmc_mode}
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    Sleep  45s  # Wait for some terrible I2C bus add messages

    # Set back to master boot please
    [Teardown]  Run Keywords
    ...  force to switch boot source
    ...  switch_to_pattern=Master Flash
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && boot_from master)  AND
    ...  open prompt and login to root user  console=${openbmc_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages


ALI_DIAG_TC056_TEMPERATURE_SENSOR_TEST
    [Tags]  ALI_DIAG_TC056_TEMPERATURE_SENSOR_TEST
    ...  migaloo
    ...  SHAMU_DIAG_TC058_TEMPERATURE_TEST
    ...  shamu

    # Have discussed with Lagune Qi for how to compare the two commands,
    # ("cel-temperature-test -a" and "sensors")
    # cause the sensor has a bit different name and its value is changing all the time,
    # read it after second(s) may not the same, cannot identify to match for both command,
    # he let me ask the automate team, if it too much complicated for auto-check,
    # rather than the manual-check, it depends on us for how to.
    #
    # In my opinion, we check for an exit code zero and find for the fail pattern to
    # detect the unexpected condition, that is should cover all.
    #
    # An example:
    # $ cel-temperature-test -a
    # ...
    # TMP275-i2c-42-0x4c
    # TPM275-i2c-44-0x48
    # ...
    #
    # $ sensors
    # ...
    # tmp75-i2c-42-4c
    # tmp75-i2c-44-48
    # ...

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-temperature-test -h
    ...  patterns=${temp_sensor_help_patterns}
    ...  path=/var/log/BMC_Diag/bin
    ...  msg=Failed to verify this command output!
    Step  2   execute command and verify with a pattern for table
    ...  console=${openbmc_mode}
    ...  command=${openbmc_show_temp_sensor_command}
    ...  pattern=${temp_sensor_pattern}
    ...  msg=Not found any sensor name!
    # The above command shows failed, but return exit code zero!
    Step  3   search for a pattern
    ...  text=${text}
    ...  pattern=${temp_overall_test_pattern}
    ...  msg=Failed, should not found the FAIL pattern!
    Step  4   execute command and verify with a pattern for table
    ...  console=${openbmc_mode}
    ...  command=sensors
    ...  pattern=${temp_sensor_pattern}
    ...  msg=Failed, not found any sensor name!


ALI_DIAG_TC057_FIRMWARE_SOFTWARE_VERSION_TEST
    [Tags]  ALI_DIAG_TC057_FIRMWARE_SOFTWARE_VERSION_TEST
    ...  migaloo

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-software-test -h
    ...  patterns=${sw_help_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify help option!
    Step  2   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-software-test -a
    ...  patterns=${sw_a_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify -a option!


ALI_DIAG_TC058_PECI_BUS_TEST
    [Tags]  ALI_DIAG_TC058_PECI_BUS_TEST
    ...  migaloo
    ...  SHAMU_DIAG_TC064_PCIE_TEST
    ...  shamu

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-peci-test -h
    ...  patterns=${option_h_and_a_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify help option!
    Step  2   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${openbmc_peci_test_command}
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=^[ \\\\t]*check_peci_access[ \\\\.]+.*(?P<result>PASS)
    ...  msg=Failed to test PCIe!


ALI_DIAG_TC059_SOL_TEST
    [Tags]  ALI_DIAG_TC059_SOL_TEST
    ...  migaloo
    ...  SHAMU_DIAG_TC071_SOL_TEST
    ...  shamu

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-sol-test -h
    ...  patterns=${option_h_and_a_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify help option!
    Step  2   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${openbmc_sol_test_command}
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=^[ \\\\t]*SOL Test[ \\\\.]+.*(?P<result>PASS)
    ...  msg=Failed to test SOL!


ALI_DIAG_TC060_POWER_MONITOR_TEST
    [Tags]  ALI_DIAG_TC060_POWER_MONITOR_TEST
    ...  migaloo

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-software-test -h
    ...  patterns=${pow_help_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify help option!
    Step  2   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=./cel-power-monitor-test -a
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=^[ \\\\t]*Power monitor test[ .]+\\\\[[ \\\\t]*PASS
    ...  msg=Failed not found the overall pass pattern!


ALI_DIAG_TC061_OOB_TEST
    [Tags]  ALI_DIAG_TC061_OOB_TEST
    ...  migaloo
    ...  SHAMU_DIAG_TC060_OOB_TEST
    ...  shamu

    Step  1   OOB menu/help verify
    Step  2   OOB menu/auto-test


ALI_DIAG_TC065_BMC_MAC_TEST
    [Tags]  ALI_DIAG_TC065_BMC_MAC_TEST
    ...  migaloo
    ...  SHAMU_DIAG_TC072_BMC_MAC_TEST
    ...  shamu

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=./cel-MAC-test -h
    ...  patterns=${option_h_and_a_patterns}
    ...  path=${openbmc_diag_bin_path}
    ...  msg=Failed to verify help option!
    Step  2   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${openbmc_bmc_mac_test_command}
    ...  pattern=^[ \\\\t]*BMC mac Test[ \\\\.]+.*(?P<result>PASS)
    ...  msg=Failed not found the pass pattern!


ALI_DIAG_TC066_COME_CPU_STRESS_TEST
    [Tags]  ALI_DIAG_TC066_COME_CPU_STRESS_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  AND  # Wait for some terrible I2C bus add messages
    ...  send a line  command=${KEY_CTRL_C}

    Step   1  remove file/folder
    ...  console=${diagos_mode}
    ...  file=${diagos_diag_utility_stress_path}/CPU_test.log
    Step   2  send a line  command=${diagos_diag_utility_stress_path}/CPU_test.sh
    Step   3  Sleep  ${diagos_tc066_cpu_test_time}
    Step   4  send a line  command=${KEY_CTRL_C}
    Step   5  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_stress_path}
    ...  command=(cat ./CPU_test.log | grep -E "errors|warnings")
    ...  patterns=${diagos_cpu_stress_unexpected_patterns}
    ...  msg=Failed, should not found and error and/or warning message(s)!


ALI_DIAG_TC067_COME_DDR_STRESS_TEST
    [Tags]  ALI_DIAG_TC067_COME_DDR_STRESS_TEST
    ...  migaloo
    ...  SHAMU_DIAG_TC035_DDR_STRESS_TEST
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  5s  # Wait for some terrible I2C bus add messages

    Step   1  remove file/folder
    ...  console=${diagos_mode}
    ...  file=${diagos_diag_utility_stress_path}/CPU_test.log
    Step   2  execute command and verify with a pattern
    ...  path=${diagos_diag_utility_stress_path}
    ...  console=${diagos_mode}
    ...  command=./DDR_test.sh ${diagos_tc067_come_ddr_time} ${diagos_tc067_come_ddr_size}
    ...  pattern=Status: (?P<result>PASS)
    ...  msg=Failed not found the pass pattern!
    ...  sec=${${diagos_tc067_come_ddr_time} + 15}
    Step   3  execute command and verify with unexpected patterns
    ...  path=${diagos_diag_utility_stress_path}
    ...  console=${diagos_mode}
    ...  command=cat DDR_stress_test.log
    ...  patterns=${diagos_come_ddr_stress_patterns}
    ...  msg=Failed, found error/warning message(s)!${\n}Please see the log file for more detail!

    [Teardown]  Run Keywords
    ...  send a line  command=\x03  # Ctrl-C
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=killall -9 DDR_test.sh
    ...  is_check_exit_code=${FALSE}
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=killall -9 stressapptest
    ...  is_check_exit_code=${FALSE}


ALI_DIAG_TC068_COME_SSD_STRESS_TEST
    [Tags]  ALI_DIAG_TC068_COME_SSD_STRESS_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step   1  remove file/folder
    ...  console=${diagos_mode}
    ...  file=${diagos_diag_utility_stress_path}/SSD.log
    Step   2  execute command and verify with a pattern
    ...  path=${diagos_diag_utility_stress_path}
    ...  console=${diagos_mode}
    ...  command=./SSD_test.sh ${diagos_tc068_come_ssd_time} SSD.log
    ...  pattern=SSD test (?P<result>done).
    ...  msg=Failed not found the test result done!
    ...  sec=${${diagos_tc068_come_ssd_time} * 5}  # The execution time is not calculable the number! Always 8 minutes and around 15 seconds
    Step   3  execute command and verify with unexpected patterns
    ...  path=${diagos_diag_utility_stress_path}
    ...  console=${diagos_mode}
    ...  command=(cat SSD.log | grep -E "Fail|fail|Error|error" | wc -l)
    ...  patterns=(?m)^(?P<error>[^0a-zA-Z]+)$
    ...  msg=Failed, should not found any error/warning/fail message(s)!${\n}Please see the log file for more detail!


ALI_DIAG_TC069_OPENBMC_DDR_STRESS_TEST
    [Tags]  ALI_DIAG_TC069_OPENBMC_DDR_STRESS_TEST
    ...  migaloo

    Step   1  remove file/folder
    ...  console=${openbmc_mode}
    ...  file=${openbmc_diag_utility_stress_path}/DDR_stress_test.log
    Step   2  execute command and verify exit code
    ...  path=${openbmc_diag_utility_stress_path}
    ...  console=${openbmc_mode}
    ...  command=./DDR_test.sh ${openbmc_tc069_ddr_stress_time} ${openbmc_tc069_ddr_stress_size}
    ...  msg=Failed not found the pass pattern!
    ...  sec=${${openbmc_tc069_ddr_stress_time} + 20}
    Step   3  execute command and verify with unexpected patterns
    ...  path=${openbmc_diag_utility_stress_path}
    ...  console=${openbmc_mode}
    ...  command=cat DDR_stress_test.log
    ...  patterns=${openbmc_ddr_stress}
    ...  msg=Failed, found error/warning message(s)!${\n}Please see the log file for more detail!


ALI_DIAG_TC070_I2C_STRESS_TEST
    [Tags]  ALI_DIAG_TC070_I2C_STRESS_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  5s  # Wait for some terrible I2C bus add messages

    Step   1  remove file/folder
    ...  console=${diagos_mode}
    ...  file=${diagos_diag_utility_stress_path}/qsfp/{*.log,current_information_1*}
    Step   2  set terminal auto-logout timeout  console=${diagos_mode}
    Step   3  execute command and verify with unexpected patterns
    ...  path=${diagos_diag_utility_stress_path}/qsfp
    ...  console=${diagos_mode}
    ...  command=(source ./run_i2cdump_stress.sh 20 && wait)
    ...  patterns=${diagos_i2c_stress_unexpected_patterns}
    ...  sec=${6 * 60 * 60 }  # 6 hours
    Step   4  execute command and verify with unexpected patterns
    ...  path=${diagos_diag_utility_stress_path}/qsfp
    ...  console=${diagos_mode}
    ...  command=(cat current_information_1* | grep -E "Fail|fail|Error|error" | wc -l)
    ...  patterns=(?m)^(?P<found_zero>0)$  # 0 is not found any fail message
    ...  msg=Failed, should not found any error/warning/fail message(s) by grep!${\n}Please see the log file for more detail!


ALI_DIAG_TC071_EMMC_STRESS_TEST
    [Tags]  ALI_DIAG_TC071_EMMC_STRESS_TEST
    ...  migaloo  long_time

    Step   1  execute command and verify with a pattern
    ...  path=${openbmc_diag_utility_stress_path}
    ...  console=${openbmc_mode}
    ...  command=./emmc_stress_test.sh -t
    ...  pattern=EMMC writing/reading test Pass
    ...  msg=Failed not found the test result done!
    ...  sec=5400

    [Teardown]  Run Keyword And Ignore Error  execute command and verify exit code
    ...  path=${openbmc_diag_utility_stress_path}
    ...  console=${openbmc_mode}
    ...  command=./emmc_stress_test.sh -c


ALI_DIAG_TC072_TH4_PCIE_STRESS_TEST
    [Tags]  ALI_DIAG_TC072_TH4_PCIE_STRESS_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  AND  # Wait for some terrible I2C bus add messages
    ...  execute command and verify exit code
    ...  path=${diagos_sdk_path}
    ...  console=${diagos_mode}
    ...  command=pkill bcm.user
    ...  exit_code_pattern=(?m)^(?P<exit_code>\\d+)$

    Step   1  send a line  command=./auto_load_user.sh
    Step   2  read until regexp  patterns=BCM.0>  timeout=120
    Step   3  send a line  command=dsh
    Step   4  read until regexp  patterns=sdklt.0>  timeout=60
    Step   5  send a line  command=test run 502.0
    Step   6  read until regexp  patterns=sdklt.0>  timeout=60
    Step   7  send a line  command=test list 502.0
    Step   8  read until regexp  patterns=sdklt.0>  timeout=600
    Step   9  send a line  command=quit
    Step  10  verify SDK pass count
    Step  11  send a line  command=quit
    Step  10  read until regexp  patterns=root@  timeout=60


ALI_DIAG_TC073_OPTICAL_MIDULES_STRESS_TEST
    [Tags]  ALI_DIAG_TC073_OPTICAL_MIDULES_STRESS_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  AND  # Wait for some terrible I2C bus add messages
    ...  remove file/folder
    ...  console=${diagos_mode}
    ...  file=/tmp/sfputil_*\\\\.txt

    Step   1  execute command and verify exit code
    ...  path=/tmp
    ...  console=${diagos_mode}
    ...  command=(sfputil show presence 2>&1 >> sfputil_present_1.txt & sfputil show eeprom --raw 2>&1 >> sfputil_eeprom_1.txt & sfputil show presence 2>&1 >> sfputil_present_2.txt & sfputil show eeprom --raw 2>&1 >> sfputil_eeprom_2.txt & sfputil show presence 2>&1 >> sfputil_present_3.txt & sfputil show eeprom --raw 2>&1 >> sfputil_eeprom_3.txt & sfputil show presence 2>&1 >> sfputil_present_4.txt & sfputil show eeprom --raw 2>&1 >> sfputil_eeprom_4.txt & sfputil show presence 2>&1 >> sfputil_present_5.txt & sfputil show eeprom --raw 2>&1 >> sfputil_eeprom_5.txt & sfputil show presence 2>&1 >> sfputil_present_6.txt & sfputil show eeprom --raw 2>&1 >> sfputil_eeprom_6.txt & sfputil show presence 2>&1 >> sfputil_present_7.txt & sfputil show eeprom --raw 2>&1 >> sfputil_eeprom_7.txt & sfputil show presence 2>&1 >> sfputil_present_8.txt & sfputil show eeprom --raw 2>&1 >> sfputil_eeprom_8.txt & sfputil show presence 2>&1 >> sfputil_present_9.txt & sfputil show eeprom --raw 2>&1 >> sfputil_eeprom_9.txt & sfputil show presence 2>&1 >> sfputil_present_10.txt & sfputil show eeprom --raw 2>&1 >> sfputil_eeprom_10.txt & wait)
    ...  sec=${10 * 60}

    # Check for all "sfputil show presence"
    Step   2  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=cat sfputil_present_1.txt
    ...  patterns=${diagos_sfputil_show_presence_unexpected_patterns}
    ...  msg=Failed, sfputil_present_1.txt: Some of ethernet not present${\n}Please see the log file for more details
    Step   3  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=cat sfputil_present_2.txt
    ...  patterns=${diagos_sfputil_show_presence_unexpected_patterns}
    ...  msg=Failed, sfputil_present_2.txt: Some of ethernet not present${\n}Please see the log file for more details
    Step   4  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=cat sfputil_present_3.txt
    ...  patterns=${diagos_sfputil_show_presence_unexpected_patterns}
    ...  msg=Failed, sfputil_present_3.txt: Some of ethernet not present${\n}Please see the log file for more details
    Step   5  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=cat sfputil_present_4.txt
    ...  patterns=${diagos_sfputil_show_presence_unexpected_patterns}
    ...  msg=Failed, sfputil_present_4.txt: Some of ethernet not present${\n}Please see the log file for more details
    Step   6  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=cat sfputil_present_5.txt
    ...  patterns=${diagos_sfputil_show_presence_unexpected_patterns}
    ...  msg=Failed, sfputil_present_5.txt: Some of ethernet not present${\n}Please see the log file for more details
    Step   7  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=cat sfputil_present_6.txt
    ...  patterns=${diagos_sfputil_show_presence_unexpected_patterns}
    ...  msg=Failed, sfputil_present_6.txt: Some of ethernet not present${\n}Please see the log file for more details
    Step   8  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=cat sfputil_present_7.txt
    ...  patterns=${diagos_sfputil_show_presence_unexpected_patterns}
    ...  msg=Failed, sfputil_present_7.txt: Some of ethernet not present${\n}Please see the log file for more details
    Step   9  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=cat sfputil_present_8.txt
    ...  patterns=${diagos_sfputil_show_presence_unexpected_patterns}
    ...  msg=Failed, sfputil_present_8.txt: Some of ethernet not present${\n}Please see the log file for more details
    Step  10  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=cat sfputil_present_9.txt
    ...  patterns=${diagos_sfputil_show_presence_unexpected_patterns}
    ...  msg=Failed, sfputil_present_9.txt: Some of ethernet not present${\n}Please see the log file for more details
    Step  11  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=cat sfputil_present_10.txt
    ...  patterns=${diagos_sfputil_show_presence_unexpected_patterns}
    ...  msg=Failed, sfputil_present_10.txt: Some of ethernet not present${\n}Please see the log file for more details

    # check for all "sfputil show eeprom --raw"
    Step  12  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=grep -i ethernet sfputil_eeprom_1.txt
    ...  patterns=${diagos_sfputil_show_eeprom_raw_unexpected_patterns}
    ...  msg=Failed, sfputil_present_1.txt: Some of ethernet not detected${\n}Please see the log file for more details
    Step  13  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=grep -i ethernet sfputil_eeprom_2.txt
    ...  patterns=${diagos_sfputil_show_eeprom_raw_unexpected_patterns}
    ...  msg=Failed, sfputil_present_2.txt: Some of ethernet not detected${\n}Please see the log file for more details
    Step  14  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=grep -i ethernet sfputil_eeprom_3.txt
    ...  patterns=${diagos_sfputil_show_eeprom_raw_unexpected_patterns}
    ...  msg=Failed, sfputil_present_3.txt: Some of ethernet not detected${\n}Please see the log file for more details
    Step  15  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=grep -i ethernet sfputil_eeprom_4.txt
    ...  patterns=${diagos_sfputil_show_eeprom_raw_unexpected_patterns}
    ...  msg=Failed, sfputil_present_4.txt: Some of ethernet not detected${\n}Please see the log file for more details
    Step  16  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=grep -i ethernet sfputil_eeprom_5.txt
    ...  patterns=${diagos_sfputil_show_eeprom_raw_unexpected_patterns}
    ...  msg=Failed, sfputil_present_5.txt: Some of ethernet not detected${\n}Please see the log file for more details
    Step  17  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=grep -i ethernet sfputil_eeprom_6.txt
    ...  patterns=${diagos_sfputil_show_eeprom_raw_unexpected_patterns}
    ...  msg=Failed, sfputil_present_6.txt: Some of ethernet not detected${\n}Please see the log file for more details
    Step  18  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=grep -i ethernet sfputil_eeprom_7.txt
    ...  patterns=${diagos_sfputil_show_eeprom_raw_unexpected_patterns}
    ...  msg=Failed, sfputil_present_7.txt: Some of ethernet not detected${\n}Please see the log file for more details
    Step  19  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=grep -i ethernet sfputil_eeprom_8.txt
    ...  patterns=${diagos_sfputil_show_eeprom_raw_unexpected_patterns}
    ...  msg=Failed, sfputil_present_8.txt: Some of ethernet not detected${\n}Please see the log file for more details
    Step  20  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=grep -i ethernet sfputil_eeprom_9.txt
    ...  patterns=${diagos_sfputil_show_eeprom_raw_unexpected_patterns}
    ...  msg=Failed, sfputil_present_9.txt: Some of ethernet not detected${\n}Please see the log file for more details
    Step  21  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=grep -i ethernet sfputil_eeprom_10.txt
    ...  patterns=${diagos_sfputil_show_eeprom_raw_unexpected_patterns}
    ...  msg=Failed, sfputil_present_10.txt: Some of ethernet not detected${\n}Please see the log file for more details
