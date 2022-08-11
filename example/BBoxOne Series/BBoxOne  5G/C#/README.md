# Getting Started — C#
## Installation
----------

    Please add your BBox Calibration table and AAkit table to the following path.

    bbox-api\example\BBoxOne Series\BBoxOne  5G\C#\ConsoleApp1\bin\Release\files

## Initialization
----------

```C#
/*
To obtain the device information, you need to call ScanningDevice. The return string contains device_sn and IP address, spliting by ','.  
Ex : B19133200-28,192.168.100.111,9
*/

BBoxOneAPI instance = new BBoxOneAPI();

string[] dev_info = instance.ScanningDevice(0);

// Get first device in scan result
string[] info = dev_info[0].Split(',');

String sn = info[0]; 
String ip = info[1]; 


instance.Init(sn, 0, 0);
```

## Control example
----------

## BBoxOne5G
### Get Device mode
---
You need to control BBox device with its serial number.

```C#
int TX = 1;
int RX = 2;
int mode = instance.getTxRxMode(sn);
```

### Switch Tx or Rx mode
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
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 14.5 dB, theta value 15 and phi value : 30 . You need to point out which BBox device used by serial number.

```C#
double db = 14.5;
int theta = 15;
int phi = 30;
instance.setBeamAngle(db, theta, phi, sn);
```

 ****

