import logging


class Logger:

    @staticmethod
    def configure_logging(level=logging.INFO) -> logging.Logger:
        logging.basicConfig(level=level)
        return logging.getLogger()
