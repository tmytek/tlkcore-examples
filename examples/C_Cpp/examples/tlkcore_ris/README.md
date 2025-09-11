# C/C++ Sample Code - RIS

Here is a C/C++ RIS example to control RIS devices via TLKCore.

![wrapper](/images/TLKCore_C_wrapper.png)

## Configuration files

```
├── lib
│   ├── TMYConfig.py
│   └── tlkcore/
└── tlkcore_ris
    ├── CMakeLists.txt
    ├── README.md
    ├── config/
    ├── libtlkcore_lib.so -> ../../lib_tlkcore_cpp/libtlkcore_lib.so
    └── src/
```
* This tlkcore_ris directory contains two sub directories, please configure to your own envirenment:
    1. [tlkcore_ris/config/](config/)
        * **device.conf** (Current default config), it mentions the device infomation for RIS.
          * *RIS devices* with SN as the key. Under each device, multiple controllable port are defined, each containing parameters that control the behavior of the RIS tiles or elements
        * **tile_up_device_with_rotate.conf**, this configuration file describes RIS devices where each tile (element) supports rotation. In addition to basic tile parameters, it allows specifying rotation angles or orientation settings for each tile, enabling scenarios where the direction of individual tiles needs to be dynamically adjusted. Please modify this file according to your device
    2. [tlkcore_ris/src/](src/)
        * **tlkcore_ris.cpp**, it contains the example code for controlling RIS devices.

* There are some **linked files**, please build lib_tlkcore_cpp/ if necessary.
  * **libtlkcore_lib.so** -> ../../lib_tlkcore_cpp/libtlkcore_lib.so
    * **include/tlkcore_lib.hpp** -> ../../lib_tlkcore_cpp/include/tlkcore_lib.hpp
* After libraries built, according to your Python environment, copy the extracted **../lib/** & **../logging.conf** from [TLKCore_release](/release) to **../lib/**, and we already placed libs for *Python 3.8* as default.

## How to Run

### 1. Building TLKCore C++ shared library using CMake

Please reference [Building TLKCore C++ shared library using CMake](../../lib_tlkcore_cpp/)

### 2. Building example applications using CMake

After the above process, build the example code then runs the left commands.


> **Notice:**  
> If you need to test `device.conf` or `tile_up_device_with_rotate.conf`, please make sure to update the config filename with `path` in the `src/tlkcore_ris.cpp` before building and running the example.
>
> **Current default config is using `device.conf`**

1. `mkdir build/` to creates a new build directory
2. `cd build/`
3. `cmake ..`
4. `make install`

### 3. Execute the built binary

This directory contains the generated binary: tlkcore_fbs, just run the command under tlkcore_ris/:

    ./tlkcore_ris
