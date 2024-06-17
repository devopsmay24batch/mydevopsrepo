#!/bin/bash
##############################################################################################################
#   Copyright (C) 2019 Celestica Ltd. All rights reserved.
#
#   File Name       : SVT_bmc_sensor_read_stress.sh                               S
#   Created Time    : 7/10/2019
#   Applied Project : xxx
#   How to Use      : Copy the script into CPU OS, run the script directly
#                     1> Need to modify the discrete sensor name and correct sensor reading 
#                     2> Need to modify the threshold sensor name whose sensor reading can be ignored
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
LOG_NAME="bmc_sensor_read_stress.log" #To save the logs

#***************Define the discrete sensor name and correct sensor reading***************#
Discrete_Sensor_1="Fan1_Status"
declare +i Discrete_Sensor_1_correct="0x0280" #Define the correct status for discrete sensor "Fan1_Status"
Discrete_Sensor_2="Fan2_Status"
declare +i Discrete_Sensor_2_correct="0x0280" #Define the correct status for discrete sensor "Fan2_Status"
Discrete_Sensor_3="Fan3_Status"
declare +i Discrete_Sensor_3_correct="0x0280" #Define the correct status for discrete sensor "Fan3_Status"
Discrete_Sensor_4="Fan4_Status"
declare +i Discrete_Sensor_4_correct="0x0280" #Define the correct status for discrete sensor "Fan4_Status"
Discrete_Sensor_5="Fan5_Status"
declare +i Discrete_Sensor_5_correct="0x0280" #Define the correct status for discrete sensor "Fan5_Status"
Discrete_Sensor_6="Watchdog2"
declare +i Discrete_Sensor_6_correct="0x0080" #Define the correct status for discrete sensor "Watchdog2"
Discrete_Sensor_7="SEL"
declare +i Discrete_Sensor_7_correct="0x0480" #Define the correct status for discrete sensor "SEL"
Discrete_Sensor_8="Power_Status"
declare +i Discrete_Sensor_8_correct="0x0180" #Define the correct status for discrete sensor "Power_Status"
Discrete_Sensor_9="PSU1_Status"
declare +i Discrete_Sensor_9_correct="0x0480" #Define the correct status for discrete sensor "PSU1_Status"
Discrete_Sensor_10="PSU2_Status"
declare +i Discrete_Sensor_10_correct="0x0480" #Define the correct status for discrete sensor "PSU2_Status"
#***************Define the discrete sensor name and correct sensor reading***************#

#***************Define the threshold sensor name whose sensor reading can be ignored***************#
Threshold_Sensor_Filter_Arr=('SW_U33_Temp' 'SW_U21_Temp')
#***************Define the threshold sensor name whose sensor reading can be ignored***************#

count=1
AllPass=1
loop=$1
#Variables Definition
##############################################################################################################
My_log_path1="/home/sensor_scan"
if [ ! -d "$My_log_path1" ];then
	mkdir /home/sensor_scan
fi

function Check_Discrete_Sensor()
{
	#Sensor_name=`echo $1 | awk -F "|" '{print $1}' |sed 's/[[:space:]]//g'`
	Sensor_name=`echo $1 | awk -F "|" '{print $1}' | sed 's/[ \t]*$//g'`
	declare +i Sensor_reading=`echo $1 | awk -F "|" '{print $4}'|sed 's/[[:space:]]//g'`
	
	#Check discrete sensor reading Fan1_Status
	if [[ $Sensor_reading != $Discrete_Sensor_1_correct ]] && \
       [[ $Sensor_name == $Discrete_Sensor_1 ]]
	then
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Discrete Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi
	
	#Check discrete sensor reading Fan2_Status
	if [[ $Sensor_reading != $Discrete_Sensor_2_correct ]] && \
       [[ $Sensor_name == $Discrete_Sensor_2 ]]
	then
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Discrete Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi

	#Check discrete sensor reading Fan3_Status
	if [[ $Sensor_reading != $Discrete_Sensor_3_correct ]] && \
       [[ $Sensor_name == $Discrete_Sensor_3 ]]
	then
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Discrete Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi	
	
	#Check discrete sensor reading Fan4_Status
	if [[ $Sensor_reading != $Discrete_Sensor_4_correct ]] && \
       [[ $Sensor_name == $Discrete_Sensor_4 ]]
	then
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Discrete Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi

	#Check discrete sensor reading Fan5_Status
	if [[ $Sensor_reading != $Discrete_Sensor_5_correct ]] && \
       [[ $Sensor_name == $Discrete_Sensor_5 ]]
	then
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Discrete Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi	
	
	#Check discrete sensor reading Watchdog2
	if [[ $Sensor_reading != $Discrete_Sensor_6_correct ]] && \
       [[ $Sensor_name == $Discrete_Sensor_6 ]]
	then
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Discrete Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi	
	
	#Check discrete sensor reading SEL
	if [[ $Sensor_reading != $Discrete_Sensor_7_correct ]] && \
       [[ $Sensor_name == $Discrete_Sensor_7 ]]
	then
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Discrete Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi

    #Check discrete sensor reading Power_Status
	if [[ $Sensor_reading != $Discrete_Sensor_8_correct ]] && \
       [[ $Sensor_name == $Discrete_Sensor_8 ]]
	then
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Discrete Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi

    #Check discrete sensor reading PSU1_Status
	if [[ $Sensor_reading != $Discrete_Sensor_9_correct ]] && \
       [[ $Sensor_name == $Discrete_Sensor_9 ]]
	then
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Discrete Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi

    #Check discrete sensor reading PSU2_Status
	if [[ $Sensor_reading != $Discrete_Sensor_10_correct ]] && \
       [[ $Sensor_name == $Discrete_Sensor_10 ]]
	then
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Discrete Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi	
}

function Check_Threshold_Sensor()
{
	echo $1 | grep -w -E "nc|nr|cr" >> /dev/null 2>&1
    Sensor_status=`echo $?`
	declare +i Sensor_reading=`echo $1 | awk -F "|" '{print $2}'|sed 's/[[:space:]]//g'`
    Sensor_name=`echo $1 | awk -F "|" '{print $1}'| sed 's/[ \t]*$//g'`
    #Sensor_name=`echo $1 | awk -F "|" '{print $1}'|sed 's/[[:space:]]//g'`  
    Sensor_reading_na="na"
    declare +i Sensor_reading_zero="0.000"
	
	for sensor in "${Threshold_Sensor_Filter_Arr[@]}"
	do
		if [ "$sensor" == "$Sensor_name" ]
		then
			return
		fi
	done
	
	if [[ $Sensor_reading == $Sensor_reading_na ]] || \
       [[ $Sensor_reading == $Sensor_reading_zero ]] || \
       [[ "$Sensor_status" == "0" ]]
	then 
		sensor_number="0x"`$TOOL_PATH_IPMITOOL/ipmitool sdr elist|grep "$Sensor_name"|awk -F '|' '{print $2}'|cut -b 2,3`
		Sensor_reading_raw=`$TOOL_PATH_IPMITOOL/ipmitool raw 0x04 0x2d $sensor_number`
		echo -e "FAILED Threshold Sensor is $Sensor_name , Get raw sensor reading: $Sensor_reading_raw \n" >> $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1
		sync
		AllPass=0
	fi	
}

while [ $count -le $loop ]; do
	echo -e "==========================================Test Loop $count==========================================\n" 2>&1 | tee -a $LOG_PATH/$LOG_NAME 2>&1
	$TOOL_PATH_IPMITOOL/ipmitool sensor > $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log 2>&1

	while read LINE
	do
		Sensor_Type=`echo $LINE |awk -F '|' '{print $3}'|sed 's/[[:space:]]//g'`
		discrete_Sensor="discrete"
		if [ "$Sensor_Type" != "$discrete_Sensor" ]
		then
			Check_Threshold_Sensor "$LINE"
		elif [ "$Sensor_Type" == "$discrete_Sensor" ]
		then 
			Check_Discrete_Sensor "$LINE"
		fi
	done < $LOG_PATH/sensor_scan/sensor_scan_loop_$count.log

	if (($AllPass == "1"))
	then
		echo 'Sensor Scan PASSED'
		echo -e "Sensor Scan PASSED\n" >> $LOG_PATH/$LOG_NAME 2>&1
		sync
	else
		echo 'Sensor Scan FAILED'
		echo -e "Sensor Scan FAILED\n" >> $LOG_PATH/$LOG_NAME 2>&1
		sync
	fi
	count=$(($count + 1))
done
echo "Function END"
		

