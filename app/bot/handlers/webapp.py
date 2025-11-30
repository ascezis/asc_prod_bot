"""
Обработчики для Telegram Web App
"""
from aiogram import Router, F
from aiogram.types import Message, WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import json
import logging

from app.bot.states import ProjectStates
from app.bot.handlers.final import save_to_db, notify_admin_with_ai, perform_ai_analysis
from app.database.connection import AsyncSessionLocal
from app.database.models import Client
from sqlalchemy.future import select

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("webapp"))
async def cmd_webapp(message: Message):
    """Открыть Web App"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    web_app_url = "https://overfemininely-subministrant-jenell.ngrok-free.dev/index.html"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="🚀 Открыть Web App",
            web_app={"url": web_app_url}
        )
    ]])
    
    await message.answer(
        "📱 Откройте Web App для работы с заявками:",
        reply_markup=keyboard
    )


@router.message(F.web_app_data)
async def handle_webapp_data(message: Message, state: FSMContext):
    """Обработка данных из Web App"""
    try:
        data = json.loads(message.web_app_data.data)
        action = data.get("action")
        
        if action == "create_project":
            # Создание заявки из Web App
            project_data = data.get("data", {})
            
            # Валидация
            required_fields = ["project_type", "duration_raw", "duration_final", "services", "deadline", "budget"]
            missing = [field for field in required_fields if not project_data.get(field)]
            
            if missing:
                await message.answer(f"❌ Заполните все обязательные поля: {', '.join(missing)}")
                return
            
            # Сохраняем данные в состояние (для совместимости с существующим кодом)
            await state.set_data(project_data)
            await state.set_state(ProjectStates.waiting_for_additional_notes)
            
            # Выполняем AI анализ и сохраняем в БД
            try:
                logger.info("🤖 Запуск AI анализа из Web App...")
                ai_analysis = await perform_ai_analysis(project_data)
                logger.info("✅ AI анализ завершен")
                
                # Сохраняем в БД
                project_id = await save_to_db(message.from_user, project_data, ai_analysis)
                logger.info(f"💾 Заявка сохранена (Project ID: {project_id})")
                
                # Уведомляем администратора
                await notify_admin_with_ai(project_data, message.from_user, ai_analysis, project_id)
                
                await message.answer(
                    f"✅ Заявка #{project_id} успешно создана!\n\n"
                    "Мы свяжемся с вами в ближайшее время.\n"
                    "Вы можете отслеживать статус заявки в Web App."
                )
                
            except Exception as e:
                logger.error(f"❌ Ошибка при обработке заявки: {e}")
                # Пытаемся сохранить без AI анализа
                try:
                    project_id = await save_to_db(message.from_user, project_data, None)
                    await message.answer(
                        f"✅ Заявка #{project_id} создана!\n"
                        "Мы свяжемся с вами в ближайшее время."
                    )
                except Exception as db_error:
                    logger.error(f"❌ Ошибка сохранения в БД: {db_error}")
                    await message.answer("❌ Ошибка при создании заявки. Попробуйте позже.")
            
            await state.clear()
            
        elif action == "get_token":
            # Запрос токена для API (опционально, если нужна авторизация)
            # Пока не используется, так как используем telegram_id напрямую
            await message.answer("Токен не требуется для Web App")
            
    except json.JSONDecodeError:
        await message.answer("❌ Ошибка обработки данных из Web App")
        logger.error("Ошибка парсинга JSON из Web App")
    except Exception as e:
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")
        logger.error(f"Ошибка обработки Web App данных: {e}")


@router.message(Command("myprojects"))
async def cmd_my_projects(message: Message):
    """Показать кнопку для открытия Web App с заявками"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    web_app_url = "https://overfemininely-subministrant-jenell.ngrok-free.dev/index.html"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="📊 Мои заявки",
            web_app={"url": web_app_url}
        )
    ]])
    
    await message.answer(
        "📊 Откройте Web App для просмотра ваших заявок:",
        reply_markup=keyboard
    )

