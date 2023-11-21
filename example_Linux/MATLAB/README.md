<style>
th {text-align:start;}
.blue{height:4px;background:#00FFFF}
.navyblue{height:4px;background:#0076a8}
</style>

# Getting Started with MATLAB Sample Code

## Prerequisites

1. Install Python <u>3.6 or 3.8 or 3.10</u> which mapping with [TLKCore_release](https://github.com/tmytek/bbox-api/tree/master/example_Linux/TLKCore_release), and follow reference user guide of [Getting Started with Python Sample Code](https://github.com/tmytek/bbox-api/tree/master/example_Linux/Python/README.md) to make sure your Python environment first.
2. According to [Versions of Python Compatible with MATLAB Products by Release](https://www.mathworks.com/support/requirements/python-compatibility.html) to download MATLAB to maps your Python version.
   <table width="100%"><tbody><tr><th rowspan="2" width="16%">MATLAB Version</th><th colspan="6">Python Version</th></tr><tr><th width="14%" class="blue">3.10</th><th width="14%">3.9</th><th width="14%" class="blue">3.8</th><th width="14%">3.7</th><th width="14%" class="blue">3.6</th><tr><th>R2023b</th><td class="navyblue"> </td><td class="navyblue"> </td><td> </td><td> </td><td> </td></tr><tr><th>R2023a</th><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td><td></td><td></td></td></tr><tr><th>R2022b</th><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td><td><td> </td> </td></tr><tr><th>R2022a</th><td> </td><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td><td> </td></tr><tr><th>R2021b</th><td> </td><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td><td> </td></tr><tr><th>R2021a</th><td> </td><td> </td><td class="navyblue"> </td ><td class="navyblue"> </td><td> </td></tr><tr><th>R2020b</th><td> </td><td> <td class="navyblue"> </td></td><td class="navyblue"> </td><td class="navyblue"> </td></tr><tr><th>R2020a</th><td> </td><td> </td><td> </td><td class="navyblue"> </td><td class="navyblue"> </td></tr><tr><th>R2019b</th><td> </td><td> </td><td> </td><td class="navyblue"> </td><td class="navyblue"> </td></tr></tbody></table><table width="100%"><tbody><td class="navyblue"> </td></tbody></table> Compatible for MATLAB Interface/MATLAB Engine
3. Extract zip file under the [TLKCore_release](https://github.com/tmytek/bbox-api/tree/master/example_Linux/TLKCore_release)
4. Create the new directory: files
   ![](../../images/TLKCore_release.png)
5. [BBoxOne/Lite] Copy your calibration & antenna tables into **files/** under the [TLKCore_release](https://github.com/tmytek/bbox-api/tree/master/example_Linux/TLKCore_release)
   * BBox calibration tables -> **{SN}_{Freq}GHz.csv**
   * BBox antenna table -> **AAKIT_{AAKitName}.csv**

P.S. The following example executes <u>MATLAB R2021b & Pyhton 3.8</u> on Windows 10

## MATLAB sample execution steps

1. Copy **TLKCoreExample.m** to extracted/unzipped directory of [TLKCore_release](https://github.com/tmytek/bbox-api/tree/master/example_Linux/TLKCore_release)
   ![](../../images/MATLAB_1.png)
2. Double-click TLKCoreExample.m to launch MATLAB process.
3. Press **Run** to execute.