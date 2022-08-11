# Getting Started — Python

## Installation
----------
    None

## Initialization
----------

```python
# pip install pythonnet
# clr Import BBoxAPI.dll

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
```

## Control example
****
#### Running sample code
    $ python BBoard_DEMO.py
****

## BBoard 5G
### Get Tx or Rx state
---
Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number.

```python
mode = instance.getTxRxMode(sn)
```

### Switch Tx & Rx mode
---
You need to control BBox device with its serial number.

```python
sn = 'D2104L001-28'
TX = 1
RX = 2
instance.SwitchTxRxMode(TX, sn)
instance.SwitchTxRxMode(RX, sn)
```

### Control Element Phase Step
---
Set the specific channel element-arm phase step : 5.625 deg per step

```python
sn = 'D2104L001-28'
board = 1
channel = 1
phase_step = 1
instance.setChannelPhaseStep(board, channel, phase_step, sn)
```

### Control Element Gain Step
---
Set the specific channel element-arm gain step : 0.5 db per step

```python
sn = 'D2104L001-28'
board = 1
channel = 1
gain_step = 1
instance.setChannelGainStep(board, channel, gain_step, sn)
```

### Control Common Gain Step
---
Set common-arm step : 1 db per step with all channels

```python
sn = 'D2104L001-28'
board = 1
gain_step = 1
instance.setCommonGainStep(board, gain_step, sn)
```

### Get Temperature ADC
---
Get device current temperature adc value

```python
sn = 'D2104L001-28'

# int[] ret
ret = b.getTemperatureADC(sn)
```
****


