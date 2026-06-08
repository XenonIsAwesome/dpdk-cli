import logging
import os
import sys


def supports_color() -> bool:
    if not sys.stderr.isatty():
        return False

    # Respect NO_COLOR standard
    if os.environ.get("NO_COLOR"):
        return False

    # Force enable if requested
    if os.environ.get("FORCE_COLOR"):
        return True

    term = os.environ.get("TERM", "").lower()

    return term not in ("", "dumb")


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",  # Cyan
        logging.INFO: "\033[32m",  # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.WARN: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",  # Red
        logging.CRITICAL: "\033[1;31m",  # Bold Red
        logging.FATAL: "\033[1;31m"  # Bold Red
    }
    RESET = "\033[0m"

    def format(self, record):
        if supports_color():
            level_color = self.COLORS.get(record.levelno, "")
            record.levelname = f"{level_color}{record.levelname}{self.RESET}"
        return super().format(record)
