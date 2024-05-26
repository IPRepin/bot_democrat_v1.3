from amocrm.v2 import tokens

from config import (AMO_CLIENT_ID, AMO_STORAGE_DIR,
                    AMO_REDIRECT_URL, AMO_SUBDOMAIN,
                    AMO_CLIENT_SECRET, AMO_TOKEN_MANAGER)


def connect_amo():
    """
    Модуль подключения к АМО CRM
    """
    tokens.default_token_manager(
        client_id=AMO_CLIENT_ID,
        client_secret=AMO_CLIENT_SECRET,
        subdomain=AMO_SUBDOMAIN,
        redirect_url=AMO_REDIRECT_URL,
        storage=tokens.FileTokensStorage(directory_path=AMO_STORAGE_DIR), )

    # tokens.default_token_manager.init(code=AMO_TOKEN_MANAGER,
    #                                   skip_error=False)
