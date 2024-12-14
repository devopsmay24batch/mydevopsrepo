ESM_prompt="ESM \w \$"
G_RETRY_COUNT = '3x'
ESMA_IP = '10.204.82.115'
ESMA_port = '2031'
ESMB_IP = '10.204.82.115'
ESMB_port = '2032'
ESMA_IP_1 ='10.204.82.115'
ESMA_port_1 = '2031'
cronus_ses_page_tmp_file = 'cronus_ses_page_tmp_file'
cronus_ses_version_read_by_01h = '0011'
cronus_ses_page_01h_gold_file = 'cronus_ses_page_01h_gold_file'
cronus_ses_page_01h_gold_file_2 = 'cronus_ses_page_01h_gold_file_2'
cronus_ses_page_01h_gold_file_ESMB = 'cronus_ses_page_01h_gold_file_ESMB'
cronus_ses_page_01h_gold_file_2_ESMB='cronus_ses_page_01h_gold_file_2_ESMB'

cronus_ses_page_01h_info = {
    'rev:\s+(\S+)' : '0011',
    'number of secondary subenclosures:\s+(\S+)' : '0',
    'generation code:\s+(\S+)' : '0x0',
    'Subenclosure identifier:\s+(.+)' : '0 [primary]',
    'relative ES process id:\s+(\w+)' : '[1|2]',
    'number of ES processes:\s+(\S+)' : '2',
    'number of type descriptor headers:\s+(\S+)' : '10',
    'enclosure logical identifier \(hex\):\s+(.+)' : '500e0eca0763dc00',
    'enclosure vendor:\s+(\S+)' : 'CELESTIC',
}

#sample_invalid_list_cronus_wb = "0-9"
sample_valid_list_cronus_wb = "0-11"

cronus_page7_slotname_check_cmd="sg_ses --page=0x07 --index=0-11"
cronus_smp_exp_index = '0'
cronus_a_page_Output=""".*Element index: 1  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 0.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 2  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 1.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 3  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 2.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 4  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 3.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 5  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 4.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 6  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 5.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 7  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 6.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 8  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 7.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 9  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 8.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 10  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 9.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 11  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 10.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*
.*Element index: 12  eiioe=1.*
.*Transport protocol: SAS.*
.*number of phys: 1, not all phys: 0, device slot number: 11.*
.*phy index: 0.*
.*SAS device type: end device.*
.*initiator port for:.*
.*target port for: SSP.*
.*attached SAS address: 0x500e0eca0763dc3f.*
.*SAS address: 0x5000.*
.*phy identifier: 0x.*"""
page_13_entries_num_cmd_cronus="sg_senddiag -p -r 13,00,00,02,00,00"
clear_log_entry_pattern_cronus="00     13 00 00 15 01 00 00 00  00 00 00 00 00 00 00 00"
cronus_sg_inquiry_cmd = "sg_inq"
cronus_sg_inquiry_pattern = {
        "Vendor identification" : "(\S+)",
        "Product identification": "(\S+)",
        "Product revision level": "(\S+)",
        "Unit serial number"    : "(\S+)"
        }
cronus_sg_inquiry_length = {
        "Vendor identification" : 8,
        "Product identification": 16,
        "Product revision level": 4,
        "Unit serial number"    : 32
        }
SENSORS = ['0', '1', '2', '3', '4', '5', '6']
voltage_SENSORS = [('0', '4.99'), ('1', '3.28'), ('2', '11.90'), ('3', '1.79'), ('4', '1.43'), ('5', '0.91'), ('6', '5.04'), ('7', '3.31'), ('8', '11.96'), ('9', '1.79'), ('10', '1.44'), ('11', '0.92')]
pg2_enc_status_cronus={
"line1":"CELESTIC  SD4100\s+\d+.",
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
info_bit_enable= 1
info_bit_off=0
sasaddesm={
        "500e0eca0763dc00",}

element_voltage_sensor_status={
        "Element type: Voltage sensor, subenclosure id: 0 [ti=8]",
        "     Overall descriptor:",
        "       Predicted failure=0, Disabled=0, Swap=0, status: Critical",
        "       Ident=0, Fail=0,  Warn Over=0, Warn Under=0, Crit Over=0",
        "       Crit Under=0",
        "       Voltage: 0.00 volts",
        "Element 11 descriptor:",
        " Predicted failure=0, Disabled=0, Swap=0, status: Critical",
        " Ident=0, Fail=0,  Warn Over=0, Warn Under=0, Crit Over=1",
        " Crit Under=0",
        " Voltage: 0.92 volts",
        }
element_threshold_status={
        "Element type: Voltage sensor, subenclosure id: 0 [ti=8]",
        "     Overall descriptor:",
        "       high critical=0.0 %, high warning=0.0 % (above nominal voltage)",
        "       low warning=0.0 %, low critical=0.0 % (below nominal voltage)",
        "     Element 11 descriptor:",
        "       high critical=0.0 %, high warning=8.0 % (above nominal voltage)",
        "       low warning=8.0 %, low critical=10.0 % (below nominal voltage)",
        }
power  = [
        "V11         ESM B 0.9                             0.920V    Abnormal      [-10%,-8%,+8%,+0%]       N/A"
        ]
threshold_get_cronus  = [
        "V11      ESM B 0.9                                              -10%   -8%    +8%    +0%"
        ]
var_voltage_sensor_status  = [
        "      Element 0 descriptor:",
        "        Predicted failure=0, Disabled=0, Swap=0, status: OK",
        "        Ident=0, Fail=0,  Warn Over=0, Warn Under=0, Crit Over=0",
        "        Crit Under=1",
        "        Voltage: 4.99 volts"
        ]

var_threshold  = [
        "      Element 0 descriptor:",
        "        high critical=6.0 %, high warning=5.0 % (above nominal voltage)",
        "        low warning=5.0 %, low critical=0.0 % (below nominal voltage)"
        ]

low_warning_sensor_status = [
"Overall descriptor:",
        "Predicted failure=0, Disabled=0, Swap=0, status: Noncritical",
        "Ident=0, Fail=0,  Warn Over=0, Warn Under=0, Crit Over=0",
        "Crit Under=0",
        "Voltage: 0.00 volts",
      "Element 0 descriptor:",
        "Predicted failure=0, Disabled=0, Swap=0, status: Noncritical",
        "Ident=0, Fail=0,  Warn Over=0, Warn Under=1, Crit Over=0",
        "Crit Under=0",
        "Voltage: 4.99 volts",
        ]
low_warning_threshold_status = [
      "Element 0 descriptor:",
        "high critical=6.0 %, high warning=5.0 % (above nominal voltage)",
        "low warning=0.0 %, low critical=6.0 % (below nominal voltage)",
       ]
var_checkPower  = [
        "V0          ESM A 5.0                             4.992V    Abnormal      [-0%,-5%,+5%,+6%]        OFF",
        ]

var_checkthreshold  = [
        "V0       ESM A 5.0                                              -0%    -5%    +5%    +6%",
        ]
psu125_status_pg2_pattern_cronus="status: OK"
psu1_cli_pattern_cronus=""".*--- Power Supply 1 ---.*
.*PS Type: FSG032.*
.*Power Capacity: 800.*
.*PS Manufacturer: ACBEL.*
.*PS Serial Number:.*\\S+.*
.*PS Part Number:.*
.*PS Firmware Version: 010190.*
.*HW EC LEVEL: A00.*"""
psu0_cli_pattern_cronus =""".*--- PSU 0 ---.*
.*PS Type: FSG032.*
.*Power Capacity: 800.*
.*PS Manufacturer: ACBEL.*
.*PS Serial Number:.*\\S+.*
.*PS Part Number: .*
.*PS Firmware Version: 010190.*
.*HW EC LEVEL: A00.*"""
drv0_11="0-11"
OK_status_cronus_wb={
                "line1":"status: Unsupported",
                        "line2":"status: Not installed"
                                }
mode_sense_page19_pattern_cronus={
"line1":"CELESTIC.*?\d+",
"line2":"Mode parameter header from MODE SENSE\(10\):",
"line3":"Mode data length=24, medium type=0x00, specific param=0x00, longlba=0",
"line4":"Block descriptor length=0",
"line5":"Protocol specific port \(SAS\), page_control: current",
"line6":"00     19 0e 66 00 07 d0 75 30  00 0a 00 00 00 00 00 00",
}
mode_sense_page3Fh_ff_pattern_cronus = {
"line1" : "CELESTIC.*?\d+",
"line2" : "Mode parameter header from MODE SENSE\(10\)",
"line3" : "Mode data length=1884, medium type=0x00, specific param=0x00, longlba=0",
"line4" : "Block descriptor length=0",
"line5" : "Protocol specific logical unit \(SAS\), page_control: current",
"line6" : " 00     18 06 06 00 00 00 00 00",
"line7" : "Protocol specific port \(SAS\), page_control: current",
"line8" : " 00     19 0e 66 00 07 d0 75 30  00 0a 00 00 00 00 00 00",
"line9" : "Phy control and discover \(SAS\), page_control: current",
}
psu1_cli_pattern_cronus=""".*--- Power Supply 1 ---.*
.*PS Type: FSG032.*
.*Power Capacity: 800.*
.*PS Manufacturer: ACBEL.*
.*PS Serial Number:.*\\S+.*
.*PS Part Number: .*
.*PS Firmware Version: 010190.*
.*HW EC LEVEL: A00.*"""

high_warning_sensor_status = [
        "Element type: Voltage sensor, subenclosure id: 0 [ti=8]",
        "      Overall descriptor:",
        "        Predicted failure=0, Disabled=0, Swap=0, status: Noncritical",
        "        Ident=0, Fail=0,  Warn Over=0, Warn Under=0, Crit Over=0",
        "        Crit Under=0",
        "      Element 6 descriptor:",
        "        Predicted failure=0, Disabled=0, Swap=0, status: Noncritical",
        "        Ident=0, Fail=0,  Warn Over=1, Warn Under=0, Crit Over=0",
        "        Crit Under=0",
        "        Voltage: 5.04 volts",
            ]
high_warning_threshold_status = [
        "Element 6 descriptor:",
        "        high critical=5.0 %, high warning=0.0 % (above nominal voltage)",
        "        low warning=6.0 %, low critical=7.0 % (below nominal voltage)",
           ]
psu0_Find_pattern_cronus=""".*--- Power Supply 0 ---.*
.*PS Type: N/A.*
.*Power Capacity: N/A.*
.*PS Manufacturer: N/A.*
.*PS Serial Number: {1}.*
.*PS Part Number: {0}.*
.*PS Firmware Version: 010190.*
.*HW EC LEVEL: {2}.*"""


