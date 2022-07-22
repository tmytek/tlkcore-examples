# Getting Started — C++

## Installation
----------

    None


## Initialization
----------
    // Import BBoxAPI.dll

    #include <array>
    #include <msclr/marshal.h>
    #include <msclr/marshal_cppstd.h>

    using namespace System;
    using namespace BBoxAPI;
    using namespace msclr::interop;

    // Scanning device in the same subnet

    BBoxAPI::BBoxOneAPI ^instance = gcnew BBoxAPI::BBoxOneAPI();
	array<String ^>^ dev_info = instance->ScanningDevice((BBoxAPI::DEV_SCAN_MODE)0);
	dev_num = dev_info->Length;

    // Initial all devices

	for (int i = 0; i < dev_num; i++)
	{
		array<String ^> ^ response_message = dev_info[i]->Split(',');	

		String ^ sn = response_message[0];
		std::string SN = msclr::interop::marshal_as<std::string>(sn);
		String ^ ip = response_message[1];
		std::string IP = msclr::interop::marshal_as<std::string>(ip);
		String ^ dev_type = response_message[2];
		std::string DEV_TYPE = msclr::interop::marshal_as<std::string>(dev_type);
		int devtype = std::stoi(DEV_TYPE);

		ret = instance->Init(sn, devtype, i);
    }


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


