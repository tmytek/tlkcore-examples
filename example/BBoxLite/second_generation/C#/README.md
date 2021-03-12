# Getting Started — C#

## Installation
----------

- Please create a folder, named "files" under current path, and then put the BBox beamsterring table in the folder.


## Initialization
----------
    // Import BBoxAPI.dll

    using System;
    using System.Linq;
    using System.Collections.Generic;
    using BBoxAPI;

    // Scanning device in the same subnet

    BBoxAPI::BBoxOneAPI ^instance = gcnew BBoxAPI::BBoxOneAPI();
	array<String ^>^ dev_info = instance->ScanningDevice((BBoxAPI::DEV_SCAN_MODE)0);
	dev_num = dev_info->Length;

    // Initial all devices

	BBoxOneAPI instance = new BBoxOneAPI();

    dev_info = instance.ScanningDevice(scanning_mode);
            
    DEV_NUM = dev_info.Count();

    for (int i = 0; i < DEV_NUM; i++)
    {
        string[] response_message = dev_info[i].Split(',');
        sn = response_message[0];
		ip = response_message[1];
		DEV_TYPE = Convert.ToInt32(response_message[2]);
        instance.Init(sn, DEV_TYPE, i);
    }

## Control example
****
#### Running sample code
    Open ConsoleApplication1.sln
    Compile and run
****

### BBox
##### Obtain Tx or Rx state

Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number.

    mode = b.getTxRxMode(sn); // 1 : Tx, 2 : Rx  

##### Switch Tx & Rx mode

BBox is TDD based device. You need to point out which BBox device used by serial number.

    b.SwitchTxRxMode(1, sn); // Switch BBox to Tx mode
    b.SwitchTxRxMode(2, sn); // Switch BBox to Rx mode


##### Control Beam direction

The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 15 dB, 10 degrees in x direction and  20 degrees in y direction. You need to point out which BBox device used by serial number.

    b.setBeamXY(15, 10, 20, sn);

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
### getTxRxMode
Get Tx/Rx Mode of device with SN. Return TxRxMode table value.

    public int getTxRxMode(String sn); 

return 0 if Tx mode, and 1 if Rx mode.

----------

### SwitchTxRxMode
    public int SwitchTxRxMode(int mode, String sn);
| Type  | Name  | Value |
| -     | -     | -     |
| int   | mode  | Tx : 0, Rx : 1 |
| String | sn   | device serial number

----------
### setBeamXY
    public string setBeamXY(double db, double angleX, double angleY, String sn);
| Type  | Name  | Value |
| -     | -     | -     |
| double       | db          | gain value
| double       | angleX      | angle value in x direction
| double       | angleY      | angle value in y direction
| String       | sn          | device serial number

----------
### setChannelGainPhase
    public string setChannelGainPhase(int board, int ch, double db, int phase, string sn);
| Type  | Name  | Value |
| -     | -     | -     |
| int       | board       | Board number   : 1-4
| int       | ch          | Channel number : 1-4
| double    | db          | Target db
| int       | phase       | Target deg
| String    | sn          | device serial number

----------
### switchChannelPower
    public string switchChannelPower(int board, int ch, int sw, string sn);
| Type  | Name  | Value |
| -     | -     | -     |
| int       | board       | Board number   : 1-4
| int       | ch          | Channel number : 1-4
| int       | sw          | switch value   : ON 0 , OFF 1
| String    | sn          | device serial number

----------

