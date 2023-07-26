using System;
using System.Linq;
using BBoxAPI;


namespace BBoard_DEMO
{
    class BBoard_Control_DEMO
    {
        const int scanning_mode = 0;

        const int STANDBY = 0;
        const int TX = 1;
        const int RX = 2;
        const int SLEEP = 3;


        static double TX_MIN_GAIN = 0;
        static double TX_MAX_GAIN = 0;
        static double RX_MIN_GAIN = 0;
        static double RX_MAX_GAIN = 0;

        static double[,] DR = null;
        static string[] AAkitList = null;


        static void Main(string[] args)
        {
            string sn = "";
            string ip = "";
            string[] dev_info = null;
            int DEV_NUM = 0;
            int DEV_TYPE = 0;

            BBoxOneAPI instance = new BBoxOneAPI();

            dev_info = instance.ScanningDevice(scanning_mode);
            
            DEV_NUM = dev_info.Count();

            if(DEV_NUM == 1 && dev_info[0] == "Result,NoDeviceFound,-1")
            {
                Console.WriteLine("[DEMO] No device found");
            }
            else
            {
                for (int i = 0; i < DEV_NUM; i++)
                {
                    string[] response_message = dev_info[i].Split(',');
                    sn = response_message[0];
                    ip = response_message[1];
                    DEV_TYPE = Convert.ToInt32(response_message[2]);

                    instance.Init(sn, DEV_TYPE);

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

                    int gain_step = 1;

                    Console.WriteLine("======================================================");
                    Console.WriteLine("[{0}][DEMO3] Channel Element Gain Step Control", sn);
                    Console.WriteLine("[{0}][DEMO3] Channel_1 gain step : {1}", sn, gain_step);
                    Console.WriteLine("[{0}][DEMO3] Channel_2 gain step : {1}", sn, gain_step);
                    Console.WriteLine("[{0}][DEMO3] Channel_3 gain step : {1}", sn, gain_step);
                    Console.WriteLine("[{0}][DEMO3] Channel_4 gain step : {1}", sn, gain_step);

                    Console.ReadKey();

                    board = 1;

                    channel = 1;
                    instance.setChannelGainStep(board, channel, gain_step, sn);

                    channel = 2;
                    instance.setChannelGainStep(board, channel, gain_step, sn);

                    channel = 3;
                    instance.setChannelGainStep(board, channel, gain_step, sn);

                    channel = 4;
                    instance.setChannelGainStep(board, channel, gain_step, sn);

                    Console.WriteLine("======================================================");
                    Console.WriteLine("[{0}][DEMO4] Common Gain Step Control", sn);
                    Console.WriteLine("[{0}][DEMO4] Com gain step : {1}", sn, gain_step);

                    Console.ReadKey();

                    instance.setCommonGainStep(board, gain_step, sn);


                    int phase_step = 1;

                    Console.WriteLine("======================================================");
                    Console.WriteLine("[{0}][DEMO5] Channel Element Phase Step Control", sn);
                    Console.WriteLine("[{0}][DEMO5] Channel_1 phase step : {1}", sn, phase_step);
                    Console.WriteLine("[{0}][DEMO5] Channel_2 phase step : {1}", sn, phase_step);
                    Console.WriteLine("[{0}][DEMO5] Channel_3 phase step : {1}", sn, phase_step);
                    Console.WriteLine("[{0}][DEMO5] Channel_4 phase step : {1}", sn, phase_step);

                    Console.ReadKey();

                    board = 1;

                    channel = 1;
                    instance.setChannelPhaseStep(board, channel, phase_step, sn);

                    channel = 2;
                    instance.setChannelPhaseStep(board, channel, phase_step, sn);

                    channel = 3;
                    instance.setChannelPhaseStep(board, channel, phase_step, sn);

                    channel = 4;
                    instance.setChannelPhaseStep(board, channel, phase_step, sn);

                    Console.WriteLine("======================================================");
                    Console.WriteLine("[{0}][DEMO5] Get temperature adc", sn);

                    Console.ReadKey();

                    var ret = instance.getTemperatureADC(sn);
                    Console.WriteLine("[{0}][DEMO5] Get temperature adc : {1}", sn, ret[0]);
                }
            }


            Console.WriteLine("======================================================");
            Console.WriteLine("[DEMO] End");
            Console.ReadKey();
        }
    }
}
