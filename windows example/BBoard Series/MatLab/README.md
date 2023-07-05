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




**Get supported AAkit list based on aakit tables under files folder**

    aakit_list = getAAKitList(obj, dev_sn)
| Type         | Name         | Value                                            |
| ------------ | ------------ | ------------------------------------------------ |
| BBoxCtrler   | obj          | BBoxCtrler class instance                        |
| string       | dev_sn       | BBox serial number                               |

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






