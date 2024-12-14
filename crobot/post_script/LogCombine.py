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

"""
Usage: put this file under any direction(generally under workspace of jenkins server, and triggered by Master Job, e.g. CR_master_job) and execute:
python3 LogCombine.py minipack2 output_files
get the result under direction 'combine_log'
"""

import os
import subprocess
import re
import yaml
import sys
import datetime

PROJECT_MP2 = 'minipack2'
PROJECT_CR = 'cloudripper'
PROJECT_400C = 'wedge400c'

REBOT_CMD = "/usr/local/bin/rebot"
cur_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = ''
project = ''  # minipack2 or cloudripper/wedge400c
date_str = ''
image_info_file = ''
log_file_name = ''
report_file_name = ''
workspace = ''
job_paths = ''

tag_stats_header = """'<table class="statistics" id="tag-stats"><thead><tr>' +"""
suite_stats_header = """'<table class="statistics" id="suite-stats"><thead><tr>' +"""
tag_stats_title = """'<th class="stats-col-name">Statistics by Tag</th>' + statHeaders +"""
suite_stats_title = """'<th class="stats-col-name">Statistics by Suite</th>' + statHeaders +"""

ver_function = '''function addVersionInfo() {
    $.tmpl('swVersionTableTemplate').insertAfter($('#header'));
}

'''

def combine_log():
    os.system('rm -fr ' + log_dir)
    os.system('mkdir -p ' + log_dir)
    cmd = REBOT_CMD + " -d " + log_dir + " -o output.xml" +  " -N '{} Combine'".format(project.capitalize())\
          + " -l {}".format(log_file_name) + ' -r {}'.format(report_file_name)

    outputs = job_paths.split()
    # start_num = 3 if project == PROJECT_400C else 1
    # if project == PROJECT_MP2:
    #     unit_count = 24
    # else:
    #     unit_count = 31
    #
    # for i in range(start_num, unit_count):
    #     if project == PROJECT_400C and i in [14, 15, 16]:
    #         continue
    #     try:
    #         path = '%s/%s-bmc-crobot-test-d1-%02d/LOG/output.xml' % (workspace, project, i)
    #         outputs.append(path)
    #         path = '%s/%s-diag-crobot-test-d1-%02d/LOG/output.xml' % (workspace, project, i)
    #         outputs.append(path)
    #         path = '%s/%s-sdk-crobot-test-d1-%02d/LOG/output.xml' % (workspace, project, i)
    #         outputs.append(path)
    #         path = '%s/%s-system-crobot-test-d1-%02d/LOG/output.xml' % (workspace, project, i)
    #         outputs.append(path)
    #     except Exception as err:
    #         print(str(err))
    #         continue
    # print(outputs)

    while True:
        out = subprocess.getoutput(cmd + ' ' +  ' '.join(outputs))
        pattern = r"\[ ERROR \] Reading XML source '(.*?)' failed"
        print(out)
        match = re.search(pattern, out)
        if match:
            print("invalid output: %s \r\n" %str(match.group(1).strip()))
            outputs.remove(match.group(1).strip())
        else:
            print("Combine log successfully !")
            break


def adjust_log():
    report_file = os.path.join(log_dir, report_file_name)
    log_file = os.path.join(log_dir, log_file_name)
    adjust_file(report_file)
    adjust_file(log_file)


def adjust_file(report_file):
    file_data = ''
    with open(report_file, "r", encoding="utf-8") as f:
        for line in f:
            if tag_stats_header in line:
                line = line.replace(tag_stats_header, suite_stats_header)
            elif tag_stats_title in line:
                line = line.replace(tag_stats_title, suite_stats_title)
            elif suite_stats_header in line:
                line = line.replace(suite_stats_header, tag_stats_header)
            elif suite_stats_title in line:
                line = line.replace(suite_stats_title, tag_stats_title)
            file_data += line
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(file_data)
    print('adjust file {} completed'.format(report_file))


def tar_file():
    os.chdir(log_dir)
    os.system('zip -q  {}_combine_log_{}.zip {} {}'.format(project, date_str, log_file_name, report_file_name))

def insert_version_info():
    with open('{}/{}-bmc-crobot-test-d1-05/SwImages.yaml'.format(workspace, project), 'r', encoding="utf-8") as file:
        string = file.read()
        image_dict = yaml.load(string)
    bmc_ver = image_dict['BMC']['newVersion']
    bios_ver = image_dict['BIOS']['newVersion']
    diag_ver = image_dict['DIAG']['newVersion']
    sdk_ver = image_dict['SDK']['newVersion']

    version_tb = f'''<script type="text/x-jquery-tmpl" id="swVersionTableTemplate">
  <h2>Software Versions</h2>
  <table class="details">
    <tr>
      <th>BMC:</th>
      <td>{bmc_ver}</td>
    </tr>
    <tr>
      <th>BIOS:</th>
      <td>{bios_ver}</td>
    </tr>
    <tr>
      <th>DIAG:</th>
      <td>{diag_ver}</td>
    </tr>
    <tr>
      <th>SDK:</th>
      <td>{sdk_ver}</td>
    </tr>
  </table>
</script>

'''

    report_file = os.path.join(log_dir, report_file_name)
    file_data = ''
    with open(report_file, "r", encoding="utf-8") as f:
        for line in f:
            if re.search(r'id="totalStatisticsRowTemplate"', line):
                print('find totalStatisticsRowTemplate')
                file_data += version_tb
            if 'addSummary(topsuite);' in line:
                file_data += '    addVersionInfo();\n'
            if 'function addSummary(topsuite)' in line:
                file_data += ver_function
            file_data += line
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(file_data)
    print('insert version table completed.')

if __name__ == '__main__':
    project = sys.argv[1]
    job_paths = sys.argv[2]
    print('project: ', project)
    log_dir = os.path.join(cur_dir, '{}_combine_log'.format(project))
    workspace = '/home/svt_home/jenkins/workspace' if project == PROJECT_400C else '/var/lib/jenkins/workspace'
    upload_task = 'CR_uploadfile2gdrive' if project == PROJECT_CR else 'uploadfile2gdrive'
    upload_output = os.path.join(workspace, upload_task, 'LOG/output.xml')
    print('upload_output: ', upload_output)
    job_paths = job_paths.replace(upload_output, '')
    print('job_paths: ', job_paths)
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')
    image_info_file = '{}_software_versions.txt'.format(project)
    log_file_name = "{}_combine_log_{}.html".format(project, date_str)
    report_file_name = "{}_combine_report_{}.html".format(project, date_str)

    combine_log()
    adjust_log()
    insert_version_info()
    tar_file()
    exit(0)
