# BBox API Document
Version: v1.2.4
Release date: Dec 30, 2019 

## Introduction

BBox API helps developers building their own applications. The release format is DLL and currently only support Windows operating system. The tested environment is Visual Studio and LabView 2015.


# Getting Started — Python
## Installation
----------

Please install pythonnet at first. It's necessary for using windows dll in python script.

Please create a folder, named "files" under C://
,and then put the BBoxLite beamsterring table in the folder.


## Initialization
----------
    clr.AddReference('BBoxLiteAPI')
    from BBoxLiteAPI import *
    instance = BBoxAPI()
    instance.Init()  


## Control example
----------
**Control Beam direction**
The core function of BBox is to control beam steering. The following code snippet steers beam to be off broadside with 15 dB of each channel and 10 degrees. You also need to point out which BBox device used by serial number.

    instance.BeamSteer("B191321000-24",instance.GetTxRxMode(), 15.0, 10.0);

 ****

**Obtain Tx or Rx state**
Use the following code to obtain the current Tx/Rx mode and store it in a variable m. You need to point out which BBox device used by serial number.

    trmode = instance.GetTxRxMode("B191321000-24");

**Switch Tx & Rx mode**
BBox is TDD based device. You need to point out which BBox device used by serial number.

    instance.SwitchTxRxMode("B191321000-24", 0); // Switch BBox to Tx mode
    instance.SwitchTxRxMode("B191321000-24", 1); // Switch BBox to Rx mode