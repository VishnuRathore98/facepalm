from logging.config import dictConfig
from src.config import DevConfig, config


async def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config, DevConfig) else 16,
                    "default_value": "-"
                }
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%d-%m-%YT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s"
                },
                "file": {
                    "class": "logging.Formatter",
                    "datefmt": "%d-%m-%YT%H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | [%(correlation_id)s] %(name)s:%(lineno)d - %(message)s"
                }
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id"]
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",  # log level to start
                    "formatter": "file",  # type of formatter
                    "filename": "facepalm.log",  # file to save logs to
                    "maxBytes": 1024 * 1024,  # 1MB logs per file
                    "backupCount": 5,  # keep last 5 log files
                    "encoding": "utf8",  # diff encodings can inc or dec log byte size
                    "filters": ["correlation_id"]
                }
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["default", "rotating_file"],
                    "level": "INFO"
                },
                "src": {
                    "handlers": ["default", "rotating_file"],
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False
                },
                "databases": {
                    "handlers": ["default"],
                    "level": "WARNING"
                },
                "aiosqlite": {
                    "handlers": ["default"],
                    "level": "WARNING"
                }
            }
        }
    )
