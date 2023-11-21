<style>
th {text-align:start;}
.blue{height:4px;background:#00FFFF}
.navyblue{height:4px;background:#03b585}
</style>

# Getting Started with LabVIEW Sample Code

## Prerequisites

1. Install Python <u>3.6 or 3.8 or 3.10</u> which mapping with [TLKCore_release](https://github.com/tmytek/bbox-api/tree/master/example_Linux/TLKCore_release), TLKCore libraries only support 64bit currently.
2. According to [Integrating Python Code in LabVIEW](https://www.ni.com/en/support/documentation/supplemental/18/installing-python-for-calling-python-code.html#section-1736000138) to download LabVIEW to maps your Python version. Please download 64bit version not 32bit.
   <table width="100%"><tbody><tr><th rowspan="2" width="16%">LabVIEW Version</th><th colspan="6">Python Version</th></tr><tr><th width="14%" class="blue">3.10</th><th width="14%">3.9</th><th width="14%" class="blue">3.8</th><th width="14%">3.7</th><th width="14%" class="blue">3.6</th><tr><th>2023 Q1</th><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td></tr><tr><th>2022 Q3</th><td> </td><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td></tr><tr><th>2021 SP1</th><td> </td><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td></tr><tr><th>2021</th><td> </td><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td><td class="navyblue"> </td></tr><tr><th>2020 SP1</th><td> </td><td> </td><td> </td><td> </td><td class="navyblue"> </td></tr><tr><th>2020</th><td> </td><td> </td><td> </td><td> </td><td class="navyblue"> </td></tr><tr><th>2019 SP1</th><td> </td><td> </td><td> </td><td> </td><td class="navyblue"> </td></tr><tr><th>2019</th><td> </td><td> </td><td> </td><td> </td><td class="navyblue"> </td></tr><tr><th>2018 SP1</th><td> </td><td> </td><td> </td><td> </td><td class="navyblue"> </td></tr></tbody></table>
   <table width="100%"><tbody><td class="navyblue"> </td></tbody></table> Compatible
3. Extract zip file under the [TLKCore_release](https://github.com/tmytek/bbox-api/tree/master/example_Linux/TLKCore_release)
4. Create the new directory named **files**
   ![](../../images/TLKCore_release.png)
5. [BBoxOne/Lite] Copy your calibration & antenna tables into **files/** under the [TLKCore_release](https://github.com/tmytek/bbox-api/tree/master/example_Linux/TLKCore_release)
   * BBox calibration tables -> **{SN}_{Freq}GHz.csv**
   * BBox antenna table -> **AAKIT_{AAKitName}.csv**

P.S. The following example executes <u>LabVIEW 2021 64bit & Pyhton 3.8 64bit</u> on Windows 10

## LabVIEW sample execution steps

1. Double-click BBox.vi or **TLKCore.lvproj** then BBox.vi.
   ![](../../images/LabVIEW_BBoxOne_1.png)
2. Please check fields under the description with <font color=#0000FF>BLUE</font> color
   1. Python version
      * Choose/edit the Python version you want to test.
   2. Module path
      * Browse the path of main.py under the TLKCore release, then assign it.
   3. SN
      * Fill the SN on your device, or you can 'Run' it to get SN from 'Scanned List' then fill it.
   4. TX/RX mode
      * Press button to switch TX/RX mode.
   5. Frequency
      * Choose/edit the frequency.
   6. AAKit name
      * Fill the AAKit name in the BBox antenna table, or you can 'Run' it to fetch from 'Current AAKit List' then fill it.
   7. Beam setting
      * Theta: degree 0~60, with step 1
      * Phi: degree 0~360, with step 1
      * Gain(dB): this example only provides the **MAX value of dynamic range** or you can modify to your setting via modifying Block Diagram of LabVIEW
3. 'Run' it.
4. Expected result shall be
   ![](../../images/LabVIEW_BBoxOne_success.png)