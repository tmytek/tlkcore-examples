# Getting Started — C#

## Installation
----------

    Please add your BBox beamsterring table and AAkit table to the following path.

    bbox-api\example\BBoxLite Series\BBoxLite 5G\C#\ConsoleApp1\bin\Release\files


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

## BBoxLite 5G
### Get Tx or Rx state
---
Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number.

    TX = 1
    RX = 2
    mode = b.getTxRxMode(sn)

### Switch Tx & Rx mode
---
BBox is TDD based device. You need to point out which BBox device used by serial number.

    TX = 1
    RX = 2
    b.SwitchTxRxMode(TX, sn)
    b.SwitchTxRxMode(RX, sn)


### Control Beam direction
---
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 14.5 dB, theta value 15 and phi value : 0 . You need to point out which BBox device used by serial number.

    db = 14.5
    theta = 15
    phi = 0
    instance.setBeamAngle(db, theta, phi, sn)

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
| int       | board       | Board number   : 1   |
| int       | ch          | Channel number : 1-4 |
| double    | db          | Target db            |
| int       | phase       | Target deg           |
| String    | sn          | Device serial number |

----------
### switchChannelPower
    public string switchChannelPower(int board, int ch, int sw, string sn)
| Type      | Name        | Value                         |
| -         | -           | -                             |
| int       | board       | Board number   : 1            |
| int       | ch          | Channel number : 1-4          |
| int       | sw          | switch value   : ON 0 , OFF 1 |
| String    | sn          | Device serial number          |

---

