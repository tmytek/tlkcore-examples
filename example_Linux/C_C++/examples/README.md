# Setup TLKCore configurations

This example directory contains two sub directories, please configure to your own envirenment:

1. example/files/ : Place your calibration & antenna files into it
   * BBox calibration tables, {SN}_{Freq}.csv
   * BBox antenna table, {AAKIT_Name}.csv
2. example/config/
   * **device.conf**, it mentions the device infomations for Beamform & UD.
      * <u>Beamform</u> devices with SN as key then includes AAKIT name and the path to beam configruation.
      * <u>UD devices</u> only include SN as key then includes STATE with json format.
         *. Beam configruation files, i.g. CustomBatchBeams_D2230E013-28.csv.
      * You can edit/pre-config it via Office-like software or any text editor, no matter what it is config to one of below options:
        * A whole beam (BeamType=0)
           * beam_db: gain with float type, please DO NOT exceed the DR (dynamic range).
           * beam_theta with integer degree
           * beam_phi with integer degree
        * Custom beam (BeamType=1), suggest use TMXLAB Kit first to makes sure your settings.
           * ch: Assigned channel to config
              * ch_sw: 0 means channel is ON, 1 is OFF.
              * ch_db: gain with float type.
              * ch_deg: phase degree with int type.
3. There are some linked files, please build lib_tlkcore_cpp/ and lib_usrp_spi/ if necessary.
   * **libtlkcore_lib.so** -> ../lib_tlkcore_cpp/libtlkcore_lib.so
   * **include/tlkcore_lib.hpp** -> ../../lib_tlkcore_cpp/include/tlkcore_lib.hpp
   * **libusrp_fbs.so** -> ../lib_usrp_spi/libusrp_fbs.so
   * **include/usrp_fbs.hpp** -> ../../lib_usrp_spi/include/usrp_fbs.hpp
4. After libraries built, according to your Python environment, copy the extracted **lib/** from **TLKCore_release/** to **example/lib/**, and we already placed libs for Python3.6 as default.

# Building TLKCore+USRP Applications using CMake
After above process, to try it out, run these commands:

1. `mkdir build/` to creates a new build directory
2. `cd build/`
3. `cmake ..`
4. `make install`

See the CMakeLists.txt file to figure out how to set up a build system.

# Execute the built binary

This directory contains the generated binary: tlkcore_fbs, just run command:

      ./tlkcore_fbs
