import sys
import csv
import time
import argparse
from BBOXLITE_Control_Interface import BBOXLITE_Control_Interface

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument("--sn", help="String_Argument : D2046L001-28", type=str)
	parser.add_argument("--mode", help="Integer_Argument : (TX, 1) , (RX, 2)", type=int)

	args = parser.parse_args()

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	if args.mode != 1 and args.mode != 2:
		print("[MAIN] Invalid mode argument")
		sys.exit(1)

	instance = BBOXLITE_Control_Interface()

	if instance.Get_SN_Index(args.sn) == -1:
		print("[MAIN][%s] Invalid sn " % (args.sn))

	Maximum_Gain = instance.Get_Dynamic_Range_Maximum_Gain(args.sn, args.mode)
	Minimum_Gain = instance.Get_Dynamic_Range_Minimum_Gain(args.sn, args.mode)

	while True:
		print("================================================================================")
		print("Usage :")
		print("Target_db : In range(Minimum_Gain, Maximum_Gain, 0.5)")
		print("Target_angle : In range(-45, 45, 1)")
		print("Program_Exit : ctrl + z")
		print("=================================================================================")

		arg = input("Target_db : ")
		Target_db = float(arg)
		if Target_db < Minimum_Gain or Target_db > Maximum_Gain:
			print("[MAIN][%s] Invalid Target_db argument" % (args.sn))
			sys.exit(1)

		arg = input("Target_angle : ")
		Target_angle = int(arg)

		if Target_angle < instance.min_angle or Target_angle > instance.max_angle:
			print("[MAIN][%s] Invalid Target_angle argument" % (args.sn))
			sys.exit(1)

		instance.SetDeviceBeamSteering(args.sn, args.mode, Target_db, Target_angle)

		instance.Get_Device_settings(args.sn, args.mode)


