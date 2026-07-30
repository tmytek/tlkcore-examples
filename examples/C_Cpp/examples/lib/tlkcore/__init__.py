
# =====================
# TLKCore package: unified API for TMYTEK device control, communication, and utilities
# Core public API - internal implementation details are hidden
# =====================
__version__ = "2.4.9"


# === CORE SERVICES ===
# Main communication and device management services
from .TLKCoreService import TLKCoreService
from .TMYCommService import TMYCommService, DevScanner, DevConnection
from .TMYDFU import TMYDFU
from .TMYBeamConfig import TMYBeamConfig
from .TMYLogging import TMYLogging


# === DEVICE CLASSES ===
# Main device types for RF and mmWave applications
from .tmydev.DevBBoard import BBoard, BBoard28A, BBoard26A, BBoard39A
from .tmydev.DevBBox import BBox, TCField
from .tmydev.DevBBoxLite import BBoxLite, BBoxLite28A, BBoxLite26A, BBoxLite39A
from .tmydev.DevBBoxOne import BBoxOne, BBoxOne26A, BBoxOne28A, BBoxOne39A
from .tmydev.DevBBoxDuo import BBoxDuo
from .tmydev.DevCloverCell import CloverCell, CloverCellEvb, CloverCellElite, CloverCellCttc, Slots
from .tmydev.device import Device, TMYDevType, DevInitState
from .tmydev.DevPD import PD
from .tmydev.DevRIS import RISController, RISRdtool
from .tmydev.DevUDB import UDB
from .tmydev.DevUDBox import UDBox
from .tmydev.DevUDC import UDConverter
from .tmydev.DevUDM import UDM


# === TABLE MANAGERS ===
# Beam pattern and calibration table management
from .tmydev.TMYTableManager import (
    BTModeFilter, BTSetOption, BTField, BTBeamField,
    BeamPatternTableManager, CalibrationTableManager,
    AAKitField, AAKitTableManager, UDDeltaFreqTableManager, TMYTableDBError
)


# === PUBLIC ENUMS & TYPES ===
# User-facing enums and configuration types
from .TMYPublic import (
    DevInterface, ScanFilter, IPMode, RFMode, CellRFMode, BeamType,
    UDFreq, UDState, UDMState, UDM_SYS, UD_PLO, UD_REF, UDM_LICENSE,
    UD_SN_TYPE, UD_LO_CONFIG, POLARIZATION, POLAR_SYNTHESIS, POLARIZATION_DEGSHIFT, POLARIZATION_TYPE,
    RIS_Dir, RIS_ModuleConfig, RetCode, AzElAngle, ThetaPhiAngle, BFICICConfig, BFICConfig
)
from .TMYUtils import RetType, VER, ScanMode

# === RIS Pattern Generator ===
from .tmydev import RIS_pattern_generator
from .tmydev.RIS_pattern_generator import (
    get_wave_len, rotate_pattern_90, calc_math, calc_numpy, calc, convert_csv
)


# === PUBLIC API DEFINITION ===
# Only core API is exported - internal implementation details are hidden
__all__ = [
    # === Core Services ===
    "TLKCoreService",
    "TMYCommService",
    "DevScanner",
    "DevConnection",
    "TMYDFU",
    "TMYBeamConfig",
    "TMYLogging",

    # === Device Classes ===
    "RISRdtool",

    # === Public Enums & Types ===
    "DevInterface", "ScanFilter", "IPMode", "RFMode", "CellRFMode", "BeamType",
    "UDFreq", "UDState", "UDMState", "UDM_SYS", "UD_PLO", "UD_REF", "UDM_LICENSE",
    "UD_SN_TYPE", "UD_LO_CONFIG", "POLARIZATION", "POLAR_SYNTHESIS", "POLARIZATION_DEGSHIFT", "POLARIZATION_TYPE",
    "RIS_Dir", "RIS_ModuleConfig", "RetCode",
    "RetType", "VER", "ScanMode", "AzElAngle", "ThetaPhiAngle", "BFICICConfig", "BFICConfig",
]


# === SECURITY & API PROTECTION ===
def __getattr__(name: str):
    """
    Dynamic attribute access control - prevents access to internal implementation details

    This function is called when users attempt to access attributes not in __all__,
    providing an additional protection layer to hide internal implementations.
    """
    # Check if attempting to access internal implementation (attributes starting with _)
    if name.startswith('_'):
        raise AttributeError(
            f"'{name}' is an internal implementation detail and not part of the public API. "
            f"Please refer to the documentation on https://tmytek.com/docs/tlkcore for available public APIs."
        )

    # Check if attempting to access known internal classes
    internal_classes = {
        'TCPConn', 'LANScanner', 'ComPortScanner', 'USBScanner', 'CLC_STAT',
        'DFU_TYPE', 'DFU_HEADER', 'ICMode', 'ChField', 'STAT', 'OPType',
        'SideBand', 'Ref_Type', 'IntRef_Type', 'ExtRef_Type', 'RspType', 'TMYTableDB',
        'Device', 'TMYDevType', 'DevInitState',
        'BBoard', 'BBoard28A', 'BBoard26A', 'BBoard39A',
        'BBox', 'TCField',
        'BBoxLite', 'BBoxLite28A', 'BBoxLite26A', 'BBoxLite39A',
        'BBoxOne', 'BBoxOne26A', 'BBoxOne28A', 'BBoxOne39A',
        'BBoxDuo',
        'CloverCell', 'CloverCellEvb', 'CloverCellElite', 'CloverCellCttc', 'Slots',
        'PD',
        'RISController',
        'UDB', 'UDBox', 'UDConverter', 'UDM',
        'BTModeFilter', 'BTSetOption', 'BTField', 'BTBeamField',
        'BeamPatternTableManager', 'CalibrationTableManager',
        'AAKitField', 'AAKitTableManager', 'UDDeltaFreqTableManager', 'TMYTableDBError',
        'RIS_pattern_generator',
        'get_wave_len', 'rotate_pattern_90', 'calc_math', 'calc_numpy', 'calc', 'convert_csv',
    }

    if name in internal_classes:
        raise AttributeError(
            f"'{name}' is an internal class and not available in the public API. "
            f"Please refer to the documentation on https://tmytek.com/docs/tlkcore to see available public classes."
        )

    # General attribute not found error
    raise AttributeError(f"module 'tlkcore' has no attribute '{name}'")


def __dir__():
    """
    Custom dir() output, only shows public APIs

    This ensures that when users use dir(tlkcore) or IDE auto-completion,
    they will only see public APIs and not internal implementations.
    """
    return __all__ + ['__version__', '__doc__', '__name__', '__package__']
