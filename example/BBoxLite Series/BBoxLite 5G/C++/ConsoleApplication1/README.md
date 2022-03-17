# Getting Started — VC++
## Installation
----------

Please copy the calibration files into "files" folder in the same direction as *.cpp source. (ex. ConsoleApplication1\ConsoleApplication1\files)


## Initialization
----------

To be able to use the external referred DLL object, please use the following instantiation method to obtain an control object.

    BBoxAPI::BBoxOneAPI ^b = gcnew BBoxAPI::BBoxOneAPI();

To obtain the device information, you need to call ScanningDevice. The return string contains device_sn and IP address, spliting by ' , '.
Ex : B19133200-24,192.168.100.121 

    
    array<String ^>^ dev_info = b->ScanningDevice();

	// Supposed only one bbox device
	array<String^>^ info_arr = dev_info[0]->Split(',');

	String^ sn = info_arr[0]; 
	String^ ip = info_arr[1]; 

Send the initialization code to BBoxOne. Parameter sn comes from the scanning results.

	String^ s_info = b->Init(sn, 0, 0);

## Control example
----------

**Get Tx or Rx state**

Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number.

    int m = b->getTxRxMode(sn);

**Switch Tx & Rx mode**

BBox is TDD based device. You need to point out which BBox device used by serial number.

    b->SwitchTxRxMode(sn, 0); // Switch BBox to Tx mode
    b->SwitchTxRxMode(sn, 1); // Switch BBox to Rx mode


**Control Beam direction**

The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 15 dB, theta value 15 and phi value : 0 . You need to point out which BBox device used by serial number.

    b.setBeamAngle(15, 15, 0, sn);

 ****


# API Usage
## Init
---
    public String^ Init(sn, 0/*BBoxOne*/, 0);

Return integer type status code.

## getTxRxMode
---
    // Get Tx/Rx Mode of device with SN. Return TxRxMode table value.
    public int getTxRxMode(String^ sn); 
    
Return 1 if Tx mode, and 2 if Rx mode.

## SwitchTxRxMode
---
    public int SwitchTxRxMode(int mode, String^ sn);
| Type          | Name    | Value                |
| -             | -       | -                    |
| int           | mode    | Tx : 1, Rx : 2       |
| String^       | sn      | Device serial number |

## setBeamAngle
---
    public string setBeamAngle(double db, int theta, int phi, String sn);
| Type         | Name        | Value                 |
| -            | -           | -                     |
| double       | db          | Gain value            |
| int          | theta       | Theta value           |
| int          | phi         | Phi value             |
| String^      | sn          | Device serial number  |



