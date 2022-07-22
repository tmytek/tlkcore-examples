using System;
using System.Linq;
using BBoxAPI;


namespace BBoxLite_DEMO
{
    class BBOXONE_CONTROL_DEMO
    {
        const int scanning_mode = 0;

		const int STANDBY = 0;
        const int TX = 1;
        const int RX = 2;
		const int SLEEP = 3;

        static double[,] DR = null;

        static double TX_MIN_GAIN = 0;
        static double TX_MAX_GAIN = 0;
        static double RX_MIN_GAIN = 0;
        static double RX_MAX_GAIN = 0;

        static string[] AAkitList = null;


        static void Main(string[] args)
        {
            string sn = null;
			string ip = null;
            string[] dev_info = null;
            int DEV_NUM = 0;
			int DEV_TYPE = 0;

            BBoxOneAPI instance = new BBoxOneAPI();

            dev_info = instance.ScanningDevice(scanning_mode);
            
            DEV_NUM = dev_info.Count();

            for (int i = 0; i < DEV_NUM; i++)
            {
                string[] response_message = dev_info[i].Split(',');
                sn = response_message[0];
				ip = response_message[1];
				DEV_TYPE = Convert.ToInt32(response_message[2]);
                instance.Init(sn, DEV_TYPE, i);

                string[] freq_list = instance.getFrequencyList(sn);

                instance.setOperatingFreq(Convert.ToDouble(freq_list[0]), sn);

                DR = instance.getDR(sn);
                TX_MIN_GAIN = DR[0, 0];
		        TX_MAX_GAIN = DR[0, 1];
		        RX_MIN_GAIN = DR[1, 0];
		        RX_MAX_GAIN = DR[1, 1];

                AAkitList = instance.getAAKitList(sn);

				if (DEV_TYPE == 7)
				{
					instance.selectAAKit("TMYTEK_28LITE_4x4_C2104L020-28", sn);
				}
				else if (DEV_TYPE == 8)
				{
					instance.selectAAKit("TMYTEK_39LITE_4x4_A2104L004-39", sn);
				}

                Console.WriteLine("======================================================");
		        Console.WriteLine("[{0}][DEMO1] Switch TX mode", sn);
		        Console.ReadKey();
                instance.SwitchTxRxMode(TX, sn);
                int mode = instance.getTxRxMode(sn);
		        Console.WriteLine("[{0}][DEMO1] Mode : " + mode, sn);

                Console.WriteLine("======================================================");
		        Console.WriteLine("[{0}][DEMO2] Channel power control : Off channel 1 power", sn);
		        Console.ReadKey();

                int board = 1;
		        int channel = 1;
		        int sw = 1;
		        instance.switchChannelPower(board, channel, sw, sn);
		        Console.WriteLine("[DEMO2] Channel 1 power off", sn);

		        double Target_db = 15;
		        int Target_ch1_deg = 15;
				int Target_ch2_deg = 30;
				int Target_ch3_deg = 45;
				int Target_ch4_deg = 60;

                Console.WriteLine("======================================================");
		        Console.WriteLine("[{0}][DEMO3] Channel Gain/Phase Control", sn);
		        Console.WriteLine("[{0}][DEMO3] Channel_1 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[{0}][DEMO3] Channel_1 phase : {1} deg", sn, Target_ch1_deg);
		        Console.WriteLine("[{0}][DEMO3] Channel_2 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[{0}][DEMO3] Channel_2 phase : {1} deg", sn, Target_ch2_deg);
		        Console.WriteLine("[{0}][DEMO3] Channel_3 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[{0}][DEMO3] Channel_3 phase : {1} deg", sn, Target_ch3_deg);
		        Console.WriteLine("[{0}][DEMO3] Channel_4 gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[{0}][DEMO3] Channel_4 phase : {1} deg", sn, Target_ch4_deg);
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

                Console.WriteLine("======================================================");
		        Console.WriteLine("[{0}][DEMO4] BeamSteering Control", sn);
		        Console.ReadKey();

		        Target_db = 12;
		        int Target_theta = 15;
		        int Target_phi = 0;

		        Console.WriteLine("[{0}][DEMO4] Channel gain  : {1} db", sn, Target_db);
		        Console.WriteLine("[{0}][DEMO4] Theta : {1} ", sn, Target_theta);
				Console.WriteLine("[{0}][DEMO4] Phi : {1} ", sn, Target_phi);

		        instance.setBeamAngle(Target_db, Target_theta, Target_phi, sn);
            }

            Console.WriteLine("======================================================");
	        Console.WriteLine("[{0}][DEMO] End", sn);
		    Console.ReadKey();
        }
    }
}
