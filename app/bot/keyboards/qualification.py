from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой отмены"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )

def get_project_type_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Лонгрид для YouTube"))
    builder.add(KeyboardButton(text="Подкаст/интервью"))
    builder.add(KeyboardButton(text="Риелс/Shorts"))
    builder.add(KeyboardButton(text="Другое (уточнить)"))
    builder.add(KeyboardButton(text="❌ Отмена"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_services_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    services = [
        "Монтаж",
        "Обработка звука", 
        "Графика/моушн",
        "Цветокоррекция",
        "Создание клипов из материала"
    ]
    
    for service in services:
        builder.button(text=f"☐ {service}", callback_data=f"service_{service}")
    
    builder.button(text="✅ Готово", callback_data="services_done")
    builder.adjust(1)
    return builder.as_markup()

def get_deadline_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Срочно (3-5 дней) +30%"))
    builder.add(KeyboardButton(text="Стандартно (7-10 дней)"))
    builder.add(KeyboardButton(text="Не срочно (14+ дней)"))
    builder.add(KeyboardButton(text="❌ Отмена"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_budget_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    budgets = ["до 10К", "10-20К", "20-30К", "30К+", "Обсудим после ТЗ"]
    for budget in budgets:
        builder.add(KeyboardButton(text=budget))
    builder.add(KeyboardButton(text="❌ Отмена"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)