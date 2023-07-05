# Getting Started with C# Sample Code

## Prerequisites

    1. Install visual studio 2022 community
    2. Open project file and rebuild solution
    3. Execute bbox-api\example\BBoard Series\C++\ConsoleApp1\bin\ReleaseConsoleApp1.exe

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

## DEMO3 : Control Channel Element Gain Step

---
Set the specific channel gain step : 0.5 db per step

```C#

int gain_step = 1;

int board = 1;

int channel = 1;
instance.setChannelGainStep(board, channel, gain_step, sn);

channel = 2;
instance.setChannelGainStep(board, channel, gain_step, sn);

channel = 3;
instance.setChannelGainStep(board, channel, gain_step, sn);

channel = 4;
instance.setChannelGainStep(board, channel, gain_step, sn);

```

## DEMO4 : Control Common Gain Step

---
Set common-arm step : 1 db per step with all channels

```C#

int gain_step = 1;

int board = 1;

instance.setCommonGainStep(board, gain_step, sn);

```

## DEMO5 : Control Element Phase Step

---
Set the specific channel phase step : 5.625 deg per step

```C#

int board = 1;

int channel = 1;
instance.setChannelPhaseStep(board, channel, phase_step, sn);

channel = 2;
instance.setChannelPhaseStep(board, channel, phase_step, sn);

channel = 3;
instance.setChannelPhaseStep(board, channel, phase_step, sn);

channel = 4;
instance.setChannelPhaseStep(board, channel, phase_step, sn);

```

## DEMO6 : Get Device Temperature ADC Value

---
Get device current temperature adc value

```C#

var ret = instance.getTemperatureADC(sn);

Console.WriteLine("[{0}][DEMO5] Get temperature adc : {1}", sn, ret[0]);

```
