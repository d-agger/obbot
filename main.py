import logging
from keys import Keys
import logs

from dotenv import load_dotenv
load_dotenv()

from obbot import obbot


token = Keys().OBBOT_TOKEN
log_handler = logs.obbot_log_handler

obbot.run(
    token,
    log_handler=log_handler,
    log_level=logging.INFO
)