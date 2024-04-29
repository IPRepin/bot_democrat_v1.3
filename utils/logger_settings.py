import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logs_path = os.getenv('LOGS_PATH')
    if not logs_path:
        logs_path = "logs"
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    dt_now = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{logs_path}/{dt_now}_bot.log"
    log_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=5)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(log_handler)
