# Getting Started with C# Sample Code

## Prerequisites

    1. Install visual studio 2022 community
    2. Open project file and rebuild solution
    3. Put your calibration table into bbox-api\example\BBoxLite Series\C#\ConsoleApp1\bin\Release\files
    4. Execute bbox-api\example\BBoxLite Series\C#\ConsoleApp1\bin\ReleaseConsoleApp1.exe

## Commandline

---
    None

## Start : Query Device information and Init Device

---

- Scan the device information from ethernet.
- sn from the scan result is the parameter for api call.

```C#

using System;
using System.Linq;
using BBoxAPI;

```

- Init all devices

```C#

BBoxOneAPI instance = new BBoxOneAPI();

dev_info = instance.ScanningDevice(scanning_mode);

DEV_NUM = dev_info.Count();

if(DEV_NUM > 0 && dev_info[0] != "Result,NoDeviceFound,-1")
{
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

        var AAkitList = instance.getAAKitList(sn);

        if (AAkitList.Length > 0)
        {
            instance.selectAAKit(AAkitList[0], sn);
        }
    }
}

```

## DEMO1 : Get/Set Device Operating Mode

---
Get/Set the device operating mode.

```C#

instance.SwitchTxRxMode(TX, sn);
int mode = instance.getTxRxMode(sn);
Console.WriteLine("[{0}][DEMO1] Mode : " + mode, sn);

```

## DEMO2 : Power Off Channel 1

---
Power Off the specific channel.

```C#

/*
sw = 0 is power-on
sw = 1 is power-off
*/

int board = 1;
int channel = 1;
int sw = 1;

instance.switchChannelPower(board, channel, sw, sn);

```

## DEMO3 : Control the specific Channel gain in db and phase in deg

---
Set the specific channel db and deg

```C#

double Target_db = TX_MAX_GAIN;
int Target_ch1_deg = 15;
int Target_ch2_deg = 30;
int Target_ch3_deg = 45;
int Target_ch4_deg = 60;

board = 1;

channel = 1;
instance.setChannelGainPhase(board, channel, Target_db, Target_ch1_deg, sn);

channel = 2;
instance.setChannelGainPhase(board, channel, Target_db, Target_ch2_deg, sn);

channel = 3;
instance.setChannelGainPhase(board, channel, Target_db, Target_ch3_deg, sn);

channel = 4;
instance.setChannelGainPhase(board, channel, Target_db, Target_ch4_deg, sn);


```

## DEMO4 : BeamSteering Control

---
Control beam direction with spherical coordinate system (theta, phi)

```C#

double Target_db = TX_MAX_GAIN;

int Target_theta = 15;
int Target_phi = 0;


instance.setBeamAngle(Target_db, Target_theta, Target_phi, sn);

```

## DEMO5 : Get Device Temperature ADC Value

---
Get device current temperature adc value

```C#

var ret = instance.getTemperatureADC(sn);
Console.WriteLine("[{0}][DEMO5] Get temperature adc : {1}", sn, ret[0]);

```
