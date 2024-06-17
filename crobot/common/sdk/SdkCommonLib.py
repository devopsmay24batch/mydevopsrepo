import re
import time
import traceback
try:
    import DeviceMgr
    import Logger as log
    import CommonLib
    import parserSDKLibs
    from Sdk_variable import *
    from Decorator import *
except Exception as err:
    log.cprint(err)
    log.cprint(traceback.format_exc())

device = DeviceMgr.getDevice()

@logThis
def check_port_ber(output,port_pattern, port_ber_tolerance):
    device.log_debug("Entering procedure check_port_BER.\n")
    fail_port = []
    match_flag = 0
    for line in output.splitlines():
        match = re.search(port_pattern, line)
        if match:
            match_flag = 1
            BER_value = float(match.group(1))
            if BER_value >= port_ber_tolerance:
                fail_port.append(str(line))
        if re.search('LossOfLock', line):
            fail_port.append(str(line))
    if fail_port:
        device.raiseException("{} failed with ports:{}".format('check_port_ber', fail_port))
    elif match_flag == 0:
        device.raiseException("Command failed with didn't match ports information")
    else:
        device.log_success("{}".format('check_port_ber'))


@logThis
def checkPktCounter():
    due_prompt = 'XLMIB_TBYT'
    finish_prompt = "{}[\s\S]+{}".format(due_prompt, BCM_promptstr)
    output = device.sendCmdRegexp(show_c_cmd, finish_prompt, timeout=300)
    # output = device.executeCommand(show_c_cmd, BCM_promptstr, timeout=300)
    log.cprint(output)
    lines = str(output).splitlines()
    linesIter = iter(lines)

    findMismatch = False

    def parsePktCounter(line, linesIter, txPattern, rxPattern):
        res = re.search(txPattern, line)
        if res:
            pktCount = res.group(2)
            log.info('pktCount: ' + pktCount)
            nextLine = next(linesIter, None)
            if nextLine is None:
                raise RuntimeError('Can not find the next line of Line: \n'.format(line))
            res = re.search(rxPattern, nextLine)
            if res:
                if pktCount != res.group(2):
                    nonlocal findMismatch
                    findMismatch = True
                    log.info('#########These two lines mismatch: ########## \n')
                    log.info('Line 1 : \n'.format(line))
                    log.info('Line 2 : \n'.format(nextLine))
            else:
                raise RuntimeError('Can not find pattern ' + rxPattern)

    while True:
        line = next(linesIter, None)
        if not line:
            break
        res = re.search(tx_rx_pkt_patterns[0], line)
        if not res:
            continue

        parsePktCounter(line, linesIter, tx_rx_pkt_patterns[0], tx_rx_pkt_patterns[1])
        line = next(linesIter).strip()
        parsePktCounter(line, linesIter, tx_rx_pkt_patterns[2], tx_rx_pkt_patterns[3])
        line = next(linesIter).strip()
        parsePktCounter(line, linesIter, tx_rx_pkt_patterns[4], tx_rx_pkt_patterns[5])
        line = next(linesIter).strip()
        parsePktCounter(line, linesIter, tx_rx_pkt_patterns[6], tx_rx_pkt_patterns[7])
        line = next(linesIter).strip()
        parsePktCounter(line, linesIter, tx_rx_pkt_patterns[8], tx_rx_pkt_patterns[9])

    if findMismatch:
        raise RuntimeError('Find mismatch lines !')
    else:
        log.success('checkPktCounter successfully.')


@logThis
def stopBcmProcess():
    output = device.executeCmd(check_bcm_user, timeout=5)
    lines = output.splitlines()
    for line in lines:
        if re.search(r'bcm.user -y|\[bcm.user\]', line):
            w = re.findall(r'\w+', line)
            device.sendCmd('kill -9 ' + w[1])
            break
    time.sleep(10)


@logThis
def findBcmProcess():
    output = device.executeCmd(check_bcm_user, timeout=5)
    lines = output.splitlines()
    for line in lines:
        if re.search('bcm.user -y', line):
            return True
    return False

@logThis
def checkOutput(output, patterns=[""], timeout=60, line_mode=True, is_negative_test=False, remark=""):
    passCount = 0
    patternNum = len(patterns)
    log.debug('output = ***%s***' % output)

    pass_p = []
    pattern_all = []
    for i in range(0, patternNum):
        p_pass = patterns[i]
        pattern_all.append(p_pass)
        if line_mode:
            for line in output.splitlines():
                match = re.search(p_pass, line)
                if match:
                    if is_negative_test:
                        passCount -= 1
                    else:
                        passCount += 1
                    pass_p.append(p_pass)
                    break
        else:
            match = re.search(p_pass, output, re.M)
            if match:
                if is_negative_test:
                    passCount -= 1
                else:
                    passCount += 1
                pass_p.append(p_pass)

    if is_negative_test:
        passCount += patternNum
    mismatch_pattern = set(pattern_all)-set(pass_p) if not is_negative_test else set(pass_p)
    log.debug('passCount = %s' %passCount)
    log.debug('patternNum = %s' %patternNum)
    ret_code = 0
    if remark:
        description = remark
    else:
        description = "All patterns "
    if passCount == patternNum:
        ret_code = 1
        log.success('%s is PASSED\n' %description)
    else:
        log.fail('Exiting checkOutput with result FAIL, {} fail with pattern: {}'.format(remark, mismatch_pattern))

    return ret_code

@logThis
def checkHmonTemperature():
    output = device.executeCommand(get_hmon_temperature_cmd, BCMLT_prompt, timeout=100)
    checkOutput(output, patterns=fail_pattern, is_negative_test=True)
    parserSDKLibs.PARSE_port_value_range_check(output, hmon_temperature_pattern, valid_value_range=(0, max_temperature))