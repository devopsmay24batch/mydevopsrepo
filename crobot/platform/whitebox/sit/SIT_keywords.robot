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
Variables         SIT_variable.py
Library           SITLib.py
#Library           CommonLib.py
Library           ../WhiteboxLibAdapter.py
Resource          CommonResource.robot


*** Keywords ***
Check System Information
    Run Keyword If  ${ExistBMC} == True
		...  Run Keywords  CheckFullyBMCVersion
        ...  AND  Step  1  Run Keyword And Continue On Failure  CheckSensorList
		...  AND  independent_step  2  CheckSdrInfo
		...  AND  independent_step  3  CheckFruListInfo
		...  AND  independent_step  4  CheckBMCIP
        ...  AND  independent_step  5  Run Keyword If  ${shared_flag} == True  GetBMCIp  shared
    independent_step  1  CheckLspciAllInfo
    independent_step  2  CheckLnKCapLnkSta
    independent_step  3  CheckBIOSVersion
    independent_step  4  CheckOSIp
    independent_step  5  CheckEthtoolSpeedLinkStatus
    independent_step  6  CheckMemtotalSize
    independent_step  7  CheckDmiMemoryInfo
    independent_step  8  CheckCpuInfo
    independent_step  9  CheckLsCpu
    independent_step  10  CheckLsBlk
    #Step  11  CheckSmartctlInfo
    independent_step  12  execute_cmd  fdisk -l


END AC And Connect OS
    Step  1  set_pdu_state_connect_os  reboot  ${PDU_Port}  180  30


END Kill Cpu full Process
    Step  1  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  2  KillProcess  memtester
    Step  3  KillProcess  fio
    Step  4  KillProcess  stressapptest
    Step  5  OS Disconnect Device












*** Keywords ***
OS Connect Device
    OSConnect
    InitOSUser
    init_stty
    execute_cmd  unset TMOUT

OS Disconnect Device
    OSDisconnect


########################################## Caleb Start ############################################################
Check System Information For One PSU
    Run Keyword If  ${ExistBMC} == True
		...  Run Keywords  CheckFullyBMCVersion
		...  AND  CheckFruListInfo
		...  AND  CheckBMCIP
        ...  AND  Run Keyword If  ${shared_flag} == True  GetBMCIp  shared
    Step  1  CheckLspciAllInfo
    Step  2  CheckLnKCapLnkSta
    Step  3  CheckBIOSVersion
    Step  4  CheckOSIp
    Step  5  CheckEthtoolSpeedLinkStatus
    Step  6  CheckMemtotalSize
    Step  7  CheckDmiMemoryInfo
    Step  8  CheckCpuInfo
    Step  9  CheckLsCpu
    Step  10  CheckLsBlk
    Step  11  CheckSmartctlInfo
    Step  12  execute_cmd  fdisk -l
########################################## Caleb END ##############################################################
