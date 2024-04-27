import asyncio
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

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

logger = logging.getLogger(__name__)
db_stocks = DatabaseStocks()
db_users = DatabaseUsers()
db_patient = DatabasePatient()


def create_tables():
    try:
        db_stocks.create_table_stocks()
        db_users.create_table_users()
        db_patient.create_table_patient()
        logger.info("Tables created")
    except Exception as e:
        logger.error(e)


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
    logs_pash = os.getenv('LOGS_PASH')
    dt_now = datetime.now()
    dt_now = dt_now.strftime("%Y-%m-%d")
    log_handler = RotatingFileHandler(f'{logs_pash}/{dt_now}bot.log', maxBytes=1e6, backupCount=5)
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    telegram_token = os.getenv('TELEGRAM_TOKEN')
    try:
        asyncio.run(connect_telegram())
    except KeyboardInterrupt:
        logger.info('Bot interrupted')
