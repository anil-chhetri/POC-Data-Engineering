import logging
import sys

class CustomFormatter(logging.Formatter):
     # ANSI color codes
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[34;20m"
    green = "\x1b[32;20m"
    reset = "\x1b[0m"
    
    format_template = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + format_template + reset,
        logging.INFO: green + format_template + reset,
        logging.WARNING: yellow + format_template + reset,
        logging.ERROR: red + format_template + reset,
        logging.CRITICAL: bold_red + format_template + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class CustomLogger(logging.Logger):
    def __init__(self, name: str, level: int = logging.DEBUG) -> None:
        super().__init__(name, level)
        self.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CustomFormatter())
        self.addHandler(handler)