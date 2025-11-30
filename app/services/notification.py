# app/services/notification.py
import logging
from aiogram import Bot
from app.config import config

logger = logging.getLogger(__name__)

async def notify_admin(project_data: dict, user_data, project_id=None):
    """Уведомление администратора о новой заявке"""
    try:
        bot = Bot(token=config.bot.token)
        
        project_id_text = f" (ID: {project_id})" if project_id else ""
        ai_analysis = project_data.get('ai_analysis', {})
        
        # Основная информация о заявке
        message_text = f"""
🎬 <b>НОВАЯ ЗАЯВКА НА ВИДЕОМОНТАЖ</b>{project_id_text}

👤 <b>Клиент:</b> {user_data.full_name} (@{user_data.username})
📋 <b>Тип проекта:</b> {project_data.get('project_type', 'Не указано')}

⏱️ <b>ДЛИТЕЛЬНОСТЬ:</b>
• Исходный материал: {project_data.get('duration_raw', 'Не указано')}
• Готовое видео: {project_data.get('duration_final', 'Не указано')}

🛠️ <b>УСЛУГИ:</b> {', '.join(project_data.get('services', []))}
📅 <b>Срок:</b> {project_data.get('deadline', 'Не указано')}
💰 <b>Бюджет:</b> {project_data.get('budget', 'Не указано')}
        """.strip()
        
        # Добавляем AI анализ если есть
        if ai_analysis and not ai_analysis.get('fallback'):
            message_text += f"""

🤖 <b>AI АНАЛИЗ:</b>

📊 <b>Оценка реалистичности:</b> {ai_analysis.get('realism_score', '?')}/10
🎯 <b>Приоритет:</b> {ai_analysis.get('priority_level', 'средний').upper()}
⚠️ <b>Риски:</b> {', '.join(ai_analysis.get('identified_risks', ['не выявлены']))}

💡 <b>Рекомендации по стоимости:</b>
• Мин: {ai_analysis.get('price_recommendations', {}).get('min_price', '?')}₽
• Реком: {ai_analysis.get('price_recommendations', {}).get('recommended_price', '?')}₽  
• Макс: {ai_analysis.get('price_recommendations', {}).get('max_price', '?')}₽

🕐 <b>Оценка времени:</b> ~{ai_analysis.get('time_estimate_hours', '?')}ч
➕ <b>Доп. услуги:</b> {', '.join(ai_analysis.get('service_recommendations', ['нет']))}

📝 <b>Резюме:</b> {ai_analysis.get('summary', 'Анализ не выполнен')}
            """
        elif ai_analysis and ai_analysis.get('fallback'):
            message_text += f"\n\n🤖 <b>AI анализ:</b> временно недоступен"
        
        # Дополнительная информация
        message_text += f"""

🔗 <b>Исходники:</b> {project_data.get('source_links', 'Не указано')}
🎨 <b>Пример стиля:</b> {project_data.get('style_examples', 'Не указано')}
📝 <b>Пожелания:</b> {project_data.get('additional_notes', 'Не указано')}
        """
        
        # Проверяем, что admin_id установлен
        if not config.bot.admin_id or config.bot.admin_id == 0:
            logger.error("❌ BOT_ADMIN_ID не установлен! Установите его в .env или app/config.py")
            return
        
        try:
            await bot.send_message(
                chat_id=config.bot.admin_id,
                text=message_text,
                parse_mode="HTML"
            )
            logger.info(f"✅ Администратор (ID: {config.bot.admin_id}) уведомлен с AI анализом")
        except Exception as send_error:
            error_msg = str(send_error)
            if "chat not found" in error_msg.lower():
                logger.error(f"❌ Чат с администратором не найден! Админ (ID: {config.bot.admin_id}) должен сначала написать боту /start")
                logger.error(f"💡 Решение: Попросите администратора написать боту @SuperGenius22299Bot команду /start")
            else:
                raise send_error
        finally:
            await bot.session.close()
        
    except Exception as e:
        logger.error(f"❌ Ошибка уведомления администратору (ID: {config.bot.admin_id}): {e}")
        import traceback
        logger.error(f"Детали ошибки: {traceback.format_exc()}")