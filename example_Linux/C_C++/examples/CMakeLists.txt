cmake_minimum_required(VERSION 3.5...3.18)
project(tmy_dev_example CXX)

### Configure Compiler ########################################################
set(CMAKE_CXX_STANDARD 11)
# set(CMAKE_CXX_FLAGS "-g")

### Set up build environment ##################################################

# need these include and link directories for the build
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)
link_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Just likes: export LD_LIBRARY_PATH
set(CMAKE_INSTALL_RPATH ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
message(STATUS "$CMAKE_INSTALL_RPATH=" ${CMAKE_INSTALL_RPATH})
message(STATUS "$CMAKE_CURRENT_SOURCE_DIR=" ${CMAKE_CURRENT_SOURCE_DIR})

### Make the executable #######################################################
set(example_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/tlkcore_fbs.cpp
)
add_executable(tlkcore_fbs ${example_sources})
target_link_libraries(tlkcore_fbs tlkcore_lib) # -Wl,--no-as-needed)

# Default TRUE to setup beam config to BBox then let SPI control beams, or FALSE to set single beam to BBox
set(FBS TRUE)
if(FBS)
    # Fast beam steering via SPI
    message(STATUS "Set Beam control from SPI")
    # Add definition into source code
    target_compile_definitions(tlkcore_fbs PRIVATE TMY_FBS)
    target_link_libraries(tlkcore_fbs usrp_fbs)
else(FBS)
    # Direct to set beam via etherent
    message(STATUS "Set Beam control directly")
endif(FBS)

# Set the related path of output file path to the same path with CMakeLists.txt
install(TARGETS tlkcore_fbs DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})
