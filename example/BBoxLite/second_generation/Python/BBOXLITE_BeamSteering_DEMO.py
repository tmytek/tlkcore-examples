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
		print("[MAIN][%s] index %d" % (sn[i], i))

		db = 15

		min_angle = -30
		max_angle = 40
		angle_step = 10

		while True:
			for angle in np.arange(min_angle, max_angle, angle_step):
				if obj.SetDeviceBeamSteering(sn[i], obj.TX, db, angle):
					print("[MAIN][SetDeviceBeamSteering][%s] TX , %f db , %d angle" % (sn[i], db, angle))
					time.sleep(timeout)


