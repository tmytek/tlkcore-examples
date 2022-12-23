# Getting Started with C# Sample Code

## Prerequisites

    1. Install python from bbox-api/pre-install/python-3.7.7-webinstall.exe
    2. Install pip packages from bbox-api/pre-install/Setup.bat
    3. Put your calibration table into bbox-api/example/BBoxOne Series/Python/files/

## Commandline

----------
    $ python BBoxOne_DEMO.py

## Start : Query Device information and Init Device

---

- Scan the device information from ethernet.
- sn from the scan result is the parameter for api call.

```python

# Import dll
path = '.\\BBoxAPI.dll'
clr.AddReference(os.path.abspath(path))


# Scanning all the devices in the same subnet
dev_info = instance.ScanningDevice(0)
device_num = len(dev_info)


for i in range(0, device_num, 1):

    response_message = dev_info[i].split(",")
    sn = response_message[0]
    ip = response_message[1]
    val = response_message[2].split("\x00")
    dev_type = int(val[0])

    print("[BBoxOne_DEMO][GetDeviceStatus] SN : %s" % (sn))
    print("[BBoxOne_DEMO][GetDeviceStatus] IP : %s" % (ip))
    print("[BBoxOne_DEMO][GetDeviceStatus] dev_type : %d" % (dev_type))


    # Init all the devices
    instance.Init(sn, dev_type, i)
    print("[BBoxOne_DEMO][InitialDevice][%s]" % (sn))


    # Choose the frequency point from calibration tables
    freq_list = instance.getFrequencyList(sn)
    if len(freq_list) == 0:
        print("[BBoxOne_DEMO][InitialDevice][%s] failed : return null" % (sn))
    else:
       for item in freq_list:
            print("[BBoxOne_DEMO][InitialDevice][%s] getFrequencyList: list %s" % (sn, item))

    ret = instance.setOperatingFreq(freq_list[0], sn)
    if ret != 0:
       print("[BBoxOne_DEMO][InitialDevice][%s] setOperatingFreq failed : error_code %d" % (sn, ret))

    # Gain dynamic range
    DR = instance.getDR(sn)
    print("[BBoxOne_DEMO][InitialDevice][%s] " % (sn))
    TX_MIN_GAIN = DR[0, 0]
    print("[BBoxOne_DEMO][InitialDevice][%s] TX_MIN_GAIN : %f" % (sn, TX_MIN_GAIN))
    TX_MAX_GAIN = DR[0, 1]
    print("[BBoxOne_DEMO][InitialDevice][%s] TX_MAX_GAIN : %f" % (sn, TX_MAX_GAIN))
    RX_MIN_GAIN = DR[1, 0]
    print("[BBoxOne_DEMO][InitialDevice][%s] RX_MIN_GAIN : %f" % (sn, RX_MIN_GAIN))
    RX_MAX_GAIN = DR[1, 1]
    print("[BBoxOne_DEMO][InitialDevice][%s] RX_MAX_GAIN : %f" % (sn, RX_MAX_GAIN))


    # Get/Set AAKIT
    AAkitList = instance.getAAKitList(sn)
    if len(AAkitList) > 0:
        instance.selectAAKit(AAkitList[0], sn)

```

## DEMO1 : Get/Set Device Operating Mode

---
Get/Set the device operating mode.

```python

# Set device operating mode as TX
instance.SwitchTxRxMode(TX, sn)

# Get device operating mode
mode = instance.getTxRxMode(sn)

```

## DEMO2 : Power Off Channel 1 and channel 5

---
Power Off the specific channel.

```python

"""
sw = 0 is power-on
sw = 1 is power-off
"""
sw = 1


# Ch 1 = board 1 and channel 1 ( 4 channel per board )

board = 1
channel = 1

instance.switchChannelPower(board, channel, sw, sn)

# Ch 5 = board 2 and channel 1 ( 4 channel per board )

board = 2
channel = 1

instance.switchChannelPower(board, channel, sw, sn)

```

## DEMO3 : Control the specific Channel gain in db and phase in deg

---
Set the specific channel db and deg

```python

Target_db = TX_MAX_GAIN   # read from instance.getDR(sn)

board = 1


# Control channel_1 

channel = 1

Target_ch1_deg = 15
instance.setChannelGainPhase(board, channel, Target_db, Target_ch1_deg, sn)


# Control channel_2

channel = 2

Target_ch2_deg = 30
instance.setChannelGainPhase(board, channel, Target_db, Target_ch2_deg, sn)


# Control channel_3

channel = 3
Target_ch3_deg = 45
instance.setChannelGainPhase(board, channel, Target_db, Target_ch3_deg, sn)


# Control channel_4

channel = 4
Target_ch4_deg = 60
instance.setChannelGainPhase(board, channel, Target_db, Target_ch4_deg, sn)

```

## DEMO4 : BeamSteering Control

---
Control beam direction with spherical coordinate system (theta, phi)

```python

    Target_db = TX_MAX_GAIN
    
    Target_theta = 15
    Target_phi = 0

    instance.setBeamAngle(Target_db, Target_theta, Target_phi, sn)

```

## DEMO5 : Get Device Temperature ADC Value

---
Get device current temperature adc value

```python

    adc_ret = instance.getTemperatureADC(sn)
    
    print("[BBoxOne_DEMO][DEMO5] Get board_1 temperature adc : %d" %adc_ret[0])
    print("[BBoxOne_DEMO][DEMO5] Get board_2 temperature adc : %d" %adc_ret[1])
    print("[BBoxOne_DEMO][DEMO5] Get board_3 temperature adc : %d" %adc_ret[2])
    print("[BBoxOne_DEMO][DEMO5] Get board_4 temperature adc : %d" %adc_ret[3])

```
