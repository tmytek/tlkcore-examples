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

		db = 15

		min_angle = -30
		max_angle = 40
		angle_step = 10

		while True:
			for angle in np.arange(min_angle, max_angle, angle_step):
				if obj.SetDeviceBeamSteering(sn[i], obj.TX, db, angle):
					print("[MAIN][SetDeviceBeamSteering][%s] TX , %f db , %d angle" % (sn[i], db, angle))
					time.sleep(timeout)


