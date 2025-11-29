from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.states import ProjectStates

router = Router()

@router.message(ProjectStates.waiting_for_source_links)
async def process_source_links(message: Message, state: FSMContext):
    await state.update_data(source_links=message.text)
    await message.answer(
        "7. Пример стиля (опционально):\\n"
        "Ссылка на YouTube-видео с понравившимся стилем\\n"
        "(или напишите 'пропустить')"
    )
    await state.set_state(ProjectStates.waiting_for_style_examples)

@router.message(ProjectStates.waiting_for_style_examples)
async def process_style_examples(message: Message, state: FSMContext):
    if message.text.lower() != 'пропустить':
        await state.update_data(style_examples=message.text)
    
    await message.answer(
        "8. Дополнительные пожелания:\\n"
        "Текстовая область для свободного ввода\\n"
        "(или напишите 'нет')"
    )
    await state.set_state(ProjectStates.waiting_for_additional_notes)

    