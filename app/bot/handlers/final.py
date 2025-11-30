from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.bot.states import ProjectStates
from app.services.notification import notify_admin
from app.services.ai_client import AIClient
from app.database.connection import AsyncSessionLocal
from app.database.models import Client, Project, AIAnalysis

router = Router()
logger = logging.getLogger(__name__)

async def perform_ai_analysis(project_data: dict) -> dict:
    """Выполняет AI анализ заявки"""
    try:
        ai_client = AIClient()
        analysis = await ai_client.analyze_project(project_data)
        logger.info(f"✅ AI анализ выполнен. Оценка: {analysis.get('realism_score')}/10")
        return analysis
    except Exception as e:
        logger.error(f"❌ Ошибка AI анализа: {e}")
        return {"error": str(e), "fallback": True}

async def notify_admin_with_ai(project_data: dict, user_data, ai_analysis: dict, project_id: int = None):
    """Отправляет уведомление с AI анализом"""
    project_data["ai_analysis"] = ai_analysis
    await notify_admin(project_data, user_data, project_id)

async def save_to_db(user, project_data, ai_analysis):
    """Сохраняет клиента, проект и AI анализ в БД. Возвращает project_id"""
    async with AsyncSessionLocal() as session:
        # Сначала проверяем, есть ли клиент
        result = await session.execute(select(Client).where(Client.telegram_id == user.id))
        client = result.scalars().first()

        if not client:
            client = Client(
                telegram_id=user.id,
                username=user.username,
                full_name=user.full_name
            )
            session.add(client)
            await session.flush()  # Чтобы получить client.id

        # Создаём проект
        project = Project(
            client_id=client.id,
            project_type=project_data.get("project_type"),
            duration_raw=project_data.get("duration_raw"),
            duration_final=project_data.get("duration_final"),
            services=project_data.get("services"),
            deadline=project_data.get("deadline"),
            budget=project_data.get("budget"),
            source_links=project_data.get("source_links"),
            style_examples=project_data.get("style_examples"),
            additional_notes=project_data.get("additional_notes"),
            status="new"
        )
        session.add(project)
        await session.flush()  # Чтобы получить project.id

        # Сохраняем AI анализ, если есть
        if ai_analysis and not ai_analysis.get("fallback"):
            analysis = AIAnalysis(
                project_id=project.id,
                realism_score=ai_analysis.get("realism_score"),
                recommended_price=ai_analysis.get("price_recommendations", {}).get("recommended_price"),
                time_estimate=ai_analysis.get("time_estimate_hours"),
                risks_detected=ai_analysis.get("identified_risks"),
                used_model=ai_analysis.get("used_model")
            )
            session.add(analysis)

        await session.commit()
        logger.info(f"💾 Данные успешно сохранены в БД (Project ID: {project.id})")
        return project.id

@router.message(ProjectStates.waiting_for_additional_notes)
async def process_additional_notes(message: Message, state: FSMContext):
    logger.info("🔄 Начало обработки финального шага")

    if message.text.lower() != 'нет':
        await state.update_data(additional_notes=message.text)
        logger.info(f"📝 Добавлены пожелания: {message.text}")

    data = await state.get_data()
    logger.info(f"📊 Данные из состояния: {data}")

    await message.answer(
        "✅ Спасибо! Вся информация передана. Свяжусь с вами в течение 6 часов для уточнения деталей."
    )
    logger.info("✅ Клиенту отправлено подтверждение")

    try:
        # AI АНАЛИЗ ЗАЯВКИ
        logger.info("🤖 Запуск AI анализа...")
        ai_analysis = await perform_ai_analysis(data)
        await state.update_data(ai_analysis=ai_analysis)
        logger.info("✅ AI анализ завершен")

        # Сохраняем всё в БД и получаем project_id
        project_id = await save_to_db(message.from_user, data, ai_analysis)

        # Отправляем уведомление администратору с project_id
        project_data_with_id = data.copy()
        await notify_admin_with_ai(project_data_with_id, message.from_user, ai_analysis, project_id)
        logger.info(f"✅ Администратор уведомлен с AI анализом (Project ID: {project_id})")

    except Exception as e:
        logger.error(f"❌ Ошибка при AI анализе/уведомлении: {e}")
        import traceback
        logger.error(f"Детали: {traceback.format_exc()}")
        
        # Пытаемся сохранить в БД даже при ошибке AI
        try:
            project_id = await save_to_db(message.from_user, data, None)
            await notify_admin(data, message.from_user, project_id)
        except Exception as db_error:
            logger.error(f"❌ Ошибка сохранения в БД: {db_error}")
            await notify_admin(data, message.from_user)
        
        logger.info("✅ Администратор уведомлен (без AI анализа)")

    await state.clear()
    logger.info("🗑️ Состояние очищено")
