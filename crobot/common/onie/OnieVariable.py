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
ACTIVATE_CONSOLE_PROMPT = 'Please press Enter to activate this console'
STARTING_DISCOVERY_PROMPT = 'Starting ONIE Service Discovery'

## @WORKAROUND "   an unexpected print out will break the line:
#    discEXT4-fs (sda3): couldn't mount as ext3 due to feature incompatibilities
#    over: installer mode detected.  Running installer."
# INSTALLER_MODE_DETECT_PROMPT = 'discover: installer mode detected'
# UPDATE_MODE_DETECT_PROMPT = 'discover: ONIE update mode detected'
# RESCUE_MODE_DETECT_PROMPT = 'discover: Rescue mode detected'
# UNINSTALL_MODE_DETECT_PROMPT = 'discover: Uninstall mode detected'

INSTALLER_MODE_DETECT_PROMPT = ': installer mode detected'
UPDATE_MODE_DETECT_PROMPT = ': ONIE update mode detected'
RESCUE_MODE_DETECT_PROMPT = ': Rescue mode detected'
UNINSTALL_MODE_DETECT_PROMPT = ': Uninstall mode detected'

ONIE_SYSEEPROM_CMD = "onie-syseeprom"
VALUE_PATTERN = "^\w+_VALUE=(.*)"

TLV_Value_Test = { "Product Name"     : ["0x21", "Seastone400"],
                    "Part Number"      : ["0x22", "R1165-F0001-04"],
                    "Serial Number"    : ["0x23", "R1165F2B028731GD00004"],
                    "Base MAC Address" : ["0x24", "00:E0:EC:C9:B1:B4"],
                    "Manufacture Date" : ["0x25", "12/14/2018 03:01:52"],
                    "Device Version"   : ["0x26", "02"],
                    "Label Revision"   : ["0x27", "R0B"],
                    "Platform Name"    : ["0x28", "arm65-celestica_cs8000-r0"],
                    "MAC Addresses"    : ["0x2A", "3"],
                    "Manufacturer"     : ["0x2B", "CSA"],
                    "Country Code"     : ["0x2C", "US"],
                    "Vendor Name"      : ["0x2D", "CSB"],
                    "Diag Version"     : ["0x2E", "1.2"],
                    "Vendor Extension" : ["0xFD", "0x0c"],
                    "ONIE Version"     : ["0x29", "2017.110.0.2"],
                    "Service Tag"      : ["0x2F", "XYZ1234E"]
        }

QUERY_EEPROM_WRITE_PROTECTION_CMD = "echo WRITE_PROTECT_VALUE=$( i2cget -y -f 8 0x60 0x05 )"
ENABLE_EEPROM_WRITE_CMD = "i2cset -y -f 8 0x60 0x05 0x0"
DISABLE_EEPROM_WRITE_CMD = "i2cset -y -f 8 0x60 0x05 {}"


fail_dict = { "fail":"fail",
              "ERROR":"ERROR",
              "Failure": "Failure",
              "cannot read file":"cannot read file",
              "command not found":"command not found",
              "No such file": "No such file",
              "not found": "not found",
              "Unknown command":"Unknown command",
              "No space left on device": "No space left on device",
              "Command exited with non-zero status": "Command exited with non-zero status"
              }

usb_dir = '/usbdir'
usb_dev = '/dev/sdb1'