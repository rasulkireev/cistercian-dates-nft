import logging

ERROR_LOG_FILENAME = ".errors.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d "
            "%(levelname)s %(message)s",  #  What to add in the message
            "datefmt": "%Y-%m-%d %H:%M:%S",  # How to display dates
        },
        "simple": {
            "format": "%(message)s",  # As simple as possible!
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",  # The class to instantiate!
            # Json is more complex, but easier to read, display all attributes!
            "format": """
                    asctime: %(asctime)s
                    created: %(created)f
                    filename: %(filename)s
                    funcName: %(funcName)s
                    levelname: %(levelname)s
                    levelno: %(levelno)s
                    lineno: %(lineno)d
                    message: %(message)s
                    module: %(module)s
                    msec: %(msecs)d
                    name: %(name)s
                    pathname: %(pathname)s
                    process: %(process)d
                    processName: %(processName)s
                    relativeCreated: %(relativeCreated)d
                    thread: %(thread)d
                    threadName: %(threadName)s
                    exc_info: %(exc_info)s
                """,
            "datefmt": "%Y-%m-%d %H:%M:%S",  # How to display dates
        },
    },
    "handlers": {
        "logfile": {
            "formatter": "default",
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ERROR_LOG_FILENAME,
            "maxBytes": 1000,
            "backupCount": 100,
        },
        "verbose_output": {  # The handler name
            "formatter": "simple",  # Refer to the formatter defined above
            "level": "DEBUG",  # FILTER: All logs
            "class": "logging.StreamHandler",  # OUTPUT: Which class to use
            "stream": "ext://sys.stdout",  # Param for class above. It means stream to console
        },
        "json": {  # The handler name
            "formatter": "json",  # Refer to the formatter defined above
            "class": "logging.StreamHandler",  # OUTPUT: Same as above, stream to console
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "scripts": {  # The name of the logger, this SHOULD match your module!
            "level": "INFO",  # FILTER: only INFO logs onwards from "tryceratops" logger
            "handlers": [
                "verbose_output",  # Refer the handler defined above
            ],
        },
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "logfile",  # Refer the handler defined above
            "json",  # Refer the handler defined above
        ],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
