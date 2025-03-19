import sys
from pathlib import Path

from loguru import logger


class LoggerService:

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

        """
            Sto facendo l'unpack perchè as_posix restituisce una tupla e non una stringa
            In questo caso usando la sintassi di unpacking otteniamo la stringa del path in
            cui il logs dovranno essere salvati
        """
        (log_file_path,) = Path(logs_dir, "app.log").as_posix(),
        print(f"Log file path: {log_file_path}")

        logger.add(
            log_file_path,
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