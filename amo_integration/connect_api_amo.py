from amocrm.v2 import tokens


def connect_amo():
    """
    Модуль подключения к АМО CRM
    """
    tokens.default_token_manager(
        client_id="831a98f2-657a-4742-94b2-baf905ecc771",
        client_secret="cxeJS7e3NgqZXRt6L3Q5xfiX3YRFU7GZD6tsT7KFlYiCJPCD94YW8gvHm6eei8D4",
        subdomain="demokratnn19",
        redirect_url="https://demokrat-nn.ru/",
        storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
    )

    # tokens.default_token_manager.init(code="def5020012e28016713aea03daf15c1c0af722cd99ed1b0d2444babc8109b66e52ea16fcd2a4b34b122314d6e6792678895adaf11ac35681325ddea6d38df3536fe46787796d5b1e4929aa16cb422074676e3a7fcf36f2ee44991c61ab138e6380d367c25e97807dd0b95988f7e6e5447c9a58e65deb83c0d51cd4d37e52f4b0686c91a4bfd9f6cfce21f14cdbedcfa5eef75d9d6cd9605f2a93fed9b856566c55eb907f693d9b6a41fe44969d4b69df8a45f6af6ffa54bc14ffd75e418882e382fbb72a7ce1ede7667fd63abf2fe37229f35b89b6736daea5a6ac84cf68e909d666408c76f56433ea013e43453bd872e9db100cb392805fd88f25e8e17dd414789b6efb248b4dac316d2219d5c2ff76e2db5b20e959dbf3659b4c63e269cae6503936d2b01240acd3296da1cd59a7d0815ab72b409a757966dbd22e02e63c1625ababddef3321830a2ddb1d2946eaca81632ea353eddcca754cf4578adca038377da31de9356bd13798677b212c7fbb37010435a62998631a7b7d1940ebfb4cb950fffd581e4bc149fd690e964aaa97e7fd5ee5f1c9f7bb91fef24252babe056df05247354d1071922ede3f1a489914fd23d9c94ceb8dc04c79070bacf7b46629b1565e70549549df922f72f46e44d7132aa41dbea72163e9267f4dc86f287fcade4da2849a2b34",
    #                                   skip_error=False)
