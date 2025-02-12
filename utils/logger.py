import sys
from pathlib import Path

from loguru import logger


class Logger:

    logger = None
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        logger.remove()
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        logger.add(
            "logs/app.log",
            rotation="10 MB",
            level="DEBUG",
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            backtrace=True,
            diagnose=True
        )

        logger.add(
            sys.stderr,
            level="INFO",
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
        )

        self.logger = logger
        self._initialized = True