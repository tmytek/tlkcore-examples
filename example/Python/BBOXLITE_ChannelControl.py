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
	parser.add_argument("--ch1_switch", help="Integer argument : ON - 0 , OFF - 1", type=int)
	parser.add_argument("--ch2_switch", help="Integer argument : ON - 0 , OFF - 1", type=int)
	parser.add_argument("--ch3_switch", help="Integer argument : ON - 0 , OFF - 1", type=int)
	parser.add_argument("--ch4_switch", help="Integer argument : ON - 0 , OFF - 1", type=int)
	parser.add_argument("--ch1_db", help="Float argument : Channel 1 gain settings in range(DynamicRange_MIN_GAIN, DynamicRange_MAX_GAIN, 0.5)", type=float)
	parser.add_argument("--ch2_db", help="Float argument : Channel 2 gain settings in range(DynamicRange_MIN_GAIN, DynamicRange_MAX_GAIN, 0.5)", type=float)
	parser.add_argument("--ch3_db", help="Float argument : Channel 3 gain settings in range(DynamicRange_MIN_GAIN, DynamicRange_MAX_GAIN, 0.5)", type=float)
	parser.add_argument("--ch4_db", help="Float argument : Channel 4 gain settings in range(DynamicRange_MIN_GAIN, DynamicRange_MAX_GAIN, 0.5)", type=float)
	parser.add_argument("--ch1_deg", help="Integer argument : Channel 1 phase settings in range(0, 360, 5)", type=int)
	parser.add_argument("--ch2_deg", help="Integer argument : Channel 2 phase settings in range(0, 360, 5)", type=int)
	parser.add_argument("--ch3_deg", help="Integer argument : Channel 3 phase settings in range(0, 360, 5)", type=int)
	parser.add_argument("--ch4_deg", help="Integer argument : Channel 4 phase settings in range(0, 360, 5)", type=int)

	args = parser.parse_args()

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	if args.mode != 1 and args.mode != 2:
		print("[MAIN][%s] Invalid mode argument")
		sys.exit(1)
	elif args.ch1_switch != 0 and args.ch1_switch != 1:
		print("[MAIN][%s] Invalid ch1_switch argument")
		sys.exit(1)
	elif args.ch2_switch != 0 and args.ch2_switch != 1:
		print("[MAIN][%s] Invalid ch2_switch argument")
		sys.exit(1)
	elif args.ch3_switch != 0 and args.ch3_switch != 1:
		print("[MAIN][%s] Invalid ch3_switch argument")
		sys.exit(1)
	elif args.ch4_switch != 0 and args.ch4_switch != 1:
		print("[MAIN][%s] Invalid ch4_switch argument")
		sys.exit(1)
	elif args.ch1_deg < 0 or args.ch1_deg > 360:
		print("[MAIN][%s] Invalid ch1_deg argument")
		sys.exit(1)
	elif args.ch2_deg < 0 or args.ch2_deg > 360:
		print("[MAIN][%s] Invalid ch2_deg argument")
		sys.exit(1)
	elif args.ch3_deg < 0 or args.ch3_deg > 360:
		print("[MAIN][%s] Invalid ch3_deg argument")
		sys.exit(1)
	elif args.ch4_deg < 0 or args.ch4_deg > 360:
		print("[MAIN][%s] Invalid ch4_deg argument")
		sys.exit(1)

	obj = BBox_Control_Interface()

	if obj.Get_SN_Index(args.sn) == -1:
		print("[MAIN][%s] Invalid sn " % (args.sn))

	Dynamic_Range = obj.Get_Dynamic_Range(args.sn, args.mode)
	min_gain = Dynamic_Range[0]
	max_gain = Dynamic_Range[1]

	if args.ch1_db < min_gain or args.ch1_db > max_gain:
		print("[MAIN][%s] Invalid ch1_db argument")
		sys.exit(1)
	elif args.ch2_db < min_gain or args.ch2_db > max_gain:
		print("[MAIN][%s] Invalid ch2_db argument")
		sys.exit(1)
	elif args.ch3_db < min_gain or args.ch3_db > max_gain:
		print("[MAIN][%s] Invalid ch3_db argument")
		sys.exit(1)
	elif args.ch4_db < min_gain or args.ch4_db > max_gain:
		print("[MAIN][%s]Invalid ch4_db argument")
		sys.exit(1)

	channel = 1
	obj.SwitchChannelPower(args.sn, args.mode, channel, args.ch1_switch)
	channel = 2
	obj.SwitchChannelPower(args.sn, args.mode, channel, args.ch2_switch)
	channel = 3
	obj.SwitchChannelPower(args.sn, args.mode, channel, args.ch3_switch)
	channel = 4
	obj.SwitchChannelPower(args.sn, args.mode, channel, args.ch4_switch)

	if obj.SetDeviceGainPhase(args.sn, args.mode, args.ch1_db, args.ch1_deg, args.ch2_db, args.ch2_deg, args.ch3_db, args.ch3_deg, args.ch4_db, args.ch4_deg):
		gain_settings = obj.Get_Channel_Gain_settings(args.sn, args.mode)
		phase_settings = obj.Get_Channel_Phase_settings(args.sn, args.mode)
		print("[MAIN][%s]" % (args.sn))
		print("[MAIN][%s] TX : channel_1 : %f db , %f deg" % (args.sn, gain_settings[0], phase_settings[0]))
		print("[MAIN][%s] TX : channel_2 : %f db , %f deg" % (args.sn, gain_settings[1], phase_settings[1]))
		print("[MAIN][%s] TX : channel_3 : %f db , %f deg" % (args.sn, gain_settings[2], phase_settings[2]))
		print("[MAIN][%s] TX : channel_4 : %f db , %f deg" % (args.sn, gain_settings[3], phase_settings[3]))
	else:
		print("[MAIN][%s] SetDeviceGainPhase failed" % (args.sn))



		

