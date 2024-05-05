from aiogram.fsm.state import StatesGroup, State


class StatesAddStocks(StatesGroup):
    """
    Модуль определения состояний для добавления акций
    """
    NAME = State()
    DESCRIPTION = State()
    IMAGE = State()
    PRICE = State()


class MailingState(StatesGroup):
    """
    Модуль определения состояний для отправки рассылки
    """
    CALL_MAILING = State()
    MAIL_TEXT = State()
    ADD_MEDIA = State()
    ADD_BUTTON = State()
    BUTTON_TEXT = State()
    BUTTON_URL = State()