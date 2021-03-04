import sys
import clr
import time
import csv
import os
import numpy as np

dll_dir = os.getcwd()

dll_name = 'BBoxAPI.dll'
path = r'%s\\%s' % (dll_dir, dll_name)
clr.AddReference(path)

from BBoxAPI import *

class BBox_Control_Interface(object):

	scanning_mode = 0

	operating_freq = 28.0

	STANDBY = 0
	TX = 1
	RX = 2
	SLEEP = 0

	board = 1

	db_step = 0.5

	min_deg = 0
	max_deg = 360
	deg_step = 5

	min_angle = -30
	max_angle = 30
	angle_step = 30

	def __init__(self):
		self.instance = BBoxOneAPI()
		self.sn = []
		self.ip = []
		self.dev_type = []

		self.TX_MIN_GAIN = []
		self.TX_MAX_GAIN = []
		self.RX_MIN_GAIN = []
		self.RX_MAX_GAIN = []

		self.TX_COM_MIN_GAIN = []
		self.TX_COM_MAX_GAIN = []
		self.RX_COM_MIN_GAIN = []
		self.RX_COM_MAX_GAIN = []

		self.TX_ELE_DYNAMIC_RANGE = []
		self.RX_ELE_DYNAMIC_RANGE = []

		self.AAkitList = []

		self.mode = []

		self.current_TX_gain_settings = [[0 for i in range(4)] for j in range(16)]
		self.current_TX_phase_settings = [[0 for i in range(4)] for j in range(16)]
		self.current_TX_BeamAngle_settings = [0 for i in range(16)]

		self.current_RX_gain_settings = [[0 for i in range(4)] for j in range(16)]
		self.current_RX_phase_settings = [[0 for i in range(4)] for j in range(16)]
		self.current_RX_BeamAngle_settings = [0 for i in range(16)]

		if self.GetDeviceStatus():
			self.InitialDevice()


	def GetDeviceStatus(self):
		dev_info = self.instance.ScanningDevice(self.scanning_mode)
		self.device_num = len(dev_info)
		print("[BBox_Control_Interface][GetDeviceStatus] Number of device = %d" % (self.device_num))

		if self.device_num > 0:
			for i in range(0, self.device_num, 1):
	   
				print("[BBox_Control_Interface][GetDeviceStatus] Index : %d" % (i))
				print("[BBox_Control_Interface][GetDeviceStatus] device_num : %d" % (self.device_num))

				ret = dev_info[i].split(",")
				self.sn.append(ret[0])
				self.ip.append(ret[1])
				val = ret[2].split("\x00")
				Dev_type = int(val[0])
				self.dev_type.append(Dev_type)


				print("[BBox_Control_Interface][GetDeviceStatus] SN : %s" % (self.sn[i]))
				print("[BBox_Control_Interface][GetDeviceStatus] IP : %s" % (self.ip[i]))
				print("[BBox_Control_Interface][GetDeviceStatus] Device_type : %s" % (self.dev_type[i]))

			return True
		else:
			return False


	def InitialDevice(self):
		for i in range(0, self.device_num):

			self.instance.Init(self.sn[i], self.dev_type[i], i)
			self.mode.append(self.STANDBY)
			print("[BBox_Control_Interface][InitialDevice][%s] mode : %d" % (self.sn[i], self.mode[i]))

			freq_list = self.instance.getFrequencyList(self.sn[i])
			if len(freq_list) == 0:
				print("[BBox_Control_Interface][InitialDevice][%s] failed : return null" % (self.sn[i]))
			else:
				for item in freq_list:
					print("[BBox_Control_Interface][InitialDevice][%s] getFrequencyList: list %s" % (self.sn[i], item))

			ret = self.instance.setOperatingFreq(self.operating_freq, self.sn[i])
			if ret != 0:
				print("[BBox_Control_Interface][InitialDevice][%s] setOperatingFreq failed : error_code %d" % (self.sn[i], ret))

			DR = self.instance.getDR(self.sn[i])
			print("[BBox_Control_Interface][InitialDevice][%s] " % (self.sn[i]))
			self.TX_MIN_GAIN.append(DR[0, 0])
			print("[BBox_Control_Interface][InitialDevice][%s] TX_MIN_GAIN : %f" % (self.sn[i], self.TX_MIN_GAIN[i]))
			self.TX_MAX_GAIN.append(DR[0, 1])
			print("[BBox_Control_Interface][InitialDevice][%s] TX_MAX_GAIN : %f" % (self.sn[i], self.TX_MAX_GAIN[i]))
			self.RX_MIN_GAIN.append(DR[1, 0])
			print("[BBox_Control_Interface][InitialDevice][%s] RX_MIN_GAIN : %f" % (self.sn[i], self.RX_MIN_GAIN[i]))
			self.RX_MAX_GAIN.append(DR[1, 1])
			print("[BBox_Control_Interface][InitialDevice][%s] RX_MAX_GAIN : %f" % (self.sn[i], self.RX_MAX_GAIN[i]))
			for j in range(0,4):
				self.current_TX_gain_settings[i][j] = self.TX_MAX_GAIN[i]
				self.current_RX_gain_settings[i][j] = self.RX_MAX_GAIN[i]

			COMDR = self.instance.getCOMDR(self.sn[i])
			print("[BBox_Control_Interface][InitialDevice][%s]" % (self.sn[i]))
			self.TX_COM_MIN_GAIN.append(COMDR[0, 0])
			print("[BBox_Control_Interface][InitialDevice][%s] TX_COM_MIN_GAIN : %f" % (self.sn[i], self.TX_COM_MIN_GAIN[i]))
			self.TX_COM_MAX_GAIN.append(COMDR[0, 1])
			print("[BBox_Control_Interface][InitialDevice][%s] TX_COM_MAX_GAIN : %f" % (self.sn[i], self.TX_COM_MAX_GAIN[i]))
			self.RX_COM_MIN_GAIN.append(COMDR[1, 0])
			print("[BBox_Control_Interface][InitialDevice][%s] RX_COM_MIN_GAIN : %f" % (self.sn[i], self.RX_COM_MIN_GAIN[i]))
			self.RX_COM_MAX_GAIN.append(COMDR[1, 1])
			print("[BBox_Control_Interface][InitialDevice][%s] RX_COM_MAX_GAIN : %f" % (self.sn[i], self.RX_COM_MAX_GAIN[i]))

			ELEDR = self.instance.getELEDR(self.sn[i])
			print("[BBox_Control_Interface][InitialDevice][%s]" % (self.sn[i]))
			self.TX_ELE_DYNAMIC_RANGE.append(ELEDR[0, 0])
			print("[BBox_Control_Interface][InitialDevice][%s] TX_ELE_DYNAMIC_RANGE : %f" % (self.sn[i], self.TX_ELE_DYNAMIC_RANGE[i]))
			self.RX_ELE_DYNAMIC_RANGE.append(ELEDR[0, 1])
			print("[BBox_Control_Interface][InitialDevice][%s] RX_ELE_DYNAMIC_RANGE : %f" % (self.sn[i], self.RX_ELE_DYNAMIC_RANGE[i]))

			self.AAkitList.append(self.instance.getAAKitNameList(self.sn[i]))
			print(self.AAkitList[i][0])
			self.instance.selectAAKit(self.AAkitList[i][0], self.sn[i])


	def CheckElementDR(self, sn_idx, mode, gain_settings):
		
		Element_DR = 0

		if mode == self.TX:
			Element_DR = self.TX_ELE_DYNAMIC_RANGE[sn_idx]
		elif mode == self.RX:
			Element_DR = self.RX_ELE_DYNAMIC_RANGE[sn_idx]
		else:
			return False

		max_db = gain_settings[0]
		min_db = gain_settings[0]
		for i in range(1, 4):
			if gain_settings[i] > max_db:
				max_db = gain_settings[i]
			elif gain_settings[i] < min_db:
				min_db = gain_settings[i]
		
		if (max_db - min_db) > Element_DR:
			return False

		self.Adjust_gain_settings(mode, sn_idx, gain_settings, Element_DR)

		return True


	def Adjust_gain_settings(self, mode, sn_idx, gain_settings, ElementDR):

		while True:
			flag = True
			for i in range(0,4):
				if mode == self.TX:
					if abs(gain_settings[i] - self.current_TX_gain_settings[sn_idx][i]) > ElementDR:
						flag = False
				elif mode == self.RX:
					if abs(gain_settings[i] - self.current_RX_gain_settings[sn_idx][i]) > ElementDR:
						flag = False

			if flag == True:
				break
			else:
				for channel in range(1, 5):
					if mode == self.TX:
						self.current_TX_gain_settings[sn_idx][channel-1] = (self.current_TX_gain_settings[sn_idx][channel-1] - ElementDR)
						self.instance.setChannelGainPhase(self.board, channel, self.current_TX_gain_settings[sn_idx][channel-1], self.current_TX_phase_settings[sn_idx][channel-1], self.sn[sn_idx])
						

					elif mode == self.RX:
						self.current_RX_gain_settings[sn_idx][channel-1] = (self.current_RX_gain_settings[sn_idx][channel-1] - ElementDR)
						self.instance.setChannelGainPhase(self.board, channel, self.current_RX_gain_settings[sn_idx][channel-1], self.current_RX_phase_settings[sn_idx][channel-1], self.sn[sn_idx])



	def CheckTRMode(self, sn_idx, mode):

		if (mode == self.TX) or (mode == self.RX):
			self.SwitchDeviceMode(self.sn[sn_idx], mode)
			return True
		else:
			print("[BBox_Control_Interface][CheckTRMode] Invalid mode")

		return False

	def SwitchDeviceMode(self, sn, mode):

		if (mode == self.STANDBY) or (mode == self.TX) or (mode == self.RX) or (mode == self.SLEEP):

			sn_idx = self.Get_SN_Index(sn)
			if sn_idx == -1:
				return False

			if self.mode[sn_idx] != mode:
				self.instance.SwitchTxRxMode(mode, sn)
				self.mode[sn_idx] = mode
				return True
		else:
			print("[BBox_Control_Interface][SwitchDeviceMode] Invalid mode")
		
		return False

	def SwitchChannelPower(self, sn, mode, channel, switch):

		if (channel < 1) or (channel > 4) :
			print("[BBox_Control_Interface][SwitchChannelPower] Invalid channel number")
			return False

		sn_idx = self.Get_SN_Index(sn)
		if sn_idx == -1:
			return False

		if self.CheckTRMode(sn_idx, mode) == False:
			return False

		if switch == 0 or switch == 1:
			self.instance.switchChannelPower(self.board, channel, switch, self.sn[sn_idx])
		else:
			print("[BBox_Control_Interface][SwitchChannelPower] Invalid switch value")
			return False

		return True


	def SetDeviceGainPhase(self, sn, mode, ch1_db, ch1_deg, ch2_db, ch2_deg, ch3_db, ch3_deg, ch4_db, ch4_deg):

		sn_idx = self.Get_SN_Index(sn)
		if sn_idx == -1:
			return False

		if self.CheckTRMode(sn_idx, mode) == False:
			return False

		channel_gain_settings = [ch1_db, ch2_db, ch3_db, ch4_db]
		channel_phase_settings = [ch1_deg, ch2_deg, ch3_deg, ch4_deg]
  
		if self.CheckElementDR(sn_idx, mode, channel_gain_settings) == False:
			return False
  
		for channel in range(1, 5):
			if self.instance.setChannelGainPhase(self.board, channel, channel_gain_settings[channel-1], channel_phase_settings[channel-1], sn) == "OK":
				if mode == self.TX:
					self.current_TX_gain_settings[sn_idx][channel-1] = channel_gain_settings[channel-1]
					self.current_TX_phase_settings[sn_idx][channel-1] = channel_phase_settings[channel-1]
				elif mode == self.RX:
					self.current_RX_gain_settings[sn_idx][channel-1] = channel_gain_settings[channel-1]
					self.current_RX_phase_settings[sn_idx][channel-1] = channel_phase_settings[channel-1]
			else:
				print("[BBox_Control_Interface][SetDeviceGainPhase] SetDeviceGainPhase failed")
				return False

		return True



	def SetDeviceBeamSteering(self, sn, mode, db ,ang_x):

		sn_idx = self.Get_SN_Index(sn)
		if sn_idx == -1:
			return False

		if self.CheckTRMode(sn_idx, mode) == False:
			return False

		if mode == self.TX:
			self.current_TX_BeamAngle_settings[sn_idx] = ang_x
		elif mode == self.RX:
			self.current_RX_BeamAngle_settings[sn_idx] = ang_x

		ang_y = 0
		ret = self.instance.setBeamXY(db, ang_x, ang_y, sn)
		if ret != 0:
			print("[BBox_Control_Interface][SetDeviceBeamSteering] SetDeviceBeamSteering failed : errorCode %d" % (ret))
			return False

		return True

	def Get_Active_DeviceNum(self):

		return self.device_num

	def Get_SN_List(self):

		return self.sn

	def Get_SN_Index(self, sn):

		index = -1
		for i in range(0, self.device_num):
			if sn == self.sn[i]:
				index = i
				break

		if index == -1:
			print("[BBox_Control_Interface][Get_SN_Index] %s not exists" % (sn))

		return index

	def Get_Dynamic_Range(self, sn, mode):

		sn_idx = self.Get_SN_Index(sn)
		if sn_idx == -1:
			return None

		if mode == self.TX:
			return [self.TX_MIN_GAIN[sn_idx], self.TX_MAX_GAIN[sn_idx]]
		elif mode == self.RX:
			return [self.RX_MIN_GAIN[sn_idx], self.RX_MAX_GAIN[sn_idx]]


	def Get_Channel_Gain_settings(self, sn, mode):

		sn_idx = self.Get_SN_Index(sn)
		if sn_idx == -1:
			return None

		if mode == self.TX:
			return [self.current_TX_gain_settings[sn_idx][0], self.current_TX_gain_settings[sn_idx][1], self.current_TX_gain_settings[sn_idx][2], self.current_TX_gain_settings[sn_idx][3]]
		elif mode == self.RX:
			return [self.current_RX_gain_settings[sn_idx][0], self.current_RX_gain_settings[sn_idx][1], self.current_RX_gain_settings[sn_idx][2], self.current_RX_gain_settings[sn_idx][3]]


	def Get_Channel_Phase_settings(self, sn, mode):

		sn_idx = self.Get_SN_Index(sn)
		if sn_idx == -1:
			return None

		if mode == self.TX:
			return [self.current_TX_phase_settings[sn_idx][0], self.current_TX_phase_settings[sn_idx][1], self.current_TX_phase_settings[sn_idx][2], self.current_TX_phase_settings[sn_idx][3]]
		elif mode == self.RX:
			return [self.current_RX_phase_settings[sn_idx][0], self.current_RX_phase_settings[sn_idx][1], self.current_RX_phase_settings[sn_idx][2], self.current_RX_phase_settings[sn_idx][3]]


	def Get_BeamAngle_settings(self, sn, mode):

		sn_idx = self.Get_SN_Index(sn)
		if sn_idx == -1:
			return None

		if mode == self.TX:
			return self.current_TX_BeamAngle_settings[sn_idx]
		elif mode == self.RX:
			return self.current_RX_BeamAngle_settings[sn_idx]


if __name__ == '__main__':

	obj = BBox_Control_Interface()

	sn = obj.Get_SN_List()
	device_num = obj.Get_Active_DeviceNum()

	TX_DR = []
	RX_DR = []

	for i in range(0, device_num):
		print("[MAIN] %d. sn : %s" % (i, sn[i]))

		TX_DR.append(obj.Get_Dynamic_Range(sn[i], obj.TX))
		RX_DR.append(obj.Get_Dynamic_Range(sn[i], obj.RX))

		for db in np.arange(TX_DR[i][0], TX_DR[i][1], obj.db_step):
			for deg in np.arange(obj.min_deg, obj.max_deg, obj.deg_step):
				if obj.SetDeviceGainPhase(sn[i], obj.TX, db, deg, db, deg, db, deg, db, deg):
					print("[MAIN][SetDeviceGainPhase][%s] TX , %f db , %d deg" % (sn[i], db, deg))

					settings = obj.Get_Channel_Gain_settings(sn[i], obj.TX)
					print("[MAIN][Get_Channel_Gain_settings][%s]" % (sn[i]))
					print("[MAIN][Get_Channel_Gain_settings][%s] TX : channel_1 : %f db" % (sn[i], settings[0]))
					print("[MAIN][Get_Channel_Gain_settings][%s] TX : channel_2 : %f db" % (sn[i], settings[1]))
					print("[MAIN][Get_Channel_Gain_settings][%s] TX : channel_3 : %f db" % (sn[i], settings[2]))
					print("[MAIN][Get_Channel_Gain_settings][%s] TX : channel_4 : %f db" % (sn[i], settings[3]))

					settings = obj.Get_Channel_Phase_settings(sn[i], obj.TX)
					print("[MAIN][Get_Channel_Phase_settings][%s]" % (sn[i]))
					print("[MAIN][Get_Channel_Phase_settings][%s] TX : channel_1 : %f deg" % (sn[i], settings[0]))
					print("[MAIN][Get_Channel_Phase_settings][%s] TX : channel_2 : %f deg" % (sn[i], settings[1]))
					print("[MAIN][Get_Channel_Phase_settings][%s] TX : channel_3 : %f deg" % (sn[i], settings[2]))
					print("[MAIN][Get_Channel_Phase_settings][%s] TX : channel_4 : %f deg" % (sn[i], settings[3]))


		for db in np.arange(RX_DR[i][0], RX_DR[i][1], obj.db_step):
			for deg in np.arange(obj.min_deg, obj.max_deg, obj.deg_step):
				if obj.SetDeviceGainPhase(sn[i], obj.RX, db, deg, db, deg, db, deg, db, deg):
					print("[MAIN][SetDeviceGainPhase] RX : SN %s , RX %f db , %d deg" % (sn[i], db, deg))

					settings = obj.Get_Channel_Gain_settings(sn[i], obj.RX)
					print("[MAIN][Get_Channel_Gain_settings][%s]" % (sn[i]))
					print("[MAIN][Get_Channel_Gain_settings][%s] RX : channel_1 : %f db" % (sn[i], settings[0]))
					print("[MAIN][Get_Channel_Gain_settings][%s] RX : channel_2 : %f db" % (sn[i], settings[1]))
					print("[MAIN][Get_Channel_Gain_settings][%s] RX : channel_3 : %f db" % (sn[i], settings[2]))
					print("[MAIN][Get_Channel_Gain_settings][%s] RX : channel_4 : %f db" % (sn[i], settings[3]))

					settings = obj.Get_Channel_Phase_settings(sn[i], obj.RX)
					print("[MAIN][Get_Channel_Phase_settings][%s]" % (sn[i]))
					print("[MAIN][Get_Channel_Phase_settings][%s] RX : channel_1 : %f deg" % (sn[i], settings[0]))
					print("[MAIN][Get_Channel_Phase_settings][%s] RX : channel_2 : %f deg" % (sn[i], settings[1]))
					print("[MAIN][Get_Channel_Phase_settings][%s] RX : channel_3 : %f deg" % (sn[i], settings[2]))
					print("[MAIN][Get_Channel_Phase_settings][%s] RX : channel_4 : %f deg" % (sn[i], settings[3]))


		for db in np.arange(TX_DR[i][0], TX_DR[i][1], 0.5):
			for angle in np.arange(obj.min_angle, obj.max_angle, obj.angle_step):
				if obj.SetDeviceBeamSteering(sn[i], obj.TX, db, angle):
					print("[MAIN][SetDeviceBeamSteering][%s] TX , %f db , %d angle" % (sn[i], db, angle))


		for db in np.arange(RX_DR[i][0], RX_DR[i][1], 0.5):
			for angle in np.arange(obj.min_angle, obj.max_angle, obj.angle_step):
				if obj.SetDeviceBeamSteering(sn[i], obj.RX, db, angle):
					print("[MAIN][SetDeviceBeamSteering][%s] RX , %f db , %d angle" % (sn[i], db, angle))
