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
import os
import sys
import re
import datetime
from subprocess import Popen, PIPE
from os.path import expanduser

HOME_DIR = expanduser("~")
ROBOT_CMD = (HOME_DIR + "/.local/bin/robot")
REBOT_CMD = (HOME_DIR + "/.local/bin/rebot")
if os.path.exists(ROBOT_CMD):
    ROBOT_DIR = (HOME_DIR + "/.local/lib/python3.6/site-packages/robot")
    ROBOT_LIB_DIR = (HOME_DIR + "/.local/lib/python3.6/site-packages/robot/libraries")
else:
    ROBOT_CMD = ("/usr/local/bin/robot")
    REBOT_CMD = ("/usr/local/bin/rebot")
    ROBOT_DIR = ("/usr/local/lib/python3.6/dist-packages/robot")
    ROBOT_LIB_DIR = ("/usr/local/lib/python3.6/dist-packages/robot/libraries")

curDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(curDir)
sys.path.append(parentDir)
sys.path.append(curDir)
sys.path.append(os.path.join(curDir, 'legacy'))
sys.path.append(os.path.join(parentDir, 'config'))
sys.path.append(os.path.join(parentDir, 'common'))
sys.path.append(os.path.join(parentDir, 'common', 'diag'))
sys.path.append(os.path.join(parentDir, 'common', 'bmc'))
sys.path.append(os.path.join(parentDir, 'common', 'commonlib'))
sys.path.append(os.path.join(parentDir, 'common', 'openbmc'))
sys.path.append(os.path.join(parentDir, 'common', 'sdk'))
sys.path.append(os.path.join(parentDir, 'common', 'system'))
sys.path.append(os.path.join(parentDir, 'common', 'bsp'))
sys.path.append(os.path.join(parentDir, 'platform'))
sys.path.append(os.path.join(parentDir, 'platform', 'dell'))
sys.path.append(os.path.join(parentDir, 'platform', 'facebook'))
sys.path.append(os.path.join(parentDir, 'platform', 'juniper'))
sys.path.append(os.path.join(parentDir, 'platform', 'google'))
sys.path.append(os.path.join(parentDir, 'platform', 'edk2'))
sys.path.append(os.path.join(parentDir, 'platform', 'edk2', 'sonic'))
sys.path.append(os.path.join(parentDir, 'platform', 'facebook', 'bmc'))
sys.path.append(os.path.join(parentDir, 'platform', 'whitebox'))
sys.path.append(os.path.join(parentDir, 'platform', 'whitebox', 'bmc'))
sys.path.append(os.path.join(parentDir, 'platform', 'whitebox', 'bios'))
sys.path.append(os.path.join(parentDir, 'platform', 'seastone'))
sys.path.append(os.path.join(parentDir, 'platform', 'seastone','diag'))
sys.path.append(os.path.join(parentDir, 'platform', 'seastone', 'bios'))
sys.path.append(os.path.join(parentDir, 'platform', 'seastone', 'onie'))
sys.path.append(os.path.join(parentDir, 'platform', 'moonstone'))
sys.path.append(os.path.join(parentDir, 'platform', 'moonstone','diag'))
sys.path.append(os.path.join(parentDir, 'platform', 'moonstone', 'bios'))
sys.path.append(os.path.join(parentDir, 'platform', 'moonstone', 'onie'))

sys.path.append(ROBOT_DIR)
sys.path.append(ROBOT_LIB_DIR)

import YamlParse

currentCase = None

def getWorkDir():
    curDir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(curDir)


def exe_cmd(cmd):
    os.system(cmd)

def getTagFromConfigFile():
    """ the tag got e.g.: ALI_**AND**AUTO_TC_002**OR**AUTO_TC_003**OR**AUTO_TC_006** """
    caseInfo = YamlParse.getTestCaseInfo()
    tag = caseInfo['prefix'] + '**AND**'
    tag += '**OR**'.join(caseInfo['cases'])
    tag += '**'
    return tag

def main(case, deviceName, testTag, loopCount, ExitCondition, cycleCount, excludeTag, criticalTag):
    outputName = "output"
    logName = "log"
    reportName = "report"
    if testTag == 'CONFIG_FILE':
        testTag = getTagFromConfigFile()
    criticalStr = ''
    if criticalTag != "none":
        criticalStr = " --critical " + criticalTag
    try:
        testSuits = YamlParse.getTestSuitInfo()
        testSuit = testSuits[case]
        robotFile = testSuit['robotFile']
        outputDir = testSuit['outputDir']
        title = testSuit['title']
        try:
            testTag = testTag + testSuit['testTag']
        except Exception:
            pass

        print ("robotFile: " + robotFile)
        print ("outputDir: " + outputDir)
        print ("title: " + title)
        print ("testTag: " + testTag)

        upperDeviceName = deviceName.upper()
        titleName = ("[" + upperDeviceName + "]\ " + title)
        combineTitleName = ("[" + upperDeviceName + "]\ Combined\ " + title)

        if loopCount.isnumeric() == False:
            print ("Error: <LOOP_COUNT> must be integer.")
            return

        if ExitCondition == 'EXIT_ON_ERROR':
            exitCond = " --ExitOnFailure "
        elif ExitCondition == 'NO_EXIT':
            exitCond = " "
        else:
            print ("Error: <EXIT_CONDITION> can only be <EXIT_ON_ERROR> or <NO_EXIT>.")
            return

        if cycleCount.isnumeric() == False:
            print ("Error: <LOOP_COUNT> must be integer.")
            return

        global currentCase
        currentCase = case
        os.environ['deviceName'] = deviceName
        # import common_lib
        from Device import Device
        # default runs full system stress test (all system stress test cases + FB_SYS_COMM_TCG1-18 + FB_SYS_COMM_TCG1-19 + FB_SYS_COMM_TCG1-20)
        FULL_SYSTEM_TEST_ENABLED = False
        if int(cycleCount) == 0:
            FULL_SYSTEM_TEST_ENABLED = False

        if ((case == 'system') or (case == 'minipack2_system') or (case == 'cloudripper_system')) and (FULL_SYSTEM_TEST_ENABLED == True):
            # run all system stress tests
            output_Name1 = (outputName + "1.xml")
            log_Name1 = (logName + "1.html")
            report_Name1 = (reportName + "1.html")
            titleName1 = ("System\ Stress\ Test")
            if case == 'system':
                robotFile1 = "../common/system/system.robot"
            elif case == 'minipack2_system':
                robotFile1 = "../common/system/minipack2_system.robot"
            else:
                robotFile1 = "../common/system/cloudripper_system.robot"
            outputDir1 = "output/system/"

            cmd = ROBOT_CMD + " -v LOOP_CNT:" + loopCount  + " --tagstatinclude " + testTag + " -i " + testTag + " -e " + excludeTag + criticalStr + " -N " + titleName1 + " -o " + output_Name1 + " -l " + log_Name1 + " -r " + report_Name1 + " --outputdir " + outputDir1 + exitCond + robotFile1
            print('cmd: ' + cmd)
            exe_cmd(cmd)

            # run all openbmc tests
            output_Name2 = (outputName + "2.xml")
            log_Name2 = (logName + "2.html")
            report_Name2 = (reportName + "2.html")
            titleName2 = ("FB_SYS_COMM_TCG1-18_Test_All_BMC_Function")
            if case == 'system':
                robotFile2 = "../common/openbmc/bmc.robot"
            elif case == 'minipack2_system':
                robotFile2 = "../common/openbmc/minipack2_bmc.robot"
            else:
                robotFile2 = "../common/openbmc/cloudripper_bmc.robot"
            outputDir2 = "output/openbmc/"
            cmd = ROBOT_CMD + " -v LOOP_CNT:" + loopCount  + " --tagstatinclude " + testTag + " -i " + testTag + " -e " + excludeTag + criticalStr + " -N " + titleName2 + " -o " + output_Name2 + " -l " + log_Name2 + " -r " + report_Name2 + " --outputdir " + outputDir2 + exitCond + robotFile2
            print('cmd: ' + cmd)
            exe_cmd(cmd)

            #run all diag tests
            output_Name3 = (outputName + "3.xml")
            log_Name3 = (logName + "3.html")
            report_Name3 = (reportName + "3.html")
            titleName3 = ("FB_SYS_COMM_TCG1-19_Test_All_Diag_Function")
            if case == 'system':
                robotFile3 = "../common/diag/diag.robot"
            elif case == 'minipack2_system':
                robotFile3 = "../common/diag/minipack2_diag.robot"
            else:
                robotFile3 = "../common/diag/cloudripper_diag.robot"
            outputDir3 = "output/diag/"
            cmd = ROBOT_CMD + " -v LOOP_CNT:" + loopCount  + " --tagstatinclude " + testTag + " -i " + testTag + " -e " + excludeTag + criticalStr + " -N " + titleName3 + " -o " + output_Name3 + " -l " + log_Name3 + " -r " + report_Name3 + " --outputdir " + outputDir3 + exitCond + robotFile3
            print('cmd: ' + cmd)
            exe_cmd(cmd)

            #run all sdk tests
            output_Name4 = (outputName + "4.xml")
            log_Name4 = (logName + "4.html")
            report_Name4 = (reportName + "4.html")
            titleName4 = ("FB_SYS_COMM_TCG1-20_Test_All_SDK_Function")
            if case == 'system':
                robotFile4 = "../common/sdk/sdk.robot"
            elif case == 'minipack2_system':
                robotFile4 = "../common/sdk/minipack2_sdk.robot"
            else:
                robotFile4 = "../common/sdk/cloudripper_sdk.robot"
            outputDir4 = "output/sdk/"
            cmd = ROBOT_CMD + " -v LOOP_CNT:" + loopCount  + " --tagstatinclude " + testTag + " -i " + testTag + " -e " + excludeTag + criticalStr + " -N " + titleName4 + " -o " + output_Name4 + " -l " + log_Name4 + " -r " + report_Name4 + " --outputdir " + outputDir4 + exitCond + robotFile4
            print('cmd: ' + cmd)
            exe_cmd(cmd)

            # combine 4 reports
            combineTitleName = ("[" + upperDeviceName + "]\ " + "System\ Stress\ Test")
            cmd = REBOT_CMD + " -d " + outputDir1 + " -o output.xml" + " -N " + combineTitleName
            cmd += (" " + outputDir1 + output_Name1)
            cmd += (" " + outputDir2 + output_Name2)
            cmd += (" " + outputDir3 + output_Name3)
            cmd += (" " + outputDir4 + output_Name4)
            print('cmd: ' + cmd)
            exe_cmd(cmd)
        else:
            if int(cycleCount) <= 1:
                output_Name = (outputName + ".xml")
                log_Name = (logName + ".html")
                report_Name = (reportName + ".html")
                cmd = ROBOT_CMD + " -v LOOP_CNT:" + loopCount + " --tagstatinclude " + re.split("AND|OR|NOT", testTag)[0] + " -i " + testTag + " -e " + excludeTag + criticalStr + " -N " + titleName + " -o " + output_Name + " -l " + log_Name + " -r " + report_Name + " --outputdir " + outputDir + exitCond + robotFile
                print('cmd: ' + cmd)
                exe_cmd(cmd)
            else:
                maxCycle = int(cycleCount) + 1
                for index in range(1, maxCycle):
                    output_Name = (outputName + str(index) + ".xml")
                    log_Name = (logName + str(index) + ".html")
                    report_Name = (reportName + str(index) + ".html")
                    testSuite_TitleName = (titleName + "\ " + str(index))
                    cmd = ROBOT_CMD + " -v LOOP_CNT:" + loopCount + " --tagstatinclude " + re.split("AND|OR|NOT", testTag)[0] + " -i " + testTag + " -e " + excludeTag + criticalStr + " -N " + testSuite_TitleName + " -o " + output_Name + " -l " + log_Name + " -r " + report_Name + " --outputdir " + outputDir + exitCond + robotFile
                    exe_cmd(cmd)
                    stop_test_flag = YamlParse.getTestConfig().get("stop_test")
                    if stop_test_flag:
                        maxCycle = index + 1
                        print("The Test Loop Will End Cause User Actively Stops")
                        break
                    merge_log_flag = YamlParse.getTestConfig().get("merge_log")
                    if merge_log_flag:
                        if os.path.exists(os.path.join(outputDir, "output.xml")):
                            os.remove(os.path.join(outputDir, "output.xml"))
                        combine_cmd = REBOT_CMD + " -d " + outputDir + " -o output.xml" + " -N " + combineTitleName
                        for existing_log in range(1, index + 1):
                            combine_cmd += (" %s%s%s.xml" % (outputDir, outputName, str(existing_log)))
                        exe_cmd(combine_cmd)
                        print("The logs of [%d] loops has been merged" % index)

                if os.path.exists(os.path.join(outputDir, "output.xml")):
                    os.remove(os.path.join(outputDir, "output.xml"))
                combine_cmd = REBOT_CMD + " -d " + outputDir + " -o output.xml" + " -N " + combineTitleName
                for existing_log in range(1, maxCycle):
                    combine_cmd += (" %s%s%s.xml" % (outputDir, outputName, str(existing_log)))
                exe_cmd(combine_cmd)

    except Exception as err:
        print(str(err))
    return



if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])


