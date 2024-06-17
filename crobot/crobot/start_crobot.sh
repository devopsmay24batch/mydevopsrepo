#!/bin/bash
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

##########################################################################################################################################################
# How to run crobot:   ./start_crobot.sh <TEST_TYPE> <PLATFORM_SKU_TYPE> <TEST_TAG> <LOOP_COUNT> <optional EXIT_CONDITION> <optional CYCLE_COUNT>
# where <optional EXIT_CONDITION> can be EXIT_ON_ERROR(default) or NO_EXIT;
# default <LOOP_COUNT> is 1; default <CYCLE_COUNT> is 1
# Example1: continue rest of testcases even when encounter error, with loop count=1 and cycle count=2:
#               ./start_crobot.sh diag Wedge400 Wedge400 1 NO_EXIT 2
# Example2: exit test immediately when encounter error, with loop count=1 and cycle count=2:
#               ./start_crobot.sh diag Wedge400 Wedge400 1 EXIT_ON_ERROR 2
##########################################################################################################################################################
# default loop count
loopCount=1
# default exit Condition
exitCondition=EXIT_ON_ERROR
# default cycle count
cycleCount=1
excludeTag="none"
# default critical tag
criticalTag="none"
##################################### tradational, can be removed if don't use location parameter any more => ####################################
opt_flag=`echo "$1" |grep -Eco "-"` #remove if don't use location parameter any more
if [ "$opt_flag" = "0" ];then #remove if don't use location parameter any more
  suite=$1
  platform=$2
  tag=$3
  if [ "$#" -eq 8 ]; then
    loopCount=$4
    exitCondition=$5
    cycleCount=$6
    excludeTag=$7
    criticalTag=$8
  elif [ "$#" -eq 7 ]; then
    loopCount=$4
    exitCondition=$5
    cycleCount=$6
    excludeTag=$7
  elif [ "$#" -eq 6 ]; then
    loopCount=$4
    exitCondition=$5
    cycleCount=$6
  elif [ "$#" -eq 5 ]; then
    loopCount=$4
    exitCondition=$5
  elif [ "$#" -eq 4 ]; then
    loopCount=$4
  elif [ "$#" -lt 3 ]; then
          echo "Usage: $0 <TEST_TYPE> <PLATFORM_SKU_TYPE> <TEST_TAG> <optional LOOP_COUNT> <optional EXIT_CONDITION> <optional CYCLE_COUNT> <optional EXCLUDE_TAG>"
  	echo "       where <optional EXIT_CONDITION> can be EXIT_ON_ERROR(default) or NO_EXIT;"
  	echo "             default <LOOP_COUNT> is 1; default <CYCLE_COUNT> is 1"
          echo "Example1: continue rest of testcases even when encounter error, with loop count=1 and cycle count=2:
  	               ./start_crobot.sh diag Wedge400 Wedge400 1 NO_EXIT 2"
          echo "Example2: exit test immediately when encounter error, with loop count=1 and cycle count=2:
  	               ./start_crobot.sh diag Wedge400 Wedge400 1 EXIT_ON_ERROR 2"
          echo "Example3: run all testcases except those with tag depend_sdk:
  	               ./start_crobot.sh diag wedge400c_d4 FB* 1 NO_EXIT 1 depend_sdk"
          echo "Example4: set the critical test with tag 'critical' in order to exit on failure only if critical test failed:
  	               ./start_crobot.sh diag wedge400c_d4 FB* 1 EXIT_ON_ERROR 1 none critical"
          exit 1
  fi
################################# <= tradational, can be removed if don't use location parameter any more #######################################################
else #remove if don't use location parameter any more
  show_usage="Usage:\n
                 -s, --suite            \t\ttest suite, such as diag, openbmc, sdk\n
                 -p, --platform         \tplatform name, such as minipack2_10002, wedge400c_d3 and etc.\n
                 -t, --tag              \t\ttest tag\n
                 -l, --loop             \t\ttest loop count, default 1\n
                 -e, --exitCondition    \texit condition, choices: EXIT_ON_ERROR, NO_EXIT, default: EXIT_ON_ERROR\n
                 -c, --cycle            \t\tcycle count, default 1\n
                 -x, --exclude          \t\texclude tag, default 'none'\n
                 -C, --critical         \tcritical tag, default 'none'\n
                 -h, --help             \t\tprint out usage\n\n

                 Example:\n
                 \tbash $0 -s sdk -p wedge400c_d3 -t FB* "

  set --  `getopt \
          -o s:p:t:l:e:c:x:C:h \
          -l suite:,platform:,tag:,loop:,exitCondition:,cycle:,exclude:,critical:,help \
  		-n "$show_usage" -- "$@"`
  while [ -n "$1" ]
  do
      option_value=`echo $2 | sed -e "s/^'//" -e "s/'$//"`
      case $1 in
          -s|--suite)
                  suite=$option_value
                  shift 2
                  ;;
          -p|--platform)
                  platform=$option_value
                  shift 2
                  ;;
          -t|--tag)
                  tag=$option_value
                  shift 2
                  ;;
          -l|--loop)
                  loopCount=$option_value
                  shift 2
                  ;;
          -e|--exitCondition)
                  exitCondition=$option_value
                  shift 2
                  ;;
          -c|--cycle)
                  cycleCount=$option_value
                  shift 2
                  ;;
          -x|--exclude)
                  excludeTag=$option_value
                  shift 2
                  ;;
          -C|--critical)
                  criticalTag=$option_value
                  shift 2
                  ;;
          -h|--help) echo -e $show_usage; exit 0;;
          --) shift; break;;
           *) echo -e $show_usage; exit 1;;
      esac
  done

fi #remove if options is new style
if [ -z "$suite" -o -z "$platform" -o -z "$tag" ];then
  echo "Error: Parameter suite, platform and tag are required"
  echo -e $show_usage
  exit 1
fi
export PYTHONPATH=$PYTHONPATH:$(pwd)\
:$(pwd)/../common/commonlib\
:$(pwd)/../platform/kapok/bsp\
:$(pwd)/../platform/kapok/diag\
:$(pwd)/../platform/ali\
:$(pwd)/../platform/ali/diag\
:$(pwd)/../platform/ali/openbmc\
:$(pwd)/../platform/ali/stress

python3 CRobot.py $suite $platform $tag $loopCount $exitCondition $cycleCount $excludeTag $criticalTag
