# Getting Started with MATLAB Sample Code

## Prerequisites

1. Install Python *3.8 ~ 3.12* and install TLKCore follow reference user guide of [Getting Started with Python Sample Code](../Python/README.md) to make sure your Python environment first.
2. According to [Versions of Python Compatible with MATLAB Products by Release](https://www.mathworks.com/support/requirements/python-compatibility.html) to download MATLAB to maps your Python version.
   ![matlab](/images/table_matlab.svg)
3. Create the new directory: *files*
```
├── files
├── main.py
├── README.md
└── TLKCoreExample.m
```
5. [BBoxOne/Lite] Copy your calibration & antenna tables into **files/**.
   * BBox calibration tables -> **{SN}_{Freq}GHz.csv**
   * BBox antenna table -> **AAKIT_{AAKitName}.csv**

P.S. The following example executes *MATLAB R2021b & Pyhton 3.8 64bit* on Windows 10

## MATLAB sample execution steps

1. Copy **TLKCoreExample.m** to extracted directory.

2. Double-click TLKCoreExample.m to launch MATLAB process.
3. Modify to your Python version

   ![MATLAB_ver](/images/MATLAB_Python_version.png)

4. Press **Run** to execute.
