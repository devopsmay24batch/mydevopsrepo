# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

import os
from collections import OrderedDict
import Logger as log
from SwImage import SwImage
from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE,ONIE_RESCUE_MODE
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()
SDK = SwImage.getSwImage("HELGA_SDK")
SDK_SCRIPT = 'auto_load_user.sh'
remote_shell_load_sdk = "./{}".format(SDK_SCRIPT)
sdkname = SDK.newImage
SDK_PATH = '/root/sdk/{}'.format(sdkname)
ifconfig_a_cmd = "ifconfig -a"
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

devicename = os.environ.get("deviceName", "")
import logging
logging.info("devicename:{}".format(devicename))
#### variable define begin ####

# Basic Function Variables
sdk_path = "/usr/local/cls_sdk"
sonic_prompt = "(root|admin)@sonic:.*"
sdk_prompt = sonic_prompt[:-2] + sdk_path
sdk_fail_pattern = "No such file or directory"

# BRIXIA_SDK_TC_13_32x2x400G_Port_Loopback_Test 
tool_64x4x100 = "Helga-Ver1-32x4x100.yml"
tool_32x8x50 = "Helga-Ver1-16x8x50.yml"
tool_256x1x100 = "Helga-Ver1-128x1x100.yml"
tool_32x2x50 = "Helga-Ver1-32x2x50.yml"
tool_32x4x25 = "Helga-Ver1-32x4x25.yml"
tool_32x4x50 = "Helga-Ver1-32x4x50.yml"
tool_64x2x100 = "Helga-Ver1-64x2x100.yml"
tool_64x2x50 = "Helga-Ver1-64x2x100.yml"
tool_32x4x100_loopback = "Helga-Ver1-32x4x100_loopback.yml"
cd_pckt_gen_cmd = "tx 1000 pbm=cd0 length=512 vlan=200"
ce_pckt_gen_cmd = "tx 1000 pbm=ce0 length=512 vlan=200"
cd_pckt_gen_cmd_180 = "snake_traffic_cpu_test_180s.soc"
cd_stop_traffic = "pvlan set cd{} 1888"
cd_stop_traffic_128 = "pvlan set ce{} 1888"
cd_lb_cmd = "port cd lb=mac"
cd_ps_cmd = "ps cd"
ce_lb_cmd = "port ce lb=mac"
ce_ps_cmd = "ps ce"
cd_snake_cmd = "snake_traffic_helga_32x4x100_set.soc"
cd_snake_cmd_16_8_50 = "snake_traffic_helga_16x8x50_set.soc"
cd_snake_cmd_128 = "snake_traffic_helga_128x1x100_set_dac.soc"
cd_snake_cmd_128_nondac = "snake_traffic_helga_128x1x100_set.soc"
cd_snake_cmd_32_4_100 = "snake_traffic_helga_32x4x100_set.soc"
port_mac_63_status_pattern = []
port_mac_ptn = ".*{}{}.*up.*MAC.*"

# TC 30
disabled_port_63_status_pattern = []
link_up_63_status_pattern = []
link_speed_63_status_pattern = []
for i in range(32):
    disabled_port_63_status_pattern.append(".*cd{}[(].*!ena.*".format(i))
    link_up_63_status_pattern.append(".*cd{}[(].*up.*".format(i))
    link_speed_63_status_pattern.append(".*cd{}[(].*400G.*".format(i))
################################################################################
#TC_16
xe_mac_patn = []
for i in range (0,2):
    regexp = ".*xe"+str(i)+"[(].*up.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE.*MAC"
    xe_mac_patn.append(regexp)

xe1_lb_cmd = "port xe lb=mac"
xe1_ps_cmd = "ps xe"
xe0_270 = "vlan create 300  pbm=xe0,xe1 ubm=ce0,ce1;pvlan set xe0 300"
xe1_271 = "vlan create 300  pbm=xe0,xe1 ubm=ce0,ce1;pvlan set xe1 300"
xe0_270_pat = "Port xe0 default VLAN is 300"
xe1_271_pat = "Port xe1 default VLAN is 300"
xe_packt_gen_cmd = "tx 1000 pbm=xe0,xe1 length=512 vlan=300"
xe_stop_traffic = "pvlan set xe1 1888"

# TC_20
xe_port_ptn = ".*xe{}[(].*[)].*up.*"
vlan_port_cmds = [
    "vlan clear",
    "vlan remove 1 pbm=all",
    "vlan create 270  pbm=xe0,xe1 ubm=xe0,xe1;pvlan set xe0 270",
    "vlan create 271  pbm=xe0,xe1 ubm=xe0,xe1;pvlan set xe1 271"
]


# TC_14
port_mac_31_status_pattern = []
for i in range(32):
    port_mac_31_status_pattern.append(port_mac_ptn.format('cd', i))

# TC_15
xe_lb_cmd = "port ce lb=mac"
xe_ps_cmd = "ps ce"
xe_snake_cmd = "snake_traffic_brixia_256.soc"

port_mac_255_status_pattern = []
for i in range(256):
    port_mac_255_status_pattern.append(port_mac_ptn.format('ce', i))

#################################################################################
#TC_04
brixiaV2_TH4G_64x4x100_pattern = []
for i in range(0,11):
    regexp = ".* cd"+str(i)+"[(].*up.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_64x4x100_pattern.append(regexp)
for i in range(0):
    regexp = ".*xe"+str(i)+"[(].*up.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE"
    brixiaV2_TH4G_64x4x100_pattern.append(regexp)
for i in range(12,35):
    regexp = ".* cd"+str(i)+"[(].*up.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_64x4x100_pattern.append(regexp)

for i in range(1):
    regexp = ".*xe"+str(i)+"[(].*up.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE"
    brixiaV2_TH4G_64x4x100_pattern.append(regexp)

for i in range(36,64):
    regexp = ".* cd"+str(i)+"[(].*up.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_64x4x100_pattern.append(regexp)

brixiaV2_TH4G_64x4x100_d_pattern = []
for i in range(0,64):
    regexp = ".* cd"+str(i)+"[(].*!ena.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_64x4x100_d_pattern.append(regexp)

brixiaV2_TH4G_64x4x100_e_pattern = []
for i in range(0,64):
    regexp = ".* cd"+str(i)+"[(].*up.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_64x4x100_e_pattern.append(regexp)

brixiaV2_TH4G_32x4x100_d_pattern = []
for i in range(0,32):
    regexp = ".* cd"+str(i)+"[(].*!ena.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_32x4x100_d_pattern.append(regexp)

brixiaV2_TH4G_32x4x100_e_pattern = []
for i in range(0,32):
    regexp = ".* cd"+str(i)+"[(].*up.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_32x4x100_e_pattern.append(regexp)
######################################################################################################
#TC_05
brixiaV2_TH4G_32x8x50_pattern = []
for i in range(0,5):
    regexp = ".* cd"+str(i)+"[(].*up.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_32x8x50_pattern.append(regexp)
for i in range(0):
    regexp = ".*xe"+str(i)+"[(].*up.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE"
    brixiaV2_TH4G_32x8x50_pattern.append(regexp)
for i in range(6,17):
    regexp = ".* cd"+str(i)+"[(].*up.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_32x8x50_pattern.append(regexp)

for i in range(1):
    regexp = ".*xe"+str(i)+"[(].*up.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE"
    brixiaV2_TH4G_32x8x50_pattern.append(regexp)

for i in range(18,32):
    regexp = ".* cd"+str(i)+"[(].*up.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_32x8x50_pattern.append(regexp)

brixiaV2_TH4G_32x8x50_d_pattern = []
for i in range(0,32):
    regexp = ".* cd"+str(i)+"[(].*!ena.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_32x8x50_d_pattern.append(regexp)

brixiaV2_TH4G_32x8x50_e_pattern = []
for i in range(0,32):
    regexp = ".* cd"+str(i)+"[(].*up.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_32x8x50_e_pattern.append(regexp)

helgaV2_TH4G_16x8x50_d_pattern = []
for i in range(0,16):
    regexp = ".* cd"+str(i)+"[(].*!ena.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    helgaV2_TH4G_16x8x50_d_pattern.append(regexp)

helgaV2_TH4G_16x8x50_e_pattern = []
for i in range(0,16):
    regexp = ".* cd"+str(i)+"[(].*up.*400G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    helgaV2_TH4G_16x8x50_e_pattern.append(regexp)

helgaV2_TH4G_64x2x100_e_pattern = []
for i in range(0,64):
    regexp = ".* cd"+str(i)+"[(].*up.*200G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    helgaV2_TH4G_64x2x100_e_pattern.append(regexp)
#for i in range(0,2):
#    regexp = ".* xe"+str(i)+"[(].*up.*10G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*"
#    helgaV2_TH4G_64x2x100_e_pattern.append(regexp)

helgaV2_TH4G_32x2x50_e_pattern = []
for i in range(0,32):
    regexp = ".* ce"+str(i)+"[(].*up.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*1xN"
    helgaV2_TH4G_32x2x50_e_pattern.append(regexp)

helgaV2_TH4G_32x2x100_disable_pattern = []
for i in range(0,32):
    regexp = ".* cd"+str(i)+"[(].*up.*200G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    helgaV2_TH4G_32x2x100_disable_pattern.append(regexp)

helgaV2_TH4G_32x2x50_disable_pattern = []
for i in range(0,32):
    regexp = ".* ce"+str(i)+"[(].*up.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*1xN"
    helgaV2_TH4G_32x2x50_disable_pattern.append(regexp)

helgaV2_TH4G_32x4x25_e_pattern = []
for i in range(0,32):
    regexp = ".* ce"+str(i)+"[(].*up.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*NONE"
    helgaV2_TH4G_32x4x25_e_pattern.append(regexp)

helgaV2_TH4G_32x4x50_e_pattern = []
for i in range(0,32):
    regexp = ".* cd"+str(i)+"[(].*up.*200G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    helgaV2_TH4G_32x4x50_e_pattern.append(regexp)

helgaV2_TH4G_64x2x50_e_pattern = []
for i in range(0,64):
    regexp = ".* ce"+str(i)+"[(].*up.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*1xN"
    helgaV2_TH4G_64x2x50_e_pattern.append(regexp)

helgaV2_TH4G_64x2x100_d_pattern = []
for i in range(0,64):
    regexp = ".* cd"+str(i)+"[(].*!ena.*200G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    helgaV2_TH4G_64x2x100_d_pattern.append(regexp)
#for i in range(0,2):
#    regexp = ".* xe"+str(i)+"[(].*!ena.*10G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*"
#    helgaV2_TH4G_64x2x100_d_pattern.append(regexp)

#########################################################################################################
#TC_06
brixiaV2_TH4G_256x1x100_pattern = []
for i in range(0,47):
    regexp = ".* ce"+str(i)+"[(].*up.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_256x1x100_pattern.append(regexp)
for i in range(0):
    regexp = ".*xe"+str(i)+"[(].*up.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE"
    brixiaV2_TH4G_256x1x100_pattern.append(regexp)
for i in range(48,143):
    regexp = ".* ce"+str(i)+"[(].*up.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_256x1x100_pattern.append(regexp)
for i in range(1):
    regexp = ".*xe"+str(i)+"[(].*up.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE"
    brixiaV2_TH4G_256x1x100_pattern.append(regexp)
for i in range(144,256):
    regexp = ".* ce"+str(i)+"[(].*up.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    brixiaV2_TH4G_256x1x100_pattern.append(regexp)

brixiaV2_TH4G_256x1x100_d_pattern = []
for i in range(0,256):
    regexp = ".* ce"+str(i)+"[(].*!ena.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544-2xN"
    brixiaV2_TH4G_256x1x100_d_pattern.append(regexp)

brixiaV2_TH4G_256x1x100_e_pattern = []
for i in range(0,256):
    regexp = ".* ce"+str(i)+"[(].*up.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544-2xN"
    brixiaV2_TH4G_256x1x100_e_pattern.append(regexp)

helgaV2_TH4G_128x1x100_pattern = []
for i in range(0,128):
    regexp = ".* ce"+str(i)+"[(].*up.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544.*2xN"
    helgaV2_TH4G_128x1x100_pattern.append(regexp)
for i in range(0):
    regexp = ".*xe"+str(i)+"[(].*up.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE"
    helgaV2_TH4G_128x1x100_pattern.append(regexp)
for i in range(1):
    regexp = ".*xe"+str(i)+"[(].*up.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE"
    helgaV2_TH4G_128x1x100_pattern.append(regexp)

helgaV2_TH4G_128x1x100_d_pattern = []
for i in range(0,128):
    regexp = ".* ce"+str(i)+"[(].*!ena.*100G.*FD.*No.*Forward.*TX RX.*Copper.*9412.*RS544-2xN"
    helgaV2_TH4G_128x1x100_d_pattern.append(regexp)
for i in range(0):
    regexp = ".*xe"+str(i)+"[(].*!ena.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE"
    helgaV2_TH4G_128x1x100_d_pattern.append(regexp)
for i in range(1):
    regexp = ".*xe"+str(i)+"[(].*!ena.*10G.*FD.*No.*Forward.*TX RX.*Backplane.*9412.*NONE"
    helgaV2_TH4G_128x1x100_d_pattern.append(regexp)
#############################################################################################################

#BER Tests
phydiag_cmds = [
        "phydiag 1-270 prbs set p=3",
        "phydiag 1-270 prbsstat start interval=30",
        "phydiag 1-270 prbsstat ber"
    ]

#TC 18,19
vlan_pattern_32x8x50 = []
for i in range(1,2):
    regexp = "vlan "+str(i)+".*ports cpu.*cd0-cd2.*cd29-cd31.*"
    vlan_pattern_32x8x50.append(regexp)
for i in range(200,231):
    regexp = "vlan "+str(i)+".*ports.*cd.*-cd.*"
    vlan_pattern_32x8x50.append(regexp)
for i in range(231,232):
    regexp ="vlan "+str(i)+".*ports.*cd.*,cd.*"
    vlan_pattern_32x8x50.append(regexp)
##########################################################################################
vlan_pattern_64x4x100 = []
for i in range(1,2):
    regexp = "vlan "+str(i)+".*ports cpu.*cd0-cd4.*cd57-cd63.*"
    vlan_pattern_64x4x100.append(regexp)
for i in range(200,260):
    regexp = "vlan "+str(i)+".*ports.*cd.*-cd.*"
    vlan_pattern_64x4x100.append(regexp)

vlan_pattern_32x4x100 = []
for i in range(1,2):
    regexp = "vlan "+str(i)+".*ports cpu.*"
    vlan_pattern_32x4x100.append(regexp)
for i in range(200,231):
    regexp = "vlan "+str(i)+".*ports.*cd.*-cd.*"
    vlan_pattern_32x4x100.append(regexp)
for i in range(231,232):
    regexp = "vlan "+str(i)+".*ports.*cd.*,cd.*"
    vlan_pattern_32x4x100.append(regexp)
for i in range(300,301):
    regexp = "vlan "+str(i)+".*ports xe.*"
    vlan_pattern_32x4x100.append(regexp)


############################################################################################
vlan_pattern_256x1x100 = []

for i in range(1,2):
     regexp = "vlan "+str(i)+".*ports.* none.*"
     vlan_pattern_256x1x100.append(regexp)

for i in range(20,30):
     regexp = "vlan "+str(i)+".*ports.*ce.*-ce.*"
     vlan_pattern_256x1x100.append(regexp)

for i in range(210,300):
     regexp = "vlan "+str(i)+".*ports.*ce.*-ce.*"
     vlan_pattern_256x1x100.append(regexp)
for i in range(2100,2255):
     regexp = "vlan "+str(i)+".*ports.*ce.*-ce.*"
     vlan_pattern_256x1x100.append(regexp)
for i in range(2255,2255):
     regexp = "vlan "+str(i)+".*ports.*ce0,ce255.*"
     vlan_pattern_256x1x100.append(regexp)


vlan_pattern_128x1x100 = []

for i in range(1,2):
     regexp = "vlan "+str(i)+".*ports.* none.*"
     vlan_pattern_128x1x100.append(regexp)

for i in range(201,208):
     regexp = "vlan "+str(i)+".*ports.*ce.*,ce.*"
     vlan_pattern_128x1x100.append(regexp)

for i in range(216,217):
     regexp = "vlan "+str(i)+".*ports.*ce.*-ce.*"
     vlan_pattern_128x1x100.append(regexp)

for i in range(217,224):
     regexp = "vlan "+str(i)+".*ports.*ce.*,ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(232,233):
     regexp = "vlan "+str(i)+".*ports.*ce.*-ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(233,240):
     regexp = "vlan "+str(i)+".*ports.*ce.*,ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(248,249):
     regexp = "vlan "+str(i)+".*ports.*ce.*-ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(249,256):
     regexp = "vlan "+str(i)+".*ports.*ce.*,ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(264,265):
     regexp = "vlan "+str(i)+".*ports.*ce.*-ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(265,272):
     regexp = "vlan "+str(i)+".*ports.*ce.*,ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(280,281):
     regexp = "vlan "+str(i)+".*ports.*ce.*-ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(281,288):
     regexp = "vlan "+str(i)+".*ports.*ce.*,ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(296,297):
     regexp = "vlan "+str(i)+".*ports.*ce.*-ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(297,304):
     regexp = "vlan "+str(i)+".*ports.*ce.*,ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(312,313):
     regexp = "vlan "+str(i)+".*ports.*ce.*-ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(313,320):
     regexp = "vlan "+str(i)+".*ports.*ce.*,ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(327,328):
     regexp = "vlan "+str(i)+".*ports.*ce.*,ce.*"
     vlan_pattern_128x1x100.append(regexp)
for i in range(400,401):
     regexp = "vlan "+str(i)+".*ports.*xe.*"
     vlan_pattern_128x1x100.append(regexp)


############################################################################################

snake_cmd_1 = "snake_traffic_brixia_set32.soc"
snake_cmd_2 = "snake_traffic_brixia_256.soc"
ce_pckt_gen_cmd = "tx 1000 pbm=ce0 length=512 vlan=20"
ce_stop_traffic = "pvlan set ce{} 1888"

############################################################################################
#TC 25
prbs = [
          "50 : PRBS OK!",
          "220 : PRBS OK!"
       ]

# TC_31
power_cycle_cmd = "echo 0x4449454a > /sys/devices/gfpga-platform/board_powercycle"
power_cycle_cmd1 = "echo 0 > /sys/devices/platform/mmcpld/mmc_reg.1.auto/system_power_cycle"
reboot_cmd = "reboot"
# TC_24
ucode = "D003_02"

#TC02
BCM_ver="Release: sdk-{}".format(SDK.newVersion) 

for i in range(2255,2255):
     regexp = "vlan "+str(i)+".*ports.*ce0,ce255.*"
     vlan_pattern_256x1x100.append(regexp)


############################################################################################

snake_cmd_1 = "snake_traffic_brixia_set32.soc"
snake_cmd_2 = "snake_traffic_brixia_256.soc"
ce_pckt_gen_cmd = "tx 1000 pbm=ce0 length=512 vlan=20"
ce_stop_traffic = "pvlan set ce{} 1888"

############################################################################################
#TC 25
prbs = [
          "50 : PRBS OK!",
          "220 : PRBS OK!"
       ]

# TC_31
power_cycle_cmd = "echo 0x4449454a > /sys/devices/gfpga-platform/board_powercycle"
# TC_24
ucode = "D003_02"

#TC02
BCM_ver="Release: sdk-{}".format(SDK.newVersion) 

