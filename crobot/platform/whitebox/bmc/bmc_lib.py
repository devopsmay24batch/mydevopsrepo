###############################################################################
# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
import re
from inspect import getframeinfo, stack
import os.path
import time
import yaml
import Logger as log
import CommonLib
import random
import Const
import bios_menu_lib
import openbmc_lib
import Const
import YamlParse
import Logger as log
import pexpect
import getpass
import os
import traceback
import parser_openbmc_lib
import json
from BIOS_variable import *
from BMC_variable import *
from datetime import datetime, timedelta
from dataStructure import nestedDict, parser
from errorsModule import noSuchClass, testFailed
from SwImage import SwImage
from Server import Server
from pexpect import pxssh
import sys
import getpass
import WhiteboxLibAdapter
import whitebox_lib

try:
    import parser_openbmc_lib as parserOpenbmc
    import DeviceMgr
    from Device import Device

except Exception as err:
    log.cprint(str(err))

deviceObj = DeviceMgr.getDevice()

def changePowerRestorePolicyStatus(device, ip, status, expectedvalue):
    """
    Set Power restore policy status to always off
    :param device       : product under test
    :param ip           : passing BMC IP
    :param expectedvalue: passing expected pattern 
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin raw 00 06 {status}"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd)
    if re.search(expectedvalue, output):
    	log.success("Verify IPMI command “Set Power Restore Policy” executed successfully")
    else:
        log.fail("Failed! IPMI command “Set Power Restore Policy” not executed :{output}")
        raise Exception("Failed! IPMI command “Set Power Restore Policy” not executed")

def verifyPowerRestorestatus(device, ip, exp_policy_status, exp_chassis_status, cycle=None):
    """
    verify the chassis power status and Power Restore Status through the BMC IP
    :param device            : product under test
    :param ip                : passing BMC IP 
    :param exp_policy_status : passing Expected Power Restore status
    :param exp_chassis_status: passing Expected Chassis power status
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin chassis status"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    power_restore_policy_status = re.findall(r"Power Restore Policy : (always-off|previous|always-on)", output, re.I|re.M)[0]
    Chassis_power_status = whitebox_lib.get_chassis_power_status(device=device, ip=ip)
    if (power_restore_policy_status == exp_policy_status) and (Chassis_power_status == exp_chassis_status):
        log.success(f"Verifed Power Restore Policy status is changed to {power_restore_policy_status} \
                \n      Chassis power status is {Chassis_power_status}")
    else:
        log.fail(f"Fail! Expected Power Restore Policy status:{exp_policy_status}, Power Restore Policy status:{power_restore_policy_status}")
        log.fail(f"Fail! Expected chassis power status:{exp_chassis_status}, chassis power status:{Chassis_power_status}")
        raise Exception("Fail! Power Restore Policy and chassis power status not matched")
    ChassisPower_Status = Chassis_power_status
    if cycle != None:
        if ChassisPower_Status == Chassis_power_status:
            log.success(f"Verifed the SUT power status is always restored last power state")
        else:
            log.fail(f"Fail! the SUT power status is not restored last power state")
            raise Exception("Fail! the SUT power status is not restored last power state")

def poweruptheunit(device, ip, exp_chassis_status):
    """
    After AC cycle, need to power up the unit through the BMC IP
    :param device            : product under test
    :param ip                : passing BMC IP
    :param exp_chassis_status: passing Expected Chassis power status
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin power on"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    time.sleep(120)
    Chassis_power_status = whitebox_lib.get_chassis_power_status(device=device, ip=ip)
    if Chassis_power_status == exp_chassis_status:
        log.success(f"Verifed Chassis power status is {Chassis_power_status}")
    else:
        log.fail(f"Fail! Expected chassis power status:{exp_chassis_status}, chassis power status:{Chassis_power_status}")
        raise Exception("Fail! Chassis power status not changed")

def verify_bmc_time_is_synced(device,time_output,dt=None):
    log.debug('Entering procedure verify_bmc_time_is_synced with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    line1 = '([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]).*([0-9][0-9]):([0-9][0-9]):([0-9][0-9])'

    match1 = re.search(line1, time_output)

    if match1:
        if match1.group(1) == dt['Month'] and match1.group(2) == dt['Day'] and match1.group(3) == dt['Year'] and match1.group(4) == dt['Hour']:
           log.success("BMC SEL Date and Time is in Sync with OS Time")
           Flag = True
    else:
        log.fail("BMC SEL Date and Time is not in Sync with OS Time")
        raise testFailed("BMC SEL Date and Time is not in Sync with OS Time")

def verifyIPMIcommandBMCcoldreset(device, ip):
    """
    Set Power restore policy status to always off
    :param device       : product under test
    :param ip           : passing BMC IP
    :param expectedvalue: passing expected pattern
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin mc reset cold"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    if re.search(r"Sent cold reset command to MC", output) and not(re.search("rror", output)):
        log.success("IPMI command BMC cold reset successfully")
    else:
        log.fail(f"Failed! IPMI command BMC cold reset :{output}")
        raise Exception("Failed! IPMI command not executed")

def verifyIPMIChassisControltopoweroffon(device, ip, status):
    """
    Set Power restore policy status to always off
    :param device       : product under test
    :param ip           : passing BMC IP
    :param expectedvalue: passing expected pattern
    """
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin raw 00 02 {status}"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    if not(re.search(r"Error|error", output)):
        log.success(f"IPMI command Chassis Control to power off/on the server successfully")
    else:
        log.fail(f"Failed! IPMI command Chassis Control not able to power off/on the server :{output}")
        raise Exception("Failed! IPMI command not executed")

def checkSensorList(Sensor_a, Sensor_b):
    non_match_Sensor = []
    match_Sensor= []
    for i in Sensor_a:
        if i not in Sensor_b:
            non_match_Sensor.append(i)
        else:
            match_Sensor.append(i)
    return non_match_Sensor,match_Sensor

def checkrange(Sensor_value, Upper_Non_Recoverable, Lower_Non_Critical=None):
    if Lower_Non_Critical != None:
        if float(Lower_Non_Critical) <= float(Sensor_value) <= float(Upper_Non_Recoverable):
            return True
        return False
    elif float(Sensor_value) <= float(Upper_Non_Recoverable):
        return True
    return False

def verifythesensorreadingandcheckwithfunspec(device, ip):
    """
    verify the all monitor sensors’ sensor reading and status through the BMC IP
    :param device            : product under test
    :param ip                : passing BMC IP
    """
    Total_Sensor=[]
    NotDetectTempSensor=[]
    Sensor_value=[]
    Sensor_Status=[]
    Lower_Non_Critical=[]
    Upper_Non_Recoverable=[]
    Sensor_value_verifed=[]
    value_not_in_range=[]
    SensorValueNotVerifed=[]

    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin sensor list"
    device_obj = Device.getDeviceObject(device)
    SensorList_output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    k = SensorList_output.split("\n")
    for i in k:
        if len(i) !=0:
            x = re.search(Sensor_pattern, i, re.I)
            Total_Sensor.append(x.group(1).replace(" ", ""))
            Sensor_value =x.group(2).replace(" ", "")
            Sensor_Status = x.group(3).replace(" ", "")
            Lower_Non_Critical = x.group(4).replace(" ", "")
            Upper_Non_Recoverable = x.group(9).replace(" ", "")
            z= Sensor_value+Lower_Non_Critical+Upper_Non_Recoverable+Sensor_Status
            if re.search(r"ok", z, re.I) and not(re.search(r"na", z, re.I)):
                if checkrange(Sensor_value,Upper_Non_Recoverable,Lower_Non_Critical):
                    Sensor_value_verifed.append(x.group(1))
                else:
                    value_not_in_range.append(x.group(1))
            elif re.search(r"ok", z, re.I) and (Lower_Non_Critical == "na"):
                if checkrange(Sensor_value,Upper_Non_Recoverable):
                    Sensor_value_verifed.append(x.group(1))
                else:
                    value_not_in_range.append(x.group(1))
            else:
                SensorValueNotVerifed.append(x.group(1))

    NotDetectTempSensor=checkSensorList(Temperature_SensorList,Total_Sensor)
    NotDetectVoltageSensor=checkSensorList(Voltage_SensorList,Total_Sensor)
    NotDetectPowerSupplySensor=checkSensorList(PowerSupply_SensorList,Total_Sensor)
    NotDetectFanSensor=checkSensorList(Fan_SensorList,Total_Sensor)
    NotDetectDiscreteSensor=checkSensorList(Discrete_SensorsList,Total_Sensor)
    log.debug(f"Detected total Sensor in device                     :{len(Total_Sensor)}")
    log.debug(f"As per functional spec total Temperature SensorList :{len(Temperature_SensorList)}")

    if len(Temperature_SensorList) == len(NotDetectTempSensor[1]):
        log.success(f"Temp Sensor detected      :{len(NotDetectTempSensor[1])}")
    else:
        log.fail(f"Temp Sensor not detected     :{len(NotDetectTempSensor[0])} out of {len(Temperature_SensorList)}")
        raise Exception(f"Failed! Temp Sensor not detected:{len(NotDetectTempSensor[0])}")
  
    log.debug(f"As per functional spec total Voltage SensorList :{len(Voltage_SensorList)}")
    if len(Voltage_SensorList) == len(NotDetectVoltageSensor[1]):
        log.success(f"Votage Sensor detected    :{len(NotDetectVoltageSensor[1])}")
    else:
        log.fail(f"Votage Sensor not detected   :{len(NotDetectVoltageSensor[0])} out of {len(Voltage_SensorList)}")
        raise Exception(f"Failed! Votage Sensor not detected   :{len(NotDetectVoltageSensor[0])}")

    log.debug(f"As per functional spec total PowerSupply SensorList :{len(PowerSupply_SensorList)}")
    if len(PowerSupply_SensorList) == len(NotDetectPowerSupplySensor[1]):
        log.success(f"PowerSupply Sensor detected   :{len(NotDetectPowerSupplySensor[1])}")
    else:
        log.fail(f"PowerSupply Sensor not detected  :{len(NotDetectPowerSupplySensor[0])} out of {len(PowerSupply_SensorList)}")
        raise Exception(f"Failed! PowerSupply Sensor not detected:{len(NotDetectPowerSupplySensor[0])}")

    log.debug(f"As per functional spec total Fan SensorList      :{len(Fan_SensorList)}")
    if len(Fan_SensorList) == len(NotDetectFanSensor[1]):
        log.success(f"Fan Sensor detected           :{len(NotDetectFanSensor[1])}")
    else:
        log.fail(f"Fan Sensor not detected          :{len(NotDetectFanSensor[0])} out of {len(Fan_SensorList)}")
        raise Exception(f"Failed! Fan Sensor not detected        :{len(NotDetectFanSensor[0])}") 

    log.debug(f"As per functional spec total Fan SensorList      :{len(Discrete_SensorsList)}")
    if len(Discrete_SensorsList) == len(NotDetectDiscreteSensor[1]):
        log.success(f"Discrete Sensor detected      :{len(NotDetectDiscreteSensor[1])}")
    else:
        log.fail(f"Discrete Sensor not detected     :{len(NotDetectDiscreteSensor[0])} out of {len(Discrete_SensorsList)}")
        raise Exception(f"Failed! Discrete Sensor not detected   :{len(NotDetectDiscreteSensor[0])}")

    log.debug(f"Total Sensor Detected as functional spec         :{len(NotDetectTempSensor[1])+len(NotDetectVoltageSensor[1])+len(NotDetectPowerSupplySensor[1])+len(NotDetectFanSensor[1])+len(NotDetectDiscreteSensor[1])}")
    log.debug(f"Verifed {len(Sensor_value_verifed)} Sensors out of {len(Total_Sensor)}")
    if (SensorValueNotVerifed == 0) and (value_not_in_range == 0):
        log.success(f"{len(SensorValueNotVerifed)} out of \
                {len(Total_Sensor)} Sensors are not verified due to Devise not Installed")
        log.success(f"{len(value_not_in_range)} out of \
                {len(Total_Sensor)} Sensors value are not in range when Status OK")
    elif SensorValueNotVerifed != 0:
        log.fail(f"{len(SensorValueNotVerifed)} out of \
                {len(Total_Sensor)} Sensors are not verified due to Devise not Installed")
        raise Exception("Failed! Sensors are not verified due to Devise not Installed")
    elif value_not_in_range != 0:
        log.fail(f"{len(value_not_in_range)} out of {len(Total_Sensor)}\
                Sensors value are not in range when Status OK")
        raise Exception("Failed! Sensors value are not in range when Status OK")


###############################################################################
#  validateAssetTag used to validate the chassis asset tag
#  Argument : output of the command dmidecode -s chassis-asset-tag
###############################################################################
def validateAssetTag(asset_tag_output):
    output=asset_tag_output.splitlines()
    pattern=" "
    count=0
    for line in output:
        match=re.search(pattern,line)
        log.info(line)
        if match:
            log.info("asset-tag check successful")
            count=count+1
            break
    if count == 0:
       log.fail("asset-tag check unsuccessful")
       raise Exception("asset-tag check unsuccessful")

def verify_power_cycle_after_watchdog_timer_expiry(device):
    log.debug('Entering procedure verify_power_cycle_after_watchdog_timer_expiry with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.read_until_regexp('Sending SIGKILL to remaining processes', timeout=60)
    match = re.search('Sending SIGKILL to remaining processes', output)
    if match:
        log.success("System Power Cycled successfully after watchdog timer expiry")
    else:
        log.fail("System waw not Power Cycled after watchdog timer expiry")
        raise testFailed("System waw not Power Cycled after watchdog timer expiry")

def verify_hard_reset_after_watchdog_timer_expiry(device):
    log.debug('Entering procedure verify_hard_reset_after_watchdog_timer_expiry with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.read_until_regexp('Linux version.*gcc version', timeout=200)
    match = re.search('Linux version.*gcc version', output)
    if match:
        log.success("System Hard reset successfully after watchdog timer expiry")
    else:
        log.fail("System waw not Hard reset after watchdog timer expiry")
        raise testFailed("System waw not Hard reset after watchdog timer expiry")

def verify_power_down_after_watchdog_timer_expiry(device):
    log.debug('Entering procedure verify_power_down_after_watchdog_timer_expiry with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.read_until_regexp('Starting Power-Off', timeout=200)
    match = re.search('Starting Power-Off', output)
    if match:
        log.success("System Power Down successfully after watchdog timer expiry")
    else:
        log.fail("System waw not Power Down after watchdog timer expiry")
        raise testFailed("System waw not Power Down after watchdog timer expiry")

def Verify_IPMI_Get_Watchdog_Timer_output(output1, output2, testname, expect_same=True):
    log.debug('Entering procedure Verify_IPMI_Get_Watchdog_Timer_output with args : %s\n' %(str(locals())))
    split_output1 = output1.splitlines()[1];
    split_output2 = output2.splitlines()[1];
    log.debug(split_output1)
    log.debug(split_output2)
    if expect_same:
        if split_output1 == split_output2:
            log.info("Successfully {}: {}".format(testname, output2))
        else:
            log.fail("Fail to {}".format(testname))
            raise RuntimeError("{}".format(testname))
    else:
        if split_output1 == split_output2:
            log.fail("Fail to {}".format(testname))
            raise RuntimeError("{}".format(testname))
        else:
            log.info("Successfully {}: {}".format(testname, output2))

def verifyeventlogSELclear(device, ip):
    cmd1 = f"ipmitool -I lanplus -H {ip} -U admin -P admin sel clear"
    cmd2 = f"ipmitool -I lanplus -H {ip} -U admin -P admin sel list"
    device_obj = Device.getDeviceObject(device)
    output1 = Device.execute_local_cmd(device_obj, cmd1)
    output2 = Device.execute_local_cmd(device_obj, cmd2)
    expectedoutput1='Clearing SEL.  Please allow a few seconds to erase.'
    expectedoutput2='Event Logging Disabled #0xa0 | Log area reset/cleared | Asserted'
    if re.search(expectedoutput1, output1) and not(re.search('rror', output1)):
        log.success('IPML command cleared SEL Successfully')
    else:
        log.fail(f'IPML command failed {output1}')
        raise RuntimeError("ESM Command Failed")
    if re.search(expectedoutput2, output2) and not(re.search('rror', output2)):
        log.success('SEL is cleared and SEL event log can be read out successfully')
    else:
        log.fail(f'SEL event log not able to read out successfully {output2}')
        raise RuntimeError("ESM Command Failed")


def installBMCFWimage(device,module,bmcupgrade=None,mseoption=None,PC=None,key='BIN'):
    log.debug("Entering install BMC FW image details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    cmd_FM_Version=str('ipmitool mc inforaw 6 1')
    if bmcupgrade == "upgrade":
        Imagedetail = imageObj.newImage[key]
        Versiondetail = imageObj.newVersion
    elif bmcupgrade == "downgrade":
        Imagedetail = imageObj.oldImage[key]
        Versiondetail = imageObj.oldVersion
    else:
        log.debug(f"There is no action on BMC FW")

    if mseoption!=None and PC!=None:
        toolname = str(f"./CFUFLASH -cd {Imagedetail} -mse {mseoption} -pc -fb")
    elif mseoption!=None and PC==None:
        toolname = str(f"./CFUFLASH -cd {Imagedetail} -mse {mseoption} -fb")
    else:
        toolname = str(f"./CFUFLASH -cd {Imagedetail} -mse 1 -fb")

    beforelog=whitebox_lib.execute(device, cmd_FM_Version, mode=None, timeout=20)
    cmd="./ipmi_driver.sh"
    whitebox_lib.execute(device, cmd, mode=None, timeout=20)
    cmd="rmmod ipmi_ssif"
    whitebox_lib.execute(device, cmd, mode=None, timeout=20)
    cmd="rmmod acpi_ipmi"
    whitebox_lib.execute(device, cmd, mode=None, timeout=20)
    log.info(f"{bmcupgrade} image :{Imagedetail} and version :{Versiondetail}")
    log.info(f"Final FW command :{toolname}")
    installationlog=whitebox_lib.execute(device, toolname, mode=None, timeout=500)
    log.info(installationlog)
    pass_message_1="Uploading Firmware Image : 100%... done"
    pass_message_2="Flashing  Firmware Image : 100%... done"
    pass_message_3="Verifying Firmware Image : 100%... done"
    pass_message_4="Beginning to Deactive flashMode...end"
    pass_message_5="Resetting the firmware.........."
    pass_message_6="Flasher Not Ready ! Please Try After Sometime"
    match1=re.search(pass_message_1,installationlog,re.I|re.M)
    match2=re.search(pass_message_2,installationlog,re.I|re.M)
    match3=re.search(pass_message_3,installationlog,re.I|re.M)
    match4=re.search(pass_message_4,installationlog,re.I|re.M)
    match5=re.search(pass_message_5,installationlog,re.I|re.M)
    match6=re.search(pass_message_6,installationlog,re.I|re.M)
    if match1 and match2 and match3 and match4 and match5:
        log.success(f"BMC FW {bmcupgrade} successfully with {module}")
    elif match6:
        raise RuntimeError(f"BMC FW {bmcupgrade} Failed due to {pass_message_6}")
    else:
        raise RuntimeError(f"BMC FW {bmcupgrade} Failed with {module}")

def checkinstalledBCMFWversion(device,module,ip,bmcupgrade=None):
    log.debug("Entering check installed BCM FW version details args : %s" %(str(locals())))
    cmd_FM_Version = f"ipmitool -I lanplus -H {ip} -U admin -P admin mc info"
    device_obj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    output = Device.execute_local_cmd(device_obj, cmd_FM_Version)
    log.info(output)
    CurrentFWversion=re.search(r"Firmware Revision\s+:\s(\d+.\d+)",output,re.I|re.M)[1]

    if bmcupgrade == "upgrade":
        Versiondetail = imageObj.newVersion
    elif bmcupgrade == "downgrade":
        Versiondetail = imageObj.oldVersion
    else:
        log.debug(f"There is no action on BMC FW")

    if CurrentFWversion == Versiondetail:
        log.success(f"FW {bmcupgrade} is success with {CurrentFWversion} version on {module}")
    else:
        raise RuntimeError(f"FW {bmcupgrade} version {Versiondetail} not success and system current version {CurrentFWversion} on {module}")

def verifyabnormaleventlog(device, ip):
    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin sel list"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd)
    expectedoutput='abnormal'
    if re.search(expectedoutput, output) and re.search('rror', output):
        log.fail(f"Abnormal event recorded in SEL :{output}")
        raise RuntimeError('Abnormal event recorded in SEL')
    else:
        log.success('Abnormal event message is not recorded in SEL')


def verifyDCcycleBMCIP(device, ip):
    cmd1 = f"ipmitool -I lanplus -H {ip} -U admin -P admin power reset"
    expectedoutput1='Chassis Power Control: Reset'
    device_obj = Device.getDeviceObject(device)
    output1 = Device.execute_local_cmd(device_obj, cmd1)
    if re.search(expectedoutput1, output1) and not(re.search('rror', output1)):
        log.success('DC cycle reset Successfully')
    else:
        log.fail(f'DC cycle reset failed :{output1}')
        raise RuntimeError('DC cycle reset failed through BMC IP')

def verifyACcycleBMCIP(device, ip):
    cmd1 = f"ipmitool -I lanplus -H {ip} -U admin -P admin power cycle"
    expectedoutput1='Chassis Power Control: Cycle'
    device_obj = Device.getDeviceObject(device)
    output1 = Device.execute_local_cmd(device_obj, cmd1)
    if re.search(expectedoutput1, output1) and not(re.search('rror', output1)):
        log.success('AC cycle reset Successfully')
    else:
        log.fail(f'AC cycle reset failed :{output1}')
        raise RuntimeError('AC cycle reset failed through BMC IP')

def Generate_SEL_Logs(device,module="Athena_FW",key='SEL_GEN'):
    log.debug("Entering Generate_SEL_Logs with args : %s" %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    imageObj = SwImage.getSwImage(module)
    localdir = imageObj.localImageDir
    deviceObj.sendline('cd %s' %(localdir))
    sel_gen = imageObj.newImage[key]
    toolname='./%s' %(sel_gen)

    msg="Looks like SEL Log is Full"
    deviceObj.sendCmd(toolname,msg,10000)

    log.debug("Exited Generate_SEL_Logs proc")

def upgrade_bmc_FW(device,module,key='IMA'):
    log.debug("Entering upgrade_bmc_FW with args : %s" %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    localdir = imageObj.localImageDir
    deviceObj.sendline('cd %s' %(localdir))
    toolname='./CFUFLASH -cd -fb'

    cmd="./ipmi_driver.sh"
    execute(device, cmd)
    cmd="rmmod ipmi_ssif"
    execute(device, cmd)
    cmd="rmmod acpi_ipmi"
    execute(device, cmd)
    err_count = 0
    timeout = 500
    package_file = imageObj.newImage[key]
    cmd="{} {}".format(toolname,package_file)
    log.info(cmd)
    msg="Resetting the firmware.........."
    deviceObj.sendCmd(cmd,msg,500)

def compare_fru_info_before_and_after_reset_powercycle(output1, output2):
    log.debug('Entering procedure compare_fru_info_before_and_after_reset_powercycle with args : %s\n' %(str(locals())))
    count=0
    output1_split=output1.splitlines()
    for line in output1_split:
        count=count+1
        if count > 2 and '(' not in line and '[' not in line :
             match=re.search(line,output2)
             if match:
                 log.info("succesfully verified {}".format(line))
             else:
                 log.fail("Fail to verify {}".format(line))
                 raise RuntimeError("Fru info mismatch before and after cold reset/power cycle")


def compare_mc_info_before_and_after_reset(output1, output2):
    log.debug('Entering procedure compare_mc_info_before_and_after_reset with args : %s\n' %(str(locals())))
    pattern1="Firmware Revision.*: (\S+)"
    pattern2="Manufacturer ID.*: (\S+)"
    pattern3="Manufacturer Name.*: Unknown \((\S+)\)"
    pattern4="Product ID.*: (\S+) \((\S+)\)"
    pattern5="Product Name.*: Unknown \((\S+)\)"
    output1_split=output1.splitlines()
    for line in output1_split:
        match1=re.search(pattern1,line)
        match2=re.search(pattern2,line)
        match3=re.search(pattern3,line)
        match4=re.search(pattern4,line)
        match5=re.search(pattern5,line)
        if match1:
            version=match1.group(1)
        if match2:
            mfg_id=match2.group(1)
        if match3:
            mfg_name=match3.group(1)
        if match4:
            pdct_id_1=match4.group(1)
            pdct_id_2=match4.group(2)
        if match5:
            pdct_name=match5.group(1)
    pattern1="Firmware Revision.*: {}".format(version)
    pattern2="Manufacturer ID.*: {}".format(mfg_id)
    pattern3="Manufacturer Name.*: Unknown \({}\)".format(mfg_name)
    pattern4="Product ID.*: {} \({}\)".format(pdct_id_1,pdct_id_2)
    pattern5="Product Name.*: Unknown \({}\)".format(pdct_name)
    match1=re.search(pattern1,output2)
    match2=re.search(pattern2,output2)
    match3=re.search(pattern3,output2)
    match4=re.search(pattern4,output2)
    match5=re.search(pattern5,output2)
    if match1:
        log.info("Firmware Revision check successful")
    else:
        log.info("Firmware Revision check Failed")
        raise RuntimeError("Firmware Revision check Failed")
    if match2:
        log.info("Manufacturer ID check successful")
    else:
        log.info("Manufacturer ID check Failed")
        raise RuntimeError("Manufacturer ID check Failed")
    if match3:
        log.info("Manufacturer Name check successful")
    else:
        log.info("Manufacturer Name check Failed")
        raise RuntimeError("Manufacturer Name check Failed")
    if match4:
        log.info("Product ID check successful")
    else:
        log.info("Product ID check Failed")
        raise RuntimeError("Product ID check Failed")
    if match4:
        log.info("Product Name check successful")
    else:
        log.info("Product Name check Failed")
        raise RuntimeError("Product Name check Failed")

################################################################################
# Function Name : verify_boot_sequence
# Parameters :
#    device             : Device Object
#    bios_password      : BIOS Password (This can vary depending on setup)
#
# Description: Goes into BIOS setup screen and check the boot sequence is not changed
#              after set to “Force boot into BIOS Setup”
################################################################################

def verify_boot_sequence(device,bios_password='c411ie'):
    log.info("Inside verify_boot_sequence procedure")
    deviceObj = Device.getDeviceObject(device)

    enter_bios_afterpowercycle(device,bios_password)

    bios_menu_lib.send_key(device, "KEY_RIGHT",times=6) #key_strokes_to_reach_boot_menu
    bios_menu_lib.send_key(device, "KEY_RIGHT",times=3) #key_strokes_to_reach_boot_option_1

    bios_menu_lib.send_key(device, "KEY_ENTER")

    line2 = 'Boot Option #1'
    output = deviceObj.read_until_regexp(line2, timeout=60)
    line3 = 'MTFDDAV240TDU'
    output = deviceObj.read_until_regexp(line3, timeout=60)
    if output:
        log.success("Device boot into BIOS setup screen and the boot sequence is not changed")
        log.success("The boot options can be set to “Force boot into BIOS Setup” successfully")
    else:
        raise RuntimeError("Device boot into BIOS setup screen and the boot sequence is changed")

    bios_menu_lib.send_key(device, "KEY_ESC")
    time.sleep(5)
    bios_menu_lib.exit_bios_1(device)

    log.debug("Device booting up and Sleeping 90 sec....")
    time.sleep(90)

def enter_bios_afterpowercycle(device,bios_password='c411ie'):
    log.debug('Entering procedure enter_bios_afterpowercycle with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    line1 = 'Enter Password'
    output = None
    output = deviceObj.read_until_regexp(line1, timeout=120)
    bios_menu_lib.send_key(device, "KEY_ENTER")

    if output is not None:
        result=deviceObj.sendline(bios_password)
        time.sleep(10)
    else:
        log.fail("Failed enter Bios Setup")
        raise testFailed("enter_bios_setup")

def Check_unit_auto_boot_to_UEFI_PXE_page(device,validation):
    log.debug('Entering procedure Check_unit_auto_boot_to_UEFI_PXE_page with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    pass_message_1="Checking Media Presence"
    pass_message_2="ERROR: Boot option loading failed"
    match1 = deviceObj.read_until_regexp(pass_message_1, timeout=150)
    match2 = deviceObj.read_until_regexp(pass_message_2, timeout=150)
    if match1 and match2:
        log.fail(f"Fail! PXE Page and Server not connected due to timeout with {validation}")
        raise RuntimeError("PXE Page and Server not connected due to timeout")
    else:
        log.success(f"Successfully! PXE Server is connected with {validation}")

def verify_command_execution(device,ip,cmd,fail_pattern):
    cmd = "{} {}".format(cmd,ip)
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    if re.search(fail_pattern, output):
        log.fail("Command not executed successfully")
        raise testFailed("Command not executed successfully")
    else:
        log.success("Command executed successfully")

def verify_bmc_version_ip_ipmitool(device, cmd1, cmd2, expected_result=None):
    """
    verify the BMC Version through the BMC IP
    :param device            : product under test
    :param cmd1              : passing BMC IP #ipmitool raw 6 1
    :param cmd2              : passing BMC IP #ipmitool raw 0x06 0x01
    """
    log.debug('Entering procedure verify_bmc_version_ip_ipmitool with args : %s\n' % (str(locals())))
    output1 = whitebox_lib.execute(device, cmd1, mode=CENTOS_MODE)
    output2 = whitebox_lib.execute(device, cmd2, mode=CENTOS_MODE)
    p1=r"[0-9]+\s[0-9]+\s[0-9]([0-9])\s([0-9]+)"
    match1 = re.search(p1, output1)
    result1=f"{match1.group(1)}.{match1.group(2)}"
    match2 = re.search(p1, output2)
    result2=f"{match1.group(1)}.{match1.group(2)}"
    if result1 == result2:
        log.success(f"Successfully verify_bmc_version_ip_ipmitool :{result1}")
    else:
        raise RuntimeError(f"Failed! BMC Version not matching : {result1} and {result2}")

def verifythesensorreadingandcheckstatus(device, ip):
    """
    verify the all monitor sensors reading and status through the BMC IP
    :param device            : product under test
    :param ip                : passing BMC IP
    """
    Total_Sensor=[]
    Sensor_Status_verifed=[]
    Sensor_value=[]
    Sensor_Status=[]
    Lower_Non_Critical=[]
    Upper_Non_Recoverable=[]
    Sensor_value_verifed=[]
    value_not_in_range=[]
    SensorValueNotVerifed=[]

    cmd = f"ipmitool -I lanplus -H {ip} -U admin -P admin sensor list"
    device_obj = Device.getDeviceObject(device)
    SensorList_output = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    k = SensorList_output.split("\n")
    for i in k:
        if len(i) !=0:
            x = re.search(Sensor_pattern, i, re.I)
            Total_Sensor.append(x.group(1).replace(" ", ""))
            Sensor_value =x.group(2).replace(" ", "")
            Sensor_Status = x.group(3).replace(" ", "")
            Lower_Non_Critical = x.group(4).replace(" ", "")
            Upper_Non_Recoverable = x.group(9).replace(" ", "")
            z= Sensor_value+Lower_Non_Critical+Upper_Non_Recoverable+Sensor_Status
            if re.search(r"ok", z, re.I) and not(re.search(r"na|nr", z, re.I)):
                if checkrange(Sensor_value,Upper_Non_Recoverable,Lower_Non_Critical):
                    Sensor_value_verifed.append(x.group(1))
                    Sensor_Status_verifed.append(x.group(0))
                else:
                    value_not_in_range.append(x.group(1))
            else:
                SensorValueNotVerifed.append(x.group(1))
    log.debug(f"Detected total Sensor in device                     :{len(Total_Sensor)}")
    log.debug("The following Sensor's Status verifed")
    for i in Sensor_Status_verifed:
        log.success(f"{i}")

def compare_mc_info_before_and_after_powercycle(output1,output2):
    log.debug('Entering procedure compare_mc_info_before_and_after_powercycle')
    pattern1="Firmware Revision.*: (\S+)"
    log.info(output1)
    log.info(output2)
    output1_split=output1.splitlines()
    for line in output1_split:
        match1=re.search(pattern1,line)
        if match1:
            version=match1.group(1)
    pattern1="Firmware Revision.*: {}".format(version)
    match1=re.search(pattern1,output2)
    if match1:
        log.info("Firmware Revision check successful")
    else:
        log.info("Firmware Revision check Failed")
        raise RuntimeError("Firmware Revision check Failed")

def check_ipmitool_BMC_version(version,expected_version):
    log.debug("Entering procedure to  validate BMC version")
    p1=r"[0-9]+\s[0-9]+\s([0-9]+)\s([0-9]+)"
    match1 = re.search(p1, version)
    result1=f"{match1.group(1)} {match1.group(2)}"
    log.info(result1)
    if result1 == expected_version:
        log.info("BMC Version matches as expected")
    else:
        log.info("version mismatch")
        raise RuntimeError("BMC Firmware Revision check Failed")

def getBMCFWimageversion(device,module,cmd1,cmd2,bmcupgrade=None):
    log.debug("Entering get BMC FW image version details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    output1 = whitebox_lib.execute(device, cmd1, mode=CENTOS_MODE)
    output2 = whitebox_lib.execute(device, cmd2, mode=CENTOS_MODE)
    log.debug(output1)
    log.debug(output2)
    if bmcupgrade == "upgrade":
        VersiondetailA = imageObj.newVersion
        BMC_version='0'+VersiondetailA[0]
    elif bmcupgrade == "downgrade":
        VersiondetailA = imageObj.oldVersion
        BMC_version ='0'+VersiondetailA[0]
    else:
        log.debug("There is no action")

    if re.search(BMC_version, output1) and re.search(BMC_version, output2):
        log.success(f"PASS! Verifed BMC version {BMC_version} after {bmcupgrade} successfully with {module}")
    else:
        log.fail(f"Failed! Verifed BMC version {BMC_version} after {bmcupgrade} successfully with {module}")

def get_bmc_version_ipmitool(device,ip):
    log.debug("Entering get_bmc_version_ipmitool details args : %s" %(str(locals())))
    cmd_FM_Version = f"ipmitool -I lanplus -H {ip} -U admin -P admin mc info"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd_FM_Version)
    log.info(output)
    CurrentFWversion=re.search(r"Firmware Revision\s+:\s(\d+.\d+)",output,re.I|re.M)[1]
    return CurrentFWversion

def get_SOL_info_remote_client(device,ip,sol_active1,sol_progress1='set-complete'):
    log.debug("Entering get_SOL_info_remote_client details args : %s" %(str(locals())))
    cmd_sol_info = f"ipmitool -I lanplus -H {ip} -U admin -P admin sol info"
    device_obj = Device.getDeviceObject(device)
    output = Device.execute_local_cmd(device_obj, cmd_sol_info)
    sol_progress=re.search(r"Set in progress\s+:\s(.*)",output,re.I|re.M)[1]
    sol_active=re.search(r"Enabled\s+:\s(.*)",output,re.I|re.M)[1]
    if sol_active1 == sol_active and sol_progress == sol_progress1:
        log.success(f"Pass! SOL operation is {sol_active} from ipmitool")
        log.success(f"Pass! SOL \"Set in progress\" is {sol_progress} from ipmitool")
    else:
        log.fail(f"Fail! SOL operation is {sol_active} from ipmitool")
        log.fail(f"Fail! SOL \"Set in progress\" is {sol_progress} from ipmitool")
        raise RuntimeError("Fail! SOL \"Set in progress\" is not set-complete from ipmitool")

def set_SOL_looptest(device,ip,testloopcycle):
    log.debug("Entering set_SOL_looptest details args : %s" %(str(locals())))
    cmd_sol_testloop = f"ipmitool -I lanplus -H {ip} -U admin -P admin sol looptest {testloopcycle} 5000 1"
    device_obj = Device.getDeviceObject(device)
    Looptest_timeout=int(testloopcycle) * 6
    log.debug(f"Sleep {Looptest_timeout} seconds for loop test completion")
    output = Device.execute_local_cmd(device_obj, cmd_sol_testloop, timeout=int(Looptest_timeout)).strip()
    log.info(output)
    match1=re.search(r"(remain loop test counter: 1$)",output,re.I|re.M)[1]
    if match1:
        log.success(f"Successfully! SOL loop test is completed")
    else:
        raise RuntimeError(f"Fail! SOL loop test is not completed within expected time")

def compare_mc_info(output1,output2):
    log.debug('Entering procedure compare mc info before and after with some action')
    pattern1="Firmware Revision.*: (\S+)"
    output1_split=output1.splitlines()
    for line in output1_split:
        match1=re.search(pattern1,line)
        if match1:
            version=match1.group(1)
    pattern1="Firmware Revision.*: {}".format(version)
    match1=re.search(pattern1,output2)
    if match1:
        log.info("Firmware Revision check successful")
    else:
        log.info("Firmware Revision check Failed")
        raise RuntimeError("Firmware Revision check Failed")

def get_BIOS_version(device):
    log.debug("Entering get BIOS version details args : %s" %(str(locals())))
    cmd = "dmidecode -t 0"
    device_obj = Device.getDeviceObject(device)
    output = whitebox_lib.execute(device, cmd, mode=CENTOS_MODE)
    log.info(output)
    CurrentBIOSversion=re.search(r"BIOS Revision: (\S+)",output,re.I|re.M)[1]
    log.debug(f"Installed BIOS version :{CurrentBIOSversion}")
    return CurrentBIOSversion

def compare_BIOS_info(output1,output2):
    log.debug("Entering procedure compare BIOS info before and after with some action: %s" %(str(locals())))
    pattern1="BIOS Revision: (\S+)"
    output1_split=output1.splitlines()
    for line in output1_split:
        match1=re.search(pattern1,line)
        if match1:
            version=match1.group(1)
    pattern1="BIOS Revision: {}".format(version)
    match1=re.search(pattern1,output2)
    if match1:
        log.info("BIOS Revision check successful")
    else:
        log.info("BIOS Revision check Failed")
        raise RuntimeError("BIOS Revision check Failed")

def update_bios_FW(device,toolname,package_file):
    log.debug("Entering procedure update_bios_FW")
    deviceObj = Device.getDeviceObject(device)
    cmd="./ipmi_drive.sh"
    whitebox_lib.execute(device, cmd)
    cmd="rmmod ipmi_ssif"
    whitebox_lib.execute(device, cmd)
    cmd="rmmod acpi_ipmi"
    whitebox_lib.execute(device, cmd)
    cmd="{} {} -fb".format(toolname,package_file)
    log.info(cmd)
    output=whitebox_lib.execute(device, cmd, mode=None, timeout=500)
    log.info(output)
    pass_message_1="Uploading Image : 100%... done"
    pass_message_2="Flashing  Firmware Image : 100%... done"
    pass_message_3="Verifying Firmware Image : 100%... done"
    pass_message_4="Beginning to Deactive flashMode...end"
    pass_message_5="Resetting the firmware........."
    match1=re.search(pass_message_1,output)
    match2=re.search(pass_message_2,output)
    match3=re.search(pass_message_3,output)
    match4=re.search(pass_message_4,output)
    match5=re.search(pass_message_5,output)
    if match1 and match2 and match3 and match4 and match5:
        log.success("BIOS upgraded successfully")
    else:
        raise RuntimeError("BIOS Upgrade Failed")

def get_EventTimestamp_sel_list(sel_list_output):
    log.debug("Entering procedure get_EventTimestamp_sel_list: %s" %(str(locals())))
    pattern = r'^\W\s+2\s+\|\s+(\d{1,2}/\d{1,2}/\d{2,4})\s+\|\s+([0-9]{2}:[0-9]{2}:[0-9]{2})'
    if sel_list_output:
        match=re.search(pattern, sel_list_output, re.I|re.M)
        date_var = match.group(1).replace("/", "-")
        data_var_next = match.group(2) + "+00:00"
        date_update = date_var.split("-")
        date_update=date_update[2] + "-" + date_update[0] + "-" + date_update[1]
        return date_update + "T" + data_var_next
    else:
        log.fail("Sel output is not valide")

def upgrade_bmc_with_bios_image(device,toolname,imagename):
   log.debug("Entering procedure to upgrade bmc with bios image")
   cmd="./ipmi_driver.sh"
   whitebox_lib.execute(device, cmd, mode=None, timeout=20)
   command="{} {}".format(toolname,imagename)
   output=whitebox_lib.execute(device, command, mode=None, timeout=500)
   message="The {} File is Corrupted".format(imagename)
   if re.search(message,output):
       log.success("BMC is not upgraded as expected")
   else:
       log.fail("BMC update occured.verify the image")
       raise RuntimeError("BMC update occured.verify the image")

def upgradeBIOSwithBMCimage(device,module,bmcupgrade=None,mseoption=None,key='BIN'):
    log.debug("Entering upgradeBIOSwithBMCimage details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    if bmcupgrade == "upgrade":
        Imagedetail = imageObj.newImage[key]
        Versiondetail = imageObj.newVersion
    elif bmcupgrade == "downgrade":
        Imagedetail = imageObj.oldImage[key]
        Versiondetail = imageObj.oldVersion
    else:
        log.debug(f"There is no action on BMC FW")
    toolname = str(f"./CFUFLASH -cd -d 2 {Imagedetail}")
    cmd="./ipmi_driver.sh"
    whitebox_lib.execute(device, cmd, mode=None, timeout=20)
    cmd="rmmod ipmi_ssif"
    whitebox_lib.execute(device, cmd, mode=None, timeout=20)
    cmd="rmmod acpi_ipmi"
    whitebox_lib.execute(device, cmd, mode=None, timeout=20)
    log.info(f"{bmcupgrade} image :{Imagedetail} and version :{Versiondetail}")
    log.info(f"Final FW command :{toolname}")
    pass_message1="Enter your Option :"
    installationlog1=deviceObj.sendCmd(toolname,pass_message1,500)
    cmd1="y"
    prompt_message="#"
    installationlog2 = deviceObj.sendCmd(cmd1, prompt_message, 500)
    log.info(installationlog2)
    pass_message2 = "Error in updating BIOS image"
    match1 = re.search(pass_message2, installationlog2, re.I | re.M)
    if match1:
        log.success(f"{bmcupgrade} BIOS with BMC image not successfully with {module}")
    else:
        raise RuntimeError(f"{bmcupgrade} BIOS with BMC image successfully with {module}")

def Upgrade_BMC_with_Local_OS(device,command):
    log.debug("Entering procedure to update BMC throught local OS")
    log.info(command)
    cmd="./ipmi_driver.sh"
    whitebox_lib.execute(device, cmd, mode=None, timeout=60)
    time.sleep(60)
    output=whitebox_lib.execute(device, command, mode=None, timeout=500)
    pass_message_1="Uploading Firmware Image : 100%... done"
    pass_message_2="Flashing  Firmware Image : 100%... done"
    pass_message_3="Verifying Firmware Image : 100%... done"
    pass_message_4="Beginning to Deactive flashMode...end"
    pass_message_5="Resetting the firmware........."
    match1=re.search(pass_message_1,output)
    match2=re.search(pass_message_2,output)
    match3=re.search(pass_message_3,output)
    match4=re.search(pass_message_4,output)
    match5=re.search(pass_message_5,output)
    if match1 and match2 and match3 and match4 and match5:
        log.success("BMC upgraded through local OS successfully")
    else:
        raise RuntimeError("BMC upgraded through local OS Failed")

def updateBMCfirmwarefromremoteclient(device,BCM_IP,module,bmcupgrade=None,mseoption=None,key='BIN'):
    log.debug("Entering updateBMCfirmwarefromremoteclient details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    current_location=os.getcwd()
    log.debug(f"Current working location :{current_location}")
    imageObj = SwImage.getSwImage(module)
    if bmcupgrade == "upgrade":
        Imagedetail = imageObj.newImage[key]
        Versiondetail = imageObj.newVersion
    elif bmcupgrade == "downgrade":
        Imagedetail = imageObj.oldImage[key]
        Versiondetail = imageObj.oldVersion
    else:
        log.debug(f"There is no action on BMC FW")

    if mseoption!=None:
        toolname = str(f"./CFUFLASH -nw -ip {BCM_IP} -u admin -p admin {Imagedetail} -mse {mseoption} -fb")
    else:
        toolname = str(f"./CFUFLASH -nw -ip {BCM_IP} -u admin -p admin {Imagedetail} -mse 1 -fb")
    log.info(f"{bmcupgrade} image :{Imagedetail} and version :{Versiondetail}")
    log.info(f"Final FW command :{toolname}")
    CommonLib.change_local_dir("/root/Athena-G2-FW/BMC")
    installationlog=Device.execute_local_cmd(device_obj, toolname, timeout=500)
    log.info(installationlog)
    pass_message_1="Uploading Firmware Image : 100%... done"
    pass_message_2="Flashing  Firmware Image : 100%... done"
    pass_message_3="Verifying Firmware Image : 100%... done"
    pass_message_4="Beginning to Deactive flashMode...end"
    pass_message_5="Resetting the firmware.........."
    pass_message_6="Flasher Not Ready ! Please Try After Sometime"
    match1=re.search(pass_message_1,installationlog,re.I|re.M)
    match2=re.search(pass_message_2,installationlog,re.I|re.M)
    match3=re.search(pass_message_3,installationlog,re.I|re.M)
    match4=re.search(pass_message_4,installationlog,re.I|re.M)
    match5=re.search(pass_message_5,installationlog,re.I|re.M)
    match6=re.search(pass_message_6,installationlog,re.I|re.M)
    if match1 and match2 and match3 and match4 and match5:
        log.success(f"BMC FW {bmcupgrade} successfully with {module} by using mse {mseoption} option")
    elif match6:
        raise RuntimeError(f"BMC FW {bmcupgrade} Failed due to {pass_message_6} by using mse {mseoption} option")
    else:
        raise RuntimeError(f"BMC FW {bmcupgrade} Failed with {module} by using mse {mseoption} option")
    os.chdir(current_location)
    changed_location=Device.execute_local_cmd(device_obj, "pwd", timeout=10)
    log.debug(f"Changed working location :{changed_location}")

def check_fan_info(device,bmc_ip):
    log.debug("Entering procedure to verify fan info show up")
    device_obj = Device.getDeviceObject(device)
    mc_info_cmd="ipmitool -I lanplus -H {} -U admin -P admin mc info".format(bmc_ip)
    mc_info_op=Device.execute_local_cmd(device_obj,mc_info_cmd,timeout=60)
    log.info(mc_info_op)
    sensor_list_cmd="ipmitool -I lanplus -H {} -U admin -P admin sensor list | grep -i FAN".format(bmc_ip)
    sensor_list_op=Device.execute_local_cmd(device_obj,sensor_list_cmd,timeout=90)
    log.info(sensor_list_op)
    if re.search(fail_pattern, mc_info_op):
        log.fail("{} Command not executed successfully".format(mc_info_cmd))
        raise testFailed("{} Command not executed successfully".format(mc_info_cmd))
    else:
        log.success("{} Command executed successfully".format(mc_info_cmd))
    if re.search(fail_pattern, sensor_list_op):
        log.fail("Fan info not verified successfully")
        raise testFailed("Fan info not verified successfully")
    else:
        log.success("Fan info verified successfully")

def installCPLDFWimage(device,module,bmcupgrade=None,mseoption=None,key='A0'):
    log.debug("Entering install CPLD FW image details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    cmd_CPLD_FM_Version=str('ipmitool raw 0x3a 0x27')
    if bmcupgrade == "upgrade":
        Imagedetail = imageObj.newImage[key]
        Versiondetail = imageObj.newVersion
    elif bmcupgrade == "downgrade":
        Imagedetail = imageObj.oldImage[key]
        Versiondetail = imageObj.oldVersion
    else:
        log.debug(f"There is no action on CPLD FW")

    if mseoption!=None:
        toolname = str(f"./CFUFLASH -cd -d 4 {Imagedetail} -mse {mseoption} -fb")
    else:
        toolname = str(f"./CFUFLASH -cd -d 4 {Imagedetail} -fb")

    beforelog=whitebox_lib.execute(device, cmd_CPLD_FM_Version, mode=None, timeout=20)
    cmd="./ipmi_driver.sh"
    whitebox_lib.execute(device, cmd, mode=None, timeout=20)
    log.info(f"{bmcupgrade} image :{Imagedetail} and version :{Versiondetail}")
    log.info(f"Final FW command :{toolname}")
    installationlog=whitebox_lib.execute(device, toolname, mode=None, timeout=500)
    log.info(installationlog)
    pass_message_1="Beginning CPLD Update"
    pass_message_2="Uploading Image : 100%... done"
    pass_message_3="Flashing  Firmware Image : 100%... done"
    pass_message_4="Verifying Firmware Image : 100%... done"
    pass_message_5="Beginning to Deactive flashMode...end"
    pass_message_6="Flasher Not Ready ! Please Try After Sometime"
    match1=re.search(pass_message_1,installationlog,re.I|re.M)
    match2=re.search(pass_message_2,installationlog,re.I|re.M)
    match3=re.search(pass_message_3,installationlog,re.I|re.M)
    match4=re.search(pass_message_4,installationlog,re.I|re.M)
    match5=re.search(pass_message_5,installationlog,re.I|re.M)
    match6=re.search(pass_message_6,installationlog,re.I|re.M)

    if match1 and match2 and match3 and match4 and match5:
        log.success(f"CPLD FW {bmcupgrade} successfully with {module}")
    elif match6:
        raise RuntimeError(f"CPLD FW {bmcupgrade} Failed due to {pass_message_6}")
    else:
        raise RuntimeError(f"CPLD FW {bmcupgrade} Failed with {module}")

def checkinstalledCPLDFWversion(device,module,ip,bmcupgrade=None):
    log.debug("Entering check installed CPLD FW version details args : %s" %(str(locals())))
    cmd_FM_Version = f"ipmitool -I lanplus -H {ip} -U admin -P admin raw 0x3a 0x27"
    device_obj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    output = Device.execute_local_cmd(device_obj, cmd_FM_Version)
    log.info(output)
    list_str = output.split()
    new_list = [x.replace('0', '') for x in list_str]
    CurrentCPLDFWversion = "v0" + "." + new_list[1] + "." + new_list[2]
    log.debug(f"Currently Installed CPLD value :{CurrentCPLDFWversion}")

    if bmcupgrade == "upgrade":
        Versiondetail = imageObj.newVersion
    elif bmcupgrade == "downgrade":
        Versiondetail = imageObj.oldVersion
    else:
        log.debug(f"There is no action on CPLD FW")

    if CurrentCPLDFWversion == Versiondetail:
        log.success(f"CPLD FW {bmcupgrade} is success with {CurrentCPLDFWversion} version on {module}")
    else:
        raise RuntimeError(f"CPLD FW {bmcupgrade} version {Versiondetail} not success and system current version {CurrentCPLDFWversion} on {module}")

def updateCPLDfirmwarefromremoteclient(device,BCM_IP,module,bmcupgrade=None,mseoption=None,key='A0'):
    log.debug("Entering updateCPLDfirmwarefromremoteclient details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    current_location=os.getcwd()
    log.debug(f"Current working location before {bmcupgrade} :{current_location}")
    imageObj = SwImage.getSwImage(module)
    if bmcupgrade == "upgrade":
        Imagedetail = imageObj.newImage[key]
        Versiondetail = imageObj.newVersion
    elif bmcupgrade == "downgrade":
        Imagedetail = imageObj.oldImage[key]
        Versiondetail = imageObj.oldVersion
    else:
        log.debug(f"There is no action on CPLD FW")

    if mseoption!=None:
        toolname = str(f"./CFUFLASH -nw -ip {BCM_IP} -u admin -p admin -d 4 {Imagedetail} -mse {mseoption}")
    else:
        toolname = str(f"./CFUFLASH -nw -ip {BCM_IP} -u admin -p admin -d 4 {Imagedetail} -fb")
    log.info(f"{bmcupgrade} image :{Imagedetail} and version :{Versiondetail}")
    log.info(f"Final FW command :{toolname}")
    CommonLib.change_local_dir("/root/Athena-G2-FW/CPLD")
    installationlog=Device.execute_local_cmd(device_obj, toolname, timeout=500)
    log.info(installationlog)
    pass_message_1="Beginning CPLD Update"
    pass_message_2="Uploading Image : 100%... done"
    pass_message_3="Flashing  Firmware Image : 100%... done"
    pass_message_4="Verifying Firmware Image : 100%... done"
    pass_message_5="Beginning to Deactive flashMode...end"
    pass_message_6="Flasher Not Ready ! Please Try After Sometime"
    pass_message_7="Start to active flash mode"
    match1=re.search(pass_message_1,installationlog,re.I|re.M)
    match2=re.search(pass_message_2,installationlog,re.I|re.M)
    match3=re.search(pass_message_3,installationlog,re.I|re.M)
    match4=re.search(pass_message_4,installationlog,re.I|re.M)
    match5=re.search(pass_message_5,installationlog,re.I|re.M)
    match6=re.search(pass_message_6,installationlog,re.I|re.M)
    match7=re.search(pass_message_7,installationlog,re.I|re.M)

    if match1 and match2 and match3 and match4 and match5:
        log.success(f"CPLD FW {bmcupgrade} successfully with {module}")
    elif match6:
        raise RuntimeError(f"CPLD FW {bmcupgrade} Failed due to {pass_message_6}")
    else:
        raise RuntimeError(f"CPLD FW {bmcupgrade} Failed with {module}")
    os.chdir(current_location)
    changed_location=Device.execute_local_cmd(device_obj, "pwd", timeout=10)
    log.debug(f"Changed working location :{changed_location}")

def BMCFWFlashUpdate(device,module,bmcupgrade=None,key='BIN'):
  log.debug("Entering BMCFWFlashUpdate details args : %s" %(str(locals())))
  device_obj = Device.getDeviceObject(device)
  imageObj = SwImage.getSwImage(module)

  if bmcupgrade == "upgrade":
    Imagedetail = imageObj.newImage[key]
    Versiondetail = imageObj.newVersion
  elif bmcupgrade == "downgrade":
    Imagedetail = imageObj.oldImage[key]
    Versiondetail = imageObj.oldVersion
  else:
    log.debug(f"There is no action on BMC FW")

  toolname1 = str(f"dd if={Imagedetail} of=test.ima count=256 bs=1024")
  toolname2 = str(f"./socflash_x64 -s test.ima")
  log.info(f"Final BMC FWFlash records in and out command :{toolname1}")
  log.info(f"Final BMC FWFlash next command :{toolname2}")
  installationlog=whitebox_lib.execute(device, toolname1, mode=None, timeout=300)
  log.info(installationlog)
  pass_message_1="records in"
  pass_message_2="records out"
  pass_message_3="copied"
  match1=re.search(pass_message_1,installationlog,re.I|re.M)
  match2=re.search(pass_message_2,installationlog,re.I|re.M)
  match3=re.search(pass_message_3,installationlog,re.I|re.M)
  if match1 and match2 and match3:
    log.success(f"BMC FWFlash records in and out successfully with {module}")
  else:
    raise RuntimeError(f"BMC FWFlash records in and out Failed with {module}")

  installationlog=whitebox_lib.execute(device, toolname2, mode=None, timeout=300)
  log.info(installationlog)
  pass_message_1="Flash Type: SPI"
  pass_message_2="Update Flash Chip #1 O.K"
  pass_message_3="Update Flash Chip O.K."
  match1=re.search(pass_message_1,installationlog,re.I|re.M)
  match2=re.search(pass_message_2,installationlog,re.I|re.M)
  match3=re.search(pass_message_3,installationlog,re.I|re.M)
  if match1 and match2 and match3:
    log.success(f"BMC FWFlash {bmcupgrade} successfully with {module}")
  else:
    raise RuntimeError(f"BMC FWFlash {bmcupgrade} Failed with {module}")

def upgrade_with_socflash(device,command):
    log.debug("Entering procedure to update BMC through socflash")
    output=whitebox_lib.execute(device, command, mode=None, timeout=500)
    pass_message_1="Update Flash Chip O.K."
    match1=re.search(pass_message_1,output)
    if match1:
        log.success("BMC upgraded through socflash successfully")
    else:
        raise RuntimeError("BMC upgraded through socflash Failed")

def CheckBMCFWFlash(device,module,bmcupgrade=None,key='BIN'):
    log.debug("Entering upgradeBIOSwithBMCimage details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    if bmcupgrade == "upgrade":
        Imagedetail = imageObj.newImage[key]
        Versiondetail = imageObj.newVersion
    elif bmcupgrade == "downgrade":
        Imagedetail = imageObj.oldImage[key]
        Versiondetail = imageObj.oldVersion
    else:
        log.debug(f"There is no action on BMC FW")
    toolname = str(f"./CFUFLASH -cd {Imagedetail} -mse 1 -fb")
    cmd="./ipmi_driver.sh"
    whitebox_lib.execute(device, cmd, mode=None, timeout=20)
    cmd="rmmod ipmi_ssif"
    whitebox_lib.execute(device, cmd, mode=None, timeout=20)
    cmd="rmmod acpi_ipmi"
    whitebox_lib.execute(device, cmd, mode=None, timeout=20)
    log.info(f"{bmcupgrade} image :{Imagedetail} and version :{Versiondetail}")
    log.info(f"Final FW command :{toolname}")
    pass_message1="CFUFLASH - Firmware Upgrade Utility"
    installationlog=deviceObj.sendCmd(toolname,pass_message1,500)
    log.info(installationlog)
    deviceObj.sendCmd(Const.KEY_CTRL_C)
    pass_message_1="Creating IPMI session via USB"
    pass_message_2="CFUFLASH - Firmware Upgrade Utility"
    match1=re.search(pass_message_1,installationlog,re.I|re.M)
    match2=re.search(pass_message_2,installationlog,re.I|re.M)

    if match1 and match2:
        log.success(f"Terminated the flash process {bmcupgrade} during bmc load driver with {module}")
    else:
        raise RuntimeError(f"Not Terminated the flash process {bmcupgrade} during bmc load driver with {module}")

def Set_in_BIOS_Mode_Athena(device,bios_password='c411ie'):
    log.debug('Entering procedure verify_BMC_version_in_BIOS with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT",1)
    send_key(device, "KEY_DOWN",1)
    send_key(device, "KEY_DOWN",1)
    send_key(device, "KEY_DOWN",1)
    verify_com0_bios_setting(device, 'Enabled', '115200' )
    exit_bios_1(device)

