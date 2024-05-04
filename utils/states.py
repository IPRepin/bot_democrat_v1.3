from aiogram.fsm.state import StatesGroup, State


class StatesAddStocks(StatesGroup):
    """
    Модуль определения состояний для добавления акций
    """
    NAME = State()
    DESCRIPTION = State()
    IMAGE = State()
    PRICE = State()
