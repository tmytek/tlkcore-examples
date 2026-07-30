from enum import Enum, Flag, auto, IntEnum
from typing import Dict, List, Union
from dataclasses import dataclass, field


# Public API definition
__all__ = [
    # Core return codes
    "RetCode",

    # Device and connection interfaces
    "DevInterface", "ScanFilter", "IPMode",

    # RF and beam configurations
    "RFMode", "CellRFMode", "BeamType",

    # UD series configurations
    "UDFreq", "UDState", "UDMState", "UDM_SYS", "UD_PLO", "UD_REF",
    "UDM_LICENSE", "UD_SN_TYPE", "UD_LO_CONFIG",

    # Polarization
    "POLARIZATION", "POLARIZATION_TYPE", "POLAR_SYNTHESIS", "POLARIZATION_DEGSHIFT",

    # RIS configurations
    "RIS_Dir", "RIS_ModuleConfig",

    # Beam configurations
    "BFICICConfig", "BFICConfig",

    # Angle configurations
    "AzElAngle", "ThetaPhiAngle"
]


class RetCode(Enum):
    """
    Error code to represent the status of operations in TLKCore.
    """
    def __str__(self):
        return self.name
    def __int__(self):
        return self.value
    OK                      = 0
    WARNING                 = auto()
    ERROR                   = auto()
    NO_RESPONSE             = auto()
    # genereal operations
    ERROR_GET_SN            = 10
    ERROR_DEV_TYPE          = auto()
    ERROR_SCAN              = auto()
    ERROR_INIT_OBJECT       = auto()
    ERROR_DEV_NOT_INIT      = auto()
    ERROR_METHOD_NOT_FOUND  = auto()
    ERROR_METHOD_NOT_SUPPORT= auto()
    ERROR_REFLECTION        = auto()
    ERROR_POWER             = auto()
    ERROR_EXPORT_LOG        = auto()
    ERROR_FW_NOT_SUPPORT    = auto()
    ERROR_INVALID_PARAMETER = auto()
    ERROR_HW_NOT_SUPPORT    = auto()

    # Communication interface related
    ERROR_COMM_NOT_INIT     = 30
    ERROR_COMM_INIT         = auto()
    ERROR_DISCONNECT        = auto()
    ERROR_SOCKET            = auto()
    ERROR_SEND_CMD          = auto()
    ERROR_RESP_CMD          = auto()
    ERROR_SEND_CMD_TIMEOUT  = auto()
    ERROR_COMPORT           = auto()
    ERROR_USB               = auto()

    # CMD to device
    ERROR_CMD               = 40
    ERROR_CMD_INIT          = auto()
    ERROR_CMD_PARAM         = auto()

    # WEB - Database related
    ERROR_DB_SERVER         = 50
    ERROR_DB_FEEDBACK       = auto()

    # DFU - Device Firmware Update related
    ERROR_DFU               = 60
    ERROR_DFU_NOT_SUPPORT   = auto()
    ERROR_DFU_TYPE          = auto()
    ERROR_DFU_HEADER        = auto()
    ERROR_DFU_TRANSMIT      = auto()

    # Beamforming device
    ERROR_BF_STATE          = 100
    ERROR_BF_AAKIT          = auto()
    ERROR_BF_NO_AAKIT       = auto()
    ERROR_BF_CALI_PATH      = auto()
    ERROR_BF_BEAM           = auto()
    ERROR_BF_GAIN           = auto()
    ERROR_BF_PHASE          = auto()
    ERROR_BF_RFMODE         = auto()
    ERROR_BF_CALI_INCOMPLTE = auto()
    ERROR_BF_CALI_PARSE     = auto()
    ERROR_BF_TC             = auto()
    ERROR_BF_BEAM_FILE      = auto()
    WARNING_BF_PDET_LOW     = auto()
    WARNING_BF_PDET_HIGH    = auto()
    WARNING_BF_PDET_UNKNOWN = auto()
    # PD device
    ERROR_PD_CALI           = 150
    ERROR_PD_SOURCE         = auto()
    # RIS device
    ERROR_RIS_MODULE        = 160
    ERROR_RIS_CONFIG        = auto()
    # UDM/UDB device
    ERROR_FREQ_RANGE        = 240
    ERROR_LICENSE_LENGTH    = auto()
    ERROR_LICENSE_KEY       = auto()
    ERROR_REF_CHANGE        = auto()
    # UD device
    ERROR_UD_FREQ           = 245
    ERROR_FREQ_EQUATION     = 250
    WARNING_HARMONIC        = auto()
    ERROR_HARMONIC_BLOCK    = auto()
    ERROR_PLO_UNLOCK        = 253
    ERROR_PLO_CRC           = auto()
    ERROR_UD_STATE          = auto()

class RIS_Dir(dict):
    """
    A dict structure for RIS direction includes distance and angle.
    Used in :func:`~tlkcore.tmydev.DevRIS.RISController.setRISAngle`.

    Args:
        distance (float): Distance from RIS to the source/target
        angle (tuple): Angle of the target, given in (theta, phi) format or theta only with phi=0, Defaults to (0,0)

    Examples:
        * For a distance of 1 meter and an angle of (0, 0):
            >>> RIS_Dir(1)
        * For a distance of 1 meter and an angle of (0, 0):
            >>> RIS_Dir(1, (0, 0))
        * For a distance of 1 meter and an angle of (30, 0):
            >>> RIS_Dir(1, (30, 0))

    .. versionadded:: v2.3.0
    """
    def __init__(self, distance, angle:Union[int, tuple]=(0,0)):
        self['distance'] = distance
        if isinstance(angle, int):
            self['angle'] = (angle, 0)
        # elif isinstance(angle, tuple):
        #     # TODO: for multiple reflection angle only
        #     self['angle'] = [angle]
        else:
            self['angle'] = angle

class RIS_ModuleConfig(dict):
    """
    A data structure for RIS module configuration.
    Used in :func:`~tlkcore.tmydev.DevRIS.RISController.setRISAngle`.

    Args:
        central_freq_mhz (int): Operating central frequency in MHz.
        module (Union[int, list]): Specifies the target module partition to control.
            It can be a single value (e.g. 1), or a list (e.g. [1, 2]),
            or a nested list (e.g. [[1, 2]] or [[1, 2], [3, 4]]). Defaults to 1.
        module_rotate (dict): Specifies the clockwise rotation degree for each module, therefore the actual pattern will be counter-clockwise rotation
            The degree must be a multiple of 90.

    Examples:
        * 28GHz with only module 1, no rotation:
            >>> RIS_ModuleConfig(28000, 1)
        * 28GHz with module 1 and 2 in landscape orientation, no rotation:
            >>> RIS_ModuleConfig(28000, [1, 2])
        * 28GHz with module 1 and 2 in portrait orientation, rotate module 1 by 90 degrees:
            >>> RIS_ModuleConfig(28000, [[1], [2]], {'1': 90})
        * 28GHz with module 1 and 2 in landscape orientation, rotate module 1 by 90 degrees and module 2 by 180 degrees:
            >>> RIS_ModuleConfig(28000, [1, 2], {'1': 90, '2': 180})
        * 28GHz with module 1,2,3,4 in landscape orientation, no rotation:
            >>> RIS_ModuleConfig(28000, [1, 2, 3, 4])
        * 28GHz with module 1,2,3,4 in portrait orientation, no rotation:
            >>> RIS_ModuleConfig(28000, [[1], [2], [3], [4]])
        * 28GHz with module 1,2,3,4 in square orientation, rotate module 1 by 90 degrees and module 2 by 180 degrees:
            >>> RIS_ModuleConfig(28000, [[1, 2],
                                         [3, 4]], {'1': 90, '2': 180})

    .. versionadded:: v2.3.0
    """
    def __init__(self, central_freq_mhz:float, module:Union[int, list]=1, module_rotate=None):
        self['central_freq_mhz'] = central_freq_mhz
        self['module'] = module
        self['module_rotate'] = module_rotate

class DevInterface(Flag):
    """
    Defines device connect interface for scanning.
    Used in :func:`~tlkcore.TLKCoreService.TLKCoreService.scanDevices`.
    """
    UNKNOWN = 0
    LAN     = auto()
    COMPORT = auto()
    USB     = auto()
    ALL     = LAN | COMPORT | USB

class ScanFilter(Flag):
    """
    Defines scan filter flags for device scanning.
    Used in :func:`~tlkcore.TLKCoreService.TLKCoreService.getScanInfo`.

    """
    NONE    = 0
    NORMAL  = auto()
    DFU     = auto()
    ALL     = NORMAL | DFU

class IPMode(Enum):
    """
    Defines device IP mode as DHCP or static IP mode.
    """
    DHCP        = 0
    STATIC_IP   = auto()

class RFMode(Enum):
    """
    Defines RF mode of beamform devices series.
    """
    TX      = 0
    RX      = auto()

class CellRFMode(Enum):
    """
    Defines RF mode of cell devices series.
    """
    STANDBY = -1
    TX      = 0
    RX      = auto()
    def __int__(self):
        return self.value

class BeamType(Enum):
    """
    Defines beam type of beamform devices series for beam configuration with dict structure.
    Used in :func:`~tlkcore.tmydev.DevBBoxOne.BBoxOne.setBeamPattern`.

    Beam config includes keys:
        - db: The gain setting in the range of :func:`~tlkcore.tmydev.DevBBoxOne.BBoxOne.getDR`
        - theta: In the range of `STEERING_H` field from :func:`~tlkcore.tmydev.DevBBoxOne.BBoxOne.getAAKitInfo`
        - phi: In the range of 0-359

    .. code-block::
        :caption: Default Beam config

        {
            "db": MAX value of dynamic range (DR),
            "theta": 0,
            "phi": 0
        }

    Channel config includes keys:
        - board_{N}: the board index, starts from 1
            - common_db: common gain setting for all channels in the board
            - channel_{N}: channel index, starts from 1
                - sw: Disable switch, 0: enable/on, 1: disable/off
                - db: The gain setting, in the range of 0 - :func:`~tlkcore.tmydev.DevBBoxOne.BBoxOne.getELEDR`
                - deg: The phase degree in the range of 0-359.

    .. code-block::
        :caption: Default Channel config

        {
            "board_1": {
                "common_db": MAX value of COMDR,
                "channel_1": {
                    "sw": 0,
                    "db": MAX value of ELEDR,
                    "deg": 0
                },
                "channel_2": {
                    "sw": 0,
                    "db": MAX value of ELEDR,
                    "deg": 0
                },
                ...
            },
            "board_2": {
                ...
            },
            ...
        }

    """
    BEAM    = 0
    CHANNEL = auto()

class UDFreq(Enum):
    """
    UD frequency related categories, also used for key name of dict when calling :func:`~tlkcore.tmydev.DevUDBox.getUDFreq`
    """
    def __str__(self):
        return self.name
    UDFreq  = 0
    RFFreq  = auto()
    IFFreq  = auto()

class UDState(Enum):
    """
    The state of UDBox5G, the key, value pairs are defined as follows:

        ===========  =================== =========================
        State        Description         Value
        ===========  =================== =========================
        NO_SET       All status
        PLO_LOCK     Lock status         0: unlock, 1: locked
        CH1          CH1 enable          0: disable, 1: enable
        CH2          CH2 enable          0: disable, 1: enable
        OUT_10M      10MHz output        0: disable, 1: enable
        OUT_100M     100MHz output       0: disable, 1: enable
        SOURCE_100M  100MHz source       0: Internal, 1: External or :class:`~tlkcore.TMYPublic.UD_REF`
        LED_100M     LED state indicator 0: OFF, 1: WHITE, 2: BLUE
        PWR_5V       5V power output     0: disable, 1: enable
        PWR_9V       9V power output     0: disable, 1: enable
        ===========  =================== =========================
    """
    NO_SET          = -1
    PLO_LOCK        = 0
    CH1             = auto()
    CH2             = auto() # ignore it if single UD
    OUT_10M         = auto()
    OUT_100M        = auto()
    SOURCE_100M     = auto() # 0:Internal, 1:External
    LED_100M        = auto() # 0:OFF, 1:WHITE, 2:BLUE
    PWR_5V          = auto()
    PWR_9V          = auto()

class UDMState(Flag):
    """
    The state of UDM

        ===========  ===================== =========================
        State        Description           Reference class/enum
        ===========  ===================== =========================
        SYSTEM       System state          :attr:`UDM_SYS`
        PLO_LOCK     PLO Lock state        :attr:`UD_PLO`
        REF_LOCK     Reference Lock state  :attr:`UD_REF`
        LICENSE      License state         :attr:`UDM_LICENSE`
        ===========  ===================== =========================
    """
    NO_SET      = 0
    SYSTEM      = auto()
    PLO_LOCK    = auto()
    REF_LOCK    = auto()
    LICENSE     = auto()
    ALL         = SYSTEM | PLO_LOCK | REF_LOCK | LICENSE

class UDM_SYS(Enum):
    """
    It defines the :attr:`UDMState.SYSTEM` state of UDM
    """
    SYS_ERROR       = -1
    NORMAL          = 0

class UD_PLO(Enum):
    """
    It defines the :attr:`UDMState.PLO_LOCK` state of UD series
    """
    UNLOCK          = -1
    LOCK            = 0

class UD_REF(Enum):
    """
    It defines the :attr:`UDMState.REF_LOCK` state of UD series
    """
    UNLOCK          = -1
    INTERNAL        = 0
    EXTERNAL        = auto()

class UDM_LICENSE(Enum):
    """
    It defines the :attr:`UDMState.LICENSE` state of UDM
    """
    VERIFY_FAIL_FLASH   = -2
    VERIFY_FAIL_DIGEST  = -1
    NON_LICENSE         = 0
    VERIFY_PASS         = auto()

class UD_SN_TYPE(Flag):
    """
    The SN type of UD
    """
    UD_BOX      = 1
    UD_MODULE   = auto()
    ALL         = UD_BOX | UD_MODULE

class UD_LO_CONFIG(Enum):
    """
    It defines the LO config for UDB series

        ===================  ======= ======================
        Config (enum)        integer Description
        ===================  ======= ======================
        LO_CFG_INTERNAL      0       Set the LO to internal mode
        LO_CFG_INTERNAL_OUT  1       Set the LO to output mode
        LO_CFG_EXTERNAL_IN   2       Set the LO to external mode
        ===================  ======= ======================
    """
    LO_CFG_INTERNAL     = 0
    LO_CFG_INTERNAL_OUT = auto()
    LO_CFG_EXTERNAL_IN  = auto()
    def __str__(self):
        return self.name

class POLARIZATION(Flag):
    """
    Defines the polarization states for beamforming devices.
    """
    HORIZON         = 1
    VERTICAL        = auto()
    DUAL            = HORIZON | VERTICAL
    def __str__(self):
        return self.name.lower()

class POLAR_SYNTHESIS(IntEnum):
    """
    Defines the polarization synthesis states and phase diff degree for beamforming devices.
    """
    FORWARD             = 0
    BACKWARD            = 180
    # RHCP => V = H + 90
    RIGHT_HAND_CIRCULAR = 90
    # LHCP => V = H - 90 => V = H + 270
    LEFT_HAND_CIRCULAR  = 270
    def __str__(self):
        return self.name
    def __int__(self):
        return self.value

class POLARIZATION_DEGSHIFT(IntEnum):
    """
    Defines the additional polarization states with ic degree for beamforming devices.
    """
    POL_1 = 1
    POL_2 = auto()
    def __str__(self):
        return self.name
    def __int__(self):
        return self.value

class POLARIZATION_TYPE(IntEnum):
    """
    Defines the polarization type for beamforming devices.
    """
    POL_1 = 0
    POL_2 = auto()
    POL_H = auto()
    POL_V = auto()
    POL_RC = auto()
    POL_LC = auto()
    def __str__(self):
        return self.name
    def __int__(self):
        return self.value
@dataclass
class AzElAngle:
    """
    A data structure for azimuth and elevation angle, used in :func:`~tlkcore.tmydev.DevBBoxDuo.BBoxDuo.setBeamAngle`
    """
    azimuth: float
    elevation: float

@dataclass
class ThetaPhiAngle:
    """
    A data structure for theta and phi angle, used in :func:`~tlkcore.tmydev.DevBBoxDuo.BBoxDuo.setBeamAngle`
    """
    theta: int
    phi: int

@dataclass
class BFICICConfig:
    enable: List[int]      # per-channel; 1=enabled, 0=disabled
    com_gain_db: float
    ele_gain_db: List[float] # per-channel element gain in dB
    phase_deg: List[int]   # per-channel phase in degrees

@dataclass
class BFICConfig:
    """
    A data structure for BFIC config, used in :func:`~tlkcore.tmydev.DevBBoxDuo.BBoxDuo.setBficConfig`
    """
    tx: Dict[str, Dict[str, "BFICICConfig"]] = field(default_factory=dict)
    rx: Dict[str, Dict[str, "BFICICConfig"]] = field(default_factory=dict)
