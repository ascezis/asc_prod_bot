import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.bot.keyboards.qualification import (
    get_services_keyboard, 
    get_deadline_keyboard,
    get_budget_keyboard,
    get_cancel_keyboard
)
from app.bot.states import ProjectStates
from app.services.validation import (
    validate_duration, format_duration_hint,
    smart_duration_processing, quick_validate_source_links
)

router = Router()
logger = logging.getLogger(__name__)

# Обработчик отмены
@router.message(F.text == "❌ Отмена")
async def cancel_handler(message: Message, state: FSMContext):
    """Обработчик отмены в любой момент диалога"""
    current_state = await state.get_state()
    
    if current_state is None:
        await message.answer(
            "Нечего отменять. Если хотите оставить заявку - напишите /start",
            reply_markup=get_cancel_keyboard()
        )
        return

    await state.clear()
    await message.answer(
        "❌ Диалог прерван. Все данные удалены.\n\n"
        "Если хотите оставить заявку - напишите /start",
        reply_markup=None
    )

@router.message(ProjectStates.waiting_for_project_type)
async def process_project_type(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_handler(message, state)
        return
        
    await state.update_data(project_type=message.text)
    
    # Получаем подсказку по формату
    duration_hint = await format_duration_hint()
    
    await message.answer(
        f"2. Примерная длительность исходного материала:\n\n{duration_hint}",
        reply_markup=get_cancel_keyboard(),
        parse_mode="Markdown"
    )
    await state.set_state(ProjectStates.waiting_for_duration_raw)

@router.message(ProjectStates.waiting_for_duration_raw)
async def process_duration_raw(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_handler(message, state)
        return
    
    # 🔥 ЛОЯЛЬНАЯ ВАЛИДАЦИЯ - ПРИНИМАЕМ ЛЮБОЙ ВВОД С ЦИФРАМИ
    is_valid, normalized, suggestion = await validate_duration(message.text)
    
    if not is_valid:
        # Показываем подсказку, но не блокируем надолго
        duration_hint = await format_duration_hint()
        await message.answer(
            f"{suggestion}\n\n{duration_hint}",
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    # Сохраняем нормализованный текст
    await state.update_data(duration_raw=normalized)
    
    await message.answer(
        "⏱️ *Длительность готового видео:*\n\n"
        "Пример: 10-15 минут для YouTube или 45-60 минут для подкаста",
        reply_markup=get_cancel_keyboard(),
        parse_mode="Markdown"
    )
    await state.set_state(ProjectStates.waiting_for_duration_final)

@router.message(ProjectStates.waiting_for_duration_final)
async def process_duration_final(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_handler(message, state)
        return
    
    # 🔥 ЛОЯЛЬНАЯ ВАЛИДАЦИЯ ДЛЯ ФИНАЛЬНОЙ ДЛИТЕЛЬНОСТИ
    is_valid, normalized, suggestion = await validate_duration(message.text)
    
    if not is_valid:
        await message.answer(
            "📏 Укажите длительность в минутах (например: 15-20 минут)",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    await state.update_data(duration_final=normalized)
    await message.answer(
        "3. Какие услуги нужны:",
        reply_markup=get_services_keyboard()
    )

@router.callback_query(F.data.startswith("service_"))
async def process_service_selection(callback: CallbackQuery, state: FSMContext):
    service_name = callback.data.replace("service_", "")
    data = await state.get_data()
    services = data.get("services", [])
    
    if service_name in services:
        services.remove(service_name)
    else:
        services.append(service_name)
    
    await state.update_data(services=services)
    
    # Обновляем клавиатуру (только если нужно)
    from app.bot.keyboards.qualification import get_services_keyboard
    try:
        await callback.message.edit_reply_markup(
            reply_markup=get_services_keyboard()
        )
    except Exception as e:
        # Игнорируем ошибку "message is not modified" - это нормально
        if "message is not modified" not in str(e).lower():
            logger.warning(f"Ошибка обновления клавиатуры: {e}")
    await callback.answer()

@router.callback_query(F.data == "services_done")
async def process_services_done(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("services"):
        await callback.answer("Выберите хотя бы одну услугу!", show_alert=True)
        return
    
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "4. Желаемый срок сдачи:",
        reply_markup=get_deadline_keyboard()
    )
    await state.set_state(ProjectStates.waiting_for_deadline)

@router.message(ProjectStates.waiting_for_deadline)
async def process_deadline(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_handler(message, state)
        return
        
    await state.update_data(deadline=message.text)
    await message.answer(
        "5. Бюджет:",
        reply_markup=get_budget_keyboard()
    )
    await state.set_state(ProjectStates.waiting_for_budget)

@router.message(ProjectStates.waiting_for_budget)
async def process_budget(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_handler(message, state)
        return
    
    # 🔥 AI ПОДСКАЗКА ПО БЮДЖЕТУ
    data = await state.get_data()
    if message.text == "до 10К" and "Графика/моушн" in data.get('services', []):
        await message.answer("💡 AI рекомендует: для сложной графики бюджет 10-20К будет оптимальнее")
    
    if message.text == "до 10К":
        await message.answer("💡 Для проектов до 10К предлагаю базовый монтаж без сложной графики")
    
    await state.update_data(budget=message.text)
    
    # Переходим к технической информации
    await message.answer(
        "6. Ссылка на исходные материалы:\n"
        "Google Drive / Yandex Disk / etc\n"
        "(или напишите 'пропустить')",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(ProjectStates.waiting_for_source_links)

@router.message(ProjectStates.waiting_for_source_links)
async def process_source_links(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_handler(message, state)
        return
    
    if message.text.lower() == 'пропустить':
        await state.update_data(source_links="Пропущено")
    else:
        # 🔥 ЛОЯЛЬНАЯ ПРОВЕРКА ССЫЛОК - ВСЕГДА ПРИНИМАЕМ
        is_valid, validation_msg, valid_urls = await quick_validate_source_links(message.text)
        
        await state.update_data(source_links=message.text)
        
        # Показываем результат проверки, но не блокируем
        if validation_msg and "⚠️" in validation_msg:
            await message.answer(validation_msg)
    
    await message.answer(
        "7. Пример стиля (опционально):\n"
        "Ссылка на YouTube-видео с понравившимся стилем\n"
        "(или напишите 'пропустить')",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(ProjectStates.waiting_for_style_examples)