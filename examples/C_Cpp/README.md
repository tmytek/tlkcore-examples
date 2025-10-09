# Getting Started with C/C++ Sample Code

## Introduction

Here is a simple architecture for C/C++ example to control BBoxOne 5G and UDBox 5G, RIS devices via TLKCore

* **examples/** includes simple applications which using library(*.so) built from lib_tlkcore_cpp/ or lib_usrp_spi/ , developer can choose one to build and execute
  1. [tlkcore_fbs](examples/tlkcore_fbs)
  2. [tlkcore_ris](examples/tlkcore_ris)

* **lib_tlkcore_cpp/** includes a tiny C++ wrappper example, it generates to libtlkcore_lib.so

* [FBS] **lib_usrp_spi/** a optional case, it includes UHD application/library and it invoke pre-installed UHD driver to raise SPI transmissions for BBox 5G series, it grnerates to libusrp_fbs.so as default.

```
├── examples
│   ├── files
│   ├── include
│   ├── lib
│   ├── tlkcore_fbs
│   └── tlkcore_ris
├── lib_tlkcore_cpp
│   ├── include
│   └── src
└── lib_usrp_spi
    └── include
```

![UHD](/images/TLKCore_UHD_usage.png)

## Prerequisites

1. Install Python *3.8 or 3.10 or 3.12*, and follow reference user guide of [Getting Started with Python Sample Code](/examples/Python/README.md)
2. For C/C++ supporting, please install related Python packages from [lib_tlkcore_cpp/requirements.txt](lib_tlkcore_cpp/requirements.txt)

   `pip install -r lib_tlkcore_cpp/requirements.txt`
