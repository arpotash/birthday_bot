import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from router.offer import offer_router
from router.register import auth_router
from db import db_initialize


async def on_startup():
    await db_initialize()


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Прочитать приглашение'),
        BotCommand(command='/location', description='Локация проведения'),
    ]
    await bot.set_my_commands(main_menu_commands)


async def main():
    api_token = os.getenv('API_TOKEN')
    bot = Bot(token=api_token)
    dp = Dispatcher()
    await set_main_menu(bot)
    dp.include_router(offer_router)
    dp.include_router(auth_router)
    await dp.start_polling(bot, on_startup=on_startup)

# Start the bot and send broadcast message
if __name__ == '__main__':
    asyncio.run(main())
