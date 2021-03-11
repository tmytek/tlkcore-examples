import sys
import clr
import time
import csv
import os
import numpy as np

dir_path = '..\\..\\..\\..\\'
os.chdir(os.path.abspath(dir_path))

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

			print("[BBoxOne_Control_Interface][GetDeviceStatus] SN : %s" % (sn))
			print("[BBoxOne_Control_Interface][GetDeviceStatus] IP : %s" % (ip))
			print("[BBoxOne_Control_Interface][GetDeviceStatus] dev_type : %d" % (dev_type))
   
			instance.Init(sn, dev_type, i)
			print("[BBoxOne_Control_Interface][InitialDevice][%s]" % (sn))

			freq_list = instance.getFrequencyList(sn)
			if len(freq_list) == 0:
				print("[BBoxOne_Control_Interface][InitialDevice][%s] failed : return null" % (sn))
			else:
				for item in freq_list:
					print("[BBoxOne_Control_Interface][InitialDevice][%s] getFrequencyList: list %s" % (sn, item))

			ret = instance.setOperatingFreq(freq_list[0], sn)
			if ret != 0:
				print("[BBoxOne_Control_Interface][InitialDevice][%s] setOperatingFreq failed : error_code %d" % (sn, ret))

			DR = instance.getDR(sn)
			print("[BBoxOne_Control_Interface][InitialDevice][%s] " % (sn))
			TX_MIN_GAIN = DR[0, 0]
			print("[BBoxOne_Control_Interface][InitialDevice][%s] TX_MIN_GAIN : %f" % (sn, TX_MIN_GAIN))
			TX_MAX_GAIN = DR[0, 1]
			print("[BBoxOne_Control_Interface][InitialDevice][%s] TX_MAX_GAIN : %f" % (sn, TX_MAX_GAIN))
			RX_MIN_GAIN = DR[1, 0]
			print("[BBoxOne_Control_Interface][InitialDevice][%s] RX_MIN_GAIN : %f" % (sn, RX_MIN_GAIN))
			RX_MAX_GAIN = DR[1, 1]
			print("[BBoxOne_Control_Interface][InitialDevice][%s] RX_MAX_GAIN : %f" % (sn, RX_MAX_GAIN))

			AAkitList.append(instance.getAAKitList(sn))
			instance.selectAAKit(AAkitList[i][0], sn)

			print("======================================================")
			print("[DEMO1] Switch TX mode")
			os.system("pause")
			instance.SwitchTxRxMode(TX, sn)
			mode = instance.getTxRxMode(sn)
			print("[DEMO1] Mode : %d" % (mode))

			print("======================================================")
			print("[DEMO2] Channel power control : Off channel 1 power")
			os.system("pause")

			board = 1
			channel = 1
			sw = 1
			instance.switchChannelPower(board, channel, sw, sn)
			print("[DEMO2] Channel 1 power off")

			print("======================================================")
			print("[DEMO3] Channel Gain/Phase Control")
			print("[DEMO3] Channel_1 gain  : 15 db")
			print("[DEMO3] Channel_1 phase : 15 deg")
			print("[DEMO3] Channel_2 gain  : 15 db")
			print("[DEMO3] Channel_2 phase : 30 deg")
			print("[DEMO3] Channel_3 gain  : 15 db")
			print("[DEMO3] Channel_3 phase : 45 deg")
			print("[DEMO3] Channel_4 gain  : 15 db")
			print("[DEMO3] Channel_4 phase : 60 deg")
			os.system("pause")

			board = 1

			channel = 1
			Target_db = 15
			Target_deg = 15
			instance.setChannelGainPhase(board, channel, Target_db, Target_deg, sn)

			channel = 2
			Target_db = 15
			Target_deg = 30
			instance.setChannelGainPhase(board, channel, Target_db, Target_deg, sn)

			channel = 3
			Target_db = 15
			Target_deg = 45
			instance.setChannelGainPhase(board, channel, Target_db, Target_deg, sn)

			channel = 4
			Target_db = 15
			Target_deg = 60
			instance.setChannelGainPhase(board, channel, Target_db, Target_deg, sn)

			print("======================================================")
			print("[DEMO4] BeamSteering Control")
			os.system("pause")
			print("[DEMO4] Channel gain  : 12 db")
			print("[DEMO4] Beam angle : 15 ")

			Target_db = 12
			Target_angle_x = 15
			Target_angle_y = 0
			instance.setBeamXY(Target_db, Target_angle_x, Target_angle_y, sn)

	print("======================================================")
	print("[DEMO] End")
	os.system("pause")
