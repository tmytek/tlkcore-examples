cmake_minimum_required(VERSION 3.5...3.18)
project(fbs_switch CXX)

### Configure Compiler ########################################################
set(CMAKE_CXX_STANDARD 17)

### Set up build environment ##################################################
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/../../include
)
link_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/../..
)

set(CMAKE_INSTALL_RPATH ${CMAKE_CURRENT_SOURCE_DIR}/../..)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

find_package(UHD 4.10.0 REQUIRED)
set(UHD_BOOST_REQUIRED_COMPONENTS
    program_options
    system
    thread
)
set(BOOST_MIN_VERSION 1.65)
include(UHDBoost)

include_directories(${Boost_INCLUDE_DIRS} ${UHD_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})

### Make the executable #######################################################
add_executable(fbs_switch src/fbs_switch.cpp)
target_link_libraries(fbs_switch usrp_fbs ${UHD_LIBRARIES} ${Boost_LIBRARIES})

install(TARGETS fbs_switch DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})
