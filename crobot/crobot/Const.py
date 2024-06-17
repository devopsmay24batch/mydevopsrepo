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
BOOT_MODE_ONIE = 'ONIE'
BOOT_MODE_DIAGOS = 'DIAGOS'
BOOT_MODE_BMC = 'OPENBMC'   # it's trick use value'OPENBMC', but BMC and OPENBMC should be one mode
BOOT_MODE_GRUB = 'GRUB'
BOOT_MODE_UBOOT = 'UBOOT'
BOOT_MODE_CENTOS = 'CENTOS'
BOOT_MODE_PYTHON3 = 'PYTHON3'
BOOT_MODE_OPENBMC = 'OPENBMC'
BOOT_MODE_UEFI = 'UEFI'
ONIE_RESCUE_MODE = 'ONIE_RESCUE_MODE'
ONIE_UNINSTALL_MODE = 'ONIE_UNINSTALL_MODE'
ONIE_UPDATE_MODE = 'ONIE_UPDATE_MODE'
ONIE_EMBED_MODE = 'ONIE_EMBED_MODE'
ONIE_INSTALL_MODE = 'ONIE_INSTALL_MODE'
ONIE_DEFAULT_MODE = 'ONIE_INSTALL_MODE'
BOOT_MODE_SEASTONE='SEASTONE'
BOOT_MODE_MOONSTONE='MOONSTONE'

TIMEOUT_DEFAULT = 5
PLATFORM_DELL = 'dell'
PLATFORM_ALI = 'ali'
PLATFORM_JUNIPER = 'juniper'
PLATFORM_FACEBOOK = 'facebook'
PLATFORM_WHITEBOX = 'whitebox'
PLATFORM_KAPOK = 'kapok'
PLATFORM_GOOGLE = 'google'
PLATFORM_EDK2='edk2'
PLATFORM_SEASTONE='seastone'
PLATFORM_MOONSTONE='moonstone'
PLATFORM_GOLDSTONE='goldstone'
PLATFORM_HELGA='Helga'

OPENBMC_PROMT_V3 = 'bmc-oob login:'
OPENBMC_PROMT_V2 = 'bmc-oob. login:'

LOGIN_PROMT = 'login:'
PSW_PROMT = 'assword:'
MATCH_ALL = '<match all>'


BOOTING_TIME = 800
COPYING_TIME = 600
TELNET_CONN_TIMEOUT_DEFAULT = 3
DUT = 'DUT'
SSH_DUT = 'SSH_DUT'

UART_LOG = './output/system/terminal_uart.log'

PROTOCOL_SSH = 'ssh'
PROTOCOL_TELNET = 'telnet'
PROTOCOL_TFTP = 'tftp'
PROTOCOL_HTTP = 'http'

TIME_REG_PROMPT = r'sys\s.*\dm.*\ds'
promptPython3 = r'(>>>)+'
promptUnusual = r'(>)+'

SSH_MAX_TIMEOUT = 800

TABWIDTH = 8

KEY_UP = '\x1b[A'
KEY_DOWN = '\x1b[B'
KEY_CTRL_C = '\x03'
KEY_CTRL_A = '\x01'
KEY_ESC = '\x1B'
KEY_ENTER='\r'
