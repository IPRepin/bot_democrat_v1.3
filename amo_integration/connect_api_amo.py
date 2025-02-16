from amocrm.v2 import tokens

from config import settings


def connect_amo():
    """
    Модуль подключения к АМО CRM
    """
    tokens.default_token_manager(
        client_id=settings.AMO_CLIENT_ID,
        client_secret=settings.AMO_CLIENT_SECRET,
        subdomain=settings.AMO_SUBDOMAIN,
        redirect_url=settings.AMO_REDIRECT_URL,
        storage=tokens.FileTokensStorage(directory_path=settings.AMO_STORAGE_DIR), )

    # tokens.default_token_manager.init(code="",
    #                                   skip_error=False)


