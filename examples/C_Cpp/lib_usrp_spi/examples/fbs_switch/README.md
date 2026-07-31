# C/C++ Sample Code - FBS Switch (BBox 8x8 Duo Standalone SPI Tester)

## Introduction

`fbs_switch` is a small standalone tool that talks directly to the USRP X410's GPIO (HDMI-shaped
connector) SPI path implemented in [lib_usrp_spi/](../../), **without** going through TLKCoreService.

Use this when the BBox 8x8 Duo is already switched into external/fast-parallel control mode and is no
longer reachable via TLKCoreService's Ethernet scan - at that point, switching FBS beams is done purely
by sending SPI commands from the host over the X410's GPIO connector, so there's no need to spin up the
whole TLKCore Python wrapper (`lib_tlkcore_cpp/`) just to test it.

## Wiring

This tool targets the BBox 8x8 Duo wiring, which only uses 6 pins of the X4x0 HDMI/GPIO connector:

| USRP X4x0 HDMI Connector Pin | Signal   |
|-------------------------------|----------|
| Pin 1                         | SPI_CSB  |
| Pin 2                         | GND      |
| Pin 4                         | TX_EN    |
| Pin 6                         | SPI_CLK  |
| Pin 9                         | SPI_SDI (data line) |
| Pin 15                        | RX_EN    |

PDI(pin7)/LDB(pin10)/MISO-SDO(pin12) are not wired at all for this device - the BBox 8x8 Duo needs no
LDB pulse and latches FBS_ADDR straight off the SPI frame. See the `TMY_8X8_DUO` option in
[../../CMakeLists.txt](../../CMakeLists.txt) if you need to build for a different device with the
original pin4/PDI + LDB wiring instead.

## Prerequisites

1. Build `libusrp_fbs.so` first, see [Building UHD application/library using CMake](../../README.md).
2. UHD >= 4.10.0 installed (required by `lib_usrp_spi/CMakeLists.txt`).
3. BBox 8x8 Duo already wired to the X410 and switched into external/fast-parallel control mode.

## How to Run

### 1. Building `lib_usrp_spi`

Please reference [Building UHD application/library using CMake](../../README.md) first.

### 2. Building `fbs_switch` using CMake

1. `mkdir build/` to create a new build directory
2. `cd build/`
3. `cmake ..`
4. `make install`

### 3. Execute the built binary

    ./fbs_switch --addr {X410_MANAGEMENT_IP} [--mode 0|1]

* `--addr`: the X410's management IP (default `192.168.10.2`, override to match your setup)
* `--mode`: `0` = TX (default, TX_EN high / RX_EN low), `1` = RX (TX_EN low / RX_EN high)

## Usage

Once connected, the tool prompts for a command in a loop:

    Please enter FBS_ADDR (mode2, e.g. '5') or 'FBS_ADDR_A FBS_ADDR_B' (mode1, e.g. '5 20') or quit('q'):

* Enter a single number (e.g. `5`) -> Fast Command Mode 2 (A=B phase), sets one FBS_ADDR for both A/B.
* Enter two numbers separated by a space (e.g. `5 20`) -> Fast Command Mode 1 (A,B phase, independent),
  sets FBS_ADDR_A and FBS_ADDR_B separately.
* Enter `q` -> quit and release the connection to the X410.

## Notes

* The X410 can only be claimed by one client at a time. If a previous run of this tool (or any other UHD
  session) didn't exit cleanly, the next connection attempt will fail with `Someone tried to claim this
  device again` - make sure any prior process is fully stopped before reconnecting.
* `debug` in [usrp_fbs.cpp](../../usrp_fbs.cpp) is `false` by default; set it to `true` and rebuild
  `lib_usrp_spi` to print the actual SPI payload/pin config for troubleshooting.
