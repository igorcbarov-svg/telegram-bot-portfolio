import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.handlers import start, menu_handler

from config import settings
from app.handlers import start

logging.basicConfig(level=logging.INFO)

async def main():
    print("Бот запускается...")
    
    # Теперь бот понимает HTML-теги (жирный шрифт и т.д.)
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Подключаем обработчики
    dp.include_router(start.router)
    dp.include_router(menu_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")