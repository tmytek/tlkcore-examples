# BBox API Document
Version: v3.0.8
Release date: Oct., 2020 

## Introduction

BBox API helps developers building their own applications. The release format is DLL and currently only support Windows operating system. The functions in DLL could be import in LabView. The tested environment and example is baseed on LabView2019.


<!-- # Getting Started — LabView
## Installation
----------

Please import BBoxLiteAPI.dll from Visual Studio and use the following code segment to include the API.

    using BBoxLiteAPI;


## Initialization
----------
    BBoxAPI b = new BBoxAPI();
    b.Init(); // This will send the init command to BBox
 -->


## Control example
<img src="BBoxLite_labView_Example.png"
     alt="labView_Example"
     style="float: left; margin-right: 10px;" />

----------

The LabView demo flow for 2 BBoxLite devices
****
Notice : The API is import to LabView environment by "Call Library Function Node" then you can find them on the LabView visual graphic. You can also modify the LabViewTest example for customized purpose. Please create a folder named "files" under the same folder with LabView Project files, and then put related table inside.
****
**Initialize the BBoxOne devices**
Initalize all the BBoxLite in the same time.

    public String Init();

**Control Beam direction**
The core function of BBox is to control beam steering. The following code snippet steers beam in diffirent direction. Please refer to next section for API parameters.  

    public string BeamSteer(string sn, TxRxMode mode, double db, double angle)


**Switch Tx & Rx mode**
BBox is TDD based device. 

    int SwitchTxRxMode(sn/*device sn*/, 0); // Switch BBox to Tx mode
    int SwitchTxRxMode(sn/*device sn*/, 1); // Switch BBox to Rx mode



----------
# API parameters

## BeamSteer
    public string BeamSteer(string sn, int mode, double db, double angle)
| Type | Name | Value                                        |
| ------------ | ------------ | ------------------------------------------------ |
| string       | sn           | bbox sn   |
| int          | trmode         | Tx : 0, Rx : 1 |
| double       | db           | gain value for each channel |
| double          | ang          | -45 to 45 degree |



----------
## Init
    public string Init();


----------
## SwitchTxRxMode
    public int SwitchTxRxMode(string sn, int trmode);
| Type | Name | Value                                        |
| ------------ | ------------ | ------------------------------------------------ |
| string       | sn           | bbox sn   |
| int          | trmode         | Tx : 0, Rx : 1 |



# Control range
## Tx dynamic range for BBoxLite
| Gain  | 10.0 to 25.0 dB |
| -------- | ---- |
Resolution is 0.5 dB

## Rx dynamic range for BBoxLite
| Gain  | 0.0 to 10.0 dB |
| -------- | ---- |
Resolution is 0.5 dB


## Tx/Rx phase range
| phase | 0-355  |
| -------- | ---- |
Resolution is 5 degrees


