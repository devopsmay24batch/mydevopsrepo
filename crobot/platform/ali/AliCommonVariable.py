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
import logging
import DeviceMgr
from SwImage import SwImage
from Const import *
import AliConst

devicename = os.environ.get("deviceName", "").lower()
logging.info("devicename:{}".format(devicename))

pc_info = DeviceMgr.getServerInfo('PC')
dev_info = DeviceMgr.getDevice()

diagos_mode = BOOT_MODE_DIAGOS
uefi_mode = BOOT_MODE_UEFI
# uboot_mode = BOOT_MODE_UBOOT
onie_mode = BOOT_MODE_ONIE
openbmc_mode = BOOT_MODE_OPENBMC
python3_mode = BOOT_MODE_PYTHON3

# SwImage shared objects
DIAG = SwImage.getSwImage("DIAG")
# End of SwImage shared objects

# uboot_prompt = dev_info.promptUboot
onie_prompt = dev_info.promptOnie
diagos_prompt = dev_info.promptDiagOS
python3_prompt = AliConst.PROMPT_PYTHON
uefi_prompt = AliConst.PROMPT_UEFI

tftp_server_ipv4 = ssh_server_ipv4 = pc_info.managementIP
tftp_interface = dhcp_interface = "eth0"
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
openbmc_username = dev_info.bmcUserName
openbmc_password = dev_info.bmcPassword
diagos_username = dev_info.userName
diagos_password = dev_info.password

keys_switch_to_sonic = list(dev_info.keysSwitchToCpu)
keys_switch_to_openbmc = list(dev_info.keysSwitchToBmc)
keys_sol_to_sonic = ["sol.sh", "\r\n"]
keys_sol_to_openbmc = ["\x0c", "x"]

tftp_root_path = "/var/lib/tftpboot"
http_root_path = "/var/www/html"

diag_deb_path = DIAG.hostImageDir
diag_deb_new_package = DIAG.newImage
diag_deb_new_version = DIAG.newVersion
diag_deb_save_to = DIAG.localImageDir

diag_new_version_patterns = r"(?mi)^[ \t]*diag[ \t]+version[ \t]*:[ \t]*(?P<diag_version>" + diag_deb_new_version + r")[ \t]*$"

bmc_diag_utility_path = '/var/log/BMC_Diag/utility'
diagos_cpu_diag_path = '/usr/local/migaloo/CPU_Diag'

regularly_unexpected_patterns = [
    r"(?i)error",
    r"(?i)fail",
    r"(?i)No such file or directory",
    r"(?i)command not found"
]

if 'shamu' in devicename:
    diagos_cpu_diag_path = '/usr/local/CPU_Diag/bin'
