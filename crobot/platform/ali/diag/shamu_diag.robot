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

*** Test Cases ***
SHAMU_DIAG_TC002_Update_FPGA_Image
     [Tags]  SHAMU_DIAG_TC002_Update_FPGA_Image  shamu
     Step  1  open prompt and login to root user  console=${diagos_mode}
     step  2  change dir  ${diagos_cpu_diag_path}
     step  3  fpga test option h
     step  4  fpga test option v
     step  5  download image  DUT  FPGA  upgrade=${FALSE}
     step  6  change dir  /tmp/
     step  7  update fpga version  old
     step  8  powerCycleToOpenbmc
     step  9  open prompt and login to root user  console=${diagos_mode}
     step  10  change dir  ${diagos_cpu_diag_path}
     step  11  check fpga old version
     step  12  download image  DUT  FPGA  upgrade=${TRUE}
     step  13  change dir  /tmp/
     step  14  update fpga version  new
     step  15  powerCycleToOpenbmc
     step  16  open prompt and login to root user  console=${diagos_mode}
     step  17  change dir  ${diagos_cpu_diag_path}
     step  18  Check current fpga version


SHAMU_DIAG_TC003_UPDATE_CPLD_IMAGE
     [Tags]  SHAMU_DIAG_TC003_UPDATE_CPLD_IMAGE  shamu
     Step  1  open prompt and login to root user  console=${diagos_mode}
     step  2  change dir  ${diagos_cpu_diag_path}
     step  3  cpld test option h
     step  4  cpld test option v
     step  5  create dir  /tmp/CPLD/  ${diagos_mode}
     step  6  download cpld image version  ${FALSE}
     step  7  change dir  /tmp/CPLD/
     step  8  update cpld image version  old
     step  9  powerCycleToOpenbmc
     step  10  open prompt and login to root user  console=${diagos_mode}
     step  11  Sleep  300s
     step  12  change dir  ${diagos_cpu_diag_path}
     step  13  check cpld image version  old
     step  14  create dir  /tmp/CPLD/  ${diagos_mode}
     step  15  download cpld image version  ${TRUE}
     step  16  change dir  /tmp/CPLD/
     step  17  update cpld image version  new
     step  18  powerCycleToOpenbmc
     step  19  open prompt and login to root user  console=${diagos_mode}
     step  20  Sleep  300s
     step  21  change dir  ${diagos_cpu_diag_path}
     step  22  check cpld image version  new


SHAMU_DIAG_TC004_UPDATE_OPENBMC_IMAGE
     [Tags]  SHAMU_DIAG_TC004_UPDATE_OPENBMC_IMAGE  shamu

#### begin downgrade master
     step  1  open prompt and login to root user  console=${openbmc_mode}
     step  2  change dir  ${openbmc_diag_bin_path}
     step  3  software test option h
     step  4  software test option i  upgrade=${TRUE}
     step  5  check boot status  Master
     step  6  open prompt and login to root user  console=${diagos_mode}
     step  7  change dir  /tmp
     step  8  execute command  mkdir BMC
     step  8  check ip address  DUT  eth0
     step  9  download image  DUT  BMC  upgrade=${FALSE}
     step  10  change dir  BMC/
     step  11  chmod download image  old
     step  12  update bmc image version  old
     step  13  powerCycleToOpenbmc
     step  14  open prompt and login to root user  console=${openbmc_mode}
     step  15  change dir  ${openbmc_diag_bin_path}
     step  16  software test option i
     step  17  check boot status  Master

#### begin downgrade slave
     step  18  boot from slave openbmc
     step  19  check boot status  Slave
     step  20  open prompt and login to root user  console=${diagos_mode}
     step  21  execute command  mkdir /tmp/BMC
     step  21  check ip address  DUT  eth0
     step  22  download image  DUT  BMC  upgrade=${FALSE}
     step  24  change dir  /tmp/BMC/
     step  25  chmod download image  old
     step  26  update bmc image version  old  update_master=${FALSE}
     step  27  powerCycleToOpenbmc
     step  28  boot from slave openbmc  ## this step is a must, AC power will always boot up with master bios/bmc
     step  29  change dir  ${openbmc_diag_bin_path}
     step  30  software test option i
     step  31  check boot status  Slave

### begin upgrade slave
     step  32  open prompt and login to root user  console=${diagos_mode}
     step  33  execute command  mkdir /tmp/BMC
     step  33  check ip address  DUT  eth0
     step  34  download image  DUT  BMC  upgrade=${TRUE}
     step  35  change dir  /tmp/BMC/
     step  36  chmod download image  new
     step  37  update bmc image version  new  update_master=${FALSE}
     step  38  powerCycleToOpenbmc
     step  39  boot from slave openbmc
     step  40  change dir  ${openbmc_diag_bin_path}
     step  41  software test option i  upgrade=${TRUE}
     step  42  check boot status  Slave

#### begin upgrade master
     step  43  boot from master openbmc
     step  44  check boot status  Master
     step  45  open prompt and login to root user  console=${diagos_mode}
     step  46  execute command  mkdir /tmp/BMC
     step  46  check ip address  DUT  eth0
     step  47  download image  DUT  BMC  upgrade=${TRUE}
     step  48  change dir  /tmp/BMC/
     step  49  chmod download image  new
     step  50  update bmc image version  new  update_master=${TRUE}
     step  51  powerCycleToOpenbmc
     step  52  open prompt and login to root user  console=${openbmc_mode}
     step  53  change dir  ${openbmc_diag_bin_path}
     step  54  software test option i  upgrade=${TRUE}
     step  55  check boot status  Master


SHAMU_DIAG_TC005_TLV_EEPROM_UPDATE
    [Tags]  SHAMU_DIAG_TC005_TLV_EEPROM_UPDATE
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  Step  x  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -d
    ...  patterns=${diagos_tlv_eeprom_tool_d_patterns}
    ...  msg=Failed, not found one or more pattern(s) for TLV EEPROM TOOL!
    ...  AND  set test variable  ${tlv_eeprom_1st}  ${matches}
    ...  AND  move file/folder
    ...  console=${diagos_mode}
    ...  source=${diagos_cpu_tlv_eeprom_path}/eeprom.bin
    ...  destination=${diagos_cpu_tlv_eeprom_path}/eeprom-setup.bin

    Step   1  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x21=AS14-40D-F"
    ...  msg=Failed to write by EEPROM Tool!
    Step   2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x22=R3130-F9001-01"
    ...  msg=Failed to write by EEPROM Tool!
    Step   3  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x23=9876543210"
    ...  msg=Failed to write by EEPROM Tool!
    Step   4  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x24=20:58:9D:9C:48:D4"
    ...  msg=Failed to write by EEPROM Tool!
    Step   5  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x25=01/01/2099 00:00:00"
    ...  msg=Failed to write by EEPROM Tool!
    Step   6  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x26=99"
    ...  msg=Failed to write by EEPROM Tool!
    Step   7  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x27=Shamu"
    ...  msg=Failed to write by EEPROM Tool!
    Step   8  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x28=0x86_64-alibaba_as14-40d-cl-r0"
    ...  msg=Failed to write by EEPROM Tool!
    Step   9  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x29=9.9.9"
    ...  msg=Failed to write by EEPROM Tool!
    Step  10  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2a=02"
    ...  msg=Failed to write by EEPROM Tool!
    Step  11  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2b=CELESTICA"
    ...  msg=Failed to write by EEPROM Tool!
    Step  12  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2c=CHN"
    ...  msg=Failed to write by EEPROM Tool!
    Step  13  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2d=ALIBABA"
    ...  msg=Failed to write by EEPROM Tool!
    Step  14  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2e=9.9.9"
    ...  msg=Failed to write by EEPROM Tool!
    Step  15  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2f=PRODUCT-TYPE"
    ...  msg=Failed to write by EEPROM Tool!
    Step  16  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0xfd=0"
    ...  msg=Failed to write by EEPROM Tool!

    Step  17  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -u
    ...  msg=Failed to write by EEPROM Tool!
    ...  sec=${3 * 60}

    Step  18  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -d
    ...  patterns=${diagos_tlv_eeprom_tool_d_patterns}
    ...  msg=Failed, not found one or more pattern(s) for TLV EEPROM TOOL!
    set test variable  ${tlv_eeprom_2nd}  ${matches}

    Step  19  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${EMPTY}
    ...  command=show platform syseeprom
    ...  patterns=${diagos_tlv_sonic_syseeprom_patterns}
    ...  msg=Failed, not found one or more pattern(s) for TLV EEPROM TOOL!
    set test variable  ${tlv_eeprom_sonic_1st}  ${matches}

    Step  20  compare two dictionaries with matched key
    ...  original=${tlv_eeprom_2nd}
    ...  compare=${tlv_eeprom_sonic_1st}
    ...  msg=Failed to compare the TLV EEPROM after write/read back by "eeprom_tool" and "SONiC Platform"!

    Step  21  powerCycleToOpenbmc
    open prompt and login to root user  console=${diagos_mode}

    Step  22  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -d
    ...  patterns=${diagos_tlv_eeprom_tool_d_patterns}
    ...  msg=Failed, not found one or more pattern(s) for TLV EEPROM TOOL!
    set test variable  ${tlv_eeprom_3rd}  ${matches}

    Step  23  compare two dictionaries with matched key
    ...  original=${tlv_eeprom_2nd}
    ...  compare=${tlv_eeprom_3rd}
    ...  msg=Failed to compare the TLV EEPROM after write/read back by "eeprom_tool"!

    [Teardown]  Run Keywords
    ...  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x21=${tlv_eeprom_1st}[addr_0x21]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x22=${tlv_eeprom_1st}[addr_0x22]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x23=${tlv_eeprom_1st}[addr_0x23]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x24=${tlv_eeprom_1st}[addr_0x24]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x25=${tlv_eeprom_1st}[addr_0x25]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x26=${tlv_eeprom_1st}[addr_0x26]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x27=${tlv_eeprom_1st}[addr_0x27]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x28=${tlv_eeprom_1st}[addr_0x28]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x29=${tlv_eeprom_1st}[addr_0x29]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2a=${tlv_eeprom_1st}[addr_0x2a]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2b=${tlv_eeprom_1st}[addr_0x2b]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2c=${tlv_eeprom_1st}[addr_0x2c]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2d=${tlv_eeprom_1st}[addr_0x2d]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2e=${tlv_eeprom_1st}[addr_0x2e]"
    ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -w "0x2f=${tlv_eeprom_1st}[addr_0x2f]"
    ...  msg=Failed to write by EEPROM Tool!
    # "0x01" != ""
    # ...  AND  execute command and verify exit code
    # ...  console=${diagos_mode}
    # ...  path=${diagos_cpu_tlv_eeprom_path}
    # ...  command=./eeprom_tool -w "0xfd=${tlv_eeprom_1st}[addr_0xfd]"
    # ...  msg=Failed to write by EEPROM Tool!
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_tlv_eeprom_path}
    ...  command=./eeprom_tool -u
    ...  msg=Failed to write by EEPROM Tool!
    ...  sec=${3 * 60}
    ...  AND  powerCycleToOpenbmc


SHAMU_DIAG_TC007_MANAGEMENT_ETHER_PORT_MAC_UPDATE
    [Tags]  SHAMU_DIAG_TC007_MANAGEMENT_ETHER_PORT_MAC_UPDATE
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3
    ...  AND  Sleep  45s  # Wait for some terrible I2C bus add messages
    ...  AND  show network interface IP  console=${diagos_mode}  interface=eth0  pattern=(?m)^ +link\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    ...  AND  set test variable  &{ifconfig_eth0_nic5_mac_original}  &{matches}

    Step   1  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=5 /MAC_DUMP
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to dump MAC for eth0/NIC=5!
    ...  is_check_exit_code=${FALSE}
    search for a pattern
    ...  text=${text}
    ...  pattern=(?mi)[ \\t]*\\d+\\: LAN MAC Address is (?P<mac>[0-9a-fA-F]{12})
    ...  msg=Failed, not found the MAC address!
    set test variable  ${eeupdate64e_eth0_nic5_mac_original_str}  ${match}[mac]

    ${ifconfig_eth0_nic5_mac_original_str}=  Replace String
    ...  string=${ifconfig_eth0_nic5_mac_original}[mac_1]
    ...  search_for=:
    ...  replace_with=

    Step   2  Should Be Equal As Strings
    ...  first=${ifconfig_eth0_nic5_mac_original_str}
    ...  second=${eeupdate64e_eth0_nic5_mac_original_str}
    ...  msg=Failed, the written MAC/eth0 does not match for ifconfig and eeupdate64e!
    ...  ignore_case=${TRUE}

    Step   3  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=5 /MAC=${diagos_eeupdate64e_mac}[base]
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to write MAC for eth0/NIC=5!
    ...  is_check_exit_code=${FALSE}
    search for a pattern
    ...  text=${text}
    ...  pattern=(?mi)[ \\t]*\\d+\\: Updating Mac Address to (?P<mac>[0-9a-fA-F]{12}).*Done
    ...  msg=Failed, not found the MAC address!
    set test variable  ${eeupdate64e_eth0_nic5_mac_before_reboot_str}  ${match}[mac]

    Step   4  powerCycleToOpenbmc
    Step   5  open prompt and login to root user  console=${diagos_mode}
    Step   6  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3
    Step   7  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step   8  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=5 /MAC_DUMP
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to dump MAC for eth0/NIC=5!
    ...  is_check_exit_code=${FALSE}
    search for a pattern
    ...  text=${text}
    ...  pattern=(?mi)[ \\t]*\\d+\\: LAN MAC Address is (?P<mac>[0-9a-fA-F]{12})
    ...  msg=Failed, not found the MAC address!
    set test variable  ${eeupdate64e_eth0_nic5_mac_after_reboot_str}  ${match}[mac]

    Step   9  Should Be Equal As Strings
    ...  first=${eeupdate64e_eth0_nic5_mac_before_reboot_str}
    ...  second=${eeupdate64e_eth0_nic5_mac_after_reboot_str}
    ...  msg=Failed, after reboot the eth0/NIC5 does not the same as written!
    ...  ignore_case=${TRUE}

    [Teardown]  Run Keywords
    # Restore the original MAC
    ...  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=5 /MAC=${eeupdate64e_eth0_nic5_mac_original_str}
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to restore original/write MAC for eth0/NIC=5!
    ...  is_check_exit_code=${FALSE}
    ...  AND  powerCycleToOpenbmc
    ...  AND  open prompt and login to root user  console=${diagos_mode}
    ...  AND  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3
    ...  AND  Sleep  45s  # Wait for some terrible I2C bus add messages
    ...  AND  show network interface IP
    ...  console=${diagos_mode}
    ...  interface=eth0
    ...  pattern=(?m)^ +link\\/ether (?P<mac>${ifconfig_eth0_nic5_mac_original}[mac_1])
    ...  msg=Failed, after teardown/reboot the MAC for eth0/NIC=5 does not the same!


SHAMU_DIAG_TC008_10GKR_PORT_MAC_ADDRESS
    [Tags]  SHAMU_DIAG_TC008_10GKR_PORT_MAC_ADDRESS
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  show network interface IP  console=${diagos_mode}  interface=eth1  pattern=(?m)^ +link\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    ...  AND  set test variable  ${ip_eth1_nic1_mac_original}  ${matches}[mac_1]
    ...  AND  show network interface IP  console=${diagos_mode}  interface=eth2  pattern=(?m)^ +link\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    ...  AND  set test variable  ${ip_eth2_nic2_mac_original}  ${matches}[mac_1]
    ...  AND  Step  x  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=1 /MAC_DUMP
    ...  pattern=(?i)LAN MAC Address is (?P<mac>\\\\w+)\\\\.
    ...  msg=Failed to dump MAC for NIC=1!
    ...  is_check_exit_code=${FALSE}
    ...  AND  set test variable  ${eeupdate64e_eth1_nic1_mac_original}  ${match}[mac]
    ...  AND  Step  x  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=2 /MAC_DUMP
    ...  pattern=(?i)LAN MAC Address is (?P<mac>\\\\w+)\\\\.
    ...  msg=Failed to dump MAC for NIC=2!
    ...  is_check_exit_code=${FALSE}
    ...  AND  set test variable  ${eeupdate64e_eth2_nic2_mac_original}  ${match}[mac]

    ${ip_eth1_nic1_mac_original_str}=  Replace String
    ...  string=${ip_eth1_nic1_mac_original}
    ...  search_for=:
    ...  replace_with=
    ${ip_eth2_nic2_mac_original_str}=  Replace String
    ...  string=${ip_eth2_nic2_mac_original}
    ...  search_for=:
    ...  replace_with=
    Step   1  Should Be Equal As Strings
    ...  first=${ip_eth1_nic1_mac_original_str}
    ...  second=${eeupdate64e_eth1_nic1_mac_original}
    ...  msg=Failed, the MAC/eth1 read by ip and eeupdate64e is not the same!
    ...  ignore_case=${TRUE}
    Step   2  Should Be Equal As Strings
    ...  first=${ip_eth2_nic2_mac_original_str}
    ...  second=${eeupdate64e_eth2_nic2_mac_original}
    ...  msg=Failed, the MAC/eth2 read by ip and eeupdate64e is not the same!
    ...  ignore_case=${TRUE}

    Step   3  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=1 /MAC=${diagos_eeupdate64e_mac}[base]
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to write MAC for eth1/NIC=1!
    ...  is_check_exit_code=${FALSE}
    Step   4  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=2 /MAC=${diagos_eeupdate64e_mac}[base_plus_2]
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to write MAC for eth2/NIC=2!
    ...  is_check_exit_code=${FALSE}

    Step   5  reboot UNIX-like OS  console=${diagos_mode}

    Step   6  show network interface IP  console=${diagos_mode}  interface=eth1  pattern=(?m)^ +link\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  ${ip_eth1_nic1_mac_original_2nd}  ${matches}[mac_1]
    Step   7  show network interface IP  console=${diagos_mode}  interface=eth2  pattern=(?m)^ +link\\/ether (?P<mac>(?:[0-9a-fA-F]{2}:?){6})
    set test variable  ${ip_eth2_nic2_mac_original_2nd}  ${matches}[mac_1]

    Step   8  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=1 /MAC_DUMP
    ...  pattern=(?i)LAN MAC Address is (?P<mac>\\\\w+)\\\\.
    ...  msg=Failed to dump MAC for NIC=5!
    ...  is_check_exit_code=${FALSE}
    set test variable  ${eeupdate64e_eth1_nic1_mac_original_2nd}  ${match}[mac]
    Step   9  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=2 /MAC_DUMP
    ...  pattern=(?i)LAN MAC Address is (?P<mac>\\\\w+)\\\\.
    ...  msg=Failed to dump MAC for NIC=5!
    ...  is_check_exit_code=${FALSE}
    set test variable  ${eeupdate64e_eth2_nic2_mac_original_2nd}  ${match}[mac]

    ${ip_eth1_nic1_mac_original_str_2nd}=  Replace String
    ...  string=${ip_eth1_nic1_mac_original_2nd}
    ...  search_for=:
    ...  replace_with=
    ${ip_eth2_nic2_mac_original_str_2nd}=  Replace String
    ...  string=${ip_eth2_nic2_mac_original_2nd}
    ...  search_for=:
    ...  replace_with=
    Step  10  Should Be Equal As Strings
    ...  first=${ip_eth1_nic1_mac_original_str_2nd}
    ...  second=${eeupdate64e_eth1_nic1_mac_original_2nd}
    ...  msg=Failed, after reboot: the MAC/eth1 read by ip and eeupdate64e is not the same!
    ...  ignore_case=${TRUE}
    Step  11  Should Be Equal As Strings
    ...  first=${ip_eth2_nic2_mac_original_str_2nd}
    ...  second=${eeupdate64e_eth2_nic2_mac_original_2nd}
    ...  msg=Failed, after reboot: the MAC/eth2 read by ip and eeupdate64e is not the same!
    ...  ignore_case=${TRUE}

    Step  12  Should Be Equal As Strings
    ...  first=${diagos_eeupdate64e_mac}[base]
    ...  second=${eeupdate64e_eth1_nic1_mac_original_2nd}
    ...  msg=Failed, after reboot: the MAC/eth1 write and read by eeupdate64e is not the same!
    ...  ignore_case=${TRUE}
    Step  13  Should Be Equal As Strings
    ...  first=${diagos_eeupdate64e_mac}[base_plus_2]
    ...  second=${eeupdate64e_eth2_nic2_mac_original_2nd}
    ...  msg=Failed, after reboot: the MAC/eth2 write and read by eeupdate64e is not the same!
    ...  ignore_case=${TRUE}

    [Teardown]  Run Keywords
    ...  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=1 /MAC=${eeupdate64e_eth1_nic1_mac_original}
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to write MAC for eth1/NIC=1!
    ...  is_check_exit_code=${FALSE}
    ...  AND  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=2 /MAC=${eeupdate64e_eth2_nic2_mac_original}
    ...  patterns=${eeupdate64e_nic_update_unexpected_patterns}
    ...  msg=Failed to write MAC for eth2/NIC=2!
    ...  is_check_exit_code=${FALSE}
    ...  AND  reboot UNIX-like OS  console=${diagos_mode}


 SHAMU_DIAG_TC009_SWITCH__FIRMWARE_UPDATE
     [Tags]  SHAMU_DIAG_TC009_SWITCH__FIRMWARE_UPDATE
     ...  shamu

     [Setup]  Run Keywords
     ...  DiagOS renew IP using DHCP and set variable  AND
     ...  secure copy file
     ...  console=${diagos_mode}
     ...  username=${scp_username}
     ...  password=${scp_password}
     ...  source_ip=${ssh_server_ipv4}
     ...  source_path=${diag_pcie_flash_path}
     ...  source_file=${diag_pcie_flash_new_image}
     ...  destination=${diag_pcie_flash_save_to}
     ...  sec=${6 * 60}

     Step   1  Execute command on SDK Prompt (sdklt.0>)
     ...  command=pciephy fwload ${diag_pcie_flash_save_to}/${diag_pcie_flash_new_image}
     ...  pattern=(?mi)[ \\\\t]*PCIE firmware updated (?P<result>successfully)
     Step   2  Execute command on SDK Prompt (sdklt.0>)
     ...  command=pciephy fwinfo
     ...  pattern=(?i)[ \\\\t]*PCIe FW loader version\\\\: (?P<pcie_fw_loader_version>${diag_pcie_flash_new_version})
     ...  msg=Failed, not found the PCIe FW Loader version or the version is not up-to-date!

     [Teardown]  Run Keyword If Test Failed  RUN KEYWORDS
     ...  send a line  command=quit
     ...  AND  send a line  command=\x03  # Ctrl-C


SHAMU_DIAG_TC010_CPU INFORMATION TEST
     [Tags]  SHAMU_DIAG_TC010_CPU INFORMATION TEST  shamu
     step  1  open prompt and login to root user  console=${diagos_mode}
     step  2  check cpu information
     step  3  sonic switch to openbmc console
     step  4  check cpu option
     step  5  show cpu info
     step  6  cel cpu test


SHAMU_DIAG_TC011_SWITCH_PCIE_FIRMWARE_VERSION_TEST
    [Tags]  SHAMU_DIAG_TC011_SWITCH_PCIE_FIRMWARE_VERSION_TEST
    ...  shamu

    Step   1  Execute command on SDK Prompt (sdklt.0>)
    ...  command=pciephy fwinfo
    ...  pattern=(?i)[ \\\\t]*PCIe FW loader version\\\\: (?P<pcie_fw_loader_version>${diag_pcie_flash_new_version})
    ...  msg=Failed, not found the PCIe FW Loader version or the version is not up-to-date!


SHAMU_DIAG_TC012_SDK_VERSION_TEST
    [Tags]  SHAMU_DIAG_TC012_SDK_VERSION_TEST
    ...  shamu

    Step   1  Execute command on BCM Prompt (BCM.0>)
    ...  command=version
    ...  pattern=(?i)[ \\\\t]*Release: sdk-(?P<sdk_release_version>.*) built
    ...  msg=Failed, not found the SKD Release version!


SHAMU_DIAG_TC013_I210_FIRMWARE_VERSION_TEST
    [Tags]  SHAMU_TC013_I210_FIRMWARE_VERSION_TEST
    ...  shamu

    [Setup]  open prompt and login to root user  console=${diagos_mode}

    Step   1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=5 /ADAPTERINFO
    ...  pattern=Firmware Version\\\\: .*\\\\:?(?P<firmware_version>\\\\d\\\\.\\\\d)
    ...  msg=Failed, not found the I210 firmware version for NIC=5!
    ...  is_check_exit_code=${FALSE}
    Step   2  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./eeupdate64e /NIC=5 /ADAPTERINFO
    ...  pattern=NVM Version:.*(?P<nvm_version>\\\\d\\\\.\\\\d+)
    ...  msg=Failed, not found the I210 nvm version for NIC=5!
    ...  is_check_exit_code=${FALSE}


SHAMU_DIAG_TC014_SOFTWARE_INFORMATION_TEST
    [Tags]  SHAMU_TC014_SOFTWARE_INFORMATION_TEST
    ...  shamu

    [Setup]  open prompt and login to root user  console=${diagos_mode}

    Step   1  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-software-test -h
    ...  patterns=${software_help_patterns}

    Step   2  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=./cel-software-test -i
    ...  patterns=${software_i_patterns}
    ...  msg=Failed, may not found some version on the patterns!
    set test variable  ${software_versions}  ${matches}
    Step   3  execute command and verify with a pattern
    ...  console=${onie_mode}
    ...  command=onie-sysinfo -v
    ...  pattern=(?m)^(?P<onie_version>\\\\d{4}[\\\\.\\\\d]*)
    ...  msg=Failed, not found the onie version!
    set test variable  ${onie_sysinfo_version}  ${match}
    Step   4  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=show version
    ...  patterns=${sonic_show_version_patterns}
    ...  msg=Failed, may not found some version on the patterns!
    set test variable  ${sonic_versions}  ${matches}

    Step   5  compare two dictionaries with matched key
    ...  original=${sonic_versions}
    ...  compare=${software_versions}
    ...  msg=Failed, some of version does not match!
    Step   6  Should Be Equal As Strings
    ...  first=${onie_sysinfo_version}[onie_version]
    ...  second=${software_versions}[onie_version]
    ...  msg=Failed the onie version does not match!
    ...  ignore_case=${TRUE}


SHAMU_DIAG_TC015_FPGA_ACCESS_TEST
    [Tags]  SHAMU_DIAG_TC015_FPGA_ACCESS_TEST
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3

    Step   1  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-fpga-test -h
    ...  patterns=${diagos_fpga_help_patterns}
    ...  msg=Failed to verify -h/help option!
    Step   2  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -v
    ...  pattern=(?i)FPGA Version:[ \\\\t]*(?P<version>0x[0-9a-fA-F]{8})
    ...  msg=Failed, not found the FPGA version!
    set test variable  ${diag_tool_fpga_version}  ${match}[version]
    Step   3  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=(echo 0x00 > /sys/devices/platform/AS1440D.switchboard/FPGA/getreg && cat /sys/devices/platform/AS1440D.switchboard/FPGA/getreg)
    ...  pattern=(?m)^(?P<version>0x[0-9a-fA-F]{8})
    ...  msg=Failed, not found the FPGA version!
    set test variable  ${bsp_fpga_version}  ${match}[version]
    Step   4  Should Be Equal As Strings
    ...  first=${diag_tool_fpga_version}
    ...  second=${bsp_fpga_version}
    ...  msg=Failed, miss match for FPGA version!
    ...  ignore_case=${TRUE}
    Step   5  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -r 0x04
    ...  msg=Failed to read the FPGA register!
    Step   6  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -w 0x04 -d 0xef
    ...  msg=Failed to write to the FPGA register!
    Step   7  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-fpga-test -r 0x04
    ...  pattern=(?m)^(?P<data>0x000000ef)
    ...  msg=Failed to read the FPGA register or miss match!


SHAMU_DIAG_TC016_CPLD_ACCESS_TEST
    [Tags]  SHAMU_DIAG_TC016_CPLD_ACCESS_TEST
    ...  shamu

    Step   1  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -h
    ...  patterns=${cpld_help_patterns}
    Step   2  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -v
    ...  patterns=${cpld_version_patterns}
    set test variable  ${cpld_versions}  ${matches}
    Step   3  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./lpc_cpld_x64_64 blu r 0xa100
    ...  pattern=(?m)^[ \\\\t]*(?P<base>0x[0-9a-fA-F]{2})
    ...  msg=Failed, CPLD/Base does not up-to-date!${\n}Or may not found the pattern!
    set test variable  ${lpc_tool_cpld_base_version}  ${match}[base]
    Step   4  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./lpc_cpld_x64_64 blu r 0xa1e0
    ...  pattern=(?m)^[ \\\\t]*(?P<come>0x[0-9a-fA-F]{2})
    ...  msg=Failed, CPLD/COMe does not up-to-date!${\n}Or may not found the pattern!
    set test variable  ${lpc_tool_cpld_come_version}  ${match}[come]

    Step   5  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=(echo 0x00 > /sys/devices/platform/AS1440D.switchboard/CPLD1/getreg && cat /sys/devices/platform/AS1440D.switchboard/CPLD1/getreg)
    ...  pattern=(?m)^[ \\\\t]*(?P<switch>0x[0-9a-fA-F]{2})
    ...  msg=Failed, CPLD/switch 1 is not up-to-date!${\n}Or may not found the pattern!
    set test variable  ${sysfs_cpld_switch_1_version}  ${match}[switch]
    Step   6  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=(echo 0x00 > /sys/devices/platform/AS1440D.switchboard/CPLD2/getreg && cat /sys/devices/platform/AS1440D.switchboard/CPLD2/getreg)
    ...  pattern=(?m)^[ \\\\t]*(?P<switch>0x[0-9a-fA-F]{2})
    ...  msg=Failed, CPLD/switch 2 is not up-to-date!${\n}Or may not found the pattern!
    set test variable  ${sysfs_cpld_switch_2_version}  ${match}[switch]

    Step   7  Should Be Equal As Strings
    ...  ${cpld_versions}[base]  ${lpc_tool_cpld_base_version}
    ...  msg=Failed, CPLD/Base version does not match!
    ...  ignore_case=${TRUE}
    Step   8  Should Be Equal As Strings
    ...  ${cpld_versions}[come]  ${lpc_tool_cpld_come_version}
    ...  msg=Failed, CPLD/COMe version does not match!
    ...  ignore_case=${TRUE}
    Step   9  Should Be Equal As Strings
    ...  ${cpld_versions}[switch_1]  ${sysfs_cpld_switch_1_version}
    ...  msg=Failed, CPLD/Switch 1 version does not match!
    ...  ignore_case=${TRUE}
    Step  10  Should Be Equal As Strings
    ...  ${cpld_versions}[switch_2]  ${sysfs_cpld_switch_2_version}
    ...  msg=Failed, CPLD/Switch 2 version does not match!
    ...  ignore_case=${TRUE}

    Step  11  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -r Base-CPLD -a 0xa1e1
    ...  pattern=(?m)^[ \\\\t]*(?P<default>0x[0-9a-fA-F]{2})
    ...  msg=Failed to read the default value!
    ...  is_check_exit_code=${FALSE}
    Step  12  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -w Base-CPLD -a 0xa1e1 -d 0x22
    ...  msg=Failed to write to the register!
    Step  13  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -r Base-CPLD -a 0xa1e1
    ...  pattern=(?m)^[ \\\\t]*(?P<written>0x22)
    ...  msg=Failed, the written value is missed the expect!

    Step  14  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -r CPLD-1 -a 0x01
    ...  pattern=(?m)^[ \\\\t]*(?P<default>0x[0-9a-fA-F]{2})
    ...  msg=Failed to read the default value!
    ...  is_check_exit_code=${FALSE}
    Step  15  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -w CPLD-1 -a 0xa101 -d 0x33
    ...  msg=Failed to write to the register!
    Step  16  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -r CPLD-1 -a 0x01
    ...  pattern=(?m)^[ \\\\t]*(?P<written>0x33)
    ...  msg=Failed, the written value is missed the expect!

    Step  17  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -r CPLD-2 -a 0x01
    ...  pattern=(?m)^[ \\\\t]*(?P<default>0x[0-9a-fA-F]{2})
    ...  msg=Failed to read the default value!
    ...  is_check_exit_code=${FALSE}
    Step  18  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -w CPLD-2 -a 0x01 -d 0xee
    ...  msg=Failed to write to the register!
    Step  19  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -r CPLD-2 -a 0x01
    ...  pattern=(?m)^[ \\\\t]*(?P<written>0xee)
    ...  msg=Failed, the written value is missed the expect!

    Step  20  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-cpld-test -t
    ...  patterns=${cpld_test_all_patterns}
    ...  msg=Failed, not found all the pass patterns!


SHAMU_DIAG_TC017_MEMORY_TEST
    [Tags]  SHAMU_DIAG_TC017_MEMORY_TEST
    ...  shamu

    Step   1  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cat /proc/meminfo
    Step   2  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-memory-test -h
    ...  patterns=${diagos_mem_help_patterns}
    ...  msg=Failed to verify -h option!
    Step   3  execute command and verify with a pattern for table
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-memory-test -i
    ...  pattern=(?i)[ \\\\t]*Size: (?P<size>\\\\d+) MB
    set test variable  ${mem_i}  ${matches}
    Step   4  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-memory-test -s
    ...  pattern=(?i)[ \\\\t]*(?P<size>\\\\d+) MB
    ...  msg=Failed, not found the memory size!
    set test variable  ${mem_s_total}  ${match}[size]

    ${status}  ${value}=  Run Keyword And Ignore Error  Length Should Be  item=${mem_i}  length=2
    RUN KEYWORD IF  '${status}' == 'FAIL'  Set To Dictionary   ${mem_i}  size_2=${0}

    ${mem_i_total}  Evaluate  ${mem_i}[size_1] + ${mem_i}[size_2]
    Step   5  Should Be Equal As Strings
    ...  first=${mem_s_total}
    ...  second=${mem_i_total}
    ...  msg=Failed, the number of memory shoule equal!

    Step   6  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-memory-test -t
    ...  pattern=(?i)[ \\\\t]*memory_read_write_test.*(?P<result>PASS)
    ...  msg=Failed, not found the pass pattern!
    ...  sec=${5 * 60}


SHAMU_DIAG_TC018_USB_STORAGE_TEST
    [Tags]  SHAMU_DIAG_TC018_USB_STORAGE_TEST
    ...  shamu

    [Setup]  open prompt and login to root user  ${diagos_mode}

    Step   1  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-usb-test -h
    ...  patterns=${usb_storage_help_patterns}
    ...  msg=Failed to verify -h option!
    Step   2  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-usb-test -t
    ...  patterns=${usb_storage_t_patterns}
    ...  msg=Failed, not found the pass pattern!
    set test variable  ${usb_storage_device}  ${matches}[drive]
    Step   3  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=fdisk -l ${usb_storage_device}
    ...  msg=Failed, the USB Storage is may not insert!


SHAMU_DIAG_TC019_RTC_TEST
    [Tags]  SHAMU_DIAG_TC019_RTC_TEST
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  OpenBMC wedge power script  sec=${10 * 60}
    ...  AND  search for a pattern
    ...  text=${text}
    ...  pattern=BIOS Date: (?P<date>(?P<month>\\d{2})\\/(?P<day>\\d{2})\\/(?P<year>\\d{4}) (?P<time>.*?)\\ )
    ...  msg=Failed, not found BIOS Date and Time!
    ...  AND  set test variable  ${bios_date_time}  ${match}[year]-${match}[month]-${match}[day] ${match}[time]
    ...  AND  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=date --rfc-3339=seconds
    ...  pattern=(?m)^[ \\t]*(?P<date>\\d{4}.*?)[\\+|\\.]
    ...  msg=Failed, not found date/time!
    ...  AND  set test variable  ${date}  ${match}
    ...  AND  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=hwclock
    ...  pattern=(?m)^[ \\t]*(?P<date>\\d{4}.*?)[\\+|\\.]
    ...  msg=Failed, not found date/time!
    ...  AND  set test variable  ${hwclock}  ${match}
    ...  AND  date/time difference
    ...  date1=${date}[date]
    ...  date2=${hwclock}[date]
    ...  diff=5
    ...  msg=Failed, the date is not the same for "date" and "hwclock"${\n}, the diff is more than 5 seconds!
    ...  AND  date/time difference
    ...  date1=${date}[date]
    ...  date2=${bios_date_time}
    ...  diff=5
    ...  msg=Failed, the date is not the same for "date" and "BIOS's date/time"${\n}, the diff is more than 5 seconds!

    Step   1  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-RTC-test -h
    ...  patterns=${diagos_rtc_help_patterns}
    ...  msg=Failed to verify -h option!
    Step   2  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-RTC-test -g
    ...  pattern=(?m)^[ \\\\t]*(?P<date>\\\\d{4}.*?)[\\\\+|\\\\.]
    ...  msg=Failed to verify -g option!
    set test variable  ${rtc}  ${match}

    # Add offset, write and read to verify
    ${offset}=  Add Time To Date
    ...  ${rtc}[date]  10 minute
    ...  exclude_millis=${TRUE}
    ${offset_formatted}=  Convert Date
    ...  ${offset}
    ...  result_format=%Y-%m-%d %H:%M:%S

    Step   3  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-RTC-test -s -d '${offset_formatted}.000000+0000'
    ...  path=${diagos_cpu_diag_path}
    ...  msg=Failed, to write the date!
    Step   4  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-RTC-test -g
    ...  pattern=(?m)^[ \\\\t]*(?P<date>\\\\d{4}.*?)[\\\\+|\\\\.]
    ...  msg=Failed to verify -g option!
    set test variable  ${rtc_2nd}  ${match}
    Step   5  date/time difference
    ...  date1=${offset_formatted}
    ...  date2=${rtc_2nd}[date]
    ...  diff=5
    ...  msg=Failed, the date is not the same for "RTC Written" and "RTC Read"${\n}, the diff is more than 5 seconds!
    Step   6  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-RTC-test -i
    ...  msg=Failed to verify -i option!

    # Reboot to check with the BIOS time
    Step   7  OpenBMC wedge power script  sec=${10 * 60}
    Step   8  search for a pattern
    ...  text=${text}
    ...  pattern=BIOS Date: (?P<date>(?P<month>\\\\d{2})\\\\/(?P<day>\\\\d{2})\\\\/(?P<year>\\\\d{4}) (?P<time>.*?)\\\\ )
    ...  msg=Failed, not found BIOS Date and Time!
    set test variable  ${bios_date_time_2nd}  ${match}[year]-${match}[month]-${match}[day] ${match}[time]
    Step   9  date/time difference
    ...  date1=${offset_formatted}
    ...  date2=${bios_date_time_2nd}
    ...  diff=${10 * 60}
    ...  msg=Failed, the date is not the same for "RTC Written" and "BIOS's date/time (reboot)"${\n}, the diff is more than ${10 * 60} seconds!

    # Adjust time back to correct it!
    Step  10  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-RTC-test -g
    ...  pattern=(?m)^[ \\\\t]*(?P<date>\\\\d{4}.*?)[\\\\+|\\\\.]
    ...  msg=Failed to verify -g option!
    set test variable  ${rtc_3rd}  ${match}
    ${offset}=  Subtract Time From Date
    ...  ${rtc_3rd}[date]  10 minute
    ...  exclude_millis=${TRUE}
    ${offset_formatted}=  Convert Date
    ...  ${offset}
    ...  result_format=%Y-%m-%d %H:%M:%S

    Step  11  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-RTC-test -s -d '${offset_formatted}.000000+0000'
    ...  path=${diagos_cpu_diag_path}
    ...  msg=Failed, to write the date!


SHAMU_DIAG_TC020_I2C_DEVICE_TEST
    [Tags]  SHAMU_DIAG_TC020_I2C_DEVICE_TEST
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    # DIAG OS
    Step  1   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-i2c-test -h
    ...  patterns=${diagos_i2c_test_help_patterns}
    ...  msg=Failed to verify help option!
    Step  2   find I2C device number by diagtool
    ...  pattern=(?P<qsfp_number>QSFP_\\\\d+)[ \\\\t]+\\\\d+[ \\\\t]+0x[0-9a-fA-F]{2}
    Step  3   execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=i2cdetect -l
    ...  path=${diagos_cpu_diag_path}
    Step  4   find I2C device number by i2cdetect
    ...  command=i2cdetect -l | grep -i QSFP | wc -l
    Step  5  Should Be Equal As Integers
    ...  ${i2cdetect_dev}[number]  ${diagtool_dev_number}
    ...  Failed, the I2C devices detected by "i2cdetect -l" and "cel-i2c-test -l" are not the same!
    Step  6   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-i2c-test -s
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?i)All the I2C devices test.*(?P<result>PASS)
    ...  sec=${2 * 60}
    Step  7   execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-i2c-test -t
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?i)All the I2C devices test.*(?P<result>PASS)
    ...  sec=${2 * 60}


SHAMU_DIAG_TC021_PCIE_DEVICES_TEST
    [Tags]  SHAMU_DIAG_TC021_PCIE_DEVICES_TEST
    ...  shamu

    Step   1  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-pcie-test -h
    ...  patterns=${pcie_help_patterns}
    ...  msg=Failed, may not found some help option!
    Step   2  execute command and verify with a pattern for table
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-pcie-test -i
    ...  pattern=(?P<pci_number>\\\\d{2}\\\\:\\\\d{2}\\\\.\\\\d)
    ...  msg=Failed, not found a PCIe device!
    ...  sec=${2 * 60}
    set test variable  &{pcie_i_devices}  &{matches}
    Step   3  Verify PCIe list of device is all exist by lspci tool  devices=\&{pcie_i_devices}
    Step   4  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./cel-pcie-test -t
    ...  path=${diagos_cpu_diag_path}
    ...  pattern=(?i)PCI Test.*(?P<result>PASS)
    ...  sec=${2 * 60}


SHAMU_DIAG_TC023_LOOPBACK_TEST
    [Tags]  SHAMU_DIAG_TC023_LOOPBACK_TEST
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3

    Step   1  Execute command on BCM Prompt (BCM.0>)
    ...  command=port cb lb=mac
    ...  pattern=BCM\\\\.0>
    ...  is_no_exit=${TRUE}
    Step   2  Execute command on BCM Prompt (BCM.0>)
    ...  command=ps cd
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   3  Execute command on BCM Prompt (BCM.0>)
    ...  command=rcload snake_script.soc
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   4  Execute command on BCM Prompt (BCM.0>)
    ...  command=clear c
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   5  Execute command on BCM Prompt (BCM.0>)
    ...  command=show c cd0
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   6  Execute command on BCM Prompt (BCM.0>)
    ...  command=tx 100 pbm=cd0 vlan=100
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   7  BuiltIn.Sleep  2 mins
    Step   8  Execute command on BCM Prompt (BCM.0>)
    ...  command=port cd0 en=off
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   9  Execute command on BCM Prompt (BCM.0>)
    ...  command=sleep 2
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step  10  Execute command on BCM Prompt (BCM.0>)
    ...  command=clear c
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step  11  Execute command on BCM Prompt (BCM.0>)
    ...  command=port cd0 en=on
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}


SHAMU_DIAG_TC024_TRAFFIC_TEST
    [Tags]  SHAMU_DIAG_TC024_TRAFFIC_TEST
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3

    Step   1  Execute command on BCM Prompt (BCM.0>)
    ...  command=port cb lb=mac
    ...  pattern=BCM\\\\.0>
    ...  is_no_exit=${TRUE}
    Step   2  Execute command on BCM Prompt (BCM.0>)
    ...  command=ps cd
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   3  Execute command on BCM Prompt (BCM.0>)
    ...  command=rcload snake_script.soc
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   4  Execute command on BCM Prompt (BCM.0>)
    ...  command=rcload snake_script.soc
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   5  Execute command on BCM Prompt (BCM.0>)
    ...  command=clear c
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   6  Execute command on BCM Prompt (BCM.0>)
    ...  command=show c cd0
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   7  Execute command on BCM Prompt (BCM.0>)
    ...  command=tx 100 pbm=cd0 vlan=100
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   8  BuiltIn.Sleep  2 mins
    Step   9  Execute command on BCM Prompt (BCM.0>)
    ...  command=port cd0 en=off
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step  10  Execute command on BCM Prompt (BCM.0>)
    ...  command=sleep 2
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step  11  Execute command on BCM Prompt (BCM.0>)
    ...  command=show c
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step  12  Execute command on BCM Prompt (BCM.0>)
    ...  command=port cd0 en=on
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}


SHAMU_DIAG_TC025_OOB_TEST
    [Tags]  SHAMU_DIAG_TC025_OOB_TEST
    ...  shamu

    Step   1  OOB menu/help verify
    ...  oob_console=${diagos_mode}
    ...  oob_path=${diagos_cpu_diag_path}
    Step   2  OOB menu/auto-test
    ...  oob_console=${diagos_mode}
    ...  oob_path=${diagos_cpu_diag_path}
    ...  oob_patterns=(?mi)^[ \\\\t]*OOB_?Test[ \\\\.]+.*(?P<result>PASS)

SHAMU_DIAG_TC026_10G_KR_Test_TEST
     [Tags]  SHAMU_DIAG_TC026_10G_KR_Test_TEST  shamu
     step  1  open prompt and login to root user  console=${diagos_mode}
     step  2  change dir  ${diagos_cpu_diag_path}
     step  3  test 10gkr option h
     step  4  test 10gkr option i
     step  5  kill bcm user
     step  6  change dir  ${diagos_sdk_path}
     step  7  auto load user
     step  8  change dir  ${diagos_cpu_diag_path}
     step  9  test 10gkr option t
     step  10  exit this program

SHAMU_DIAG_TC027_SATA_Parameter_Test
     [Tags]  SHAMU_DIAG_TC027_SATA_Parameter_Test  shamu
     step  1  open prompt and login to root user  console=${diagos_mode}
     step  2  change dir  ${diagos_cpu_diag_path}
     step  3  sata test option h
     step  4  sata test option t


SHAMU_DIAG_TC029_LPC_TEST
    [Tags]  SHAMU_DIAG_TC029_LPC_TEST
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${openbmc_mode}
    ...  AND  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    ...  AND  open prompt and login to root user  console=${diagos_mode}
    ...  AND  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3

    # Method one
    Step   1  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=set snoop addr to 80
    Step   2  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=devmem 0x1e789090 32 0x80
    Step   3  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=enable snooping address
    ...  is_check_exit_code=${FALSE}
    Step   4  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=source /usr/local/fbpackages/utils/ast-functions
    Step   5  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=devmem_set_bit 0x1e789080 0

    ${data_1_written}=  Evaluate  random.randint(10, 99)
    Step   6  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./lpc_cpld_x64_64 blu w 0x80 0x${data_1_written}
    Step   7  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=devmem 0x1e789094 8
    ...  pattern=(?mi)^(?P<data_1_read>0x[0-9a-fA-F]{2})
    ...  msg=Failed, can not read the data!
    Step   8  Should Be Equal As Strings
    ...  0x${data_1_written}  ${match}[data_1_read]
    ...  msg=Failed, OpenBMC and DiagOS does not the same data!

    ${data_2_written}=  Evaluate  random.randint(10, 99)
    Step   9  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./lpc_cpld_x64_64 blu w 0x80 0x${data_2_written}
    Step  10  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=devmem 0x1e789094 8
    ...  pattern=(?mi)^(?P<data_2_read>0x[0-9a-fA-F]{2})
    ...  msg=Failed, can not read the data!
    Step  11  Should Be Equal As Strings
    ...  0x${data_2_written}  ${match}[data_2_read]
    ...  msg=Failed, OpenBMC and DiagOS does not the same data!

    ${data_3_written}=  Evaluate  random.randint(10, 99)
    Step  12  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./lpc_cpld_x64_64 blu w 0x80 0x${data_3_written}
    Step  13  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=devmem 0x1e789094 8
    ...  pattern=(?mi)^(?P<data_3_read>0x[0-9a-fA-F]{2})
    ...  msg=Failed, can not read the data!
    Step  14  Should Be Equal As Strings
    ...  0x${data_3_written}  ${match}[data_3_read]
    ...  msg=Failed, OpenBMC and DiagOS does not the same data!

    # Method two
    Step  15  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=ssh-keygen -f "/root/.ssh/known_hosts" -R 240.1.1.1
    Step  16  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_auto_tool}
    ...  command=./cel-LPC-test
    ...  pattern=(?i)CPU-BMC LPC.*(?P<result>PASS)
    ...  msg=Failed, not found the pass pattern!
    ...  sec=${5 * 60}


# How to compare the number!
# The meminfo is not equal to dmidecode (in kB)
# 7548692.0 != 8388608.0
SHAMU_DIAG_TC030_SPD_TEST
    [Tags]  SHAMU_DIAG_TC030_SPD_TEST
    ...  shamu
    ...  pending

    Step   1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=(cat /proc/meminfo | grep -i MemTotal)
    ...  pattern=(?P<kB>\\\\d+) kB
    ...  msg=Failed, not found how many memory!
    ${meminfo_k_bytes}=  Set Variable  ${match}[kB]
    Step   2  Total memory byte by dmidecode
    Step   3  Should Be Equal As Numbers
    ...  first=${meminfo_k_bytes}
    ...  second=${dmimem_k_bytes}
    ...  msg=Failed, the total memory is not equal!
    ...  precision=0


SHAMU_DIAG_TC033_PRBS_TEST
    [Tags]  SHAMU_TC033_PRBS_TEST
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3

    Step   1  Execute command on BCM Prompt (BCM.0>)
    ...  command=dsh -c "phy diag 1-69 prbs set p=3"
    ...  pattern=BCM\\\\.0>
    ...  is_no_exit=${TRUE}
    Step   2  Execute command on BCM Prompt (BCM.0>)
    ...  command=dsh -c "phy diag 1-69 prbs get"
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   3  Execute command on BCM Prompt (BCM.0>)
    ...  command=dsh -c "phy diag 1-69 prbsstat start interval=120"
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   4  Execute command on BCM Prompt (BCM.0>)
    ...  command=sleep 5
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   5  Execute command on BCM Prompt (BCM.0>)
    ...  command=dsh -c "phy diag 1-69 prbsstat ber"
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   6  Execute command on BCM Prompt (BCM.0>)
    ...  command=sleep 120  # Now, it supports 180s
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   7  Execute command on BCM Prompt (BCM.0>)
    ...  command=dsh -c "phy diag 1-69 prbsstat ber"
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   8  Execute command on BCM Prompt (BCM.0>)
    ...  command=dsh -c "phy diag 1-69 prbsstat stop"
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_exit=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}
    Step   9  Execute command on BCM Prompt (BCM.0>)
    ...  command=dsh -c "phy diag 1-69 prbs clear"
    ...  pattern=BCM\\\\.0>
    ...  is_no_kill=${TRUE}
    ...  is_no_reload=${TRUE}
    ...  is_no_login_to_root_user=${TRUE}

    [Teardown]  Run Keyword If Test Failed  RUN KEYWORDS
    ...  send a line  command=quit
    ...  AND  send a line  command=\x03  # Ctrl-C

SHAMU_DIAG_TC036_SSD_STRESS_TEST
    [Tags]  SHAMU_DIAG_TC036_SSD_STRESS_TEST  shamu
    Step  1  open prompt and login to root user  console=${diagos_mode}
    Step  2  ssd script test
    Step  3  cat ssd stress log
    [Teardown]  recover cpu

SHAMU_DIAG_TC034_CPU_STRESS_TEST
    [Tags]   SHAMU_DIAG_TC034_CPU_STRESS_TEST  shamu
    Step  1  open prompt and login to root user  console=${diagos_mode}
    Step  2  cpu Option Test
    Step  3  cat Cpu Log

SHAMU_DIAG_TC037_OPTICAL_MODULES_STRESS_TEST
     [Tags]  SHAMU_DIAG_TC037_OPTICAL_MODULES_STRESS_TEST  shamu
     step  1  open prompt and login to root user  console=${diagos_mode}
     step  2  sfputil test eeprom
     step  3  optical modules stress Test

SHAMU_DIAG_TC038_Qsfp_i2cdump_stress_test
     [Tags]  SHAMU_DIAG_TC038_Qsfp_i2cdump_stress_test  shamu
     step  1  open prompt and login to root user  console=${diagos_mode}
     step  2  qsfp I2cdump Stress Test
     [Teardown]  reboot To DiagOS

SHAMU_DIAG_TC039_MODIFY_QSFP_POWER_CONSUMPTION
    [Tags]  SHAMU_DIAG_TC039_MODIFY_QSFP_POWER_CONSUMPTION
    ...  shamu

    Step   1  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${diagos_diag_utility_path}
    ...  command=./luxshare_power_config.sh -h
    ...  patterns=${luxshare_power_config_help_patterns}
    Step   2  execute command and verify with a pattern for table
    ...  console=${diagos_mode}
    ...  command=./luxshare_power_config.sh -n
    ...  pattern=[ \\\\t]*set (port|i2cbus)_(?P<port>\\\\d+) power\\\\: 1\\\\.5W
    ...  path=${diagos_diag_utility_path}
    ...  msg=Failed to set all module ports to normal power 1.5W
    ...  sec=${5 * 60}
    Step   3  set high power according to port number

    # Set it back to normal power 1.5W
    [Teardown]  execute command and verify with a pattern for table
    ...  console=${diagos_mode}
    ...  command=./luxshare_power_config.sh -n
    ...  pattern=[ \\t]*set (port|i2cbus)_(?P<port>\\d+) power\\: 1\\.5W
    ...  path=${diagos_diag_utility_path}
    ...  msg=Failed to set all module ports to normal power 1.5W
    ...  sec=${5 * 60}


SHAMU_DIAG_TC040_PRIMARY_FPGA_AND_GOLDEN_FPGA_FUNCTION_TEST
    [Tags]  SHAMU_DIAG_TC040_PRIMARY_FPGA_AND_GOLDEN_FPGA_FUNCTION_TEST
    ...  shamu

    Step   1  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${diagos_fpga_path}
    ...  source_file=${diagos_fpga_new_image}
    ...  destination=${diagos_fpga_save_to}
    ...  sec=${10 * 60}
    Step   2  send a line  command=fpga_prog ${diagos_fpga_new_image}
    Step   3  Sleep  10s  # Approximately 50%
    Step   4  powerCycleToOpenbmc
    Sleep  2mins
    Step   5  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-fpga-test -v
    ...  pattern=[ \\\\t]*FPGA Version: (?P<fpga_version>0x[0-9a-fA-F]{8})  # What is the golden version?
    ...  msg=Failed, not found FPGA Version!

    Step   6  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${diagos_fpga_path}
    ...  source_file=${diagos_fpga_new_image}
    ...  destination=${diagos_fpga_save_to}
    ...  sec=${10 * 60}
    Step   7  ssh execute
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  server_ip=${ssh_server_ipv4}
    ...  command=md5sum ${diagos_fpga_path}/${diagos_fpga_new_image}
    Step   8  search for a pattern
    ...  text=${text}
    ...  pattern=^(?P<md5sum>[0-9a-fA-F]{32})[ \\\\t]+[\\\\/\\\\w]*?(?P<file_name>\\\\w+\\\\.\\\\w+)
    ...  msg=Failed, not found md5sum!
    set test variable  ${ssh_fpga_md5sum}  ${match}[md5sum]
    Step   9  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_fpga_save_to}
    ...  command=md5sum ${diagos_fpga_new_image}
    ...  pattern=(?mi)^(?P<md5sum>[0-9a-fA-F]+)[ \\\\t]*(?P<file>.*)
    ...  msg=Failed, not found MD5SUM!
    set test variable  ${tftp_fpga_md5sum}  ${match}[md5sum]
    Step  10  Should Be Equal As Strings
    ...  first=${ssh_fpga_md5sum}
    ...  second=${tftp_fpga_md5sum}
    ...  msg=Failed, the MD5SUM mismatch!
    ...  ignore_case=${TRUE}

    Step  11  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${diagos_fpga_save_to}
    ...  command=fpga_prog ${diagos_fpga_new_image}
    ...  msg=Failed to program FPGA!${\n}The command is not return exit code zero!

    Step  12  powerCycleToOpenbmc
    Step  13  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_cpu_diag_path}
    ...  command=./cel-fpga-test -v
    ...  pattern=[ \\\\t]*FPGA Version: (?P<fpga_version>${diagos_fpga_new_version})
    ...  msg=Failed, not found FPGA Version or not up-to-date!


SHAMU_DIAG_TC042_CPU_FREQUENCY_TEST
    [Tags]  SHAMU_DIAG_TC042_CPU_FREQUENCY_TEST
    ...  shamu

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3

    Step   1  change directory  console=${diagos_mode}  dir=${diagos_diag_utility_stress_path}
    Step   2  send a line  command=./mprime -d -t &
    Step   3  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=sleep 20  # Robot also supports delay, buy let the unit do it for us!
    Step   4  execute command and verify with a pattern for table
    ...  command=cat /proc/cpuinfo | grep MHz
    ...  console=${diagos_mode}
    ...  pattern=(?P<freq_mhz_of_cpu>\\\\d+\\\\.?\\\\\d+)
    ...  msg=Failed, not found the CPU frequency!

    # Then, how to verify the CPU frequency!

    [Teardown]  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=killall -9 mprime
    ...  is_check_exit_code=${FALSE}


SHAMU_DIAG_TC043_PORT_SIGNAL_TEST
    [Tags]   SHAMU_DIAG_TC043_PORT_SIGNAL_TEST  shamu
    Step  1  change dir  ${diagos_cpu_diag_path}
    Step  2  port present test
    Step  3  port reset test
    Step  4  port modsel test
    Step  5  port lpmod test
    Step  6  port interrupt test


SHAMU_DIAG_TC044_PORT_SPLIT_TEST
    [Tags]   SHAMU_DIAG_TC044_PORT_SPLIT_TEST  shamu
    Step  1  check Port Consistent


SHAMU_DIAG_TC048_CPLD UPDATE IMAGE
     [Tags]  SHAMU_DIAG_TC048_CPLD UPDATE IMAGE  shamu
     step  1  open prompt and login to root user  console=${diagos_mode}
     step  2  change dir  ${diagos_cpu_diag_path}
     step  3  cpld test option v
     step  4  open prompt and login to root user  console=${openbmc_mode}
     step  5  check cpld version
     step  6  change dir  /tmp/
     step  7  execute command  mkdir CPLD
     step  8  execute command  dhclient eth0
     step  9  download cpld image version  ${FALSE}
     step  10  change dir  /tmp/CPLD/
     step  11  update base cpld version  old
     step  12  update come cpld version  old
     step  13  update switch cpld version  old
     step  14  update fan cpld version  old
     step  15  check cpu power status
     step  16  powerCycleToOpenbmc
     step  17  open prompt and login to root user  console=${diagos_mode}
     step  18  Sleep  300s
     step  19  change dir  ${diagos_cpu_diag_path}
     step  20  check cpld image version  old
     step  21  open prompt and login to root user  console=${openbmc_mode}
     step  22  change dir  /tmp/
     step  23  execute command  mkdir CPLD
     step  24  execute command  dhclient eth0
     step  25  download cpld image version  ${TRUE}
     step  26  change dir  /tmp/CPLD/
     step  27  update base cpld version  new
     step  28  update come cpld version  new
     step  29  update switch cpld version  new
     step  30  update fan cpld version  new
     step  31  check cpu power status
     step  32  powerCycleToOpenbmc
     step  33  open prompt and login to root user  console=${diagos_mode}
     step  34  Sleep  300s
     step  35  change dir  ${diagos_cpu_diag_path}
     step  36  check cpld image version  new

SHAMU_DIAG_TC049_FRU_EEPROM_UPDATE
    [Tags]  SHAMU_DIAG_TC049_FRU_EEPROM_UPDATE
    ...  shamu  long_time

    # Typically total run time is 65 minutes

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  Sleep  45s  # Wait for some terrible I2C bus add messages

    Step  1  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> BMC <<
    ...  path=${openbmc_bmc_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d
    ...  eeprom_tool_write=./eeprom_tool -w
    ...  eeprom_tool_update=./eeprom_tool -u
    Step  2  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> COMe <<
    ...  path=${openbmc_come_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d
    ...  eeprom_tool_write=./eeprom_tool -w
    ...  eeprom_tool_update=./eeprom_tool -u
    Step  3  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> Fan 1 <<
    ...  path=${openbmc_fan_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d -f 1
    ...  eeprom_tool_write=./eeprom_tool -w -f 1
    ...  eeprom_tool_update=./eeprom_tool -u -f 1
    Step  4  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> Fan 2 <<
    ...  path=${openbmc_fan_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d -f 2
    ...  eeprom_tool_write=./eeprom_tool -w -f 2
    ...  eeprom_tool_update=./eeprom_tool -u -f 2
    Step  5  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> Fan 3 <<
    ...  path=${openbmc_fan_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d -f 3
    ...  eeprom_tool_write=./eeprom_tool -w -f 3
    ...  eeprom_tool_update=./eeprom_tool -u -f 3
    Step  6  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> Fan 4 <<
    ...  path=${openbmc_fan_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d -f 4
    ...  eeprom_tool_write=./eeprom_tool -w -f 4
    ...  eeprom_tool_update=./eeprom_tool -u -f 4
    Step  7  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> Fan 5 <<
    ...  path=${openbmc_fan_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d -f 5
    ...  eeprom_tool_write=./eeprom_tool -w -f 5
    ...  eeprom_tool_update=./eeprom_tool -u -f 5
    Step  8  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> Fan 6 <<
    ...  path=${openbmc_fan_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d -f 6
    ...  eeprom_tool_write=./eeprom_tool -w -f 6
    ...  eeprom_tool_update=./eeprom_tool -u -f 6
    Step  9  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> FCB <<
    ...  path=${openbmc_fcb_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d
    ...  eeprom_tool_write=./eeprom_tool -w
    ...  eeprom_tool_update=./eeprom_tool -u
    Step  10  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> Switch <<
    ...  path=${openbmc_switch_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d
    ...  eeprom_tool_write=./eeprom_tool -w
    ...  eeprom_tool_update=./eeprom_tool -u
    Step   11  Edit eeprom.cfg, write, update and dump to verify
    ...  log_msg_header=>> System <<
    ...  path=${openbmc_system_fru_eeprom_path}
    ...  eeprom_tool_dump=./eeprom_tool -d
    ...  eeprom_tool_write=./eeprom_tool -w
    ...  eeprom_tool_update=./eeprom_tool -u


SHAMU_DIAG_TC051_SOFTWARE TEST
      [Tags]  SHAMU_DIAG_TC051_SOFTWARE TEST  shamu
      step  1  open prompt and login to root user  console=${diagos_mode}
      step  2  check OS version
      step  3  sonic switch to openbmc console
      step  4  run version dump
      step  5  check software test

SHAMU_DIAG_TC055_POWER MONITOR_TEST
     [Tags]  SHAMU_DIAG_TC055_POWER MONITOR_TEST  shamu
     step  1  sonic switch to openbmc console
     step  2  check power monitor
     step  3  run power monitor
     step  4  run cmd sensors

SHAMU_DIAG_TC057_EMMC TEST
     [Tags]  SHAMU_DIAG_TC057_EMMC TEST  shamu
     step  1  sonic switch to openbmc console
     step  2  cel emmc test
     step  3  cel emmc info
     step  4  cel emmc pass

SHAMU_DIAG_TC058_TEMPERATURE TEST
     [Tags]  SHAMU_DIAG_TC058_TEMPERATURE TEST  shamu
     step  1  sonic switch to openbmc console
     step  2  check help option
     step  3  run cmd sensors
     step  4  cel temperature test

SHAMU_DIAG_TC061_BMC_CONTROL_CPU_POWER
    [Tags]   SHAMU_DIAG_TC061_BMC_CONTROL_CPU_POWER  shamu
    [Setup]  change kernel log level  console=${openbmc_mode}  level=3

    Step  1   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh cycle
    ...  msg=Failed, not success to cycle the Microserver Power!
    ...  is_check_exit_code=${FALSE}
    ...  sec=300
    Sleep  7s
    Step  2   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh status
    ...  pattern=(?i)Microserver power is (?P<result>off)
    ...  msg=Failed, the Microserver Power is not off!
    ...  is_check_exit_code=${FALSE}
    ...  sec=300
    Sleep  30s
    Step  3   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh status
    ...  pattern=(?i)Microserver power is (?P<result>on)
    ...  msg=Failed, the Microserver Power is not on!
    ...  is_check_exit_code=${FALSE}
    ...  sec=300
    Step  4   OpenBMC switch to SONiC console
    Step  5   read until pattern  pattern=\ login:  sec=300

    Step  6   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh off
    ...  pattern=(?i)Power.*?microserver.*?(?P<result>Done)
    ...  msg=Failed, not success to turn off the Microserver Power!
    ...  is_check_exit_code=${FALSE}
    ...  sec=300
    Step  7   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh status
    ...  pattern=(?i)Microserver power is (?P<result>off)
    ...  msg=Failed, the Microserver Power is not off!
    ...  is_check_exit_code=${FALSE}
    ...  sec=300
    Step  8   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh on
    ...  pattern=(?i)Power.*?microserver.*?(?P<result>Done)
    ...  msg=Failed, not success to turn on the Microserver Power!
    ...  is_check_exit_code=${FALSE}
    ...  sec=300
    Step  9   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh status
    ...  pattern=(?i)Microserver power is (?P<result>on)
    ...  msg=Failed, the Microserver Power is not on!
    ...  is_check_exit_code=${FALSE}
    ...  sec=300
    Step  10  open prompt  ${diagos_mode}  sec=300

    [Teardown]  Run Keywords
    ...  recover cpu  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7


SHAMU_DIAG_TC065_MDIO_BCM54616_TEST
    [Tags]   SHAMU_DIAG_TC065_MDIO_BCM54616_TEST  shamu

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  path=${openbmc_diag_bin_path}
    ...  command=./cel-mdio-test -h
    ...  patterns=${openbmc_mdio_help_patterns}
    ...  msg=Failed to verify -h/help option!
    Step  2  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  path=${openbmc_diag_bin_path}
    ...  command=./cel-mdio-test -t
    ...  patterns=${openbmc_mdio_test_patterns}
    ...  msg=Failed to verify mdio test option!


SHAMU_DIAG_TC066_MDIO_BCM5387_TEST
    [Tags]   SHAMU_DIAG_TC066_MDIO_BCM5387_TEST  shamu

    Step  1   execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=mdio-util
    ...  patterns=${openbmc_mdio_util_help_patterns}
    ...  msg=Failed to verify command usage!
    ...  is_check_exit_code=${FALSE}
    Step  2   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=(printf "y\n" | bcm5387.sh --mode mdio)
    Step  3   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=mdio-util -s read 0x1e 0x34 0x00
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?mi)^(?P<default>0x[0-9a-fA-F]{2})$
    ...  msg=Failed to read from MDIO!
    set test variable  ${mdio_default}  ${match}
    Step  4   execute command and verify with unexpected patterns
    ...  console=${openbmc_mode}
    ...  command=mdio-util -s write 0x1e 0x34 0x00 0xaa
    ...  patterns=${openbmc_mdio_write_unexpected_patterns}
    ...  msg=Failed to write 0xaa to MDIO!
    Step  5   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=mdio-util -s read 0x1e 0x34 0x00
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?mi)^(?P<read>0xaa)$
    ...  msg=Failed to read from MDIO, expected to get 0xaa!
    Step  6   execute command and verify with unexpected patterns
    ...  console=${openbmc_mode}
    ...  command=mdio-util -s write 0x1e 0x34 0x00 ${mdio_default}[default]
    ...  patterns=${openbmc_mdio_write_unexpected_patterns}
    ...  msg=Failed to write ${mdio_default}[default] to MDIO!
    Step  7  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=mdio-util -s read 0x1e 0x34 0x00
    ...  path=${openbmc_diag_bin_path}
    ...  pattern=(?mi)^(?P<read>${mdio_default}[default])$
    ...  msg=Failed to read from MDIO, expected to get ${mdio_default}[default]!
    [teardown]  reboot openbmc


SHAMU_DIAG_TC070_UART_MUX_Function_TEST
    [Tags]   SHAMU_DIAG_TC070_UART_MUX_Function_TEST  shamu
    Step  1  open prompt and login to root user  console=${openbmc_mode}
    Step  2  ifconfig and cat  openbmc
    Step  3  open prompt and login to root user  console=${diagos_mode}
    Step  4  ifconfig and cat  diagos

SHAMU_DIAG_TC073_RTC_TEST
    [Tags]   SHAMU_DIAG_TC073_RTC_TEST  shamu
    Step  1  open prompt and login to root user  console=${openbmc_mode}
    Step  2  rtc Option Test  -h
    Step  3  rtc Option Test  -t

SHAMU_DIAG_TC074_DDR_STRESS_TEST
    [Tags]   SHAMU_DIAG_TC074_DDR_STRESS_TEST  shamu
    Step  1  open prompt and login to root user  console=${openbmc_mode}
    Step  2  ddr Option Test
    Step  3  cat Ddr Log

SHAMU_DIAG_TC075_EMMC_STRESS_TEST
    [Tags]   SHAMU_DIAG_TC075_EMMC_STRESS_TEST  shamu
    Step  1  open prompt and login to root user  console=${openbmc_mode}
    Step  2  emmc Option Help Test
    Step  3  emmc Option Test
    [TearDown]  emmc Option C Test

SHAMU_DIAG_TC076_AVS_ON_SWITCH_CHIP_TEST
    [Tags]  SHAMU_DIAG_TC076_AVS_ON_SWITCH_CHIP_TEST  shamu
    Step  1  open prompt and login to root user  console=${openbmc_mode}
    Step  2  avs Option Help Test
    Step  3  avs Option Test

SHAMU_DIAG_TC077_RACK_TEST
    [Tags]  SHAMU_DIAG_TC077_RACK_TEST  shamu
    Step  1  open prompt and login to root user  console=${openbmc_mode}
    Step  2  check Fan Eeprom Info
    Step  3  open prompt and login to root user  console=${diagos_mode}
    Step  4  test 40 Loopback  ${test40_pattern}
    Step  5  check Confighwsku File
    Step  6  run Ali Diag Center

SHAMU_DIAG_TC032_INTERNEL_USB_TEST
    [Tags]  SHAMU_DIAG_TC032_INTERNEL_USB_TEST  shamu
    Step  1  sonic switch to openbmc console
    Step  2  execute command  ifconfig usb0 192.168.1.11 up
    Step  3  OpenBMC switch to SONiC console
    Step  4  execute command  ifconfig usb0 192.168.1.12 up
    Step  5  exec ping  DUT  192.168.1.11  5
    step  6  sonic switch to openbmc console
    step  7  exec ping  DUT  192.168.1.12  5
    Step  8  open prompt and login to root user  console=${diagos_mode}
    Step  9  check address info

SHAMU_DIAG_TC068_MAster_BIOS_AND_SLAVE_BIOS_TEST
     [Tags]  SHAMU_DIAG_TC068_MAster_BIOS_AND_SLAVE_BIOS_TEST  shamu
     step  1  sonic switch to openbmc console
     step  2  check openbmc master bios
     step  3  come reset slave
     step  4  OpenBMC switch to SONiC console
     step  5  sonic switch to openbmc console
     step  6  check openbmc slave bios
     step  7  come reset master
     step  8  OpenBMC switch to SONiC console
     step  9  sonic switch to openbmc console
     step  10  check openbmc master bios

SHAMU_DIAG_TC069_MASTER_BMC_AND_SLAVE_BMC_TEST
     [Tags]  SHAMU_DIAG_TC069_MASTER_BMC_AND_SLAVE_BMC_TEST  shamu
     step  1  sonic switch to openbmc console
     step  2  check openbmc master info
     step  3  boot from slave openbmc
     step  4  check openbmc slave info
     [Teardown]  boot from master openbmc

SHAMU_DIAG_TC070_BMC_FAMWARE_Update
     [Tags]  SHAMU_DIAG_TC070_BMC_FAMWARE_Update  shamu
     Step  1  open prompt and login to root user  console=${openbmc_mode}
     step  2  change dir  ${openbmc_exe_path}
     step  3  execute command  dhclient eth0
     step  4  download image  DUT  BMC  upgrade=${FALSE}
     step  5  curl to check bmc version  none
     step  6  change dir  ${openbmc_tmp}
     step  7  flashcp update bmc ver  5  old
     step  8  reboot Openbmc
     step  9  curl to check bmc version  none
     step  10  powerCycleToOpenbmc
     step  12  open prompt and login to root user  console=${openbmc_mode}
     step  13  change dir  ${openbmc_tmp}
     step  14  curl to check bmc version  False
     step  15  execute command  dhclient eth0
     step  16  download image  DUT  BMC  upgrade=${TRUE}
     step  17  flashcp update bmc ver  11  new
     step  18  open prompt and login to root user  console=${openbmc_mode}
     step  19  change dir  ${openbmc_exe_path}
     step  20  source and reboot boot  Slave
     step  21  curl to check bmc version  True
     Step  22  powerCycleToOpenbmc
     Step  23  source and reboot boot  Master
     [Teardown]  return to master mode
