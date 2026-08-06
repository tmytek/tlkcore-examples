# FBS/TDBS Example (FT4232H / C232HM)

Sends BBox 8x8 Duo **Fast Broadcast Command** frames (Mode0/Mode1/Mode2)
via FTDI MPSSE, using either an **FT4232H** (channel A) or a **C232HM**
MPSSE cable (FT232H-based). Both expose the same ADBUS pin layout, so the
wiring and frame logic below apply to either device — only the pyftdi
device URL differs.

## Frame Formats

### Mode0 — 35-bit frame (individual TDBS + FBS per channel)

| Bits    | Field   | Width | Range            |
|---------|---------|-------|------------------|
| [34:30] | prefix  | 5     | Tx=0x1E, Rx=0x1C |
| [29:24] | TDBS_2  | 6     | 0–63             |
| [23:18] | TDBS_1  | 6     | 0–63             |
| [17:9]  | FBS_2   | 9     | 0–511            |
| [8:0]   | FBS_1   | 9     | 0–511            |


### Mode1 — 23-bit frame (independent FBS address per channel)

| Bits    | Field      | Width | Range            |
|---------|------------|-------|------------------|
| [22:18] | prefix     | 5     | Tx=0x1E, Rx=0x1C |
| [17:9]  | FBS_ADDR_2 | 9     | 0–511            |
| [8:0]   | FBS_ADDR_1 | 9     | 0–511            |

### Mode2 — 14-bit frame (same FBS address for both channels)

| Bits    | Field      | Width | Range            |
|---------|------------|-------|------------------|
| [13:9]  | prefix     | 5     | Tx=0x1E, Rx=0x1C |
| [8:0]   | FBS_ADDR   | 9     | 0–511            |

## Hardware Setup

MPSSE pin mapping (FT4232H channel A, and equivalently C232HM ADBUS):

| MPSSE Pin   | Signal  | Direction | C232HM wire color |
|-------------|---------|-----------|--------------------|
| bit 0 / TCK | SPI CLK | Output    | Orange (SK)        |
| bit 1 / TDI | SPI DO  | Output    | Yellow (DO)        |
| bit 3 / TMS | SPI CS  | Output (active low) | Brown (CS)  |
| bit 6 / GPIOL2 | TX_EN | Output  | White (GPIOL2)     |
| bit 7 / GPIOL3 | RX_EN | Output  | Blue (GPIOL3)      |

On Windows: use **Zadig** to install the WinUSB driver for the FT4232H
channel, or for the C232HM's single interface, before running.

## Requirements

```
pyftdi>=0.54.0
libusb-package
```

Install:

```bash
pip install -r requirements.txt
```

On Windows, also use **Zadig** to install the WinUSB driver before running
(one-time setup per machine):

1. Download Zadig from https://zadig.akeo.ie
2. Options → List All Devices
3. Select `FT4232H` Interface 0, or the C232HM's `USB Serial Converter` device
4. Driver → **WinUSB** → Replace Driver

Confirm the pyftdi device URL after driver setup:

```bash
python -c "from pyftdi.ftdi import Ftdi; Ftdi.show_devices()"
```

## Usage

### Interactive CLI

```bash
python FT232h_tdbs_fbs_module.py
```

Connecting opens the device and automatically pulses CS once — no need to
trigger CS manually. Commands available in the session:

| Command | Action                                    |
|---------|--------------------------------------------|
| `rf`    | Set Tx/Rx mode (GPIO held until changed)   |
| `0`     | Send a Mode0 frame (prompts for fields)    |
| `1`     | Send a Mode1 frame (prompts for fields)    |
| `2`     | Send a Mode2 frame (prompts for fields)    |
| `q`     | Quit                                       |

### One-off calls (stateless helper functions)

Each call opens the device, sends the frame, and closes it:

```python
from FT232h_tdbs_fbs_module import send_fbs_mode0, send_fbs_mode1, send_fbs_mode2

# Mode0 — Tx mode: TDBS_2=5, TDBS_1=3, FBS_2=100, FBS_1=200
send_fbs_mode0(mode=0, tdbs_2=5, tdbs_1=3, fbs_2=100, fbs_1=200)

# Mode1 — Tx mode: ADDR_1=100, ADDR_2=200
send_fbs_mode1(mode=0, addr_1=100, addr_2=200)

# Mode2 — Tx mode: ADDR=300
send_fbs_mode2(mode=0, addr=300)

# Custom device URL (if multiple FTDI devices connected)
send_fbs_mode2(mode=0, addr=300, url="ftdi://ftdi:232h:SERIALNO/1")
# (FT4232H channel A: url="ftdi://ftdi:4232:SERIALNO/1")
```

### Persistent session (`_FtdiSession`)

Keeps one FTDI connection open across multiple sends, so RF enable (TX/RX)
state isn't reset on every call. `session.open()` also pulses CS once, same
as the CLI — no manual CS call needed.

```python
from FT232h_tdbs_fbs_module import _FtdiSession, pack_mode0_frame, pack_mode2_frame

session = _FtdiSession(url="ftdi://ftdi:232h/1")
session.open()  # connect + auto CS pulse

session.set_rf(mode=0)  # Tx mode
frame = pack_mode0_frame(mode=0, tdbs_2=5, tdbs_1=3, fbs_2=100, fbs_1=200)
session.send_frame(frame, num_bits=35)

session.close()
```
