//#define MULTIPLEBBOXONE

using System;
using System.Linq;


namespace ConsoleApp1
{
    using BBoxAPI;
    using System.Collections.Generic;

    public class Class1 : MarshalByRefObject
    {
        public void callConstructor()
        {
            BBoxOneAPI b = new BBoxOneAPI();
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            BBoxOneAPI b = new BBoxOneAPI();
            string[] dev_info = b.ScanningDevice();
            string s_info_1 = null;
            List<string> sn = new List<String>();
            
            for (int i = 0; i < dev_info.Count(); i++)
            {
                string p = dev_info[i];
                if (p != "")
                {
                    Console.WriteLine("device info from API side : " + p);
                    string[] info = dev_info[i].Split(',');
                    sn.Add(info[0]); // BBoxOne SN
                    s_info_1 = b.Init(info[0], 0/*BBoxOne*/, sn.Count-1);
                    Console.WriteLine(s_info_1);
                    b.selectAAKit("TMYTEK_8x8", sn[sn.Count - 1]);
                    b.SwitchTxRxMode(0, sn[sn.Count - 1]); // Tx mode
                }
            }
            
            
            long start_milliseconds = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;

            int deg = 10;

            // We expect only one BBoxOne here.
            for (int count = 0; count < 10; count++)
            {
                s_info_1 = "";
                try
                {
                    s_info_1 += b.setBeamX(0/*dB*/, deg/*degree*/, sn[0]);
                    s_info_1 += b.setBeamY(0/*dB*/, deg/*degree*/, sn[0]);
                    s_info_1 += b.setBeamXY(0/*dB*/, deg/*degree*/, deg/*degree*/, sn[0]);
                    Console.WriteLine("Device control : ");
                    Console.WriteLine(s_info_1);      
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
