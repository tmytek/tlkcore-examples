"""
Usage examples for FT232h_tdbs_fbs_module.py

Shows how to call each public function.
No hardware required for the frame-packing examples;
hardware (FT4232H or C232HM + BBox 8x8 Duo) is required for the send/GPIO examples.
"""

from FT232h_tdbs_fbs_module import (
    pack_mode0_frame,
    pack_mode1_frame,
    pack_mode2_frame,
    send_fbs_mode0,
    send_fbs_mode1,
    send_fbs_mode2,
    set_rf_enable,
    _FtdiSession,
)

# ---------------------------------------------------------------------------
# Frame packing (no hardware needed)
# ---------------------------------------------------------------------------

# Mode0: individual 1/2 channels, FBS + TDBS addresses
frame0 = pack_mode0_frame(mode=0, tdbs_addr_2=5, tdbs_addr_1=3, fbs_addr_2=100, fbs_addr_1=200)
print(f"Mode0 frame (Tx): 0x{frame0:09X}  ({frame0.bit_length()} bits)")

frame0_rx = pack_mode0_frame(mode=1, tdbs_addr_2=5, tdbs_addr_1=3, fbs_addr_2=100, fbs_addr_1=200)
print(f"Mode0 frame (Rx): 0x{frame0_rx:09X}  ({frame0_rx.bit_length()} bits)")

# Mode1: independent FBS address per channel
frame1 = pack_mode1_frame(mode=0, addr_1=100, addr_2=200)
print(f"Mode1 frame (Tx): 0x{frame1:07X}  ({frame1.bit_length()} bits)")

# Mode2: same FBS address for both channels
frame2 = pack_mode2_frame(mode=0, addr=300)
print(f"Mode2 frame (Tx): 0x{frame2:05X}  ({frame2.bit_length()} bits)")

# ---------------------------------------------------------------------------
# Send via FTDI MPSSE device (hardware required)
# ---------------------------------------------------------------------------

# Set RF mode to Tx and keep GPIO held
# set_rf_enable(mode=0)

# Send Mode0 frame (Tx, TDBS_ADDR_2=5, TDBS_ADDR_1=3, FBS_ADDR_2=100, FBS_ADDR_1=200)
# send_fbs_mode0(mode=0, tdbs_addr_2=5, tdbs_addr_1=3, fbs_addr_2=100, fbs_addr_1=200)

# Send Mode1 frame (Tx, ADDR_1=100, ADDR_2=200)
# send_fbs_mode1(mode=0, addr_1=100, addr_2=200)

# Send Mode2 frame (Tx, ADDR=300)
# send_fbs_mode2(mode=0, addr=300)

# Switch to Rx mode
# set_rf_enable(mode=1)
# send_fbs_mode2(mode=1, addr=300)

# ---------------------------------------------------------------------------
# Custom device URL (if multiple FTDI devices connected)
# ---------------------------------------------------------------------------

# send_fbs_mode2(mode=0, addr=300, url="ftdi://ftdi:232h:SERIALNO/1")
# (FT4232H channel A: url="ftdi://ftdi:4232:SERIALNO/1")

# ---------------------------------------------------------------------------
# _FtdiSession class (hardware required)
#
# Keeps one FTDI connection open across multiple sends, so RF enable (TX/RX)
# and CS stay in the state you last set instead of resetting on every call.
# session.open() also pulses CS once, so you don't need to call it manually.
# ---------------------------------------------------------------------------

# session = _FtdiSession(url="ftdi://ftdi:232h/1")
# session.open()                                     # connect + auto CS pulse
#
# session.set_rf(mode=0)                              # Tx mode
# frame = pack_mode0_frame(mode=0, tdbs_addr_2=5, tdbs_addr_1=3, fbs_addr_2=100, fbs_addr_1=200)
# session.send_frame(frame, num_bits=35)
#
# session.close()
