import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def get_logger():
    logger = logging.getLogger(__name__)
    logs_pash = os.getenv('LOGS_PASH')
    dt_now = datetime.now()
    dt_now = dt_now.strftime("%Y-%m-%d")
    log_handler = RotatingFileHandler(f'{logs_pash}/{dt_now}bot.log', maxBytes=1e6, backupCount=5)
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)