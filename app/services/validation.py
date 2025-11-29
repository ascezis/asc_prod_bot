import re
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

async def validate_duration(text: str) -> Tuple[bool, str, str]:
    """
    Умная валидация длительности
    Возвращает: (успех, нормализованный текст, подсказка)
    """
    text = text.strip()
    
    # 🔥 ПРИНИМАЕМ ПРАКТИЧЕСКИ ЛЮБОЙ ВВОД С ЦИФРАМИ
    if not any(char.isdigit() for char in text):
        return False, text, "❌ Укажите цифры (например: 2 часа или 120 минут)"
    
    # Автоматически нормализуем ввод
    normalized = await _normalize_duration(text)
    
    return True, normalized, ""

async def _normalize_duration(text: str) -> str:
    """Нормализует ввод длительности в читаемый формат"""
    text = text.lower().strip()
    
    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text)
    
    # Паттерны для распознавания
    patterns = {
        'hours_minutes': r'(\d+)\s*(?:час|часа|часов|ч)?\s*(\d+)\s*(?:минут|минуты|мин|м)?',
        'hours_only': r'(\d+)\s*(?:час|часа|часов|ч)',
        'minutes_only': r'(\d+)\s*(?:минут|минуты|мин|м)',
        'only_numbers_with_spaces': r'(\d+)\s+(\d+)',
        'only_numbers': r'^(\d+)$'
    }
    
    # Пробуем распознать паттерны
    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            if pattern_name == 'hours_minutes':
                hours, minutes = match.groups()
                return f"{hours} час {minutes} минут"
            elif pattern_name == 'hours_only':
                hours = match.group(1)
                return f"{hours} часов"
            elif pattern_name == 'minutes_only':
                minutes = match.group(1)
                return f"{minutes} минут"
            elif pattern_name == 'only_numbers_with_spaces':
                num1, num2 = match.groups()
                # Предполагаем что первое число - часы, второе - минуты
                if int(num1) < 24:  # Если число маленькое, вероятно это часы
                    return f"{num1} час {num2} минут"
                else:
                    return f"{num1} минут"
            elif pattern_name == 'only_numbers':
                number = match.group(1)
                num = int(number)
                if num < 10:  # Маленькие числа - вероятно часы
                    return f"{num} часов"
                elif num < 200:  # Средние числа - вероятно минуты
                    return f"{num} минут"
                else:  # Большие числа - вероятно минуты для длинных записей
                    hours = num // 60
                    minutes = num % 60
                    if hours > 0:
                        return f"{hours} час {minutes} минут"
                    else:
                        return f"{num} минут"
    
    # 🔥 ЕСЛИ НИЧЕГО НЕ РАСПОЗНАНО - ВОЗВРАЩАЕМ ОРИГИНАЛЬНЫЙ ТЕКСТ
    return text

async def validate_links(text: str) -> Tuple[bool, str, list]:
    """
    Проверяет и анализирует ссылки
    Возвращает: (успех, сообщение, список найденных ссылок)
    """
    text = text.strip()
    
    # Поиск URL в тексте
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    
    if not urls:
        # 🔥 НЕ БЛОКИРУЕМ если нет ссылок - просто предупреждаем
        return True, "⚠️ Ссылки не найдены, но продолжаем", []
    
    valid_domains = [
        'drive.google.com', 'yadi.sk', 'disk.yandex.ru',
        'dropbox.com', 'mega.nz', 'cloud.mail.ru',
        'youtube.com', 'youtu.be', 'vimeo.com'
    ]
    
    valid_urls = []
    
    for url in urls:
        try:
            # Упрощенная проверка - есть ли знакомые домены
            if any(domain in url.lower() for domain in valid_domains):
                valid_urls.append(url)
        except Exception:
            continue
    
    if valid_urls:
        return True, f"✅ Найдено корректных ссылок: {len(valid_urls)}", valid_urls
    else:
        # 🔥 ВСЕ РАВНО ПРОПУСКАЕМ, НО ПРЕДУПРЕЖДАЕМ
        return True, "⚠️ Ссылки на неподдерживаемые ресурсы", []

async def suggest_duration_format(current_text: str) -> str:
    """Предлагает правильный формат для длительности"""
    if not any(char.isdigit() for char in current_text):
        return "Например: 2 часа или 120 минут"
    
    return ""

async def quick_validate_source_links(text: str) -> bool:
    """
    Быстрая проверка ссылок без блокировки
    Всегда возвращает True - не блокируем пользователей
    """
    return True

# 🔥 НОВЫЕ ФУНКЦИИ ДЛЯ УМНОЙ ОБРАБОТКИ

async def smart_duration_processing(text: str) -> str:
    """
    Умная обработка длительности с подсказками
    """
    # Всегда принимаем ввод, но даем подсказки если нужно
    normalized = await _normalize_duration(text)
    
    # Логируем для отладки
    logger.info(f"📏 Обработана длительность: '{text}' -> '{normalized}'")
    
    return normalized

async def validate_budget(budget_text: str, project_type: str = "") -> Tuple[bool, str, str]:
    """
    Валидация бюджета - всегда принимаем любой ввод
    """
    budget_text = budget_text.strip()
    
    # 🔥 ВСЕГДА ПРИНИМАЕМ БЮДЖЕТ
    return True, budget_text, ""

async def validate_project_type(project_type: str) -> Tuple[bool, str]:
    """
    Валидация типа проекта - всегда принимаем
    """
    return True, "✅ Принято"

# 🔥 УТИЛИТЫ ДЛЯ ФОРМАТИРОВАНИЯ ПОДСКАЗОК

async def format_duration_hint() -> str:
    """Возвращает подсказку для формата длительности"""
    return """
📏 *Укажите длительность в удобном формате:*
• `2 часа` • `120 минут` • `1.5 часа`
• `2 30` • `90` • `3 часа 15 минут`

*Любой формат с цифрами будет принят!* ✅
"""

async def format_links_hint() -> str:
    """Возвращает подсказку для формата ссылок"""
    return """
📎 *Можете указать ссылки на:*
• Google Drive • Yandex Disk • Dropbox
• YouTube • Vimeo (для примеров)

*Или просто напишите "пропустить"* ⏭️
"""