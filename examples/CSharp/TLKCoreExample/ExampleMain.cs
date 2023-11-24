using Python.Runtime;
using System;
using System.IO;
using System.Reflection;

namespace TLKCoreExample
{
    class ExampleMain
    {
        static void Main(string[] args)
        {
            // Getting Python execute environment from environment: "Path"
            string env = Environment.GetEnvironmentVariable("Path");
            string[] array = env.Split(new[] { ";" }, StringSplitOptions.None);
            string pathToVirtualEnv = "";
            // Asign your Python version
            string PyVer = "38";
            foreach (var path in array)
            {
                if (path.Contains("Python"+ PyVer+"\\") && !path.Contains("Script")) {
                    pathToVirtualEnv = path;
                    break;
                }
            }
            Console.WriteLine($"Python installed path: {pathToVirtualEnv}\n");

            // Setting relative environment for execute Python, please update parameters from your real Python version 
            Runtime.PythonDLL = Path.Combine(pathToVirtualEnv, "python"+ PyVer + ".dll");
            PythonEngine.PythonHome = Path.Combine(pathToVirtualEnv, "python.exe");
            
            // Set default Python lib path and path to import TLKCore
            PythonEngine.PythonPath = $".;lib;{pathToVirtualEnv}\\Lib\\site-packages;{pathToVirtualEnv}\\Lib;{pathToVirtualEnv}\\DLLs";

            PythonEngine.Initialize();
            using (Py.GIL())
            {
                // Import modules which we need
                dynamic tlkcoreIns = Py.Import("TLKCoreService");
                dynamic tmy_public = Py.Import("TMYPublic");

                // Please keep this instance
                dynamic service = tlkcoreIns.TLKCoreService();
                Console.WriteLine("TLKCore version: v" + service.queryTLKCoreVer());

                dynamic dev_interface = tmy_public.DevInterface.ALL;
                dynamic ret = service.scanDevices(dev_interface.value);
                dynamic scanlist = ret.RetData;
                Console.WriteLine("Scanned device list: " + scanlist);

                ExampleMain example = new ExampleMain();
                foreach (string sn_addr_type in scanlist)
                {
                    dynamic element = sn_addr_type.Split(',');
                    string sn = element[0];
                    string addr = element[1];
                    string dev_type = element[2];
                    ret = service.initDev(sn);
                    if (ret.RetCode.value != tmy_public.RetCode.OK.value)
                    {
                        Console.WriteLine("Init failed, skip it");
                        continue;
                    }

                    string dev_name = service.getDevTypeName(sn);
                    if (dev_name.Contains("BBox")) {
                        dev_name = "BBox";
                    }
                    // Invoke example methods
                    Object[] param = { sn, service };
                    Console.WriteLine("Going to test " + dev_name);
                    example.GetType().InvokeMember("Test"+dev_name, BindingFlags.InvokeMethod, Type.DefaultBinder, example, param);
                }

                Console.WriteLine("Presss any key to exit ...");
                Console.ReadKey();
            }
        }
        public void TestBBox(string sn, dynamic service)
        {
            dynamic tmy_public = Py.Import("TMYPublic");

            dynamic mode = tmy_public.RFMode.TX;
            dynamic ret = service.setRFMode(sn, mode);
            Console.WriteLine("Set RF mode: {0}", ret.RetCode);
            ret = service.getRFMode(sn);
            Console.WriteLine("Get RF mode: {0}", ret);

            // Convert Python: list to C# array []
            dynamic freqList = service.getFrequencyList(sn).RetData;
            Console.WriteLine("Freq list: " + freqList);

            // Please edit your target freq
            Double targetFreq = 28.0;
            bool found = false;
            foreach (dynamic f in freqList)
            {
                if (f == targetFreq)
                {
                    found = true;
                    break;
                }
            }
            if (!found)
            {
                Console.WriteLine("Not support your target freq:{0} in freq list!", targetFreq);
                return;
            }

            ret = service.setOperatingFreq(sn, targetFreq);
            if (ret.RetCode.value != tmy_public.RetCode.OK.value)
            {
                Console.WriteLine("Set freq failed: " + ret);
                return;
            }
            Console.WriteLine("Set freq: {0}", ret);

            // Gain setting for BBoxOne/Lite
            dynamic rng = service.getDR(sn, mode).RetData;
            Console.WriteLine("DR range: " + rng);

            // Select AAKit, please call getAAKitList() to fetch all AAKit list in files/
            bool aakit_selected = false;
            string[] aakitList = (string[])service.getAAKitList(sn).RetData;
            foreach (string aakit in aakitList)
            {
                if (aakit.Contains("4x4"))
                {
                    Console.WriteLine("Select AAKit: {0}: {1}", aakit, service.selectAAKit(sn, aakit).name);
                    aakit_selected = true;
                    break;
                }
            }
            if (!aakit_selected)
                Console.WriteLine("PhiA mode");

            // ------- Get basic informations -------
            Double gain_max = rng[1];

            // Set IC channel gain, we use board 1 (its index in com_dr is 0) as example
            dynamic board_count = service.getBoardCount(sn).RetData;
            int board = 1;
            Console.WriteLine("Selected board: {0}/{1}", board, board_count);

            dynamic com_dr = service.getCOMDR(sn).RetData;
            dynamic common_gain_rng = com_dr[mode.value][board - 1];
            // Here we takes the maximum common gain as example
            dynamic common_gain_max = common_gain_rng[1];
            dynamic ele_dr_limit = service.getELEDR(sn).RetData[mode.value][board - 1];
            Console.WriteLine("Board:{0} common gain range: {1}, and element gain limit: {2}", board, common_gain_rng, ele_dr_limit);

            // ------- Beam control example -------
            if (aakit_selected)
            {
                //Passing: gain, theta, phi
                Console.WriteLine("SetBeamAngle: " + service.setBeamAngle(sn, gain_max, 0, 0));
            }
            else
            {
                Console.WriteLine("PhiA mode cannot process beam steering");
            }
        }
                
        public void TestUDBox(string sn, dynamic service)
        {
            dynamic tmy_public = Py.Import("TMYPublic");
            dynamic UDState = tmy_public.UDState;

            Console.WriteLine("PLO state: " + service.getUDState(sn, UDState.PLO_LOCK).RetData);
            Console.WriteLine("All state: " + service.getUDState(sn).RetData);
            
            Console.WriteLine(service.setUDState(sn, 0, UDState.CH1));
            Console.WriteLine("Wait for CH1 OFF");
            Console.ReadKey();
            Console.WriteLine(service.setUDState(sn, 1, UDState.CH1));
            Console.WriteLine("Check CH1 is ON");
            Console.ReadKey();
            // Other setate options
            Console.WriteLine(service.setUDState(sn, 1, UDState.CH2));
            Console.WriteLine(service.setUDState(sn, 1, UDState.OUT_10M));
            Console.WriteLine(service.setUDState(sn, 1, UDState.OUT_100M));
            Console.WriteLine(service.setUDState(sn, 1, UDState.PWR_5V));
            Console.WriteLine(service.setUDState(sn, 1, UDState.PWR_9V));

            // Passing: LO, RF, IF, Bandwidth with kHz
            Double LO = 24e6;
            Double RF = 28e6;
            Double IF = 4e6;
            Double BW = 1e5;
            // A check function, should be false -> not harmonic
            Console.WriteLine("Check harmonic: " + service.getHarmonic(sn, LO, RF, IF, BW).RetData);
            // SetUDFreq also includes check function
            dynamic ret = service.setUDFreq(sn, LO, RF, IF, BW);
            Console.WriteLine("Freq config: " + ret);
        }
        public void TestUDM(string sn, dynamic service)
        {
            dynamic tmy_public = Py.Import("TMYPublic");

            dynamic ret = service.getUDState(sn);
            if (ret.RetCode.value != tmy_public.RetCode.OK.value)
            {
                Console.WriteLine("Error to get UDM state:" + ret);
                return;
            }
            Console.WriteLine("UDM state: " + ret);

            // Passing: LO, RF, IF, Bandwidth with kHz
            Double LO = 7e6;
            Double RF = 10e6;
            Double IF = 3e6;
            Double BW = 1e5;
            ret = service.setUDFreq(sn, LO, RF, IF, BW);
            Console.WriteLine("Set UDM freq to {0}: {1}", LO, ret.RetCode);

            ret = service.getUDFreq(sn);
            Console.WriteLine("UDM current freq: " + ret);

            dynamic source = tmy_public.UDM_REF.INTERNAL;

            // A case to set internal source to output
            dynamic supported = service.getRefFrequencyList(sn, source).RetData;
            Console.WriteLine("Supported internal reference clock(KHz): {0}", supported);
            dynamic output_freq = supported[0];
            Console.WriteLine("Enable UDM ref output({0}KHz): {1}", output_freq, service.setOutputReference(sn, true, output_freq));
            Console.WriteLine("Get UDM ref ouput: {0}", service.getOutputReference(sn));

            Console.WriteLine("Press ENTER to disable output");
            Console.ReadKey();

            Console.WriteLine("Disable UDM ref output({0}KHz): {1}", output_freq, service.setOutputReference(sn, true, output_freq));
            Console.WriteLine("Get UDM ref ouput: {0}", service.getOutputReference(sn));

            // A case to change reference source to EXTERNAL
            source = tmy_public.UDM_REF.EXTERNAL;
            // Get external reference source supported list
            supported = service.getRefFrequencyList(sn, source).RetData;
            Console.WriteLine("Supported external reference clock(KHz): {0}", supported);
            // Try to change reference source to external: 10M
            ret = service.setRefSource(sn, source, supported[0]);
            Console.WriteLine("Change UDM ref source to {0} -> {1} with freq: {2}", source, ret, supported[0]);

            Console.WriteLine("\r\nWaiting for external reference clock input...\n");
            Console.ReadKey();

            // Check last state
            dynamic refer = tmy_public.UDMState.REF_LOCK;
            dynamic lock_state = service.getUDState(sn, refer.value);
            Console.WriteLine("UDM current reference status: {0}", lock_state);
        }
    }
}
