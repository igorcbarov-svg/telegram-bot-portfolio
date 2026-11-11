from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import settings
from app.keyboards.menu import get_main_menu

router = Router()

# Создаем состояния для формы заявки
class OrderForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_contact = State()

# --- Обработчики обычных кнопок ---

@router.message(F.text == "📋 Услуги / Прайс")
async def show_services(message: Message):
    text = (
        "<b>Мои услуги и цены:</b>\n\n"
        "1. Разработка Telegram-ботов — от 5 000 ₽\n"
        "2. Настройка автоворонок — от 3 000 ₽\n"
        "3. Техническая поддержка — 1 000 ₽/мес\n\n"
        "Чтобы заказать, нажмите кнопку ниже:"
    )
    
    # Создаем inline-кнопку
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Оформить заявку", callback_data="start_order_inline")]
        ]
    )
    await message.answer(text, reply_markup=inline_kb)

@router.message(F.text == "ℹ️ Обо мне")
async def about_me(message: Message):
    text = (
        "<b>Обо мне:</b>\n\n"
        "Привет! Я разработчик Telegram-ботов на Python (aiogram 3).\n"
        "Делаю ботов для бизнеса, магазинов и автоматизации.\n\n"
        "Мой стек: Python, aiogram, SQLite, Docker."
    )
    await message.answer(text)

@router.message(F.text == "📞 Контакты")
async def contacts(message: Message):
    await message.answer("Связаться со мной: @твой_никнейм_в_тг")

# --- Логика формы заявки (FSM) ---

@router.message(F.text == "📝 Оставить заявку")
async def start_order(message: Message, state: FSMContext):
    await state.set_state(OrderForm.waiting_for_name)
    await message.answer("Давайте оформим заявку.\n\nКак вас зовут?", reply_markup=None)

@router.message(OrderForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderForm.waiting_for_contact)
    await message.answer(f"Приятно познакомиться, {message.text}!\n\nНапишите ваш номер телефона или @username для связи.")

@router.message(OrderForm.waiting_for_contact)
async def process_contact(message: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get('name')
    contact = message.text
    
    # 1. Отвечаем пользователю
    await message.answer("✅ Спасибо! Ваша заявка принята. Я свяжусь с вами в ближайшее время.")
    
    # 2. Возвращаем главное меню
    await message.answer("Возвращаемся в меню:", reply_markup=get_main_menu())
    
    # 3. ОТПРАВЛЯЕМ УВЕДОМЛЕНИЕ АДМИНУ
    admin_text = (
        f"🔥 <b>Новая заявка!</b>\n\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"📞 <b>Контакт:</b> {contact}\n"
        f"🆔 <b>Юзернейм:</b> @{message.from_user.username}"
    )
    try:
        await message.bot.send_message(chat_id=settings.ADMIN_ID, text=admin_text)
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")
    
    # Очищаем состояние
    await state.clear()

# --- Обработка inline-кнопки ---

@router.callback_query(F.data == "start_order_inline")
async def start_order_inline(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(OrderForm.waiting_for_name)
    await callback.message.answer("Давайте оформим заявку.\n\nКак вас зовут?", reply_markup=None)
    await callback.answer()