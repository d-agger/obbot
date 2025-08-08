import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from paths import LOGS_DIR
import os


os.makedirs(LOGS_DIR, exist_ok=True)

obbot_log_handler = TimedRotatingFileHandler(
    filename=LOGS_DIR / "obbot.log",
    when="midnight",
    interval=1,
    backupCount=14,
    encoding="utf-8",
    utc=True
)
obbot_log_handler.suffix = "%dd-%mm-%YY"

obbot_formatter = logging.Formatter('│ %(asctime)s │ %(name)s │ %(levelname)s ║║ %(message)s')
obbot_log_handler.setFormatter(obbot_formatter)

_root_logger = logging.getLogger()
_root_logger.setLevel(logging.INFO)

for handler in _root_logger.handlers[:]:
    _root_logger.removeHandler(handler)

_root_logger.addHandler(obbot_log_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(obbot_formatter)
_root_logger.addHandler(console_handler)

logging.getLogger("discord").setLevel(logging.INFO)