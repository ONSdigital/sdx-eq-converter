import os
import sys

import structlog
import logging
from structlog import configure
from structlog.contextvars import merge_contextvars
from structlog.stdlib import LoggerFactory


class _MaxLevelFilter(object):
    """Filter logs that are not above or equal to the current logging level"""

    def __init__(self, highest_log_level):
        self._highest_log_level = highest_log_level

    def filter(self, log_record):
        return log_record.levelno <= self._highest_log_level


def logging_config():
    """
    Sets the configuration for the logger
    The logging level is taken from the environment and defaults to INFO.
    """
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.ERROR)

    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    info_handler.addFilter(_MaxLevelFilter(logging.WARNING))

    logging.basicConfig(
        format='%(message)s',
        level=os.getenv('LOGGING_LEVEL', 'INFO'),
        handlers=[info_handler, error_handler]
    )

    configure(
        logger_factory=LoggerFactory(),
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            merge_contextvars,
            structlog.processors.JSONRenderer(),
        ],
    )
