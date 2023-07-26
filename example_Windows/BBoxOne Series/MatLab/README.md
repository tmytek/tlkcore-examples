# API Sample Code Description

## Introduction

- Enviroment : Windows 10
- API Format : .dll
- Matlab Version : Matlab2021

## Control example

****
Notice : The API is import to MatLab environment by "NET.addAssembly(dll_path);". You can also modify the main.m example for customized purpose. Please create a folder named "files" under the same folder with MatLab Project files, and then put related table inside. TMYTEK provide a control class wrapper named BBoxCtrler.m
****

**Consructor of BBoxCtrler**
Put the dll filepath as parameter when initializing


    dll_path = '...'
    obj = BBoxCtrler(dll_path);

**Initialize the BBoxOne devices**
Initialize all BBoxOne devices and then obtain the related Serial number list

    dev_sn_list = deviceInit(obj, bbox_type_str)

| Type | Name | Value                                                             |
| ------------ | ------------  | ------------------------------------------------ |
| BBoxCtrler   | obj           | BBoxCtrler class instance                        |
| string       | bbox_type_str | bbox type : 'BBoxOne' or 'BBoxLite'              |

  &emsp;

**Get support operating frequencies based on frequency tables under files folder**

    freq_list = getFrequencyList(obj, dev_sn)

| Type | Name | Value                                                             |
| ------------ | ------------  | ------------------------------------------------ |
| BBoxCtrler   | obj           | BBoxCtrler class instance                        |
| string       | dev_sn        | BBox serial number                               |

  &emsp;

**Set operating frequency for BBoxOne device**

    setOperatingFreq(obj, dev_sn, freq)
| Type         | Name         | Value                                            |
| ------------ | ------------ | ------------------------------------------------ |
| BBoxCtrler   | obj          | BBoxCtrler class instance                        |
| string       | dev_sn       | BBox serial number                               |
| int          | freq         | operating frequency                              |

  &emsp;


**Get supported AAkit list based on aakit tables under files folder**

    aakit_list = getAAKitList(obj, dev_sn)
| Type         | Name         | Value                                            |
| ------------ | ------------ | ------------------------------------------------ |
| BBoxCtrler   | obj          | BBoxCtrler class instance                        |
| string       | dev_sn       | BBox serial number                               |

  &emsp;

**Select AAkit by aakit_name from list of getAAKitList return value**

    selectAAKit(obj, dev_sn, aakit_name)
| Type         | Name         | Value                                            |
| ------------ | ------------ | ------------------------------------------------ |
| BBoxCtrler   | obj          | BBoxCtrler class instance                        |
| string       | dev_sn       | BBox serial number                               |
| string       | aakit_name   | aakit name                                       |

  &emsp;


**Switch Tx & Rx mode**
BBox is TDD based device.
    setOperationMode(obj, dev_sn, mode)
| Type         | Name         | Value                                            |
| ------------ | ------------ | ------------------------------------------------ |
| BBoxCtrler   | obj          | BBoxCtrler class instance                        |
| string       | dev_sn       | BBox serial number                               |
| int          | mode         |  Tx : 1, Rx : 2                                  |

  &emsp;


**Set BBoxOne specific channel gain/phase**

    setChannelGainPhase(obj, dev_sn, board, ch, db, deg)
| Type         | Name         | Value                                            |
| ------------ | ------------ | ------------------------------------------------ |
| BBoxCtrler   | obj          | BBoxCtrler class instance                        |
| string       | dev_sn       | BBox serial number                               |
| int          | board        |  target board number : 1 - 4                     |
| int          | ch           |  target channel number : 1 - 4                   |
| float        | db           |  0                                               |
| int          | deg          |  0-360                                           |


**Control BBoxOne beam direction by theta and phi angle**
The core function of BBox is to control beam steering. The following code snippet steers beam in diffirent direction. Please refer to next section for API parameters.

    setBeamAngle(obj, dev_sn, db, theta, phi)
| Type         | Name         | Value                                            |
| ------------ | ------------ | ------------------------------------------------ |
| BBoxCtrler   | obj          | BBoxCtrler class instance                        |
| string       | dev_sn       | BBox serial number                               |
| float        | db           |  0                                               |
| int          | theta        |  0-45                                            |
| int          | phi          |  0-360                                           |




