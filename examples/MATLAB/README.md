# Getting Started with MATLAB Sample Code

## Prerequisites

1. Install Python *3.8 ~ 3.12* and install TLKCore follow reference user guide of [Getting Started with Python Sample Code](../Python/README.md) to make sure your Python environment first.
2. According to [Versions of Python Compatible with MATLAB Products by Release](https://www.mathworks.com/support/requirements/python-compatibility.html) to download MATLAB to maps your Python version.

| MATLAB Version | Python 3.12 | Python 3.11 | Python 3.10 | Python 3.9 | Python 3.8 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **R2026a** | ✅ | ✅ | ✅ | ✅ | |
| **R2025b** | ✅ | ✅ | ✅ | ✅ | |
| **R2025a** | ✅ | ✅ | ✅ | ✅ | |
| **R2024b** | ✅ | ✅ | ✅ | ✅ | |
| **R2024a** | | ✅ | ✅ | ✅ | |
| **R2023b** | | ✅ | ✅ | ✅ | |
| **R2023a** | | | ✅ | ✅ | ✅ |
| **R2022b** | | | ✅ | ✅ | ✅ |
| **R2022a** | | | | ✅ | ✅ |
| **R2021b** | | | | ✅ | ✅ |
| **R2021a** | | | | | ✅ |

> Notice：`✅` mean supported。

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

P.S. The following example executes *MATLAB R2025a & Pyhton 3.10 64bit* on Windows 10

## MATLAB sample execution steps

1. Copy **TLKCoreExample.m** to extracted directory.

2. Double-click TLKCoreExample.m to launch MATLAB process.
3. Modify to your Python version

   ![MATLAB_ver](/images/MATLAB_Python_version.png)

4. Press **Run** to execute.
