# Getting Started — C#

## Installation
----------

    Please add your BBox Calibration table and AAkit table to the following path.

    bbox-api\example\BBoxLite Series\BBoxLite 5G\C#\ConsoleApp1\bin\Release\files

    The compiled binary at

    D:\tmytek\Source\bbox-api\example\BBoxLite Series\BBoxLite 5G\C#\ConsoleApp1\bin\Release\ConsoleApp1.exe


## Initialization
----------

```C#
using System;
using System.Linq;
using System.Collections.Generic;

// Import BBoxAPI.dll
using BBoxAPI;

// Scanning device in the same subnet
BBoxOneAPI instance = new BBoxOneAPI();

var dev_info = instance.ScanningDevice(scanning_mode);
            
DEV_NUM = dev_info.Count();

// Initial all devices
for (int i = 0; i < DEV_NUM; i++)
{
    string[] response_message = dev_info[i].Split(',');
    sn = response_message[0];
	ip = response_message[1];
	DEV_TYPE = Convert.ToInt32(response_message[2]);
    instance.Init(sn, DEV_TYPE, i);
}
```

## Control example
---
### Running sample code
    Open ConsoleApplication1.sln
    Compile and run
---

## BBoxLite 5G
### Get Tx or Rx state
---
You need to control BBox device with its serial number.

```C#
int TX = 1;
int RX = 2;
int mode = instance.getTxRxMode(sn);
```

### Switch Tx & Rx mode
---
You need to control BBox device with its serial number.

```C#
int TX = 1;
int RX = 2;
instance.SwitchTxRxMode(TX, sn);
instance.SwitchTxRxMode(RX, sn);
```

### Control Beam direction
---
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 14.5 dB, theta value 15 and phi value : 0 . You need to point out which BBox device used by serial number.

```C#
double db = 14.5;
int theta = 15;
int phi = 0;
instance.setBeamAngle(db, theta, phi, sn);
```

### Get Temperature Sensor ADC Value
---
Board-based Temperature Sensor. Lite has only one board.

```C#
int[] ret = instance.getTemperatureADC(sn);
int adc = ret[0];
```


