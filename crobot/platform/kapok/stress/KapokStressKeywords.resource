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

*** Keywords ***
Print Loop Info
    [Arguments]    ${CUR_INDEX}  ${MAX_LOOP}
    KapokStressLib.Log Info  ********************************************************
    KapokStressLib.Log Info  *** Test Command Loop \#: ${CUR_INDEX} / ${MAX_LOOP} ***
    KapokStressLib.Log Info  ********************************************************

I2C bus scan stress test
    [Documentation]  I2C bus scan stress test
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-i2c-test --all
    ...  ${path}=${diag_tools_path}
    ...  ${pattern}=${i2c_bus_scan_stress_pass_pattern}

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=(${diag_export_env} ${command})
    ...  path=${path}
    ...  pattern=${pattern}
    ...  msg=Fail!I2C test Failed!
    ...  is_check_exit_code=${FALSE}

run all diagnostic test
    [Documentation]  run all diagnostic test
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-all-test --all
    ...  ${path}=${diag_tools_path}
    ...  ${pattern}=${diagnose_test_all_fail_pattern}
    ...  ${sec}=900

    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=(${diag_export_env} ${command})
    ...  path=${path}
    ...  pattern=${pattern}
    ...  msg=Should not found the fail pattern!
    ...  is_check_exit_code=${FALSE}
    ...  sec=${sec}
    Run Keyword If  '${status}' == 'PASS'
    ...  Fail  Failed for some command(s):${\n*2}Number:command name${\n}${matches}

U-Boot mdio read
    [Documentation]  U-Boot execute mdio read
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${args}=0 0.21

    execute command and verify exit code
    ...  console=${console}
    ...  command=mdio read ${args}

U-Boot sleep
    [Documentation]  U-Boot execute sleep
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${sleep}=1

    execute command and verify exit code
    ...  console=${console}
    ...  command=sleep ${sleep}

U-Boot tftpboot
    [Documentation]  U-Boot execute tftpboot
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${args}=0x08000000 uboot_stress.tar
    ...  ${patterns}=${uboot_tftpboot_patterns}
    ...  ${sec}=60

    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=tftpboot ${args}
    ...  patterns=${patterns}
    ...  msg=Failed to run tftpboot "${args}" on U-Boot!
    ...  sec=${sec}

Self Update Onie
    [Arguments]  ${version}
    Step  1  KapokCommonLib.boot Into Onie Rescue Mode
    Step  2  KapokStressLib.config static ip
    Step  3  KapokStressLib.onie Self Update  update=${version}
    Step  4  KapokStressLib.verify Onie And CPLD Version  version=${version}

Check network connectivity
    [Arguments]  ${MODE}
    execute_check_dict  DUT  ${ifconfig_a_cmd}  mode=${MODE}
    ...  patterns_dict=${fail_dict}  timeout=5  is_negative_test=True
    ${ip} =  get ip address from config  PC
    exec_ping  DUT  ipAddress=${ip}  count=5  mode=${MODE}

Stress Onie Connect Device
    StressOnieConnect

Stress Onie Disconnect Device
    StressOnieDisconnect
