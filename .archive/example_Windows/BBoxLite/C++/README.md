# Getting Started with C++ Sample Code

## Prerequisites

    1. Install visual studio 2022 community
    2. Open project file and rebuild solution
    3. Put your calibration table into bbox-api\example\BBoxLite Series\C++\ConsoleApplication1\ConsoleApplication1\files
    4. Execute bbox-api\example\BBoxLite Series\C++\ConsoleApplication1\Release\ConsoleApp1.exe

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

    ret = instance->Init(sn, devtype, i);

    array<String ^> ^ freq_list = instance->getFrequencyList(sn);
    String ^ freq = freq_list[0];
    std::string FREQ = msclr::interop::marshal_as<std::string>(freq);
    double operating_freq = std::stod(FREQ);
    ret = instance->setOperatingFreq(operating_freq, sn);

    array<Double, 2> ^ DR = instance->getDR(sn);
    TX_MIN_GAIN = DR[0, 0];
    TX_MAX_GAIN = DR[0, 1];
    RX_MIN_GAIN = DR[1, 0];
    RX_MAX_GAIN = DR[1, 1];

    array<Double, 2> ^ COM_DR = instance->getCOMDR(sn);
    TX_COM_MIN_GAIN = COM_DR[0, 0];
    TX_COM_MAX_GAIN = COM_DR[0, 1];
    RX_COM_MIN_GAIN = COM_DR[1, 0];
    RX_COM_MAX_GAIN = COM_DR[1, 1];

    array<Double, 2> ^ ELE_DR = instance->getELEDR(sn);
    TX_ELE_DR = ELE_DR[0, 0];
    RX_ELE_DR = ELE_DR[0, 1];

    array<String ^> ^ AAkitList = instance->getAAKitList(sn);

    instance->selectAAKit(AAkitList[0], sn);

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

```

## DEMO3 : Control the specific Channel gain in db and phase in deg

---
Set the specific channel db and deg

```C++

double Target_db = TX_MAX_GAIN;
int Target_ch1_deg = 15;
int Target_ch2_deg = 30;
int Target_ch3_deg = 45;
int Target_ch4_deg = 60;

board = 1;

channel = 1;
instance->setChannelGainPhase(board, channel, Target_db, Target_ch1_deg, sn);

channel = 2;
instance->setChannelGainPhase(board, channel, Target_db, Target_ch2_deg, sn);

channel = 3;
instance->setChannelGainPhase(board, channel, Target_db, Target_ch3_deg, sn);

channel = 4;
instance->setChannelGainPhase(board, channel, Target_db, Target_ch4_deg, sn);

```

## DEMO4 : BeamSteering Control

---
Control beam direction with spherical coordinate system (theta, phi)

```C++

Target_db = TX_MAX_GAIN;
int Target_theta = 15;
int Target_phi = 0;

instance->setBeamAngle(Target_db, Target_theta, Target_phi, sn);

```

## DEMO5 : Get Device Temperature ADC Value

---
Get device current temperature adc value

```C++

Console::WriteLine("[{0}][DEMO5] Get temperature adc : {1}", sn, instance->getTemperatureADC(sn)[0]);

```
