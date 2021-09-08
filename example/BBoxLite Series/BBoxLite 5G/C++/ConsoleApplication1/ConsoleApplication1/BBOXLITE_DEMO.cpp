#include "stdio.h"
#include "pch.h"

#include <iostream>
#include <string>
#include <array>
#include <msclr/marshal.h>
#include <msclr/marshal_cppstd.h>

using namespace System;
using namespace BBoxAPI;
using namespace msclr::interop;


int main()
{
	int dev_num = 0;
	BBoxAPI::retCode ^ ret;
	
	int STANDBY = 0;
	int TX = 1;
	int RX = 2;
	int SLEEP = 3;

	double TX_MIN_GAIN = 0;
	double TX_MAX_GAIN = 0;
	double RX_MIN_GAIN = 0;
	double RX_MAX_GAIN = 0;

	double TX_COM_MIN_GAIN = 0;
	double TX_COM_MAX_GAIN = 0;
	double RX_COM_MIN_GAIN = 0;
	double RX_COM_MAX_GAIN = 0;

	double TX_ELE_DR = 0;
	double RX_ELE_DR = 0;

	// GetDeviceStatus
	BBoxAPI::BBoxOneAPI ^instance = gcnew BBoxAPI::BBoxOneAPI();

	array<String ^>^ dev_info = instance->ScanningDevice((BBoxAPI::DEV_SCAN_MODE)0);
	dev_num = dev_info->Length;

	for (int i = 0; i < dev_num; i++)
	{
		array<String ^> ^ response_message = dev_info[i]->Split(',');	

		String ^ sn = response_message[0];
		std::string SN = msclr::interop::marshal_as<std::string>(sn);
		String ^ ip = response_message[1];
		std::string IP = msclr::interop::marshal_as<std::string>(ip);
		String ^ dev_type = response_message[2];
		std::string DEV_TYPE = msclr::interop::marshal_as<std::string>(dev_type);
		int devtype = std::stoi(DEV_TYPE);

		ret = instance->Init(sn, devtype, i);

		array<String ^> ^ freq_list = instance->getFrequencyList(sn);
		String ^ freq = freq_list[0];
		std::string FREQ = msclr::interop::marshal_as<std::string>(freq);
		double operating_freq = std::stod(FREQ);
		ret = instance->setOperatingFreq(operating_freq, sn);

		array<Double, 2> ^ DR = instance->getDR(sn);
		TX_MIN_GAIN = DR[0, 0];
		TX_MAX_GAIN = DR[0, 1];
		RX_MIN_GAIN = DR[1, 0];
		RX_MAX_GAIN = DR[1, 1];

		array<Double, 2> ^ COM_DR = instance->getCOMDR(sn);
		TX_COM_MIN_GAIN = COM_DR[0, 0];
		TX_COM_MAX_GAIN = COM_DR[0, 1];
		RX_COM_MIN_GAIN = COM_DR[1, 0];
		RX_COM_MAX_GAIN = COM_DR[1, 1];

		array<Double, 2> ^ ELE_DR = instance->getELEDR(sn);
		TX_ELE_DR = ELE_DR[0, 0];
		RX_ELE_DR = ELE_DR[0, 1];

		array<String ^> ^ AAkitList = instance->getAAKitList(sn);
		
		if (devtype == 7)
		{
			instance->selectAAKit("TMYTEK_28LITE_4x4_C2104L020-28", sn);
		}
		else if (devtype == 8)
		{
			instance->selectAAKit("TMYTEK_39LITE_4x4_A2104L004-39", sn);
		}

		Console::WriteLine("======================================================");
		Console::WriteLine("[DEMO1] Switch TX mode");
		system("pause");

		instance->SwitchTxRxMode(TX, sn);
		int mode = instance->getTxRxMode(sn);
		Console::WriteLine("[DEMO1] Mode : " + mode);

		Console::WriteLine("======================================================");
		Console::WriteLine("[DEMO2] Channel power control : Off channel 1 power");
		system("pause");

		int board = 1;
		int channel = 1;
		int sw = 1;
		instance->switchChannelPower(board, channel, sw, sn);
		Console::WriteLine("[DEMO2] Channel 1 power off");

		Console::WriteLine("======================================================");
		Console::WriteLine("[DEMO3] Channel Gain/Phase Control");
		Console::WriteLine("[DEMO3] Channel_1 gain  : 15 db");
		Console::WriteLine("[DEMO3] Channel_1 phase : 15 deg");
		Console::WriteLine("[DEMO3] Channel_2 gain  : 15 db");
		Console::WriteLine("[DEMO3] Channel_2 phase : 30 deg");
		Console::WriteLine("[DEMO3] Channel_3 gain  : 15 db");
		Console::WriteLine("[DEMO3] Channel_3 phase : 45 deg");
		Console::WriteLine("[DEMO3] Channel_4 gain  : 15 db");
		Console::WriteLine("[DEMO3] Channel_4 phase : 60 deg");
		system("pause");

		board = 1;

		channel = 1;
		double Target_db = 15;
		int Target_deg = 15;
		instance->setChannelGainPhase(board, channel, Target_db, Target_deg, sn);

		channel = 2;
		Target_db = 15;
		Target_deg = 30;
		instance->setChannelGainPhase(board, channel, Target_db, Target_deg, sn);

		channel = 3;
		Target_db = 15;
		Target_deg = 45;
		instance->setChannelGainPhase(board, channel, Target_db, Target_deg, sn);

		channel = 4;
		Target_db = 15;
		Target_deg = 60;
		instance->setChannelGainPhase(board, channel, Target_db, Target_deg, sn);

		Console::WriteLine("======================================================");
		Console::WriteLine("[DEMO4] BeamSteering Control");
		system("pause");
		Console::WriteLine("[DEMO4] Channel gain  : 12 db");
		Console::WriteLine("[DEMO4] Beam angle : 15 ");

		Target_db = 12;
		int Target_angle_x = 15;
		int Target_angle_y = 0;
		instance->setBeamXY(Target_db, Target_angle_x, Target_angle_y, sn);
	}

	Console::WriteLine("======================================================");
	Console::WriteLine("[DEMO] End");
	system("pause");
}
