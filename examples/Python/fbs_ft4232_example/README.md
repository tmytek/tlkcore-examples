# FT4232H FBS/TDBS Example

Sends BBox 8x8 Duo **Fast Broadcast Command** frames (Mode0/Mode1/Mode2)
via FT4232H MPSSE.

## Frame Formats

### Mode0 — 35-bit frame (individual TDBS + FBS per channel)

| Bits    | Field   | Width | Range            |
|---------|---------|-------|------------------|
| [34:30] | prefix  | 5     | Tx=0x1E, Rx=0x1C |
| [29:24] | TDBS_2  | 6     | 0–63             |
| [23:18] | TDBS_1  | 6     | 0–63             |
| [17:9]  | FBS_2   | 9     | 0–511            |
| [8:0]   | FBS_1   | 9     | 0–511            |

Sent as 32 bits (MPSSE `0x11`) + 3 bits (MPSSE `0x13`) — exactly 35 clock cycles.

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

FT4232H Channel A MPSSE pin mapping:

| MPSSE Pin   | Signal  | Direction |
|-------------|---------|-----------|
| bit 0 / TCK | SPI CLK | Output    |
| bit 1 / TDI | SPI DO  | Output    |
| bit 2 / TDO | SPI DI  | Input     |
| bit 3 / TMS | SPI CS  | Output (active low) |

On Windows: use **Zadig** to install WinUSB or libusb-win32 driver for
the FT4232H channel before running.

## Requirements

```
pyftdi>=0.54.0
libusb-package
```

Install:

```bash
pip install -r requirements.txt
```

On Windows, also use **Zadig** to install the WinUSB driver for the FT4232H
channel before running (one-time setup per machine):

1. Download Zadig from https://zadig.akeo.ie
2. Options → List All Devices
3. Select `FT4232H` Interface 0
4. Driver → **WinUSB** → Replace Driver

## Usage

### Interactive CLI

```bash
python ft4232_fbs.py
```

Connecting opens the FT4232H and automatically pulses CS once — no need to
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
from ft4232_fbs import send_fbs_mode0, send_fbs_mode1, send_fbs_mode2

# Mode0 — Tx mode: TDBS_2=5, TDBS_1=3, FBS_2=100, FBS_1=200
send_fbs_mode0(mode=0, tdbs_2=5, tdbs_1=3, fbs_2=100, fbs_1=200)

# Mode1 — Tx mode: ADDR_1=100, ADDR_2=200
send_fbs_mode1(mode=0, addr_1=100, addr_2=200)

# Mode2 — Tx mode: ADDR=300
send_fbs_mode2(mode=0, addr=300)

# Custom device URL (if multiple FTDI devices connected)
send_fbs_mode2(mode=0, addr=300, url="ftdi://ftdi:4232:SERIALNO/1")
```

### Persistent session (`_FtdiSession`)

Keeps one FTDI connection open across multiple sends, so RF enable (TX/RX)
state isn't reset on every call. `session.open()` also pulses CS once, same
as the CLI — no manual CS call needed.

```python
from ft4232_fbs import _FtdiSession, pack_mode0_frame, pack_mode2_frame

session = _FtdiSession(url="ftdi://ftdi:4232/1")
session.open()  # connect + auto CS pulse

session.set_rf(mode=0)  # Tx mode
frame = pack_mode0_frame(mode=0, tdbs_2=5, tdbs_1=3, fbs_2=100, fbs_1=200)
session.send_frame(frame, num_bits=35)

session.set_rf(mode=1)  # switch to Rx mode
frame = pack_mode2_frame(mode=1, addr=300)
session.send_frame(frame, num_bits=14)

session.close()
```

## Usage Examples (no hardware needed to run)

```bash
python test_ft4232_fbs.py
```

`test_ft4232_fbs.py` prints frame-packing examples (no hardware required)
and shows commented-out examples of every send/GPIO/session call that
does require the FT4232H + BBox 8x8 Duo hardware.
