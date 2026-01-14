"""
 _____            _   _ _                              ____    _____  ___
|  ___|__  _ __  | |_| | | _____ ___  _ __ ___  __   _|___ \  |___ / / _ \   _
| |_ / _ \| '__| | __| | |/ / __/ _ \| '__/ _ \ \ \ / / __) |   |_ \| | | |_| |_
|  _| (_) | |    | |_| |   < (_| (_) | | |  __/  \ V / / __/ _ ___) | |_| |_   _|
|_|  \___/|_|     \__|_|_|\_\___\___/|_|  \___|   \_/ |_____(_)____(_)___/  |_|

This main.py requires tlkcore version >= v2.3.0

Please make sure you have the correct version installed.

"""

import argparse
import json
import logging
import os
from pathlib import Path
import platform
import sys
import time
import traceback

service = None
root_path = Path(__file__).absolute().parent

# Please setup path of tlkcore libraries to environment variables,
# here is a example to search from 'lib/' or '.'
prefix = "lib/"
lib_path = os.path.join(root_path, prefix)
if os.path.exists(lib_path):
    sys.path.insert(0, os.path.abspath(lib_path))
elif os.path.exists("tlkcore") and os.path.isdir("tlkcore"):
    print("Importing from source code")
else:
    print("Importing from Python site-packages")
    # If you want to import from Python site-packages, please remove the following line
    # sys.path.insert(0, os.path.abspath(root_path))

def check_ex_files(directory, extension=".so"):
    for file in os.listdir(directory):
        if file.endswith(extension):
            return True
    return False

try:
    from tlkcore import (
        TLKCoreService,
        DevInterface,
        RetCode,
        RFMode,
        UDState,
        UDMState,
        BeamType,
        UD_REF,
        UD_LO_CONFIG,
        RIS_Dir,
        RIS_ModuleConfig,
        CellRFMode,     # For CloverCell series AiP
        POLARIZATION    # For CloverCell series AiP
    )
except Exception as e:
    myos = platform.system()
    d = os.path.join(sys.path[0], 'tlkcore',)
    if ((myos == 'Windows' and check_ex_files(d), ".so")
        or (myos == 'Linux' and check_ex_files(d), ".pyd")):
        print(f"[Main] Import the wrong library for {myos}")
    else:
        print("[Main] Import path has something wrong")
        print(sys.path)
    traceback.print_exc()
    os._exit(-1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debug.log')),
    ]
)

logger = logging.getLogger("Main")
logger.info("Python v%d.%d.%d (%s) on the %s platform" %(sys.version_info.major,
                                            sys.version_info.minor,
                                            sys.version_info.micro,
                                            platform.architecture()[0],
                                            platform.system()))

class TMYLogFileHandler(logging.FileHandler):
    """Handle relative path to absolute path"""
    def __init__(self, fileName, mode):
        super(TMYLogFileHandler, self).__init__(os.path.join(root_path, fileName), mode)

def getJSONFmt(data:str):
    return json.dumps(data, indent=4, ensure_ascii=False)

def wrapper(*args, **kwarg):
    """It's a wrapper function to help some API developers who can't call TLKCoreService class driectly,
    so developer must define return type if using LabVIEW/MATLAB"""
    global service
    if len(args) == 0:
        logger.error("Invalid parameter: please passing function name and parameters")
        raise Exception
    if service is None:
        service = TLKCoreService(working_root=root_path)
        logger.info("TLKCoreService v%s %s" %(service.version, "is running" if service.running else "can not run"))
        logger.info(sys.path)

    arg_list = list(args)
    func_name = arg_list.pop(0)
    logger.info("Calling dev_func: \'%s()\'with %r and %r" % (func_name, arg_list, kwarg))
    if not hasattr(service, func_name):
        service = None
        msg = "TLKCoreService not support function name: %s()" %func_name
        logger.error(msg)
        raise Exception(msg)

    for i in range(1, len(arg_list)): # skip first for sn
        p = arg_list[i]
        if type(p) is str and p.__contains__('.'):
            try:
                # Parsing and update to enum type
                logger.debug("Parsing: %s" %p)
                str_list = p.split('.')
                type_str = str_list[0]
                value_str = str_list[1]
                f = globals()[type_str]
                v = getattr(f, value_str)
                arg_list[i] = v
            except Exception:
                service = None
                msg = "TLKCoreService scan result parsing failed"
                logger.error(msg)
                raise Exception(msg)

    # Relfect and execute function in TLKCoreService
    ret = getattr(service, func_name)(*tuple(arg_list))
    if not hasattr(ret, "RetCode"):
        return ret
    if ret.RetCode is not RetCode.OK:
        service = None
        msg = "%s() returned: [%s] %s" %(func_name, ret.RetCode, ret.RetMsg)
        logger.error(msg)
        raise Exception(msg)

    if ret.RetData is None:
        logger.info("%s() returned: %s" %(func_name, ret.RetCode))
        return str(ret.RetCode)
    else:
        logger.info("%s() returned: %s" %(func_name, ret.RetData))
        return ret.RetData

def startService(root:str=root_path, direct_connect_info:list=None, dfu_image:str=""):
    """ALL return type from TLKCoreService always be RetType,
    and it include: RetCode, RetMsg, RetData,
    you could fetch service.func().RetData
    or just print string result directly if you make sure it always OK"""
    # You can assign a new root directory into TLKCoreService() to change files and log directory
    if Path(root).exists() and Path(root).absolute() != Path(root_path):
        service_root = root
    else:
        service_root = root_path
    service = TLKCoreService(working_root = service_root)
    logger.info("TLKCoreService v%s %s" %(service.version, "is running" if service.running else "can not run"))

    if not service.running:
        return False

    if isinstance(direct_connect_info, list) and len(direct_connect_info) == 3:
        # For some developers just connect device and the address always constant (static IP or somthing),
        # So we provide a extend init function to connect device driectly without scanning,
        # the parameter address and devtype could fetch by previous results of scanning.
        # The following is simple example, please modify it
        kw = {'sn': direct_connect_info[0], 'address':direct_connect_info[1], 'dev_type':int(direct_connect_info[2]), 'is_custom_calibration': False}
        # Parameter: SN, Address, Devtype
        ret = service.initDev(**kw)
        if ret.RetCode is RetCode.OK:
            kw['service'] = service
            kw['dfu_image'] = dfu_image
            testDevice(**kw)
    else:
        # Please select or combine your interface or not pass any parameters: service.scanDevices()
        interface = DevInterface.ALL #DevInterface.LAN | DevInterface.COMPORT
        logger.info("Searching devices via: %s" %interface)
        ret = service.scanDevices(interface=interface)

        scan_dict = service.getScanInfo().RetData
        i = 0
        for sn, (addr, devtype, in_dfu) in list(scan_dict.items()):
            i+=1
            logger.info("====== Dev_%d: %s, %s, %d, %r ======" %(i, sn, addr, devtype, in_dfu))

            # Init device, the first action for device before the operations
            if service.initDev(sn, is_custom_calibration=False).RetCode is not RetCode.OK and not in_dfu:
                continue
            testDevice(sn, service, dfu_image, addr, devtype, in_dfu)

    return True

def testDevice(sn, service, dfu_image:str="", address:str="", dev_type:int=0, in_dfu=False):
    """ A simple query operations to device """
    dev_name = service.getDevTypeName(sn)
    # print(dev_name)

    fw_ver = None
    hw_ver = None
    loader_ver = None
    if in_dfu:
        logger.info("Device in DFU mode, you can skip error log for previous connection failed")
    else:
        logger.info("SN: %s" %service.querySN(sn))
        fw_ver = service.queryFWVer(sn).RetData
        hw_ver = service.queryHWVer(sn).RetData
        logger.info("FW ver: %s" %fw_ver)
        logger.info("HW ver: %s" %hw_ver)

    # Process device testing, runs a device test function likes testPD, testBBox, testUD ...etc
    # 1. parameters
    kw = {}
    kw['sn'] = sn
    kw['service'] = service

    # 2. Test function name
    if len(dfu_image) > 0:
        while not in_dfu:
            ret = service.queryLoaderVer(sn)
            if ret.RetCode is not RetCode.OK:
                logger.warning("Error to query bootloader version: \'%s\', maybe it's in DFU mode" %ret.RetMsg)
                in_dfu = True
                break
            loader_ver = ret.RetData
            logger.info(f"[DFU] Bootloader version: {loader_ver}")
            break

        # DFU function
        kw['dfu_image'] = dfu_image
        kw['dfu_dev_info'] = {
                            "sn": sn,
                            "address": address,
                            "dev_type": dev_type,
                            "in_dfu": in_dfu,
                            "fw_ver": fw_ver,
                            "hw_ver": hw_ver,
                            "loader_ver": loader_ver
                        }
        f = globals()["startDFU"]
    else:
        if dev_type == 32:
            dev_name = "BBoxDuo"
        elif 'BBoard' in dev_name:
            dev_name = "BBoard"
        elif 'BBox' in dev_name:
            dev_name = "BBox"
        f = globals()["test"+dev_name]

    # Start testing
    f(**kw)

    service.DeInitDev(sn)

""" ----------------- Test examples for TMY devices ----------------- """

__caliConfig = {
    "0.1GHz": {
            "lowPower": -35,
            "lowVolt": 34.68,
            "highPower": -5,
            "highVolt": 901.68
        },
    "0.3GHz": {
            "lowPower": -36,
            "lowVolt": 34.68,
            "highPower": -5,
            "highVolt": 901.68
        },
    "0.5GHz": {
            "lowPower": -36,
            "lowVolt": 109.98,
            "highPower": -5,
            "highVolt": 984.18
        },
    "1GHz": {
            "lowPower": -36,
            "lowVolt": 109.98,
            "highPower": -5,
            "highVolt": 984.18
        },
    "10GHz": {
            "lowPower": -36,
            "lowVolt": 57.6,
            "highPower": -5,
            "highVolt": 950.4
        },
    "20GHz": {
            "lowPower": -36,
            "lowVolt": 40.46,
            "highPower": -5,
            "highVolt": 936.36
        },
    "30GHz": {
            "lowPower": -36,
            "lowVolt": 83.81,
            "highPower": -5,
            "highVolt": 979.71
        },
    "40GHz": {
            "lowPower": -30,
            "lowVolt": 20.65,
            "highPower": -5,
            "highVolt": 787.65
        },
    "43GHz": {
            "lowPower": -28,
            "lowVolt": 20.65,
            "highPower": -5,
            "highVolt": 787.65
        }
}

def testPD(sn, service):
    for freq, config in __caliConfig.items():
        logger.info("Process cali %s: %s" %(freq, service.setCaliConfig(sn, {freq: config})))

    target_freq = 28
    for _ in range(10):
        logger.info("Fetch voltage: %s" %service.getVoltageValue(sn, target_freq))
        logger.info("        power: %s" %service.getPowerValue(sn, target_freq))
    logger.info("Reboot test: %s" %service.reboot(sn))

    while(True):
        try:
            logger.info("power: %s" %(service.getPowerValue(sn, target_freq)))
            time.sleep(0.5)
        except (KeyboardInterrupt, SystemExit):
            print("Detected Ctrl+C")
            break

def testUDBox(sn, service):
    logger.info("PLO state: %r" %service.getUDState(sn, UDState.PLO_LOCK).RetData)
    logger.info("All state: %r" %service.getUDState(sn).RetData)

    # Test example options, you can decide what to test
    testUDState = False
    testUDFreq = True

    if testUDState:
        # Advanced test options for setting UD state, you can decide what to test
        testCH1 = True
        testExt = False
        testOthers = False

        if testCH1:
            # CH1 off/on testing
            logger.info(service.setUDState(sn, 0, UDState.CH1))
            input("Wait for ch1 off")
            logger.info(service.setUDState(sn, 1, UDState.CH1))

        if testExt:
            # Switch 100M reference source to external, then please plug-in reference source
            input("Start to switch reference source to external")
            logger.info(service.setUDState(sn, UD_REF.EXTERNAL, UDState.SOURCE_100M))
            logger.info("PLO state: %r" %service.getUDState(sn, UDState.PLO_LOCK).RetData)

            # Switch 100M reference source to internal
            input("Press to switch reference source to internal")
            logger.info(service.setUDState(sn, UD_REF.INTERNAL, UDState.SOURCE_100M))
            logger.info("PLO state: %r" %service.getUDState(sn, UDState.PLO_LOCK).RetData)

        if testOthers:
            # Other optional switches
            logger.info(service.setUDState(sn, 1, UDState.CH2))
            logger.info(service.setUDState(sn, 1, UDState.OUT_10M))
            logger.info(service.setUDState(sn, 1, UDState.OUT_100M))
            logger.info(service.setUDState(sn, 1, UDState.PWR_5V))
            logger.info(service.setUDState(sn, 1, UDState.PWR_9V))

    if testUDFreq:
        logger.info("Get current freq: %s" %service.getUDFreq(sn))
        # Passing: LO, RF, IF, Bandwidth with kHz
        LO = 24e6
        RF = 28e6
        IF = 4e6
        BW = 1e5
        # A check function
        logger.info("Check harmonic: %r" %service.getHarmonic(sn, LO, IF, BW).RetData)
        # SetUDFreq also includes check function
        ret = service.setUDFreq(sn, LO, RF, IF, BW)
        logger.info("Freq config: %s" %ret)
        logger.info("Get current freq: %s" %service.getUDFreq(sn))

def testUDM(sn, service):
    return testUDC(sn, service)

def testUDB(sn, service):
    from tlkcore import UD_SN_TYPE
    logger.info("SN: %s" %service.querySN(sn, UD_SN_TYPE.ALL))
    return testUDC(sn, service, "UDB")

def testUDC(sn, service, name="UDM"):
    # Just passing parameter via another way
    param = {"sn": sn}
    param['item'] = UDMState.REF_LOCK | UDMState.SYSTEM | UDMState.PLO_LOCK
    ret = service.getUDState(**param)
    if ret.RetCode is not RetCode.OK:
        return logger.error("Error to get UDM state: %s" %ret)
    logger.info("%s state: %s" %(name, ret))
    lock = ret.RetData[UDMState.REF_LOCK.name]

    # Passing parameter with normal way
    logger.info("%s freq capability range: %s" %(name, service.getUDFreqLimit(sn)))
    logger.info("%s available freq range : %s" %(name, service.getUDFreqRange(sn)))

    # Example for unlock UDM/UDB freq range, then reboot to take effect
    # key = "808d5b00002d31010647a88299153a16404073215d69a6936ce49c69d48055ed354c58a1f563b241"
    # service.unlockUDFreqRange(sn, key)

    # service.reboot(sn)
    # input("Wait for rebooting...Please press ENTER to continue")

    testFreq = True
    testRefSource = True
    if name == "UDB":
        testLOInOut = True

    logger.info(f"{name} current freq: {service.getUDFreq(sn)}")

    if testFreq:
        service.setUDFreq(sn, 7e6, 10e6, 3e6, 100000)
        logger.info(f"{name} new freq: {service.getUDFreq(sn)}")

    if testRefSource:
        # We use reference config to try reference source switching
        source = service.getRefConfig(sn).RetData['source']
        logger.info("%s current ref source setting: %s, and real reference status is: %s" %(name, source, lock))

        if source is UD_REF.INTERNAL:
            # INTERNAL -> EXTERNAL
            source = UD_REF.EXTERNAL
            # Get external reference source supported list
            supported = service.getRefFrequencyList(sn, source).RetData
            logger.info("Supported external reference clock(kHz): %s" %supported)
            # Try to change reference source to external: 10M
            ret = service.setRefSource(sn, source, supported[0])
            logger.info("Change %s ref source to %s -> %s with freq: %d" %(name, source, ret, supported[0]))
            input("Waiting for external reference clock input")
        elif source is UD_REF.EXTERNAL:
            # EXTERNAL -> INTERNAL
            source = UD_REF.INTERNAL
            ret = service.setRefSource(sn, source)
            logger.info("Change %s ref source to %s -> %s" %(name, source, ret))

            # Get internal reference source supported list
            supported = service.getRefFrequencyList(sn, source).RetData
            logger.info("Supported internal output reference clock(kHz): %s" %supported)

            # Output 10MHz/100MHz ref clock
            logger.info(f"Get {name} ref output: {service.getOutputReference(sn)}")
            lo_output = False
            # Choose out ref freq from support list
            output_ref_freq = supported[0]

            logger.info("%s %s ref output(%dkHz): %s"
                        %("Enable" if lo_output else "Disable",
                          name,
                          output_ref_freq,
                          service.setOutputReference(sn, lo_output, output_ref_freq)))
            logger.info(f"Get {name} ref output: {service.getOutputReference(sn)}")

            input("Press ENTER to disable output")
            lo_output = not lo_output
            logger.info("%s %s ref output: %s"
                        %("Enable" if lo_output else "Disable",
                          name,
                          service.setOutputReference(sn, lo_output)))
            logger.info(f"Get {name} ref output: {service.getOutputReference(sn)}")

        source = service.getRefConfig(sn).RetData

        lock = service.getUDState(sn, UDMState.REF_LOCK).RetData[UDMState.REF_LOCK.name]
        logger.info("%s current ref source setting: %s, and real reference status is: %s" %(name, source, lock))

    if testLOInOut:
        lo_cfg = service.getLOConfig(sn).RetData
        logger.info("Get UDB LO config: %s" %lo_cfg)

        if lo_cfg['lo'] is UD_LO_CONFIG.LO_CFG_INTERNAL:
            # NORMAL -> OUTPUT(LO_CFG_INTERNAL_OUT) or INPUT(LO_CFG_EXTERNAL_IN)
            lo_cfg = UD_LO_CONFIG.LO_CFG_INTERNAL_OUT
        else:
            # Switch back to NORMAL mode
            lo_cfg = UD_LO_CONFIG.LO_CFG_INTERNAL
        ret = service.setLOConfig(sn, lo_cfg)
        logger.info("Change UDB LO to %s: %s" %(lo_cfg, ret))

def testBBox(sn, service):
    logger.info("MAC: %s" %service.queryMAC(sn))
    logger.info("Static IP: %s" %service.queryStaticIP(sn))
    # Sample to passing parameter with dict
    # a = {}
    # a["ip"] = '192.168.100.122'
    # a["sn"] = sn
    # logger.info("Static IP: %s" %service.setStaticIP(**a))
    # logger.info("Export dev log: %s" %service.exportDevLog(sn))

    mode = RFMode.TX
    logger.info("Set RF mode: %s" %service.setRFMode(sn, mode).name)
    logger.info("Get RF mode: %s" %service.getRFMode(sn))

    freq_list = service.getFrequencyList(sn).RetData
    if len(freq_list) == 0:
        logger.error("CAN NOT find your calibration files in \'files\' -> exit")
        return
    logger.info(f"Available frequency list: {freq_list}")

    # Please edit your target freq
    target_freq = 28.0
    if target_freq not in freq_list:
        logger.error(f"Not support your target freq:{target_freq} in freq list!")
        return

    ret = service.setOperatingFreq(sn, target_freq)
    if ret.RetCode is not RetCode.OK:
        logger.error("Set freq: %s" %ret)
        ans = input("Do you want to continue to processing? (Y/N)")
        if ans.upper() == 'N':
            return
    logger.info("Set freq: %s" %ret.RetCode)
    logger.info("Get freq: %s" %service.getOperatingFreq(sn))
    logger.info("Cali ver: %s" %service.queryCaliTableVer(sn))

    # Gain setting for BBoxOne/Lite
    rng = service.getDR(sn, mode).RetData
    logger.info("DR range: %s" %rng)

    custom_aakit = False
    if custom_aakit:
        # Set/save AAKit
        custAAKitName = 'MyAAKIT'
        aakit_info = {
                    "kitName": custAAKitName,
                    "spacing": [5.0, 5.0],
                    "steeringH": [-45.0, 45.0],
                    "steeringV": [-45.0, 45.0],
                    "offsetTx": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "offsetRx": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
        logger.info("Set AAKit: %s" %service.setAAKitInfo(sn, aakit_info))

        logger.info("Save AAKit: %s" %service.saveAAKitFile(sn, custAAKitName))
        logger.info("Get AAKitList: %s" %service.getAAKitList(sn))
        logger.info("Get AAKitInfo: %s" %service.getAAKitInfo(sn, custAAKitName))
    else:
        # Select AAKit, please call getAAKitList() to fetch all AAKit list in files/
        aakit_selected = False
        aakitList = service.getAAKitList(sn).RetData
        for aakit in aakitList:
            if '4x4' in aakit:
                logger.info("Select AAKit: %s, return %s" %(aakit, service.selectAAKit(sn, aakit).name))
                aakit_selected = True
                logger.info("Get AAKitInfo: %s" %service.getAAKitInfo(sn))
                break
        if not aakit_selected:
            logger.warning("PhiA mode")

    # Get basic operating informations
    gain_max = rng[1]

    # Set IC channel gain, we use board 1 (its index in com_dr is 0) as example
    board_count = service.getBoardCount(sn).RetData
    board = 1
    logger.info("Selected board:%d/%d" %(board, board_count))

    com_dr = service.getCOMDR(sn).RetData
    common_gain_rng = com_dr[mode.value][board-1]
    # Here we takes the maximum common gain as example
    ele_dr = service.getELEDR(sn).RetData
    logger.info("ELE DR range: %s" %ele_dr)
    ele_dr_limit = ele_dr[mode.value][board-1]
    logger.info("Board:%d common gain range: %s, and element gain limit: %s"
                    %(board, common_gain_rng, ele_dr_limit))

    # Test example options, you can decide what to test
    testChannels = False
    testBeam = False
    testFBS = True

    if testChannels:
        """Individual gain/phase/switch control example, there are some advanced test options, you can decide what to test"""
        testGain = True
        testGainPhase = True
        testSwitch = False

        if testGain:
            # Case1: Set IC channel gain without common gain
            # gain_list = [gain_max for x in range(4)]
            # logger.info("Set Gain of IC: %s" %service.setIcChannelGain(sn, board, gain_list))

            # Case2: Set IC channel gain with common gain, and gain means element gain(offset) if assign common gain
            # Each element gain must between 0 and common_gain_rng if using common gain
            ele_offsets = [ele_dr_limit for x in range(4)]
            logger.info("Set Gain of IC: %s" %service.setIcChannelGain(sn, 1, ele_offsets, common_gain_rng[1]))

        if testGainPhase:
            # input("WAIT.........Set Gain/Phase")
            gain_list = [-3.5, -3.5, -4, -3.5,
                         -14, -14, -10.5, -10.5,
                         -3, -3, -3, -3,
                         -2, -2, -2, -2]
            phase_list = [0, 285, 210, 135,
                          25, 310, 235, 160,
                          50, 335, 260, 185,
                          70, 355, 280, 205]
            # Wrong usage: set all channel iteratively
            # for i in range(16):
            #     logger.info("%d) Set Gain/Phase for specific channel: %s" %(i+1, service.setChannelGainPhase(sn, i+1, gain_list[i], phase_list[i])))
            # Correct usage: set all channels together
            logger.info("Set Gain/Phase for all channels: %s" %(service.setChannelGainPhase(sn, 0, gain_list, phase_list)))

        if testSwitch:
            # Disable specific channel example
            logger.info("Show channel disable status: %s" %service.getChannelSwitch(sn, mode))

            input("WAIT.........Channel Control - Disable")
            logger.info("Disable channel: %s" %service.switchChannel(sn, 1, True))
            logger.info("Disable channel: %s" %service.switchChannel(sn, 6, True))

            input("WAIT.........Channel Control - Enable")
            logger.info("Enable channel: %s" %service.switchChannel(sn, 1, False))
            logger.info("Enable channel: %s" %service.switchChannel(sn, 6, False))

    # Beam control example
    if testBeam:
        if aakit_selected:
            input("WAIT.........Beam Control")
            # Passing: gain, theta, phi
            logger.info("SetBeamAngle-1: %s" %service.setBeamAngle(sn, gain_max, 0, 0))
            logger.info("getBeamGainList: %s" %service.getBeamGainList(sn))
            logger.info("getBeamPhaseList: %s" %service.getBeamPhaseList(sn))
            logger.info("SetBeamAngle-2: %s" %service.setBeamAngle(sn, gain_max, 10, 30))
            logger.info("SetBeamAngle-3: %s" %service.setBeamAngle(sn, gain_max, 2, 180))
        else:
            logger.error("PhiA mode cannot process beam steering")

    if testFBS:
        # Fast Beam Steering control example
        input("WAIT.........Fast Beam Steering Mode")
        # Beam pattern functions:
        logger.info("BeamId limit: %s" %service.getBeamIdStorage(sn))

        batch_import = False
        if batch_import:
            from tlkcore import TMYBeamConfig
            batch = TMYBeamConfig(sn, service)
            if not batch.applyBeams():
                logger.error("Beam Config setting failed")
                return
        else:
            if aakit_selected:
                # Custom beam config
                beamID = 1
                # Another way to setting
                #   args = {'beamId': beamID, 'mode': RFMode.TX, 'sn': sn}
                #   ret = service.getBeamPattern(**args)
                ret = service.getBeamPattern(sn, RFMode.TX, beamID)
                beam = ret.RetData
                logger.info("BeamID %d info: %s" %(beamID, beam))

                # Edit to beam config
                config = {}
                config['db'] = gain_max
                config['theta'] = 0
                config['phi'] = 0
                ret = service.setBeamPattern(sn, RFMode.TX, beamID, BeamType.BEAM, config)
                if ret.RetCode is not RetCode.OK:
                    logger.error(ret.RetMsg)
                    return

                beamID = 2
                config = {}
                config['db'] = gain_max
                config['theta'] = 45
                config['phi'] = 0
                ret = service.setBeamPattern(sn, RFMode.TX, beamID, BeamType.BEAM, config)
                if ret.RetCode is not RetCode.OK:
                    logger.error(ret.RetMsg)
                    return

            # Custom channel config
            # beamID = 2
            # ret = service.getBeamPattern(sn, RFMode.TX, beamID)
            # beam = ret.RetData
            # logger.info("BeamID %d info: %s" %(beamID, beam))
            # if beam.get('channel_config') is None:
            #     config = {}
            # else:
            #     # Extends original config
            #     config = beam['channel_config']

            # # Edit board 1
            # # Assign random values for each channel in board_1, please modify to your case.

            # # Common gain
            # config['board_1']['common_db'] = common_gain_max-1
            # # CH1
            # config['board_1']['channel_1']['db'] = ele_dr_limit-3
            # config['board_1']['channel_1']['deg'] = 190
            # # CH2
            # config['board_1']['channel_2']['db'] = ele_dr_limit-2
            # config['board_1']['channel_2']['deg'] = 20
            # # CH3
            # config['board_1']['channel_3']['sw'] = 1
            # # CH4
            # config['board_1']['channel_4']['db'] = ele_dr_limit-4
            # ret = service.setBeamPattern(sn, RFMode.TX, beamID, BeamType.CHANNEL, config)
            # if ret.RetCode is not RetCode.OK:
            #     logger.error(ret.RetMsg)
            #     return

        # Set BBox to FBS mode
        service.setFastParallelMode(sn, True)
        logger.info("Fast Beam Steering Mode done")

def testBBoard(sn, service):
    mode = RFMode.TX
    logger.info("Set RF mode: %s" %service.setRFMode(sn, mode).name)
    logger.info("Get RF mode: %s" %service.getRFMode(sn))

    testTC = True
    testDis = True
    testGainPhase = False

    if testTC:
        logger.info("Temp ADC: %s" %service.getTemperatureADC(sn))
        logger.info(f"Query TCConfig-1: {service.queryTCConfig(sn)}")
        # It's a list inlcudes [TXC, TXQ, RXC, RXQ]
        service.setTCConfig(sn, [8, 6, 2, 9])
        logger.info(f"Query TCConfig-2: {service.queryTCConfig(sn)}")

    if testDis:
        logger.info("Show channel disable status: %s" %service.getChannelSwitch(sn, mode))

        # Disable specific channel
        logger.info("Disable channel: %s" %service.switchChannel(sn, 1, True))
        logger.info("Disable channel: %s" %service.switchChannel(sn, 4, True))

        input("WAIT.........Channel Control - Enable")

        logger.info("Enable channel: %s" %service.switchChannel(sn, 1, False))
        logger.info("Enable channel: %s" %service.switchChannel(sn, 4, False))

    if testGainPhase:
        logger.info("Set common gain step: %s" %(service.setComGainStep(sn, 9)))
        ch = 1
        ps = 2
        gs = 8
        logger.info("Set ch%d with phase step(%d): %s" %(ch, ps, service.setChannelPhaseStep(sn, ch, ps)))
        logger.info("Set ch%d with gain step(%d): %s" %(ch, gs, service.setChannelGainStep(sn, ch, gs)))
        ch = 3
        ps = 3
        gs = 7
        logger.info("Set ch%d with phase step(%d): %s" %(ch, ps, service.setChannelPhaseStep(sn, ch, ps)))
        logger.info("Set ch%d with gain step(%d): %s" %(ch, gs, service.setChannelGainStep(sn, ch, gs)))

def testCloverCell(sn, service):
    # Please use CellRFMode to replace RFMode
    logger.info("Get current RF mode: %s" %service.getRFMode(sn))
    mode = CellRFMode.TX
    logger.info("Set RF mode to %s: %s" %(mode, service.setRFMode(sn, mode).name))

    logger.info(f"Query TCConfig: {service.queryTCConfig(sn)}")

    logger.info("Get IC operaring status: %s" %service.getOperatingStatus(sn))

    freq_list = service.getFrequencyList(sn).RetData
    if len(freq_list) == 0:
        logger.error("CAN NOT find your calibration files in \'files\' -> exit")
        return
    logger.info("Available frequency list: %s" %freq_list)

    # Please edit your target freq
    target_freq = 28.0
    if target_freq not in freq_list:
        logger.error(f"Not support your target freq:{target_freq} in freq list!")
        return

    ret = service.setOperatingFreq(sn, target_freq)
    if ret.RetCode is not RetCode.OK:
        logger.error("Set freq: %s" %ret)
        ans = input("Do you want to continue to processing? (Y/N)")
        if ans.upper() == 'N':
            return
    logger.info("Set freq: %s" %ret.RetCode)
    logger.info("Get freq: %s" %service.getOperatingFreq(sn))
    logger.info("Cali ver: %s" %service.queryCaliTableVer(sn))

    # Gain setting for Clover
    rng = service.getDR(sn, mode).RetData
    logger.info("DR range: %s" %rng)

    # Polarization setting
    polar = POLARIZATION.HORIZON

    # Get basic operating informations
    gain_max = rng[polar.name][1]

    # Set IC channel gain, we use board_1 (its index in com_dr is 0) as example
    board_count = service.getBoardCount(sn).RetData
    board = 1
    logger.info("Selected board:%d/%d" %(board, board_count))

    com_dr = service.getCOMDR(sn).RetData
    logger.info("COM DR range: %s" %com_dr)
    common_gain_rng = com_dr[mode.value][board-1][polar.name]
    # # Here we takes the maximum common gain as example
    common_gain_max = common_gain_rng[1]
    ele_dr = service.getELEDR(sn).RetData
    logger.info("ELE DR range: %s" %ele_dr)
    ele_dr_limit = ele_dr[mode.value][board-1][polar.name]
    logger.info("Board:%d with %s plane common gain range: %s, and element gain limit: %s"
                    %(board, polar.name, common_gain_rng, ele_dr_limit))

    # Test example options, you can decide what to test
    testChannels = True
    testBeam = True

    if testChannels:
        """
        Individual gain/phase/switch control example,
        there are some advanced test options, you can decide what to test
        """
        testGain = True
        testGainPhase = True
        testSwitch = True

        if testGain:
            # Set IC common gain
            logger.info("[%s_%s] Set Com Gain:%f to IC: %s"
                        %(mode.name, polar.name[0], common_gain_max,
                        service.setIcComGain(sn, polar, board, common_gain_max)))

            # Each element gain must between 0 and common_gain_rng if using common gain
            ele_offsets = [ele_dr_limit for x in range(4)]
            logger.info("Set Channel Gains to IC: %s for %s polarization"
                        %(service.setIcChannelGain(sn, board, ele_offsets, common_gain_max, polar),
                        polar))

        if testGainPhase:
            logger.info("Set Gain/Phase: %s" %service.setChannelGainPhase(sn, 1, common_gain_max+1, 30, polar))

            gain_list = [gain_max for x in range(board_count*4)]
            phase_list = [30 for x in range(board_count*4)]
            logger.info("Set Gain/Phase: %s" %service.setChannelGainPhase(sn, 0, gain_list, phase_list, polar))

        if testSwitch:
            # Disable specific channel example
            logger.info("Show channel disable status: %s" %service.getChannelSwitch(sn, mode, polar))

            input("WAIT.........Channel Control - Disable")
            logger.info("Disable channel: %s for %s polarization" %(service.switchChannel(sn, 1, True, polar), polar))
            logger.info("Disable channel: %s for all polarization" %service.switchChannel(sn, 4, True))

            input("WAIT.........Channel Control - Enable")
            logger.info("Enable channel: %s" %service.switchChannel(sn, 1, False, polar))
            logger.info("Enable channel: %s" %service.switchChannel(sn, 4, False))

    # Beam control example
    if testBeam:
        input("WAIT.........Beam Control")
        # Passing: gain, theta, phi
        logger.info("SetBeamAngle-1: %s" %service.setBeamAngle(sn, gain_max, 0, 0, polar))
        logger.info("SetBeamAngle-2: %s" %service.setBeamAngle(sn, gain_max-1, 10, 30, polar))
        logger.info("SetBeamAngle-3: %s" %service.setBeamAngle(sn, gain_max-ele_dr_limit+1, 5, 30, polar))
        # logger.info("getBeamGainList: %s" %service.getBeamGainList(sn, polar))
        # logger.info("getBeamPhaseList: %s" %service.getBeamPhaseList(sn, polar))

    # -----------------
    logger.info("Get last IC operating config: %s" %service.getOperatingConfig(sn, mode))
    mode = CellRFMode.STANDBY
    logger.info("Get current RF mode: %s" %service.getRFMode(sn))
    logger.info("Set RF mode: %s" %service.setRFMode(sn, mode).name)

def testRIS(sn, service):
    logger.info("Get Net config: %s" %service.getNetInfo(sn))
    # logger.info("Set Net: %s" %service.setIPMode(sn, 0))
    # logger.info("Set Net: %s" %service.setSubnetMsk(sn, "255.255.255.0"))
    # logger.info("Set Net: %s" %service.setGateway(sn, "192.168.100.1"))

    ret = service.getRISModuleInfo(sn)
    if ret.RetCode is not RetCode.OK:
        logger.error("Get RIS Module Info failed: %s" %ret.RetMsg)
        return
    info = ret.RetData
    logger.info(f"Get RIS Module Info: {getJSONFmt(info)}")

    # Here we use frequency of the first module as central freq for this example, please modify it
    first_module = next(iter(info))  # Get the first available module

    # Test example options, you can decide what to test, True to test RISAngle or False to import pattern
    testAngleElseImport = True

    # Please assign module to setting, here use the first module
    target_module = int(first_module)
    target_module_rotate = {int(first_module): 0}

    if testAngleElseImport:
        # Set RIS angle example

        # Decide test tile up RIS modules or set False to set only one module
        testTileUp = True

        if testTileUp:
            # Here we assume there are 4 modules to tileup,
            # and it specifies the target module partition to control.
            # It can be a single value likes 1, a list likes [1, 2],
            # or a nested list likes [[1, 2]] or [[1],
            #                                     [2]]. Defaults to 1.
            target_module = [[2,1],
                             [3,4]]
            # It specifies the clockwise rotation angle of each module,
            # and the degree must be a multiple of 90
            target_module_rotate = {1: 90.0, 2: 0, 3: -90, 4: -180}

        # And we +100Mhz as our target frequency, PLEASE MODIFY with every 100Mhz step.
        adjust_mhz = 0#100
        target_freq = info[first_module]['freq_mhz']['central'] + adjust_mhz

        param = {
            'sn': sn,
            'incident': RIS_Dir(distance=1), # given distance, and optional param: angle with [theta, phi] or only theta for [theta, 0]
            'reflection': { # another parameter usage
                'distance': 1,
                'angle': (30, 0),
            },
            # set module_config with dict
            'module_config': {
                'central_freq_mhz': target_freq,
                'module': target_module,
                'module_rotate': target_module_rotate
            }
            # Or you can use another way to set module_config
            # 'module_config' = RIS_ModuleConfig(central_freq_mhz=target_freq, module=target_module, module_rotate=target_module_rotate),
        }
        ret = service.setRISAngle(**param)
        if ret.RetCode is not RetCode.OK:
            logger.error("Set RIS with angle error: %s" %ret)
            return
        logger.info("Set RIS with angle: OK")

    else:
        # Import pattern example
        import csv
        # Import csv with 1,0,1,0,1,1,... format to the target module
        # Please modify the file name to your case and care about the row/col count should meet antenna size
        with open("Sample.csv", 'r') as infile:
            reader = csv.reader(infile)
            single_pattern = [[int(num) for num in row] for row in reader]
        # Modify to one module to maps to the pattern, or you can set all modules to the different patterns
        module_ptn = {target_module: single_pattern}
        logger.info("Set imported RIS pattern: %s" %service.setRISPattern(sn, module_ptn))

    # Get pattern example
    pattern = service.getRISPattern(sn, target_module).RetData
    if isinstance(pattern, list):
        # single module returns list only
        logger.info(f" ===== Pattern of Module {target_module} =====")
        i = 1
        for row in pattern:
            logger.info(f"Get Ptn {i:>2} = {row}")
            i+=1
    else:
        # multi modules returns dict
        for m, p in pattern.items():
            logger.info(f" ===== Pattern of Module {m} =====")
            i = 1
            for row in p:
                logger.info(f"Get Ptn {i:>2} = {row}")
                i+=1

def testBBoxDuo(sn, service):
    logger.info("MAC: %s" %service.queryMAC(sn))
    logger.info("Static IP: %s" %service.queryStaticIP(sn))

    logger.info("========= BBox Duo Get functions =========")

    ret = service.getRfFreq(sn).RetData
    logger.info("Get RF freq: %s kHz" % ret)

    ret = service.getLoFreq(sn).RetData
    logger.info("Get LO freq: %s kHz" % ret)

    ret = service.getLoStatus(sn).RetData
    logger.info("Get LO status: %s" % ret)

    ret = service.getRefSource(sn).RetData
    logger.info("Get Ref source: %s" % ret)

    ret = service.getTRx(sn).RetData
    logger.info("Get TRx status: %s" % ret)

    ret = service.checkHarmonic(sn, lo_freq = 22500000, if_freq = 5000000, bandwidth = 2000000).RetData
    logger.info("Check Harmonic: %s" % ret)

    logger.info("========= BBox Duo Set functions =========")

    ret = service.setRfFreq(sn, 28000000).RetData
    logger.info("Set RF freq to 28000000 kHz: %s" % ret)

    ret = service.setLoFreq(sn, 22500000).RetData
    logger.info("Set LO freq to 22500000 kHz: %s" % ret)

    ret = service.setRefSource(sn, 0).RetData
    logger.info("Set Ref source to External 10M: %s" % ret)

    ret = service.setBeam(sn, theta = 30, phi = 60).RetData
    logger.info("Set Beam to theta=30, phi=60: %s" % ret)

    ret = service.setTRx(sn, 2).RetData
    logger.info("Set TRx to 2 (RX): %s" % ret)

    ret = service.setRxUdAtt(sn, 0).RetData
    logger.info("Set RX user attenuation to 0: %s" % ret)

    ret = service.setTxUdAtt(sn, 0).RetData
    logger.info("Set TX user attenuation to 0: %s" % ret)

def startDFU(sn, service, dfu_image:str, dfu_dev_info:dict):
    """A example to process DFU"""
    if len(dfu_image) <= 0:
        logger.error("[DFU] image path is wrong -> exit")
        return
    if not service.getDFUSupport(sn).RetData:
        logger.error("[DFU] device does not support DFU -> exit")
        return

    logger.info("[DFU] Starting DFU mode, and passing info to middleware")
    ret = service.processDFU(sn, dfu_image, dfu_dev_info)
    if ret.RetCode is not RetCode.OK:
        logger.error("[DFU] DFU failed -> quit")
        return

    ver_new = ret.RetData
    msg = "\r\n***********************************************************************\r\n"
    msg += "[DFU] Done! FW ver: %s -> %s" %(dfu_dev_info["fw_ver"], ver_new) + msg
    logger.info(msg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--dc", help="Direct connect device to skip scanning, must provide 3 parameters: SN IP dev_type", metavar=('SN','Address','DevType'), nargs=3)
    parser.add_argument("--dfu", help="DFU image path", type=str, default="")
    parser.add_argument("--root", help="The root path/directory of for log/ & files/", type=str, default=".")
    args = parser.parse_args()

    startService(args.root, args.dc, args.dfu)
    logger.info("========= end =========")