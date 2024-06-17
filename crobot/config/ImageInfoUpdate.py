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

## this file will be putted under the parent dir of image files putted
## e.g /home/automation/Auto_Test/automation/FB-Wedge400C/autotest
## Jenkins task will call this script as: python3 ImageInfoUpdate.py newImageName

import yaml
import sys
import re
from subprocess import Popen,PIPE

NEW_IMAGE = 'newImage'
OLD_IMAGE = 'oldImage'
NEW_VER = 'newVersion'
OLD_VER = 'oldVersion'

def execute_local_cmd(cmd, timeout=10):
    print('\r\nexecute_local_cmd cmd[%s]' % cmd)
    output = ''
    errs = ''
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, encoding='latin-1')
    try:
        # wait for process to complete
        output, errs = proc.communicate(timeout=timeout)
        print(output)
    except Exception as err:
        # clean up if error occurs
        proc.kill()
        raise RuntimeError(str(err))
    print('\r\nSuccessfully execute_local_cmd cmd: [%s]' % cmd)
    return output

def main(newImage):
    filename = ''
    newVer = ''
    if 'migaloo-openbmc' in newImage: # bmc image of migaloo
        filename = './BMC/ImageInfo.yaml'
        p = r'U-Boot\s\d+\.\d+\s\w+-cl-(.*) \(.*'
        cmd = 'strings  ./BMC/' + newImage + ' | grep U-Boot | grep 20'
        output = execute_local_cmd(cmd)
        newVer = re.search(p, output).group(1)
        if newVer.startswith('v'):
            newVer = newVer.lstrip('v')
    elif 'flash-' in newImage or 'openbmc' in newImage: # bmc image of wedge400
        filename = './BMC/ImageInfo.yaml'
        p = r'U-Boot\s\d+\.\d+\s\w+-(.*) \(.*'
        cmd = 'strings  ./BMC/' + newImage + ' | grep U-Boot | grep 20'
        output = execute_local_cmd(cmd)
        newVer = re.search(p, output).group(1)
        if newVer.startswith('v'):
            newVer = newVer.lstrip('v')
    elif 'migaloo_diag' in newImage: # diag image of wedge400
        filename = './DIAG/ImageInfo.yaml'
        p = r'diag_([0-9.]+)_20.*?\.deb'
        newImage = newImage.split("/")[-1]
        newVer = re.search(p, newImage).group(1)
    elif 'AS14-40D' in newImage: # diag image of wedge400
        filename = './BIOS/ImageInfo.yaml'
        p = r'AS14-40D-F.([0-9.]+).bin'
        newImage = newImage.split("/")[-1]
        newVer = re.search(p, newImage).group(1)
    elif 'R3174' in newImage: # diag image of wedge400
        filename = './SDK/ImageInfo.yaml'
        p = r'R3174-J0005-01_(v[0-9.]+)_Migaloo_SDK.zip'
        newImage = newImage.split("/")[-1]
        newVer = re.search(p, newImage).group(1)
    elif 'Diag' in newImage: # diag image of wedge400
        filename = './DIAG/ImageInfo.yaml'
        #p = r'diag_([0-9.]+)_20.*?\.rpm'
        p = r'Diag-([0-9.]+)-.*?\.rpm'
        newImage = newImage.split("/")[-1]
        newVer = re.search(p, newImage).group(1)
    else:
        return

    file = open(filename, 'r', encoding="utf-8")
    str = file.read()
    file.close()
    imageDict = yaml.load(str)

    doc = None
    with open(filename) as f:
        doc = yaml.load(f)
        doc[OLD_IMAGE] = imageDict[NEW_IMAGE]
        doc[OLD_VER] = imageDict[NEW_VER]
        doc[NEW_IMAGE] = newImage
        doc[NEW_VER] = newVer

    with open(filename, 'w') as f:
        yaml.dump(doc, f)

if __name__ == '__main__':
    main(sys.argv[1])
