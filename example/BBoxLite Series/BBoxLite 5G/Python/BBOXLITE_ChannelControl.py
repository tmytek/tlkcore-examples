import sys
import csv
import time
import argparse
from BBOXLITE_Control_Interface import BBOXLITE_Control_Interface

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument("--sn", help="String_argument : D2104L011-28", type=str)
	parser.add_argument("--mode", help="Integer_argument : (TX, 1) , (RX, 2)", type=int)

	args = parser.parse_args()

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	if args.mode != 1 and args.mode != 2:
		print("[BBOXLITE_ChannelControl][%s] Invalid mode argument")
		sys.exit(1)

	instance = BBOXLITE_Control_Interface()

	if instance.Get_SN_Index(args.sn) == -1:
		print("[BBOXLITE_ChannelControl][%s] Invalid sn " % (args.sn))

	Minimum_Gain = instance.Get_Dynamic_Range_Minimum_Gain(args.sn, args.mode)
	Maximum_Gain = instance.Get_Dynamic_Range_Maximum_Gain(args.sn, args.mode)

	while True:
		print("================================================================================")
		print("Usage :")
		print("ch1_db : In range(%f, %f, 0.5)" %(Minimum_Gain, Maximum_Gain))
		print("ch2_db : In range(%f, %f, 0.5)" %(Minimum_Gain, Maximum_Gain))
		print("ch3_db : In range(%f, %f, 0.5)" %(Minimum_Gain, Maximum_Gain))
		print("ch4_db : In range(%f, %f, 0.5)" %(Minimum_Gain, Maximum_Gain))
		print("ch1_deg : In range(0, 360, 5)")
		print("ch2_deg : In range(0, 360, 5)")
		print("ch3_deg : In range(0, 360, 5)")
		print("ch4_deg : In range(0, 360, 5)")
		print("Program_Exit : ctrl + z")
		print("=================================================================================")

		arg = input("Target_ch1_db : ")
		Target_ch1_db = float(arg)
		if Target_ch1_db < Minimum_Gain or Target_ch1_db > Maximum_Gain:
			print("[BBOXLITE_ChannelControl][%s] Invalid Target_ch1_db argument" % (args.sn))
			sys.exit(1)

		arg = input("Target_ch1_deg : ")
		Target_ch1_deg = int(arg)
		if Target_ch1_deg < 0 or Target_ch1_deg > 360:
			print("[BBOXLITE_ChannelControl][%s] Invalid Target_ch1_deg argument" % (args.sn))
			sys.exit(1)

		arg = input("Target_ch2_db : ")
		Target_ch2_db = float(arg)
		if Target_ch2_db < Minimum_Gain or Target_ch2_db > Maximum_Gain:
			print("[BBOXLITE_ChannelControl][%s] Invalid Target_ch2_db argument" % (args.sn))
			sys.exit(1)
   
		arg = input("Target_ch2_deg : ")
		Target_ch2_deg = int(arg)
		if Target_ch2_deg < 0 or Target_ch2_deg > 360:
			print("[BBOXLITE_ChannelControl][%s] Invalid Target_ch2_deg argument" % (args.sn))
			sys.exit(1)

		arg = input("Target_ch3_db : ")
		Target_ch3_db = float(arg)
		if Target_ch3_db < Minimum_Gain or Target_ch3_db > Maximum_Gain:
			print("[BBOXLITE_ChannelControl][%s] Invalid Target_ch3_db argument" % (args.sn))
			sys.exit(1)

		arg = input("Target_ch3_deg : ")
		Target_ch3_deg = int(arg)
		if Target_ch3_deg < 0 or Target_ch3_deg > 360:
			print("[BBOXLITE_ChannelControl][%s] Invalid Target_ch3_deg argument" % (args.sn))
			sys.exit(1)

		arg = input("Target_ch4_db : ")
		Target_ch4_db = float(arg)
		if Target_ch4_db < Minimum_Gain or Target_ch4_db > Maximum_Gain:
			print("[BBOXLITE_ChannelControl][%s] Invalid Target_ch4_db argument" % (args.sn))
			sys.exit(1)
   
		arg = input("Target_ch4_deg : ")
		Target_ch4_deg = int(arg)
		if Target_ch4_deg < 0 or Target_ch4_deg > 360:
			print("[BBOXLITE_ChannelControl][%s] Invalid Target_ch4_deg argument" % (args.sn))
			sys.exit(1)

		instance.SetDeviceGainPhase(args.sn, args.mode, Target_ch1_db, Target_ch1_deg, Target_ch2_db, Target_ch2_deg, Target_ch3_db, Target_ch3_deg, Target_ch4_db, Target_ch4_deg)
			
		instance.Get_Device_settings(args.sn, args.mode)
