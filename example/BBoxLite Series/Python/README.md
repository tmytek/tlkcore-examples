# Getting Started — Python

## Installation
----------

    Please add your BBox calibration table and AAkit table to the following path.

    bbox-api\files\


## Initialization
----------

```python
# Import BBoxAPI.dll

dir_path = '..\\..\\..\\..\\'
os.chdir(os.path.abspath(dir_path))

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
    $ python .\BBoxOne_DEMO.py
****
## BBoxLite 5G
### Obtain Tx or Rx state
---
You need to control BBox device with its serial number.

```python
sn = "D2104L001-28"
TX = 1
RX = 2
mode = instance.getTxRxMode(sn)
```
### Switch Tx & Rx mode
---
You need to control BBox device with its serial number.

```python
sn = "D2104L001-28"
TX = 1
RX = 2
instance.SwitchTxRxMode(TX, sn)
instance.SwitchTxRxMode(RX, sn)
```

### Control Beam direction
---
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 14.5 dB, theta value 15 and phi value : 0 . You need to point out which BBox device used by serial number.

```python
db = 14.5
theta = 15
phi = 0
instance.setBeamAngle(db, theta, phi, sn)
```

****

# API Usage
## ScanningDevice
---
    public string[] ScanningDevice(DEV_SCAN_MODE scanMode)
| Type          | Name     | Value                |
| -             | -        | -                    |
| DEV_SCAN_MODE | scanMode | Normal : 0, Fast : 1 |

Return scan results from devices
## Init
---
    public int Init(sn, dev_type, idx)
| Type    | Name        | Value                           |
| -       | -           | -                               |
| String  | sn          | Serial Number from scan result |
| int     | dev_type    | Type from scan result           |
| int     | idx         | Index in scan result            |

Return integer type status code.

## getTxRxMode
---
Get Tx/Rx Mode of device with SN. Return TxRxMode table value.

    public int getTxRxMode(String sn); 

return 1 if Tx mode, and 2 if Rx mode.

## SwitchTxRxMode
---
    public int SwitchTxRxMode(int mode, String sn)
| Type   | Name  | Value                |
| -      | -     | -                    |
| int    | mode  | Tx : 1, Rx : 2       |
| String | sn    | device serial number |

## setBeamAngle
---
    public int setBeamAngle(double db, int theta, int phi, String sn)
| Type         | Name        | Value                 |
| -            | -           | -                     |
| double       | db          | Gain value            |
| int          | theta       | Theta value           |
| int          | phi         | Phi value             |
| String       | sn          | Device serial number  |


## setChannelGainPhase
---
    public string setChannelGainPhase(int board, int ch, double db, int phase, string sn)
| Type      | Name        | Value                 |
| -         | -           | -                     |
| int       | board       | Board number   : 1    |
| int       | ch          | Channel number : 1-4  |
| double    | db          | Target db             |
| int       | phase       | Target deg            |
| String    | sn          | Device serial number  |

## switchChannelPower
---
    public string switchChannelPower(int board, int ch, int sw, string sn)
| Type      | Name        | Value                          |
| -         | -           | -                              |
| int       | board       | Board number   : 1             |
| int       | ch          | Channel number : 1-4           |
| int       | sw          | ON/OFF value   : ON 0 , OFF 1  |
| String    | sn          | Device serial number           |


## getTemperatureADC
---
    int[] getTemperatureADC(string sn)

| Type      | Name        | Value                                  |
| ---       | ---         | ---                                    |
| string    | sn          | Device Serial Number : "D2104L011-28"  |

