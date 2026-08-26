"""FTDI MPSSE SPI (FT4232H / C232HM) — BBox 8x8 Duo FBS/TDBS Fast Broadcast Command Modes 0/1/2."""

import logging
import time
from typing import Tuple

from pyftdi.ftdi import Ftdi

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

FBS_TX_PREFIX = 0x1E  # 0b11110
FBS_RX_PREFIX = 0x1C  # 0b11100

# MPSSE Low Byte GPIO command
_MPSSE_SET_BITS_LOW = 0x80
# CS is bit3 (active low); CLK=bit0, DO=bit1, DI=bit2(in), TX_EN=bit6, RX_EN=bit7
_GPIO_CS_BIT  = 0x08
_GPIO_DIR     = 0xCB  # bits 0,1,3,6,7 = output; bit 2 = input

# RF mode bits (ADBUS6=TX_EN, ADBUS7=RX_EN)
_GPIO_TX = 0x40  # ADBUS6=1, ADBUS7=0
_GPIO_RX = 0x80  # ADBUS6=0, ADBUS7=1

# MPSSE clock-data commands (negative edge = data changes on falling CLK, MSB first)
_MPSSE_BYTES_OUT_NEG_MSB = 0x11
_MPSSE_BITS_OUT_NEG_MSB  = 0x13

# pyftdi device URL. Same ADBUS/MPSSE pin mapping on FT4232H channel A and
# C232HM (FT232H-based cable) — only the product string differs.
DEFAULT_URL = "ftdi://ftdi:232h/1"


# ---------------------------------------------------------------------------
# Frame packing
# ---------------------------------------------------------------------------

def pack_mode0_frame(mode: int, tdbs_addr_2: int, tdbs_addr_1: int, fbs_addr_2: int, fbs_addr_1: int) -> int:
    """Pack a 35-bit Mode0 FBS/TDBS frame (Individual 1,2).

    Bit layout (MSB first):
      [34:30] prefix[4:0]  — Tx=0x1E, Rx=0x1C
      [29:24] TDBS_ADDR_2[5:0]
      [23:18] TDBS_ADDR_1[5:0]
      [17:9]  FBS_ADDR_2[8:0]
      [8:0]   FBS_ADDR_1[8:0]
    """
    if mode not in (0, 1):
        raise ValueError(f"mode must be 0 (Tx) or 1 (Rx), got {mode}")
    if not (0 <= tdbs_addr_2 <= 63):
        raise ValueError(f"tdbs_addr_2 out of range [0,63]: {tdbs_addr_2}")
    if not (0 <= tdbs_addr_1 <= 63):
        raise ValueError(f"tdbs_addr_1 out of range [0,63]: {tdbs_addr_1}")
    if not (0 <= fbs_addr_2 <= 511):
        raise ValueError(f"fbs_addr_2 out of range [0,511]: {fbs_addr_2}")
    if not (0 <= fbs_addr_1 <= 511):
        raise ValueError(f"fbs_addr_1 out of range [0,511]: {fbs_addr_1}")

    prefix = FBS_TX_PREFIX if mode == 0 else FBS_RX_PREFIX
    return (
        (prefix & 0x1F)  << 30 |
        (tdbs_addr_2 & 0x3F)  << 24 |
        (tdbs_addr_1 & 0x3F)  << 18 |
        (fbs_addr_2  & 0x1FF) <<  9 |
        (fbs_addr_1  & 0x1FF)
    )


def pack_mode1_frame(mode: int, addr_1: int, addr_2: int) -> int:
    """Pack a 23-bit Mode1 FBS frame (1,2 phase, independent).

    Bit layout (MSB first):
      [22:18] prefix[4:0]
      [17:9]  FBS_ADDR_2[8:0]
      [8:0]   FBS_ADDR_1[8:0]
    """
    if mode not in (0, 1):
        raise ValueError(f"mode must be 0 (Tx) or 1 (Rx), got {mode}")
    if not (0 <= addr_1 <= 511):
        raise ValueError(f"addr_1 out of range [0,511]: {addr_1}")
    if not (0 <= addr_2 <= 511):
        raise ValueError(f"addr_2 out of range [0,511]: {addr_2}")

    prefix = FBS_TX_PREFIX if mode == 0 else FBS_RX_PREFIX
    return (
        (prefix & 0x1F)  << 18 |
        (addr_2 & 0x1FF) <<  9 |
        (addr_1 & 0x1FF)
    )


def pack_mode2_frame(mode: int, addr: int) -> int:
    """Pack a 14-bit Mode2 FBS frame (1=2 phase).

    Bit layout (MSB first):
      [13:9] prefix[4:0]
      [8:0]  FBS_ADDR[8:0]
    """
    if mode not in (0, 1):
        raise ValueError(f"mode must be 0 (Tx) or 1 (Rx), got {mode}")
    if not (0 <= addr <= 511):
        raise ValueError(f"addr out of range [0,511]: {addr}")

    prefix = FBS_TX_PREFIX if mode == 0 else FBS_RX_PREFIX
    return (
        (prefix & 0x1F) << 9 |
        (addr   & 0x1FF)
    )


# ---------------------------------------------------------------------------
# MPSSE helpers
# ---------------------------------------------------------------------------

def _frame_to_mpsse_bytes(frame: int) -> Tuple[bytes, int]:
    """Split 35-bit frame into MPSSE send components (backward-compat helper)."""
    upper_32 = (frame >> 3) & 0xFFFFFFFF
    lower_3  = (frame & 0x7) << 5
    return upper_32.to_bytes(4, byteorder='big'), lower_3


def _split_frame(frame: int, num_bits: int) -> Tuple[bytes, int, int]:
    """Split an N-bit frame into full bytes + tail bits for MPSSE.

    Returns:
        full_bytes:  bytes for the full-byte portion (may be empty)
        tail_byte:   remaining bits MSB-aligned in a byte (0 if none)
        tail_bits:   number of remaining bits (0 if byte-aligned)
    """
    num_full_bytes = num_bits // 8
    remaining_bits = num_bits % 8

    if remaining_bits == 0:
        return frame.to_bytes(num_full_bytes, byteorder='big'), 0, 0

    full_val  = frame >> remaining_bits
    tail_val  = (frame & ((1 << remaining_bits) - 1)) << (8 - remaining_bits)
    full_bytes = full_val.to_bytes(num_full_bytes, byteorder='big')
    return full_bytes, tail_val, remaining_bits


def _build_mpsse_init(rf_bits: int = _GPIO_TX) -> bytes:
    """Return MPSSE initialization sequence (30 MHz SPI clock).

    Args:
        rf_bits: RF enable GPIO bits to set on init (_GPIO_TX or _GPIO_RX)
    """
    return bytes([
        0x8A,        # Disable divide-by-5 (use 60 MHz master clock)
        0x97,        # Turn off adaptive clocking
        0x8D,        # Disable three-phase clocking
        0x86, 0x00, 0x00,  # Set clock divisor: 60 MHz / ((1+0)*2) = 30 MHz
        _MPSSE_SET_BITS_LOW, _GPIO_CS_BIT | rf_bits, _GPIO_DIR,  # CS=1, RF bits set
    ])


def _build_mpsse_send(full_bytes: bytes, tail_byte: int, tail_bits: int, rf_bits: int = _GPIO_TX) -> bytes:
    """Build MPSSE command sequence: CS low -> bytes -> bits -> CS high.

    rf_bits is ORed into every GPIO write so TX/RX enable are never clobbered.
    """
    cmd = bytearray([_MPSSE_SET_BITS_LOW, rf_bits, _GPIO_DIR])  # CS=0

    if full_bytes:
        n = len(full_bytes) - 1
        cmd += bytes([_MPSSE_BYTES_OUT_NEG_MSB, n & 0xFF, (n >> 8) & 0xFF])
        cmd += full_bytes

    if tail_bits > 0:
        cmd += bytes([_MPSSE_BITS_OUT_NEG_MSB, tail_bits - 1, tail_byte])

    cmd += bytes([_MPSSE_SET_BITS_LOW, _GPIO_CS_BIT | rf_bits, _GPIO_DIR])  # CS=1
    return bytes(cmd)


def _send_raw_frame(frame: int, num_bits: int, url: str, rf_bits: int = _GPIO_TX) -> None:
    """Open the FTDI MPSSE device, send an N-bit frame via MPSSE, close."""
    full_bytes, tail_byte, tail_bits = _split_frame(frame, num_bits)

    ftdi = Ftdi()
    try:
        ftdi.open_from_url(url)
        ftdi.set_bitmode(0xFF, Ftdi.BitMode.MPSSE)
        time.sleep(0.05)
        ftdi.purge_buffers()

        ftdi.write_data(_build_mpsse_init(rf_bits))
        time.sleep(0.01)

        ftdi.write_data(_build_mpsse_send(full_bytes, tail_byte, tail_bits, rf_bits))
    except Exception as exc:
        logger.error(f"Failed to send frame: {exc}")
        raise
    finally:
        ftdi.close()


# ---------------------------------------------------------------------------
# Public send functions
# ---------------------------------------------------------------------------

def pulse_cs(mode: int = 0, url: str = DEFAULT_URL) -> None:
    """Assert CS low then deassert high, without clocking any data.

    Args:
        mode: 0 = Tx (ADBUS6 high), 1 = Rx (ADBUS7 high)
    """
    rf_bits = _GPIO_TX if mode == 0 else _GPIO_RX
    ftdi = Ftdi()
    try:
        ftdi.open_from_url(url)
        ftdi.set_bitmode(0xFF, Ftdi.BitMode.MPSSE)
        time.sleep(0.05)
        ftdi.purge_buffers()

        ftdi.write_data(_build_mpsse_init(rf_bits))
        time.sleep(0.01)

        ftdi.write_data(bytes([
            _MPSSE_SET_BITS_LOW, rf_bits,_GPIO_DIR,                  # CS=0
            _MPSSE_SET_BITS_LOW, _GPIO_CS_BIT | rf_bits, _GPIO_DIR,  # CS=1
        ]))
        logger.info(f"CS pulsed ({'Tx' if mode == 0 else 'Rx'} mode).")
    except Exception as exc:
        logger.error(f"Failed to pulse CS: {exc}")
        raise
    finally:
        ftdi.close()


def send_fbs_mode0(
    mode: int,
    tdbs_addr_2: int,
    tdbs_addr_1: int,
    fbs_addr_2: int,
    fbs_addr_1: int,
    url: str = DEFAULT_URL,
) -> None:
    """Send a 35-bit Mode0 FBS/TDBS frame (Individual 1,2)."""
    frame = pack_mode0_frame(mode, tdbs_addr_2, tdbs_addr_1, fbs_addr_2, fbs_addr_1)
    logger.info(
        f"Mode0 frame: mode={'Tx' if mode == 0 else 'Rx'} "
        f"TDBS_ADDR_2={tdbs_addr_2} TDBS_ADDR_1={tdbs_addr_1} FBS_ADDR_2={fbs_addr_2} FBS_ADDR_1={fbs_addr_1} "
        f"(0x{frame:09X}, 35 bits)"
    )
    _send_raw_frame(frame, 35, url, _GPIO_TX if mode == 0 else _GPIO_RX)
    logger.info("Mode0 frame sent successfully.")


def send_fbs_mode1(
    mode: int,
    addr_2: int,
    addr_1: int,
    url: str = DEFAULT_URL,
) -> None:
    """Send a 23-bit Mode1 FBS frame (1,2 phase, independent)."""
    frame = pack_mode1_frame(mode, addr_1, addr_2)
    logger.info(
        f"Mode1 frame: mode={'Tx' if mode == 0 else 'Rx'} "
        f"ADDR_1={addr_1} ADDR_2={addr_2} "
        f"(0x{frame:06X}, 23 bits)"
    )
    _send_raw_frame(frame, 23, url, _GPIO_TX if mode == 0 else _GPIO_RX)
    logger.info("Mode1 frame sent successfully.")


def set_rf_enable(mode: int, url: str = DEFAULT_URL) -> None:
    """Set TX/RX enable via ADBUS6/7 without clocking any SPI data.

    Args:
        mode: 0 = Tx (ADBUS6=1, ADBUS7=0), 1 = Rx (ADBUS6=0, ADBUS7=1)
    """
    if mode not in (0, 1):
        raise ValueError(f"mode must be 0 (Tx) or 1 (Rx), got {mode}")
    rf_bits = _GPIO_TX if mode == 0 else _GPIO_RX
    ftdi = Ftdi()
    try:
        ftdi.open_from_url(url)
        ftdi.set_bitmode(0xFF, Ftdi.BitMode.MPSSE)
        time.sleep(0.05)
        ftdi.purge_buffers()
        ftdi.write_data(_build_mpsse_init(rf_bits))
        logger.info(f"RF enable set to {'Tx' if mode == 0 else 'Rx'} (ADBUS6={'1' if mode == 0 else '0'}, ADBUS7={'0' if mode == 0 else '1'})")
    except Exception as exc:
        logger.error(f"Failed to set RF enable: {exc}")
        raise
    finally:
        ftdi.close()


def send_fbs_mode2(
    mode: int,
    addr: int,
    url: str = DEFAULT_URL,
) -> None:
    """Send a 14-bit Mode2 FBS frame"""
    frame = pack_mode2_frame(mode, addr)
    logger.info(
        f"Mode2 frame: mode={'Tx' if mode == 0 else 'Rx'} "
        f"ADDR={addr} "
        f"(0x{frame:04X}, 14 bits)"
    )
    _send_raw_frame(frame, 14, url, _GPIO_TX if mode == 0 else _GPIO_RX)
    logger.info("Mode2 frame sent successfully.")


class _FtdiSession:
    """Holds an open FTDI MPSSE session for the CLI.

    Keeps the device open so GPIO state (TX/RX enable) persists between
    commands without being reset by set_bitmode on each open.
    """

    def __init__(self, url: str = DEFAULT_URL) -> None:
        self._url     = url
        self._ftdi    = Ftdi()
        self._rf_bits = _GPIO_TX  # default TX

    def open(self) -> None:
        self._ftdi.open_from_url(self._url)
        self._ftdi.set_bitmode(0xFF, Ftdi.BitMode.MPSSE)
        time.sleep(0.05)
        self._ftdi.purge_buffers()
        self._ftdi.write_data(_build_mpsse_init(self._rf_bits))
        time.sleep(0.01)

    def close(self) -> None:
        self._ftdi.close()

    def set_rf(self, mode: int) -> None:
        """Set TX/RX enable pins without clocking any SPI data."""
        self._rf_bits = _GPIO_TX if mode == 0 else _GPIO_RX
        self._ftdi.write_data(bytes([
            _MPSSE_SET_BITS_LOW, _GPIO_CS_BIT | self._rf_bits, _GPIO_DIR,
        ]))
        logger.info(
            f"RF enable set to {'Tx' if mode == 0 else 'Rx'} "
            f"(ADBUS6={'1' if mode == 0 else '0'}, ADBUS7={'0' if mode == 0 else '1'})"
        )

    def pulse_cs(self) -> None:
        """Assert CS low then deassert high, without clocking any data."""
        self._ftdi.write_data(bytes([
            _MPSSE_SET_BITS_LOW, self._rf_bits,                _GPIO_DIR,
            _MPSSE_SET_BITS_LOW, _GPIO_CS_BIT | self._rf_bits, _GPIO_DIR,
        ]))
        logger.info("CS pulsed.")

    def send_frame(self, frame: int, num_bits: int) -> None:
        full_bytes, tail_byte, tail_bits = _split_frame(frame, num_bits)
        self._ftdi.write_data(_build_mpsse_send(full_bytes, tail_byte, tail_bits, self._rf_bits))


def main() -> None:
    url     = DEFAULT_URL
    rf_mode = 0  # session RF mode: 0=Tx, 1=Rx

    session = _FtdiSession(url)
    try:
        session.open()
        session.pulse_cs()
    except Exception as exc:
        logger.error(f"Failed to open device: {exc}")
        return

    print(f"FBS/TDBS CLI  (device: {url})")
    print("Commands: rf | 0 | 1 | 2 | q")
    print("Use 'rf' to set Tx/Rx — GPIO stays high/low until changed.")

    def _rf_label() -> str:
        return "Tx" if rf_mode == 0 else "Rx"

    try:
        while True:
            try:
                cmd = input(f"\n[{_rf_label()}]> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                break

            if cmd in ("q", "quit", "exit"):
                print("Bye.")
                break

            elif cmd == "rf":
                try:
                    new_mode = int(input("  mode (0=Tx, 1=Rx): "))
                    if new_mode not in (0, 1):
                        raise ValueError(f"mode must be 0 or 1, got {new_mode}")
                    session.set_rf(new_mode)
                    rf_mode = new_mode
                    print(f"  RF mode set to {_rf_label()} — GPIO held until next 'rf' command.")
                except ValueError as e:
                    print(f"  Error: {e}")

            elif cmd == "0":
                try:
                    tdbs_addr_2 = int(input("  TDBS_ADDR_2 [0-63]:  "))
                    tdbs_addr_1 = int(input("  TDBS_ADDR_1 [0-63]:  "))
                    fbs_addr_2  = int(input("  FBS_ADDR_2  [0-511]: "))
                    fbs_addr_1  = int(input("  FBS_ADDR_1  [0-511]: "))
                    frame = pack_mode0_frame(rf_mode, tdbs_addr_2, tdbs_addr_1, fbs_addr_2, fbs_addr_1)
                    logger.info(
                        f"Mode0 frame: mode={_rf_label()} "
                        f"TDBS_ADDR_2={tdbs_addr_2} TDBS_ADDR_1={tdbs_addr_1} FBS_ADDR_2={fbs_addr_2} FBS_ADDR_1={fbs_addr_1} "
                        f"(0x{frame:09X}, 35 bits)"
                    )
                    session.send_frame(frame, 35)
                    logger.info("Mode0 frame sent successfully.")
                except ValueError as e:
                    print(f"  Error: {e}")

            elif cmd == "1":
                try:
                    addr_1 = int(input("  ADDR_1 [0-511]: "))
                    addr_2 = int(input("  ADDR_2 [0-511]: "))
                    frame = pack_mode1_frame(rf_mode, addr_1, addr_2)
                    logger.info(
                        f"Mode1 frame: mode={_rf_label()} "
                        f"ADDR_1={addr_1} ADDR_2={addr_2} "
                        f"(0x{frame:06X}, 23 bits)"
                    )
                    session.send_frame(frame, 23)
                    logger.info("Mode1 frame sent successfully.")
                except ValueError as e:
                    print(f"  Error: {e}")

            elif cmd == "2":
                try:
                    addr = int(input("  ADDR [0-511]: "))
                    frame = pack_mode2_frame(rf_mode, addr)
                    logger.info(
                        f"Mode2 frame: mode={_rf_label()} "
                        f"ADDR={addr} "
                        f"(0x{frame:04X}, 14 bits)"
                    )
                    session.send_frame(frame, 14)
                    logger.info("Mode2 frame sent successfully.")
                except ValueError as e:
                    print(f"  Error: {e}")

            else:
                print("  Unknown command. Use: rf | 0 | 1 | 2 | q")

    finally:
        session.close()


if __name__ == "__main__":
    main()
