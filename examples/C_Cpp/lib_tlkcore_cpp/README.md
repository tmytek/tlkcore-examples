# Building TLKCore C++ shared library using CMake

This directory contains a tiny **C++ wrappper** example of a TLKCore-based library, it's completely independent of the TLKCore source tree.

For C/C++ supporting, please install related Python packages from requirements.txt
    `pip install -r requirements.txt`
    - P.S. Please check your install/execute environment are mapped for user account or root.

To try it out, run these commands:

1. `mkdir build/` to creates a new build directory
2. `cd build/`
3. `cmake {options} ..`
4. `make install` to generate to your output path

`options` might be(modify to **your Python version** here):

    -Dpybind11_DIR=~/.local/share/cmake/pybind11
    -DPYBIND11_PYTHON_VERSION=3.8

See the **CMakeLists.txt** file to figure out how to set up a build system.

  ```shell
  # This Python version gets used for Python API (if requested) as well as
  # all the build-time Python scripts
  set(PYTHON_MIN_VERSION "3.8")
  set(PYBIND11_PYTHON_VERSION 3.8)
  ```

## Guideline of C++ wrapper for TLKCore

Here provide some tips to enhance your wrapper/examples

1. Import external TLKCore libraries (if not under ./lib/)
    * New feature after TLKCore v1.2.1
    * Modify tlkcore_fbs.cpp:

      ```C++
      ptr = tlkcore_lib::make({Your_Import_Path});
      ```

2. Change default path for files/ and tlk_core_log/
    * New feature after TLKCore v1.2.0
    * Steps
        1. Open tlkcore_lib.cpp
        2. Add the specfic path as parameter to new TLKCoreService instance `py::module::import("tlkcore.TLKCoreService").attr("TLKCoreService")({Your_Path});`
        3. Remember to put tables into new files/
