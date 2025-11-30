from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command  # Добавили Command
from aiogram.fsm.context import FSMContext

from app.bot.keyboards.qualification import get_project_type_keyboard  # Абсолютный импорт
from app.bot.states import ProjectStates
from app.services.ai_client import AIClient
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    welcome_text = (
        "Привет! Я ascer - ассистент по заявкам ascezis production.\n\n"
        "🎬 *Наш профиль:*\n"
        "• Монтаж YouTube-лонгридов, подкастов, образовательного контента\n"  
        "• Глубокая обработка звука (очистка, выправка, усиление, улучшение)\n"
        "• Графика и моушн-дизайн\n\n"
        "Выберите способ создания заявки:"
    )
    
    # Кнопки для выбора способа создания заявки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📱 Создать через Web App",
                web_app={"url": "https://overfemininely-subministrant-jenell.ngrok-free.dev/index.html"}
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Создать в чате",
                callback_data="create_in_chat"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Мои заявки",
                web_app={"url": "https://overfemininely-subministrant-jenell.ngrok-free.dev/index.html"}
            )
        ]
    ])
    
    await message.answer(welcome_text, reply_markup=keyboard)


@router.callback_query(F.data == "create_in_chat")
async def create_in_chat(callback: CallbackQuery, state: FSMContext):
    """Создание заявки в чате (старый способ)"""
    await callback.answer()
    await callback.message.answer(
        "1. Тип проекта:",
        reply_markup=get_project_type_keyboard()
    )
    await state.set_state(ProjectStates.waiting_for_project_type)


# AI анализ

@router.message(Command("analyze"))
async def cmd_analyze(message: Message, state: FSMContext):
    """AI анализ текущей заявки"""
    current_state = await state.get_state()
    
    if not current_state:
        await message.answer("❌ Нет активной заявки для анализа")
        return
    
    # Получаем текущие данные
    data = await state.get_data()
    
    await message.answer("🤖 Запускаю AI анализ текущей заявки...")
    
    try:
        ai_client = AIClient()
        analysis = await ai_client.analyze_project(data)
        
        response = f"""
📊 <b>AI АНАЛИЗ ТЕКУЩЕЙ ЗАЯВКИ</b>

🎯 <b>Оценка:</b> {analysis.get('realism_score')}/10
💰 <b>Бюджет:</b> {analysis.get('budget_adequacy')}
🚨 <b>Приоритет:</b> {analysis.get('priority_level')}

💵 <b>Цены:</b>
• Мин: {analysis.get('price_recommendations', {}).get('min_price')}₽
• Реком: {analysis.get('price_recommendations', {}).get('recommended_price')}₽  
• Макс: {analysis.get('price_recommendations', {}).get('max_price')}₽

⏱️ <b>Время:</b> {analysis.get('time_estimate_hours')}ч
⚠️ <b>Риски:</b> {', '.join(analysis.get('identified_risks', []))}
➕ <b>Рекомендации:</b> {', '.join(analysis.get('service_recommendations', []))}

📝 {analysis.get('summary')}
        """
        
        await message.answer(response, parse_mode="HTML")
        
    except Exception as e:
        await message.answer(f"❌ Ошибка AI анализа: {e}")


# Тестовая команда

@router.message(Command("testai"))
async def cmd_test_ai(message: Message):
    """Тест AI анализа"""
    from app.services.ai_client import AIClient
    from app.config import config
    
    # Проверяем API ключ
    if not config.ai.api_key or config.ai.api_key == "your_openrouter_api_key_here":
        await message.answer("❌ API ключ OpenRouter не установлен!")
        return
    
    await message.answer("🤖 Запускаю AI анализ тестовой заявки...")
    
    test_data = {
        "project_type": "Лонгрид для YouTube",
        "budget": "20-30К", 
        "services": ["Монтаж", "Обработка звука"],
        "deadline": "Стандартно (7-10 дней)",
        "duration_raw": "2 часа",
        "duration_final": "10-12 минут",
        "additional_notes": "Тестовый запрос для проверки AI"
    }
    
    try:
        ai_client = AIClient()
        result = await ai_client.analyze_project(test_data)
        
        response = f"""
✅ AI АНАЛИЗ УСПЕШЕН!

📊 Результаты:
• Оценка: {result.get('realism_score')}/10
• Бюджет: {result.get('budget_adequacy')}
• Приоритет: {result.get('priority_level')}

💰 Цены: {result.get('price_recommendations', {}).get('recommended_price')}₽
⏱️ Время: {result.get('time_estimate_hours')}ч

📝 {result.get('summary', 'Анализ завершен')}
        """
        
        await message.answer(response)
        
    except Exception as e:
        await message.answer(f"❌ Ошибка AI: {e}")