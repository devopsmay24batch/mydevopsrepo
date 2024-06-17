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
##### Variable file used for ses.robot #####
#import ses_lib
ESM_prompt="ESM \w \$"
G_RETRY_COUNT = '3x'
ESMA_IP = '10.204.82.115'
ESMA_port = '2031'
ESMB_IP = '10.204.82.115'
ESMB_port = '2032'
ESMA_IP_1 ='10.204.82.115'
ESMA_port_1 = '2031'
ses_page_tmp_file = 'ses_page_tmp_file'
fail_dict = { "fail"             : "fail",
              "ERROR"            : "ERROR",
              "Failure"          : "Failure",
              "cannot read file" : "cannot read file",
              "command not found": "command not found",
              "No such file"     : "No such file",
              "not found"        : "not found",
              "Unknown command"  : "Unknown command",
              "No space left on device"            : "No space left on device",
              "Command exited with non-zero status": "Command exited with non-zero status"
              }
threshold_type_dict = {
        "low warning"  : "2:7:8",
        "low critical" : "3:7:8",
        "high critical": "high_crit",
        "high warning" : "high_warn"
        }
descriptor_length_dict = {
        "Array device slot" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Power supply" : [0x48, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Cooling": [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Temperature sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Enclosure services controller electronics" : [0x50, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Enclosure" : [0x50, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Voltage sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "SAS expander" : [0x20, "Element \d+ descriptor:\s+(.*)\r\n"],
        "SAS connector" : [0x58, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Current sensor" : [0x10, "Element \d+ descriptor:\s+(.*)\r\n"],
        "Display" : [0x40, "Element \d+ descriptor:\s+(.*)\r\n"]
        }
elements_status_dict = {
        "Array device slot"  : "Element (\d+) descriptor:.*?\n.*?status: (\w+)",
        "Power supply"       : "Element (\d+) descriptor:.*?\n.*?status: (\w+)",
        "Cooling"            : "Element (\d+) descriptor:.*?\n.*?status: (\w+)",
        "Temperature sensor" : "Element (\d+) descriptor:.*?\n.*?status: (\w+)",
        "Enclosure"          : "Element (\d+) descriptor:.*?\n.*?status: (\w+)",
        "Voltage sensor"     : "Element (\d+) descriptor:.*?\n.*?status: (\w+)",
        "SAS expander"       : "Element (\d+) descriptor:.*?\n.*?status: (\w+)",
        "SAS connector"      : "Element (\d+) descriptor:.*?\n.*?status: (\w+)",
        "Current sensor"     : "Element (\d+) descriptor:.*?\n.*?status: (\w+)",
        "Display"            : "Element (\d+) descriptor:.*?\n.*?status: (\w+)",
        "Enclosure services controller electronics" : "Element (\d+) descriptor:.*?\n.*?status: (\w+)"
        }
check_sbb_cmd = "sg_ses --page=0x2 -I esc,0 --get=2:7:4 "
check_sbb_result = { "2" : "^2$" }
check_sbb_result_lenovo = { "3" : "^3$" }
check_sbb_result_nebula = { "0" : "^0$" }
bsp_expander_cmd = "ls /dev/bsg/expander*"
search_bsp_expander = { "/dev/bsg/expander*" : "/dev/bsg/expander-\d+" }
HDD_RESET_TIME = 35
ESM_BOOTING_TIME = 60
reset_expander_00_cmd = "sg_senddiag -p -r 04,00,00,04,a0,00,00,00"
reset_expander_01_cmd = "sg_senddiag -p -r 04,00,00,04,a0,00,00,01"
reset_expander_03_cmd = "sg_senddiag -p -r 04,00,00,04,a0,00,00,03"
reset_expander_0x_cmd = "sg_senddiag -p -r 10,00,00,07,00,00,61,62,6f,75,74"
get_pagex_cmd = "sg_ses -p 0x10"
get_page2_cmd = "sg_ses -p 2"
get_page7_cmd = "sg_ses -p 7"
get_pageA_cmd = "sg_ses -p 0xa"
esm_fw_version_pattern = {"FW Revision": "([0-9.]+)"}
download_microcode_mode7_cmd = "sg_ses_microcode -b 4096 -m 7"
download_microcode_modeE_cmd = "sg_ses_microcode -b 4096 -m 0xe"
download_cpld_microcode_modeE_cmd_titan_g2_wb = "sg_ses_microcode -b 4096 -m 0xe -i 4"
download_microcode_modeE_cmd_nebula = "sg_ses_microcode -b 3072 -m 0xe"
download_microcode_modeE_cmd_Athena = "sg_ses_microcode -b 3072 -m 0xe"
download_microcode_mode7_4k_cmd = "sg_ses_microcode -m 7 -b 4k"
download_microcode_mode7_3k_cmd = "sg_ses_microcode -m 7 -b 3k"
sg_write_buffer_mode7_cmd = "sg_write_buffer -b 4k -m 7"
fw_active_cmd = "sg_ses_microcode -m 0xf"
fw_active_fail_msg_fault_image = "mc offset=0: status: Unexpected activate_mc received \[0x85, additional=0x0\]"
check_modeE_cmd = "sg_ses -p 0xe"
modeE_status = {"No download microcode operation in progress":
        "No download microcode operation in progress"}
modeE_downloading_status = {"Download in progress": "Download in progress"}
modeE_downloading_status_Athena = ".*download microcode status: No download microcode operation in progress \[0x0\].*"
sensor_pattern_dict = {
        "Temperature sensor": "Element\s+(\d+)\s+descriptor.*?\n.*?\n.*?\n.*?\n.*?Temperature=(\d{2,})\s+C",
        "Voltage sensor"    : "Element\s+(\d+)\s+descriptor.*?\n.*?\n.*?\n.*?\n.*?Voltage:\s+(\d[.0-9]*)\s+volts",
        }
index_abbr_dict = {
        "Voltage sensor" : "vs",
        "Temperature sensor" : "ts"
        }
setting_threshold_waiting = 5
check_scsi_ready_cmd  = "scsi_ready"
scsi_ready_pattern = {"ready": "^\s+ready\s*$"}
Fru_in_cmd_list = [
    'sg_senddiag -p -r 12,00,00,05,02,07,00,02,09 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,09,14,43,75,73,74,6F,6D,65,72,20,41,73,73,20,53,4E,20,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,07,00,02,09 /dev/sg'
]
Fru_fa_cmd_list = [
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,09,10,43,75,73,74,6F,6D,65,72,20,41,73,73,20,53,4E,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,09,15,43,75,73,74,6F,6D,65,72,20,41,73,73,20,53,4E,20,20,20,20,20,30 /dev/sg'
]
chassis_in_cmd_list = [
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,01,01 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,01,01,14,52,31,30,36,36,2D,46,31,30,31,33,2D,30,33,20,20,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,01,01 /dev/sg'
]
chassis_fa_cmd_list= [
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,01,01,0e,52,31,30,36,36,2D,46,31,30,31,33,2D,30,33 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,01,01,15,52,31,30,36,36,2D,46,31,30,31,33,2D,30,33,20,20,20,20,20,20,20 /dev/sg'
]
chassis_in_cmd_list_77 = [
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,01,02 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,01,02,14,46,46,46,46,46,48,48,48,48,48,48,59,59,57,57,53,53,53,53,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,01,02 /dev/sg'
]
chassis_fa_cmd_list_77 = [
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,01,02,0e,46,46,46,46,46,48,48,48,48,48,48,59,59,57 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,01,02,15,46,46,46,46,46,48,48,48,48,48,48,59,59,57,57,53,53,53,53,20,20 /dev/sg'
]
chassis_in_cmd_list_78 = [
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,02,02 /dev/sg',
    'sg_senddiag -p -r 12,00,00,15,01,0e,00,02,02,0f,44,52,49,56,45,20,42,4F,41,52,44,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,02,02 /dev/sg'
]
chassis_fa_cmd_list_78 = [
    'sg_senddiag -p -r 12,00,00,15,01,0e,00,02,02,0B,44,52,49,56,45,20,42,4F,41,52,44 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,01,02,16,46,46,46,46,46,48,48,48,48,48,48,59,59,57,57,53,53,53,53,20,20,20 /dev/sg'
]
chassis_in_cmd_list_79 = [
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,02,03 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,02,03,14,46,46,46,46,46,48,48,48,48,48,48,59,59,57,57,53,53,53,53,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,02,03 /dev/sg'
]
chassis_fa_cmd_list_79 = [
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,02,03,10,46,46,46,46,46,48,48,48,48,48,48,59,59,57,57,53 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,02,03,15,46,46,46,46,46,48,48,48,48,48,48,59,59,57,57,53,53,53,53,20,20 /dev/sg'
]
chassis_in_cmd_list_80 = [
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,02,04 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,02,04,14,52,31,30,36,36,2D,47,30,30,34,34,2D,30,32,20,20,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,02,04 /dev/sg'
]
chassis_fa_cmd_list_80 = [
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,02,04,10,52,31,30,36,36,2D,47,30,30,34,34,2D,30,32,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,02,04,15,52,31,30,36,36,2D,47,30,30,34,34,2D,30,32,20,20,20,20,20,20,20 /dev/sg'
]
chassis_in_cmd_list_81 = [
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,03,06 /dev/sg',
    'sg_senddiag -p -r 12,00,00,0e,01,0e,00,03,06,08,30,31,32,33,34,35,36,37 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,03,06 /dev/sg'
]
chassis_fa_cmd_list_81 = [
    'sg_senddiag -p -r 12,00,00,0e,01,0e,00,03,06,06,30,31,32,33,34,35 /dev/sg',
    'sg_senddiag -p -r 12,00,00,0e,01,0e,00,03,06,09,30,31,32,33,34,35 /dev/sg'
]
chassis_in_cmd_list_82 = [
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,04,02 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,04,02,14,52,30,38,38,35,2D,46,30,31,30,33,2D,30,31,20,20,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,04,02 /dev/sg'
]
chassis_fa_cmd_list_82 = [
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,04,02,10,52,30,38,38,35,2D,46,30,31,30,33,2D,30,31,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,04,02,15,52,30,38,38,35,2D,46,30,31,30,33,2D,30,31,20,20,20,20,20,20,20 /dev/sg'
]
chassis_in_cmd_list_83 = [
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,04,03 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,04,03,14,47,30,38,38,35,58,45,44,43,52,46,56,54,47,42,59,48,4E,55,4A /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,04,03 /dev/sg'
]
chassis_fa_cmd_list_83 = [
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,04,03,10,47,30,38,38,35,58,45,44,43,52,46,56,54,47,42,59 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,04,03,15,47,30,38,38,35,58,45,44,43,52,46,56,54,47,42,59,48,4E,55,4A,30 /dev/sg'
]
chassis_in_cmd_list_84 = [
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,05,02 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,05,02,14,43,75,73,74,6F,6D,65,72,20,41,73,73,20,50,4E,20,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,05,02 /dev/sg'
]
chassis_fa_cmd_list_84 = [
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,05,02,10,43,75,73,74,6F,6D,65,72,20,41,73,73,20,50,4E,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,05,02,14,43,75,73,74,6F,6D,65,72,20,41,73,73,20,50,4E,20,20,20,20,20,30 /dev/sg'
]
chassis_in_cmd_list_85 = [
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,05,03 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,05,03,14,43,75,73,74,6F,6D,65,72,20,41,73,73,20,53,4E,20,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,0e,00,05,03 /dev/sg'
]
chassis_fa_cmd_list_85 = [
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,05,03,10,43,75,73,74,6F,6D,65,72,20,41,73,73,20,53,4E,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,0e,00,05,03,15,43,75,73,74,6F,6D,65,72,20,41,73,73,20,53,4E,20,20,20,20,20,30 /dev/sg'
]
chassis_in_cmd_list_86 = [
    'sg_senddiag -p -r 12,00,00,05,02,07,00,01,02 /dev/sg',
    'sg_senddiag -p -r 12,00,00,15,01,07,00,01,02,0f,50,4D,43,20,45,53,4D,20,20,20,20,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,07,00,01,02 /dev/sg'
]
chassis_fa_cmd_list_86 = [
    'sg_senddiag -p -r 12,00,00,15,01,07,00,01,02,0b,50,4D,43,20,45,53,4D,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,15,01,07,00,01,02,10,50,4D,43,20,45,53,4D,20,20,20,20,20,20,20,20,30 /dev/sg'
]
chassis_in_cmd_list_87 = [
    'sg_senddiag -p -r 12,00,00,05,02,07,00,01,03 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,01,03,14,46,46,46,46,46,48,48,48,48,48,48,59,59,57,57,53,53,53,53,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,07,00,01,03 /dev/sg'
]
chassis_fa_cmd_list_87 = [
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,01,03,10,46,46,46,46,46,48,48,48,48,48,48,59,59,57,57,53 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,01,03,15,46,46,46,46,46,48,48,48,48,48,48,59,59,57,57,53,53,53,53,20,20 /dev/sg'
]
chassis_in_cmd_list_88 = [
    'sg_senddiag -p -r 12,00,00,05,02,07,00,01,04 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,01,04,14,52,31,31,33,36,2D,47,30,30,30,32,2D,30,32,20,20,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,07,00,01,04 /dev/sg'
]
chassis_fa_cmd_list_88 = [
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,01,04,10,52,31,31,33,36,2D,47,30,30,30,32,2D,30,32,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,01,04,16,52,31,31,33,36,2D,47,30,30,30,32,2D,30,32,20,20,20,20,20,30 /dev/sg'
]
chassis_in_cmd_list_89 = [
    'sg_senddiag -p -r 12,00,00,05,02,07,00,02,02 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,02,14,52,30,38,38,35,2D,46,30,31,30,33,2D,30,31,20,20,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,07,00,02,02 /dev/sg'
]
chassis_fa_cmd_list_89 = [
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,02,10,52,30,38,38,35,2D,46,30,31,30,33,2D,30,31,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,02,15,52,30,38,38,35,2D,46,30,31,30,33,2D,30,31,20,20,20,20,20,20,20 /dev/sg'
]
chassis_in_cmd_list_90 = [
    'sg_senddiag -p -r 12,00,00,05,02,07,00,02,03 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,03,14,47,30,38,38,35,58,45,44,43,52,46,56,54,47,42,59,48,4E,55,4A /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,07,00,02,03 /dev/sg'
]
chassis_fa_cmd_list_90 = [
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,03,10,47,30,38,38,35,58,45,44,43,52,46,56,54,47,42,59 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,03,15,47,30,38,38,35,58,45,44,43,52,46,56,54,47,42,59,48,4E,55,4A,30 /dev/sg'
]
chassis_in_cmd_list_91 = [
    'sg_senddiag -p -r 12,00,00,05,02,07,00,02,08 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,08,14,43,75,73,74,6F,6D,65,72,20,41,73,73,20,50,4E,20,20,20,20,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,05,02,07,00,02,08 /dev/sg'
]
chassis_fa_cmd_list_91 = [
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,08,10,43,75,73,74,6F,6D,65,72,20,41,73,73,20,50,4E,20 /dev/sg',
    'sg_senddiag -p -r 12,00,00,1a,01,07,00,02,08,14,43,75,73,74,6F,6D,65,72,20,41,73,73,20,50,4E,20,20,20,20,20,30 /dev/sg'
]
compare_FRU_SN = 'CAN.*Ass[ \t]+SN'
FRU_SN = 'r.*SN'
right_pattern_SN = 'Ass SN'
compare_FRU_SN_76 = 'Chassis Part Number\: R1066-F1013-03'
compare_FRU_PN = 'CAN.*Ass[ \t]+PN'
FRU_PN = 'r.*PN'
right_pattern_PN = 'Ass PN'
FRU_SN_76 = '1013\-03'
compare_90 = 'Assembly SN\: G0885XEDCRFVTGBYHNUJ'
FRU_90 = 'EDCRFVTGBYHNU'
right_pattern_90 = 'EDC.*U'
compare_89 = 'Assembly PN\: R0885\-F0103\-01'
FRU_89 = 'F0103\-01'
right_pattern_89 = 'F.*\-01'
compare_88 = 'Part Number\: R1136\-G0002\-02'
FRU_88 = 'G0002\-02'
right_pattern_88 = 'G.*\-\d{2}'
compare_87 = 'Serial Number\: FFFFFHHHHHHYYWWSSSS'
FRU_87 = 'HHHHYYWWSSSS'
right_pattern_87 = 'H.*SSSS'
compare_86 = 'Product Name\: PMC ESM'
FRU_86 = '\.{10}PMC ES'
right_pattern_86 = 'PMC ES'
compare_85 = 'Customer Assembly SN\: Customer Ass SN'
compare_84 = 'Customer Assembly PN\: Customer Ass PN'
compare_83 = 'Assembly SN\: G0885XEDCRFVTGBYHNUJ'
FRU_83 = 'DCRFVTGBYHNUJ'
right_pattern_83 = 'D.*NUJ'
compare_82 = 'Assembly PN\: R0885-F0103-01'
FRU_82 = '0103-01'
right_pattern_82 = '01.*01'
compare_80 = 'Midplane Part Number\: R1066-G0044-02'
FRU_80 = '0044\-02'
right_pattern_80 = '0{2}4{2}\-02'
compare_79 = 'Midplane Serial Number\: FFFFFHHHHHHYYWWSSSS'
compare_78 = 'Midplane Product Name\: DRIVE BOARD'
FRU_78 = 'OARD'
right_pattern_78 = 'OARD'
compare_77 = 'Chassis Serial Number\: FFFFFHHHHHHYYWWSSSS'

sg_inquiry_cmd = "sg_inq"
sq_inquiry_pattern = {
        "Vendor identification" : "(\S+)",
        "Product identification": "(\S+)",
        "Product revision level": "(\S+)",
        "Unit serial number"    : "(\S+)"
        }
sq_inquiry_length = {
        "Vendor identification" : 8,
        "Product identification": 16,
        "Product revision level": 4,
        "Unit serial number"    : 20
        }
sq_inquiry_length_Athena = {
        "Vendor identification" : 8,
        "Product identification": 5,
        "Product revision level": 4,
        "Unit serial number"    : 32
        }
sq_inquiry_pattern_Athena = {
        "Vendor identification"  : "(\S+)",
        "Product identification" : "(\S+)",
        "Product revision level" : "(\S+)",
        "Unit serial number"     : "(\S+)"
        }
sg_inquiry_page_0x00_cmd = "{} -p 0x00".format(sg_inquiry_cmd)
sg_inquiry_page_0x00_pattern = {
        "0x00": "\s00\s",
        "0x83": "\s83",
        "0x80": "\s80\s"
        }
sg_inquiry_page_0x80_cmd = "{} -p 0x80".format(sg_inquiry_cmd)
sq_inquiry_pattern_VPD_80_Athena = {
        "Unit serial number" : "(\S+)"}
sq_inquiry_length_VPD_80_Athena = {"Unit serial number" : 32}

sq_inquiry_length = {"Unit serial number" : 16}
sq_inquiry_pattern = {
        "Unit serial number" : "(\S+)"}

sg_inquiry_page_0x83_cmd = "{} -p 0x83 -H".format(sg_inquiry_cmd)
sg_inquiry_page_0x83_pattern = {
        "00     0d 83 00 20 01 03 00 08 "    : "00     0d 83 00 20 01 03 00 08 ",
        "10     61 93 00 08 ... 61 94 00 04" : "10     61 93 00 08[\s\da-f]+61 94 00 04",
        "20     01 00 00 00"                 : "20     01 00 00 00"
        }

sg_inquiry_page_0x83_pattern_Athena = {
        "00     0d 83 00 18 01 03 00 08  50 0e 0e ca 06 63 dc 00 "    : "00     0d 83 00 18 01 03 00 08  50 0e 0e ca 06 63 dc 00 ",
        "10     01 13 00 08 50 0e 0e ca  06 63 dc ff" : "10     01 13 00 08 50 0e 0e ca  06 63 dc ff"
        }
set_log_sense_cmd = "sg_logs -S -p 0x30,0x01"
set_log_sense_pattern = { "CELESTIC": "CELESTIC.*?\d+" }
get_log_sense_cmd = "sg_logs -p 0x00,0xff"
get_log_sense_pattern = {
        "CELESTIC"  : "CELESTIC.*?\d+",
        "log sense:": "log sense:",
        "Driver_status ... DRIVER_OK": "Driver_status.*?DRIVER_OK",
        "Supported log pages and subpages": "Supported log pages and subpages"
        }
select_control_mode_cmd = "sg_modes --page=0x0a --maxlen=0x0a"
select_control_mode_pattern = {
        "CELESTIC"  : "CELESTIC.*?\d+",
        "Mode parameter header from MODE SENSE(10)": "Mode parameter header from MODE SENSE\(10\)",
        "Mode data length=10": "Mode data length=10",
        "Control, page_control: current": "Control, page_control: current"
        }
select_protocol_specific_mode_cmd = "sg_modes --page=0x19 --maxlen=0x0e"
select_protocol_specific_mode_pattern = {
        "CELESTIC"  : "CELESTIC.*?\d+",
        "Mode data length=14": "Mode data length=14",
        "Block descriptor length=0": "Block descriptor length=0",
        "Protocol specific port (SAS)":
          "Protocol specific port \(SAS\), page_control: current"
        }
#############################CONSR-SEST-SPCK-0002-0001#########################
ses_version_read_by_01h = '0398'
ses_page_01h_gold_file = 'ses_page_01h_gold_file'
ses_page_01h_gold_file_2 = 'ses_page_01h_gold_file_2'
ses_page_01h_gold_file_ESMB = 'ses_page_01h_gold_file_ESMB'
ses_page_01h_gold_file_2_ESMB='ses_page_01h_gold_file_2_ESMB'
ses_page_01h_info = {
    'rev:\s+(\S+)' : '0398',
    'number of secondary subenclosures:\s+(\S+)' : '0',
    'generation code:\s+(\S+)' : '0x0',
    'Subenclosure identifier:\s+(.+)' : '0 [primary]',
    'relative ES process id:\s+(\w+)' : '1',
    'number of ES processes:\s+(\S+)' : '2',
    'number of type descriptor headers:\s+(\S+)' : '11',
    'enclosure logical identifier \(hex\):\s+(.+)' : '500e0eca09228c00',
    'enclosure vendor:\s+(\S+)' : 'CELESTIC',
}
##############################CONSR-SEST-SPCK-0003-0001#########################
ses_page_02h_gold_file_1 = 'ses_page_02h_gold_file_1'
ses_page_02h_gold_file_2 = 'ses_page_02h_gold_file_2'
ses_page_02h_gold_file_1_ESMB = 'ses_page_02h_gold_file_1_ESMB'
ses_page_02h_gold_file_2_ESMB = 'ses_page_02h_gold_file_2_ESMB'
##############################CONSR-SEST-SPCK-0020-0001#########################
fan_speed_1 = '11'
fan_speed_cli_1 = '50%'
fan_speed_2 = '10'
fan_speed_cli_2 = '40%'
fan_speed_1_Athena = "11"
fan_speed_cli_1_Athena = "60"
fan_speed_2_Athena = '12'
fan_speed_cli_2_Athena = '70%'
##############################CONSR-SEST-SPCK-0021-0001#########################
fan_max_speed = '15'
fan_max_speed_titan_g2_wb = '14'
fan_max_speed_cli = '90%'
fan_max_speed_cli_Athena = '100%'
##############################CONSR-SEST-SPCK-0021-0001#########################
fan_min_speed = '9'
fan_min_speed_cli = '35%'
fan_min_speed_cli_Athena = '55%'
##############################CONSR-SEST-SPCK-0037-0001#########################
ses_page_04h_gold_file = 'ses_page_04h_gold_file'
ses_page_05h_gold_file = 'ses_page_05h_gold_file'
ses_page_07h_gold_file = 'ses_page_07h_gold_file'
ses_page_a_gold_file_1 = 'ses_page_a_gold_file_1'
ses_page_a_gold_file_2 = 'ses_page_a_gold_file_2'
ses_page_e_gold_file = 'ses_page_e_gold_file'
ses_page_04h_gold_file_ESMB='ses_page_04h_gold_file_ESMB'
ses_page_04h_gold_file_ESMB = 'ses_page_04h_gold_file_ESMB'
ses_page_05h_gold_file_ESMB = 'ses_page_05h_gold_file_ESMB'
ses_page_07h_gold_file_ESMB = 'ses_page_07h_gold_file_ESMB'
ses_page_a_gold_file_1_ESMB = 'ses_page_a_gold_file_1_ESMB'
ses_page_a_gold_file_2_ESMB = 'ses_page_a_gold_file_2_ESMB'
ses_page_e_gold_file_ESMB = 'ses_page_e_gold_file_ESMB'

##############################CONSR-SEST-STRS-0001-0001#########################
MAXINDEX= '1'
##############################CONSR-SEST-STRS-0006-0001#########################
MAXLOOP = '1'
##############################Debug-Test########################################
#cmd_check_disk_num = "sg_scan -ai|grep sg|wc -l"
cmd_check_disk_num = "lsscsi -g |grep sg|wc -l"
rsp_check_disk_num = '90' #sg_scan -ai|grep sg|wc -l==> 96 - not_test_hdd - 2
rsp_check_disk_num_titan_g2_wb = '59'
rsp_check_disk_os_num = '90' #ls /sys/block/|grep sd|wc -l => rsp_check_disk_slot_os_num x 2
rsp_check_disk_slot_os_num= '90'#ls /sys/block/*/device |grep -i slot|wc -l 
remove_disk = ''
not_test_hdd = '6'
##############################CONSR-SEST-STRS-0026-0001#########################
cmd_reset_esm_ses_command = 'sg_senddiag -p -r 04,00,00,04,a0,00,00,03'
cmd_reset_esm_cli_command = 'reset 0'
##############################CONSR-SEST-SPCK-0062-0001#########################
phy_read_command = "sg_senddiag -p -r 14,00,01,11,44,00,01,01,00,01,01,01,00,02,01,01,00,03,01,01,00,04,01,01,00,05,01,01,00,06,01,01,00,07,01,01,00,08,01,01,00,09,01,01,00,0a,01,01,00,0b,01,01,00,0c,01,01,00,0d,01,01,00,0e,01,01,00,0f,01,01,00,10,01,01,00,11,01,01,00,12,01,01,00,13,01,01,00,14,01,01,00,15,01,01,00,16,01,01,00,17,01,01,00,18,01,01,00,19,01,01,00,1a,01,01,00,1b,01,01,00,1c,01,01,00,1d,01,01,00,1e,01,01,00,1f,01,01,00,20,01,01,00,21,01,01,00,22,01,01,00,23,01,01,00,24,01,01,00,25,01,01,00,26,01,01,00,27,01,01,00,28,01,01,00,29,01,01,00,2a,01,01,00,2b,01,01,00,2c,01,01,00,2d,01,01,00,2e,01,01,00,2f,01,01,00,30,01,01,00,31,01,01,00,32,01,01,00,33,01,01,00,34,01,01,00,35,01,01,00,36,01,01,00,37,01,01,00,38,01,01,00,39,01,01,00,3a,01,01,00,3b,01,01,00,3c,01,01,00,3d,01,01,00,3e,01,01,00,3f,01,01,00,40,01,01,00,41,01,01,00,42,01,01,00,43,01,01,00"
phy_get_command = "sg_ses -p 0x14"
phy_check_pattern = {
"line1":"00     14 00 05 d9 44 00 01 00  00 ff 00 00 00 00 00 00",
"line2":"10     00 00 00 00 00 00 00 00  00 00 00 01 01 00 00 ff",
"line3":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line4":"30     00 02 01 00 00 ff 00 00  00 00 00 00 00 00 00 00",
"line5":"40     00 00 00 00 00 00 00 03  01 00 00 ff 00 00 00 00",
"line6":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 04 01 00",
"line7":"60     00 ff 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"70     00 00 00 05 01 00 00 ff  00 00 00 00 00 00 00 00",
"line9":"80     00 00 00 00 00 00 00 00  00 06 01 00 00 ff 00 00",
"line10":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 07",
"line11":"a0     01 00 00 ff 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"b0     00 00 00 00 00 08 01 00  00 ff 00 00 00 00 00 00",
"line13":"c0     00 00 00 00 00 00 00 00  00 00 00 09 01 00 00 ff",
"line14":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"e0     00 0a 01 00 01 03 00 00  00 00 00 00 00 00 00 00",
"line16":"f0     00 00 00 00 00 00 00 0b  01 00 01 03 00 00 00 00",
"line17":"100    00 00 00 00 00 00 00 00  00 00 00 00 00 0c 01 00",
"line18":"110    01 03 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line19":"120    00 00 00 0d 01 00 01 03  00 00 00 00 00 00 00 00",
"line20":"130    00 00 00 00 00 00 00 00  00 0e 01 00 01 03 00 00",
"line21":"140    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 0f",
"line22":"150    01 00 01 03 00 00 00 00  00 00 00 00 00 00 00 00",
"line23":"160    00 00 00 00 00 10 01 00  01 03 00 00 00 00 00 00",
"line24":"170    00 00 00 00 00 00 00 00  00 00 00 11 01 00 01 03",
"line25":"180    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line26":"190    00 12 01 00 01 03 00 00  00 00 00 00 00 00 00 00",
"line27":"1a0    00 00 00 00 00 00 00 13  01 00 01 03 00 00 00 00",
"line28":"1b0    a2 00 00 00 a4 00 00 00  03 00 00 00 00 14 01 00",
"line29":"1c0    01 03 00 00 00 00 7d 00  00 00 7e 00 00 00 04 00",
"line30":"1d0    00 00 00 15 01 00 01 03  00 00 00 09 1b 00 00 08",
"line31":"1e0    fc 00 00 00 03 00 00 00  00 16 01 00 01 03 00 00",
"line32":"1f0    00 00 02 00 00 00 02 00  00 00 00 00 00 00 00 17",
"line33":"200    01 00 01 03 00 00 00 00  96 00 00 00 97 00 00 00",
"line34":"210    04 00 00 00 00 18 01 00  01 03 00 00 00 00 63 00",
"line35":"220    00 00 65 00 00 00 04 00  00 00 01 19 01 00 01 03",
"line36":"230    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line37":"240    01 1a 01 00 01 03 00 00  00 00 26 00 00 00 27 00",
"line38":"250    00 00 01 00 00 00 01 1b  01 00 01 03 00 00 00 00",
"line39":"260    7d 00 00 00 80 00 00 00  04 00 00 00 01 1c 01 00",
"line40":"270    01 03 00 00 00 f2 91 00  00 f2 92 00 00 00 02 00",
"line41":"280    00 00 01 1d 01 00 01 03  00 00 00 01 b3 00 00 01",
"line42":"290    b7 00 00 00 04 00 00 00  01 1e 01 00 01 03 00 00",
"line43":"2a0    00 00 a5 00 00 00 aa 00  00 00 05 00 00 00 01 1f",
"line44":"2b0    01 00 01 03 00 00 00 00  79 00 00 00 78 00 00 00",
"line45":"2c0    02 00 00 00 00 20 01 00  01 03 00 00 00 00 66 00",
"line46":"2d0    00 00 63 00 00 00 02 00  00 00 00 21 01 00 01 03",
"line47":"2e0    00 00 00 01 b9 00 00 01  b1 00 00 00 06 00 00 00",
"line48":"2f0    00 22 01 00 01 03 00 00  00 00 72 00 00 00 75 00",
"line49":"300    00 00 04 00 00 00 01 23  01 00 00 ff 00 00 00 00",
"line50":"310    00 00 00 00 00 00 00 00  00 00 00 00 00 24 01 00",
"line51":"320    00 ff 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line52":"330    00 00 00 25 01 00 00 ff  00 00 00 00 00 00 00 00",
"line53":"340    00 00 00 00 00 00 00 00  00 26 01 00 00 ff 00 00",
"line54":"350    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 27",
"line55":"360    01 00 00 ff 00 00 00 00  00 00 00 00 00 00 00 00",
"line56":"370    00 00 00 00 00 28 01 00  00 ff 00 00 00 00 00 00",
"line57":"380    00 00 00 00 00 00 00 00  00 00 00 29 01 00 00 ff",
"line58":"390    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line59":"3a0    00 2a 01 00 00 ff 00 00  00 00 00 00 00 00 00 00",
"line60":"3b0    00 00 00 00 00 00 00 2b  01 00 00 ff 00 00 00 00",
"line61":"3c0    00 00 00 00 00 00 00 00  00 00 00 00 00 2c 01 00",
"line62":"3d0    00 ff 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line63":"3e0    00 00 00 2d 01 00 00 ff  00 00 00 00 00 00 00 00",
"line64":"3f0    00 00 00 00 00 00 00 00  00 2e 01 00 00 ff 00 00",
"line65":"400    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 2f",
"line66":"410    01 00 00 ff 00 00 00 00  00 00 00 00 00 00 00 00",
"line67":"420    00 00 00 00 00 30 01 00  00 ff 00 00 00 00 00 00",
"line68":"430    00 00 00 00 00 00 00 00  00 00 00 31 01 00 00 ff",
"line69":"440    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line70":"450    00 32 01 00 00 ff 00 00  00 00 00 00 00 00 00 00",
"line71":"460    00 00 00 00 00 00 00 33  01 00 01 03 00 00 00 00",
"line72":"470    00 00 00 00 00 00 00 00  00 00 00 00 00 34 01 00",
"line73":"480    01 03 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line74":"490    00 00 00 35 01 00 01 03  00 00 00 00 00 00 00 00",
"line75":"4a0    00 00 00 00 00 00 00 00  00 36 01 00 01 03 00 00",
"line76":"4b0    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 37",
"line77":"4c0    01 00 01 03 00 00 00 00  00 00 00 00 00 00 00 00",
"line78":"4d0    00 00 00 00 00 38 01 00  01 03 00 00 00 00 00 00",
"line79":"4e0    00 00 00 00 00 00 00 00  00 00 00 39 01 00 01 03",
"line80":"4f0    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line81":"500    00 3a 01 00 01 03 00 00  00 00 00 00 00 00 00 00",
"line82":"510    00 00 00 00 00 00 00 3b  01 00 01 03 00 00 00 00",
"line83":"520    00 00 00 00 00 00 00 00  00 00 00 00 00 3c 01 00",
"line84":"530    01 03 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line85":"540    00 00 00 3d 01 00 01 03  00 00 00 00 00 00 00 00",
"line86":"550    00 00 00 00 00 00 00 00  00 3e 01 00 01 03 00 00",
"line87":"560    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 3f",
"line88":"570    01 00 01 03 00 00 00 00  00 00 00 00 00 00 00 00",
"line89":"580    00 00 00 00 00 40 01 00  01 03 00 00 00 00 00 00",
"line90":"590    00 00 00 00 00 00 00 00  00 00 00 41 01 00 01 03",
"line91":"5a0    00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line92":"5b0    00 42 01 00 01 03 00 00  00 00 00 00 00 00 00 00",
"line93":"5c0    00 00 00 00 00 00 00 43  01 00 01 03 00 00 00 00",
"line94":"5d0    00 00 00 00 00 00 00 00  00 00 00 00 00",
}
##############################CONSR-SEST-SPCK-0064-0001#########################
enable_phy_command = "sg_senddiag -p -r 14,00,01,11,44,00,01,00,01,01,01,00,01,02,01,00,01,03,01,00,01,04,01,00,01,05,01,00,01,06,01,00,01,07,01,00,01,08,01,00,01,09,01,00,01,0a,01,00,01,0b,01,00,01,0c,01,00,01,0d,01,00,01,0e,01,00,01,0f,01,00,01,10,01,00,01,11,01,00,01,12,01,00,01,13,01,00,01,14,01,00,01,15,01,00,01,16,01,00,01,17,01,00,01,18,01,00,01,19,01,00,01,1a,01,00,01,1b,01,00,01,1c,01,00,01,1d,01,00,01,1e,01,00,01,1f,01,00,01,20,01,00,01,21,01,00,01,22,01,00,01,23,01,00,01,24,01,00,01,25,01,00,01,26,01,00,01,27,01,00,01,28,01,00,01,29,01,00,01,2a,01,00,01,2b,01,00,01,2c,01,00,01,2d,01,00,01,2e,01,00,01,2f,01,00,01,30,01,00,01,31,01,00,01,32,01,00,01,33,01,00,01,34,01,00,01,35,01,00,01,36,01,00,01,37,01,00,01,38,01,00,01,39,01,00,01,3a,01,00,01,3b,01,00,01,3c,01,00,01,3d,01,00,01,3e,01,00,01,3f,01,00,01,40,01,00,01,41,01,00,01,42,01,00,01,43,01,00,01"
phy_enable_check_pattern = {
         "line1":"00     14 00 00 cd 44 00 00 01  01 00 01 02 00 01 03 00",
         "line2":"10     01 04 00 01 05 00 01 06  00 01 07 00 01 08 00 01",
         "line3":"20     09 00 01 0a 00 01 0b 00  01 0c 00 01 0d 00 01 0e",
         "line4":"30     00 01 0f 00 01 10 00 01  11 00 01 12 00 01 13 00",
         "line5":"40     01 14 00 01 15 00 01 16  00 01 17 00 01 18 00 01",
         "line6":"50     19 00 01 1a 00 01 1b 00  01 1c 00 01 1d 00 01 1e",
         "line7":"60     00 01 1f 00 01 20 00 01  21 00 01 22 00 01 23 00",
         "line8":"70     01 24 00 01 25 00 01 26  00 01 27 00 01 28 00 01",
         "line9":"80     29 00 01 2a 00 01 2b 00  01 2c 00 01 2d 00 01 2e",
         "line10":"90     00 01 2f 00 01 30 00 01  31 00 01 32 00 01 33 00",
         "line11":"a0     01 34 00 01 35 00 01 36  00 01 37 00 01 38 00 01",
         "line12":"b0     39 00 01 3a 00 01 3b 00  01 3c 00 01 3d 00 01 3e",
         "line13":"c0     00 01 3f 00 01 40 00 01  41 00 01 42 00 01 43 00",
         "line14":"d0     01",
         }
mode_sense_page3Fh_00_cmd =  "sg_modes --page=0x3f,0x00 --maxlen=0x8000"
mode_sense_page3Fh_ff_cmd =  "sg_modes --page=0x3f,0xff --maxlen=0x8000"
mode_sense_page3Fh_00_pattern = {
"line1" : "CELESTIC.*?\d+",
"line2" : "Mode parameter header from MODE SENSE\(10\)",
"line3" : "Mode data length=60, medium type=0x00, specific param=0x00, longlba=0",
"line4" : "Block descriptor length=0",
"line5" : "Disconnect-Reconnect, page_control: current",
"line6" : " 00     02 0e 00 00 00 00 00 00  27 10 00 11 00 00 00 00",
"line7" : "Control, page_control: current",
"line8" : " 00     0a 0a 00 00 00 00 00 00  00 00 00 00",
"line9" : "Protocol specific logical unit \(SAS\), page_control: current",
"line10" : " 00     18 06 06 00 00 00 00 00",
"line11" : "Protocol specific port \(SAS\), page_control: current",
"line12" : " 00     19 0e 46 00 07 d0 1f 40  00 64 00 00 00 00 00 00",
}
mode_sense_page3Fh_00_pattern_titan_g2_wb = {
"line1" : "CELESTIC.*?\d+",
"line2" : "Mode parameter header from MODE SENSE\(10\)",
"line3" : "Mode data length=32, medium type=0x00, specific param=0x00, longlba=0",
"line4" : "Block descriptor length=0",
"line5" : "Protocol specific logical unit \(SAS\), page_control: current",
"line6" : " 00     18 06 06 00 00 00 00 00",
"line7" : "Protocol specific port \(SAS\), page_control: current",
"line8" : " 00     19 0e 66 00 07 d0 75 30  00 0a 00 00 00 00 00 00",
}
mode_sense_page3Fh_ff_pattern = {
"line1" : "CELESTIC.*?\d+",
"line2" : "Mode parameter header from MODE SENSE\(10\)",
"line3" : "Mode data length=60, medium type=0x00, specific param=0x00, longlba=0",
"line4" : "Block descriptor length=0",
"line5" : "Disconnect-Reconnect, page_control: current",
"line6" : " 00     02 0e 00 00 00 00 00 00  27 10 00 11 00 00 00 00",
"line7" : "Control, page_control: current",
"line8" : " 00     0a 0a 00 00 00 00 00 00  00 00 00 00",
"line9" : "Protocol specific logical unit \(SAS\), page_control: current",
"line10" : " 00     18 06 06 00 00 00 00 00",
"line11" : "Protocol specific port \(SAS\), page_control: current",
"line12" : " 00     19 0e 46 00 07 d0 1f 40  00 64 00 00 00 00 00 00",
}
mode_sense_page3Fh_ff_pattern_titan_g2_wb = {
"line1" : "CELESTIC.*?\d+",
"line2" : "Mode parameter header from MODE SENSE\(10\)",
"line3" : "Mode data length=3516, medium type=0x00, specific param=0x00, longlba=0",
"line4" : "Block descriptor length=0",
"line9" : "Protocol specific logical unit \(SAS\), page_control: current",
"line10" : " 00     18 06 06 00 00 00 00 00",
"line11" : "Protocol specific port \(SAS\), page_control: current",
"line12" : " 00     19 0e 66 00 07 d0 75 30  00 0a 00 00 00 00 00 00",
"line13" : "Phy control and discover \(SAS\), page_control: current",
"line14" : "Enhanced phy control \(SAS\), page_control: current"
}

##############################CONSR-SEST-SPCK-0063-0001#########################
phy_disable_check_pattern = {
"line1":"00     14 00 00 cd 44 00 00 01  01 00 01 02 00 01 03 00",
"line2":"10     01 04 00 01 05 00 01 06  00 01 07 00 01 08 00 01",
"line3":"20     09 00 01 0a 00 01 0b 00  01 0c 00 01 0d 00 01 0e",
"line4":"30     00 01 0f 00 01 10 00 01  11 00 01 12 00 01 13 00",
"line5":"40     01 14 00 01 15 00 01 16  00 01 17 00 01 18 00 01",
"line6":"50     19 00 01 1a 00 01 1b 00  01 1c 00 01 1d 00 01 1e",
"line7":"60     00 01 1f 00 01 20 00 01  21 00 01 22 00 01 23 00",
"line8":"70     01 24 00 01 25 00 01 26  00 01 27 00 01 28 00 01",
"line9":"80     29 00 01 2a 00 01 2b 00  01 2c 00 01 2d 00 01 2e",
"line10":"90     00 01 2f 00 01 30 00 01  31 00 01 32 00 01 33 00",
"line11":"a0     01 34 00 01 35 00 01 36  00 01 37 00 01 38 00 01",
"line12":"b0     39 00 01 3a 00 01 3b 00  01 3c 00 01 3d 00 00 3e",
"line13":"c0     00 00 3f 00 00 40 00 00  41 00 00 42 00 00 43 00",
"line14":"d0     00",
}
disable_phy_command = "sg_senddiag -p -r 14,00,01,11,44,00,01,00,01,01,01,00,01,02,01,00,01,03,01,00,01,04,01,00,01,05,01,00,01,06,01,00,01,07,01,00,01,08,01,00,01,09,01,00,01,0a,01,00,01,0b,01,00,01,0c,01,00,01,0d,01,00,01,0e,01,00,01,0f,01,00,01,10,01,00,01,11,01,00,01,12,01,00,01,13,01,00,01,14,01,00,01,15,01,00,01,16,01,00,01,17,01,00,01,18,01,00,01,19,01,00,01,1a,01,00,01,1b,01,00,01,1c,01,00,01,1d,01,00,01,1e,01,00,01,1f,01,00,01,20,01,00,01,21,01,00,01,22,01,00,01,23,01,00,01,24,01,00,01,25,01,00,01,26,01,00,01,27,01,00,01,28,01,00,01,29,01,00,01,2a,01,00,01,2b,01,00,01,2c,01,00,01,2d,01,00,01,2e,01,00,01,2f,01,00,01,30,01,00,01,31,01,00,01,32,01,00,01,33,01,00,01,34,01,00,01,35,01,00,01,36,01,00,01,37,01,00,01,38,01,00,01,39,01,00,01,3a,01,00,01,3b,01,00,01,3c,01,00,01,3d,01,00,00,3e,01,00,00,3f,01,00,00,40,01,00,00,41,01,00,00,42,01,00,00,43,01,00,00"
mode_sense_page18_cmd = "sg_modes --page=0x18 --maxlen=0xf0"
mode_sense_page19_cmd = "sg_modes --page=0x19 --maxlen=0xf0"
mode_sense_page18_pattern = {
"line1": "CELESTIC.*?\d+",
"line2": "Mode parameter header from MODE SENSE\(10\)",
"line3":"Mode data length=16, medium type=0x00, specific param=0x00, longlba=0",
"line4":"Block descriptor length=0",
"line5":"Protocol specific logical unit \(SAS\), page_control: current",
"line6":"00     18 06 06 00 00 00 00 00",
}
mode_sense_page19_pattern={
"line1":"CELESTIC.*?\d+",
"line2":"Mode parameter header from MODE SENSE\(10\):",
"line3":"Mode data length=24, medium type=0x00, specific param=0x00, longlba=0",
"line4":"Block descriptor length=0",
"line5":"Protocol specific port \(SAS\), page_control: current",
"line6":" 00     19 0e 46 00 07 d0 1f 40  00 64 00 00 00 00 00 00",
}
mode_sense_page19_pattern_titan_g2_wb={
"line1":"CELESTIC.*?\d+",
"line2":"Mode parameter header from MODE SENSE\(10\):",
"line3":"Mode data length=24, medium type=0x00, specific param=0x00, longlba=0",
"line4":"Block descriptor length=0",
"line5":"Protocol specific port \(SAS\), page_control: current",
"line6":" 00     19 0e 66 00 07 d0 75 30  00 0a 00 00 00 00 00 00",
}
control_descriptor_cmd="sg_senddiag -p -r 15,00,00,02,00,00"
page_15_status_cmd="sg_ses -p 0x15"
page_15_status_pattern={
        "line1":"CELESTIC.*?\d+",
        "line2":"Cannot decode response from diagnostic page: dpage 0x15",
        "line3":" 00     15 00 00 0b 00 02 06 03  05 04 16 12 10 13 04",
}
page_15_status_pattern={
        "line1":"CELESTIC.*?\d+",
        "line2":"Cannot decode response from diagnostic page: dpage 0x15",
        "line3":" 00     15 00 00 0b 00 02 06 03  05 04 12 12 10 13 04",
}

ses_page_tool_cmd="./ses_page_tool -p 0x15 -d"
elem_id_0 ='0'
psu_trigger_on_value = '2'
psu_trigger_off_value = '3'
psu_trigger_on_pattern_0 = {
"line1":"2",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 C0 08 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

psu_trigger_on_pattern_0_titan_g2_wb = {
"line1":"2",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 221 bytes data, len = 221 :",
"line5":"15 00 00 D9 01 00 00 00 00 C0 08 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_psu_trigger_on_pattern_0 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 d9 03 20 00 00  00 20 08 00 00 00 00 00",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

page_15_psu_trigger_on_pattern_0_titan_g2_wb = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 d9 03 20 00 00  00 20 08 00 00 00 00 00",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

psu_trigger_off_pattern_0 = {
"line1":"3",        
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 80 08 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

psu_trigger_off_pattern_0_titan_g2_wb = {
"line1":"3",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 221 bytes data, len = 221 :",
"line5":"15 00 00 D9 01 00 00 00 00 80 08 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}



page_15_psu_trigger_off_pattern_0 ={
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

page_15_psu_trigger_off_pattern_0_titan_g2_wb ={
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 d9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}



elem_id_1 ='1'
psu_trigger_on_pattern_1 = {
"line1":"2",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 C0 08 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_psu_trigger_on_pattern_1 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 20 00 00  00 00 00 00 00 20 08 00",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

psu_trigger_off_pattern_1 = {
"line1":"3",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 80 08 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
elem_id_2 ='2'
psu_trigger_on_pattern_2 = {
"line1":"2",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 C0 08 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_psu_trigger_on_pattern_2 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 20 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 20 08 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
psu_trigger_off_pattern_2 = {
"line1":"3",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 80 08 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

elem_id_3 ='3'
psu_trigger_on_pattern_3 = {
"line1":"2",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 C0 08 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_psu_trigger_on_pattern_3 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 20 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 20 08 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
psu_trigger_off_pattern_3 = {
"line1":"3",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 80 08 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
elem_id_4 ='4'
psu_trigger_on_pattern_4 = {
"line1":"2",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 C0 08 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_psu_trigger_on_pattern_4 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 20 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 20 08 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
psu_trigger_off_pattern_4 = {
"line1":"3",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 80 08 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
elem_id_5 ='5'
psu_trigger_on_pattern_5 = {
"line1":"2",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 C0 08 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_psu_trigger_on_pattern_5 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 20 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 20 08 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
psu_trigger_off_pattern_5 = {
"line1":"3",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 80 08 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}



##################################CONSR-SEST-SPCK-0067-0001#####################
cooling_trigger_on_value = '4'
cooling_trigger_off_value = '5'
cooling_trigger_on_pattern_0 = {
"line1":"4",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",   
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line7":"00 00 00 00 00 C0 80 00 00 00 00 00 00 00 00 00",   
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",            
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_cooling_trigger_on_pattern_0 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",    
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line5":"20     00 20 00 00 00 20 80 00  00 00 00 00 00 00 00 00",      
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
cooling_trigger_off_pattern_0 = {
"line1":"5",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",   
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line7":"00 00 00 00 00 80 80 00 00 00 00 00 00 00 00 00",   
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",            
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_cooling_trigger_off_pattern_0 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",    
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",   
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

page_15_cooling_trigger_off_pattern_2_titan_g2_wb = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 d9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

cooling_trigger_on_pattern_1 = {
"line1":"4",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",   
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line7":"00 00 00 00 00 00 00 00 00 C0 80 00 00 00 00 00",   
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",            
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_cooling_trigger_on_pattern_1 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",    
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line5":"20     00 20 00 00 00 00 00 00  00 20 80 00 00 00 00 00",      
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
cooling_trigger_off_pattern_1 = {
"line1":"5",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",   
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line7":"00 00 00 00 00 00 00 00 00 80 80 00 00 00 00 00",   
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",            
"line20":"Page \(17h\): error injection contrl Done",
}
cooling_trigger_on_pattern_2 = {
"line1":"4",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",   
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 C0 80 00",   
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",            
"line20":"Page \(17h\): error injection contrl Done",
}

cooling_trigger_on_pattern_2_titan_g2_wb = {
"line1":"4",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 221 bytes data, len = 221 :",
"line5":"15 00 00 D9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 C0 80 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_cooling_trigger_on_pattern_2 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 d9 03 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 20 00 00 00 00 00 00  00 00 00 00 00 20 80 00",
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

page_15_cooling_trigger_on_pattern_2_titan_g2_wb = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 d9 03 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 20 00 00 00 00 00 00  00 00 00 00 00 20 80 00",
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

cooling_trigger_off_pattern_2 = {
"line1":"5",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 80 80 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
cooling_trigger_off_pattern_2_titan_g2_wb = {
"line1":"5",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 221 bytes data, len = 221 :",
"line5":"15 00 00 D9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 80 80 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

cooling_trigger_on_pattern_3 = {
"line1":"4",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 C0 80 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_cooling_trigger_on_pattern_3 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",    
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line5":"20     00 20 00 00 00 00 00 00  00 00 00 00 00 00 00 00",     
"line6":"30     00 20 80 00 00 00 00 00  00 00 00 00 00 00 00 00",     
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
cooling_trigger_off_pattern_3 = {
"line1":"5",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",   
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line8":"00 80 80 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",            
"line20":"Page \(17h\): error injection contrl Done",
}
cooling_trigger_on_pattern_4 = {
"line1":"4",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",   
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line8":"00 00 00 00 00 C0 80 00 00 00 00 00 00 00 00 00",   
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",            
"line20":"Page \(17h\): error injection contrl Done", 
}
page_15_cooling_trigger_on_pattern_4 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",    
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line5":"20     00 20 00 00 00 00 00 00  00 00 00 00 00 00 00 00",     
"line6":"30     00 00 00 00 00 20 80 00  00 00 00 00 00 00 00 00",     
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00", 
}
cooling_trigger_off_pattern_4 = {
"line1":"5",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",   
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line8":"00 00 00 00 00 80 80 00 00 00 00 00 00 00 00 00",   
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",            
"line20":"Page \(17h\): error injection contrl Done",
}
voltage_trigger_on_value = '8'
voltage_trigger_off_value = '9'


voltage_trigger_on_pattern_0 = {
"line1":"8",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 C0 80 00 00 00 00 00 ",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}



page_15_voltage_trigger_on_pattern_0 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 20 00 00  00 20 80 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
voltage_trigger_off_pattern_0 = {
"line1":"9",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 80 80 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_voltage_trigger_off_pattern_0 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
voltage_trigger_on_pattern_1 = {
"line1":"8",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 C0 80 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}



page_15_voltage_trigger_on_pattern_1 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 20 00 00  00 00 00 00 00 20 80 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
voltage_trigger_off_pattern_1= {
"line1":"9",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 80 80 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
voltage_trigger_on_pattern_2 = {
"line1":"8",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 C0 80 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_voltage_trigger_on_pattern_2 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 20 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 20 80 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
voltage_trigger_off_pattern_2= {
"line1":"9",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 80 80 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
voltage_trigger_on_pattern_3 = {
"line1":"8",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 C0 80 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_voltage_trigger_on_pattern_3 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 20 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 20 80 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
voltage_trigger_off_pattern_3= {
"line1":"9",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 80 80 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}


voltage_trigger_on_pattern_4 = {
"line1":"8",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 C0 80 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

voltage_trigger_on_pattern_4_titan_g2_wb = {
"line1":"8",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 221 bytes data, len = 221 :",
"line5":"15 00 00 D9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 C0 80 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_voltage_trigger_on_pattern_4 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 20 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 20 80 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

page_15_voltage_trigger_on_pattern_4_titan_g2_wb = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 d9 03 00 00 00  00 00 00 00 00 00 00 00",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 20 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 00 00 00  00 20 80 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

voltage_trigger_off_pattern_4= {
"line1":"9",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 80 80 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

voltage_trigger_off_pattern_4_titan_g2_wb= {
"line1":"9",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 221 bytes data, len = 221 :",
"line5":"15 00 00 D9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 80 80 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_voltage_trigger_off_pattern_4_titan_g2_wb = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 d9 02 00 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}

voltage_trigger_on_pattern_5 = {
"line1":"8",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 C0 80 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_voltage_trigger_on_pattern_5 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 20 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 20 80 00 ",
"line14":" b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
voltage_trigger_off_pattern_5= {
"line1":"9",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 80 80 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

voltage_trigger_on_pattern_6 = {
"line1":"8",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 C0 80 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_voltage_trigger_on_pattern_6 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 20 80 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
voltage_trigger_off_pattern_6= {
"line1":"9",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 80 80 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
elem_id_6='6'
elem_id_7='7'
elem_id_8='8'
elem_id_9='9'
voltage_trigger_on_pattern_7 = {
"line1":"8",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 C0 80 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_voltage_trigger_on_pattern_7 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":" 00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00 ",
"line4":" 10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line5":" 20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line6":" 30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line7":" 40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line8":" 50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line9":" 60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line10":" 70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line11":" 80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line12":" 90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line13":" a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line14":" b0     00 00 00 00 00 20 80 00  00 00 00 00 00 00 00 00 ",
"line15":" c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line16":" d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ",
"line17":" e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
voltage_trigger_off_pattern_7= {
"line1":"9",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00 ",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 80 80 00 00 00 00 00 00 00 00 00 ",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
}

#############################################CONSR-SEST-SPCK-0068-0001#########################################
temp_trigger_on_value = '6'
temp_trigger_off_value = '7'
temp_trigger_on_pattern_0 = {
"line1":"6",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",   
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 C0 80 00",   
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",   
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",            
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_temp_trigger_on_pattern_0 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",      
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",     
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",      
"line6":"30     00 00 00 00 00 00 00 00  00 20 00 00 00 20 80 00",      
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",      
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",    
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
temp_trigger_off_pattern_0 = {
"line1":"7",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 80 80 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_temp_trigger_off_pattern_0 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
page_15_temp_trigger_off_pattern_6_titan_g2_wb = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 d9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
temp_trigger_on_pattern_1 = {
"line1":"6",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 C0 80 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_temp_trigger_on_pattern_1 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 20 00 00 00 00 00 00",
"line7":"40     00 20 80 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
temp_trigger_off_pattern_1 = {
"line1":"7",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 80 80 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
temp_trigger_on_pattern_2 = {
"line1":"6",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 C0 80 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_temp_trigger_on_pattern_2 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 20 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 20 80 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
temp_trigger_off_pattern_2 = {
"line1":"7",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 80 80 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
temp_trigger_on_pattern_3 = {
"line1":"6",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 C0 80 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_temp_trigger_on_pattern_3 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 20 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 20 80 00 00 00 00 00",
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
temp_trigger_off_pattern_3 = {
"line1":"7",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 80 80 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
temp_trigger_on_pattern_4 = {
"line1":"6",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 C0 80 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_temp_trigger_on_pattern_4 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 20 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 20 80 00",
"line8":"50     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
temp_trigger_off_pattern_4 = {
"line1":"7",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 80 80 00",
"line10":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
temp_trigger_on_pattern_5 = {
"line1":"6",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 C0 80 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_temp_trigger_on_pattern_5 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 20 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 20 80 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
temp_trigger_off_pattern_5 = {
"line1":"7",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 80 80 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
temp_trigger_on_pattern_6 = {
"line1":"6",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 C0 80 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
temp_trigger_on_pattern_6_titan_g2_wb = {
"line1":"6",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 221 bytes data, len = 221 :",
"line5":"15 00 00 D9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 C0 80 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}

page_15_temp_trigger_on_pattern_6 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 d9 03 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 20 80 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
page_15_temp_trigger_on_pattern_6_titan_g2_wb = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 d9 03 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 20 80 00  00 00 00 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
temp_trigger_off_pattern_6 = {
"line1":"7",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 80 80 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
temp_trigger_off_pattern_6_titan_g2_wb = {
"line1":"7",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 221 bytes data, len = 221 :",
"line5":"15 00 00 D9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 80 80 00 00 00 00 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
temp_trigger_on_pattern_7 = {
"line1":"6",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 C0 80 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_15_temp_trigger_on_pattern_7 = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x15",
"line3":"00     15 00 00 e9 02 00 00 00  00 00 00 00 00 00 00 00",
"line4":"10     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line5":"20     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line6":"30     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line7":"40     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line8":"50     00 00 00 00 00 00 00 00  00 20 80 00 00 00 00 00",
"line9":"60     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line10":"70     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line11":"80     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line12":"90     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line13":"a0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line14":"b0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line15":"c0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line16":"d0     00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00",
"line17":"e0     00 00 00 00 00 00 00 00  00 00 00 00 00",
}
temp_trigger_off_pattern_7 = {
"line1":"7",
"line2":"page num: 21",
"line3":"ei_ele_type_mgr_ptr->ei_ele_type_no = 5",
"line4":"dump ctrl Page\[0x15\] 237 bytes data, len = 237 :",
"line5":"15 00 00 E9 01 00 00 00 00 00 00 00 00 00 00 00",
"line6":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line7":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line8":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line9":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line10":"00 00 00 00 00 00 00 00 00 80 80 00 00 00 00 00",
"line11":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line12":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line13":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line14":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line15":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line16":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line17":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line18":"00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
"line19":"00 00 00 00 00 00 00 00 00 00 00 00 00",
"line20":"Page \(17h\): error injection contrl Done",
}
page_13_status_cmd = "sg_ses -p 0x13 -H"
page_13_status_pattern = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x13",
"line3":"00     13 00 00 15 00 00 00 00[\s\da-f]",
}
###################################CONSR-SEST-SPCK-0060-0001#########################
page_13_entries_num_cmd = "sg_senddiag -p -r 13,00,00,06,02,00,00,01,ff,ff"

page_13_status_cmd = "sg_ses -p 0x13 -H"

page_13_clear_log_cmd = "sg_senddiag -p -r 13,00,00,03,01,00,03"
page_13_status_pattern = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x13",
"line3":"00     13 00 00 05 02 00 06 00  00",
}
log_entry_code="1"
clear_log_entry_code="2"
psu0_status_pg2_cmd="sg_ses --page=0x02 --index=ps,0"
psu034_status_pg2_pattern="status: OK"
psu1_status_pg2_cmd="sg_ses --page=0x02 --index=ps,1"
psu125_status_pg2_pattern="status: Not installed"
psu2_status_pg2_cmd="sg_ses --page=0x02 --index=ps,2"
psu3_status_pg2_cmd="sg_ses --page=0x02 --index=ps,3"
psu4_status_pg2_cmd="sg_ses --page=0x02 --index=ps,4"
psu5_status_pg2_cmd="sg_ses --page=0x02 --index=ps,5"
psu0_status_pg7_cmd="sg_ses --page=0x07 --index=ps,1"
psu1_status_pg7_cmd="sg_ses --page=0x07 --index=ps,1"
psu2_status_pg7_cmd="sg_ses --page=0x07 --index=ps,2"
psu3_status_pg7_cmd="sg_ses --page=0x07 --index=ps,3"
psu4_status_pg7_cmd="sg_ses --page=0x07 --index=ps,4"
psu5_status_pg7_cmd="sg_ses --page=0x07 --index=ps,5"
psu1_status_pg7_pattern = {
"line1":"CELESTIC.*?\d+",
"line2":"Element Descriptor In diagnostic page:",
"line3":"generation code: 0x0",
"line4":"element descriptor list \(grouped by type\):",
"line5":"Element 1 descriptor: PSU 2",
}
psu2_status_pg7_pattern = {
"line1":"CELESTIC.*?\d+",
"line2":"Element Descriptor In diagnostic page:",
"line3":"generation code: 0x0",
"line4":"element descriptor list \(grouped by type\):",
"line5":"Element 2 descriptor: PSU 3",
}
psu5_status_pg7_pattern = {
"line1":"CELESTIC.*?\d+",
"line2":"Element Descriptor In diagnostic page:",
"line3":"generation code: 0x0",
"line4":"element descriptor list \(grouped by type\):",
"line5":"Element 5 descriptor: REG 2",
}
psu0_cli_pattern =""".*--- PSU 1 ---.*
.*PS Type: DPS-1300AB-6 J.*
.*Power Capacity: 1300.*
.*PS Manufacturer: DELTA.*
.*PS Serial Number:.*\\S+.*
.*PS Part Number: DPS-1300AB-6 J.*
.*PS Firmware Version: 00.00.*
.*HW EC LEVEL:.*\\S+.*"""

psu0_cli_pattern_titan_g2_wb ="""--- Power Supply 0 ---.*
PS Type: DPS-1300AB-6 J.*
Power Capacity: 1300.*
PS Manufacturer: DELTA.*
PS Serial Number:.*\\S+.*
PS Part Number: DPS-1300AB-6 J.*
PS Firmware Version: 00.04.*
HW EC LEVEL:.*\\S+.*"""

psu1_cli_pattern_titan_g2_wb ="""--- Power Supply 1 ---.*
PS Type: DPS-1300AB-6 J.*
Power Capacity: 1300.*
PS Manufacturer: DELTA.*
PS Serial Number:.*\\S+.*
PS Part Number: DPS-1300AB-6 J.*
PS Firmware Version: 00.04.*
HW EC LEVEL:.*\\S+.*"""

psu2_cli_pattern_titan_g2_wb ="""--- Power Supply 2 ---.*
PS Type: DPS-1300AB-6 J.*
Power Capacity: 1300.*
PS Manufacturer: DELTA.*
PS Serial Number:.*\\S+.*
PS Part Number: DPS-1300AB-6 J.*
PS Firmware Version: 00.04.*
HW EC LEVEL:.*\\S+.*"""

psu3_cli_pattern_titan_g2_wb ="""--- Power Supply 3 ---.*
PS Type: DPS-1300AB-6 J.*
Power Capacity: 1300.*
PS Manufacturer: DELTA.*
PS Serial Number:.*\\S+.*
PS Firmware Version: 00.04.*
HW EC LEVEL:.*\\S+.*"""

psu1_cli_pattern =""".*--- PSU 2 ---.*
.*NotInstalled.*"""
psu2_cli_pattern=""".*--- PSU 3 ---.*
.*NotInstalled.*"""
psu3_cli_pattern=""".*--- PSU 4 ---.*
.*PS Type: DPS-1300AB-6 J.*
.*Power Capacity: 1300.*
.*PS Manufacturer: DELTA.*
.*PS Serial Number:.*[a-zA-Z0-9_.-]*.*
.*PS Part Number: DPS-1300AB-6 J.*
.*PS Firmware Version: 00.00.*
.*HW EC LEVEL:.*[a-zA-Z0-9_.-]*.*"""
psu4_cli_pattern =""".*--- REG 1 ---.*
.*PS Type: DC-DC BOARD.*
.*Power Capacity: 120A.*
.*PS Manufacturer: CELESTICA-CTH.*
.*PS Serial Number:.*[a-zA-Z0-9_.-]*.*
.*PS Part Number: R1066-F1014-02.*
.*PS Firmware Version: N\/A.*
.*HW EC LEVEL:.*[a-zA-Z0-9_.-]*.*"""

psu5_cli_pattern=""".*--- REG 2 ---.*
.*NotInstalled.*"""

psu0_Find_pattern =""".*--- PSU 1 ---.*
.*PS Type: DPS-1300AB-6 J.*
.*Power Capacity: 1300.*
.*PS Manufacturer: DELTA.*
.*PS Serial Number: {1}.*
.*PS Part Number: {0}.*
.*PS Firmware Version: 00.00.*
.*HW EC LEVEL: {2}.*"""




psu0_cli_pattern_Athena =""".*--- Power Supply 0 ---.*
.*PS Type: {0}.*
.*PS Manufacturer: DELTA.*
.*PS Serial Number: {1}.*
.*PS Part Number: {2}.*
.*PS Hardware Version: {3}.*
.*PS Firmware Version: {4}.*"""


psu1_cli_pattern_Athena =""".*--- Power Supply 1 ---.*
.*PS Type: {0}.*
.*PS Manufacturer: DELTA.*
.*PS Serial Number: {1}.*
.*PS Part Number: {2}.*
.*PS Hardware Version: {3}.*
.*PS Firmware Version: {4}.*"""


psu1_Find_pattern_titan_g2_wb =""".*--- Power Supply 1 ---.*
.*PS Type: DPS-1300AB-6 J.*
.*Power Capacity: 1300.*
.*PS Manufacturer: DELTA.*
.*PS Serial Number: {1}.*
.*PS Part Number: {0}.*
.*PS Firmware Version: 00.04.*
.*HW EC LEVEL: {2}.*"""

psu2_Find_pattern_titan_g2_wb =""".*--- Power Supply 2 ---.*
.*PS Type: DPS-1300AB-6 J.*
.*Power Capacity: 1300.*
.*PS Manufacturer: DELTA.*
.*PS Serial Number: {1}.*
.*PS Part Number: {0}.*
.*PS Firmware Version: 00.04.*
.*HW EC LEVEL: {2}.*"""

psu3_Find_pattern_titan_g2_wb =""".*--- Power Supply 3 ---.*
.*PS Type: DPS-1300AB-6 J.*
.*Power Capacity: 1300.*
.*PS Manufacturer: DELTA.*"""

PSU1="1"
PSU2="2"
PSU3="3"
PSU4="4"
psu3_Find_pattern =""".*--- PSU 4 ---.*
.*PS Type: DPS-1300AB-6 J.*
.*Power Capacity: 1300.*
.*PS Manufacturer: DELTA.*
.*PS Serial Number: {1}.*
.*PS Part Number: {0}.*
.*PS Firmware Version: 00.00.*
.*HW EC LEVEL: {2}.*"""
psu4_Find_pattern=""".*--- REG 1 ---.*
.*PS Type: DC-DC BOARD.*
.*Power Capacity: 120A.*
.*PS Manufacturer: CELESTICA-CTH.*
.*PS Serial Number: {1}.*
.*PS Part Number: {0}.*
.*PS Firmware Version: N/A.*
.*HW EC LEVEL: {2}.*"""


Page13_run_diag_command="sg_senddiag -p -r 04,00,00,04,a0,00,00,00"
page_13_new_log_check_cmd="sg_senddiag -p -r 13,00,00,03,01,00,00"
page_13_read_status_cmd="sg_senddiag -p -r 13,00,00,03,01,00,01"
page_13_unread_status_cmd="sg_senddiag -p -r 13,00,00,03,01,00,02"
log_read_code="3"
log_unread_code="4"
page_13_read_status_pattern="00     13 00 00 05 02 00 02 00  00"
page_13_unread_status_pattern="00     13 00 00 05 02 00 04 00  00"
clear_log_entry_pattern="00     13 00 00 05 02 00 06 00  00"
page_13_new_log_check_cmd="sg_senddiag -p -r 13,00,00,03,01,00,00"
page_13_read_status_cmd="sg_senddiag -p -r 13,00,00,03,01,00,01"
page_13_unread_status_cmd="sg_senddiag -p -r 13,00,00,03,01,00,02"
log_read_code="3"
log_unread_code="4"
page_13_read_status_pattern="00     13 00 00 05 02 00 02 00  00"
page_13_unread_status_pattern="00     13 00 00 05 02 00 04 00  00"
clear_log_entry_pattern="00     13 00 00 05 02 00 06 00  00"
page_13_clear_log_cmd="sg_senddiag -p -r 13,00,00,03,01,00,03"

page_0a_command="sg_ses --page=0x0a --index="

dev1_index1_30="0-29"
dev1_index31_60="30-59"
dev1_index61_67="60-66"
dev1_index68_90="67-89"
dev2_index1_30="0-29"
dev2_index31_60="30-59"
dev2_index61_67="60-66"
dev2_index68_75="67-74"
dev2_index76_90="75-89"

sample_invalid_list_titan_g2_wb = "0-29"
sample_valid_list_titan_g2_wb = "75-89"

page_drvstatus_cmd="sg_ses --page=0x02 --index="
drv0_29="0-29"
drv30_59="30-59"
drv75_82="75-82"
drv83_89="83-89"
drv60_66="60-66"
drv67_74="67-74"
OK_status={
        "line1":"status: Unsupported",
        "line2":"status: Not installed"
        }

OK_status_titan_g2_wb={
        "line1":"status: Unsupported",
        }


unsupported_status={
        "line1":"status: OK",
        "line2":"status:Not installed"
        }

Notinstalled_status={
        "line1":"status: OK",
        "line2":"status: Unsupported"
        }
page7_slotname_check_cmd="sg_ses --page=0x07 --index=0-89"
fan_min_speed_l75cli="41%"
fan_min_speed_g75cli="38%"
fan_max_speed_g75cli="54%"
fan_max_speed_l75cli="51%"
fan_min_speed_athena="55%"
fan_max_speed_athena="100"
fan_speed_10="10"
fan_speed_11="11"
fan_speed_12="12"
fan_speed_13="13"
fan_speed_14="14"
fan_speed_8="8"
fan_speed_10_cli_athena="55"
fan_speed_11_cli_athena="60"
fan_speed_12_cli_athena="70"
fan_speed_13_cli_athena="80"
fan_speed_14_cli_athena="90"
fan_speed_10_l75cli="36%"
fan_speed_10_g75cli="41%"
fan_speed_11_l75cli="37%"
fan_speed_11_g75cli="43%"
fan_speed_12_l75cli="40%"
fan_speed_12_g75cli="45%"
fan_speed_13_l75cli="42%"
fan_speed_13_g75cli="47%"
fan_speed_14_l75cli="46%"
fan_speed_14_g75cli="50%"
page13_readlog_cmd="sg_senddiag -p -r 13,00,00,02,00,00"
pg10_diag_cmd="sg_senddiag -p -r 10,00,00,09,00,00,6c,6F,67,20,67,65,74"
pg10_status_cmd="sg_ses -p 0x10"
pg_Fail_pattern="sg_ses failed: Illegal request"
pg17_diag_cmd="sg_senddiag -p -r 17,00,00,0B,00,00,00,00,6c,6F,67,20,67,65,74"
pg17_diag_sec1_cmd="sg_senddiag -p -r 17,00,00,0B,00,00,00,01,6c,6F,67,20,67,65,74"
pg17_diag_sec2_cmd="sg_senddiag -p -r 17,00,00,0B,00,00,00,02,6c,6F,67,20,67,65,74"
pg17_status_cmd="sg_ses -p 0x17"
expdr_sec_1="$%^0"
expdr_sec_2="$%^2"
expdr_pri="$%^1"


ses_diag_17cmd="sg_senddiag -p -r 10,00,00,09,00,00,6c,6F,67,20,67,65,74"
ses_17page_cmd ="sg_ses -p 0x17"
pattern="Invalid response, wanted page code: 0x17 but got 0x10"

ses_diag_10cmd="sg_senddiag -p -r 17,00,00,0B,00,00,00,00,6c,6F,67,20,67,65,74"
ses_10page_cmd="sg_ses -p 0x10"
pattern0x10="Invalid response, wanted page code: 0x10 but got 0x17"

log_filter_diag_cmd="sg_senddiag -p -r 10,00,00,13,00,00,6c,6F,67,20,66,69,6c,74,65,72,20,67,65,74,20,2d,73"
log_filter_page_cmd="sg_ses -p 0x10"
log_filter_CLI_cmd="log filter get -s"

log_about_diag_cmd="sg_senddiag -p -r 10,00,00,07,00,00,61,62,6f,75,74"
log_about_page_cmd="sg_ses -p 0x10"
log_about_CLI_cmd="about"


log_LED_diag_cmd="sg_senddiag -p -r 10,00,00,09,00,00,6c,65,64,20,67,65,74"
log_LED_page_cmd="sg_ses -p 0x10"
log_LED_CLI_cmd="led get"

log_sespage_diag_cmd="sg_senddiag -p -r 10,00,00,0b,00,00,6c,6f,67,20,63,6c,65,61,72"
log_sespage_page_cmd="sg_ses -p 0x10"

log_filter_diag_17cmd="sg_senddiag -p -r 17,00,00,15,00,00,00,00,6c,6F,67,20,66,69,6c,74,65,72,20,67,65,74,20,2d,73"
log_about_diag_17cmd="sg_senddiag -p -r 17,00,00,09,00,00,00,00,61,62,6f,75,74"
log_LED_diag_17cmd="sg_senddiag -p -r 17,00,00,0B,00,00,00,00,6c,65,64,20,67,65,74"
log_sespage_diag_17cmd="sg_senddiag -p -r 17,00,00,0d,00,00,00,00,6c,6f,67,20,63,6c,65,61,72"

log_filter_page_17cmd="sg_ses -p 0x17"
page02_canisterB_cmd="sg_ses --page=0x02 --index=esc,1"
canisterB_status="status: Not installed"
canisterA_status="status: OK"
canisterB_status_titan_G2_WB="status: OK"
page02_canisterA_cmd="sg_ses --page=0x02 --index=esc,0"
setmode_internal_cmd="fan set -m i \r"
setmode_external_cmd="fan set -m e \r"
set_pwm_cli_cmd="fan set -p 35 \r"
set_pwm_value="35%"
fan_speed_1_cmd="fan set -l 1 \r"
fan_speed_2_cmd="fan set -l 2 \r"
fan_speed_3_cmd="fan set -l 3 \r"
fan_speed_4_cmd="fan set -l 4 \r"
fan_speed_5_cmd="fan set -l 5 \r"
fan_speed_6_cmd="fan set -l 6 \r"
fan_speed_7_cmd="fan set -l 7 \r"

canister_b_ses_cmd="sg_ses --page=0x07 --index=esc,1"
canister_b_pattern="Element 1 descriptor: ESM B"
canister_a_ses_cmd="sg_ses --page=0x07 --index=esc,0"
canister_CLI_cmd="fru get"

scsi_support_ses_cmd="sg_luns"
scsi_option="-H"
lun_ses_pattern = {
"line1":"00     00 00 00 08 00 00 00 00  00 00 00 00 00 00 00 00",
}
pg2_enc_status_cmd="sg_ses --page=0x02 --index=enc,0"
pg2_enc_status={
"line1":"CELESTIC  TITAN-4U90\s+\d+.",
"line2":"Enclosure Status diagnostic page:",
"line3":"INVOP.*",
"line4":"generation code: 0x0",
"line5":"status descriptor list",
"line6":"Element 0 descriptor:",
"line7":"Predicted failure=0, Disabled=0, Swap=0, status: OK",
"line8":"Ident=0, Time until power cycle=0, Failure indication=0",
"line9":"Warning indication=0, Requested power off duration=0",
"line10":"Failure requested=0, Warning requested=0",
}
log_wrongdata_cmd="sg_senddiag -p -r 13,00,00,02,00,00,00"
pg2_esc0_cmd="sg_ses --page=0x02 --index=esc,0"
pg2_esc1_cmd="sg_ses --page=0x02 --index=esc,1"
reset_exp_cmd="sg_senddiag -p -r 04,00,00,04,a0,00,00,00"
esc0_report_bit="Report=1"
esc1_report_bit="Report=0"
slot_num_sec1="46"
slot_num_pri_sec1="46"
slot_num_sec2="47"
slot_num_pri_sec2="47"
read_mid_plane_VPD_cmd="sg_senddiag -p -r 12,00,00,05,00,0e,00,00,00"
read_canister_VPD_cmd="sg_senddiag -p -r 12,00,00,05,00,07,00,00,00"
read_PSU_VPD_cmd="sg_senddiag -p -r 12,00,00,05,00,02,00,00,00"
read_all_VPD_cmd="sg_senddiag -p -r 12,00,00,05,00,ff,00,00,00"
get_VPD_cmd="sg_ses -p 0x12"
set_on_ident_LED="sg_ses -p 0x2 -I arr,-1 --set=2:1:1=1"
set_off_ident_LED="sg_ses -p 0x2 -I arr,-1 --set=2:1:1=0"
set_on_disk_fault_LED="sg_ses -p 0x2 -I arr,-1 --set=3:5:1=1"
set_off_disk_fault_LED="sg_ses -p 0x2 -I arr,-1 --set=3:5:1=0"
get_page2_cmd="sg_ses -p 0x2"
get_LED_1="|grep -i"
get_LED_2="Array device"
get_LED_3="-A 728 |grep"
get_ident_LED="Ident=1"
get_LED_4="|wc -l"
get_disk_fault_LED="Fault reqstd=1"
ident_disk_fault_LED_on_pattern="90"
ident_disk_fault_LED_off_pattern="0"
set_on_enc_LED="sg_ses -p 2 --index=enc,0 --set=1:7:1=1"
set_off_enc_LED="sg_ses -p 2 --index=enc,0 --set=1:7:1=0"
get_cmd="sg_ses -p 2 --index=enc,0 --get=1:7:1"
get_enc_LED="Enclosure"
get_LED_5="-A 10 |grep"
enc_LED_on_pattern="1"
enc_LED_off_pattern="0"
set_canister_ident_on="sg_ses -p 0x2 -I esc,-1 --set=1:7:1=1"
clear_canister_ident="sg_ses -p 0x2 -I esc,-1 --set=1:7:1=0"
check_can_ident0_cmd="sg_ses -p 0x2 -I esc,0 --get=1:7:1"
check_can_ident1_cmd="sg_ses -p 0x2 -I esc,1 --get=1:7:1"
get_LED_6="Enclosure services"
get_LED_7="-A 9 |grep"
can_iden_on_pattern="1"
can_ident_off_pattern="0"
can_ident_on_pattern_total="2"
set_canister_fault_on="sg_ses -p 0x2 --index=esc,-1 --set=1:6:1=1"
clear_canister_fault="sg_ses -p 0x2 -I esc,-1 --set=1:6:1=0"
can_fault_on_pattern="1"
can_fault_on_pattern_total="2"
can_fault_off_pattern="0"
check_can_fault0_cmd="sg_ses -p 0x2 --index=esc,0 --get=1:6:1"
check_can_fault1_cmd="sg_ses -p 0x2 --index=esc,1 --get=1:6:1"
get_LED_8="Fail=1"
read_asset_tag_cmd="sg_senddiag -p -r 12,00,00,05,02,0e,00,03,06"
write_asset_tag_cmd="sg_senddiag -p -r 12,00,00,0e,01,0e,00,03,06,08,30,31,32,33,34,35,36,37"
write_asset_tag_lesslength_cmd="sg_senddiag -p -r 12,00,00,0e,01,0e,00,03,06,06,30,31,32,33,34,35"
write_asset_tag_morelength_cmd="sg_senddiag -p -r 12,00,00,0e,01,0e,00,03,06,09,30,31,32,33,34,35,36,37,38"
updated_asset_tag_pattern = {
"line1":"CELESTIC.*?\d+",
"line2":"Cannot decode response from diagnostic page: dpage 0x12",
"line3":"00     .*  06 30 31 32 33 34 35 36",
"line4":"10     37",
}
asset_tag_update_error_pattern="sg_senddiag failed: Illegal request"

Inventory_ses_cmd="sg_ses --page=0x07 --index=enc,0"
Inventory_CLI_cmd="fru get\r"



set_drivedisk_power_off_cmd="sg_ses --page=0x02 --index=arr,-1 --set=3:4:1=1"
set_drivedisk_power_on_cmd="sg_ses --page=0x02 --index=arr,-1 --set=3:4:1=0"
get_drivedisk_power_cmd="sg_ses --page=0x02 --index=arr,"
device_off_pattern="Device off =1"
device_on_pattern="Device off =0"

date_set_cmd1="dd_dbg -can_vpd w 0x02000007 F0 6B 21"
mfg_date_pattern1="Manufacture MFG Date: 2000/3/1 1:20"
date_set_cmd2="dd_dbg -can_vpd w 0x02000007 D0 14 20"
mfg_date_pattern2="Manufacture MFG Date: 1999/12/31 1:20"

reset_all_expanders_cmd="sg_senddiag -p -r 04,00,00,04,a0,00,00,00"
reset_expanders_in_ESMA_cmd="sg_senddiag -p -r 04,00,00,04,a0,00,00,01"
reset_expanders_in_ESMB_cmd="sg_senddiag -p -r 04,00,00,04,a0,00,00,02"
reset_local_ESMs_cmd="sg_senddiag -p -r 04,00,00,04,a0,00,00,03"
reset_peer_ESM_cmd="sg_senddiag -p -r 04,00,00,04,a0,00,00,04"
set_dhcp_ip_cmd="sg_senddiag -p -r 04,00,00,14,a1,00,01,00,12,13,14,15,21,22,23,24,ff,ff,ff,ff,12,13,14,10"
set_static_ip_cmd="sg_senddiag -p -r 04,00,00,14,a1,00,00,00,c0,a8,01,0a,c0,a8,01,0b,ff,ff,ff,00,c0,a8,01,01"
pg4_cmd="sg_ses -p 4"
dhcp_ip_pattern = {
"line1":"CELESTIC.*?\d+",
"line2":"\# Response in hex for String In \(SES\) dpage:",
"line3":"00     04 .* 81 00",
"line4":"10     0a cc 7d 35 00 00 00 00  ff ff ff 00 0a cc 7d 01",
"line5":"20     ff 00 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line6":"30     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line7":"40     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line8":"50     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line9":"60     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line10":"70     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line11":"80     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line12":"90     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line13":"a0     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line14":"b0     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line15":"c0     20 20 00",
}
dhcp_ip_pattern_titan_g2_wb = {
"line1":"CELESTIC.*?\d+",
"line2":"\# Response in hex for String In \(SES\) dpage:",
"line3":"00     04 00 00 bf 00 00 01 be  00 00 01 bc 00 80 80 80",
"line4":"10     00 00 00 00 00 00 00 00  ff ff ff ff 00 00 00 00",
"line5":"20     ff 00 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line6":"30     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line7":"40     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line8":"50     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line9":"60     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line10":"70     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line11":"80     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line12":"90     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line13":"a0     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line14":"b0     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line15":"c0     20 20 00",
}

static_ip_pattern = {
"line1":"CELESTIC.*?\d+",
"line2":"\# Response in hex for String In \(SES\) dpage:",
"line3":"00     04 .* 80 00",
"line4":"10     0a 01 a8 c0 00 00 00 00  00 ff ff ff 01 01 a8 c0",
"line5":"20     ff 00 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line6":"30     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line7":"40     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line8":"50     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line9":"60     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line10":"70     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line11":"80     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line12":"90     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line13":"a0     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line14":"b0     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line15":"c0     20 20 00",
}
static_ip_pattern_titan_g2_wb = {
"line1":"CELESTIC.*?\d+",
"line2":"\# Response in hex for String In \(SES\) dpage:",
"line3":"00     04 .* 80 00",
"line4":"10     0a 01 a8 c0 00 00 00 00  00 ff ff ff 01 01 a8 c0",
"line5":"20     ff 00 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line6":"30     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line7":"40     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line8":"50     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line9":"60     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line10":"70     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line11":"80     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line12":"90     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line13":"a0     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line14":"b0     20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20",
"line15":"c0     20 20 00",
}

fan_mode_set_internal_cmd="fan set -m i\r"
fan_mode_set_external_cmd="fan set -m e\r"
fan_mode_get_cmd="fan get\r"
ESM0_cmd="$%^0"
ESM1_cmd="$%^1"
mode_internal_pattern="Internal"
mode_external_pattern="External"
canisterA="A"
canisterB="B"
read_buffer_cmd="sg_read_buffer -m 1 -o 0 -l 0x100"
lun_report_cmd="sg_luns"
lun_report_pattern={
"line1":"Lun list length = 8 which imples 1 lun entry",
"line2":"Report luns \[select_report=0x0\]:",
"line3":"  00000000000000"
}

set_board_product_name = '04,00,00,18,01,01,02,14,41,41,41,41,42,42,42,42,43,43,43,43,32,32,32,33,33,34,34,35'
VPD_update_status_diag_1 = '04,00,00,02,02,01'
VPD_field_data_diag_1 = '04,00,00,04,02,02,01,02'
illegal_request_1 = '04,00,00,18,01,01,02,14,41,41,41,41,42,42,42,42,43,43,43,43,32,32,32,33,33,34,34,35,36'
check_update_status_1 = '00 00 01 01 01 00'
check_board_product_name = '41 41 41 41 42 42 42 42  43 43 43 43 32 32 32 33'

encl_cmd="sg_ses -p 2 /dev/sg2 | grep -v \"INFO=\|rpm\|volts\|Temperature=\""

set_board_product_name_106='04,00,00,11,01,01,01,0d,41,41,41,41,42,42,42,42,31,31,31,31,32'
VPD_update_status_diag_106='04,00,00,02,02,01'
check_update_status_106='00 00 01 01 01 00'
VPD_field_data_diag_106='04,00,00,04,02,02,01,01'
check_board_product_name_106='41 41 41 41 42 42 42 42  31 31 31 31 32'
illegal_request_106='04,00,00,10,01,01,01,0e,41,41,41,41,42,42,42,42,31,31,31,31,31,31'


set_board_product_name_108='04,00,00,24,01,01,03,20,41,41,41,41,42,42,42,42,43,43,43,43,44,44,44,44,32,32,32,32,33,33,33,33,34,34,34,34,34,35,35,35'
VPD_update_status_diag_108='04,00,00,02,02,01'
check_update_status_108='00 00 01 01 01 00'
VPD_field_data_diag_108='04,00,00,04,02,02,01,03'
check_board_product_name_108='41 41 41 41 42 42 42 42  43 43 43 43 44 44 44 44'
illegal_request_108='04,00,00,27,01,01,03,23,41,41,41,41,42,42,42,42,43,43,43,43,44,44,44,44,45,45,45,45,46,46,46,46,32,32,32,32,33,33,33,33,33'

set_board_part_number_109='04,00,00,18,01,01,04,14,41,41,41,41,42,42,42,42,43,43,43,43,44,44,44,44,32,32,32,32'
VPD_update_status_diag_109='04,00,00,02,02,01'
check_update_status_109='00 00 01 01 01 00'
VPD_field_data_diag_109='04,00,00,04,02,02,01,04'
check_board_part_number_109='41 41 41 41 42 42 42 42  43 43 43 43 44 44 44 44'
illegal_request_109='04,00,00,19,01,01,04,15,41,41,41,41,42,42,42,42,43,43,43,43,44,44,44,44,32,32,32,32,33'

set_chassis_part_number = '04,00,00,18,01,02,01,14,44,44,44,44,45,45,45,45,46,46,46,46,47,47,47,47,35,35,35,35'
VPD_update_status_diag_2 = '04,00,00,02,02,01'
VPD_field_data_diag_2 = '04,00,00,04,02,02,02,01'
illegal_request_2 = '04,00,00,19,01,02,01,15,44,44,44,44,45,45,45,45,46,46,46,46,47,47,47,47,35,35,35,35,36'
check_update_status_2 = '00 00 01 01 01 00'
check_chassis_part_number = '44 44 44 44 45 45 45 45  46 46 46 46 47 47 47 47'

set_chassis_product_name='04,00,00,18,01,02,03,14,44,44,44,44,45,45,45,45,46,46,46,46,47,47,47,47,37,37,38,38'
VPD_field_data_diag_112='04,00,00,04,02,02,02,03'
illegal_request_112='04,00,00,19,01,02,03,13,44,44,44,44,45,45,45,45,46,46,46,46,47,47,47,47,37,37,38'
check_chassis_product_name='44 44 44 44 45 45 45 45  46 46 46 46 47 47 47 47'
check_update_status_112='00     00'

set_product_manufacturer = '04,00,00,11,01,03,01,0d,44,44,44,44,45,45,45,45,46,46,46,46,31'
VPD_update_status_diag_3 = '04,00,00,02,02,01'
VPD_field_data_diag_3 = '04,00,00,04,02,02,03,01'
illegal_request_3 = '04,00,00,12,01,03,01,0c,44,44,44,44,45,45,45,45,46,46,46,46'
check_update_status_3 = '00 00 01 01 01 00'
check_product_manufacturer = '44 44 44 44 45 45 45 45  46 46 46 46 31'

set_product_part_number='04,00,00,18,01,03,03,14,43,43,43,43,44,44,44,44,45,45,45,45,46,46,33,33,34,35,36,37'
check_update_status_115=' 00     00'
VPD_field_data_diag_115='04,00,00,04,02,02,03,03'
check_product_part_number='43 43 43 43 44 44 44 44  45 45 45 45 46 46 33 33'
illegal_request_115='04,00,00,25,01,03,03,11,43,43,43,43,44,44,44,44,45,45,45,45,46,46,33,33,34'

set_product_version=' 04,00,00,08,01,03,04,04,43,43,33,33'
check_update_status_116=' 00     00 '
VPD_field_data_diag_116='04,00,00,04,02,02,03,04'
check_product_version='43 43 33 33'
illegal_request_116='04,00,00,09,01,03,04,05,43,43,33,33,35'

set_product_name = '04,00,00,18,01,03,02,14,41,41,41,41,42,42,42,42,43,43,43,43,32,32,32,33,33,34,34,35'
VPD_update_status_diag_4 = '04,00,00,02,02,01'
VPD_field_data_diag_4 = '04,00,00,04,02,02,03,02'
illegal_request_4 = '04,00,00,18,01,03,02,14,41,41,41,41,42,42,42,42,43,43,43,43,32,32,32,33,33,34,34,35,36'
check_update_status_4 = '00 00 01 01 01 00'
check_product_name = '41 41 41 41 42 42 42 42  43 43 43 43 32 32 32 33'

set_wrong_timestamp='11,00,00,0a,00,00,f1,ff,ff,ff,ff,ff,00,00'
diag_failed_check='sg_senddiag failed: Illegal request'

set_chassis_part_number_111 = '04,00,00,24,01,02,02,20,41,41,41,41,42,42,42,42,43,43,43,43,44,44,44,44,32,32,32,32,33,33,33,33,34,34,34,34,34,35,35,35'
VPD_update_status_diag_111 = '04,00,00,02,02,01'
VPD_field_data_diag_111 = '04,00,00,04,02,02,02,02'
illegal_request_111 = '04,00,00,25,01,02,02,15,44,44,44,44,45,45,45,45,46,46,46,46,47,47,47,47,35,35,35,35,36'
check_update_status_111 = '00     00'
check_chassis_part_number_111 = '41 41 41 41 42 42 42 42  43 43 43 43 44 44 44 44'

set_chassis_part_number_117 = '04,00,00,24,01,03,05,20,43,43,43,43,44,44,44,44,46,46,46,46,31,31,33,33,31,31,32,32,33,33,34,34,35,35,36,37,38,39,31,32'
VPD_update_status_diag_117 = '04,00,00,02,02,01'
check_update_status_117 = '00     00'
VPD_field_data_diag_117 = '04,00,00,04,02,02,03,05'
check_chassis_part_number_117 = '43 43 43 43 44 44 44 44  46 46 46 46 31 31 33 33'
illegal_request_117 = '04,00,00,25,01,03,05,11,43,43,43,43,44,44,44,44,46,46,46,46,31,31,33,33,35'

set_chassis_part_number_118 = '04,00,00,0c,01,03,06,08,43,43,43,43,33,33,33,33'
VPD_update_status_diag_118 = '04,00,00,02,02,01'
check_update_status_118 = '00     00'
VPD_field_data_diag_118 = '04,00,00,04,02,02,03,06'
check_chassis_part_number_118 = '43 43 43 43 33 33 33 33'
illegal_request_118 = '04,00,00,0d,01,03,06,09,43,43,43,43,33,33,33,33,34'

timestamp_min = '11,00,00,0a,00,00,00,00,00,00,00,00,00,00'
timestamp_max = '11,00,00,0a,00,00,00,ff,ff,ff,ff,ff,00,00'

version_pattern='FW Revision'
download_log_check='.Upgrade cmpl with no Err.*OSA1.'
CPLD_FW_download_log_check='.Upgrade cmpl with no Err.*PLD , 3'

ses_reset_cmd1='sg_ses -p 2 -I esc,0 --set=1:2:1=1'
ses_reset_cmd2='sg_ses -p 2 -I esc,1 --set=1:2:1=1'

installed_disk_count=10

expect_ESMA_IP_lenovo="000.000.000.000"
expect_gateway_lenovo="000.000.000.000"
expect_ESM_A_DHCP_Mode_lenovo="80"
expect_ESMB_IP_lenovo="000.000.000.000"
expect_ESM_B_DHCP_Mode_lenovo="80"
expect_ESM_Zoning_Mode="80"
expect_ESM_Zoning_Mode_titan_g2_wb="80"
expect_netmask="255.255.255.255"

##############################CONSR-SEST-STRS-0012-0001#########################
sg_pg10_diag_cmd1="10,00,00,09,00,00,66,72,75,20,67,65,74"
sg_pg17_diag_cmd1="17,00,00,0b,00,00,00,00,66,72,75,20,67,65,74"
ses_page_10h_gold_file_1 = 'ses_page_10h_gold_file_1'
ses_page_10h_gold_file_2 = 'ses_page_10h_gold_file_2'
ses_page_17h_gold_file_1 = 'ses_page_17h_gold_file_1'
ses_page_17h_gold_file_2 = 'ses_page_17h_gold_file_2'
ses_page_10h_gold_file_tmp = 'ses_page_10h_gold_file_tmp'
ses_page_17h_gold_file_tmp = 'ses_page_17h_gold_file_tmp'
#############################CTLRS-SYTM-CPU1-0001-0001#########################
expected_cpu_model_name_ESMA="Model name.*:.*Genuine Intel.*R.*CPU"
expected_BIOS_Model_name_ESMA="BIOS.*Model name.*:.*Genuine Intel.*R.*CPU"
expected_cpu_model_name_ESMB="Model name.*:.*Intel.*R.*Xeon.*R.*Gold 5318Y CPU"
expected_BIOS_Model_name_ESMB="BIOS.*Model name.*:.*Intel.*R.*Xeon.*R.*Gold 5318Y CPU"
#############################CTLRS-SYTM-DMT1-0001-0001#########################
expected_part_number1="Part Number.*: 36ASF8G72PZ-3G2B2"
expected_part_number2="Part Number.*: NMB1XBD128GQ"
#############################CTLRS-SYTM-USB1-0005-0001#########################
expected_usb_link_speed="5000M"
#############################CTLRS-SYTM-PCIE-0002-0001#########################
pcie_slotlist_1_A=['17:00.0',]  # slots '31:00.0', 'ca:00.0' and 'b1:00.0' to be added to this list once it is available
pcie_slotlist_2_A=['5a:00.0','a7:00.0','f2:00.0','74:00.0'] 
pcie_slotlist_1_B=['17:00.0',]  # slots '31:00.0', 'ca:00.0' and 'b1:00.0' to be added to this list once it is available
pcie_slotlist_2_B=['5a:00.0','a7:00.0','f2:00.0','74:00.0']
expected_pcie_speed="LnkSta.*:.*Speed 16GT"
expected_width_list1="LnkSta:.*Width x8"
expected_width_list2="LnkSta:.*Width x16"
#############################CTLRS-SYTM-DMT1-0009-0001#########################
expected_memory_info_A='65985.*kB'
expected_memory_info_B='10562.*kB'
#############################CTLRS-SYTM-USB1-0001-0001#########################
expected_USB_Devices1='Bus.*Device.*:.*ID.*Linux Foundation.*root hub'
expected_USB_Devices2='Bus.*Device.*:.*ID.*Dell Computer Corp.*Keyboard'
expected_USB_Devices3='Bus.*Device.*:.*ID.*Linux Foundation.*root hub'
#############################CTLRS-SYTM-PCIE-0001-0001#########################
expected_number_PCIE_devices='462'
#############################CTLRS-SYTM-PCIE-0004-0001#########################
PCIE_device_info='Broadcom.*LSI.*PCIe.*Switch.*management.*endpoint'
PCIE_device_id=['5a:00.0','74:00.0','a7:00.0','f2:00.0']
#############################CTLRS-SYTM-LANT-0003-0001#########################
expected_auto_neg_support='Supports auto-negotiation: Yes'
#############################CTLRS-SYTM-UUID-0001-0001#########################
serial_number="Serial.* Number: 0987654321098765ABCDEFGHIJKLMNOP"
#############################CTLRS-SYTM-POWE-0003-0001#########################
error_messages_sell_list = 'error,fault,fail,warning'
cmd_check_disk_num_nebula='lsscsi -g |grep nvme|wc -l'
expected_disk_count='2'
smp_exp_index = '1'
canisterB_status_Athena="status: OK"
canister_CLI_cmd="fru get\r"
canister_b_pattern_athena="Element 1 descriptor: ESMB"
Inventory_CLI_cmd="fru get\r"
Athena_pg2_enc_status={
"line1":"CELESTIC  P2523\s+\d+.",
"line2":"Enclosure Status diagnostic page:",
"line3":"INVOP.*",
"line4":"generation code: 0x0",
"line5":"status descriptor list",
"line6":"Element 0 descriptor:",
"line7":"Predicted failure=0, Disabled=0, Swap=0, status: OK",
"line8":"Ident=0, Time until power cycle=0, Failure indication=0",
"line9":"Warning indication=0, Requested power off duration=0",
"line10":"Failure requested=0, Warning requested=0",
}
psu0_cli_pattern_athena=""".*--- Power Supply 0 ---.*
.*PS Type: TDPS2400HB A.*
.*PS Manufacturer: DELTA.*
.*PS Serial Number:.*\\S+.*
.*PS Part Number:.*\\S+.*
.*PS Hardware Version: S2F.*
.*PS Firmware Version: 01000M.*"""

psu1_cli_pattern_athena=""".*--- Power Supply 1 ---.*
.*PS Type: CPR-2021-2M16.*
.*PS Manufacturer: COMPUWARE.*
.*PS Serial Number:.*\\S+.*
.*PS Part Number:.*\\S+.*
.*PS Hardware Version: 1.0.*
.*PS Firmware Version: N/A.*"""
psu125_status_pg2_pattern_athena="status: OK"
canisterB_status_Athena="status: OK"
canister_CLI_cmd="fru get\r"
canister_b_pattern_athena="Element 1 descriptor: ESMB"
Inventory_CLI_cmd="fru get\r"
Athena_pg2_enc_status={
"line1":"CELESTIC  P2523\s+\d+.",
"line2":"Enclosure Status diagnostic page:",
"line3":"INVOP.*",
"line4":"generation code: 0x0",
"line5":"status descriptor list",
"line6":"Element 0 descriptor:",
"line7":"Predicted failure=0, Disabled=0, Swap=0, status: OK",
"line8":"Ident=0, Time until power cycle=0, Failure indication=0",
"line9":"Warning indication=0, Requested power off duration=0",
"line10":"Failure requested=0, Warning requested=0",
}
psu0_cli_pattern_athena=""".*--- Power Supply 0 ---.*
.*PS Type: TDPS2400HB A.*
.*PS Manufacturer: DELTA.*
.*PS Serial Number:.*\\S+.*
.*PS Part Number:.*\\S+.*
.*PS Hardware Version: S2F.*
.*PS Firmware Version: 01000M.*"""

psu1_cli_pattern_athena=""".*--- Power Supply 1 ---.*
.*PS Type: CPR-2021-2M16.*
.*PS Manufacturer: COMPUWARE.*
.*PS Serial Number:.*\\S+.*
.*PS Part Number:.*\\S+.*
.*PS Hardware Version: 1.0.*
.*PS Firmware Version: N/A.*"""
psu125_status_pg2_pattern_athena="status: OK"
a_page_Output=""".*Element index: 3  eiioe=0.*
.*Transport protocol: PCIe.*
.*PCIe protocol type: NVMe.*
.*number of ports: 1, not all ports: 0, device slot number: 4.*
.*PCIe vendor id: 0x144d.*
.*serial number: .*
.*model number: SAMSUNG.*
.*port index: 0.*"""
page_a_command="sg_ses --page=0x0a"
drv0_2="0-2"
drv3="3"
drv4="4"
drv5="5"
OK_status1={
        "line1":"status: Not installed"
        }
unsupported_status1={
        "line1":"status: OK",
        }
clear_log_entry_pattern_athena="00     13 00 00 18 04 00 00 01  00"
page_13_clear_log_cmd_b = "sg_senddiag -p -r 13,00,00,03,01,01,03"
page_13_entries_num_cmd_b = "sg_senddiag -p -r 13,00,00,06,02,01,00,01,ff,ff"
clear_log_entry_pattern_athena_b="00     13 00 00 18 04 01 00 01  00"
psu125_status_pg2_pattern_athena="status: OK"
athena_fan_min_speed_cli="55%"
athena_fan_speed_10_l75cli="55%"
athena_fan_speed_11_l75cli="60%"
athena_fan_speed_12_l75cli="70%"
athena_fan_speed_13_l75cli="80%"
athena_fan_speed_14_l75cli="90%"
athena_fan_max_speed_l75cli="100%"
athena_read_mid_plane_VPD_cmd="sg_senddiag -p -r 12,00,00,03,00,0e,00"
athena_read_canister_VPD_cmd="sg_senddiag -p -r 12,00,00,03,00,07,00"
athena_read_PSU_VPD_cmd="sg_senddiag -p -r 12,00,00,03,00,02,00"
athena_read_all_VPD_cmd="sg_senddiag -p -r 12,00,00,03,00,ff,00"
###################################CONSR-SEST-CMDL-0003-0001#########################
delay_seconds="2"
