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
import re, os
import YamlParse
from Server import Server
import Logger as log

class SwImage:
    MASTER = 'master'
    SLAVE = 'slave'
    BMC = 'BMC'
    BIOS = 'BIOS'
    CPLD = 'CPLD'
    MCB = 'MCB'
    SCM = 'SCM'
    SMB = 'SMB'
    SMB1 = 'SMB1'
    SMB2 = 'SMB2'
    PWR = 'PWR'
    BASE_CPLD = 'BASE_CPLD'
    COME_CPLD = 'COME_CPLD'
    SWITCH_CPLD = 'SWITCH_CPLD'
    FAN_CPLD = 'FAN_CPLD'
    FPGA = 'FPGA'
    BIC = 'BIC'
    TH3 = 'TH3'
    TH5 = 'TH5'
    UDEV = 'UDEV'
    BSP = 'BSP'
    IOB = 'IOB'
    OOB = 'OOB'
    SCM = 'SCM'
    TPM = 'TPM'
    BIOS_VER = 'BIOS Version'
    BMC_VER = 'BMC Version'
    BIC_VER = 'Bridge-IC Version'
    OS = 'OS'
    KERNEL = 'KERNEL'
    PSU = 'PSU'
    DIAG = 'DIAG'
    DIAG_OS = 'DIAG_OS'
    SDK = 'SDK'
    CIT = 'CIT'
    I210 = 'I210'
    TH4 = 'TH4_PCIE_FLASH'
    PCIE_FLASH_SHAMU = 'PCIE_FLASH_SHAMU'
    FPGA_DRIVER = 'FPGA_DRIVER'
    UBOOT = 'UBOOT'
    ONIE = 'ONIE_INSTALLER'
    BRIXIA_SONIC = 'BRIXIA_SONIC'
    ABERLOUR_DIAG = 'ABERLOUR_DIAG'
    swImages = {}

    def __init__(self, imageDict, device = 'DUT'):
        self.imageDict = imageDict
        self.name = imageDict['name']
        self.hostImageDir = imageDict['hostImageDir']
        self.isAutoBuild = imageDict['isAutoBuild']
        self.imageInfoFile = imageDict['imageInfoFile']
        self.localImageDir = imageDict['localImageDir']
        if self.name in ['BSP']:
            self.oldlocalImageDir = imageDict['oldlocalImageDir']
            self.newlocalImageDir = imageDict['newlocalImageDir']
            self.oldImageZip = imageDict['oldImageZip']
            self.newImageZip = imageDict['newImageZip']
            self.spiUtilScript = imageDict['spiUtilScript']
            self.weUtilScript = imageDict['weUtilScript']
            self.weUtilJson = imageDict['weUtilJson']
            self.libicuuc = imageDict['libicuuc']
            self.libicudata = imageDict['libicudata']
            self.libicui18n = imageDict['libicui18n']
        self.imageServer = imageDict['imageServer']
        self.oldImage = imageDict['oldImage']
        self.newImage = imageDict['newImage']
        self.oldVersion = imageDict['oldVersion']
        self.newVersion = imageDict['newVersion']
        self.currentUpdateVer = {}
        self.hostBaseDir = ''
        self.device = device
        if self.isAutoBuild:
            self.refreshImageInfo()

    def getImageList(self):
        log.debug('Entering procedure getImageList with args : %s\n'%(str(locals())))
        imgList = []
        if self.name in ['BIOS','OOB', 'TH3', 'BIC', 'ONIE_INSTALLER', 'TH5', 'UDEV', 'IOB', 'MCB', 'SCM', 'SMB', 'SMB1', 'SMB2', 'PWR', 'COME_CPLD']:
            imgList.append(self.oldImage)
            imgList.append(self.newImage)
        if self.name in ['BSP']:
            imgList.append(self.oldImage)
            imgList.append(self.oldImageZip)
            imgList.append(self.newImage)
            imgList.append(self.newImageZip)
            imgList.append(self.spiUtilScript)
            imgList.append(self.weUtilScript)
            imgList.append(self.weUtilJson)
            imgList.append(self.libicuuc)
            imgList.append(self.libicudata)
            imgList.append(self.libicui18n)
        elif self.name in ['TPM', 'CIT']:
            imgList.append(self.oldImage)
        elif self.name in ['CPLD', 'PSU']:
            imgList.append(self.oldImage.values())
            imgList.append(self.newImage.values())
        elif self.name in [SwImage.BMC, SwImage.DIAG]:
            if self.isAutoBuild:
                self.refreshImageInfo()
            if self.name == SwImage.BMC:
                imgList.append(self.oldImage)
            imgList.append(self.newImage)
        elif self.name in [SwImage.FPGA]:
            if isinstance(self.newImage, dict):
                imgList = list(self.oldImage.values()) + list(self.newImage.values())
            else:
                imgList.append(self.oldImage)
                imgList.append(self.newImage)
        else:
            imgList.append(self.newImage)
        return imgList

    def refreshImageInfo(self):
        log.debug('Entering procedure refreshImageInfo with args : %s\n'%(str(locals())))
        serverObj = Server.getServer(self.imageServer)
        import CommonLib
        ret = CommonLib.get_file_by_scp(serverObj.managementIP, serverObj.username, serverObj.password,
                                        self.hostImageDir, self.imageInfoFile, './')
        imageInfofile_with_path = os.path.join(self.hostImageDir, self.imageInfoFile)
        if ret == 1:
            raise RuntimeError("can't get image info file: {} !".format(imageInfofile_with_path))
        imageDict = YamlParse.parse('./' + self.imageInfoFile)
        self.newImage = imageDict['newImage']
        self.oldImage = imageDict['oldImage']
        self.newVersion = imageDict['newVersion']
        self.oldVersion = imageDict['oldVersion']

    # def parseImages(self, out):
    #     list = []
    #     p1 = r'newImage: (.*),'
    #     p2 = r'oldImage: (.*),'
    #     match = re.search(p1, out)
    #     if match:
    #         list.append(match.group(0).strip())
    #     match = re.search(p2, out)
    #     if match:
    #         list.append(match.group(0).strip())
    #     return list

    @classmethod
    def getSwImage(cls, name):
        log.debug('Entering procedure getSwImage with args : %s\n'%(str(locals())))
        if name in cls.swImages.keys():
            return cls.swImages[name]
        imageInfo = YamlParse.getSwImageInfo()
        imageDict = imageInfo[name]
        cls.swImages[name] = SwImage(imageDict)
        return cls.swImages[name]
