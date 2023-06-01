# Building TLKCore C++ shared library using CMake

This directory contains a tiny C++ wrappper example of a TLKCore-based application.
It is completely independent of the TLKCore source tree.

To try it out, run these commands:

1. `mkdir build/` to creates a new build directory
2. `cd build/`
3. `cmake {options} ..`
4. `make install` to generate to your output path

`options` might be:

    -Dpybind11_DIR=~/.local/share/cmake/pybind11
    -DPYBIND11_PYTHON_VERSION=3.6

See the CMakeLists.txt file to figure out how to set up a build system.
