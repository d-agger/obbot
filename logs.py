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