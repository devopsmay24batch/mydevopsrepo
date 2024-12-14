###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

import Const
import AliConst
import CommonLib
import Logger as log
import time
from crobot.Decorator import logThis

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

@logThis
def powerCycleToOpenbmc(timeout=AliConst.BOOT_TIME):
    device.powerCycleDevice()
    device.read_until_regexp('login:', timeout)
    time.sleep(40)
    return device.getPrompt(Const.BOOT_MODE_OPENBMC)

@logThis
def powerCycleSonic(mode):
    device.getPrompt(Const.BOOT_MODE_OPENBMC)
    device.executeCmd('source /usr/local/bin/openbmc-utils.sh', Const.BOOT_MODE_OPENBMC)
    device.sendCmd('wedge_power.sh cycle')
    device.trySwitchToCpu()
    device.receive('System Reset', timeout=180)
    output = device.receive('sonic login:', timeout=AliConst.BOOT_TIME)
    device.getPrompt(Const.BOOT_MODE_DIAGOS, timeout=AliConst.BOOT_TIME)
    device.getPrompt(mode)
    time.sleep(10)
    return output

@logThis
def powerOffOnSonic(mode):
    device.getPrompt(Const.BOOT_MODE_OPENBMC)
    device.executeCmd('source /usr/local/bin/openbmc-utils.sh', Const.BOOT_MODE_OPENBMC)
    device.executeCmd('wedge_power.sh off')
    time.sleep(10)
    device.sendCmd('wedge_power.sh on')
    device.trySwitchToCpu()
    device.receive('System Reset', timeout=180)
    output = device.receive('sonic login:', timeout=AliConst.BOOT_TIME)
    device.getPrompt(Const.BOOT_MODE_DIAGOS, timeout=AliConst.BOOT_TIME)
    device.getPrompt(mode)
    time.sleep(10)
    return output

@logThis
def powerResetSonic(mode):
    device.getPrompt(Const.BOOT_MODE_OPENBMC)
    device.executeCmd('source /usr/local/bin/openbmc-utils.sh', Const.BOOT_MODE_OPENBMC)
    device.sendCmd('wedge_power.sh reset')
    device.trySwitchToCpu()
    device.receive('System Reset', timeout=180)
    output = device.receive('sonic login:', timeout=AliConst.BOOT_TIME)
    device.getPrompt(Const.BOOT_MODE_DIAGOS, timeout=AliConst.BOOT_TIME)
    device.getPrompt(mode)
    time.sleep(10)
    return output

@logThis
def rebootOpenbmc(mode=Const.BOOT_MODE_OPENBMC, timeout=AliConst.BOOT_TIME):
    device.getPrompt(mode)
    device.transmit("reboot")
    output = device.read_until_regexp('Restarting', timeout)
    output += device.read_until_regexp('login:', timeout)
    device.getPrompt(mode)
    time.sleep(40)
    return output

@logThis
def openbmcCmdOffOnPsu(mode):
    """
    This function can use OpenBMC command to off the DUT PSU then about 10s later the PDU PSU will auto turn on.
    The OpenBMC and DiagOS will both off then on.
    Only supports OpenBMC version 2.0.0 and above.
    """
    device.getPrompt(Const.BOOT_MODE_OPENBMC)
    device.transmit("psu_off_on.sh -a")
    device.receive('System Reset', timeout=240)
    output = device.receive('sonic login:', timeout=AliConst.BOOT_TIME)
    device.getPrompt(Const.BOOT_MODE_DIAGOS, timeout=AliConst.BOOT_TIME)
    device.getPrompt(mode)
    time.sleep(10)
    return output

@logThis
def powerCycleToOnieRescueMode():
    return device.powerCycleToMode(Const.ONIE_RESCUE_MODE)

@logThis
def rebootToDiagOS():
    device.sendCmd("reboot")
    device.readUntil("will be executed automatically in", 180)
    device.toDiagOS()

@logThis
def bootIntoOnieRescueMode():
    device.getPrompt(Const.ONIE_RESCUE_MODE)

@logThis
def bootIntoOnieUpdateMode():
    device.getPrompt(Const.ONIE_UPDATE_MODE)

@logThis
def bootIntoOnieInstallMode():
    device.getPrompt(Const.ONIE_INSTALL_MODE)

@logThis
def bootIntoDiagOSMode():
    device.getPrompt(Const.BOOT_MODE_DIAGOS)

@logThis
def bootIntoUbootMode():
    device.getPrompt(Const.BOOT_MODE_UBOOT)

@logThis
def bootIntoUefiMode():
    device.getPrompt(Const.BOOT_MODE_UEFI)

@logThis
def ali_generate_eeprom_cfg(eeprom_name, fru_type='biapia'):
    BIA_EEPROM_MAP_KEY = {
        'Board Mfg'         : 'manufacturer',
        'Board Product'     : 'product_name',
        'Board Serial'      : 'serial_number',
        'Board Part Number' : 'part_number',
        'Board FRU ID'      : 'fru_file_id',
        'Board Extra_1'     : 'board_custom_1',
    }
    PIA_EEPROM_MAP_KEY = {
        'Product Manufacturer': 'manufacturer',
        'Product Name'        : 'product_name',
        'Product Serial'      : 'serial_number',
        'Product Part Number' : 'part_number',
        'Product Version'     : 'version',
        'Product FRU ID'      : 'fru_file_id',
        'Product Extra_1'     : 'product_custom_1',
        'Product Extra_2'     : 'product_custom_2',
        'Product Extra_3'     : 'product_custom_3',
        'Product Extra_4'     : 'product_custom_4',
    }
    eeprom_config_dict = CommonLib.get_eeprom_cfg_dict(eeprom_name)
    if fru_type == 'biapia':
        eeprom_str = ali_generate_eeprom_by_fru_type(eeprom_config_dict, BIA_EEPROM_MAP_KEY, 'bia')
        eeprom_str += ali_generate_eeprom_by_fru_type(eeprom_config_dict, PIA_EEPROM_MAP_KEY, 'pia')
    elif fru_type == 'bia':
        eeprom_str = ali_generate_eeprom_by_fru_type(eeprom_config_dict, BIA_EEPROM_MAP_KEY, 'bia')
    elif fru_type == 'pia':
        eeprom_str = ali_generate_eeprom_by_fru_type(eeprom_config_dict, PIA_EEPROM_MAP_KEY, 'pia')
    else:
        log.info('ali generate eeprom does not support eeprom type: %s'%(fru_type))
        raise RuntimeError("ali_generate_eeprom_cfg failed")
    eeprom_str += '\n'
    log.debug('eeprom_str: ' + eeprom_str)
    return eeprom_str

@logThis
def ali_generate_eeprom_by_fru_type(eeprom_dict, eeprom_map_dict, fru_type):
    eeprom_str = '[%s]'%fru_type.lower()
    for key, value in eeprom_dict.items():
        if key in eeprom_map_dict:
            new_key = eeprom_map_dict[key]
            eeprom_str += '\n' + new_key + '=' + value
    eeprom_str += '\n\n'
    return eeprom_str


@logThis
def recoverCpu():
    try:
        device.switchToCpu(timeout=30)
    except:
        log.error('CPU hung, need recover it!')
        powerCycleToOpenbmc()
        device.getPrompt(Const.BOOT_MODE_DIAGOS, timeout=AliConst.BOOT_TIME)
        device.getPrompt(Const.BOOT_MODE_OPENBMC)
        raise RuntimeError('CPU hung after run this case, recovered it by power cycle !')
    device.switchToBmc()

@logThis
def restoreNetwork(mode):
    CommonLib.get_dhcp_ip_address(Const.DUT, 'eth0', mode)
    time.sleep(5)
    try:
        CommonLib.exec_ping(Const.DUT, DeviceMgr.getServerInfo('PC').managementIP, 4, mode)
    except:
        log.error('network is broken down, need recover it !')
        powerCycleToOpenbmc()
        device.getPrompt(mode)
        raise RuntimeError('network is broken down, after running this case !')

@logThis
def executePythonCommand(cmd, mode=None, timeout=60):
    return device.executeCommand(cmd, AliConst.PROMPT_PYTHON, mode, timeout=timeout)
