#!/bin/bash
##############################################################################################################
#   Copyright (C) 2019 Celestica Ltd. All rights reserved.
#
#   File Name       : SVT_bmc_fru_read_stress.sh                               S
#   Created Time    : 7/10/2019
#   Applied Project : All AMI BMC platforms
#   How to Use      : Copy the script into CPU OS, run the script directly
#                     1> Need to burn correct FRU data before start this stress testing
##############################################################################################################

##############################################################################################################
# Version History:
#                 0.1 : 7/10/2019 Initial version by Claire Ren
#
##############################################################################################################

##############################################################################################################
#Variables Definition
LOG_PATH=/home/
SCRIPT_PATH=/home/
TOOL_PATH_IPMITOOL=/usr/bin/ #ipmitool absolute path
LOG_NAME="bmc_fru_read_stress.log" #To save the logs
count=1
loop=$1
#Variables Definition
##############################################################################################################

My_log_path1="/home/fru_scan"
if [ ! -d "$My_log_path1" ];then
	mkdir /home/fru_scan
fi

function CompareFRU
{
    fru_ref=$1
    $TOOL_PATH_IPMITOOL/ipmitool fru print >  $LOG_PATH/fru_scan/fru_print_loop_$count.log 2>&1

    diff $fru_ref $LOG_PATH/fru_scan/fru_print_loop_$count.log
    if [ $? == 0 ]; then
		echo 'FRU Test PASSED'
        echo -e "FRU Test PASSED \n" >> $LOG_PATH/$LOG_NAME 2>&1
    else
		echo 'FRU Test FAILED'
        echo -e "FRU Test FAILED \n" >> $LOG_PATH/$LOG_NAME 2>&1
    fi
}

$TOOL_PATH_IPMITOOL/ipmitool fru print > $LOG_PATH/fru_scan/fru_ref.log 2>&1

while [ $count -le $loop ]; do
	echo -e "==========================================Test Loop $count==========================================\n" 2>&1 | tee -a $LOG_PATH/$LOG_NAME 2>&1
	CompareFRU $LOG_PATH/fru_scan/fru_ref.log
	count=$(($count + 1))
done
echo "Function END"

		

