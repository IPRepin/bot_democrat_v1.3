import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from dotenv import load_dotenv

from hendlers.hendler_commands import router_commands

logger = logging.getLogger(__name__)


async def connect_telegram():
    bot = Bot(token=telegram_token, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(router_commands)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except TelegramNetworkError as error:
        logger.error(error)
    finally:
        await bot.close()


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    try:
        asyncio.run(connect_telegram())
    except KeyboardInterrupt:
        logger.info('Bot interrupted')
