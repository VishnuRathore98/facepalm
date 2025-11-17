import logging
from logging.config import dictConfig
from config import DevConfig, config


def obfuscated(email: str, obfuscated_length: int) -> int:
    characters = email[:obfuscated_length]
    first, last = email.split("@")
    return characters + ("*" * (len(first) - characters)) + "@" + last


class EmailObfuscationFilter(logging.Filter):
    def __init__(self, name: str = "", obfuscated_length: int = 2) -> None:
        super().__init__(name)
        self.obfuscated_length = obfuscated_length

    def filter(self, record: logging.LogRecord) -> bool:
        if "email" in record.__dict__:
            record.email = obfuscated(record.email, self.obfuscated_length)
        return True


handlers = ["default", "rotating_file", "logtail"]
if isinstance(config, DevConfig):
    handlers = ["default", "rotating_file", "logtail"]


async def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config, DevConfig) else 16,
                    "default_value": "-",
                },
                "email_obfuscation": {
                    "()": EmailObfuscationFilter,
                    "obfuscated_length": 2 if isinstance(config, DevConfig) else 0,
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%d-%m-%YT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%d-%m-%YT%H:%M:%S",
                    "format": "%(asctime)s %(msecs)03d %(levelname)-8s %(correlation_id)s %(name)s %(lineno)d %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",  # log level to start
                    "formatter": "file",  # type of formatter
                    "filename": "facepalm.log",  # file to save logs to
                    "maxBytes": 1024 * 1024,  # 1MB logs per file
                    "backupCount": 5,  # keep last 5 log files
                    "encoding": "utf8",  # diff encodings can inc or dec log byte size
                    "filters": ["correlation_id"],
                },
                "logtail": {
                    "class": "logtail.LogtailHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                    "source_token": config.LOGTAIL_API_KEY,
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "src": {
                    "handlers": handlers,
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False,
                },
                "databases": {"handlers": ["default"], "level": "WARNING"},
                "aiosqlite": {"handlers": ["default"], "level": "WARNING"},
            },
        }
    )
