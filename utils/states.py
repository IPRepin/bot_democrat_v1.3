from aiogram.fsm.state import StatesGroup, State


class StatesAddStocks(StatesGroup):
    """
    Модуль определения состояний для добавления акций
    """
    NAME = State()
    DESCRIPTION = State()
    PRICE = State()
