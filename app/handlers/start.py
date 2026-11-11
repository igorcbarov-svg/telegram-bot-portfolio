from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.menu import get_main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>!\n\n"
        "Я бот-визитка. Здесь вы можете посмотреть мои услуги или оставить заявку.",
        reply_markup=get_main_menu()
    )