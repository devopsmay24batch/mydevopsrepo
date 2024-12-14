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
import os
import sys
import Logger as log
import CRobot
import Const
import re
from Decorator import *
import time
from functools import partial
import YamlParse
import GOLDSTONECommonLib
#import ixiaLib

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/goldstone'))
import GoldstoneSdkVariable as var

import CommonLib
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
exec_cmd = device.executeCmd
send_cmd = device.sendCmd


@logThis
def open_sdk_path(path):
    cmd = 'cd ' + path
    exec_cmd(cmd)

@logThis
def auto_load_user(mode, media='backplane'):
    res=None
    if mode == 'daemon':
        cmd = './auto_load_user.sh -d'
        exec_cmd(cmd)
    else:
        cmd = './auto_load_user.sh -y configs/' + mode + '/' + media + '.yml'
        res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(10)
    if res:
        if 'BCM.0>' in res:
            log.info('auto load user script started successfully')
        else:
            raise RuntimeError('BCM prompt not available')

@logThis
def check_port_status(mode='16x1x400',status='up',port=None,res=None):
    if not res:
        log.info('ps command output is not available')
    if port:
        for line in res:
            if port in line:
                if status not in line:
                    log.fail('Port %s status is not as expected. Expected status %s'%(port,status))
                    raise RuntimeError('Port %s status is not as expected. Expected status %s'%(port,status))
                else:
                    log.success('Port %s status as expected'%port)
                    return
        log.fail('Port %s not found in %s'%(port,mode))
        raise RuntimeError('Port %s not found in %s'%(port,mode))
    else:
        log.info("No port specified")


@logThis
def check_all_port_status(mode='16x1x400',status='up',verify=True):
    time.sleep(3)
    res = send_cmd('ps',promptStr=var.sdkBCMPrompt,timeout=120)
    if not verify:
        return
    res = res.split('\n')
    portPrefix=var.portMap[mode]['prefix']
    numPorts=var.portMap[mode]['numPorts']
    for num in range(numPorts):
        port=portPrefix+str(num)
        check_port_status(mode=mode,status=status,port=port,res=res)

@logThis
def disable_port(mode,portNum='all'):
    portkey = var.portMap[mode]['prefix']
    if portNum == 'all':
        cmd = 'port ' + portkey + ' en=0'
    else:
        cmd = 'port ' + portkey + str(portNum) + ' en=0'
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    if portNum == 'all':
        time.sleep(10)
    else:
        time.sleep(0.5)

@logThis
def enable_port(mode,portNum='all'):
    portkey = var.portMap[mode]['prefix']
    if portNum == 'all':
        cmd = 'port ' + portkey + ' en=1'
    else:
        cmd = 'port ' + portkey + str(portNum) + ' en=1'
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    if portNum == 'all':
        time.sleep(10)
    else:
        time.sleep(0.5)

@logThis
def exit_auto_load_user():
    send_cmd('exit')
    time.sleep(10)

@logThis
def run_prbs_test(mode='16x1x400',maxBERepow=5,verify=True):
    cmd = 'configs/%s/prbs_start.soc'%mode
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(30)
    cmd = 'configs/%s/prbs_get.soc'%mode
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(10)
    if verify:
        verify_ber(stats=res,maxBERepow=maxBERepow)
    cmd = 'configs/%s/prbs_stop.soc'%mode
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(2)

@logThis
def verify_ber(stats=None,maxBERepow=5):
    if not stats:
        raise RuntimeError("PRBS output not available")
    stats=stats.split('\n')
    for line in stats:
        if 'e-' in line:
            try:
                ber = re.search('.*e-(\d+)',line)
                epow = ber.group(1)
            except AttributeError:
                raise AttributeError('Could not grep the BER e-power value')
            if int(epow) < maxBERepow:
                log.fail("BER %s higher than acceptable"%ber.group())
                raise RuntimeError("BER %s higher than acceptable"%ber.group())
            if int(epow) == maxBERepow:
                try:
                    mutiplier = re.search('\s+(\S+)e-',line).group(1)
                except AttributeError:
                    raise AttributeError('Could not grep the multiplier value')
                if float(mutiplier) > 1:
                    log.fail("BER %s higher than acceptable"%ber.group())
                    raise RuntimeError("BER %s higher than acceptable"%ber.group())


@logThis
def verify_serdes_version(mode='16x1x400',serdesVersion=var.serdes_version):
    numPorts = var.portMap[mode]['numPorts']
    log.info('Running serdes version check for all ports')
    cmd = 'configs/%s/phydiag_dsc.soc'%mode
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=1200)
    res = res.split('\n')
    count=0
    for line in res:
        if 'Common Ucode Version' in line:
            count +=1
            version= re.search('Common Ucode Version\s*=\s*(\S+)',line).group(1)
            if version == serdesVersion:
                continue
            else:
                log.fail('serdes version mismatch for port %s'%count)
                raise RuntimeError('serdes version mismatch for port %s'%count)
    if count == numPorts:
        log.success('Serdes version check passed for all ports')
    time.sleep(5)


@logThis
def set_lb_mode(lb='mac',mode='16x1x400',portNum='all'):
    portkey = var.portMap[mode]['prefix']
    portRange = var.portMap[mode]['numPorts']
    if portNum == 'all':
        log.info('Setting lb mode for all ports')
    elif int(portNum) in range(portRange):
        portkey+=portNum
    else:
        log.fail('Unknown port number %s'%portNum)
        raise RuntimeError('Invalid port number %s for mode %s'%(portNum,mode))
    cmd = 'port ' + portkey + ' lb=' + lb
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(5)

@logThis
def p2p_internal_traffic_start(mode='16x1x400'):
    count= int(mode.split('x')[1])
    num = str(num)
    cmd = 'shell cat configs/%s/p2p_snake%s_set.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    cmd = 'configs/%s/p2p_snake%s_set.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(5)
    cmd = 'shell cat configs/%s/p2p_snake%s_start.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    cmd = 'configs/%s/p2p_snake%s_start.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(5)
    log.info('Started all traffic.. Wait for 120 seconds')
    time.sleep(120)

@logThis
def p2p_internal_traffic_stop_verify(mode='16x1x400'):
    count= int(mode.split('x')[1])
    cmd = 'shell cat configs/%s/p2p_snake%s_stop.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    cmd = 'configs/%s/p2p_snake%s_stop.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(5)
    cmd = 'shell cat configs/%s/p2p_snake%s_show.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    cmd = 'configs/%s/p2p_snake%s_show.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(5)
    verify_tx_rx_stats(res,mode=mode,snake='dac')

@logThis
def loopback_traffic_start(mode='16x1x400',lb='None'):
    count= int(mode.split('x')[1])
    if lb != 'None':
        set_lb_mode(lb=lb,mode=mode)
        check_all_port_status(mode=mode)
    num = str(num)
    cmd = 'shell cat configs/%s/lb_snake%s_set.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    cmd = 'configs/%s/lb_snake%s_set.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(5)
    cmd = 'shell cat configs/%s/lb_snake%s_start.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    cmd = 'configs/%s/lb_snake%s_start.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(5)
    log.info('Started all traffic.. Wait for 120 seconds')
    time.sleep(120)

@logThis
def loopback_traffic_stop_verify(mode='16x1x400'):
    count= int(mode.split('x')[1])
    cmd = 'shell cat configs/%s/lb_snake%s_stop.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    cmd = 'configs/%s/lb_snake%s_stop.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(5)
    cmd = 'shell cat configs/%s/lb_snake%s_show.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    cmd = 'configs/%s/lb_snake%s_show.soc'%(mode,num)
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(2)
    verify_tx_rx_stats(res,mode=mode)

@logThis
def verify_tx_rx_stats(stats,mode='16x1x400',breakoutSet=None,txParamPattern='_TPKT',rxParamPattern='_RPKT',snake='elb'):
    #import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    if snake == 'elb':
        stats = stats.split('\n')
        tx_pkt_ref_count = 0
        rx_pkt_ref_count = 0
        for line in stats:
            if txParamPattern in line:
                tx_pkt_count = re.search('\S+\s+:\s+(\S+)\s+\S+',line)[1]
                if not tx_pkt_ref_count:
                    log.info(line)
                    tx_pkt_ref_count = tx_pkt_count
                if tx_pkt_count != tx_pkt_ref_count:
                    log.info(line)
                    log.fail('Expected tx_pkt_count is %s and tx_pkt_count is %s'%(tx_pkt_ref_count,tx_pkt_count))
                    raise RuntimeError('Tx Packet count mismatch')
            elif rxParamPattern in line:
                rx_pkt_count = re.search('\S+\s+:\s+(\S+)\s+\S+',line)[1]
                if not rx_pkt_ref_count:
                    log.info(line)
                    rx_pkt_ref_count = rx_pkt_count
                    if rx_pkt_ref_count != tx_pkt_ref_count:
                        raise RuntimeError('Tx and Rx count mismatch for the first port')
                if rx_pkt_count != rx_pkt_ref_count:
                    log.info(line)
                    log.fail('Expected rx_pkt_count is %s and rx_pkt_count is %s'%(rx_pkt_ref_count,rx_pkt_count))
                    raise RuntimeError('Rx Packet count mismatch')
            else:
                continue
        log.success('tx_pkt_count is %s and rx_pkt_count is %s for all ports'%(tx_pkt_count,rx_pkt_count))
    elif snake == 'dac':
        count= int(mode.split('x')[1])
        portkey = var.portMap[mode]['prefix']
        portRange = var.portMap[mode]['numPorts']
        #import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        portList = []
        if not breakoutSet:
            for num in range(1,count+1):
                verify_tx_rx_stats(stats,mode=mode,breakoutSet=num,snake='dac')
            return
        stats = stats.split('\n')
        for num in range(breakoutSet-1,portRange,count):
            portList.append(portkey+str(num))
        for subPortList in (portList[::2],portList[1::2]):
            tx_pkt_ref_count = 0
            rx_pkt_ref_count = 0
            log.info('Verifying traffic stats for %s'%subPortList)
            for line in stats:
                if not any((port+' ') in line for port in subPortList):
                    continue
                if txParamPattern in line:
                    tx_pkt_count = re.search('\S+\s+:\s+(\S+)\s+\S+',line)[1]
                    if not tx_pkt_ref_count:
                        log.info(line)
                        tx_pkt_ref_count = tx_pkt_count
                    if tx_pkt_count != tx_pkt_ref_count:
                        log.info(line)
                        log.fail('Expected tx_pkt_count is %s and tx_pkt_count is %s'%(tx_pkt_ref_count,tx_pkt_count))
                        raise RuntimeError('Tx Packet count mismatch')
                elif rxParamPattern in line:
                    rx_pkt_count = re.search('\S+\s+:\s+(\S+)\s+\S+',line)[1]
                    if not rx_pkt_ref_count:
                        log.info(line)
                        rx_pkt_ref_count = rx_pkt_count
                    if rx_pkt_count != rx_pkt_ref_count:
                        log.info(line)
                        log.fail('Expected rx_pkt_count is %s and rx_pkt_count is %s'%(rx_pkt_ref_count,rx_pkt_count))
                        raise RuntimeError('Rx Packet count mismatch')
                else:
                    continue
            log.success('tx_pkt_count is %s and rx_pkt_count is %s for subPortList %s'%(tx_pkt_count,rx_pkt_count,subPortList))



@logThis
def run_pcie_dma_test(loopCount=1000):
    cmd = "dsh -c 'loop %s \"tr 500\"'"%loopCount
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=180)
    time.sleep(2)
    cmd = 'dsh -c "tl hmi"'
    res = send_cmd(cmd,promptStr=var.sdkBCMPrompt,timeout=120)
    time.sleep(2)
    stat=re.search('Packet DMA\s+\|\s+\d+\|\s*(\d+)\|\s*(\d+)',res)
    if stat.group(1) == stat.group(2):
        log.success("PCIE packet DMA test pass for loop count %s"%loopCount)
    else:
        log.fail("PCIE packet DMA test failed for loop count %s"%loopCount)
        raise RuntimeError("PCIE packet DMA test failed for loop count %s"%loopCount)

@logThis
def remote_shell_test():
    cmd = 'ps -p `pidof bcm.user`'
    res = exec_cmd(cmd)
    if re.search('error',res):
        raise RuntimeError('Process bcm.user does not exist')
    else:
        for line in res.split('\n'):
            pid = re.match('\d+',line.strip())
            if pid:
                log.info('bcm.user process exists and pid is {0}'.format(pid.group(0)))
                break
        if not pid.group(0):
            raise RuntimeError('Could not fetch the pid of bcm.user process')
    cmd = './cls_shell ps'
    res = send_cmd(cmd,promptStr=var.hostPrompt,timeout=120)
    time.sleep(2)
    res = res.split('\n')
    import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    portPrefix=var.portMap[var.native_mode]['prefix']
    numPorts=var.portMap[var.native_mode]['numPorts']
    for num in range(numPorts):
        port=portPrefix+str(num)
        check_port_status(mode=mode,status=status,port=port,res=res)
    
