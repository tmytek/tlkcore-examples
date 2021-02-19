# BBox API Document
Version: v3.0.8
Release date: Oct., 2020 

## Introduction

BBox API helps developers building their own applications. The release format is DLL and currently only support Windows operating system. The tested environment is Visual Studio and LabView 2019.


# Getting Started — Python
## Installation
----------

- Please install **pythonnet** at first. It's necessary for using windows dll in python script.

    You also could install pythonnet by launching <pre><code>pythonnet_installation\lib_install.bat</code></pre> 
    ![](./images/pythonnet.PNG)

- Please create a folder, named "files" under current path, and then put the BBox beamsterring table in the folder.


## Initialization
----------
    clr.AddReference('BBoxLiteAPI')
    from BBoxAPI import *
    instance = BBoxAPI()
    instance.Init(sn, dev_type, idx)  

To obtain the device information, you need to call ScanningDevice. The return string contains device SN, IP address and device type, spliting by ','.  
Ex1(BBox) : B19133200-24,192.168.100.111
Ex2(UDBox) : UD-BD20231000-24,192.168.100.112,4

    dev_info = b.ScanningDevice(0);
    devone = dev_info[0].split(",")   # Suppose there is only one device
    sn = devone[0]
    ip = devone[1]
    if len(devone) > 2:
        dev_type = int(devone[2])
    else:
        dev_type = 0

Send the initialization code to BBoxOne/UDBox. Parameter sn/dev_type comes from the scanning results.

    info = instance.Init(sn, dev_type, idx);


## Control example
****
### General Device
#### Running python
    $ python .\BBoxOne_BeamSteering.py
or

    $ python .\UD_SetFreq.py
****
### BBoxOne
##### Obtain Tx or Rx state

Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number.

    mode = b.getTxRxMode(sn); // 0 : Tx, 1 : Rx  

##### Switch Tx & Rx mode

BBox is TDD based device. You need to point out which BBox device used by serial number.

    b.SwitchTxRxMode(0, sn); // Switch BBox to Tx mode
    b.SwitchTxRxMode(1, sn); // Switch BBox to Rx mode


##### Control Beam direction

The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 15 dB, 10 degrees in x direction and  20 degrees in y direction. You need to point out which BBox device used by serial number.

    b.setBeamXY(15, 10, 20, sn);

****
### UDBox

##### Set UD Frequency
The core function of UDBox is to control LO frequency for your IF & RF frequency. The following code is setting LO freq: 26GHz, RF: 28GHz, IF: 2GHz. You need to point out which BBox device used by serial number.

    info = instance.SetUDFreq(26000000, 28000000, 2000000, sn)
****

# API parameters

----------
### ScanningDevice
    public string[] ScanningDevice(DEV_SCAN_MODE scanMode)
| Type | Name | Value |
| - | - | - |
| DEV_SCAN_MODE | scanMode | Normal : 0, Fast : 1 |

return scan results from devices

----------
### Init
    public String Init(sn, dev_type, idx);
| Type | Name | Value |
| - | - | - |
| String     | sn         | Serial Numnber from scan result |
| int     | dev_type         | Type from scan result |
| int     | idx         | Index in scan result |
return initialized condition.

----------
### getTxRxMode (BBoxOne only)
Get Tx/Rx Mode of device with SN. Return TxRxMode table value.

    public int getTxRxMode(String sn); 

return 0 if Tx mode, and 1 if Rx mode.

----------

### SwitchTxRxMode (BBoxOne only)
    public int SwitchTxRxMode(int mode, String sn);
| Type  | Name  | Value |
| -     | -     | -     |
| int   | mode  | Tx : 0, Rx : 1 |
| String | sn   | device serial number

----------
### setBeamXY (BBoxOne only)
    public string setBeamXY(double db, double angleX, double angleY, String sn);
| Type  | Name  | Value |
| -     | -     | -     |
| double       | db          | gain value
| double       | angleX      | angle value in x direction
| double       | angleY      | angle value in y direction
| String       | sn          | device serial number

----------
### setChannelGainPhase (BBoxOne only)
    public string setChannelGainPhase(int board, int ch, double db, int phase, string sn);
| Type  | Name  | Value |
| -     | -     | -     |
| int       | board       | Board number   : 1-4
| int       | ch          | Channel number : 1-4
| double    | db          | Target db
| int       | phase       | Target deg
| String    | sn          | device serial number

----------
### switchChannelPower (BBoxOne only)
    public string switchChannelPower(int board, int ch, int sw, string sn);
| Type  | Name  | Value |
| -     | -     | -     |
| int       | board       | Board number   : 1-4
| int       | ch          | Channel number : 1-4
| int       | sw          | switch value   : ON 0 , OFF 1
| String    | sn          | device serial number

----------
### GetState (UDBox only)
    public int GetState(int state_index, string sn)

| Type  | Name  | Value |
| -     | -     | -     |
| int    | state_index | 0: Lock<br>1: CH1<br>2: CH2<br>3: 10M output<br>4: 100M output<br>5: 100M source<br>6: LED 100M<br>7: 5V<br>8: 9V
| String | sn  | SN which you assign

return state from the state_index

### SetState (UDBox only)
    public int SetState(int state_index, int value, string sn)

| Type  | Name  | Value |
| -     | -     | -     |
| int       | state_index           | 0: Lock<br>1: CH1<br>2: CH2<br>3: 10M output<br>4: 100M output<br>5: 100M source<br>6: LED 100M<br>7: 5V<br>8: 9V
| int    | value    | value
| String | sn       | SN which you assign

return state from the state_index

### Set Freq(UDBox only)
    public string SetUDFreq(double freq_ud, double freq_rf, double freq_if, string sn)
| Type  | Name  | Value |
| -     | -     | -     |
| double    | freq_ud    | UD frequency(KHz)
| double    | freq_rf    | RF frequency(KHz)
| double    | freq_if    | IF frequency(KHz)
| String    | sn         | device serial number

return 0 if successful