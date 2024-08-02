# Getting Started with Python Sample Code

## Prerequisites

1. Install Python *3.6 or 3.8 or 3.10*, the version must mapping with [TLKCore_release](/release)
    * Example gives a default libraries for *Python 3.8* ([python-3.8.10 64-bit download Link](https://www.python.org/downloads/release/python-3810))
    * Remember to **allow** the option: `Add python.exe to PATH`

        ![python38](/images/Python_Install38.png)

        ![python310](/images/Python_Install310.png)

2. Extract zip file.
3. Install related Python packages from requirements.txt

    `pip install -r requirements.txt`

4. Create the new directory named **files** to target directory.

   ![files](/images/TLKCore_release_files.png)

5. [BBoxOne/Lite] Copy your calibration & antenna tables into **files/** under the target directory.
   * BBox calibration tables -> **{SN}_{Freq}GHz.csv**
   * BBox antenna table -> **AAKIT_{AAKitName}.csv**

## Introduction of main.py

### Usage

```Python
usage: main.py [-h] [--dc SN Address DevType] [--dfu DFU] [--root ROOT]

optional arguments:
  -h, --help            show this help message and exit
  --dc SN Address DevType
                        Direct connect device to skip scanning, must provide 3 parameters: SN, IP and dev_type
  --dfu DFU             DFU image path
  --root ROOT           The root path/directory of for log/ & files/
```

### Basic call flow

* main() -> startService() -> testDevice() -> testXXX()

#### startService()

```Python
# You can assign a new root directory into TLKCoreService() to change files and log directory
service = TLKCoreService()

# Scan for devices
service.scanDevices(interface=interface)

# Some handling for scan result -> get: SN, address, dev type
# ...

# Init device, the first action for device before the operations
service.initDev(sn)

# Next function to test your device, it depends on SN or dev type to trigger its test function.
testDevice(sn, service)
```

#### testBBox()

```Python
# ====== MUST SET RFMODE TO BBOX ======
mode = RFMode.TX
service.setRFMode(sn, mode)

# ====== MUST SET FREQ TO LOAD CALIBRATION TABLE ======
target_freq = 28.0
ret = service.setOperatingFreq(sn, target_freq)

# Get dynamic range of gain for BBoxOne/Lite, the data lists are from calibration tables.
rng = service.getDR(sn, mode).RetData
gain_max = rng[1]

# ====== Select AAKit, please call getAAKitList() to fetch all AAKit list in files/ ======
aakit_selected = False
aakitList = service.getAAKitList(sn).RetData
for aakit in aakitList:
    if '4x4' in aakit:
        service.selectAAKit(sn, aakit)
        aakit_selected = True
        break
if not aakit_selected:
    logger.warning("PhiA mode")

# Test example options, you can decide what to test
testChannels = True
testBeam = False
testFBS = False

if testChannels:
    """Individual gain/phase/switch control example"""
    # Set IC channel gain with common gain, and gain means element gain(offset) if assign common gain
    # Each element gain must between 0 and common_gain_rng if using common gain
    common_gain_max = 0 # Please ref getCOMDR()
    ele_dr_limit = 0 # Please ref getELEDR()
    ele_offsets = [ele_dr_limit, ele_dr_limit, ele_dr_limit, ele_dr_limit]
    logger.info("Set Gain for channel 1: %s" %service.setIcChannelGain(sn, 1, ele_offsets, common_gain_max))
    logger.info("Set Gain/Phase for channel 1: %s" %service.setChannelGainPhase(sn, 1, gain_max, 30))

    # Disable specific channel example
    logger.info("Disable channel 1: %s" %service.switchChannel(sn, 1, disable=True))

# Beam control example
if testBeam:
    if aakit_selected:
        service.setBeamAngle(sn, gain_max, 0, 0))
    else:
        logger.error("PhiA mode cannot process beam steering")

if testFBS:
    # Test example options
    batch_import = False

    if batch_import:
        # Please reference #FBS topic
        beam_config_file = "CustomBatchBeams.csv"
        batch = TMYBeamConfig(sn, service, beam_config_file)
        batch.applyBeams():
    else:
        # Skip it
```

#### testUDBox()

``` Python
# Get UD state
service.getUDState(sn)
# Off channel1
logger.info(service.setUDState(sn, 0, UDState.CH1))

# Get & set freq
logger.info("Get current freq: %s" %service.getUDFreq(sn))
# Passing: LO, RF, IF, Bandwidth with kHz
LO = 24e6
RF = 28e6
IF = 4e6
BW = 1e5
service.setUDFreq(sn, LO, RF, IF, BW)
```

## Commandline to run

    python3 main.py

## FBS

This topic introduces TLKCore how to process FBS (Fast Beam Steering), it loads a readable beam configuration file, then generates a internal data structure, and converts to SPI signals to BBoxOne/Lite.

* TMYBeamConfig
  * It comes from *tlkcore.TMYBeamConfig.py* in the downloaded library package with source code.

* Beam configuration file, i.g. [CustomBatchBeams_D2230E058-28.csv](/examples/C_Cpp/examples/config/CustomBatchBeams_D2252E058-28.csv). You can edit/pre-config it via Office-like software or any text editor, **PLEASE RENAME** it for real environment, and passing parameter to TMYBeamConfig()
  * Basic beam type, there are two basic types, usually we define to CHANNEL CONFIG as default.
    * A whole **BEAM config (BeamType=0)**
      * beam_db: gain with float type, please DO NOT EXCEED the DR (dynamic range).
      * beam_theta with integer degree
      * beam_phi with integer degree
    * **CHANNEL/Custom beam config(BeamType=1)**, suggest use TMXLAB Kit first to makes sure your settings.
      * ch: Assigned channel to config
      * ch_sw: 0 means channel is ON, 1 is OFF.
      * ch_db: gain with float type.
      * ch_deg: phase degree with int type.
  * Edit rule: lost fields always follow the rule of default beam/channel config
    * **Must assign TX/RX and BeamID**
    * Default takes **channel config** (not a beam)
    * Default **enabled** if not mentioned.
    * Default gives a **MAX value of gain DR** if BEAM config not mentioned.
    * Default gives a **MAX value of gain common+element DR** if CHANNEL config not mentioned.
    * Default gives **degree 0** for theta, phi ... etc
  * Example: TX beam1 will be MAX of DR with degree(0, 0), and TX beam8 just modify ch 9~12 to 1dB
     ![CustomBatchBeams](/images/CustomBatchBeams.png)

## Extra usage

1. I have my own project to import TLKCore, so I can not import TLKCore libraries under the current directory, how to import TLKCore libraries?
    * You can set the system environment variables to caller to finding TLKCore libraries, just modify the  caller (main.py) in the following example:

        ```Python
        # Please setup path of tlkcore libraries to environment variables,
        # here is a example to search from 'lib/' or '.'

        # REMOVED:
        # prefix = "lib/"
        # lib_path = os.path.join(root_path, prefix)
        # ADDED:
        lib_path = Path("C:\\MyTLKCore\\lib\\").absolute()
        ```

2. How to assign the path of **files/** and **tlk_core_log/** ?
    * You can assign a new root path as parameter to TLKCoreService

        ```Python
        service = TLKCoreService({Your_Path})
        ```

    * Or you can also try:

            python3 main.py --root {Your_Path}

3. I connected my device directly and I will not change my network environment, Is there any way to skip scanning procedure?
    * Please make sure you have scanned the device before, and record the scanned result from the log, then just passing the result to initDev() in the following example:

        1. Record SN, address, device type from log

            ![scanned](/images/scanned.png)

        2. Direct connect
           1. Via typing:

                    python3 main.py --dc D2230E013-28 192.168.100.121 9

           2. Or passing to initDev()
            `service.initDev(sn, addr, dev_type)`

4. DFU(Device FW Update), from TLKCore v1.2.1, support to update BBox series firmware via TLKCore now!
    1. Query/download FW image for your BBoxOne/BBoxLite/BBoard device
    2. Please disable firewall first to allow tftp protocol transmission
        * Windows
            * `netsh advfirewall set allprofile state off`
        * Ubuntu
            * `sudo ufw disable`
        * CentOS
            * `sudo systemctl stop firewalld`
        * macOS
            * `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off`
    3. Argument assign image path to main.py

            python3 main.py --dfu {IMAGE_PATH}
