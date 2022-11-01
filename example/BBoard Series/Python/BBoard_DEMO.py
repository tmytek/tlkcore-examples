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

    if device_num > 0:
        for i in range(0, device_num, 1):

            response_message = dev_info[i].split(",")
            sn = response_message[0]
            ip = response_message[1]
            val = response_message[2].split("\x00")
            dev_type = int(val[0])

            print("[BBoard_DEMO][GetDeviceStatus] SN : %s" % (sn))
            print("[BBoard_DEMO][GetDeviceStatus] IP : %s" % (ip))
            print("[BBoard_DEMO][GetDeviceStatus] dev_type : %d" % (dev_type))

            instance.Init(sn, dev_type, i)
            print("[BBoard_DEMO][InitialDevice][%s]" % (sn))


            print("======================================================")
            print("[BBoard_DEMO][DEMO1] Switch TX mode")
            os.system("pause")
            instance.SwitchTxRxMode(TX, sn)
            mode = instance.getTxRxMode(sn)
            print("[BBoard_DEMO][DEMO1] Mode : %d" % (mode))

            print("======================================================")
            print("[BBoard_DEMO][DEMO2] Channel power control : Off channel 1 power")
            os.system("pause")

            board = 1
            channel = 1
            sw = 1
            instance.switchChannelPower(board, channel, sw, sn)
            print("[BBoard_DEMO][DEMO2] Channel 1 power off")


            gain_step = 1
            print("======================================================");
            print("[BBoard_DEMO][DEMO3] Channel Element Gain Step Control")
            print("[BBoard_DEMO][DEMO3] Channel_1 gain step : %d" % (gain_step))
            print("[BBoard_DEMO][DEMO3] Channel_2 gain step : %d" % (gain_step))
            print("[BBoard_DEMO][DEMO3] Channel_3 gain step : %d" % (gain_step))
            print("[BBoard_DEMO][DEMO3] Channel_4 gain step : %d" %( gain_step))

            os.system("pause")

            board = 1

            channel = 1
            instance.setChannelGainStep(board, channel, gain_step, sn)

            channel = 2
            instance.setChannelGainStep(board, channel, gain_step, sn)

            channel = 3
            instance.setChannelGainStep(board, channel, gain_step, sn)

            channel = 4
            instance.setChannelGainStep(board, channel, gain_step, sn)

            print("======================================================")
            print("[BBoard_DEMO][DEMO4] Common Gain Step Control")
            print("[BBoard_DEMO][DEMO4] Com gain step : %d" % (gain_step))

            os.system("pause")

            instance.setCommonGainStep(board, gain_step, sn);

            phase_step = 1

            print("======================================================")
            print("[BBoard_DEMO][DEMO5] Channel Element Phase Step Control", sn)
            print("[BBoard_DEMO][DEMO5] Channel_1 phase step : %d" % (phase_step))
            print("[BBoard_DEMO][DEMO5] Channel_2 phase step : %d" % (phase_step))
            print("[BBoard_DEMO][DEMO5] Channel_3 phase step : %d" % (phase_step))
            print("[BBoard_DEMO][DEMO5] Channel_4 phase step : %d" % (phase_step))

            os.system("pause")

            board = 1

            channel = 1
            instance.setChannelPhaseStep(board, channel, phase_step, sn)

            channel = 2
            instance.setChannelPhaseStep(board, channel, phase_step, sn)

            channel = 3
            instance.setChannelPhaseStep(board, channel, phase_step, sn)

            channel = 4
            instance.setChannelPhaseStep(board, channel, phase_step, sn)

            print("======================================================")
            print("[BBoard_DEMO][DEMO5] Get temperature adc")

            os.system("pause")

            ret = instance.getTemperatureADC(sn)
            print("[BBoard_DEMO][DEMO5] Get temperature adc : %d" %ret[0])


    print("======================================================")
    print("[BBoard_DEMO][DEMO] End")
    os.system("pause")

