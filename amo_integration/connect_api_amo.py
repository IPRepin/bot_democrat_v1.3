from amocrm.v2 import tokens
import os
from dotenv import load_dotenv

load_dotenv()


def connect_amo():
    """
    Модуль подключения к АМО CRM
    """
    tokens.default_token_manager(
        client_id=os.getenv('AMO_CLIENT_ID'),
        client_secret=os.getenv('AMO_CLIENT_SECRET'),
        subdomain=os.getenv('AMO_SUBDOMAIN'),
        redirect_url=os.getenv('AMO_REDIRECT_URL'),
        storage=tokens.FileTokensStorage(directory_path=os.getenv('AMO_STORAGE_DIR')),  # by default FileTokensStorage
    )

    # tokens.default_token_manager.init(code=os.getenv('AMO_TOKEN_MANAGER'),
    #                                   skip_error=False)

