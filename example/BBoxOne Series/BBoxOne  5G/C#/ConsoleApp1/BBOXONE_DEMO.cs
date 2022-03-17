using System;
using System.Linq;
using System.Collections.Generic;
using BBoxAPI;


namespace BBOXONE_DEMO
{
    class BBOXONE_CONTROL_DEMO
    {
        const int scanning_mode = 0;

        const int TX = 1;
        const int RX = 2;

        static double[,] DR = null;

        static double TX_MIN_GAIN = 0;
        static double TX_MAX_GAIN = 0;
        static double RX_MIN_GAIN = 0;
        static double RX_MAX_GAIN = 0;

        static string[] AAkitList = null;


        static void Main(string[] args)
        {
            string sn = null;
            string[] dev_info = null;
            int DEV_NUM = 0;

            BBoxOneAPI instance = new BBoxOneAPI();

            dev_info = instance.ScanningDevice(scanning_mode);
            
            DEV_NUM = dev_info.Count();

            for (int i = 0; i < DEV_NUM; i++)
            {
                string[] response_message = dev_info[i].Split(',');
                sn = response_message[0];
                instance.Init(sn, 0, i);

                string[] freq_list = instance.getFrequencyList(sn);

                instance.setOperatingFreq(Convert.ToDouble(freq_list[0]), sn);

                DR = instance.getDR(sn);
                TX_MIN_GAIN = DR[0, 0];
		        TX_MAX_GAIN = DR[0, 1];
		        RX_MIN_GAIN = DR[1, 0];
		        RX_MAX_GAIN = DR[1, 1];

                AAkitList = instance.getAAKitList(sn);
		        instance.selectAAKit(AAkitList[0], sn);

                Console.WriteLine("======================================================");
		        Console.WriteLine("[DEMO1][{0}] Switch TX mode", sn);
		        Console.ReadKey();
                instance.SwitchTxRxMode(TX, sn);
                int mode = instance.getTxRxMode(sn);
		        Console.WriteLine("[DEMO1][{0}] Mode : " + mode, sn);

                Console.WriteLine("======================================================");
		        Console.WriteLine("[DEMO2][{0}] Channel power control : Off channel 1 power");
		        Console.ReadKey();

                int board = 1;
		        int channel = 1;
		        int sw = 1;
		        instance.switchChannelPower(board, channel, sw, sn);
		        Console.WriteLine("[DEMO2][{0}] Channel 1 power off");

		        double Target_db = TX_MAX_GAIN;
		        int Target_ch1_deg = 15;
				int Target_ch2_deg = 30;
				int Target_ch3_deg = 45;
				int Target_ch4_deg = 60;

                Console.WriteLine("======================================================");
		        Console.WriteLine("[DEMO3][{0}] Channel Gain/Phase Control", sn);
		        Console.WriteLine("[DEMO3][{0}] Channel_1 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[DEMO3][{0}] Channel_1 phase : {1} deg", sn, Target_ch1_deg);
		        Console.WriteLine("[DEMO3][{0}] Channel_2 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[DEMO3][{0}] Channel_2 phase : {1} deg", sn, Target_ch2_deg);
		        Console.WriteLine("[DEMO3][{0}] Channel_3 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[DEMO3][{0}] Channel_3 phase : {1} deg", sn, Target_ch3_deg);
		        Console.WriteLine("[DEMO3][{0}] Channel_4 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[DEMO3][{0}] Channel_4 phase : {1} deg", sn, Target_ch4_deg);
		        Console.ReadKey();

                board = 1;

		        channel = 1;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_ch1_deg, sn);

		        channel = 2;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_ch2_deg, sn);

		        channel = 3;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_ch3_deg, sn);

		        channel = 4;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_ch4_deg, sn);

				Target_ch1_deg = 45;
				Target_ch2_deg = 60;
				Target_ch3_deg = 75;
				Target_ch4_deg = 90;

                Console.WriteLine("======================================================");
		        Console.WriteLine("[DEMO3][{0}] Channel Gain/Phase Control", sn);
		        Console.WriteLine("[DEMO3][{0}] Channel_5 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[DEMO3][{0}] Channel_5 phase : {1} deg", sn, Target_ch1_deg);
		        Console.WriteLine("[DEMO3][{0}] Channel_6 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[DEMO3][{0}] Channel_6 phase : {1} deg", sn, Target_ch2_deg);
		        Console.WriteLine("[DEMO3][{0}] Channel_7 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[DEMO3][{0}] Channel_7 phase : {1} deg", sn, Target_ch3_deg);
		        Console.WriteLine("[DEMO3][{0}] Channel_8 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[DEMO3][{0}] Channel_8 phase : {1} deg", sn, Target_ch4_deg);
		        Console.ReadKey();

                board = 2;

		        channel = 1;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_ch1_deg, sn);

		        channel = 2;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_ch2_deg, sn);

		        channel = 3;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_ch3_deg, sn);

		        channel = 4;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_ch4_deg, sn);

		        Target_db = TX_MAX_GAIN - 2;
		        int Target_theta = 15;
		        int Target_phi = 30;

                Console.WriteLine("======================================================");
		        Console.WriteLine("[DEMO4][{0}] BeamSteering Control", sn);
		        Console.ReadKey();
		        Console.WriteLine("[DEMO4][{0}] Channel gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[DEMO4][{0}] Theta : {1} ", sn, Target_theta);
		        Console.WriteLine("[DEMO4][{0}] Phi : {1} ", sn, Target_phi);

		        instance.setBeamAngle(Target_db, Target_theta, Target_phi, sn);
            }

            Console.WriteLine("======================================================");
	        Console.WriteLine("[DEMO] End", sn);
		    Console.ReadKey();
        }
    }
}
