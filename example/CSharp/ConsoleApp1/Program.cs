//#define MULTIPLEBBOXONE

using System;
using System.Linq;
using BBoxAPI;

namespace ConsoleApp1
{
    public class Class1 : MarshalByRefObject
    {
        public void callConstructor()
        {
            BBoxOneAPI b = new BBoxOneAPI();
        }
    }
    enum TRMODE
    {
        TX = 0,
        RX = 1,
    };
    class Program
    {
        static void Main(string[] args)
        {
            BBoxOneAPI b = new BBoxOneAPI();
            string[] dev_info = b.ScanningDevice();

            for (int i = 0; i < dev_info.Count(); i++)
            {
                string p = dev_info[i];
                if (p != "")
                    Console.WriteLine("device info from API side : " + p);
            }

            Console.WriteLine("dll location : ", b.GetCurrentPath());

            /* It will send the init command to BBox. */
            /* first BBoxOne */
            string s_info_1 = b.Init("B19312200-24", 0);
            Console.WriteLine(s_info_1);
            Console.WriteLine("Init first one");

            double dev_1_spacing = b.selectAntenna(Device.AntennaType.FOURBYFOUR, 0);
            Console.WriteLine("1st device antenna spacing : " + dev_1_spacing);
            b.SwitchTxRxMode((int)TRMODE.TX, 0);

#if MULTIPLEBBOXONE
            /* second BBoxOne */
            String s_info_2 = b.Init("B19178000-24", 1);
            Console.WriteLine(s_info_2);
            Console.WriteLine("Init second one");
            double dev_2_spacing = b.selectAntenna(Device.AntennaType.FOURBYFOUR, 1);
            Console.WriteLine("2nd device antenna spacing : " + dev_2_spacing);
            b.SwitchTxRxMode((int)TRMODE.TX, 1);
#endif 

            long start_milliseconds = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
          
            int deg = 0;
            int dir = -1;
            for(int count = 0; count < 1000; count++)
            {
                try
                {
                    s_info_1 = b.setBeamX(5/*dB*/, deg/*degree*/, 0);
                    s_info_1 = b.setBeamY(5/*dB*/, deg/*degree*/, 0);
                    s_info_1 = b.setBeamXY(5/*dB*/, deg/*degree*/, deg/*degree*/, 0);
                    Console.WriteLine("Firsr Device control : " + s_info_1);
#if MULTIPLEBBOXONE
          
                    s_info_2 = b.setBeamX(0, deg, 1);
                    s_info_2 = b.setBeamY(0, deg, 1);
                    s_info_2 = b.setBeamXY(0, deg, deg, 1);
                    Console.WriteLine("Second Device control : " + s_info_2);
#endif
      
                    if (deg <= -25)
                        dir = 1;
                    else if (deg >= 25)
                        dir = -1;
                    deg += dir;
                }
                catch (Exception e)
                {
                    Console.WriteLine("EEROR : " + e.ToString());
                }
            }
            long end_milliseconds = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
            Console.WriteLine("Time : " + (end_milliseconds - start_milliseconds) + " ms");
        
            Console.Read();
        }
    }
}
