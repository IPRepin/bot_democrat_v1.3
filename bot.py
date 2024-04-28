import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from dotenv import load_dotenv

from data.sqlite_db_patient import DatabasePatient
from data.sqlite_db_stocks import DatabaseStocks
from data.sqlite_db_users import DatabaseUsers
from hendlers.hendler_commands import router_commands
from hendlers.main_users_handler import main_users_router
from hendlers.states_recording_handler import recorder_router
from hendlers.stocks_hendler import router_stocks
from utils.commands import register_commands
from utils.logger_settings import get_logger


def create_tables():
    try:
        db_stocks.create_table_stocks()
        db_users.create_table_users()
        db_patient.create_table_patient()
        logger.info("Tables created")
    except Exception as e:
        logger.exception(e)


async def connect_telegram():
    bot = Bot(token=telegram_token, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(router_commands,
                       main_users_router,
                       router_stocks,
                       recorder_router)
    create_tables()
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        await register_commands(bot)
    except TelegramNetworkError as error:
        logger.error(error)
    finally:
        await bot.close()


if __name__ == '__main__':
    load_dotenv()
    logger = logging.getLogger(__name__)
    get_logger()
    db_stocks = DatabaseStocks()
    db_users = DatabaseUsers()
    db_patient = DatabasePatient()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    try:
        asyncio.run(connect_telegram())
    except KeyboardInterrupt:
        logger.info('Bot interrupted')
