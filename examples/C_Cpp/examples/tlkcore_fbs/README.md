# C/C++ Sample Code - Fast Beamsteering

Here is a C/C++ fast beamsteering example to control BBoxOne 5G and UD devices via TLKCore, also control USRP to raise SPI signal via UHD driver to BBox.

![UHD](/images/TLKCore_UHD_usage.png)

## Configuration files

```
├── files
│   ├── AAKIT_TMYTEK-4x4_ONE_28_IDEAL.csv
│   ├── AAKIT_TMYTEK_28ONE_4x4_C2104L020-28.csv
│   ├── BeamTable
│   ├── D2230E013-28_28GHz.csv
│   └── D2252E058-28_28GHz.csv
├── lib
│   ├── TMYConfig.py
│   └── tlkcore/
└── tlkcore_fbs
    ├── CMakeLists.txt
    ├── README.md
    ├── config/
    ├── libtlkcore_lib.so -> ../../lib_tlkcore_cpp/libtlkcore_lib.so
    ├── libusrp_fbs.so -> ../../lib_usrp_spi/libusrp_fbs.so
    └── src/
```

* This example directory contains two sub directories, please configure to your own envirenment:
    1. [example/files/](/examples/C_Cpp//examples/files/) : [BBoxOne/Lite] Copy your calibration & antenna tables into **example/files/** under the [TLKCore_release](/release), see more to [change default path](../../lib_tlkcore_cpp/README.md#guideline-of-c-wrapper-for-tlkcore)
        * BBox calibration tables -> **{SN}_{Freq}GHz.csv**
        * BBox antenna table -> **AAKIT_{AAKitName}.csv**
    2. [example/config/](config/)
        * **device.conf**, it mentions the device infomations for Beamform & UD.
          * *Beamform devices* with SN as key then includes AAKIT name and the path to beam configruation.
          * *UD devices* only includes SN as key then includes STATE with json format.
        * [FBS] **Beam configuration file**, i.g. [CustomBatchBeams_D2230E058-28.csv](config/CustomBatchBeams_D2252E058-28.csv), please reference [FBS topic](/examples/Python/README.md#FBS) in Python example.

* There are some linked files, please build lib_tlkcore_cpp/ and lib_usrp_spi/ if necessary.
  * **libtlkcore_lib.so** -> ../../lib_tlkcore_cpp/libtlkcore_lib.so
    * **include/tlkcore_lib.hpp** -> ../../lib_tlkcore_cpp/include/tlkcore_lib.hpp
  * [FBS] **libusrp_fbs.so** -> ../../lib_usrp_spi/libusrp_fbs.so
  * **include/usrp_fbs.hpp** -> ../../lib_usrp_spi/include/usrp_fbs.hpp
* After libraries built, according to your Python environment, copy the extracted **lib/** & **logging.conf** from [TLKCore_release](/release) to **example/lib/**, and we already placed libs for *Python 3.8* as default.

## How to Run

### 1. Building TLKCore C++ shared library using CMake

Please reference [Building TLKCore C++ shared library using CMake](../../lib_tlkcore_cpp/)

### 2. [FBS] Building UHD application/library using CMake

Please reference [Building UHD application/library using CMake](../../lib_usrp_spi/)

### 3. Building example applications using CMake

After above process, there are 2 build options to choose example runs for FBS or direct beam, FBS is enabled in default, then runs the left commands.

1. Set build options to Enable FBS as TRUE or not, via edit examples/CMakeLists.txt
  ![FBS](/images/C_Cpp_FBS_option.png)
2. `mkdir build/` to creates a new build directory
3. `cd build/`
4. `cmake ..`
5. `make install`

### 4. Execute the built binary

This directory contains the generated binary: tlkcore_fbs, just run the command under examples/:

    ./tlkcore_fbs
