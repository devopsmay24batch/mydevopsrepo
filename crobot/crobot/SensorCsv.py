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
import csv
import re
import Logger as log

class SensorCsv:
    sensorDict = {}
    SENSOR_NAME = 'Sensor Name'
    SENSOR_TYPE = 'Sensor Type'
    UNIT = 'unit'
    THRESHOLD_S0 = 'HW Target Value under S0'
    THRESHOLD_S5 = 'HW Target Value under S5'
    UCR = 'UCR'
    UNC = 'UNC'
    UNR = 'UNR'
    LCR = 'LCR'
    LNC = 'LNC'
    LNR = 'LNR'
    NA_VALUE = 'NA'
    VARIANCE = 0.99
    ALLOW_DIFF = 0.006

    def __init__(self):
        self.sensorConfig = '../config/SensorConfig.csv'

    def getSensorDict(self):
        log.debug('Entering procedure getSensorDict : %s\n '%(str(locals())))
        self.sensorDict = self.csvTodict(self.sensorConfig)
        return self.preProcessSensorDict(self.sensorDict)

    def csvTodict(self, variables_file):
        log.debug('Entering procedure csvTodict : %s\n '%(str(locals())))
        # Open variable-based csv, iterate over the rows and map values to a nested dictionaries containing key/value pairs
        f = open(variables_file, 'rt')
        try:
            reader = csv.DictReader(f, restval='NA')
            all_dict = {}
            for line in reader:
                dict_line = dict(line)
                key = dict_line.pop(self.SENSOR_NAME)
                all_dict[key] = dict_line
            return all_dict
        except Exception as err:
            log.fail(str(err))
            raise RuntimeError("Fail to read csv file (%s) to dict"%(variables_file))
        finally:
            f.close()

    ### convert threshold to float and re-format of NA
    def preProcessSensorDict(self, input_dict):
        log.debug('Entering procedure preProcessSensorDict : %s\n '%(str(locals())))
        p1 = r'^N\/?-?A-?'
        key_list = [self.UCR, self.UNC, self.UNR, self.LCR, self.LNC, self.LNR]
        for s_name, s in input_dict.items():
            ### convert sensor name to upper letter
            if not s_name.isupper():
                input_dict[s_name.upper().strip()] = input_dict.pop(s_name)
        for s_name, s in input_dict.items():
            for key in key_list:
                ### convert N/A, na, n/a to NA
                if (s[key] == '') or (re.search(p1, s[key], re.IGNORECASE) and s[key] != self.NA_VALUE):
                    input_dict[s_name].update({key : self.NA_VALUE})
                ### convert string to float if value is number
                else:
                    input_dict[s_name].update({key : self.string_to_float(s[key])})
        return input_dict

    def string_to_float(self, s):
        try:
            return float(s)
        except ValueError:
            return s

    ### filter sensor by Sensor Type
    def getSensorDictByType(sensor_type='all'):
        log.debug('Entering procedure getSensorDictByType : %s\n '%(str(locals())))
        SensorObj = SensorCsv()
        SensorObj.getSensorDict()
        if sensor_type == 'all':
            return SensorObj.sensorDict
        return {k:v for k,v in SensorObj.sensorDict.items() if v[SensorObj.SENSOR_TYPE].lower() == sensor_type.lower()}
