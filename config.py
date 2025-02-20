from pydantic import computed_field, PostgresDsn
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str
    TELEGRAM_TOKEN: str
    LOGS_PATH: str

    TELEGRAM_LOGS_TOKEN: str
    TG_CHATID_LOGS: str

    PATH_TO_DB: str

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

    class Config:
        env_file: str = ".env"

    @computed_field
    @property
    def asyncpg_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            port=self.POSTGRES_PORT,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            port=self.POSTGRES_PORT,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_DB,
        )

settings = Settings()
