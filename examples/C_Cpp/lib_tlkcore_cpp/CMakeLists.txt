
########################################################################
# Dependency Minimum Versions
########################################################################
set(CMAKE_MIN_VERSION "3.8")
set(GCC_MIN_VERSION "6.3.0")
set(CLANG_MIN_VERSION "6.0.0")
# This Python version gets used for Python API (if requested) as well as
# all the build-time Python scripts
set(PYTHON_MIN_VERSION "3.8")
#set(PYTHON_VERSION 3.6)
set(PYBIND11_PYTHON_VERSION 3.8)

cmake_minimum_required(VERSION 3.4...3.18)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "-g")

########################################################################
# Helpful Macros
########################################################################
macro(INCLUDE_SUBDIRECTORY subdir)
    #insert the current directories on the front of the list
    list(INSERT _cmake_source_dirs 0 ${CMAKE_CURRENT_SOURCE_DIR})
    list(INSERT _cmake_binary_dirs 0 ${CMAKE_CURRENT_BINARY_DIR})

    #set the current directories to the names of the subdirs
    set(CMAKE_CURRENT_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/${subdir})
    set(CMAKE_CURRENT_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/${subdir})

    #include the subdirectory CMakeLists to run it
    file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
    include(${CMAKE_CURRENT_SOURCE_DIR}/CMakeLists.txt)

    #reset the value of the current directories
    list(GET _cmake_source_dirs 0 CMAKE_CURRENT_SOURCE_DIR)
    list(GET _cmake_binary_dirs 0 CMAKE_CURRENT_BINARY_DIR)

    #pop the subdir names of the front of the list
    list(REMOVE_AT _cmake_source_dirs 0)
    list(REMOVE_AT _cmake_binary_dirs 0)
endmacro(INCLUDE_SUBDIRECTORY)

########################################################################
# Project setup
########################################################################
project(tlkcore CXX)
find_package(pybind11 REQUIRED)
# or add_subdirectory(pybind11)
# or cmake -Dpybind11_DIR={your path for pybind11xxx.cmake} ..

########################################################################
# Append to the list of sources for lib tlkcore
########################################################################
set(wrapper_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/src/tlkcore_lib.cpp
)
add_library(tlkcore_lib SHARED ${wrapper_sources})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(tlkcore_lib PRIVATE pybind11::embed)

# Set the related path of output file path to the same path with CMakeLists.txt
install(TARGETS tlkcore_lib DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})
message([MAIN] "TLKCORE=" ${wrapper_sources})

# cmake -DCMAKE_INSTALL_PREFIX="xxx" <build_path>
# 1. cmake -DCMAKE_INSTALL_PREFIX=".." ..
# 2. make install to generate to your output path
message([MAIN] "$CMAKE_INSTALL_PREFIX=" ${CMAKE_INSTALL_PREFIX})
message([MAIN] "$pybind11_DIR=" ${pybind11_DIR})
message([MAIN] "$CMAKE_CURRENT_SOURCE_DIR=" ${CMAKE_CURRENT_SOURCE_DIR})

########################################################################
# Include subdirectories (different than add)
########################################################################
# add_subdirectory(examples)
# INCLUDE_SUBDIRECTORY(examples)