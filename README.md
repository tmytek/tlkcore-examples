# BBox API Document
Version: v.0.6.0
Release date: December 3, 2018 

## Introduction

BBox API helps developers building their own applications. The release format is DLL and currently only support Windows operating system. The tested environment is Visual Studio.


# Getting Started — C#
## Installation
----------

Please import BBoxLiteAPI.dll from Visual Studio and use the following code segment to include the API.

    using BBoxLiteAPI;


## Initialization
----------
    BBoxAPI b = new BBoxAPI();
    b.Init(); // This will send the init command to BBox



## Control example
----------

**Control PA gain**
Power Amplifier (PA) can be setup at run-time. The recommended code snippet as below

    // Following code setup channel 1's PA gain with valude 15
    b.ControlCmd(b.GetTxRxMode(), 1, BBoxAPI.Control.PA_GAIN, (byte)15); 

**Control Beam direction**
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 10 degrees

    b.BeamSteer(b.GetTxRxMode(), 10.0);

 ****
**Read value** 

    // This will return the LNA bias value out of channel 1
    b.GetStepVal(b.GetTxRxMode(), 1, BBoxAPI.Control.LNA_BIAS);

**Obtain Tx or Rx state**
Use the following code to obtain the current Tx/Rx mode and store it in a variable m.

    BBoxAPI.TxRxMode m = b.GetTxRxMode();

**Switch Tx & Rx mode**
BBox is TDD based device. 

    b.SwitchTxRxMode(BBoxAPI.TxRxMode.Tx); // Switch BBox to Tx mode
    b.SwitchTxRxMode(BBoxAPI.TxRxMode.Rx); // Switch BBox to Rx mode



----------
# Getting Started — VC++
## Installation
----------

Please copy BBoxLiteAPI.dll to the project folder (e.g. root folder of the project or ./Debug). Add the following lines in the top of the .cpp file to include necessary DLL files. 


    #using "..\Debug\BBoxLiteAPI.dll"
    #using "..\Debug\MPSSELight.dll"


## Initialization
----------

To be able to use the external referred DLL object, please use the following instantiation method to obtain an object and send the initialization code to BBox.

    BBoxAPI ^b = gcnew BBoxAPI();
    b->Init(); // This will send the init command to BBox



## Control example
----------

**Obtain Tx or Rx state**
Use the following code to obtain the current Tx/Rx mode and store it in a variable m.

    BBoxAPI::TxRxMode m = b->GetTxRxMode();

**Switch Tx & Rx mode**
BBox is TDD based device. 

    b->SwitchTxRxMode(BBoxAPI::TxRxMode::Tx); // Switch BBox to Tx mode
    b->SwitchTxRxMode(BBoxAPI::TxRxMode::Rx); // Switch BBox to Rx mode

**Control PA gain**
Power Amplifier (PA) can be setup at run-time. The recommended code snippet as below

    // Following code setup channel 1's PA gain with valude 15
    b->ControlCmd(BBoxAPI::TxRxMode::Tx, 1, BBoxAPI::Control::PA_GAIN, (byte)15); 

**Control Beam direction**
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 10 degrees

    b->BeamSteer(b->GetTxRxMode(), 10.0);

 ****
**Read value** 

    // This will return the LNA bias value out of channel 1
    b->GetStepVal(BBoxAPI::TxRxMode::Rx, 1, BBoxAPI::Control::LNA_BIAS);



----------
# API parameters
## ControlCmd
    public int ControlCmd(int channel, Control ctrl, byte val);
| **T****ype** | **N****ame** | **Value**                                 |
| ------------ | ------------ | ----------------------------------------- |
| int          | channel      | { 1 | 2 | 3 | 4 } in BBox Lite            |
| Control      | ctrl         | Please refer to Enumeration table below   |
| byte         | val          | Please refer to Control range table below |

----------
## GetStepVal
    public int GetStepVal(TxRxMode trmode, int channel, Control ctrl);
| **T****ype** | **N****ame** | **Value**                                        |
| ------------ | ------------ | ------------------------------------------------ |
| TxRxMode     | trmode       | Please refer to Enumeration TxRxMode table below |
| int          | channel      | { 1 | 2 | 3 | 4 } in BBox Lite                   |
| Control      | ctrl         | Please refer to Enumeration Control table below  |

----------
## GetTxRxMode
    public TxRxMode GetTxRxMode(); // Get Tx/Rx Mode. Return TxRxMode table value.
----------
## Init
    public int Init();
----------
## SwitchTxRxMode
    public int SwitchTxRxMode(TxRxMode mode);
| **T****ype** | **N****ame** | **Value**                                        |
| ------------ | ------------ | ------------------------------------------------ |
| TxRxMode     | mode         | Please refer to Enumeration TxRxMode table below |

----------
## BeamSteer
    public int BeamSteer(TxRxMode mode, double angle);
| **T****ype** | **N****ame** | **Value**                                        |
| ------------ | ------------ | ------------------------------------------------ |
| TxRxMode     | mode         | Please refer to Enumeration TxRxMode table below |
| double       | angle        | Angle value range: -26.5°~26.5°                  |



# Enumeration values
    public enum Control
    {
        CHANNEL_POWER = 0,
        PA_BIAS = 1,
        PA_GAIN = 2,
        VGA_BIAS = 3,
        VGA_GAIN = 4,
        PS_BIAS = 5,
        PS_PHASE = 6,
        LNA_BIAS = 7,
        LNA_GAIN = 8
    }
    public enum TxRxMode
    {
        Tx = 0,
        Rx = 1
    }
    



# Control range
## Tx
| PA_BIAS  | 0-7  |
| -------- | ---- |
| PA_GAIN  | 0-15 |
| VGA_BIAS | 0-7  |
| VGA_GAIN | 0-15 |
| PS_BIAS  | 0-3  |
| PS_PHASE | 0-63 |

## Rx
| LNA_BIAS | 0-7  |
| -------- | ---- |
| LNA_GAIN | 0-7  |
| VGA_BIAS | 0-7  |
| VGA_GAIN | 0-31 |
| PS_BIAS  | 0-3  |
| PS_PHASE | 0-63 |


