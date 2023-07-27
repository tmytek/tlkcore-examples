import sys
import csv
import time
import numpy as np
from BBoxLite_Control_Interface import BBOXLITE_Control_Interface

if __name__ == '__main__':

	obj = BBOXLITE_Control_Interface()

	sn = obj.Get_SN_List()
	device_num = obj.Get_Active_DeviceNum()

	timeout = 2

	for i in range(0, device_num):
		print("[BBoxLite_BeamSteering_DEMO][%s] Index %d" % (sn[i], i))

		db = 15
		phi = 0

		min_theta = 0
		max_theta = 30
		theta_step = 5

		while True:
			for theta in np.arange(min_theta, max_theta, theta_step):
				if obj.SetDeviceBeamSteering(sn[i], obj.TX, db, theta, phi):
					print("[BBoxLite_BeamSteering_DEMO][SetDeviceBeamSteering][%s] TX , %f db , theta : %d, phi : %d" % (sn[i], db, theta, phi))
					time.sleep(timeout)


