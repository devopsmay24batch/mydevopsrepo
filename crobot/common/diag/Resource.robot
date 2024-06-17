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
*** Settings ***
Library           Collections
Library           String
Library           DiagLibAdapter.py
Variables         Diag_OS_variable.py


*** Variables ***
${exit_code_zero}        (?m)^0$


*** Keywords ***
WPL Set Library Order
    WPL_DiagSetLibraryOrder


WPL Init Test Library
    WPL_DiagInitTestLibrary   device=None


verify "fpga scm r 0-4" on CentOS prompt
    [Documentation]  verify "fpga scm r 0-4" on CentOS prompt
    FOR  ${i}  ${e}  IN ENUMERATE  @{mp2_fpga_scm_r_0_to_4}
        Execute command and verify pattern list
        ...  path=${FPGA_TOOL_PATH}
        ...  command=./fpga scm r ${i}
        ...  console=CentOS
        ...  sec=60
        ...  regex=${e}
    END


verify "fpga -h" on CentOS prompt
    [Documentation]  verify "fpga -h" and "fpga scm r 0-4" on CentOS prompt

    Execute command and verify with paired & ordered pattern list
    ...  path=${FPGA_TOOL_PATH}
    ...  command=./fpga -h
    ...  console=CentOS
    ...  sec=60
    ...  regex=${mp2_fpga_h}


verify "ifconfig -a" on OpenBMC prompt with its show interface(s)
    [Documentation]  verify "cel-eth-test -s" on OpenBMC prompt with its show interface(s)

    ${output}=  execute "ifconfig -a" on OpenBMC prompt and wait for 60 second(s)
    FOR    ${if}    IN    @{cel_eth_test_s_pattern}
        should contain  ${output}  ${if}  ignore_case=True
        ...  msg=Not found an interface name "${if}"
    END

show cel-qsfp-test help menu with short and long options
    [Documentation]  Show cel-qsfp-test help menu with short and long options

    run and verify for centos
    ...  tool=./${cel_qsfp_test["bin_tool"]}
    ...  args=-h

    run and verify for centos
    ...  tool=./${cel_qsfp_test["bin_tool"]}
    ...  args=--help


set QSFP reset and low power modes to default
    [Documentation]  Set QSFP reset and low power status to default

    turn off QSFP reset mode with short option
    trun on QSFP low power mode with short option


verify individually QSFP port status
    [Documentation]  Verify the QSFP port status with short and long options
    [Arguments]  ${number}

    FOR    ${port}    IN RANGE    1    ${number}+1
        ${pattern}=  Create List    ^(?! )1.*${port}${cel_qsfp_test_port_status_default}[0]

        verify QSFP port status with short option
        ...  port=${port}
        ...  regex=${pattern}
        verify QSFP port status with long option
        ...  port=${port}
        ...  regex=${pattern}
    END


verify individually QSFP EEPROM information
    [Documentation]  verify individually QSFP EEPROM information with short and long options
    [Arguments]  ${number}

    FOR    ${port}    IN RANGE    1    ${number}+1
        ${pattern}=    Create List    ${cel_qsfp_test_eeprom_pattern}[0]

        verify QSFP EEPROM information with short option
        ...  port=${port}
        ...  regex=${pattern}
        verify QSFP EEPROM information with long option
        ...  port=${port}
        ...  regex=${pattern}
    END


turn ${x} QSFP reset mode with short option
    [Documentation]  Turn on/off QSFP reset mode with short option

    ${exit_code}=  change the current directory to ${DIAG_TOOL_PATH} for CentOS prompt and wait for 60 second(s)
    Search for a regex pattern
    ...  text=${exit_code}
    ...  regex=${exit_code_zero}
    ...  msg=Failed to change directory to ${DIAG_TOOL_PATH}, it may not exist!

    ${output}=  execute "./${cel_qsfp_test['bin_tool']} -p=0 -r ${x}" on CentOS prompt and wait for 60 second(s)
    should not contain  ${output}  ERROR  ignore_case=True


turn ${x} QSFP reset mode with long option
    [Documentation]  Turn on/off QSFP reset mode with long option

    ${exit_code}=  change the current directory to ${DIAG_TOOL_PATH} for CentOS prompt and wait for 60 second(s)
    Search for a regex pattern
    ...  text=${exit_code}
    ...  regex=${exit_code_zero}
    ...  msg=Failed to change directory to ${DIAG_TOOL_PATH}, it may not exist!

    ${output}=  execute "./${cel_qsfp_test['bin_tool']} --port=0 --reset ${x}" on CentOS prompt and wait for 60 second(s)
    should not contain  ${output}  ERROR  ignore_case=True


trun ${x} QSFP low power mode with short option
    [Documentation]  Turn on/off QSFP low power mode with short option

    ${exit_code}=  change the current directory to ${DIAG_TOOL_PATH} for CentOS prompt and wait for 60 second(s)
    Search for a regex pattern
    ...  text=${exit_code}
    ...  regex=${exit_code_zero}
    ...  msg=Failed to change directory to ${DIAG_TOOL_PATH}, it may not exist!

    ${output}=  execute "./${cel_qsfp_test['bin_tool']} -p=0 -l ${x}" on CentOS prompt and wait for 60 second(s)
    should not contain  ${output}  ERROR  ignore_case=True


trun ${x} QSFP low power mode with long option
    [Documentation]  Turn on/off QSFP low power mode with long option

    ${exit_code}=  change the current directory to ${DIAG_TOOL_PATH} for CentOS prompt and wait for 60 second(s)
    Search for a regex pattern
    ...  text=${exit_code}
    ...  regex=${exit_code_zero}
    ...  msg=Failed to change directory to ${DIAG_TOOL_PATH}, it may not exist!

    ${output}=  execute "./${cel_qsfp_test['bin_tool']} --port=0 --lpmode ${x}" on CentOS prompt and wait for 60 second(s)
    should not contain  ${output}  ERROR  ignore_case=True


verify QSFP port status with short option
    [Documentation]  verify QSFP port status with short option
    [Arguments]  ${port}=0  ${regex}=  ${match_count}=-1

    run and verify for centos
    ...  tool=./${cel_qsfp_test["bin_tool"]}
    ...  args=-s -p ${port}
    ...  regex=${regex}
    ...  match_count=${match_count}


verify QSFP port status with long option
    [Documentation]  verify QSFP port status with long option
    [Arguments]  ${port}=0  ${regex}=  ${match_count}=-1

    run and verify for centos
    ...  tool=./${cel_qsfp_test["bin_tool"]}
    ...  args=--status --port=${port}
    ...  regex=${regex}
    ...  match_count=${match_count}


verify QSFP EEPROM information with short option
    [Documentation]  verify QSFP EEPROM information with short option
    [Arguments]  ${port}=0  ${regex}=  ${match_count}=-1

    run and verify for centos
    ...  tool=./${cel_qsfp_test["bin_tool"]}
    ...  args=-i -p ${port}
    ...  regex=${regex}
    ...  match_count=${match_count}


verify QSFP EEPROM information with long option
    [Documentation]  verify QSFP EEPROM information with long option
    [Arguments]  ${port}=0  ${regex}=  ${match_count}=-1

    run and verify for centos
    ...  tool=./${cel_qsfp_test["bin_tool"]}
    ...  args=--info --port=${port}
    ...  regex=${regex}
    ...  match_count=${match_count}


verify QSFP automaticaly
    [Documentation]  verify QSFP automaticaly
    [Arguments]  ${option}=-a  ${regex}=

    run and verify for centos
    ...  tool=./${cel_qsfp_test["bin_tool"]}
    ...  args=${option}
    ...  regex=${regex}


verify a disk.dump file was removed after ran "cel-emmc-test -a"
    [Documentation]  Verify a disk.dump files should be auto-remove
    ...  after run cel-emmc-test -a
    [Arguments]  ${where}=${BMC_DIAG_TOOL_PATH}

    ${exit_code_zero} =    Create List    ^0$
    ${exit_code_one} =     Create List    ^1$

    run and verify for openbmc
    ...  prefix=
    ...  tool=test
    ...  args=-d ${where}; echo $?
    ...  regex=${exit_code_zero}

    run and verify for openbmc
    ...  prefix=
    ...  tool=find
    ...  args=${where}/disk.dump; echo $?
    ...  regex=${exit_code_one}


# Common utilities
request for ${console} prompt with timeout ${sec} second(s)
    [Documentation]  Open the ${console} prompt and wait for ${sec}
    ...  to execute next command

    prompt
    ...  mode=${prompt}
    ...  timeout=${sec}


get recently exit code on ${console} prompt and wait for ${sec} second(s)
    [Documentation]  Verify an exit code for previously executed command

    ${exit_code}=  execute command
    ...  cmd=echo $?
    ...  mode=${console}
    ...  timeout=${sec}

    [Return]  ${exit_code}


change the current directory to ${path} for ${console} prompt and wait for ${sec} second(s)
    [Documentation]  Go to the given directory

    ${exit_code}=  execute command
    ...  cmd=cd ${path}; echo $?
    ...  mode=${console}
    ...  timeout=${sec}

    [Return]  ${exit_code}


execute "${command}" on ${console} prompt and wait for ${sec} second(s)
    [Documentation]  Execute "${command}" on ${console} prompt

    ${output}=  execute command
    ...  cmd=${command}
    ...  mode=${console}
    ...  timeout=${sec}

    [Return]  ${output}


Search for regex pattern list with paired and ordered matches
    [Documentation]  Search for regular expression list through the text line-by-line
    ...  with paired and ordered matches of the line and pattern and raised an error message
    ...  if not found
    [Arguments]
    ...  ${text}=
    ...  @{regex}=
    ...  ${msg}=Be sure your given pattern(s) to search is properly paired and ordered with${\n}your expected result

    Should Not Be Empty  ${regex}  A regex is empty!

    @{_lines}=  Split To Lines  ${text}

    FOR  ${_offset_line}  ${_line}  IN ENUMERATE  @{_lines}
        ${_status}  ${_value}=  Run Keyword And Ignore Error
        ...  Should Match Regexp  ${_line}  ${regex}[0]
        ...  values=False

        Run Keyword If  '${_status}' == 'PASS'
        ...  Exit For Loop
    END

    Run Keyword If  '${_status}' == 'FAIL'
    ...  Fail  Not found first pattern:${\n * 2}${regex}[0]

    @{lines}=  Get Slice From List  ${_lines}  ${_offset_line}

    FOR  ${line}  ${re}  IN ZIP  ${lines}  ${regex}
        Should Match Regexp  ${line}  ${re}
        ...  Not matched:${\n * 2}${SPACE * 3}text = ${line}${\n}pattern = ${re}${\n * 2}${msg}
    END


Search for regex pattern list
    [Documentation]  Search for regular expression list through the text line-by-line
    ...  and raised an error message if not found
    [Arguments]
    ...  ${text}=
    ...  @{regex}=
    ...  ${msg}=Be sure your given pattern(s) to search is properly ordered with your${\n}expected result

    Should Not Be Empty  ${regex}  A regex is empty!

    @{lines}=  Split To Lines  ${text}
    ${regex_index}=  Set Variable  ${0}
    ${number_of_regex}=  Get Length  ${regex}

    FOR  ${line}  IN  @{lines}
        ${re}=  Get From List  ${regex}  ${regex_index}

        ${status}  ${value}=  Run Keyword And Ignore Error
        ...  Should Match Regexp  ${line}  ${re}
        ...  values=False

        ${regex_index}=  Set Variable If  '${status}' == 'PASS'
        ...  ${regex_index+1}  ${regex_index}

        Exit For Loop If  ${regex_index} > ${number_of_regex-1}
    END

    Run Keyword If  ${regex_index} < ${number_of_regex}
    ...  Fail  Not found pattern(s) or it may not in properly ordered:${\n * 2}${re}${\n * 2}${msg}


Search for a regex pattern
    [Documentation]  Search for a regular expression through the text line-by-line
    ...  and raised an error message if not found
    [Arguments]
    ...  ${text}=
    ...  ${regex}=
    ...  ${msg}=Be sure your given pattern matches to expected result

    Should Not Be Empty  ${regex}  A regex is empty!

    @{lines}=  Split To Lines  ${text}
    ${number_of_line}=  Get Length  ${lines}

    FOR  ${line_index}  ${line}  IN ENUMERATE  @{lines}
        ${status}  ${value}=  Run Keyword And Ignore Error
        ...  Should Match Regexp  ${line}  ${regex}
        ...  values=False

        Exit For Loop If  '${status}' == 'PASS'

        Run Keyword If  ${line_index} >= ${number_of_line-1}
        ...  Fail  Not found pattern:${\n * 2}${regex}${\n * 2}${msg}
    END


Execute command and verify with paired & ordered pattern list
    [Documentation]  Execute command and verify with paired & ordered pattern list
    [Arguments]
    ...  ${path}=
    ...  ${command}=
    ...  ${console}=
    ...  ${sec}=60
    ...  ${regex}=

    ${exit_code}=  change the current directory to ${path} for ${console} prompt and wait for ${sec} second(s)
    Search for a regex pattern
    ...  text=${exit_code}
    ...  regex=${exit_code_zero}
    ...  msg=Failed to change directory to ${path}, it may not exist!

    ${output}=  execute "${command}" on ${console} prompt and wait for ${sec} second(s)
    ${exit_code}=  get recently exit code on ${console} prompt and wait for ${sec} second(s)
    Search for a regex pattern
    ...  text=${exit_code}
    ...  regex=${exit_code_zero}
    ...  msg=Command "${command}" not return zero / success
    Search for regex pattern list with paired and ordered matches
    ...  text=${output}
    ...  regex=@{regex}


Execute command and verify pattern list
    [Documentation]  Execute command and verify with paired & ordered pattern list
    [Arguments]
    ...  ${path}=
    ...  ${command}=
    ...  ${console}=
    ...  ${sec}=60
    ...  ${regex}=

    ${exit_code}=  change the current directory to ${path} for ${console} prompt and wait for ${sec} second(s)
    Search for a regex pattern
    ...  text=${exit_code}
    ...  regex=${exit_code_zero}
    ...  msg=Failed to change directory to ${path}, it may not exist!

    ${output}=  execute "${command}" on ${console} prompt and wait for ${sec} second(s)
    ${exit_code}=  get recently exit code on ${console} prompt and wait for ${sec} second(s)
    Search for a regex pattern
    ...  text=${exit_code}
    ...  regex=${exit_code_zero}
    ...  msg=Command "${command}" not return zero / success
    Search for a regex pattern
    ...  text=${output}
    ...  regex=${regex}
# End of common utilities
