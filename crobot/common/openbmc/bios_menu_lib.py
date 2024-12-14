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
import time
import re
import Logger as log
from robot import utils
import parser_openbmc_lib
import CommonLib
import subprocess
from Device import Device
from errorsModule import noSuchClass, testFailed
from dataStructure import nestedDict, parser
from Openbmc_variable import BOOT_ORDER_LIST
from SwImage import SwImage

KEY_DATA = {
    'KEY_DEL': '\x1b[3~',
    'KEY_F1': '\x1bOP',
    'KEY_F2': '\x1bOQ',
    'KEY_F3': '\x1bOR',
    'KEY_F4': '\x1bOS',
    'KEY_F5': '\x1b[15~',
    'KEY_F7': '\x1b[18~',
    'KEY_F9': '\x1b[20~',
    'KEY_F10': '\x1b[21~',
    'KEY_ESC': '\x1b',
    'KEY_ENTER': '\r',
    'KEY_PLUS': '+',
    'KEY_MINUS': '-',
    'KEY_UP': '\x1b[A',
    'KEY_DOWN': '\x1b[B',
    'KEY_RIGHT': '\x1b[C',
    'KEY_LEFT': '\x1b[D',
    'KEY_BKSP': '\x08',
    'KEY_DOT': '\x2E',
    #'KEY_7': '7',
    'KEY_2000': '2000',
    'KEY_1': '1',
    'KEY_2': '2',
    'KEY_3': '3',
    'KEY_4': '4',
    'KEY_5': '5',
    'KEY_6': '6',
    'KEY_7': '7',
    'KEY_8': '8',
    'KEY_9': '9',
    'KEY_0': '0',
    'KEY_s': 's',
    'KEY_y': 'y',
    'KEY_x': 'x'
}

MENU_DATA = {
    'Main': 'BIOS Information',
    'Advanced': 'Trusted Computing',
    'IntelRCSetup': 'Harcuvar',
    'Server Mgmt': 'BMC Self Test Status',
    'Event Logs': 'Change Smbios Event Log Settings',
    'Security': 'Password Description',
    'Boot': 'Boot Configuration',
    'Save & Exit': 'Save Options'
}

MENU_KEY_FREQ = {
    'Main': 0,
    'Advanced': 1,
    'IntelRCSetup': 2,
    'Server Mgmt': 3,
    'Event Logs': 4,
    'Security': 5,
    'Boot': 6,
    'Save & Exit': 7
}

################################################################
### Function to send the control key for n times (default=1) ###
################################################################
def send_key(device, key_name, times=1, delay=2):
    log.debug('Entering send_key with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    for i in range(times):
        log.debug("Sending %s #%d"%(key_name, i+1))
        # deviceObj.flush()
        deviceObj.sendline(KEY_DATA[key_name], CR=False)
        time.sleep(delay)

###################################################
### Function to verify that the keyword appears ###
###################################################
def verify_keyword(device, keyword):
    log.debug('Entering verify_keyword with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.receive(keyword, timeout=10)

#################################################################
### Function to remove the escape ansi characters from string ###
#################################################################
def escape_ansi(output):
    ansi_escape = r'\x1b[\[][0-?]*[ -/]*[@-~]'
    return re.sub(ansi_escape, ' ', output)

####################################################
### Function to reboot and enter into bios setup ###
####################################################
def enter_bios_setup(device):
    log.debug('Entering enter_bios_setup with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    line1 = 'Press <DEL> or <F2> to enter setup.'
    line2 = 'Enter Setup...'
    line3 = '.*Aptio Setup Utility.*'
    line4 = 'Enter Password'
    line5 = '------'

    deviceObj.getPrompt("centos")
    deviceObj.sendline("")
    deviceObj.sendline("reboot")
    deviceObj.read_until_regexp(line1, timeout=600)

    # Enter BIOS Setup Menu
    send_key(device, "KEY_DEL")
    # deviceObj.read_until_regexp(line2, timeout=20)
    output = deviceObj.read_until_regexp(line5, timeout=60)
    match = re.search(line4, output)
    match1 = re.search(line3, output)
    if match:
        log.debug("Found '%s'"%(line4))
        send_key(device, "KEY_ENTER")
        deviceObj.read_until_regexp(line3, timeout=60)
        log.success("Successfully enter Bios Setup")
    elif match1:
        log.debug("Found '%s'"%(line3))
        log.success("Successfully enter Bios Setup")
    else:
        log.fail("Failed enter Bios Setup")
        raise testFailed("enter_bios_setup")

##################################################################
### Function to send key ESC to exit bios and boot into diagos ###
##################################################################
def exit_bios_setup(device, prompt="centos"):
    log.debug('Entering exit_bios_setup with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    line1 = '>>Start PXE over.*'
    line2 = 'Yes'
    line3 = 'Quit without saving?'

    send_key(device, "KEY_ESC")
    deviceObj.read_until_regexp(line3, timeout=10)
    send_key(device, "KEY_ENTER")
    # deviceObj.read_until_regexp(line1, timeout=60)

    deviceObj.getPrompt(prompt, timeout=600)

####################################################################
### Function to verify bios setup menu by test name and keywords ###
####################################################################
def verify_menu_bios_setup(device, keyword):
    log.debug('Entering verify_menu_bios_setup with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    # output = deviceObj.read_until_regexp(boundary_line)
    time.sleep(2)
    output = deviceObj.readMsg()
    # deviceObj.flush()
    output = escape_ansi(output)
    log.debug(output)
    match = re.search(keyword, output)
    if match:
        log.success("Found keyword: %s"%(keyword))
    else:
        log.fail("Not found keyword: %s"%(keyword))
        raise testFailed("verify_menu_bios_setup")

####################################################################
### Function to verify bios bootorder ###
####################################################################
def verify_menu_bios_bootorder(device, boundary_line, bootorder):
    log.debug('Entering verify_menu_bios_bootorder with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    output = deviceObj.receive(boundary_line)
    # deviceObj.flush()
    output = escape_ansi(output)
    log.debug(output)
    parsed_output = parser_openbmc_lib.parse_menu_boot_sequence(output)
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, bootorder)
    if err_count:
        raise testFailed("verify_menu_bios_bootorder")

################################################################################
# Function Name: enter_menu_bios_boot_override
# Date         : 6th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def enter_menu_bios_boot_override(device, boundary_line, p1):
    log.debug('Entering verify_menu_bios_bootorder with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    output = deviceObj.receive(boundary_line)
    output = escape_ansi(output)
    log.debug(output)
    parsed_output = parser_openbmc_lib.parse_menu_boot_override(output)
    for line in parsed_output:
        match = re.search(p1, line)
        if match:
            key_number = parsed_output.index(line) + 4
    send_key(device, "KEY_DOWN", key_number)
    time.sleep(1)
    send_key(device, "KEY_ENTER", 1)
    deviceObj.getPrompt("centos", timeout=420)

################################################################################
# Function Name: enter_menu_bios_boot_order
# Date         : 15th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def enter_menu_bios_boot_order(device, boundary_line, target_list, ipv6=False):
    log.debug('Entering enter_menu_bios_boot_order with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    send_key(device, "KEY_DOWN", 1)
    target_list_1 = target_list.split(",")
    select_bios_boot_order(device, boundary_line, number='boot option 1', target=target_list_1[0])
    select_bios_boot_order(device, boundary_line, number='boot option 2', target=target_list_1[1])
    send_key(device, "KEY_DOWN")
    select_bios_boot_order(device, boundary_line, number='boot option 4', target=target_list_1[3])
    select_bios_boot_order(device, boundary_line, number='boot option 5', target=target_list_1[4])
    if ipv6:
        send_key(device, "KEY_DOWN")
        select_bios_network_drive_bbs_priorities(device)
    else:
        pass
    if err_count:
        raise testFailed("enter_menu_bios_boot_order FAIL")

################################################################################
# Function Name: select_bios_boot_order
# Date         : 15th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def select_bios_boot_order(device, boundary_line, number, target):
    log.debug('Entering select_bios_boot_order with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    send_key(device, "KEY_LEFT")
    send_key(device, "KEY_RIGHT")
    output = deviceObj.receive(boundary_line)
    output = escape_ansi(output)
    parsed_output = parser_openbmc_lib.parse_menu_boot_sequence(output)
    if 'USB  |' in list(parsed_output.values()):
        modify_key = list(parsed_output.keys())[list (parsed_output.values()).index ('USB  |')]
        parsed_output[modify_key] = 'USB'
    else:
        pass
    if 'CD/DVD  |' in list(parsed_output.values()):
        modify_key = list(parsed_output.keys())[list (parsed_output.values()).index ('CD/DVD  |')]
        parsed_output[modify_key] = 'CD/DVD'
    else:
        pass
    if 'Other  |' in list(parsed_output.values()):
        modify_key = list(parsed_output.keys())[list (parsed_output.values()).index ('Other  |')]
        parsed_output[modify_key] = 'Other'
    else:
        pass
    current_location = parsed_output[number]
    current_location_index = BOOT_ORDER_LIST.index(current_location)
    target_location_index = BOOT_ORDER_LIST.index(target)
    value = target_location_index - current_location_index
    send_key(device, "KEY_DOWN", 1)
    if value == 0:
        pass
    elif value > 0:
        send_key(device, "KEY_ENTER")
        time.sleep(1)
        send_key(device, "KEY_DOWN", value)
        send_key(device, "KEY_ENTER")
    else:
        send_key(device, "KEY_ENTER")
        time.sleep(1)
        send_key(device, "KEY_UP", -value)
        send_key(device, "KEY_ENTER")

################################################################################
# Function Name: save_bios_setup
# Date         : 15th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def save_bios_setup(device):
    log.debug('Entering exit_bios_setup with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    line1 = 'Yes'
    line2 = 'Save configuration and reset?'
    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp(line2, timeout=10)
    send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp(line1, timeout=20)
    deviceObj.getPrompt("centos", timeout=420)

################################################################################
# Function Name: estore_bios_defaults
# Date         : 15th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def restore_bios_defaults(device):
    log.debug('Entering exit_bios_setup with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    line1 = 'Load Optimized Defaults'
    send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp(line1, timeout=10)
    send_key(device, "KEY_ENTER")

################################################################################
# Function Name: select_bios_network_drive_bbs_priorities
# Date         : 15th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def select_bios_network_drive_bbs_priorities(device):
    log.debug('Entering select_bios_network_drive_bbs_priorities with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    line1 = 'UEFI: IPv6 Intel(R)'
    line2 = 'UEFI: IPv4 Intel(R)'
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ESC")

################################################################################
# Function Name: restore_bios_network_drive_bbs_priorities_defaults
# Date         : 15th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def restore_bios_network_drive_bbs_priorities_defaults(device, boundary_line):
    log.debug('Entering restore_bios_network_drive_bbs_priorities_defaults with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    send_key(device, "KEY_ENTER")
    output = deviceObj.receive(boundary_line)
    output = escape_ansi(output)
    parsed_output = parser_openbmc_lib.parse_menu_boot_sequence(output)
    if list(parsed_output.values()).index('UEFI: IPv4 Intel(R)') < list(parsed_output.values()).index('UEFI: IPv6 Intel(R)'):
        send_key(device, "KEY_ESC")
    else:
        send_key(device, "KEY_ENTER")
        send_key(device, "KEY_DOWN")
        send_key(device, "KEY_ENTER")
        send_key(device, "KEY_ESC")

################################################################################
# Function Name: power_reset_enter_into_bios
# Date         : 15th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def power_reset_enter_into_bios(device):
    ###reset come os by bmc side when come os enter into bios.
    log.debug('Entering procedure power_reset_enter_into_bios with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'wedge_power.sh reset'
    cmd1 = 'sol.sh'
    err_count = 0
    output = execute(deviceObj, cmd, timeout=10)
    deviceObj.getPrompt(OPENBMC_MODE)
    deviceObj.sendline(cmd1)
    log.debug('Entering enter_bios_setup with args : %s' %(str(locals())))
    line1 = 'Press <DEL> or <F2> to enter setup.'
    line2 = 'Enter Setup...'
    line3 = '.*Aptio Setup Utility.*'
    line4 = 'Enter Password'
    line5 = '------'
    deviceObj.read_until_regexp(line1, timeout=200)
    send_key(device, "KEY_DEL")
    output = deviceObj.read_until_regexp(line5, timeout=60)
    match = re.search(line4, output)
    match1 = re.search(line3, output)
    if match:
        log.debug("Found '%s'"%(line4))
        send_key(device, "KEY_ENTER")
        deviceObj.read_until_regexp(line3, timeout=60)
        log.success("Successfully enter Bios Setup")
    elif match1:
        log.debug("Found '%s'"%(line3))
        log.success("Successfully enter Bios Setup")
    else:
        log.fail("Failed enter Bios Setup")
        raise testFailed("enter_bios_setup")

def verify_bios_version_in_bios(device,bios_password='c411ie',bios_version=None):
    log.debug('Entering procedure verify_bios_version_in_bios with args : %s\n' %(str(locals())))

    enter_bios_1(device,bios_password)

    deviceObj = Device.getDeviceObject(device)
    line2 = 'BIOS Version.*(ATHG[0-9]\.[0-9]\.[0-9][0-9]\.[0-9][0-9])'
    output = deviceObj.read_until_regexp(line2, timeout=60)
    match = re.search(line2, output)

    if match:
        log.debug("Found '%s'"%(line2))
        log.success(match.group(1))
        if match.group(1) in bios_version:
           log.success("Expected BIOS version is shown in BIOS")
        else:
           log.fail("Expected BIOS version is not shown in BIOS")
           raise testFailed("Expected BIOS version is not shown in BIOS")
    else:
        log.fail("BIOS Version Pattern Not Found")
        raise testFailed("BIOS Version Pattern Not Found")

    exit_bios_1(device)

def enter_bios_1(device,bios_password='c411ie'):
    log.debug('Entering procedure enter_bios_1 with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    line1 = 'Enter Password'

    deviceObj.getPrompt("centos")
    deviceObj.sendline("")
    deviceObj.sendline("reboot")

    # Enter BIOS Setup Menu

    counter = 30
    while counter >= 0:
        send_key(device, "KEY_DEL")
        counter -= 1
        time.sleep(1)
    output = None
    output = deviceObj.read_until_regexp(line1, timeout=60)
    if output is not None:
       deviceObj.sendline(bios_password)
       time.sleep(5)
    else:
        log.fail("Failed enter Bios Setup")
        raise testFailed("enter_bios_setup")

def exit_bios_1(device):
    log.debug('Entering procedure exit_bios_1 with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    send_key(device, "KEY_ESC")
    time.sleep(5)
    send_key(device, "KEY_ENTER")
    log.success("Successfully exited Bios Setup")

def change_date_time_in_bios(device,bios_password='c411ie',dt=None):
    log.debug('Entering procedure change_date_time_in_bios with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    line2 = 'BIOS Version.*(ATHG[0-9]\.[0-9]\.[0-9][0-9]\.[0-9][0-9])'
    output = deviceObj.read_until_regexp(line2, timeout=10)

    send_key(device, "KEY_DOWN")

    deviceObj.sendline(dt['Month'][0], CR=False)
    time.sleep(2)
    deviceObj.sendline(dt['Month'][1], CR=False)
    time.sleep(2)
    send_key(device, "KEY_ENTER")

    deviceObj.sendline(dt['Day'][0], CR=False)
    time.sleep(2)
    deviceObj.sendline(dt['Day'][1], CR=False)
    time.sleep(2)
    send_key(device, "KEY_ENTER")

    deviceObj.sendline(dt['Year'][0], CR=False)
    time.sleep(2)
    deviceObj.sendline(dt['Year'][1], CR=False)
    time.sleep(2)
    deviceObj.sendline(dt['Year'][2], CR=False)
    time.sleep(2)
    deviceObj.sendline(dt['Year'][3], CR=False)
    time.sleep(2)
    send_key(device, "KEY_DOWN")

    deviceObj.sendline(dt['Hour'][0], CR=False)
    time.sleep(2)
    deviceObj.sendline(dt['Hour'][1], CR=False)
    time.sleep(2)
    send_key(device, "KEY_ENTER")

    deviceObj.sendline(dt['Minute'][0], CR=False)
    time.sleep(2)
    deviceObj.sendline(dt['Minute'][1], CR=False)
    time.sleep(2)
    send_key(device, "KEY_ENTER")

    deviceObj.sendline(dt['Second'][0], CR=False)
    time.sleep(2)
    deviceObj.sendline(dt['Second'][1], CR=False)
    time.sleep(2)
    send_key(device, "KEY_ENTER")

    time.sleep(5)

    exit_bios_1(device)


def verify_time_in_OS(output,dt):
    log.debug('Entering procedure verify_time_in_OS with args : %s\n' %(str(locals())))
    p1 = 'Universal time:.* (?P<year>\S+)-(?P<month>\S+)-(?P<day>\S+) (?P<hour>\S+):(?P<minute>\S+):(?P<second>\S+).*UTC'
    split_output = output.splitlines();
    for line in split_output:
        line = line.strip();
        match = re.search(p1,line)
        if match:
            if match.group('year') == dt['Year'] and match.group('month') == dt['Month'] and match.group('day') == dt['Day'] and match.group('hour') == dt['Hour']:
                log.success('BIOS and OS Time are same')
            else:
                log.fail("BIOS and OS Time are not Same")
                raise testFailed("BIOS and OS Time are not Same")

def change_date_time_in_os(device):
    log.debug('Entering procedure change_date_time_in_os with args : %s\n' %(str(locals())))
    return_dict = {}
    deviceObj = Device.getDeviceObject(device)
    cap_time_output = subprocess.check_output('timedatectl')
    p1 = 'Universal time:.* (?P<year>\S+)-(?P<month>\S+)-(?P<day>\S+) (?P<hour>\S+):(?P<minute>\S+):(?P<second>\S+).*UTC'
    split_output = cap_time_output.splitlines();
    Flag = False
    for line in split_output:
        line = str(line.strip());
        match = re.search(p1,line)
        if match:
            deviceObj.sendline('date +%%Y%%m%%d -s "%s%s%s"' %(match.group('year'),match.group('month'),match.group('day')))
            deviceObj.sendline('date +%%T -s "%s:13:13"' %(str(int(match.group('hour')) + 8)))
            return_dict['Year'] = match.group('year')
            return_dict['Month'] = match.group('month')
            return_dict['Day'] = match.group('day')
            return_dict['Hour'] = match.group('hour')
            return_dict['Minute'] = '00'
            return_dict['Sec'] = '00'
            return return_dict
    if not Flag:
        log.fail("Failed to set Time in OS")
        raise testFailed("Failed to set Time in OS")

def verify_time_in_BIOS(device,bios_password='c411ie',dt=None):
    log.debug('Entering procedure change_date_time_in_bios with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    line1 = 'System Date.*([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9])'
    line2 = 'System Time.*([0-9][0-9]):([0-9][0-9]):([0-9][0-9])'

    enter_bios_1(device,bios_password)

    output1 = deviceObj.read_until_regexp(line1, timeout=10)
    output2 = deviceObj.read_until_regexp(line2, timeout=10)
    match1 = re.search(line1, output1)
    match2 = re.search(line2, output2)

    exit_bios_1(device)

    if match1 and match2:
        if match1.group(1) == dt['Month'] and match1.group(2) == dt['Day'] and match1.group(3) == dt['Year'] and match2.group(1) == dt['Hour']:
           log.success("BIOS Date and Time is in Sync with OS Time")
           Flag = True
    else:
        log.fail("BIOS Date and Time is not in Sync with OS Time")
        raise testFailed("BIOS Date and Time is not in Sync with OS Time")

def get_cpu_microcode_revision_from_bios(device,bios_password='c411ie'):
    log.debug('Entering procedute to get microcode revision: %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_ENTER")
    line='L1 Cache RAM'
    output=deviceObj.read_until_regexp(line, timeout=10)
    time.sleep(5)
    send_key(device, "KEY_ESC")
    time.sleep(5)
    exit_bios_1(device)
    count = 0
    pattern='Microcode Revision.*([0-9A-F]{8})\s.*'
    output1=output.splitlines()
    for a in output1:
       match=re.search(pattern,a)
       if match:
          log.info("Match line found")
          cpu_microcode_revision_from_bios=match.group(1)
          return cpu_microcode_revision_from_bios
          count=1
    if count == 0:
        log.fail("cpu_microcode_revision_from_bios is not available")
        raise  testFailed("cpu_microcode_revision_from_bios is not available")

################################################################################
# Function Name: enter_uefi_shell
# Parameters :
#    device             : Device Object
#    bios_password      : BIOS Password (This can vary depending on setup)
#
# Description: Goes into BIOS and selects UEFI Shell as boot option 1 and 
#             Enters UEFI Shell
################################################################################

def enter_uefi_shell(device,bios_password='c411ie'):
    log.debug('Entering procedure verify_bios_version_in_uefi_shell with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    line1 = 'BIOS Version.*(ATHG[0-9]\.[0-9]\.[0-9][0-9]\.[0-9][0-9])'
    output = deviceObj.read_until_regexp(line1, timeout=10)

    key_strokes_to_reach_boot_menu = 6
    key_strokes_to_reach_boot_option_1 = 3
    key_strokes_to_select_uefi_shell = 3

    for i in range(key_strokes_to_reach_boot_menu):
        send_key(device, "KEY_RIGHT")

    for i in range(key_strokes_to_reach_boot_option_1):
        send_key(device, "KEY_DOWN")

    send_key(device, "KEY_ENTER")

    line2 = '----- Boot Option #1 -----'
    output = deviceObj.read_until_regexp(line2, timeout=10)

    for i in range(key_strokes_to_select_uefi_shell):
        send_key(device, "KEY_DOWN")

    send_key(device, "KEY_ENTER")

    # Exit BIOS
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ENTER")

    time.sleep(120)

################################################################################
# Function Name: verify_bios_version_in_uefi_shell
# Parameters :
#    device             : Device Object
#    bios_version       : BIOS Version to Check
#
# Description: Verifies if the BIOS Version (Specified) is present in 
#              output of UEFI shell command smbiosview -t 0 
################################################################################


def verify_bios_version_in_uefi_shell(device,bios_version):
    log.info("Inside verify_bios_version_in_uefi_shell procedure")
    deviceObj = Device.getDeviceObject(device)

    deviceObj.read_until_regexp('Shell>', timeout=10)
    send_str_on_bios(device, 'smbiosview -t 0')

    line3 = 'BiosVersion.*(ATHG[0-9]\.[0-9]\.[0-9][0-9]\.[0-9][0-9])'
    output = deviceObj.read_until_regexp(line3, timeout=10)
    match = re.search(line3, output)

    log.debug("Found '%s'"%(line3))
    log.success(match.group(1))
    if match.group(1) in bios_version:
        log.success("Expected BIOS version is shown in UEFI Shell")
    else:
        log.fail("Expected BIOS version is not shown in UEFI Shell")
        raise testFailed("Expected BIOS version is not shown in UEFI Shell")

################################################################################
# Function Name: exit_uefi_shell
# Parameters :
#    device             : Device Object
#
# Description: Exits UEFI Shell and reboot the Device. Device Connection reset
#              is required after using this proc
################################################################################

def exit_uefi_shell(device):
    log.info("Inside exit_uefi_shell procedure")
    deviceObj = Device.getDeviceObject(device)

    send_str_on_bios(device, 'exit')
    time.sleep(150)

################################################################################
# Function Name : revert_boot_order
# Parameters :
#    device             : Device Object
#    bios_password      : BIOS Password (This can vary depending on setup)
#
# Description: Goes into BIOS and reverts the boot order which was changed by 
#              enter_uefi_shell proc
################################################################################

def revert_boot_order(device,bios_password='c411ie'):
    log.info("Inside revert_boot_order procedure")
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    line1 = 'BIOS Version.*(ATHG[0-9]\.[0-9]\.[0-9][0-9]\.[0-9][0-9])'
    output = deviceObj.read_until_regexp(line1, timeout=10)

    key_strokes_to_reach_boot_menu = 6
    key_strokes_to_reach_boot_option_1 = 3
    key_strokes_to_select_os = 3

    for i in range(key_strokes_to_reach_boot_menu):
        send_key(device, "KEY_RIGHT")

    for i in range(key_strokes_to_reach_boot_option_1):
        send_key(device, "KEY_DOWN")

    send_key(device, "KEY_ENTER")

    line2 = '----- Boot Option #1 -----'
    output = deviceObj.read_until_regexp(line2, timeout=10)

    for i in range(key_strokes_to_select_os):
        send_key(device, "KEY_UP")

    send_key(device, "KEY_ENTER")

    # Exit BIOS
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ENTER")

    time.sleep(120)

################################################################################
# Function Name : send_str_on_bios
# Parameters :
#    device             : Device Object
#    cmd                : Command String to send
#
# Description: Since in BIOS and UEFI Shell there needs to a delay while send 
#              each character of the command string, this function does that
################################################################################

def send_str_on_bios(device,cmd):
    log.info("Inside send_str_on_bios procedure")
    deviceObj = Device.getDeviceObject(device)
    for i in cmd:
        deviceObj.sendline(i, CR=False)
        time.sleep(2)
    send_key(device, "KEY_ENTER")

######################################################################################################
# Function Name : verify_BMC_self_test_status_version_log
# Parameters :
#    device               : Device Object
#    bmc_firmware_version : BMC Firmware Version as per the release notes
#    bios_password        : Password to enter the bios
#
# Description: This function enters to BIOS mode,checks the below steps and exit the bios mode
#     - BMC self test status should be passed
#     - BMC Firmware Revision should be the sameas in release notes
#     - BMC self test log should have the message "Log Empty"
#
######################################################################################################
def verify_BMC_self_test_status_version_log(device,bmc_firmware_version,bios_password='c411ie'):
    log.debug('Entering procedure to get BMS self test status firmware version and log: %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT",times=4)
    line="IPMI Version"
    output_status_version=deviceObj.read_until_regexp(line, timeout=10)
    send_key(device, "KEY_DOWN",times=8)
    send_key(device, "KEY_ENTER")
    line1="Log Empty"
    output_log=deviceObj.read_until_regexp(line1, timeout=10)
    send_key(device, "KEY_ESC")
    time.sleep(5)
    exit_bios_1(device)
    status_pattern="BMC Self Test Status.*PASSED"
    version_pattern="BMC Firmware Revision.*{}".format(bmc_firmware_version)
    log_pattern="Log Empty"
    match=re.search(status_pattern,output_status_version)
    match1=re.search(version_pattern,output_status_version)
    match2=re.search(log_pattern,output_log)
    if match:
        log.info("BMC Self Test Status check is successful")
    else:
        log.fail("BMC Self Test Status check is unsuccessful")
        raise  testFailed("BMC Self Test Status check is unsuccessful")
    if match1:
        log.info("BMC Firmware Revision check is successful")
    else:
        log.fail("BMC Firmware Revision check is unsuccessful")
        raise  testFailed("BMC Firmware Revision check is unsuccessful")
    log.info(output_log)
    if match2:
         log.info("BMC Self Test log check is successful")
    else:
         log.fail("BMC Self Test log check is unsuccessful")
         raise  testFailed("BMC Self Test log check is unsuccessful")

################################################################################
# Function Name: clear_SEL_log_in_BIOS
# Parameters :
#    device             : Device Object
#    bios_password      : Password to enter the bios
#
# Description: Goes into BIOS and clears SEL Logs. Device Connection reset
#              is required after using this proc
################################################################################

def clear_SEL_log_in_BIOS(device,bios_password='c411ie'):
    log.debug('Entering procedure clear_SEL_log_in_BIOS with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    key_strokes_to_reach_Server_Mgmt_menu = 4
    key_strokes_to_reach_SEL_menu = 6
    key_strokes_to_save_and_exit = 3

    send_key(device, "KEY_RIGHT", key_strokes_to_reach_Server_Mgmt_menu)
    send_key(device, "KEY_DOWN", key_strokes_to_reach_SEL_menu)
    send_key(device, "KEY_ENTER")

    line2 = 'Enabling.*Disabling Options'
    output = deviceObj.read_until_regexp(line2, timeout=10)

    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")

    line3 = 'Yes.*On next reset'
    output = deviceObj.read_until_regexp(line3, timeout=10)

    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ESC",delay=5)

    # Exit BIOS
    send_key(device, "KEY_RIGHT",key_strokes_to_save_and_exit)
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ENTER")

    time.sleep(120)

################################################################################
# Function Name: verify_in_BIOS_if_SEL_logs_are_cleared
# Parameters :
#    device             : Device Object
#    bios_password      : Password to enter the bios
#
# Description: Goes into BIOS and verifies if SEL Logs are cleared. Since
#              there could be some logs even after clear command is issues,
#              a variable to tolerate such number of logs is used
################################################################################

def verify_in_BIOS_if_SEL_logs_are_cleared(device,bios_password='c411ie'):
    log.debug('Entering procedure verify_in_BIOS_if_SEL_logs_are_cleared with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    number_of_logs_to_tolerate = 5

    key_strokes_to_reach_Server_Mgmt_menu = 4
    key_strokes_to_reach_view_SEL_logs = 10

    send_key(device, "KEY_RIGHT", key_strokes_to_reach_Server_Mgmt_menu)
    send_key(device, "KEY_DOWN", key_strokes_to_reach_view_SEL_logs)
    send_key(device, "KEY_ENTER")

    line2 = '----- View System Event Log -----'
    output = deviceObj.read_until_regexp(line2, timeout=10)

    send_key(device, "KEY_ENTER")
    time.sleep(40)

    line3 = 'No. of log entries in SEL : ([0-9]*)'
    output = deviceObj.read_until_regexp(line3, timeout=10)
    match = re.search(line3, output)

    log.debug("Found '%s'"%(line3))
    log.success(match.group(1))
    if int(match.group(1)) < number_of_logs_to_tolerate:
        log.success("SEL Logs are cleared as expected")
    else:
        log.fail("SEL Logs are not cleared as expected")
        raise testFailed("SEL Logs are cleared as expected")

    send_key(device, "KEY_ESC", delay=5)

    exit_bios_1(device)

################################################################################
# Function Name: BIOS_Memory_Topology_validation
# Parameters :
#    device             : Device Object
#    pattern_to_check   : Memory pattern to be matched from ESM
#    bios_password      : Password to enter the bios
#
# Description: Goes into BIOS and validates the memory topology.
#           
################################################################################

def BIOS_Memory_Topology_validation(device,pattern_to_check,bios_password='c411ie'):
    log.debug('Entering procedure to validate memory topology in BIOS')
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")
    count =9
    for i in range(count):
        send_key(device, "KEY_UP")
        time.sleep(2)
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ENTER")
    pattern=".*Socket1.*MM.*"
    output = deviceObj.read_until_regexp(pattern, timeout=10)
    log.info(output)
    pattern_to_check=pattern_to_check.splitlines()
    for line in pattern_to_check:
        match=re.search(line,output)
        if match:
            log.success("Memory topology shown as expected")
        else:
            log.fail("Memory topology not shown as expected")
            raise testFailed("Memory topology not shown as expected")
    send_key(device, "KEY_ESC")
    time.sleep(2)
    send_key(device, "KEY_ESC")
    time.sleep(5)
    exit_bios_1(device)


######################################################################################################
# Function Name : verify_version_in_ME
# Parameters :
#    device               : Device Object
#    bmc_firmware_version : ME Firmware Version as per the release notes
#    bios_password        : Password to enter the bios
#
# Description: This function enters to BIOS mode,checks the below steps and exit the bios mode
#     - ME Firmware Version
#     - ME Current  status
#
######################################################################################################
def verify_version_in_ME(device,ME_firmware_version,bios_password='c411ie'):
    log.debug('Entering procedure to get ME Firmware Version and operational status: %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT",times=2)
    send_key(device, "KEY_DOWN",times=2)
    send_key(device, "KEY_ENTER")
    line='Error Code'
    output=deviceObj.read_until_regexp(line, timeout=10)
    send_key(device, "KEY_ESC")
    time.sleep(5)
    exit_bios_1(device)
    log.info(output)
    ME_firmware_version="Oper. Firmware Version.*{}".format(ME_firmware_version)
    Operational_status="Current State.*Operational"
    match1=re.search(ME_firmware_version,output)
    match2=re.search(Operational_status,output)
    if match1:
        log.info("ME_firmware_version check is successful")
    else:
        log.fail("ME_firmware_version check is unsuccessful")
        raise  testFailed("ME_firmware_version check is unsuccessful")
    if match2:
        log.info("ME_firmware_current_status check is successful")
    else:
        log.fail("ME_firmware_current_status check is unsuccessful")
        raise  testFailed("ME_firmware_current_status check is unsuccessful")

################################################################################
# Function Name: change_some_settings_in_BIOS
# Parameters :
#    device             : Device Object
#    bios_password      : Password to enter the bios
#
# Description: Goes into BIOS and does some configs like changing Security 
#              Device Support and Hyper-Threading settings. This may be used
#              to check if config is preserved before/after BIOS FW Upgrade
#              Device Connection reset is required after using this proc
################################################################################

def change_some_settings_in_BIOS(device,bios_password='c411ie'):
    log.debug('Entering procedure change_some_settings_in_BIOS with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_ENTER",2)

    # Change Security Device Support from Enabled to Disabled
    line2 = '---   Security Device Support ----'
    output = deviceObj.read_until_regexp(line2, timeout=10)

    send_key(device, "KEY_UP")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ESC")
    time.sleep(5)

    send_key(device, "KEY_RIGHT",2)
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")

    # Change Hyper-Threading ALL from Enabled to Disabled
    line3 = '--- Hyper-Threading.*ALL.*----'
    output = deviceObj.read_until_regexp(line3, timeout=10)

    send_key(device, "KEY_UP")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ESC")
    time.sleep(5)

    # Exit BIOS
    send_key(device, "KEY_RIGHT",4)
    send_key(device, "KEY_ENTER")
    line4 = '----- Save.*Exit Setup ------'
    output = deviceObj.read_until_regexp(line4, timeout=10)
    send_key(device, "KEY_ENTER")
    time.sleep(30)

################################################################################
# Function Name: verify_settings_saved_in_BIOS
# Parameters :
#    device             : Device Object
#    module             : That Primary Key used in SwImages.yaml
#    bios_password      : Password to enter the bios
#
# Description: Goes into BIOS and used to check if config done using 
#              change_some_settings_in_BIOS is preserved after BIOS FW Upgrade
#              Also checks if BIOS version is correct
#              Device Connection reset is required after using this proc
################################################################################

def verify_settings_saved_in_BIOS(device,module,bios_password='c411ie'):
    log.debug('Entering procedure verify_settings_saved_in_BIOS with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    imageObj = SwImage.getSwImage(module)
    version_to_verify = imageObj.newVersion

    line2 = 'BIOS Version.*(ATHG[0-9]\.[0-9]\.[0-9][0-9]\.[0-9][0-9])'
    output = deviceObj.read_until_regexp(line2, timeout=10)
    match = re.search(line2, output)

    if match:
        log.success(match.group(1))
        if version_to_verify in match.group(1):
           log.success("Expected BIOS version is shown in BIOS")
        else:
           log.fail("Expected BIOS version is not shown in BIOS")
           raise testFailed("Expected BIOS version is not shown in BIOS")

    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_ENTER")

    # Verify if Security Device Support is Disabled
    line2 = 'Security Device Support.*Disable'
    output = deviceObj.read_until_regexp(line2, timeout=10)
    match1 = re.search(line2, output)

    send_key(device, "KEY_ENTER")

    # Change Security Device Support from Enabled to Disabled
    line2 = '---   Security Device Support ----'
    output = deviceObj.read_until_regexp(line2, timeout=10)

    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ESC")
    time.sleep(5)

    send_key(device, "KEY_RIGHT",2)
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_DOWN")

    # Verify if Hyper-Threading ALL is Disabled
    line3 = 'Hyper-Threading.*ALL.*Disable'
    output = deviceObj.read_until_regexp(line3, timeout=10)
    match2 = re.search(line3, output)


    send_key(device, "KEY_ENTER")

    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ESC")
    time.sleep(5)

    # Exit BIOS
    send_key(device, "KEY_RIGHT",4)
    send_key(device, "KEY_ENTER")
    line4 = '----- Save.*Exit Setup ------'
    output = deviceObj.read_until_regexp(line4, timeout=10)
    send_key(device, "KEY_ENTER")
    time.sleep(30)

    if match1 and match2:
        log.success("Config is same as before BIOS FW Upgrade")
    else:
        log.fail("Config is not the same as before BIOS FW Upgrade")
        raise testFailed("Config is not the same as before BIOS FW Upgrade")

################################################################################
# Function Name: NVME_info_validation
# Parameters :
#    device             : Device Object
#    output_check       : Pattern to validate with output 
#    bios_password      : Password to enter the bios
#
# Description: NVME details validation
################################################################################
def NVME_info_validation(device,output_check,device_count,bios_password='c411ie'):
    deviceObj = Device.getDeviceObject(device)
    output_check=output_check.splitlines()
    sn_list=[]
    model_list=[]
    FW_Revision_list=[]
    count_list=[]
    for i in range(device_count):
        count=10+int(i)
        count_list.append(count)
    for line in output_check:
        pattern="^/dev/.*"
        match=re.search(pattern,line)
        line=line.split()
        if match:
            sn_list.append(line[1])
            model_list.append(line[2])
            FW_Revision_list.append(line[14])
    for count in count_list:
        enter_bios_1(device,bios_password)
        send_key(device, "KEY_RIGHT")
        for i in range(count):
            send_key(device, "KEY_DOWN")
            time.sleep(2)
        send_key(device, "KEY_ENTER")
        pattern=".*Healthy.*"
        output = deviceObj.read_until_regexp(pattern, timeout=10)
        sn_count=0
        for i in sn_list:
            pattern = "Serial Number.*{}.*".format(i)
            match=re.search(pattern,output)
            if match:
                log.success("Serial number matched")
                sn_count=sn_count+1
                break
        if sn_count == 0:
            log.fail("Serial number not matched")
            raise testFailed("Serial number not shown as expected")
        model_count=0
        for i in model_list:
             pattern = "Model Number.*{}.*".format(i)
             match=re.search(pattern,output)
             if match:
                 log.success("Model number matched")
                 model_count=model_count+1
                 break
        if sn_count == 0:
            log.fail("Model number not matched")
            raise testFailed("Model number not shown as expected")
        FW_Revision_count=0
        for i in FW_Revision_list:
             pattern = "Firmware Revision.*{}.*".format(i)
             match=re.search(pattern,output)
             if match:
                 log.success("FW Revision number matched")
                 FW_Revision_count=FW_Revision_count+1
                 break
        if FW_Revision_count == 0:
            log.fail("Model number not matched")
            raise testFailed("Model number not shown as expected")
        send_key(device, "KEY_ESC")
        time.sleep(5)
        exit_bios_1(device)
        time.sleep(120)

def UEFI_shell_reset(device,cmd,bios_password='c411ie'):
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_RIGHT")
    send_key(device, "KEY_UP")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp('Shell>', timeout=10)
    CommonLib.send_command("reset -w",promptStr=None)
    time.sleep(160)

################################################################################
# Function Name: get_BMC_fru_info
# Parameters :
#    device             : Device Object
#    bios_password      : Password to enter the bios
#
# Description: The function  returns  all the fru parameters from the BIOS page
################################################################################

def get_BMC_fru_info(device,bios_password='c411ie'):
    log.info("Entering procedure to get fru information")
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT",times=4)
    send_key(device, "KEY_DOWN",times=7)
    send_key(device, "KEY_ENTER")
    line1="needs to be filled by O.E.M"
    output=deviceObj.read_until_regexp(line1, timeout=10)
    send_key(device, "KEY_ESC")
    time.sleep(5)
    exit_bios_1(device)
    return output

#######################################################################################################################################
# Function Name: check_system_event_log
# Parameters :
#    device             : Device Object
#    bios_password      : Password to enter the bios
#
# Description: The function checks whether all the previous logs are cleared and only the log added in the previous step to be present.
########################################################################################################################################

def check_system_event_log(device,bios_password='c411ie'):
    log.info("Entering procedure to verify system event log")
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT",times=4)
    send_key(device, "KEY_DOWN",times=10)
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ENTER")
    line="DATE"
    pattern="No. of log entries in SEL : 2"
    output=deviceObj.read_until_regexp(line, timeout=10)
    send_key(device, "KEY_ESC")
    time.sleep(5)
    exit_bios_1(device)
    match=re.search(pattern,output)
    if match:
        log.info("system event log check successful")
    else:
        log.info("system event log check unsuccessful")
        raise testFailed("system event log check unsuccessful")

################################################################################
# Function Name: verify_BMC_version_in_BIOS
# Parameters :
#    device             : Device Object
#    module             : That Primary Key used in SwImages.yaml
#    action             : upgrade/downgrade
#    bios_password      : Password to enter the bios
#
# Description: Checks if BMC version is correct in BIOS
#              Device Connection reset is required after using this proc
################################################################################

def verify_BMC_version_in_BIOS(device,module,action,bios_password='c411ie'):
    log.debug('Entering procedure verify_BMC_version_in_BIOS with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    imageObj = SwImage.getSwImage(module)

    if action == "upgrade":
      version_to_verify = imageObj.newVersion
    elif action == "downgrade":
      version_to_verify = imageObj.oldVersion
    else:
      log.debug("There is no action")

    send_key(device, "KEY_RIGHT",4)

    line2 = 'BMC Firmware Revision.*([0-9]\.[0-9][0-9])'
    output = deviceObj.read_until_regexp(line2, timeout=10)
    match = re.search(line2, output)

    if match:
        log.success(match.group(1))
        if version_to_verify in match.group(1):
           log.success("Expected BMC version is shown in BIOS")
        else:
           log.fail("Expected BMC version is not shown in BIOS")
           raise testFailed("Expected BMC version is not shown in BIOS")

    exit_bios_1(device)

def enable_p_state(device,bios_password='c411ie'):
    log.debug('Entering procedure enable_p_state with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    send_key(device, "KEY_RIGHT",3)
    send_key(device, "KEY_DOWN",5)
    send_key(device, "KEY_ENTER",1)

    line1 = 'Advanced Power Management Configuration'
    output = deviceObj.read_until_regexp(line1, timeout=10)

    send_key(device, "KEY_DOWN",1)
    send_key(device, "KEY_ENTER",1)

    line2 = 'CPU P State Control'
    output = deviceObj.read_until_regexp(line2, timeout=10)

    send_key(device, "KEY_DOWN",1)
    send_key(device, "KEY_ENTER",1)

    line3 = '--- SpeedStep.*Pstates.*----'
    output = deviceObj.read_until_regexp(line3, timeout=10)

    send_key(device, "KEY_UP",1)
    send_key(device, "KEY_ESC",1)

    line4 = 'SpeedStep.*Pstates.*Enable'
    output = deviceObj.read_until_regexp(line4, timeout=10)

    send_key(device, "KEY_ESC",2)
    send_key(device, "KEY_RIGHT",4)
    send_key(device, "KEY_ENTER")

    line5 = '----- Save.*Exit Setup ------'
    output = deviceObj.read_until_regexp(line5, timeout=10)
    send_key(device, "KEY_ENTER")
    time.sleep(30)


def disable_p_state(device,bios_password='c411ie'):
    log.debug('Entering procedure disable_p_state with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    send_key(device, "KEY_RIGHT",3)
    send_key(device, "KEY_DOWN",5)
    send_key(device, "KEY_ENTER",1)

    line1 = 'Advanced Power Management Configuration'
    output = deviceObj.read_until_regexp(line1, timeout=10)

    send_key(device, "KEY_DOWN",1)
    send_key(device, "KEY_ENTER",1)

    line2 = 'CPU P State Control'
    output = deviceObj.read_until_regexp(line2, timeout=10)

    send_key(device, "KEY_DOWN",1)
    send_key(device, "KEY_ENTER",1)

    line3 = '--- SpeedStep.*Pstates.*----'
    output = deviceObj.read_until_regexp(line3, timeout=10)

    send_key(device, "KEY_DOWN",1)
    send_key(device, "KEY_ESC",1)

    line4 = 'SpeedStep.*Pstates.*Enable'
    output = deviceObj.read_until_regexp(line4, timeout=10)

    send_key(device, "KEY_ESC",2)
    send_key(device, "KEY_RIGHT",4)
    send_key(device, "KEY_ENTER")

    line5 = '----- Save.*Exit Setup ------'
    output = deviceObj.read_until_regexp(line5, timeout=10)
    send_key(device, "KEY_ENTER")
    time.sleep(30)

################################################################################
# Function Name:  Check_PCIE_ports_in_BIOS
# Parameters :
#    device             : Device Object
#    bios_password      : Password to enter the bios
#
# Description: Checks the details of PCIE ports in the BIOS page as per 
# specifications
################################################################################

def Check_PCIE_ports_in_BIOS(device,bios_password='c411ie'):
    log.debug("Entering procedure to check PCIE ports")
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT",3)
    send_key(device, "KEY_DOWN",4)
    send_key(device, "KEY_ENTER",2)
    line="Enable PCI-E Completion Timeout"
    pattern="IOU0.*Auto"
    pattern1="IOU1.*Auto"
    pattern2="IOU2.*Auto"
    pattern3="IOU3.*Auto"
    pattern4="IOU4.*x16"
    output = deviceObj.read_until_regexp(line, timeout=20)
    checkpattern(pattern,output,"check IOU0 PCIE")
    checkpattern(pattern1,output,"check IOU1 PCIE")
    checkpattern(pattern2,output,"check IOU2 PCIE")
    checkpattern(pattern3,output,"check IOU3 PCIE")
    checkpattern(pattern4,output,"check IOU4 PCIE")
    line="PCI-E Port DeEmphasis"
    pattern="PCI-E Port.*Auto.*"
    pattern2="Link Speed.*Auto.*"
    pattern3="Override Max Link Width.*Auto.*"
    send_key(device, "KEY_DOWN",11)
    send_key(device, "KEY_ENTER")
    port_1_output=deviceObj.read_until_regexp(line, timeout=20)
    log.info(port_1_output)
    checkpattern(pattern,port_1_output,"PCI-E")
    checkpattern(pattern2,port_1_output,"Link Speed")
    checkpattern(pattern3,port_1_output,"Override Max Link Width")
    send_key(device, "KEY_ESC")
    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")
    port_2_output=deviceObj.read_until_regexp(line, timeout=20)
    checkpattern(pattern,port_2_output,"PCI-E")
    checkpattern(pattern2,port_2_output,"Link Speed")
    checkpattern(pattern3,port_2_output,"Override Max Link Width")
    send_key(device, "KEY_ESC")
    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")
    port_4_output=deviceObj.read_until_regexp(line, timeout=20)
    checkpattern(pattern,port_4_output,"PCI-E")
    checkpattern(pattern2,port_4_output,"Link Speed")
    checkpattern(pattern3,port_4_output,"Override Max Link Width")
    send_key(device, "KEY_ESC")
    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")
    port_5_output=deviceObj.read_until_regexp(line, timeout=20)
    checkpattern(pattern,port_5_output,"PCI-E")
    checkpattern(pattern2,port_5_output,"Link Speed")
    checkpattern(pattern3,port_5_output,"Override Max Link Width")
    send_key(device, "KEY_ESC",3)

################################################################################
# Function Name:  checkpattern
# Parameters :
#    pattern = The pattern needs to be verified in the output
#    output  = Value needs to be validated with the given pattern
#    testname= Name of the validation done with the given output and pattern
# Description: Checks the availability of the given pattern in the output 
################################################################################

def checkpattern(pattern,output,testname):
    match=re.search(pattern,output)
    if match:
        log.info("check {} is successfull".format(testname))
    else:
        log.info("check {} failed".format(testname))
        raise RuntimeError("check {} Failed".format(testname))

################################################################################
# Function Name:  get_PCIE_in_UEFI_shell
# Parameters :
#    device             : Device Object
#    bios_password      : Password to enter the bios
#
# Description: The proc enters to UEFI shell mode and executed pci -i command
# for all pci devices and returns the output of all devices in a list.
################################################################################
    
def get_PCIE_in_UEFI_shell(device,bios_password='c411ie'):
    deviceObj = Device.getDeviceObject(device)
    send_key(device, "KEY_RIGHT",4)
    send_key(device, "KEY_UP")
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp('Shell>', timeout=10)
    output= CommonLib.send_command("pci",promptStr='Shell>')
    output=output.splitlines()
    pattern="Serial Attached SCSI"
    pci=[]
    for line in output:
        match=re.search(pattern,line)
        if match:
            log.info(line)
            pci.append(line)
    pattern=".*00.*(\S+)(\S+).*(\S+)(\S+).*(\S+)(\S+).*==.*"
    pci_list=[]
    for i in pci:
        match = re.search(pattern,i)
        if match:
            line=match.group(1)+match.group(2)+" "+match.group(3)+match.group(4)+" "+match.group(5)+match.group(6)
            pci_list.append(line)
    pci_i_output_list=[]
    for i in pci_list:
        cmd="pci -i {}".format(i)
        send_str_on_bios(device, cmd)
        line="Shell"
        output = deviceObj.read_until_regexp(line, timeout=10)
        log.info(output)
        pci_i_output_list.append(output)
    CommonLib.send_command("exit")
    exit_bios_1(device)
    return pci_i_output_list

def verify_bios_default_password(device,bios_password='c411ie'):
    log.debug('Entering procedure verify_bios_default_password with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    line1 = 'Enter Password'
    line2 = 'BIOS Version.*(ATHG[0-9]\.[0-9]\.[0-9][0-9]\.[0-9][0-9])'

    deviceObj.getPrompt("centos")
    deviceObj.sendline("")
    deviceObj.sendline("reboot")

    # Enter BIOS Setup Menu

    counter = 30
    while counter >= 0:
        send_key(device, "KEY_DEL")
        counter -= 1
        time.sleep(1)
    output = None
    output = deviceObj.read_until_regexp(line1, timeout=10)
    if output is not None:
       deviceObj.sendline(bios_password)
       time.sleep(5)

    deviceObj = Device.getDeviceObject(device)
    line2 = 'BIOS Version.*(ATHG[0-9]\.[0-9]\.[0-9][0-9]\.[0-9][0-9])'
    output = deviceObj.read_until_regexp(line2, timeout=60)
    match = re.search(line2, output)

    if match:
        log.debug("Found '%s'"%(line2))
        log.success(match.group(1))
        log.success("Successfully entered BIOS with default password")
    else:
        log.fail("Failed to enter BIOS with default password")
        raise testFailed("Failed to enter BIOS with default password")

    exit_bios_1(device)

def enable_watchdog_timer_in_bios(device,bios_password='c411ie'):
    log.debug('Entering procedure enable_watchdog_timer_in_bios with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    send_key(device, "KEY_RIGHT",4)

    line1 = 'OS Watchdog Timer.*Disabled'
    output1 = deviceObj.read_until_regexp(line1, timeout=10)
    match = re.search(line1, output1)

    send_key(device, "KEY_DOWN",5)
    send_key(device, "KEY_ENTER",1)

    line2 = '--- OS Watchdog Timer ----'
    output2 = deviceObj.read_until_regexp(line2, timeout=10)
       
    send_key(device, "KEY_UP",1)
    send_key(device, "KEY_ENTER",1)
    send_key(device, "KEY_DOWN",1)
        
    send_str_on_bios(device, '2')

    send_key(device, "KEY_DOWN",1)
    send_key(device, "KEY_ENTER",1)

    line3 = '--- OS Wtd Timer Policy ----'
    output3 = deviceObj.read_until_regexp(line3, timeout=10)

    send_key(device, "KEY_DOWN",1)
    send_key(device, "KEY_ENTER",1)

    send_key(device, "KEY_RIGHT",3)
    send_key(device, "KEY_ENTER")

    line5 = '----- Save.*Exit Setup ------'
    output = deviceObj.read_until_regexp(line5, timeout=10)
    send_key(device, "KEY_ENTER")
    time.sleep(30)

def disable_watchdog_timer_in_bios(device,bios_password='c411ie'):
    log.debug('Entering procedure disable_watchdog_timer_in_bios with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)

    enter_bios_1(device,bios_password)

    send_key(device, "KEY_RIGHT",4)

    line1 = 'OS Watchdog Timer.*Enabled'
    output1 = deviceObj.read_until_regexp(line1, timeout=10)
    match = re.search(line1, output1)

    send_key(device, "KEY_DOWN",7)
    send_key(device, "KEY_ENTER",1)

    line2 = '--- OS Wtd Timer Policy ----'
    output2 = deviceObj.read_until_regexp(line2, timeout=10)

    send_key(device, "KEY_UP",1)
    send_key(device, "KEY_ENTER",1)

    send_key(device, "KEY_UP",2)
    send_key(device, "KEY_ENTER",1)

    line3 = '--- OS Watchdog Timer ----'
    output3 = deviceObj.read_until_regexp(line3, timeout=10)

    send_key(device, "KEY_DOWN",1)
    send_key(device, "KEY_ENTER",1)

    send_key(device, "KEY_RIGHT",3)
    send_key(device, "KEY_ENTER")

    line5 = '----- Save.*Exit Setup ------'
    output = deviceObj.read_until_regexp(line5, timeout=10)
    send_key(device, "KEY_ENTER")
    time.sleep(30)

def flash_BIOS_under_UEFI_shell_mode(device,image_to_upgrade,bios_flash_cmd,bios_password='c411ie'):
    log.debug('Entering procedure flash_BIOS_under_UEFI_shell_mode with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT",7)
    send_key(device, "KEY_UP",1)
    send_key(device, "KEY_ENTER",2)
    deviceObj.read_until_regexp('Shell>', timeout=60)
    CommonLib.send_command("fs0:",promptStr='FS0:\>')
    CommonLib.send_command("fs1:",promptStr='FS1:\>')
    CommonLib.send_command("ls",promptStr='FS1:\>')
    flash_cmd = f"AfuEfix64.efi {image_to_upgrade} {bios_flash_cmd}"
    log.info(flash_cmd)
    send_str_on_bios(device, flash_cmd)
    output = deviceObj.read_until_regexp('Process completed', timeout=800)
    log.info(output)
    CommonLib.send_command("exit")
    exit_bios_1(device)

def navigate_to_AEP_security(device,bios_password='c411ie'):
    log.debug('Entering procedure to navigate to AEP security')
    deviceObj = Device.getDeviceObject(device)
    enter_bios_1(device,bios_password)
    send_key(device, "KEY_RIGHT",1)
    send_key(device, "KEY_DOWN",10)
    send_key(device, "KEY_ENTER",1)
    send_key(device, "KEY_DOWN",2)
    send_key(device, "KEY_ENTER",1)
    send_key(device, "KEY_DOWN",5)
    send_key(device, "KEY_ENTER",1)
    send_key(device, "KEY_DOWN",1)
    output = deviceObj.read_until_regexp("Back to main menu", timeout=10)
    log.info(output)

def Enable_AEP_security(device):
    log.debug('Entering procedure to enable AEP security')
    deviceObj = Device.getDeviceObject(device)
    send_key(device, "KEY_ENTER",1)
    pwd="1111"
    for i in pwd:
        deviceObj.sendline(i, CR=False)
        time.sleep(2)
    send_key(device, "KEY_ENTER")
    for i in pwd:
        deviceObj.sendline(i, CR=False)
        time.sleep(2)
    log.info("password created")
    output = deviceObj.read_until_regexp("Back to main menu", timeout=10)
    log.info(output)
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ESC",3)
    send_key(device, "KEY_RIGHT",6)
    send_key(device, "KEY_DOWN",2)
    send_key(device, "KEY_ENTER",2)

def verify_AEP_security_state(device,status):
    log.debug('Entering procedure to verify AEP security state')
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.read_until_regexp("Back to main menu", timeout=10)
    if status == "enabled":
        pattern="State:.*Locked.*"
        if re.search(pattern,output):
           log.info("Locked state")
           log.info("security enabled")
    if status == "disabled":
        pattern="State:.*Disabled.*"
        if re.search(pattern,output):
           log.info("Disabled state")
           log.info("security disabled")

def disable_AEP_security(device):
    log.debug('Entering procedure to disable AEP security')
    deviceObj = Device.getDeviceObject(device)
    send_key(device, "KEY_ENTER",1)
    pwd="1111"
    for i in pwd:
        deviceObj.sendline(i, CR=False)
        time.sleep(2)
        log.info(i)
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_UP",5)
    send_key(device, "KEY_ENTER",1)
    pwd="1111"
    for i in pwd:
        deviceObj.sendline(i, CR=False)
        time.sleep(2)
        log.info(i)
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_ESC",3)
    send_key(device, "KEY_RIGHT",6)
    send_key(device, "KEY_DOWN",2)
    send_key(device, "KEY_ENTER",2)

def exit_from_AEP_security(device):
    log.debug("Entering procedure to exit from AEP security page")
    send_key(device, "KEY_ESC",4)
    send_key(device, "KEY_ENTER",1)
