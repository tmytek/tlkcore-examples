# Getting Started with C++ Sample Code

## Prerequisites

    1. Install visual studio 2022 community
    2. Open project file and rebuild solution
    3. Execute bbox-api\example\BBoard Series\C++\ConsoleApplication1\Release\ConsoleApp1.exe

## Commandline

---
    None

## Start : Query Device information and Init Device

---

- Scan the device information from ethernet.
- sn from the scan result is the parameter for api call.

```C++

#include "stdio.h"
#include "pch.h"

#include <iostream>
#include <string>
#include <array>
#include <msclr/marshal.h>
#include <msclr/marshal_cppstd.h>

using namespace System;
using namespace BBoxAPI;
using namespace msclr::interop;


```

- Init all devices

```C++

// GetDeviceStatus
BBoxAPI::BBoxOneAPI ^instance = gcnew BBoxAPI::BBoxOneAPI();

array<String ^>^ dev_info = instance->ScanningDevice((BBoxAPI::DEV_SCAN_MODE)0);
dev_num = dev_info->Length;

for (int i = 0; i < dev_num; i++)
{
    array<String ^> ^ response_message = dev_info[i]->Split(','); 

    String ^ sn = response_message[0];
    std::string SN = msclr::interop::marshal_as<std::string>(sn);
    String ^ ip = response_message[1];
    std::string IP = msclr::interop::marshal_as<std::string>(ip);
    String ^ dev_type = response_message[2];
    std::string DEV_TYPE = msclr::interop::marshal_as<std::string>(dev_type);
    int devtype = std::stoi(DEV_TYPE);

    BBoxAPI::retCode ^ ret; = instance->Init(sn, devtype, i);
}

```

## DEMO1 : Get/Set Device Operating Mode

---
Get/Set the device operating mode.

```C++

instance->SwitchTxRxMode(TX, sn);
int mode = instance->getTxRxMode(sn);
Console::WriteLine("[{0}][DEMO1] Mode : " + mode, sn);

```

## DEMO2 : Power Off Channel 1

---
Power Off the specific channel.

```C++

int board = 1;
int channel = 1;
int sw = 1;

instance->switchChannelPower(board, channel, sw, sn);
Console::WriteLine("[{0}][DEMO2] Channel 1 power off", sn);

```


## DEMO3 : Control Channel Element Gain Step

---
Set the specific channel gain step : 0.5 db per step

```C++

int gain_step = 1;

int board = 1;

int channel = 1;
instance->setChannelGainStep(board, channel, gain_step, sn);

channel = 2;
instance->setChannelGainStep(board, channel, gain_step, sn);

channel = 3;
instance->setChannelGainStep(board, channel, gain_step, sn);

channel = 4;
instance->setChannelGainStep(board, channel, gain_step, sn);

```

## DEMO4 : Control Common Gain Step

---
Set common-arm step : 1 db per step with all channels

```C++

int board = 1;
int gain_step = 1;

instance->setCommonGainStep(board, gain_step, sn);

```

## DEMO5 : Control Element Phase Step

---
Set the specific channel phase step : 5.625 deg per step

```C++

int phase_step = 1;

int board = 1;

int channel = 1;
instance->setChannelPhaseStep(board, channel, phase_step, sn);

channel = 2;
instance->setChannelPhaseStep(board, channel, phase_step, sn);

channel = 3;
instance->setChannelPhaseStep(board, channel, phase_step, sn);

channel = 4;
instance->setChannelPhaseStep(board, channel, phase_step, sn);

```

## DEMO6 : Get Device Temperature ADC Value

---
Get device current temperature adc value

```C++

Console::WriteLine("[{0}][DEMO5] Get temperature adc : {1}", sn, instance->getTemperatureADC(sn)[0]);

```
