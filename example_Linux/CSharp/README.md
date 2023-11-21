# Getting Started with C# Sample Code

## Prerequisites

* Python 3
    1. Install Python <u>3.6 or 3.8 or 3.10</u> which mapping with [TLKCore_release](https://github.com/tmytek/bbox-api/tree/master/example_Linux/TLKCore_release), and follow reference user guide of [Getting Started with Python Sample Code](https://github.com/tmytek/bbox-api/tree/master/example_Linux/Python/README.md) to make sure your Python environment first.
        * Example gives a default libraries for Python 3.8 ([python-3.8.0 64-bit download Link](https://www.python.org/downloads/release/python-380/))
    2. Extract zip file under the [TLKCore_release](https://github.com/tmytek/bbox-api/tree/master/example_Linux/TLKCore_release) then copy the whole `lib/` & `logging.conf` to TLKCoreExample/
        ![](../../images/CS_Lib_copy.png)
    3. Make sure your Python related path already exist in environment variable: `Path`
* Visual Studio - Example runs on Visual Studio 2019 with .NET Framework 4.7.2
    1. Install **pythonnet**
        * Please follow [the reference link](https://learn.microsoft.com/en-us/nuget/consume-packages/install-use-packages-visual-studio) to install pythonnet 3.x.x
        ![](../../images/CS_Install_Python_Runtime.png)

    2. Setup Python version/path in ExampleMain.cs, and '.' is your output folder
        ![](../../images/CS_Python_Path_Setup.png)

## C# sample build steps

1. Launch TLKCoreExample\TLKCoreExample.sln
2. Build project

## C# sample execution steps

1. [BBoxOne/Lite] Copy your calibration & antenna tables into **files/** under the built folder likes <u>bin/Debug/<u>
    * BBox calibration tables -> **{SN}_{Freq}GHz.csv**
    * BBox antenna table -> **AAKIT_{AAKitName}.csv**
2. Launch TLKCoreExample.exe
