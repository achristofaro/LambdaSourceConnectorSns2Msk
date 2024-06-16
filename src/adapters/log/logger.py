import logging
from typing import Optional


class Logger:
    __instance: Optional[logging.Logger] = None

    def __configure_logging(
        self, level: int = logging.INFO, log_file: Optional[str] = None
    ) -> logging.Logger:
        logger = logging.getLogger()

        # Remove all existing handlers (if any)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler, if log_file is provided
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        Logger.__instance = logger
        return logger

    @classmethod
    def get_logger(
        cls, level: int = logging.INFO, log_file: Optional[str] = None
    ) -> logging.Logger:
        if cls.__instance is None:
            cls.__instance = cls().__configure_logging(level, log_file)
        return cls.__instance
