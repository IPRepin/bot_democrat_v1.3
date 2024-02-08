from aiogram.fsm.state import StatesGroup, State


class OnlineRecording(StatesGroup):
    """
    Модуль определения состояний для машины состояний онлайн записи
    """
    NAME = State()
    PHONE = State()
