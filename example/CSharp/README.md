# BBox API Document
Version: v3.0.4
Release date: July, 2020 

## Introduction

BBox API helps developers building their own applications. The release format is DLL and currently only support Windows operating system. The tested environment is Visual Studio.


# Getting Started — C#
## Installation
----------

Please copy **BBoxAPI.dll** to the project folder (e.g. root folder of the project or ./Release). Add the following DLL lib from Project References.
Import BBoxAPI.dll from Visual Studio and use the following code segment to include the API.

    using BBoxAPI;


## Initialization
----------
     BBoxOneAPI b = new BBoxOneAPI();

To obtain the device information, you need to call ScanningDevice. The return string contains device_sn and IP address, spliting by ','.  
Ex : B19133200-24,192.168.100.121 

    
    string[] dev_info = b.ScanningDevice();

	// suppose only one bboxone device
	string[] info = dev_info[0].Split(',');

	String sn = info[0]; // sn
	String ip = info[1]; // ip

Send the initialization code to BBoxOne. Parameter sn comes from the scanning results.

	String s_info = b.Init(sn, 0/*BBoxOne*/, 0);



## Control example
----------

**Obtain Tx or Rx state**

Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number. 

    int m = b.getTxRxMode(sn); // 0 : Tx, 1 : Rx  

**Switch Tx & Rx mode**

BBox is TDD based device. You need to point out which BBox device used by serial number.

    b.SwitchTxRxMode(sn, 0); // Switch BBox to Tx mode
    b.SwitchTxRxMode(sn, 1); // Switch BBox to Rx mode


**Control Beam direction**

The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 15 dB, 10 degrees in x direction and  20 degrees in y direction. You need to point out which BBox device used by serial number.

    b.setBeamXY(15, 10, 20, sn);

 ****


# API parameters

## getTxRxMode
    // Get Tx/Rx Mode of device with SN. Return TxRxMode table value.
    public int getTxRxMode(String sn); 
    
return 0 if Tx mode, and 1 if Rx mode.
    
----------
## Init
    public String Init(sn, 0/*BBoxOne*/, 0);

return initialized condition.

----------
## SwitchTxRxMode
    public int SwitchTxRxMode(int mode, String sn);
| Type | Name | Value                                        |
| ------------ | ------------ | ------------------------------------------------ |
| int     | mode         | Tx : 0, Rx : 1 |
| String       | sn           | device serial number |


----------
## setBeamXY
    public string setBeamXY(double db, double angleX, double angleY, String sn);
| Type | Name | Value                                        |
| ------------ | ------------ | ------------------------------------------------ |
| double       | db           | gain value
| double       | angleX        | angle value in x direction
| double       | angleY        | angle value in y direction
| String      | sn           | device serial number |