# Getting Started with Python Sample Code

## Prerequisites

1. Install Python *3.6 or 3.8 or 3.10*, the version must mapping with [TLKCore_release](/release)
    * Example gives a default libraries for *Python 3.8* ([python-3.8.10 64-bit download Link](https://www.python.org/downloads/release/python-3810))
2. Extract zip file & put related files(BBox 5G Series) into files/
    ![release](/images/TLKCore_release_files.png)

3. Install related Python packages from requirements.txt
    `pip install -r requirements.txt`

## Commandline

    python3 main.py

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
    * Please make sure you have scanned the devuce before, and record the scanned result from the log, then just passing the result to initDev() in the following example:

        1. Record SN, address, device type from log

            ![scanned](/images/scanned.png)

        2. Direct connect v
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

