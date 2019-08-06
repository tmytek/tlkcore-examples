# BBox API Document
Version: v.1.0.0
Release date: Aug 2, 2019 

## Introduction

BBox API helps developers building their own applications. The release format is DLL and currently only support Windows operating system. The tested environment is Visual Studio.


# Getting Started — C#
## Installation
----------

Please import BBoxAPI.dll from Visual Studio and use the following code segment to include the API.

    using BBoxAPI;


## Initialization
----------
    BBoxAPI b = new BBoxAPI();
    b.Init(); // This will send the init command to BBox



## Control example
----------
**Control Beam direction**
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 15 dB of each channel and 10 degrees. You also need to point out which BBox device used by serial number.

    b.BeamSteer("B191321000-24",b.GetTxRxMode(), 15.0, 10.0);

 ****

**Obtain Tx or Rx state**
Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number.

    BBoxAPI.TxRxMode m = b.GetTxRxMode("B191321000-24");

**Switch Tx & Rx mode**
BBox is TDD based device. You need to point out which BBox device used by serial number.

    b.SwitchTxRxMode("B191321000-24", GetTxRxModeBBoxAPI.TxRxMode.Tx); // Switch BBox to Tx mode
    b.SwitchTxRxMode("B191321000-24", BBoxAPI.TxRxMode.Rx); // Switch BBox to Rx mode



----------
# Getting Started — VC++
## Installation
----------

Please copy **BBoxLiteAPI.dll** and **MPSSELight.dll** to the project folder (e.g. root folder of the project or ./Debug). Add the following lines in the top of the .cpp file to include necessary DLL files. 


    #using "..\Debug\BBoxAPI.dll"
    #using "..\Debug\MPSSELight.dll"


## Initialization
----------

To be able to use the external referred DLL object, please use the following instantiation method to obtain an object and send the initialization code to BBox.

    BBoxAPI ^b = gcnew BBoxAPI();
    b->Init(); // This will send the init command to BBox



## Control example
----------

**Obtain Tx or Rx state**
Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number.

    BBoxAPI::TxRxMode m = b->GetTxRxMode("B191321000-24");

**Switch Tx & Rx mode**
BBox is TDD based device. You need to point out which BBox device used by serial number.

    b->SwitchTxRxMode("B191321000-24", BBoxAPI::TxRxMode::Tx); // Switch BBox to Tx mode
    b->SwitchTxRxMode("B191321000-24", BBoxAPI::TxRxMode::Rx); // Switch BBox to Rx mode


**Control Beam direction**
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 15dB and 10 degrees. You need to point out which BBox device used by serial number.


    b->BeamSteer("B191321000-24", b->GetTxRxMode(), 15.0, 10.0);

 ****


----------
# API parameters
----------
## GetTxRxMode
    public TxRxMode GetTxRxMode(String sn); // Get Tx/Rx Mode of device with SN. Return TxRxMode table value.
----------
## Init
    public int Init();
----------
## SwitchTxRxMode
    public int SwitchTxRxMode(String sn, TxRxMode mode);
| Type | Name | Value                                        |
| ------------ | ------------ | ------------------------------------------------ |
| String       | sn           | device serial number |
| TxRxMode     | mode         | Please refer to Enumeration TxRxMode table below |

----------
## BeamSteer
    public int BeamSteer(String sn, TxRxMode mode, double db, double angle);
| Type | Name | Value                                        |
| ------------ | ------------ | ------------------------------------------------ |
| String       | sn           | device serial number |
| TxRxMode     | mode         | Please refer to Enumeration TxRxMode table below |
| double       | db           | gain value range: 25 - 15 dB in Tx mode and 10 - 0 dB in Rx mode for BBox Lite
| double       | angle        | Angle value range: -26.5°~26.5° for BBox Lite                  |



# Enumeration values
    public enum TxRxMode
    {
        Tx = 0,
        Rx = 1
    }
    


