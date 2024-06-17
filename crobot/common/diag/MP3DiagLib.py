
import re
import time
import Logger as log
try:
    from Device import Device
    import DeviceMgr
    import Const
    import CommonLib
except Exception as err:
    log.cprint(str(err))


def check_login():
    log.success("Successfully logged into diag ")

    

