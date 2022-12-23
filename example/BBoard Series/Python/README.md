# Getting Started with Python Sample Code

## Prerequisites

    1. Install python from bbox-api/pre-install/python-3.7.7-webinstall.exe
    2. Install pip packages from bbox-api/pre-install/Setup.bat

## Commandline
----------
    $ python BBoard_DEMO.py

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

# Init all the devices
for i in range(0, device_num, 1):

    response_message = dev_info[i].split(",")
    sn = response_message[0]
    ip = response_message[1]
    val = response_message[2].split("\x00")
    dev_type = int(val[0])

    print("[BBoard_DEMO][GetDeviceStatus] SN : %s" % (sn))
    print("[BBoard_DEMO][GetDeviceStatus] IP : %s" % (ip))
    print("[BBoard_DEMO][GetDeviceStatus] dev_type : %d" % (dev_type))

    instance.Init(sn, dev_type, i)
    print("[BBoard_DEMO][InitialDevice][%s]" % (sn))

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

## DEMO2 : Power Off Channel 1
---
Power Off the specific channel.
```python

"""
sw = 0 is power-on
sw = 1 is power-off
"""
sw = 1

board = 1
channel = 1

instance.switchChannelPower(board, channel, sw, sn)

```

## DEMO3 : Control Channel Element Gain Step
---
Set the specific channel gain step : 0.5 db per step

```python

gain_step = 1

board = 1

# Control channel_1 
channel = 1
instance.setChannelGainStep(board, channel, gain_step, sn)


# Control channel_2
channel = 2
instance.setChannelGainStep(board, channel, gain_step, sn)


# Control channel_3
channel = 3
instance.setChannelGainStep(board, channel, gain_step, sn)


# Control channel_4
channel = 4
instance.setChannelGainStep(board, channel, gain_step, sn)

```

## DEMO4 : Control Common Gain Step
---
Set common-arm step : 1 db per step with all channels

```python

gain_step = 1

board = 1

instance.setCommonGainStep(board, gain_step, sn)

```

## DEMO5 : Control Element Phase Step

---
Set the specific channel phase step : 5.625 deg per step

```python

phase_step = 1

board = 1

# Control channel_1
 
channel = 1
instance.setChannelPhaseStep(board, channel, phase_step, sn)


# Control channel_2
 
channel = 2
instance.setChannelPhaseStep(board, channel, phase_step, sn)


# Control channel_3
 
channel = 3
instance.setChannelPhaseStep(board, channel, phase_step, sn)

# Control channel_4
 
channel = 4
instance.setChannelPhaseStep(board, channel, phase_step, sn)

```


## DEMO6 : Get Device Temperature ADC Value
---
Get device current temperature adc value

```python

adc = instance.getTemperatureADC(sn)

print(adc[0])

```
