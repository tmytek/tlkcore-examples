import sys
import csv
import time
import numpy as np
from BBOXLITE_Control_Interface import BBOXLITE_Control_Interface

if __name__ == '__main__':

	obj = BBOXLITE_Control_Interface()

	sn = obj.Get_SN_List()
	device_num = obj.Get_Active_DeviceNum()

	timeout = 2

	for i in range(0, device_num):
		print("[BBOXLITE_ChannelControl_DEMO] %d. sn : %s" % (i, sn[i]))

		Off = 1
		channel = 2
		obj.SwitchChannelPower(sn[i], obj.TX, channel, Off)
		channel = 3
		obj.SwitchChannelPower(sn[i], obj.TX, channel, Off)
		channel = 4
		obj.SwitchChannelPower(sn[i], obj.TX, channel, Off)

		min_db = obj.Get_Dynamic_Range_Minimum_Gain(sn[i], obj.TX)
		max_db = obj.Get_Dynamic_Range_Maximum_Gain(sn[i], obj.TX)
		db_step = 0.5

		min_deg = 0
		max_deg = 359
		deg_step = 30

		while True:
			for db in np.arange(min_db, max_db, db_step):
				for deg in np.arange(min_deg, max_deg, deg_step):
					if obj.SetDeviceGainPhase(sn[i], obj.TX, db, deg, db, deg, db, deg, db, deg):
						print("[BBOXLITE_ChannelControl_DEMO][SetDeviceGainPhase][%s] TX , %f db , %d deg" % (sn[i], db, deg))

						gain_settings = obj.Get_Channel_Gain_settings(sn[i], obj.TX)
						phase_settings = obj.Get_Channel_Phase_settings(sn[i], obj.TX)
						print("[BBOXLITE_ChannelControl_DEMO][Get_Channel_Gain_settings][%s]" % (sn[i]))
						print("[BBOXLITE_ChannelControl_DEMO][Get_Channel_Gain_settings][%s] TX : channel_1 : %f db , %f deg" % (sn[i], gain_settings[0], phase_settings[0]))
						print("[BBOXLITE_ChannelControl_DEMO][Get_Channel_Gain_settings][%s] TX : channel_2 : %f db , %f deg" % (sn[i], gain_settings[1], phase_settings[1]))
						print("[BBOXLITE_ChannelControl_DEMO][Get_Channel_Gain_settings][%s] TX : channel_3 : %f db , %f deg" % (sn[i], gain_settings[2], phase_settings[2]))
						print("[BBOXLITE_ChannelControl_DEMO][Get_Channel_Gain_settings][%s] TX : channel_4 : %f db , %f deg" % (sn[i], gain_settings[3], phase_settings[3]))
						time.sleep(timeout)
					else:
						print("[BBOXLITE_ChannelControl_DEMO][Get_Channel_Gain_settings][%s] SetDeviceGainPhase failed" % (sn[i]))
						break

