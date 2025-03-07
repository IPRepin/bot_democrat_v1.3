import asyncio
import logging

from config import settings

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter
from aiogram.fsm.storage.redis import RedisStorage


from hendlers.stock_hendlers.admin_add_stock import admin_stocks_router
from hendlers.admin_handlers.admin_handler import admin_router
from hendlers.admin_handlers.admin_mailing_hendlers import router_admin_mailing
from hendlers.hendler_commands import router_commands
from hendlers.user_handlers.main_users_handler import main_users_router
from hendlers.states_recording_handler import recorder_router
from hendlers.stock_hendlers.edit_stock import edit_stock_router
from hendlers.stock_hendlers.stocks_hendler import router_stocks
from middleware.phone_middleware import PhoneValidationMiddleware
from notification.scheduler import setup_scheduler
from utils.commands import register_commands
from utils.logger_settings import setup_logging



async def connect_telegram():

    storage = RedisStorage.from_url(settings.REDIS_URL)
    bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode="HTML")

    # Инициализируем планировщик здесь
    scheduler = setup_scheduler(bot)
    scheduler.start()

    dp = Dispatcher(storage=storage)
    dp.message.middleware(PhoneValidationMiddleware())
    dp.include_routers(router_commands,
                       main_users_router,
                       router_stocks,
                       recorder_router,
                       admin_router,
                       admin_stocks_router,
                       edit_stock_router,
                       router_admin_mailing,
                       )
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
    setup_logging()
    logger = logging.getLogger(setup_logging())
    main()

