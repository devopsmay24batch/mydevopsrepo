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
import os
import sys
import re
import time
import Logger as log
import CRobot
from crobot import Const
from Decorator import *
from crobot.Decorator import logThis

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'common', 'onie'))
sys.path.append(os.path.join(workDir, 'platform/ali'))

import AliCommonVariable as commonVar
import AliOnieVariable as var
import OnieVariable
import OnieLib
import CommonKeywords
import CommonLib
import AliConst
from SwImage import SwImage
try:
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

@logThis
def onieConnect():
    device.loginOnie()
    return

@logThis
def onieDisconnect():
    device.disconnect()
    return

@logThis
def installDiagOS(protocol):
    ### # onie-nos-install tftp://10.10.88.246/onie-installer-x86_64-alibaba_as24-128d-cl-r0.bin
    imageObj = SwImage.getSwImage("DIAGOS")
    package_file = imageObj.newImage
    image_path = imageObj.hostImageDir + '/' + package_file
    cmd = "onie-nos-install %s://%s/%s"%(protocol.lower(), commonVar.tftp_server_ipv4, image_path)
    device.sendCmd(cmd)
    device.read_until_regexp(var.diagos_install_msg, timeout=1200)
    device.read_until_regexp(var.diagos_install_pass, timeout=180)
    device.getPrompt(commonVar.diagos_mode)

@logThis
def switchOnieModeAndCheckOutput(mode):
    device.sendCmd('reboot')
    output = device.readUntil("will be executed automatically in", AliConst.BOOT_TIME)
    device.toTopOnieMenuItem(output)
    time.sleep(1)

    if mode == 'installer':
        device.sendMsg('\r')
        out = getOnieBootMsg()
        CommonKeywords.should_match_a_regexp(out, 'ONIE: OS Install Mode ...')
        log.info('find word: ONIE: OS Install Mode ...')
        CommonKeywords.should_match_a_regexp(out, OnieVariable.INSTALLER_MODE_DETECT_PROMPT)
        log.info('find word: ' + OnieVariable.INSTALLER_MODE_DETECT_PROMPT)
        time.sleep(5)

    elif mode == 'rescue':
        device.keyDown(1)
        device.sendMsg('\r')
        out = getOnieBootMsg()
        CommonKeywords.should_match_a_regexp(out, 'ONIE: Rescue Mode ...')
        log.info('find word: ONIE: Rescue Mode ...')
        CommonKeywords.should_match_a_regexp(out, OnieVariable.RESCUE_MODE_DETECT_PROMPT)
        log.info('find word: ' + OnieVariable.RESCUE_MODE_DETECT_PROMPT)
        if hasError(out):
            raise RuntimeError('have error during boot to onie mode: ' + mode)
        time.sleep(5)

    elif mode == 'uninstall':
        device.keyDown(2)
        device.sendMsg('\r')
        out = getOnieBootMsg()
        CommonKeywords.should_match_a_regexp(out, 'ONIE: OS Uninstall Mode ...')
        log.info('find word: ONIE: OS Uninstall Mode ...')
        CommonKeywords.should_match_a_regexp(out, OnieVariable.UNINSTALL_MODE_DETECT_PROMPT)
        log.info('find word: ' + OnieVariable.UNINSTALL_MODE_DETECT_PROMPT)
        time.sleep(5)

    elif mode == 'update':
        device.keyDown(3)
        device.sendMsg('\r')
        out = getOnieBootMsg()
        CommonKeywords.should_match_a_regexp(out, 'ONIE: ONIE Update Mode ...')
        log.info('find word: ONIE: ONIE Update Mode ...')
        CommonKeywords.should_match_a_regexp(out, OnieVariable.UPDATE_MODE_DETECT_PROMPT)
        log.info('find word: ' + OnieVariable.UPDATE_MODE_DETECT_PROMPT)
        time.sleep(5)

    imageObj = SwImage.getSwImage("ONIE_UPDATER")
    device.sendCmd('')
    output = device.executeCmd('onie-sysinfo -v')
    CommonKeywords.should_match_a_regexp(output, imageObj.newVersion)


def getOnieBootMsg():
    out = device.read_until_regexp('|'.join([OnieVariable.ACTIVATE_CONSOLE_PROMPT, OnieVariable.STARTING_DISCOVERY_PROMPT,"Running uninstaller"]), timeout=AliConst.ONIE_BOOT_TIME)
    device.sendMsg("\n")
    out += device.read_until_regexp(device.promptOnie, timeout=10)
    out = re.sub(var.ext4_fs_msg, '', out)  ## @WORKAROUND avoid ext4_fs_msg break the line
    # log.cprint(out)
    if hasError(out):
        log.error('Find error in getOnieBootMsg')
    return out


@logThis
def uninstallDiagOSUnderOnie():
    device.sendCmd('reboot')
    output = device.readUntil("will be executed automatically in", AliConst.BOOT_TIME)
    device.toTopOnieMenuItem(output)
    time.sleep(3)
    device.keyDown(2)
    device.sendMsg('\r')
    out = getOnieBootMsg()
    CommonKeywords.should_match_a_regexp(out, 'ONIE: OS Uninstall Mode ...')
    log.info('find word: ONIE: OS Uninstall Mode ...')
    CommonKeywords.should_match_a_regexp(out, OnieVariable.UNINSTALL_MODE_DETECT_PROMPT)
    log.info('find word: ' + OnieVariable.UNINSTALL_MODE_DETECT_PROMPT)
    time.sleep(5)

    output = device.read_until_regexp('Uninstall complete.  Rebooting...', 1600)
    output += device.read_until_regexp('reboot: Restarting system', 60)
    if hasError(output):
        log.error('Find error in uninstallDiagOSUnderOnie')
    output = device.readUntil("will be executed automatically in", AliConst.BOOT_TIME)
    if 'SONiC-OS-' in output:
        raise RuntimeError('Uninstall OS failed!')

    device.read_until_regexp('Starting ONIE Service Discovery', AliConst.ONIE_BOOT_TIME)
    device.sendCmd('')
    device.sendCmd('onie-stop')

@logThis
def checkAutoInstallDiagOS(protocol):
    if protocol == 'usb':
        pattern = 'ONIE: Executing installer: file:/{}/{}'.format(OnieVariable.usb_dev, var.sonic_installer)
        device.executeCmd('onie-discovery-start')
    else:
        pattern = 'ONIE: Executing installer: {}://{}/{}'.format(protocol, DeviceMgr.getServerInfo('PC').managementIP, var.sonic_installer)
    device.read_until_regexp(pattern, 480)
    output = device.readUntil('Installed SONiC base image SONiC-OS successfully', AliConst.BOOT_TIME)
    hasInstallError = hasError(output)
    if hasInstallError:
        log.error('has error during install sonic')
    output = device.readUntil("will be executed automatically in", AliConst.BOOT_TIME)
    if 'SONiC-OS-' not in output:
        device.getPrompt(Const.ONIE_INSTALL_MODE, timeout=AliConst.BOOT_TIME)
        raise RuntimeError('install DiagOS failed!')
    output = device.read_until_regexp(device.loginPromptDiagOS, timeout=AliConst.BOOT_TIME)
    hasBootError = hasError(output)
    if hasBootError:
        log.error('has error during install sonic')
    device.getPrompt(Const.BOOT_MODE_DIAGOS, timeout=AliConst.BOOT_TIME)
    # if hasInstallError or hasBootError:  # TEMP_DISABLED, always have error/fail in the print out.
    #     raise RuntimeError('Find error/fail !')

def hasError(output):
    errors = ['error', 'fail']
    matchOne = False
    matches = dict()
    for error in errors:
        for line in output.splitlines():
            res = re.search(error, line, re.IGNORECASE)
            if res:
                log.error('Find {} in: {}'.format(error, line))
                matchOne = True
    return matchOne


@logThis
def prepareOsInstaller(protocol, prepare=True):
    server = DeviceMgr.getDevice('PC')
    server.sendCmd('sudo su')
    server.sendCmd(server.password)

    if protocol == Const.PROTOCOL_TFTP:
        server.executeCmd('cd ' + commonVar.tftp_root_path)
    elif protocol == Const.PROTOCOL_HTTP:
        server.executeCmd('cd ' + commonVar.http_root_path)

    imageObj = SwImage.getSwImage("DIAGOS")
    if protocol == 'usb':
        device.sendCmd('cd /')
        filePathDut = os.path.join(OnieVariable.usb_dir, var.sonic_installer)
        if prepare:
            device.execCmd('mkdir -p {}'.format(OnieVariable.usb_dir))
            device.execCmd('mount {} {}'.format(OnieVariable.usb_dev, OnieVariable.usb_dir))
            filePathServer = os.path.join(commonVar.tftp_root_path, imageObj.hostImageDir, imageObj.newImage)
            dutIp = CommonLib.get_ip_address('DUT', 'eth0')
            cmd = 'scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {} root@{}:{}'.format(filePathServer, dutIp, filePathDut)
            server.sendCmdRegexp(cmd, '100%', timeout=300)
        else:
            device.execCmd('mkdir -p {}'.format(OnieVariable.usb_dir))
            device.execCmd('mount {} {}'.format(OnieVariable.usb_dev, OnieVariable.usb_dir))
            device.executeCmd('rm -f {}'.format(filePathDut))
            device.executeCmd('umount {}'.format(OnieVariable.usb_dir))
    else:
        if prepare:
            server.executeCmd('cp -f {} {}'.format(os.path.join(commonVar.tftp_root_path, imageObj.hostImageDir, imageObj.newImage), var.sonic_installer), timeout=300)
        else:
            server.executeCmd('rm -f {}'.format(var.sonic_installer))


@logThis
def installDiagOsUnderSonic(oldVersion=True):
    device.executeCmd('touch ' + var.specific_file, mode=Const.BOOT_MODE_DIAGOS)
    filePath =  os.path.join('/tmp', 'sonic_os.bin')
    if oldVersion:
        CommonLib.download_image(Const.DUT, 'DIAGOS', destinationDir=filePath, upgrade=False, hostBaseDir=commonVar.tftp_root_path)
    else:
        serverFilePath = os.path.join(commonVar.tftp_root_path, SwImage.getSwImage('DIAGOS').hostImageDir)
        OnieLib.copyFileFromServer(serverFilePath, var.backup_sonic, filePath)
    out = device.executeCmd('sonic_installer install -y ' + filePath)
    if hasError(out):
        log.error('Find error in installDiagOsUnderSonic')
        # raise RuntimeError('Find error during install sonic!')
        pass
    if 'Installed SONiC base image SONiC-OS successfully' in out or 'is already installed' in out:
        log.success('installDiagOsUnderSonic successfully.')
    else:
        raise RuntimeError('installDiagOsUnderSonic failed!')


@logThis
def uninstallDiagOsUnderSonic(oldVersion=False):
    version = SwImage.getSwImage('DIAGOS').oldVersion if oldVersion else var.backup_sonic_version
    out = device.executeCmd('sonic_installer list')
    out = out.split('Available:')[1]
    versionStr=''
    for line in out.splitlines():
        if version in line:
            versionStr = line.strip('')
    out = device.executeCmd('sonic_installer remove -y ' + versionStr)
    if hasError(out):
        raise RuntimeError('Find error when uninstallDiagOsUnderSonic!')
    if 'Image removed' not in out:
        raise RuntimeError('uninstallDiagOsUnderSonic failed!')
    log.success('uninstallDiagOsUnderSonic successfully.')


@logThis
def checkGrubMenu(hasTwoSonic=False):
    device.sendCmd('reboot')
    output = device.readUntil("will be executed automatically in", AliConst.BOOT_TIME)
    log.cprint(output)
    res = re.findall('SONiC-OS-', str(output))
    log.cprint(res)
    # if hasTwoSonic:
    #     patternList = ['SONiC-OS-', 'SONiC-OS-']
    # else:
    #     patternList = ['SONiC-OS-', 'ONIE']
    # CommonKeywords.should_match_ordered_regexp_list(output, patternList)
    device.readUntil(device.loginPromptDiagOS, AliConst.BOOT_TIME)
    device.loginToDiagOS()
    if len(res) == 2 and hasTwoSonic or len(res) == 1 and not hasTwoSonic:
        log.success('checkGrubMenu successfully.')
    else:
        raise RuntimeError('checkGrubMenu failed!')

@logThis
def checkNewInstalledOs(oldVersion=True):
    out = device.executeCmd('sonic_installer list')
    version = SwImage.getSwImage('DIAGOS').oldVersion if oldVersion else var.backup_sonic_version
    # log.cprint(version)
    log.cprint(out)
    pattern = r'Current: SONiC-OS-.*?{}'.format(version)
    if not re.search(pattern, out):
        raise RuntimeError('checkActiveOs failed!')

    out = device.executeCmd('ls ' + var.specific_file)
    if 'No such file or directory' not in out:
        raise RuntimeError('Is not in the new installed os!')

    log.success('checkActiveOs successfully.')

@logThis
def checkOriginalOs():
    device.sendCmd('reboot')
    output = device.readUntil("will be executed automatically in", AliConst.BOOT_TIME)
    device.sendMsg(Const.KEY_CTRL_A)
    device.sendMsg(Const.KEY_CTRL_A)
    time.sleep(3)
    device.sendMsg(Const.KEY_DOWN)
    time.sleep(3)
    device.sendMsg('\r')
    device.readUntil(device.loginPromptDiagOS, AliConst.BOOT_TIME)
    device.loginToDiagOS()

    out = device.executeCmd('ls ' + var.specific_file)
    if 'No such file or directory' in out:
        raise RuntimeError('Is not in the none active os!')
    log.success('checkNoneActiveOs successfully.')


@logThis
def updateOnie(protocol):
    # onie-self-update tftp://192.168.0.1/onie-updater-x86_64-alibaba_as24-128d-cl-r0
    imageObj = SwImage.getSwImage("ONIE_UPDATER")
    package_file = imageObj.newImage
    image_path = imageObj.hostImageDir + '/' + package_file
    cmd = "onie-self-update %s://%s/%s"%(protocol.lower(), commonVar.tftp_server_ipv4, image_path)
    device.sendCmd(cmd + "\n")
    checkOnieUpdateProcess(imageObj)

@logThis
def prepareOnieUpdater(protocol, prepare=True):
    server = DeviceMgr.getDevice('PC')
    server.sendCmd('sudo su')
    server.sendCmd(server.password)
    if protocol == Const.PROTOCOL_TFTP:
        server.executeCmd('cd ' + commonVar.tftp_root_path)
    elif protocol == Const.PROTOCOL_HTTP:
        server.executeCmd('cd ' + commonVar.http_root_path)
    imageObj = SwImage.getSwImage("ONIE_UPDATER")

    if protocol == 'usb':
        device.sendCmd('cd /')
        filePathDut = os.path.join(OnieVariable.usb_dir, imageObj.newImage)
        if prepare:
            device.execCmd('mkdir -p {}'.format(OnieVariable.usb_dir))
            device.execCmd('mount {} {}'.format(OnieVariable.usb_dev, OnieVariable.usb_dir))
            filePathServer = os.path.join(commonVar.tftp_root_path, imageObj.hostImageDir, imageObj.newImage)
            dutIp = CommonLib.get_ip_address('DUT', 'eth0')
            cmd = 'scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {} root@{}:{}'.format(filePathServer, dutIp, filePathDut)
            server.sendCmdRegexp(cmd, '100%', timeout=300)
        else:
            device.execCmd('mkdir -p {}'.format(OnieVariable.usb_dir))
            device.execCmd('mount {} {}'.format(OnieVariable.usb_dev, OnieVariable.usb_dir))
            device.executeCmd('rm -f {}'.format(filePathDut))
            device.executeCmd('umount {}'.format(OnieVariable.usb_dir))
    else:
        if prepare:
            server.executeCmd('cp -f {} {}'.format(os.path.join(commonVar.tftp_root_path, imageObj.hostImageDir, imageObj.newImage), imageObj.newImage))
        else:
            server.executeCmd('rm -f {}'.format(imageObj.newImage))

@logThis
def checkAutoUpdateOnie(protocol):
    imageObj = SwImage.getSwImage("ONIE_UPDATER")
    if protocol == 'usb':
        pattern = 'ONIE: Executing installer: file:/{}/{}'.format(OnieVariable.usb_dev, imageObj.newImage)
        device.executeCmd('onie-discovery-start')
    else:
        pattern = 'ONIE: Executing installer: {}://{}/{}'.format(protocol, DeviceMgr.getServerInfo('PC').managementIP,
                                                                 imageObj.newImage)
    device.read_until_regexp(pattern, AliConst.BOOT_TIME)
    checkOnieUpdateProcess(imageObj)

@logThis
def checkOnieUpdateProcess(imageObj):
    output = device.read_until_regexp('ONIE: Success: Firmware update version|ONIE: Success: Firmware update URL', AliConst.ONIE_BOOT_TIME)
    if hasError(output):
        raise RuntimeError('Have error during update onie!')
    # device.read_until_regexp('ONIE: Rebooting...', timeout=30)
    output = device.readUntil("will be executed automatically in", AliConst.BOOT_TIME)
    device.toTopOnieMenuItem(output)
    time.sleep(1)
    device.keyDown(1)  # select onie rescue mode
    device.sendMsg('\r')
    device.read_until_regexp('Please press Enter to activate this console', AliConst.BOOT_TIME)
    device.sendCmd('')
    output = device.executeCmd('onie-sysinfo -v')
    CommonKeywords.should_match_a_regexp(output, imageObj.newVersion)

@logThis
def rebootToOnieMode(mode):
    device.sendCmd('reboot')
    output = device.readUntil("will be executed automatically in", AliConst.BOOT_TIME)
    device.toTopOnieMenuItem(output)
    time.sleep(1)

    if mode == Const.ONIE_INSTALL_MODE:
        device.sendMsg('\r')
        device.read_until_regexp(OnieVariable.STARTING_DISCOVERY_PROMPT, AliConst.ONIE_BOOT_TIME)
    elif mode == Const.ONIE_RESCUE_MODE:
        device.keyDown(1)
        device.sendMsg('\r')
        device.read_until_regexp(OnieVariable.ACTIVATE_CONSOLE_PROMPT, AliConst.ONIE_BOOT_TIME)
    elif mode == Const.ONIE_UPDATE_MODE:
        device.keyDown(3)
        device.sendMsg('\r')
        device.read_until_regexp(OnieVariable.STARTING_DISCOVERY_PROMPT, AliConst.ONIE_BOOT_TIME)
    device.sendCmd('')

@logThis
def shouldHaveNoDiscoveryMessage():
    try:
        device.readUntil(OnieVariable.STARTING_DISCOVERY_PROMPT, timeout=60)
        raise RuntimeError("Find discovery massage")
    except:
        pass
    try:
        device.readUntil('Info: Attempting ', timeout=60)
        raise RuntimeError("Find discovery Attempting massage")
    except:
        pass

@logThis
def verifyMacAddress(mac):
    currentMac = CommonLib.get_mac_address('DUT', 'eth0')
    if currentMac != mac:
        raise RuntimeError('verify mac address failed, current mac: {}, expected mac: {}'.format(currentMac, mac))

@logThis
def restoreMacAddress(mac):
    if mac is None:
        log.warning('mac is None!')
        return
    device.execCmd('onie-syseeprom -s 0x24=' + mac)
    rebootToOnieMode(Const.ONIE_RESCUE_MODE)

@logThis
def changeModeTest():
    device.getPrompt(Const.ONIE_INSTALL_MODE)
    device.getPrompt(Const.BOOT_MODE_DIAGOS)
    out = device.executeCmd('pwd')
    log.cprint(out)
    device.getPrompt(Const.BOOT_MODE_OPENBMC)
    device.getPrompt(Const.ONIE_RESCUE_MODE)
    device.getPrompt(Const.ONIE_UPDATE_MODE)
    device.getPrompt(Const.ONIE_INSTALL_MODE)
    device.getPrompt(Const.BOOT_MODE_OPENBMC)
    device.getPrompt(Const.BOOT_MODE_DIAGOS)

@logThis
def checkDiscoveryMessage(shouldHasDiscoveryMsg=True):
    output = device.receive(Const.MATCH_ALL, 180)
    if 'Info: Attempting' in output:
        if shouldHasDiscoveryMsg:
            log.success('Find Discovery Message as expected.')
        else:
            raise RuntimeError('Find Discovery Message unexpectedly!')
    else:
        if shouldHasDiscoveryMsg:
            raise RuntimeError('Can not Find Discovery Message!')
        else:
            log.success('Do not Find Discovery Message as expected.')

