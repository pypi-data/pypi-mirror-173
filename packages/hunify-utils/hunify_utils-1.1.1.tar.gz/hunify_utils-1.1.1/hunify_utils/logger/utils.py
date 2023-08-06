import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

from .extras import ColorMethod
from .handler import ColoredStreamHandler


def set_root_logger(level: int, fmt: str = "%(levelname)s - %(message)s",
                    color_mode: ColorMethod = ColorMethod.LEVEL):
    r = logging.root
    r.setLevel(level)
    for h in r.handlers:
        r.removeHandler(h)
    c_handler = ColoredStreamHandler(sys.stdout, color_mode, fmt)
    c_handler.setLevel(level)
    r.addHandler(c_handler)


def add_simple_log_file(log_file: str, fmt: str = "%(asctimes)s - %(levelname)s - %(message)s"):
    if log_file is None or fmt is None:
        logging.error("Invalid parameters")
        raise AttributeError("Invalid parameters")

    root_logger = logging.root
    logging.info("Setting up file logging")
    file_handler = logging.FileHandler(filename=log_file)
    file_handler.setFormatter(logging.Formatter(fmt))
    file_handler.setLevel(root_logger.level)
    logging.root.addHandler(file_handler)


def add_rotating_log_file(log_file: str, fmt: str = "%(asctimes)s - %(levelname)s - %(message)s",
                          when: str = "midnight", interval: int = 1, backup_count: int = 10):
    if log_file is None or fmt is None:
        logging.error("Invalid parameters")
        raise AttributeError("Invalid parameters")

    root_logger = logging.root
    logging.info("Setting up file logging")
    file_handler = TimedRotatingFileHandler(filename=log_file, when=when, interval=interval, backupCount=backup_count)
    file_handler.setFormatter(logging.Formatter(fmt))
    file_handler.setLevel(root_logger.level)
    logging.root.addHandler(file_handler)
