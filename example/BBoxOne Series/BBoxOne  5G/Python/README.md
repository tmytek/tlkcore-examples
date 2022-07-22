# Getting Started — Python

## Installation
----------

    Please add your BBox Calibration table and AAkit table to the following path.

    bbox-api\example\BBoxOne Series\BBoxOne  5G\Python\files\


## Initialization
----------
    # Import BBoxAPI.dll

    path = '.\\BBoxAPI.dll'
    clr.AddReference(os.path.abspath(path))

    # Scanning device in the same subnet

    dev_info = instance.ScanningDevice(0)
	device_num = len(dev_info)

    # Initial all devices

	for i in range(0, device_num, 1):

		response_message = dev_info[i].split(",")
		sn = response_message[0]
		ip = response_message[1]
		val = response_message[2].split("\x00")
		dev_type = int(val[0])

		instance.Init(sn, dev_type, i)

## Control example
****
### Running sample code
    $ python .\BBoxOne_DEMO.py
****

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
