#!/bin/bash

#================================================================
#   Copyright (C) 2019 Celestica Inc. All rights reserved.
#   
#   File Name   : SELPolicy.sh
#   Author      : Fred
#   Created Time: 2019年07月15日 星期一 11时23分17秒
#   Description : 
#
#================================================================

# BMC IP
bmcip=$1

# NetFn
netfn=0x32

# CMD
get_policy_cmd=0x7E
set_policy_cmd=0x7F

sel_policy=$2
sel_maxnum=$3

: ${bmcip:='10.204.121.23'}
: ${sel_policy:='1'}
: ${sel_maxnum:='65540'}

# IPMI Common Command 
ipmicmd="ipmitool -I lanplus -H $bmcip -U admin -P admin"

function Help
{
    echo -e "$0 Help:\n"
    echo -e " $0 <BMC IP> <SEL POLICY> <SEL NUM> "
    echo -e "\t <BMC IP>     xx.xx.xx.xx"
    echo -e "\t <SEL POLICY> 0 - Linear, 1 - Circular"
    echo -e "\t <SEL NUM>    Linear: 3639 , Circular: 65535"
}


function GetSELPolicy
{
    result=`$ipmicmd raw $netfn $get_policy_cmd | sed 's/^[ \t]*//g'` 
    echo "Get SEL Policy: "
    case $result in
        00) echo "Linear SEL" ;;
        01) echo "Circular SEL" ;;
        *)  echo "Command error: $result" ;;
    esac
}

function SetSELPolicy
{
    echo -n "Set SEL Policy to: "
    case $sel_policy in
        0) echo "Linear SEL" ;;
        1) echo "Circular SEL" ;;
        *)  echo "Command error: $result" ;;
    esac
    $ipmicmd raw $netfn $set_policy_cmd $sel_policy
}

function CheckSELInfo
{
    echo -e "\n\nSEL Info: "
    $ipmicmd sel info
}

function CheckSELList
{
    echo -e "\n\nSEL list: "
    $ipmicmd sel elist
}

function CheckSELListHead
{
    echo -e "\n\nThe first 10 SEL: "
    $ipmicmd sel elist | head -n 10
}

function CheckSELListTail
{
    echo -e "\n\nThe last 10 SEL: "
    $ipmicmd sel elist | tail -n 10
}

function ClearSEL
{
    echo -e "\n\nClear SEL entry: "
    $ipmicmd sel clear    
}

function GenerateFullSEL
{
    SNR_NUM=01
    SNR_TYPE=1
    EvMRev=4
    
    num=0

    max=$sel_maxnum

    echo -e "\n\nGenerate $max SEL entries: "

    while [ $num -le $max ]
    do
        $ipmicmd raw 0x04 0x02 $EvMRev $SNR_TYPE $SNR_NUM 1 0 0 0 >/dev/null
        printf "Generate SEL: %d\r" "$num"  
        sleep 0.2
                
        let num++  
    done
    printf "\n"
}

if [ $# == 0 ]; then
    Help
else    

    SetSELPolicy
    GetSELPolicy
    #ClearSEL
    #CheckSELInfo
    #CheckSELListHead
    GenerateFullSEL
    #CheckSELInfo
    #CheckSELListHead

fi

