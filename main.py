import logging

# Preliminaries
from dotenv import load_dotenv
import paths
load_dotenv()
from keys import ObKeys
import logs

# Import (and create) obbot
from obbot import obbot

# Import obbot modules
import importlib.util as iu
for m_file in paths.MODULES_DIR.glob("*.py"):
    m_name = m_file.stem
    logging.info(f"Loading module [{m_name}]...")
    m_path = m_file.resolve()
    spec = iu.spec_from_file_location(m_name, m_path)
    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)
logging.info(f"Modules loaded.")

# Start obbot
token = ObKeys().OBBOT_TOKEN
obbot.run(
    token,
    log_handler=logs.obbot_log_handler,
    log_formatter=logs.obbot_formatter,
    log_level=logging.INFO
)