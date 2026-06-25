# -*- coding: utf-8 -*-
"""
FT4222 SPI Master Example Code

This hardware communication architecture and initialization flow is derived from
and references the python-ft4222 project:
Source: https://gitlab.com/msrelectronics/python-ft4222
License: MIT License

Copyright (c) MSR Electronics GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
"""

import logging
import ft4222
from ft4222.SPI import Cpha, Cpol
from ft4222.SPIMaster import Mode, Clock, SlaveSelect

# Configure logging format
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Pattern ID (index) to set for FPS
TARGET_PATTERN_ID = 1


def set_fps_config(devA, pattern_id: int):
    """
    Set RIS_FPS Pattern ID and trigger FPS.
    """
    logger.info(f"==== Set RIS_FPS Pattern ID:{pattern_id} ====")

    # Extract to low and high bytes
    low_byte = int(pattern_id) & 0xFF
    high_byte = (int(pattern_id) >> 8) & 0xFF
    cmd = bytes.fromhex(f"08 F0 {low_byte:02X} {high_byte:02X}")

    # Set pattern
    devA.spiMaster_SingleReadWrite(cmd)

    # Trigger FPS
    cmd = bytes.fromhex("08 05 02")
    devA.spiMaster_SingleReadWrite(cmd)


def main():
    logger.info("Detecting connected FT4222 devices...")

    try:
        # 1. Create device info list and display details
        nbDev = ft4222.createDeviceInfoList()
        for i in range(nbDev):
            logger.info(f"Device [{i}]: {ft4222.getDeviceInfoDetail(i, False)}")

        if nbDev == 0:
            logger.warning(
                "No FT4222 devices detected. Please check hardware connections or drivers."
            )
            return

        # 2. Open the specified FT4222 device (The first channel typically defaults to 'FT4222 A')
        dev_description = "FT4222 A"
        logger.info(f"Attempting to open device: {dev_description}")
        devA = ft4222.openByDescription(dev_description)

        # 3. Initialize SPI Master mode
        # Parameters: Single mode, Clock div 8, CPOL Idle Low, CPHA Leading Edge, Slave Select 0
        # Adjust these timing parameters according to your actual external chip specification
        logger.info("Initializing SPI Master...")
        devA.spiMaster_Init(
            Mode.SINGLE, Clock.DIV_8, Cpol.IDLE_LOW, Cpha.CLK_LEADING, SlaveSelect.SS0
        )

        # 4. Set FPS Pattern ID and trigger FPS
        set_fps_config(devA, TARGET_PATTERN_ID)

        logger.info("FPS configuration and trigger commands sent successfully.")

    except Exception as e:
        logger.error(f"An error occurred during execution: {e}", exc_info=True)

    # Note: The python-ft4222 object automatically closes the underlying handle
    # when its lifecycle ends (GC collection), so explicit deletion/closure is omitted here.


if __name__ == "__main__":
    main()
