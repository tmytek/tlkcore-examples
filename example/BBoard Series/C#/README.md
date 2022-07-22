# Getting Started — C#

## Installation
----------

    None

## Initialization
----------
    using System;
    using System.Linq;
    using System.Collections.Generic;

    // Import BBoxAPI.dll
    using BBoxAPI;

    // Scanning device in the same subnet
	BBoxOneAPI instance = new BBoxOneAPI();

    dev_info = instance.ScanningDevice(scanning_mode);
            
    DEV_NUM = dev_info.Count();

    // Initial all devices
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
### Running sample code
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


