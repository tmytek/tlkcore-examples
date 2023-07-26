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
	
	int TX = 1;
	int RX = 2;

	double TX_MIN_GAIN = 0;
	double TX_MAX_GAIN = 0;
	double RX_MIN_GAIN = 0;
	double RX_MAX_GAIN = 0;

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

            ret = instance->Init(sn);

            if (instance->checkCaliTableLocation(sn))
            {
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

                array<String ^> ^ AAkitList = instance->getAAKitList(sn);
                instance->selectAAKit(AAkitList[0], sn);

                Console::WriteLine("======================================================");
                Console::WriteLine("[DEMO1][{0}] Switch TX mode", sn);
                system("pause");

                instance->SwitchTxRxMode(TX, sn);
                int mode = instance->getTxRxMode(sn);
                Console::WriteLine("[DEMO1][{0}] Mode : " + mode, sn);

                Console::WriteLine("======================================================");
                Console::WriteLine("[DEMO2][{0}] Channel power control : Off channel 1 and channel 5 power", sn);
                system("pause");

                int board = 1;
                int channel = 1;
                int sw = 1;
                instance->switchChannelPower(board, channel, sw, sn);
                Console::WriteLine("[DEMO2][{0}] Channel 1 power off", sn);

                board = 2;
                channel = 1;
                sw = 1;
                instance->switchChannelPower(board, channel, sw, sn);
                Console::WriteLine("[DEMO2][{0}] Channel 5 power off", sn);

                double Target_db = TX_MAX_GAIN;
                int Target_ch1_deg = 15;
                int Target_ch2_deg = 30;
                int Target_ch3_deg = 45;
                int Target_ch4_deg = 60;

                Console::WriteLine("======================================================");
                Console::WriteLine("[DEMO3][{0}] Channel Gain/Phase Control", sn);
                Console::WriteLine("[DEMO3][{0}] Channel_1 gain  : {1} db", sn, Target_db);
                Console::WriteLine("[DEMO3][{0}] Channel_1 phase : {1} deg", sn, Target_ch1_deg);
                Console::WriteLine("[DEMO3][{0}] Channel_2 gain  : {1} db", sn, Target_db);
                Console::WriteLine("[DEMO3][{0}] Channel_2 phase : {1} deg", sn, Target_ch2_deg);
                Console::WriteLine("[DEMO3][{0}] Channel_3 gain  : {1} db", sn, Target_db);
                Console::WriteLine("[DEMO3][{0}] Channel_3 phase : {1} deg", sn, Target_ch3_deg);
                Console::WriteLine("[DEMO3][{0}] Channel_4 gain  : {1} db", sn, Target_db);
                Console::WriteLine("[DEMO3][{0}] Channel_4 phase : {1} deg", sn, Target_ch4_deg);
                system("pause");

                board = 1;

                channel = 1;
                instance->setChannelGainPhase(board, channel, Target_db, Target_ch1_deg, sn);

                channel = 2;
                instance->setChannelGainPhase(board, channel, Target_db, Target_ch2_deg, sn);

                channel = 3;
                instance->setChannelGainPhase(board, channel, Target_db, Target_ch3_deg, sn);

                channel = 4;
                instance->setChannelGainPhase(board, channel, Target_db, Target_ch4_deg, sn);

                Target_ch1_deg = 45;
                Target_ch2_deg = 60;
                Target_ch3_deg = 75;
                Target_ch4_deg = 90;

                Console::WriteLine("======================================================");
                Console::WriteLine("[DEMO3][{0}] Channel Gain/Phase Control", sn);
                Console::WriteLine("[DEMO3][{0}] Channel_5 gain  : {1} db", sn, Target_db);
                Console::WriteLine("[DEMO3][{0}] Channel_5 phase : {1} deg", sn, Target_ch1_deg);
                Console::WriteLine("[DEMO3][{0}] Channel_6 gain  : {1} db", sn, Target_db);
                Console::WriteLine("[DEMO3][{0}] Channel_6 phase : {1} deg", sn, Target_ch2_deg);
                Console::WriteLine("[DEMO3][{0}] Channel_7 gain  : {1} db", sn, Target_db);
                Console::WriteLine("[DEMO3][{0}] Channel_7 phase : {1} deg", sn, Target_ch3_deg);
                Console::WriteLine("[DEMO3][{0}] Channel_8 gain  : {1} db", sn, Target_db);
                Console::WriteLine("[DEMO3][{0}] Channel_8 phase : {1} deg", sn, Target_ch4_deg);
                system("pause");

                board = 2;

                channel = 1;
                instance->setChannelGainPhase(board, channel, Target_db, Target_ch1_deg, sn);

                channel = 2;
                instance->setChannelGainPhase(board, channel, Target_db, Target_ch2_deg, sn);

                channel = 3;
                instance->setChannelGainPhase(board, channel, Target_db, Target_ch3_deg, sn);

                channel = 4;
                instance->setChannelGainPhase(board, channel, Target_db, Target_ch4_deg, sn);

                Console::WriteLine("======================================================");
                Console::WriteLine("[DEMO4][{0}] BeamSteering Control", sn);
                system("pause");

                Target_db = TX_MAX_GAIN - 2;
                int Target_theta = 15;
                int Target_phi = 30;

                Console::WriteLine("[DEMO4][{0}] Channel gain  : {1} db", sn, Target_db);
                Console::WriteLine("[DEMO4][{0}] Theta : {1} ", sn, Target_theta);
                Console::WriteLine("[DEMO4][{0}] Phi : {1} ", sn, Target_phi);

                instance->setBeamAngle(Target_db, Target_theta, Target_phi, sn);

                system("pause");
                Console::WriteLine("[{0}][DEMO5] Get board_1 temperature adc : {1}", sn, instance->getTemperatureADC(sn)[0]);
                Console::WriteLine("[{0}][DEMO5] Get board_2 temperature adc : {1}", sn, instance->getTemperatureADC(sn)[1]);
                Console::WriteLine("[{0}][DEMO5] Get board_3 temperature adc : {1}", sn, instance->getTemperatureADC(sn)[2]);
                Console::WriteLine("[{0}][DEMO5] Get board_4 temperature adc : {1}", sn, instance->getTemperatureADC(sn)[3]);
            }
            else
            {
                Console::WriteLine("[DEMO] Calibration table of {0} not exists in files folder" , sn);
            }
        }
    }

	Console::WriteLine("======================================================");
	Console::WriteLine("[DEMO] End");
	system("pause");
}
