import sys
import csv
import time
import numpy as np
from Control_Interface import BBox_Control_Interface

if __name__ == '__main__':

	obj = BBox_Control_Interface()

	sn = obj.Get_SN_List()
	device_num = obj.Get_Active_DeviceNum()

	TX_DR = []
	RX_DR = []

	timeout = 2

	for i in range(0, device_num):
		print("[MAIN] %d. sn : %s" % (i, sn[i]))

		TX_DR.append(obj.Get_Dynamic_Range(sn[i], obj.TX))
		RX_DR.append(obj.Get_Dynamic_Range(sn[i], obj.RX))

		Off = 1
		channel = 2
		obj.SwitchChannelPower(sn[i], obj.TX, channel, Off)
		channel = 3
		obj.SwitchChannelPower(sn[i], obj.TX, channel, Off)
		channel = 4
		obj.SwitchChannelPower(sn[i], obj.TX, channel, Off)

		min_db = 0
		max_db = 20
		db_step = 5

		min_deg = 0
		max_deg = 360
		deg_step = 60

		while True:
			for db in np.arange(0, 20, 5):
				for deg in np.arange(0, 360, 60):
					if obj.SetDeviceGainPhase(sn[i], obj.TX, db, deg, db, deg, db, deg, db, deg):
						print("[MAIN][SetDeviceGainPhase][%s] TX , %f db , %d deg" % (sn[i], db, deg))

						gain_settings = obj.Get_Channel_Gain_settings(sn[i], obj.TX)
						phase_settings = obj.Get_Channel_Phase_settings(sn[i], obj.TX)
						print("[MAIN][Get_Channel_Gain_settings][%s]" % (sn[i]))
						print("[MAIN][Get_Channel_Gain_settings][%s] TX : channel_1 : %f db , %f deg" % (sn[i], gain_settings[0], phase_settings[0]))
						print("[MAIN][Get_Channel_Gain_settings][%s] TX : channel_2 : %f db , %f deg" % (sn[i], gain_settings[1], phase_settings[1]))
						print("[MAIN][Get_Channel_Gain_settings][%s] TX : channel_3 : %f db , %f deg" % (sn[i], gain_settings[2], phase_settings[2]))
						print("[MAIN][Get_Channel_Gain_settings][%s] TX : channel_4 : %f db , %f deg" % (sn[i], gain_settings[3], phase_settings[3]))
						time.sleep(timeout)

