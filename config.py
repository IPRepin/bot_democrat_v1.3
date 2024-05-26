import os
from dotenv import load_dotenv


load_dotenv()


REDIS_URL = os.getenv("REDIS_URL")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AMO_CLIENT_ID = os.getenv("AMO_CLIENT_ID")
AMO_CLIENT_SECRET = os.getenv("AMO_CLIENT_SECRET")
AMO_SUBDOMAIN = os.getenv("AMO_SUBDOMAIN")
AMO_REDIRECT_URL = os.getenv("AMO_REDIRECT_URL")
AMO_STORAGE_DIR = os.getenv("AMO_STORAGE_DIR")
TELEGRAM_LOGS_TOKEN = os.getenv("TELEGRAM_LOGS_TOKEN")
TG_CHAT_ID_LOGS = os.getenv("TG_CHATID_LOGS")
LOGS_PATH = os.getenv("LOGS_PATH")
AMO_TOKEN_MANAGER = os.getenv("AMO_TOKEN_MANAGER")