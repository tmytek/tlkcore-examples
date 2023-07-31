Building UHD Application/Library using CMake
=====================================

This directory contains a tiny example of a UHD-based application.
It is completely independent of the UHD source tree and can be compiled
from any path as long as UHD is currently installed on the current machine.

To try it out, run these commands:

    $ mkdir build/
    $ cd build/
    $ cmake ..
    $ make install

This will find the pre-installed libraries from [UHD libraries](https://github.com/EttusResearch/uhd) and [UHD Installation](https://files.ettus.com/manual/page_install.html#install_linux), then link and compile the example program. Include header directories and library names are automatically gathered.

See the CMakeLists.txt file to figure out how to set up a build system.
