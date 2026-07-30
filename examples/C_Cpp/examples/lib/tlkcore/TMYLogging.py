from datetime import datetime
import logging
import logging.config

from pathlib import Path
from .TMYUtils import _Utils


# Public API definition
__all__ = [
    "TMYLogging",
]


class TMYLogging():
    """
    Customerize your logging setting here
    """
    _LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "": { # root logger
                "handlers": ["console", "file"],
                "level": logging.DEBUG,
                "propagate": False,
            },
            "TLKCoreService": {
                "handlers": ["console", "libFile"],
                "qualname": "TLKCoreService",
                "propagate": False,
            },
            "Comm":{
                "handlers": ["libConsole", "libFile"],
                "qualname": "Comm",
                "propagate": False,
            },
            "Device":{
                "handlers": ["libConsole", "libFile"],
                "qualname": "Device",
                "propagate": False,
            },
            "DFU":{
                "handlers": ["console", "libFile"],
                "qualname": "DFU",
                "propagate": False,
            },
            "CaliTbl":{
                "handlers": ["libFile"],
                "qualname": "CaliTbl",
                "propagate": False,
            },
            "AAKitTbl":{
                "handlers": ["libFile"],
                "qualname": "AAKitTbl",
                "propagate": False,
            },
            "BeamTbl":{
                "handlers": ["libFile"],
                "qualname": "BeamTbl",
                "propagate": False,
            },
            "UDDeltaTbl":{
                "handlers": ["libFile"],
                "qualname": "UDDeltaTbl",
                "propagate": False,
            },
            "TblDB":{
                "handlers": ["libFile"],
                "qualname": "TblDB",
                "propagate": False,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": logging.INFO,
                "formatter": "default",
            },
            "file":{
                "class": "logging.FileHandler",
                "level": logging.DEBUG,
                "filename": datetime.now().strftime("tlk_core_log/main-%Y-%m-%d.log"),
                "formatter": "default",
            },
            "libConsole": {
                "class": "logging.StreamHandler",
                "level": logging.ERROR,
                "formatter": "default",
            },
            "libFile":{
                "class": "logging.FileHandler",
                "level": logging.DEBUG,
                "filename": datetime.now().strftime("tlk_core_log/tlkcore-%Y-%m-%d.log"),
                "formatter": "default",
            }
        },
        "formatters": {
            "default": {
                "format": "%(asctime)s.%(msecs)3d - %(name)s - %(levelname)s : %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "plain": {
                "format": "%(message)s",
            },
        },
    }

    def __init__(self):
        """
        TLKCoreService calls TMYLogging.py if change another root path
        """
        print('TMYLogging __init__')

    def applyLogger(self):
        """
        Apply logging configuration
        """
        # Update current dict
        print(f"Apply logger path to : {_Utils._get_log_dir()}")

        # Get log directory (guaranteed to have value after _initRoot validation)
        log_dir_path = _Utils._get_log_dir()
        log_dir = Path(log_dir_path)
        log_dir.mkdir(parents = True, exist_ok = True)

        # Update filename path to use the log directory
        filename = self._LOGGING_CONFIG["handlers"]["file"]["filename"]
        self._LOGGING_CONFIG["handlers"]["file"]["filename"] = str(log_dir / Path(filename).name)

        # Update libFile handler path as well
        lib_filename = self._LOGGING_CONFIG["handlers"]["libFile"]["filename"]
        self._LOGGING_CONFIG["handlers"]["libFile"]["filename"] = str(log_dir / Path(lib_filename).name)

        logging.config.dictConfig(self._LOGGING_CONFIG)