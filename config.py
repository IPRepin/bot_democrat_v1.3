from functools import lru_cache

from pydantic.v1 import BaseSettings
from pydantic_settings import SettingsConfigDict

from dotenv import load_dotenv
load_dotenv()



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    REDIS_URL: str
    TELEGRAM_TOKEN: str
    LOGS_PATH: str

    TELEGRAM_LOGS_TOKEN: str
    TG_CHATID_LOGS: str

    POSTGRES_URL: str

    AMO_TOKEN_MANAGER: str
    AMO_CLIENT_ID: str
    AMO_CLIENT_SECRET: str
    AMO_SUBDOMAIN: str
    AMO_REDIRECT_URL: str
    AMO_STORAGE_DIR: str

    ADMINS_ID: str

    PRODOKTOROV_URL: str
    YANDEX_MAPS_URL: str

    CALL_A_TAXI: str

    STICKER_START: str
    STICKER_HELP: str

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
