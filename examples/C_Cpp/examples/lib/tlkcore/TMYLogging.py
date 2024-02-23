from datetime import datetime
import logging
import logging.config
import os

import tlkcore.TMYUtils as Utils

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
        """TLKCoreService calls TMYLogging.py if change another root path"""
        print('TMYLogging __init__')

    def applyLogger(self):
        # Update current dict
        print("applyLogger: %s" %Utils.root)
        self._LOGGING_CONFIG["handlers"]["file"]["filename"] = os.path.join(Utils.root, self._LOGGING_CONFIG["handlers"]["file"]["filename"])
        self._LOGGING_CONFIG["handlers"]["libFile"]["filename"] = os.path.join(Utils.root, self._LOGGING_CONFIG["handlers"]["libFile"]["filename"])

        logging.config.dictConfig(self._LOGGING_CONFIG)