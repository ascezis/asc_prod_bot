import aiohttp
import json
import logging
from app.config import config

logger = logging.getLogger(__name__)

class AIClient:
    def __init__(self):
        self.api_key = config.ai.api_key
        self.base_url = config.ai.base_url
        # 🔥 ИСПОЛЬЗУЕМ Claude 3.5 - САМУЮ НАДЕЖНУЮ БЕСПЛАТНУЮ МОДЕЛЬ
        self.default_model = "anthropic/claude-3.5-sonnet:free"
    
    async def analyze_project(self, project_data: dict) -> dict:
        """
        Анализирует заявку через AI
        Пробуем модели от самой надежной к менее надежным
        """
        # 🎯 ОБНОВЛЕННЫЙ СПИСОК РАБОЧИХ МОДЕЛЕЙ
        models_to_try = [
            "anthropic/claude-3.5-sonnet:free",  # 👈 ОСНОВНАЯ - Claude 3.5
            "google/gemini-2.0-flash-exp:free",   # 👈 ВТОРАЯ - Gemini Flash
            "x-ai/grok-4.1-fast:free",           # 👈 ТРЕТЬЯ - Grok 4.1
            "meta-llama/llama-3.3-70b-instruct:free",  # 👈 РЕЗЕРВНАЯ - Llama 3.3
        ]
        
        for model in models_to_try:
            try:
                logger.info(f"🤖 Пробуем модель: {model}")
                prompt = self._build_analysis_prompt(project_data)
                response = await self._make_request(prompt, model)
                
                if response and "choices" in response:
                    content = response["choices"][0]["message"]["content"]
                    analysis = self._parse_ai_response(content)
                    analysis["used_model"] = model  # Добавляем информацию о модели
                    logger.info(f"✅ AI анализ успешен с моделью: {model}")
                    return analysis
                    
            except Exception as e:
                logger.warning(f"❌ Модель {model} не сработала: {e}")
                continue
        
        logger.error("❌ Все AI модели не сработали")
        return self._get_fallback_analysis()
    
    async def _make_request(self, prompt: str, model: str = None) -> dict:
        """Делает запрос к OpenRouter API"""
        if not self.api_key:
            logger.warning("OpenRouter API ключ не установлен")
            return None
        
        model = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ascezis/video-editor-bot",
            "X-Title": "Video Editor Bot"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system", 
                    "content": """Ты AI помощник профессионального видеомонтажера. 
                    Анализируй заявки клиентов и давай структурированные рекомендации.
                    Всегда возвращай валидный JSON. Отвечай на русском.
                    
                    КРИТИЧЕСКИ ВАЖНО: Твой ответ должен быть ТОЛЬКО в формате JSON, без каких-либо дополнительных текстов, объяснений или markdown разметки."""
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 2000,  # 👈 Увеличиваем для сложных ответов
            "temperature": 0.3
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.post(
                    self.base_url, 
                    headers=headers, 
                    json=payload
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"✅ AI запрос успешен. Модель: {model}")
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ API ошибка {response.status} для модели {model}: {error_text}")
                        return None
                        
        except Exception as e:
            logger.error(f"❌ Ошибка соединения с AI (модель {model}): {e}")
            return None
    
    def _build_analysis_prompt(self, project_data: dict) -> str:
        """Строит промпт для анализа заявки"""
        return f"""
        ПРОАнализируй заявку на видеомонтаж как опытный продюсер:

        ДАННЫЕ КЛИЕНТА:
        - Тип проекта: {project_data.get('project_type', 'Не указан')}
        - Бюджет: {project_data.get('budget', 'Не указан')}
        - Выбранные услуги: {', '.join(project_data.get('services', []))}
        - Срок сдачи: {project_data.get('deadline', 'Не указан')}
        - Длительность: {project_data.get('duration_raw', '?')} → {project_data.get('duration_final', '?')}
        - Исходники: {project_data.get('source_links', 'Не указаны')}
        - Пожелания: {project_data.get('additional_notes', 'Нет')}

        ПРОАнализируй по следующим критериям:

        1. ОЦЕНКА РЕАЛИСТИЧНОСТИ (1-10 баллов):
           - Соответствие бюджета и запрашиваемых услуг
           - Реалистичность сроков относительно сложности проекта
           - Ясность технического задания и наличие всей необходимой информации

        2. РЕКОМЕНДАЦИИ ПО СТОИМОСТИ (в рублях):
           - Минимальная разумная цена за базовый пакет
           - Рекомендуемая рыночная цена за качественную работу
           - Премиум цена за срочность или дополнительные услуги

        3. ОЦЕНКА РИСКОВ:
           - Потенциальные проблемы с исходными материалами
           - Риски несоблюдения сроков
           - Технические сложности проекта
           - Что требует дополнительного уточнения у клиента

        4. ДОПОЛНИТЕЛЬНЫЕ РЕКОМЕНДАЦИИ:
           - Какие услуги стоит добавить для улучшения результата
           - Как оптимизировать workflow для данного проекта
           - Советы по коммуникации с клиентом

        5. ОЦЕНКА ВРЕМЕНИ:
           - Реальное время на выполнение работы в часах

        ВНИМАНИЕ: Верни ответ ТОЛЬКО в валидном JSON формате без каких-либо дополнительных текстов, комментариев или объяснений.

        JSON СХЕМА:
        {{
            "realism_score": число от 1 до 10,
            "budget_adequacy": "низкий/средний/высокий",
            "price_recommendations": {{
                "min_price": число,
                "recommended_price": число, 
                "max_price": число
            }},
            "identified_risks": ["конкретный риск 1", "конкретный риск 2", "конкретный риск 3"],
            "service_recommendations": ["конкретная услуга 1", "конкретная услуга 2"],
            "time_estimate_hours": число,
            "priority_level": "низкий/средний/высокий",
            "summary": "краткое профессиональное резюме на 2-3 предложения"
        }}
        """
    
    def _parse_ai_response(self, content: str) -> dict:
        """Парсит ответ AI в структурированные данные"""
        try:
            # Интенсивная очистка ответа
            clean_content = content.strip()
            
            # Удаляем все возможные обертки кода
            wrappers = [
                ("```json", "```"),
                ("```", "```"), 
                ("```javascript", "```"),
                ("JSON:", ""),
                ("json:", ""),
            ]
            
            for start, end in wrappers:
                if clean_content.startswith(start):
                    clean_content = clean_content[len(start):]
                if clean_content.endswith(end):
                    clean_content = clean_content[:-len(end)] if end else clean_content
            
            clean_content = clean_content.strip()
            
            # Пробуем распарсить JSON
            analysis = json.loads(clean_content)
            
            # Валидация и нормализация полей
            required_fields = ["realism_score", "budget_adequacy", "price_recommendations"]
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = self._get_fallback_value(field)
            
            # Нормализация числовых полей
            if "realism_score" in analysis:
                analysis["realism_score"] = max(1, min(10, int(analysis["realism_score"])))
            
            if "time_estimate_hours" in analysis:
                analysis["time_estimate_hours"] = max(1, int(analysis["time_estimate_hours"]))
            
            # Нормализация цен
            price_rec = analysis.get("price_recommendations", {})
            for price_key in ["min_price", "recommended_price", "max_price"]:
                if price_key in price_rec:
                    price_rec[price_key] = max(1000, int(price_rec[price_key]))
            
            # Убедимся что массивы существуют
            if "identified_risks" not in analysis:
                analysis["identified_risks"] = []
            if "service_recommendations" not in analysis:
                analysis["service_recommendations"] = []
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Ошибка парсинга AI ответа: {e}")
            logger.error(f"📝 Исходный ответ: {content}")
            logger.error(f"🧹 Очищенный ответ: {clean_content}")
            return self._get_fallback_analysis()
        except Exception as e:
            logger.error(f"❌ Неожиданная ошибка при парсинге: {e}")
            return self._get_fallback_analysis()
    
    def _get_fallback_analysis(self) -> dict:
        """Возвращает fallback анализ если AI не сработал"""
        return {
            "realism_score": 5,
            "budget_adequacy": "средний",
            "price_recommendations": {
                "min_price": 5000,
                "recommended_price": 15000,
                "max_price": 25000
            },
            "identified_risks": ["Недостаточно данных для точного анализа"],
            "service_recommendations": [],
            "time_estimate_hours": 10,
            "priority_level": "средний",
            "summary": "AI анализ временно недоступен. Проверьте заявку вручную.",
            "fallback": True
        }
    
    def _get_fallback_value(self, field: str):
        """Возвращает значения по умолчанию для полей"""
        fallbacks = {
            "realism_score": 5,
            "budget_adequacy": "средний",
            "price_recommendations": {"min_price": 5000, "recommended_price": 15000, "max_price": 25000},
            "identified_risks": [],
            "service_recommendations": [],
            "time_estimate_hours": 8,
            "priority_level": "средний",
            "summary": "Анализ не выполнен"
        }
        return fallbacks.get(field, "")