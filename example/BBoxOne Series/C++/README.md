# Getting Started — C++

## Installation
----------

    Please add your own BBox Calibration table and AAkit table to the following path.

    bbox-api\example\BBoxOne Series\BBoxOne  5G\C++\ConsoleApplication1\ConsoleApplication1\files


## Initialization
----------

```C++
// Import BBoxAPI.dll

#include <array>
#include <msclr/marshal.h>
#include <msclr/marshal_cppstd.h>

using namespace System;
using namespace BBoxAPI;
using namespace msclr::interop;

// Scanning device in the same subnet

BBoxAPI::BBoxOneAPI ^instance = gcnew BBoxAPI::BBoxOneAPI();
array<String ^>^ dev_info = instance->ScanningDevice((BBoxAPI::DEV_SCAN_MODE)0);
dev_num = dev_info->Length;

// Initializing all devices
for (int i = 0; i < dev_num; i++)
{
	array<String ^> ^ response_message = dev_info[i]->Split(',');	

	String ^ sn = response_message[0];
	std::string SN = msclr::interop::marshal_as<std::string>(sn);
	String ^ ip = response_message[1];
	std::string IP = msclr::interop::marshal_as<std::string>(ip);

	ret = instance->Init(sn, 0, i);
}

## Control example
****
#### Running sample code
    Open ConsoleApplication1.sln
    Compile and run
****

## BBoxOne5G
### Get Device mode
---
You need to control BBox device with its serial number.

```C++
int TX = 1;
int RX = 2;
int mode = instance->getTxRxMode(sn);
```

### Switch Tx or Rx mode
---
You need to control BBox device with its serial number.

```C++
int TX = 1;
int RX = 2;
instance->SwitchTxRxMode(TX, sn);
instance->SwitchTxRxMode(RX, sn);
```

### Control Beam direction
---
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 14.5 dB, theta value 15 and phi value : 30 . You need to point out which BBox device used by serial number.

```C++
double db = 14.5;
int theta = 15;
int phi = 30;
instance->setBeamAngle(db, theta, phi, sn);
```

### Get Temperature Sensor ADC Value
---
Board-based Temperature Sensor. Lite has only one board.

```C++
int board1_adc = instance->getTemperatureADC(sn)[0];
int board2_adc = instance->getTemperatureADC(sn)[1];
int board3_adc = instance->getTemperatureADC(sn)[2];
int board4_adc = instance->getTemperatureADC(sn)[3];
```

