using System;
using System.Linq;
using System.Collections.Generic;
using BBoxAPI;


namespace BBOXONE_DEMO
{
    class BBOXONE_CONTROL_DEMO
    {
        const int scanning_mode = 0;

        const int TX = 0;
        const int RX = 1;

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
		        Console.WriteLine("[DEMO1] Switch TX mode");
		        Console.ReadKey();
                instance.SwitchTxRxMode(TX, sn);
                int mode = instance.getTxRxMode(sn);
		        Console.WriteLine("[DEMO1] Mode : " + mode);

                Console.WriteLine("======================================================");
		        Console.WriteLine("[DEMO2] Channel power control : Off channel 1 power");
		        Console.ReadKey();

                int board = 1;
		        int channel = 1;
		        int sw = 1;
		        instance.switchChannelPower(board, channel, sw, sn);
		        Console.WriteLine("[DEMO2] Channel 1 power off");

                Console.WriteLine("======================================================");
		        Console.WriteLine("[DEMO3] Channel Gain/Phase Control");
		        Console.WriteLine("[DEMO3] Channel_1 gain  : 15 db");
		        Console.WriteLine("[DEMO3] Channel_1 phase : 15 deg");
		        Console.WriteLine("[DEMO3] Channel_2 gain  : 15 db");
		        Console.WriteLine("[DEMO3] Channel_2 phase : 30 deg");
		        Console.WriteLine("[DEMO3] Channel_3 gain  : 15 db");
		        Console.WriteLine("[DEMO3] Channel_3 phase : 45 deg");
		        Console.WriteLine("[DEMO3] Channel_4 gain  : 15 db");
		        Console.WriteLine("[DEMO3] Channel_4 phase : 60 deg");
		        Console.ReadKey();

                board = 1;

		        channel = 1;
		        double Target_db = 15;
		        int Target_deg = 15;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_deg, sn);

		        channel = 2;
		        Target_db = 15;
		        Target_deg = 30;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_deg, sn);

		        channel = 3;
		        Target_db = 15;
		        Target_deg = 45;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_deg, sn);

		        channel = 4;
		        Target_db = 15;
		        Target_deg = 60;
		        instance.setChannelGainPhase(board, channel, Target_db, Target_deg, sn);

                Console.WriteLine("======================================================");
		        Console.WriteLine("[DEMO4] BeamSteering Control");
		        Console.ReadKey();
		        Console.WriteLine("[DEMO4] Channel gain  : 12 db");
		        Console.WriteLine("[DEMO4] Beam angle : 15 ");

		        Target_db = 12;
		        int Target_angle_x = 15;
		        int Target_angle_y = 0;
		        instance.setBeamXY(Target_db, Target_angle_x, Target_angle_y, sn);
            }

            Console.WriteLine("======================================================");
	        Console.WriteLine("[DEMO] End");
		    Console.ReadKey();
        }
    }
}
