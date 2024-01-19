from enum import Enum, Flag, auto

class DevInterface(Flag):
    UNKNOWN = 0
    LAN     = auto()
    COMPORT = auto()
    USB     = auto()
    ALL     = LAN | COMPORT | USB

class RFMode(Enum):
    TX      = 0
    RX      = auto()

class BeamType(Enum):
    BEAM    = 0
    CHANNEL = auto()

class RetCode(Enum):
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
    ERROR_DFU               = auto()

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

    # WEB - Database related
    ERROR_DB_SERVER         = 50
    ERROR_DB_FEEDBACK       = auto()

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
    # PD device
    ERROR_PD_CALI           = 150
    ERROR_PD_SOURCE         = auto()
    # UDM device
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

class UDFreq(Enum):
    def __str__(self):
        return self.name
    UDFreq  = 0
    RFFreq  = auto()
    IFFreq  = auto()

class UDState(Enum):
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
    NO_SET      = 0
    SYSTEM      = auto()
    PLO_LOCK    = auto()
    REF_LOCK    = auto()
    LICENSE     = auto()
    ALL         = SYSTEM | PLO_LOCK | REF_LOCK | LICENSE

class UDM_SYS(Enum):
    SYS_ERROR       = -1
    NORMAL          = 0

class UD_PLO(Enum):
    UNLOCK          = -1
    LOCK            = 0

class UD_REF(Enum):
    UNLOCK          = -1
    INTERNAL        = 0
    EXTERNAL        = auto()

class UDM_LICENSE(Enum):
    VERIFY_FAIL_FLASH   = -2
    VERIFY_FAIL_DIGEST  = -1
    NON_LICENSE         = 0
    VERIFY_PASS         = auto()
