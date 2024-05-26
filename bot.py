import asyncio
import logging
import os
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv

from config import REDIS_URL, TELEGRAM_TOKEN
from data.sqlite_db_patient import DatabasePatient
from data.sqlite_db_stocks import DatabaseStocks
from data.sqlite_db_users import DatabaseUsers
from hendlers.stock_hendlers.admin_add_stock import admin_stocks_router
from hendlers.admin_handler import admin_router
from hendlers.admin_mailing_hendlers import router_admin_mailing
from hendlers.hendler_commands import router_commands
from hendlers.main_users_handler import main_users_router
from hendlers.states_recording_handler import recorder_router
from hendlers.stock_hendlers.edit_stock import edit_stock_router
from hendlers.stock_hendlers.stocks_hendler import router_stocks
from utils.commands import register_commands
from utils.logger_settings import setup_logging


def create_tables():
    try:
        db_stocks.create_table_stocks()
        db_users.create_table_users()
        db_patient.create_table_patient()
        logger.info("Tables created")
    except sqlite3.IntegrityError as err:
        logger.exception(err)
    except sqlite3.OperationalError as err:
        logger.exception(err)
    except sqlite3.DatabaseError as err:
        logger.exception(err)


async def connect_telegram():
    storage = RedisStorage.from_url(REDIS_URL)
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=storage)
    dp.include_routers(router_commands,
                       main_users_router,
                       router_stocks,
                       recorder_router,
                       admin_router,
                       admin_stocks_router,
                       edit_stock_router,
                       router_admin_mailing,
                       )
    create_tables()
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        await register_commands(bot)
    except TelegramNetworkError as error:
        logger.error(error)
    finally:
        await bot.close()


def main():
    try:
        asyncio.run(connect_telegram())
    except KeyboardInterrupt:
        logger.info('Bot interrupted')
        return
    except TelegramRetryAfter as error:
        logger.error(error)


if __name__ == '__main__':
    load_dotenv()
    setup_logging()
    logger = logging.getLogger(__name__)
    db_stocks = DatabaseStocks()
    db_users = DatabaseUsers()
    db_patient = DatabasePatient()
    main()
