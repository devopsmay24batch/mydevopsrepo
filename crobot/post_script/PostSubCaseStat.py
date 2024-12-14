#!/usr/bin/env python
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
"""Post-script for collecting Sub-case statistics

Usage:  PostSubCaseStat.py input-xml input-html [output-html]

This script reads status from suite, tests and keywords and collect status only
keyword name 'Sub-Case', and group them by test case. Then add these data into
log.html template by adding new 3 columns into html, then writes them into html
file. If the html output file is not given, its name is the same as the input file.

Requirement: pip install beautifulsoup4

"""

import os.path
import sys
import re
import json
from robot.result import ExecutionResult
from bs4 import BeautifulSoup
#### ref: https://www.crummy.com/software/BeautifulSoup/bs4/doc

SUB_CASE_KW = 'CommonResource.Sub-Case'
TEST_FAIL_MSG = [
    'Critical failure occurred', ### critical failed, exit on failure
    'Parent suite setup failed', ### setup suite fail
    'Setup failed'               ### setup test fail
]
CRITICAL_TAG = 'critical'
NOT_EXIT_TAG = 'NOT robot:exit'
CRITICAL_TESTS = "Critical Tests"
ALL_TESTS = "All Tests"
SUB_TOTAL = 'subtotal'
SUB_PASS = 'subpass'
SUB_FAIL = 'subfail'

pass_sc = 0
fail_sc = 0
total_keywords = 0
total_pass_sc = 0
total_fail_sc = 0
pass_crit = 0
fail_crit = 0
sc_stats = {}

def process_file(infile):
    ### now only support 1 file per 1 test suite
    suite = ExecutionResult(infile).suite
    process_suite(suite)

def process_suite(suite):
    for test in suite.tests:
        process_test(test)

    sc_stats[ALL_TESTS] = {}
    sc_stats[ALL_TESTS][SUB_TOTAL] = total_pass_sc + total_fail_sc
    sc_stats[ALL_TESTS][SUB_PASS] = total_pass_sc
    sc_stats[ALL_TESTS][SUB_FAIL] = total_fail_sc

    sc_stats[CRITICAL_TESTS] = {}
    sc_stats[CRITICAL_TESTS][SUB_TOTAL] = pass_crit + fail_crit
    sc_stats[CRITICAL_TESTS][SUB_PASS] = pass_crit
    sc_stats[CRITICAL_TESTS][SUB_FAIL] = fail_crit

    sc_stats[CRITICAL_TAG] = sc_stats[CRITICAL_TESTS].copy()
    sc_stats[NOT_EXIT_TAG] = sc_stats[ALL_TESTS].copy()
    sc_stats[suite.name] = sc_stats[ALL_TESTS].copy()

def process_test(test):
    if test.status == 'FAIL' and \
        (any(x in test.message for x in TEST_FAIL_MSG)):
        global sc_stats
        sc_stats[test.name] = {}
        sc_stats[test.name][SUB_TOTAL] = 0
        sc_stats[test.name][SUB_PASS] = 0
        sc_stats[test.name][SUB_FAIL] = 0
        return
    for kw in test.keywords:
        process_keyword(kw)

def process_keyword(kw):
    if kw is None:
        return
    global total_keywords
    global total_pass_sc
    global total_fail_sc
    global pass_sc
    global fail_sc
    global pass_crit
    global fail_crit
    global sc_stats
    if kw.type == "kw":
        if kw.parent.name in kw.parent.tags:
            if kw.parent.name not in sc_stats:
                total_keywords = 0
                pass_sc = 0
                fail_sc = 0
                sc_stats[kw.parent.name] = {}
            if kw.name == SUB_CASE_KW:
                total_keywords += 1
                if kw.status == "PASS":
                    pass_sc += 1
                    total_pass_sc += 1
                    if CRITICAL_TAG in kw.parent.tags:
                        pass_crit += 1
                else:
                    fail_sc += 1
                    total_fail_sc += 1
                    if CRITICAL_TAG in kw.parent.tags:
                        fail_crit += 1
                sc_stats[kw.parent.name][SUB_TOTAL] = total_keywords
                sc_stats[kw.parent.name][SUB_PASS] = pass_sc
                sc_stats[kw.parent.name][SUB_FAIL] = fail_sc

def edit_log_html(infile, outfile):
    ### load the file
    with open(infile) as inf:
        txt = inf.read()
        soup = BeautifulSoup(txt, 'html.parser')

    ### modify window.output["stats"] raw data
    regex1 = r'window\.output\["stats"\] = '
    output = soup.find(string=re.compile(regex1))
    post_output = re.sub(regex1, '', output)
    post_output = re.sub(';', '', post_output)
    res = json.loads(post_output)
    for i in range(len(res)):
        for j in range(len(res[i])):
            if  res[i][j]['label'] in sc_stats:
                if SUB_TOTAL in sc_stats[res[i][j]['label']]:
                    res[i][j][SUB_TOTAL] = sc_stats[res[i][j]['label']][SUB_TOTAL]
                    res[i][j][SUB_PASS] = sc_stats[res[i][j]['label']][SUB_PASS]
                    res[i][j][SUB_FAIL] = sc_stats[res[i][j]['label']][SUB_FAIL]
                else:
                    print('%s EXIT: Test cases does not contain %s, Sub Case statistics will be not generated' \
                        %(sys.argv[0], SUB_CASE_KW))
                    return
    result = '\nwindow.output["stats"] = '
    result += json.dumps(res)
    result += ';'
    soup.find(string=re.compile(regex1)).replace_with(result)

    ### modify statistics table
    stat_fn = r'addStatistics\(\) \{'
    output = soup.head.find(string=re.compile(stat_fn))
    css_stats = "stats-col-elapsed"
    table_width = '85'
    ###### modify function addStatistics()
    old_th = "        '<th class=\"stats-col-graph\">Pass / Fail</th>';"
    new_th = f'''        '<th class="stats-col-graph">Pass / Fail</th>' +
        '<th class="{css_stats}">Total Executed Sub Case</th>' +
        '<th class="{css_stats}">Pass Sub Case</th>' +
        '<th class="{css_stats}">Fail Sub Case</th>';'''
    result = output.replace(old_th, new_th)
    ###### modify function renderNoTagStatTable()
    old_notag = r"\'</td>\' \+\n      \'</tr>"
    new_notag = f'''\'</td>' +
        '<td class="{css_stats}"></td>' +
        '<td class="{css_stats}"></td>' +
        '<td class="{css_stats}"></td>' +
    '</tr>'''
    result = re.sub(old_notag, new_notag, result)
    ###### modify template statColumnsTemplate
    old_td = r"'</td>'\n"
    new_td = f'''\'</td>' +
    '<td class="{css_stats}">${{{SUB_TOTAL}}}</td>' +
    '<td class="{css_stats}">${{{SUB_PASS}}}</td>' +
    '<td class="{css_stats}">${{{SUB_FAIL}}}</td>'
    '''
    result = re.sub(old_td, new_td, result)
    soup.head.find(string=re.compile(stat_fn)).replace_with(result)
    ###### modify .statistics css (table width)
    css_fn = r'\n\.statistics \{\n    width: (\d+)em'
    output = soup.head.find(string=re.compile(css_fn))
    new_css = f'''\n.statistics {{
    width: {table_width}em'''
    result = re.sub(css_fn, new_css, output)
    soup.head.find(string=re.compile(css_fn)).replace_with(result)

    ### save the file again
    with open(outfile, "w") as outf:
        outf.write(str(soup))
    print('New Log: %s'%os.path.abspath(outhtml))

if __name__ == '__main__':
    inxml = sys.argv[1]
    inhtml = sys.argv[2]
    try:
        outhtml = sys.argv[3]
    except IndexError:
        outhtml = inhtml

    process_file(inxml)
    edit_log_html(inhtml, outhtml)
