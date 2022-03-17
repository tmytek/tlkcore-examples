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

# API Usage
### ScanningDevice
---
    public string[] ScanningDevice(DEV_SCAN_MODE scanMode)
| Type          | Name     | Value                |
| -             | -        | -                    |
| DEV_SCAN_MODE | scanMode | Normal : 0, Fast : 1 |

Return scan results from devices

### Init
---
    public int Init(sn, dev_type, idx)
| Type    | Name        | Value                           |
| -       | -           | -                               |
| String  | sn          | Serial Numnber from scan result |
| int     | dev_type    | Type from scan result           |
| int     | idx         | Index in scan result            |

Return integer type status code.

### getTxRxMode
---
    // Get Device Mode  with SN. Return integer type value.

    public int getTxRxMode(String sn); 

Return 1 if Tx mode, and 2 if Rx mode.

### SwitchTxRxMode
---
    public int SwitchTxRxMode(int mode, String sn)
| Type   | Name  | Value                |
| -      | -     | -                    |
| int    | mode  | Tx : 1, Rx : 2       |
| String | sn    | Device serial number |

## setBeamAngle
---
    public string setBeamAngle(double db, int theta, int phi, String sn)
| Type         | Name        | Value                 |
| -            | -           | -                     |
| double       | db          | Gain value            |
| int          | theta       | Theta value           |
| int          | phi         | Phi value             |
| String       | sn          | Device serial number  |

### setChannelGainPhase
---
    public string setChannelGainPhase(int board, int ch, double db, int phase, string sn)
| Type      | Name        | Value                |
| -         | -           | -                    |
| int       | board       | Board number   : 1-4 |
| int       | ch          | Channel number : 1-4 |
| double    | db          | Target db            |
| int       | phase       | Target deg           |
| String    | sn          | Device serial number |

----------
### switchChannelPower
    public string switchChannelPower(int board, int ch, int sw, string sn)
| Type      | Name        | Value                         |
| -         | -           | -                             |
| int       | board       | Board number   : 1-4          |
| int       | ch          | Channel number : 1-4          |
| int       | sw          | switch value   : ON 0 , OFF 1 |
| String    | sn          | Device serial number          |

---