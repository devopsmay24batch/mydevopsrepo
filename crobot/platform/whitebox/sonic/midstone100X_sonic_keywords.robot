# Script       : sonic_keywords.robot                                                                                  #
# Date         : 8/3/2021
# Author       : Yagami Jiang<yajiang@celestica.com>
# Description  : This script used as keywords in midstone100X_sonic.robot

*** Settings ***
Variables         midstone100X_sonic_variable.py
Library           midstone100X_sonic_lib.py
#Library           CommonLib.py
Library           ../WhiteboxLibAdapter.py
Resource          CommonResource.robot


*** Keywords ***
END AC And Connect OS
    Step  1  SetPduStatusConnectOS  reboot  ${PDU_Port}  600  60


END Switch Board CPLD Register Access
    FOR  ${index}  IN RANGE  0  4
        independent_step  1  SendCmdWithoutRule  echo 0xde > /sys/bus/i2c/devices/10-003${index}/setreg
        independent_step  2  SetWait  10
    END


Onie Connect Device
    OnieConnect


OS Connect Device
    OSConnect
    InitOSUser

OS Disconnect Device
    OSDisconnect









