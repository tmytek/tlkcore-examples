# Getting Started — C#
## Installation
----------

    Please add your BBox Calibration table and AAkit table to the following path.

    bbox-api\example\BBoxOne Series\BBoxOne  5G\C#\ConsoleApp1\bin\Release\files

## Initialization
----------
     BBoxOneAPI b = new BBoxOneAPI();

To obtain the device information, you need to call ScanningDevice. The return string contains device_sn and IP address, spliting by ','.  
Ex : B19133200-28,192.168.100.111,9

    BBoxOneAPI instance = new BBoxOneAPI();

    string[] dev_info = instance.ScanningDevice(0);

	// suppose only one bboxone device
	string[] info = dev_info[0].Split(',');

	String sn = info[0]; // sn
	String ip = info[1]; // ip

Send the initialization code to BBoxOne. Parameter sn comes from the scanning results.

	instance.Init(sn, 0, 0);

## Control example
----------

## BBoxOne5G
### Get Device mode
---
Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number.

    TX = 1
    RX = 2
    mode = instance.getTxRxMode(sn)

### Switch Tx or Rx mode
---
BBox is TDD based device. You need to point out which BBox device used by serial number.

    TX = 1
    RX = 2
    instance.SwitchTxRxMode(TX, sn)
    instance.SwitchTxRxMode(RX, sn)


### Control Beam direction
---
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 14.5 dB, theta value 15 and phi value : 30 . You need to point out which BBox device used by serial number.

    db = 14.5
    theta = 15
    phi = 30
    instance.setBeamAngle(db, theta, phi, sn);

 ****

---