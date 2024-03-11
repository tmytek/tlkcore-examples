# TMYTEK TLKCore Documentation

* TMYTEK general API for Windows/Linux platform.

## Introduction

**TLKCore** is a core service which inside the TMXLAB KIT(TLK/[WEB-TLK](https://web-tlk.tmytek.com/)), it integrates Python built libraries which developing mmWave( n257 / n258 / n260 / n261 ) **beamforming** and **beam steering** applications on **BBox 5G Series(mmwave beamformer)** and **UDBox 5G Series(mmwave Up-down frequency converter)** and other standard products developed by TMYTEK.

The **.pyd** format release is for Windows shared library and **.so** format release is for Linux shared library. Python is a cross-platform programming language, and we provide the basic Python example for all devices/platforms in the release package, and C/C++ examples for Linux platform in **C_Cpp** folder. Please refer to the sample code inside each folder for the specific programming language.

### Architecture

#### Hardware

* TLKCore is running on Windows/Linux PC, to communicate with standard products developed by TMYTEK via Ethernet/ComPort/USB cable.
* (Optional) FBS part is optional solution to control BBox 5G series as fast beam steering.
  ![block](/images/TLKCore_block.png)

#### Software

* **TLKCoreService** is a  **entry point** for developer, all of operations/functions must passed by TLKCoreService, e.g. scanDevices(), initDev().
* TMYCommService is maintaining physical communications for all devices, it usually not handled directly by developer.
* TMYUtils defines all data structure for return data, let developer more easier to know current status of processed function.
* **TMYPublic** is a open source code, it defines all data structure which developer might used, e.g. RFMode(TX/RX), RetCode(OK/ERROR/...), UDState...etc.
* (Optional) **TMYBeamConfig** is option solution for FBS (fast beam steering), it aims to parse assigned csv file to a dict structure and check beam configuration, please reference [FBS](/examples//Python/README.md#FBS)
* All files/function under tmydev/ are all operating logic of standard products
* db/ used for WEB-TLK, developer could ignore it.

  ![architecture](/images/TLKCore_architecture.png)

##### Latest Release & Reference Guide

* [[Download Link](/release)]

* Supported languages

  ![support](/images/support_languages.png)

## Prerequisites

### Python 3

* Install Python *3.6 or 3.8 or 3.10* which mapping with [TLKCore_release](/release), and follow reference user guide of [Getting Started with Python Sample Code](/examples/Python/README.md) to make sure your Python environment first.

### Communication environment

Host PC can communicate with TMYTEK product through physical connection as the following items, most of products using Ethernet/RJ-45.

#### Ethernet/RJ-45

* DHCP - Put devide and host PC in the LAN.
* Static IP - Configure your network environment to IP: **192.168.100**.xxx, and Subnet Mask Bits <= `/24`, likes: 255.255.255.0

  ![network](/images/Network.png)

#### ComPort

* Windows
  * Launch **Device Manager**
* Linux
  1. `lsusb` to check your device.
  2. Create or extend **/etc/udev/rules.d/99-tmytek-usb.rules** including:

      ```shell
      SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", GROUP="plugdev", MODE="0666"
      SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", GROUP="plugdev", MODE="0666"
      ```

  3. To add blacklist of ModemManager, please create or extend **/lib/udev/rules.d/78-tmytek-usb.rules** including:

      ```shell
      # Overwrite to 77-mm-usb-device-blacklist.rules

      ACTION!="add|change|move|bind", GOTO="mm_usb_device_blacklist_end"
      SUBSYSTEM!="usb", GOTO="mm_usb_device_blacklist_end"

      # TMYTEK's PD
      ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", ENV{ID_MM_DEVICE_IGNORE}="1"
      ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", ENV{ID_MM_DEVICE_IGNORE}="1"

      LABEL="mm_usb_device_blacklist_end"
      ```

  4. Try to reload udev rules.
     1. `sudo udevadm control --reload-rules`
     2. `sudo udevadm trigger`
     3. Re-plugin com port device.

#### USB (Optional)

Install USB driver if scan interface includes `DevInterface.USB` -> [Installation Guides for all platforms](https://ftdichip.com/document/installation-guides/)

* Windows
  * Online-Host with external internet capability
    * Auto detect a new device and install driver
  * Offline-Host
    * Download [setup executable driver from FTDI](https://ftdichip.com/drivers/d2xx-drivers/) and install it.
* Linux
  1. `lsusb` to check your device.
  2. Follow [steps](https://gitlab.com/msrelectronics/python-ft4222/-/tree/master#accessrights) to create or extend **/etc/udev/rules.d/99-tmytek-usb.rules** including:

      ```shell
      SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="601c", GROUP="plugdev", MODE="0666"
      ```

  3. Try to reload udev rules or re-plugin USB devices.
     1. `sudo udevadm control --reload-rules`
     2. `sudo udevadm trigger`

## Troubleshooting

1. I called `scanDevices()` but can not find my device via Ethernet.
   * [Action] Please check the following steps
     1. Make sure your physical connection, PC-device or PC-Router-Device...etc.
     2. Make sure your [network setting](#communication-environment).
     3. Check your firewall disabled, if you must enable firewall, please enable outgoing/incoming UDP or enable whitelist UDP ports: 5025, 7025-7040
        * Windows
          * `netsh advfirewall firewall add rule name="Allow UDP out" protocol=UDP dir=out localport=5025 action=allow`
          * `netsh advfirewall firewall add rule name="Allow UDP in" protocol=UDP dir=in localport=7025-7040 action=allow`
        * Ubuntu
          * `sudo ufw allow 5025/udp`
          * `sudo ufw allow 7025-7040/udp`
        * CentOS
          * `sudo firewall-cmd --permanent --add-port=5025/udp --add-port=7025-7040/udp`
          * `sudo systemctl restart firewalld`

2. Where is my calibration table or antenna table(AA-Kit)?
    * [Action] They shall put on your USB FLASH, copy them to **files/**.
