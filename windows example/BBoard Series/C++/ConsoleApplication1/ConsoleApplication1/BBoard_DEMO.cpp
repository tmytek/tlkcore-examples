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

    if ((dev_num == 1) && (dev_info[0] == "Result,NoDeviceFound,-1"))
    {
        Console::WriteLine("[DEMO] No device found");
    }
    else
    {
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

            ret = instance->Init(sn, devtype);

            Console::WriteLine("======================================================");
            Console::WriteLine("[{0}][DEMO1] Switch TX mode", sn);
            system("pause");

            instance->SwitchTxRxMode(TX, sn);
            int mode = instance->getTxRxMode(sn);
            Console::WriteLine("[{0}][DEMO1] Mode : " + mode, sn);

            Console::WriteLine("======================================================");
            Console::WriteLine("[{0}][DEMO2] Channel power control : Off channel 1 power", sn);
            system("pause");

            int board = 1;
            int channel = 1;
            int sw = 1;
            instance->switchChannelPower(board, channel, sw, sn);
            Console::WriteLine("[{0}][DEMO2] Channel 1 power off", sn);

            int gain_step = 1;

            Console::WriteLine("======================================================");
            Console::WriteLine("[{0}][DEMO3] Channel Element Gain Step Control", sn);
            Console::WriteLine("[{0}][DEMO3] Channel_1 gain step : {1}", sn, gain_step);
            Console::WriteLine("[{0}][DEMO3] Channel_2 gain step : {1}", sn, gain_step);
            Console::WriteLine("[{0}][DEMO3] Channel_3 gain step : {1}", sn, gain_step);
            Console::WriteLine("[{0}][DEMO3] Channel_4 gain step : {1}", sn, gain_step);

            system("pause");

            board = 1;

            channel = 1;
            instance->setChannelGainStep(board, channel, gain_step, sn);

            channel = 2;
            instance->setChannelGainStep(board, channel, gain_step, sn);

            channel = 3;
            instance->setChannelGainStep(board, channel, gain_step, sn);

            channel = 4;
            instance->setChannelGainStep(board, channel, gain_step, sn);

            Console::WriteLine("======================================================");
            Console::WriteLine("[{0}][DEMO4] Common Gain Step Control", sn);
            Console::WriteLine("[{0}][DEMO4] Com gain step : {1}", sn, gain_step);

            system("pause");

            instance->setCommonGainStep(board, gain_step, sn);

            int phase_step = 1;

            Console::WriteLine("======================================================");
            Console::WriteLine("[{0}][DEMO5] Channel Element Phase Step Control", sn);
            Console::WriteLine("[{0}][DEMO5] Channel_1 phase step : {1}", sn, phase_step);
            Console::WriteLine("[{0}][DEMO5] Channel_2 phase step : {1}", sn, phase_step);
            Console::WriteLine("[{0}][DEMO5] Channel_3 phase step : {1}", sn, phase_step);
            Console::WriteLine("[{0}][DEMO5] Channel_4 phase step : {1}", sn, phase_step);

            system("pause");

            board = 1;

            channel = 1;
            instance->setChannelPhaseStep(board, channel, phase_step, sn);

            channel = 2;
            instance->setChannelPhaseStep(board, channel, phase_step, sn);

            channel = 3;
            instance->setChannelPhaseStep(board, channel, phase_step, sn);

            channel = 4;
            instance->setChannelPhaseStep(board, channel, phase_step, sn);

            Console::WriteLine("======================================================");
            Console::WriteLine("[{0}][DEMO5] Get temperature adc", sn);

            system("pause");

            Console::WriteLine("[{0}][DEMO5] Get temperature adc : {1}", sn, instance->getTemperatureADC(sn)[0]);
        }
    }


	Console::WriteLine("======================================================");
	Console::WriteLine("[DEMO] End");
	system("pause");

	return 0;
}
