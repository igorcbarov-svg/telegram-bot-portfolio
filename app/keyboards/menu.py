from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="📋 Услуги / Прайс"), KeyboardButton(text="📝 Оставить заявку")],
        [KeyboardButton(text="ℹ️ Обо мне"), KeyboardButton(text="📞 Контакты")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard, 
        resize_keyboard=True, 
        input_field_placeholder="Выберите пункт меню..."
    )