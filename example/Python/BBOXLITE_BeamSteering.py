import sys
import csv
import time
import argparse
import numpy as np
from Control_Interface import BBox_Control_Interface

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument("--sn", help="String argument : D20461000-28", type=str)
	parser.add_argument("--mode", help="Integer argument : TX - 1 , RX - 2", type=int)
	parser.add_argument("--db", help="Float argument : gain settings in range(DynamicRange_MIN_GAIN, DynamicRange_MAX_GAIN, 0.5)", type=float)
	parser.add_argument("--angle", help="Integer argument : in range(-45, 45, 1)", type=int)

	args = parser.parse_args()

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	if args.mode != 1 and args.mode != 2:
		print("[MAIN][%s] Invalid mode argument")
		sys.exit(1)
	elif args.angle < -45 or args.angle > 45:
		print("[MAIN][%s] Invalid angle argument")
		sys.exit(1)

	obj = BBox_Control_Interface()

	if obj.Get_SN_Index(args.sn) == -1:
		print("[MAIN][%s] Invalid sn " % (args.sn))

	Dynamic_Range = obj.Get_Dynamic_Range(args.sn, args.mode)
	min_gain = Dynamic_Range[0]
	max_gain = Dynamic_Range[1]

	if args.db < min_gain or args.db > max_gain:
		print("[MAIN][%s] Invalid db argument")
		sys.exit(1)

	if obj.SetDeviceBeamSteering(args.sn, args.mode, args.db, args.angle):
		print("[MAIN][%s] SetDeviceBeamSteering success" % (args.sn))
	else:
		print("[MAIN][%s] SetDeviceBeamSteering failed" % (args.sn))
