# Getting Started — Python

## Installation
----------

    None

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
#### Running sample code
    Open ConsoleApplication1.sln
    Compile and run
****

## BBoard 5G
### Get Tx or Rx state
---
Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number.

    mode = b.getTxRxMode(sn)


### Switch Tx & Rx mode
---
BBox is TDD based device. You need to point out which BBox device used by serial number.

    TX = 1
    RX = 2
    b.SwitchTxRxMode(TX, sn)
    b.SwitchTxRxMode(RX, sn)


### Control Element Phase Step
---
Set the specific channel element-arm phase step : 5.625 deg per step

    phase_step = 1
	channel = 1;
	b.setChannelPhaseStep(board, channel, phase_step, sn)


### Control Element Gain Step
---
Set the specific channel element-arm gain step : 0.5 db per step

    gain_step = 1
	channel = 1;
	b.setChannelGainStep(board, channel, gain_step, sn)


### Control Common Gain Step
---
Set common-arm step : 1 db per step with all channels

    gain_step = 1
	channel = 1;
	b.setCommonGainStep(board, gain_step, sn)


### Get Temperature ADC
---
    Get device current temperature adc value

    int[] ret;
	ret = b.getTemperatureADC(sn)

****


