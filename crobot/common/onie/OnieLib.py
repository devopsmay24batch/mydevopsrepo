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
import copy
import re
import pexpect

import Logger as log
import CommonLib
import CommonKeywords
import OnieVariable
import Const
from Server import Server
from crobot.Decorator import logThis

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()


def checkOnieTlvValueExisted():
    log.debug("Entering OnieLib class procedure: checkOnieTlvValueExisted")

    tlv_value_dict = getOnieTlvValue()
    null_list = []
    for key, value in tlv_value_dict.items():
        if not value[1]:
            null_list.append(key)
    if null_list:
        log.info("TLV value is not got in items: {}".format(null_list))

def parseSyseeprom(output):
    log.debug("Entering OnieLib class procedure: parseSyseeprom")

    backup_value = copy.deepcopy(OnieVariable.TLV_Value_Test)
    for key, value in backup_value.items():
        backup_value[key][1] = ""

    item_num = 0
    for key, value in backup_value.items():
        pattern = "{}\s+{}\s+\d+\s+(.*)$".format(key, value[0].replace(".", "\."))
        match = re.search(pattern, output, re.M)
        if match:
            backup_value[key][1] = match.group(1).strip()
            item_num += 1
        else:
            log.info("Not found: {}".format(key))

    if  item_num == 0:
        return {}
    else:
        return backup_value


def getOnieTlvValue():
    log.debug("Entering OnieLib class procedure: getOnieTlvValue")

    output = CommonLib.execute_command(OnieVariable.ONIE_SYSEEPROM_CMD, mode=Const.ONIE_RESCUE_MODE)
    backup_value = parseSyseeprom(output)
    if backup_value:
        log.info("{} is got.".format(backup_value))
    else:
        raise Exception("Got EEPROM TSV value failed")
    return backup_value


def enableEepromWrite():
    log.debug("Entering OnieLib class procedure: enableEepromWrite")

    output = CommonLib.execute_command(OnieVariable.QUERY_EEPROM_WRITE_PROTECTION_CMD, mode=Const.ONIE_RESCUE_MODE)
    protect_value = parseSingleValue(output, OnieVariable.VALUE_PATTERN)
    if not protect_value:
        raise Exception("Can't get EEPROM write protection value.")

    CommonLib.execute_check_dict("DUT", OnieVariable.ENABLE_EEPROM_WRITE_CMD, mode=Const.ONIE_RESCUE_MODE,
                                 patterns_dict=OnieVariable.fail_dict, timeout=10, is_negative_test=True)

    return protect_value

def parseSingleValue(output, pattern):
    log.debug("Entering OnieLib class procedure: parseSingleValue")

    match = re.search(pattern, output, re.M)
    parsed_value = ""
    if match:
        parsed_value = match.group(1).strip()

    return parsed_value


def writeTlvValueToEeprom(TLV_Value):
    log.debug("Entering OnieLib class procedure: writeTlvValueToEeprom")

    # enableEepromWrite()
    # cmd = OnieVariable.QUERY_EEPROM_WRITE_PROTECTION_CMD
    # CommonLib.run_command(OnieVariable.QUERY_EEPROM_WRITE_PROTECTION_CMD)

    output = ""
    for key, value in TLV_Value.items():
        if not value[1]:
            continue
        log.info("Write value for {}".format(key))
        if value[0] in ("0xFD", ): #unset first before setting for "0xFD"
            for i in range(3):
                cmd = 'onie-syseeprom -s {}'.format(value[0].lower())
                output += CommonLib.execute_command(cmd, timeout=10)
        cmd = 'onie-syseeprom -s {}={}'.format(value[0].lower(), value[1])
        if key in ("Manufacture Date", "Vendor Extension"):
            cmd = 'onie-syseeprom -s {}="{}"'.format(value[0].lower(), value[1])
        output += CommonLib.execute_command(cmd, timeout=10)

    CommonLib.execute_check_dict("DUT", "", patterns_dict=OnieVariable.fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)


def checkTlvValueFromEeprom(TLV_Value):
    log.debug("Entering OnieLib class procedure: checkTlvValueFromEeprom")

    onie_syseeprom_info = CommonLib.execute_command(OnieVariable.ONIE_SYSEEPROM_CMD, mode=Const.ONIE_RESCUE_MODE)
    parsed_value = parseSyseeprom(onie_syseeprom_info)
    fail_count = 0
    for key, value in TLV_Value.items():
        parsed = parsed_value.get(key, "NotFound")
        if parsed != value:
            if value[0] in ("0x26",) and parsed[1].lstrip("0") == value[1].lstrip("0"):
                continue
            else:
                log.error("Key: {}, value : {}, expected: {}".format(key, parsed, value))
                fail_count += 1

    if fail_count:
        raise Exception("Read value is not match written value.")


def disableEepromWrite(write_protect_value):
    log.debug("Entering OnieLib class procedure: disableEepromWrite.")

    CommonLib.execute_command(OnieVariable.QUERY_EEPROM_WRITE_PROTECTION_CMD, mode=Const.ONIE_RESCUE_MODE)
    disable_write_cmd = copy.deepcopy(OnieVariable.DISABLE_EEPROM_WRITE_CMD)
    disable_write_cmd = disable_write_cmd.format(write_protect_value)
    CommonLib.execute_check_dict(Const.DUT, disable_write_cmd, patterns_dict=OnieVariable.fail_dict,
                                 timeout=10, is_negative_test=True)

@logThis
def checkIpAddr(interfaceName, ipv6=False):
    if ipv6:
        ipformat = r'inet6 (addr:\s?)?(.+)(\/|prefixlen).*(Scope:Link|scopeid.*link)'
    else:
        ipformat = r'inet (addr:)?(\d+\.\d+\.\d+\.\d+)'
    output = device.executeCmd("ifconfig %s"%interfaceName, timeout=30)
    ip = ''
    for line in output.splitlines():
        line = line.strip()
        match = re.search(ipformat, line)
        if match:
            ip = match.group(2).strip()
            log.success('Successfully get ip address: %s'%(ip))
            return ip
            break
    raise RuntimeError('Can not get ip address!')



def checkOnieSysInfoV():
    log.debug("Entering OnieLib class procedure: checkOnieSysInfoV.")

    cmd = "onie-sysinfo -v"
    oine_version = CommonLib.get_swinfo_dict("ONIE_INSTALLER").get("newVersion", "NotFound")
    pattern = { oine_version: oine_version.replace(".", "\.")}

    CommonLib.execute_check_dict(Const.DUT, cmd, patterns_dict=pattern, timeout=10)

def checkOnieSysInfo(pattern):
    log.debug("Entering OnieLib class procedure: checkOnieSysInfo.")

    cmd = "onie-sysinfo"
    output = device.executeCmd(cmd)
    CommonKeywords.should_match_one_of_regexp_list(output, pattern)


@logThis
def copyFileFromServer(filePathServer, file, filePathDut, server='PC'):
    """ this function copy file from server to dut    """
    serverObj = Server.getServer(server, needLogin=False)
    serverIP = serverObj.managementIP
    CommonLib.copy_files_through_scp(Const.DUT, serverObj.username, serverObj.password, serverIP, [file], filePathServer, filePathDut)
