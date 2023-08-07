# Getting Started with Python Sample Code

## Prerequisites

1. Install Python 3.6 or 3.8 or 3.10, the version must mapping with [TLKCore_release](https://github.com/tmytek/bbox-api/tree/master/example_Linux/TLKCore_release)
2. Extract zip file & put related files(BBox 5G Series) into files/
   ![](../../images/TLKCore_release.png)
3. Install related Python packages from requirements.txt
    `pip install -r requirements.txt`
4. (Optional)Install USB driver if scan interface includes *DevInterface.USB*
   * [Installation Guides for all platforms](https://ftdichip.com/document/installation-guides/)
   * Windows
       * Online-Host with external internet capability
           * Auto detect a new device and install driver
       * Offline-Host
           * Download [setup executable driver from FTDI](https://ftdichip.com/drivers/d2xx-drivers/) and install it.
   * Linux
       1. Follow [steps](https://gitlab.com/msrelectronics/python-ft4222/-/tree/master#accessrights) to create or extend **/etc/udev/rules.d/99-ftdi.rules** includes:
           `SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="601c", GROUP="plugdev", MODE="0666"`
       2. Try to reload udev rules or re-plugin USB devices.
           `sudo udevadm control --reload-rules`
           `sudo udevadm trigger`

## Commandline

---
    python3 main.py
