import sys
import csv
import time
import argparse
from BBOXLITE_Control_Interface import BBOXLITE_Control_Interface

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument("--sn", help="String_argument : D2046L001-28", type=str)
	parser.add_argument("--mode", help="Integer_argument : (TX, 1) , (RX, 2)", type=int)

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


	while True:
		print("================================================================================")
		print("Usage :")
		print("Channel_number : In range(1, 4)")
		print("Channel_switch : (ON, 0) , (OFF, 1)")
		print("Program_Exit : ctrl + z")
		print("=================================================================================")
  
		arg = input("Channel_number : ")
		channel = int(arg)
		if channel < 1 or channel > 4:
			print("[MAIN][%s] Invalid Channel_number argument" % (args.sn))
			sys.exit(1)

		arg = input("Channel_switch : ")
		switch = int(arg)
  
		if int(switch) != 0 and int(switch) != 1:
			print("[MAIN][%s] Invalid Channel_switch argument" % (args.sn))
			sys.exit(1)
  
		instance.SwitchChannelPower(args.sn, args.mode, channel, switch)

		instance.Get_Device_settings(args.sn, args.mode)




		

