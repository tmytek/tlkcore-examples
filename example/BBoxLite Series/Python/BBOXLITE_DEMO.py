import sys
import clr
import time
import csv
import os
import numpy as np


path = '.\\BBoxAPI.dll'
clr.AddReference(os.path.abspath(path))


from BBoxAPI import *

if __name__ == '__main__':

    TX = 1
    RX = 2

    AAkitList = []

    instance = BBoxOneAPI()

    dev_info = instance.ScanningDevice(0)
    device_num = len(dev_info)

    if device_num > 0 and dev_info[0] != "Result,NoDeviceFound,-1":
        for i in range(0, device_num, 1):

            response_message = dev_info[i].split(",")
            sn = response_message[0]
            ip = response_message[1]
            val = response_message[2].split("\x00")
            dev_type = int(val[0])

            print("[BBoxLite_DEMO][GetDeviceStatus] SN : %s" % (sn))
            print("[BBoxLite_DEMO][GetDeviceStatus] IP : %s" % (ip))
            print("[BBoxLite_DEMO][GetDeviceStatus] dev_type : %d" % (dev_type))

            instance.Init(sn, dev_type, i)
            print("[BBoxLite_DEMO][InitialDevice][%s]" % (sn))

            freq_list = instance.getFrequencyList(sn)
            if len(freq_list) == 0:
                print("[BBoxLite_DEMO][InitialDevice][%s] failed : return null" % (sn))
            else:
                for item in freq_list:
                    print("[BBoxLite_DEMO][InitialDevice][%s] getFrequencyList: list %s" % (sn, item))

            ret = instance.setOperatingFreq(freq_list[0], sn)
            if ret != 0:
                print("[BBoxLite_DEMO][InitialDevice][%s] setOperatingFreq failed : error_code %d" % (sn, ret))

            DR = instance.getDR(sn)
            print("[BBoxLite_DEMO][InitialDevice][%s] " % (sn))
            TX_MIN_GAIN = DR[0, 0]
            print("[BBoxLite_DEMO][InitialDevice][%s] TX_MIN_GAIN : %f" % (sn, TX_MIN_GAIN))
            TX_MAX_GAIN = DR[0, 1]
            print("[BBoxLite_DEMO][InitialDevice][%s] TX_MAX_GAIN : %f" % (sn, TX_MAX_GAIN))
            RX_MIN_GAIN = DR[1, 0]
            print("[BBoxLite_DEMO][InitialDevice][%s] RX_MIN_GAIN : %f" % (sn, RX_MIN_GAIN))
            RX_MAX_GAIN = DR[1, 1]
            print("[BBoxLite_DEMO][InitialDevice][%s] RX_MAX_GAIN : %f" % (sn, RX_MAX_GAIN))

            AAkitList = instance.getAAKitList(sn)
            if len(AAkitList) > 0:
                instance.selectAAKit(AAkitList[0], sn)


            print("======================================================")
            print("[BBoxLite_DEMO][DEMO1] Switch TX mode")
            os.system("pause")
            instance.SwitchTxRxMode(TX, sn)
            mode = instance.getTxRxMode(sn)
            print("[BBoxLite_DEMO][DEMO1] Mode : %d" % (mode))

            print("======================================================")
            print("[BBoxLite_DEMO][DEMO2] Channel power control : Off channel 1 power")
            os.system("pause")

            board = 1
            channel = 1
            sw = 1
            instance.switchChannelPower(board, channel, sw, sn)
            print("[BBoxLite_DEMO][DEMO2] Channel 1 power off")

            Target_db = TX_MAX_GAIN
            Target_ch1_deg = 15
            Target_ch2_deg = 30
            Target_ch3_deg = 45
            Target_ch4_deg = 60
            print("======================================================")
            print("[BBoxLite_DEMO][DEMO3] Channel Gain/Phase Control")
            print("[BBoxLite_DEMO][DEMO3] Channel_1 gain  : %f db" %(Target_db))
            print("[BBoxLite_DEMO][DEMO3] Channel_1 phase : %d deg" %(Target_ch1_deg))
            print("[BBoxLite_DEMO][DEMO3] Channel_2 gain  : %f db" %(Target_db))
            print("[BBoxLite_DEMO][DEMO3] Channel_2 phase : %d deg" %(Target_ch2_deg))
            print("[BBoxLite_DEMO][DEMO3] Channel_3 gain  : %f db" %(Target_db))
            print("[BBoxLite_DEMO][DEMO3] Channel_3 phase : %d deg" %(Target_ch3_deg))
            print("[BBoxLite_DEMO][DEMO3] Channel_4 gain  : %f db" %(Target_db))
            print("[BBoxLite_DEMO][DEMO3] Channel_4 phase : %d deg" %(Target_ch4_deg))
            os.system("pause")

            board = 1

            channel = 1
            instance.setChannelGainPhase(board, channel, Target_db, Target_ch1_deg, sn)

            channel = 2
            instance.setChannelGainPhase(board, channel, Target_db, Target_ch2_deg, sn)

            channel = 3
            instance.setChannelGainPhase(board, channel, Target_db, Target_ch3_deg, sn)

            channel = 4
            instance.setChannelGainPhase(board, channel, Target_db, Target_ch4_deg, sn)

            print("======================================================")
            print("[BBoxLite_DEMO][DEMO4] BeamSteering Control")
            os.system("pause")

            Target_db = TX_MAX_GAIN
            Target_theta = 15
            Target_phi = 0
            print("[BBoxLite_DEMO][DEMO4] Channel gain  : %f db" %(Target_db))
            print("[BBoxLite_DEMO][DEMO4] Beam theta : %d " %(Target_theta))
            print("[BBoxLite_DEMO][DEMO4] Beam phi : %d " %(Target_phi))

            instance.setBeamAngle(Target_db, Target_theta, Target_phi, sn)

            os.system("pause")

            adc_ret = instance.getTemperatureADC(sn)
            print("[BBoxLite_DEMO][DEMO5] Get temperature adc : %d" %adc_ret[0])
    else:
        print("[BBoxLite_DEMO][DEMO] No device found")


    print("======================================================")
    print("[BBoxLite_DEMO][DEMO] End")
    os.system("pause")
