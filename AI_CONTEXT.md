# AI Context - ASC Prod Bot

Полное описание проекта для AI-ассистентов. Этот файл содержит всю необходимую информацию о структуре, архитектуре и реализации проекта.

---

## 📋 ОБЩЕЕ ОПИСАНИЕ

**ASC Prod Bot** - комплексная система для приема заявок на видеомонтаж через Telegram-бота с админ-панелью и AI-анализом заявок.

**Основные функции:**
- Прием заявок от клиентов через Telegram-бота
- AI-анализ заявок через OpenRouter API
- Админ-панель для управления клиентами и проектами
- Автоматические уведомления администратору
- Статистика и аналитика

---

## 🏗️ АРХИТЕКТУРА

Проект состоит из **трех независимых компонентов**:

### 1. Telegram Bot (`app/`)
- **Технология:** aiogram 3.10.0
- **Язык:** Python 3.10+
- **Функции:** 
  - Прием заявок через диалог с клиентом
  - FSM (Finite State Machine) для управления диалогом
  - AI-анализ заявок
  - Сохранение данных в БД
  - Уведомления администратору

### 2. Admin Backend (`admin/backend/`)
- **Технология:** FastAPI + Uvicorn
- **Язык:** Python 3.10+
- **Порт:** 8000
- **Функции:**
  - REST API для админ-панели
  - CRUD операции для клиентов и проектов
  - Статистика
  - Автоматическая инициализация БД при старте

### 3. Admin Frontend (`admin/frontend/`)
- **Технология:** React 18.3.1 + Vite 6.4.1 + Chakra UI
- **Порт:** 5173
- **Функции:**
  - Dashboard со статистикой
  - Управление клиентами
  - Управление проектами
  - Фильтрация и поиск

---

## 📁 СТРУКТУРА ПРОЕКТА

```
asc_prod_bot/
├── app/                          # Telegram бот
│   ├── bot/
│   │   ├── handlers/             # Обработчики сообщений
│   │   │   ├── start.py          # /start, /analyze, /testai
│   │   │   ├── qualification.py  # Квалификация проекта (тип, длительность, услуги, дедлайн, бюджет)
│   │   │   ├── technical.py      # Техническая информация (исходники, примеры стиля)
│   │   │   └── final.py          # Финальный шаг (пожелания) + сохранение в БД + AI анализ + уведомления
│   │   ├── keyboards/
│   │   │   └── qualification.py  # Inline-клавиатуры для выбора опций
│   │   └── states.py             # FSM состояния диалога
│   ├── database/
│   │   ├── models.py             # SQLAlchemy модели (Client, Project, AIAnalysis)
│   │   └── connection.py         # Подключение к PostgreSQL + инициализация БД
│   ├── services/
│   │   ├── ai_client.py          # Клиент для OpenRouter API (AI анализ)
│   │   ├── notification.py       # Уведомления администратору
│   │   └── validation.py         # Валидация данных от пользователя
│   ├── config.py                 # Конфигурация (токены, БД, AI)
│   └── main.py                   # Точка входа бота
│
├── admin/
│   ├── backend/                   # FastAPI backend
│   │   ├── routers/
│   │   │   ├── clients.py        # CRUD для клиентов
│   │   │   ├── projects.py       # CRUD для проектов
│   │   │   └── statistics.py     # Статистика
│   │   ├── crud.py                # Вспомогательные CRUD функции
│   │   └── main.py               # FastAPI приложение + CORS + инициализация БД
│   └── frontend/                  # React админ-панель
│       └── src/
│           ├── api/              # API клиенты (axios)
│           ├── pages/             # Страницы (Dashboard, Clients, Projects)
│           └── components/        # Компоненты (Sidebar, Navbar)
│
├── run.py                         # Менеджер процессов (запуск всех компонентов)
└── requirements.txt               # Python зависимости
```

---

## 🗄️ БАЗА ДАННЫХ

**СУБД:** PostgreSQL 14+

**Подключение:** Асинхронное через `asyncpg` + SQLAlchemy 2.0

### Модели (app/database/models.py)

#### 1. Client
```python
- id: Integer (PK)
- telegram_id: BigInteger (unique, indexed) - Telegram user ID
- username: String(100) - Telegram username
- full_name: String(200) - Полное имя
- created_at: DateTime(timezone=True)
```

#### 2. Project
```python
- id: Integer (PK)
- client_id: Integer (FK -> clients.id)
- project_type: String(50) - Тип проекта
- duration_raw: String(50) - Исходный материал
- duration_final: String(50) - Готовое видео
- services: ARRAY(String) - Массив услуг
- deadline: String(50) - Срок сдачи
- budget: String(50) - Бюджет
- source_links: Text - Ссылки на исходники
- style_examples: Text - Примеры стиля
- additional_notes: Text - Дополнительные пожелания
- status: String(20) - new, in_progress, completed, rejected
- created_at: DateTime(timezone=True)
- updated_at: DateTime(timezone=True)
```

#### 3. AIAnalysis
```python
- id: Integer (PK)
- project_id: Integer (FK -> projects.id)
- realism_score: Integer - Оценка реалистичности (1-10)
- recommended_price: Integer - Рекомендуемая цена
- time_estimate: Integer - Оценка времени в часах
- risks_detected: ARRAY(String) - Массив выявленных рисков
- used_model: String - Использованная AI модель
- created_at: DateTime(timezone=True)
```

**Важно:** При удалении проекта сначала удаляются все связанные AI анализы (каскадное удаление в коде).

---

## 🤖 TELEGRAM BOT

### FSM Состояния (app/bot/states.py)

Диалог проходит через следующие состояния:
1. `waiting_for_project_type` - Выбор типа проекта
2. `waiting_for_duration_raw` - Длительность исходного материала
3. `waiting_for_duration_final` - Длительность готового видео
4. `waiting_for_services` - Выбор услуг (можно несколько)
5. `waiting_for_deadline` - Срок сдачи
6. `waiting_for_budget` - Бюджет
7. `waiting_for_source_links` - Ссылки на исходники (можно пропустить)
8. `waiting_for_style_examples` - Примеры стиля (можно пропустить)
9. `waiting_for_additional_notes` - Дополнительные пожелания (можно "нет")

### Обработчики (app/bot/handlers/)

#### start.py
- `/start` - Начало диалога, приветствие, переход к выбору типа проекта
- `/analyze` - AI анализ текущей заявки (если есть активное состояние)
- `/testai` - Тест AI анализа с тестовыми данными

#### qualification.py
- Обработка выбора типа проекта (callback или текст)
- Обработка длительности (валидация через `validation.py`)
- Обработка выбора услуг (множественный выбор через inline-кнопки)
- Обработка дедлайна (выбор из вариантов)
- Обработка бюджета (выбор из вариантов)
- Обработка отмены (`❌ Отмена`) - очистка состояния

#### technical.py
- Обработка ссылок на исходники (валидация URL)
- Обработка примеров стиля
- Возможность пропустить шаги

#### final.py
- Обработка дополнительных пожеланий
- **Критический момент:** После финального шага:
  1. Выполняется AI анализ заявки
  2. Сохраняется клиент в БД (если не существует)
  3. Сохраняется проект в БД
  4. Сохраняется AI анализ в БД (если успешен)
  5. Отправляется уведомление администратору с полной информацией
  6. Очищается FSM состояние

### Клавиатуры (app/bot/keyboards/qualification.py)

Используются inline-клавиатуры для выбора:
- Тип проекта: "Лонгрид для YouTube", "Подкаст/интервью", "Риелс/Shorts", "Образовательный контент"
- Услуги: "Монтаж", "Обработка звука", "Графика/моушн", "Создание клипов из материала"
- Дедлайн: "Срочно (3-5 дней) +30%", "Стандартно (7-10 дней)", "Не срочно (14+ дней)"
- Бюджет: "10-20К", "20-30К", "30-50К", "50К+", "Обсудим после ТЗ"

---

## 🔌 API ENDPOINTS

**Base URL:** `http://localhost:8000`

### Clients (`/clients`)

- `GET /clients/` - Список клиентов
  - Параметры: `search`, `telegram_id`, `limit`, `offset`
  - Возвращает: `List[ClientResponse]` с полем `projects_count`
  
- `GET /clients/{client_id}` - Получить клиента по ID
  
- `POST /clients/` - Создать клиента
  - Body: `ClientCreate` (telegram_id, username, full_name)
  
- `PUT /clients/{client_id}` - Обновить клиента
  - Body: `ClientUpdate` (все поля опциональны)
  
- `DELETE /clients/{client_id}` - Удалить клиента
  - **Ограничение:** Нельзя удалить клиента с проектами

### Projects (`/projects`)

- `GET /projects/` - Список проектов
  - Параметры: `client_id`, `status`, `search`, `limit`, `offset`
  - Возвращает: `List[ProjectResponse]` с полем `client_name`
  
- `GET /projects/{project_id}` - Получить проект по ID
  
- `POST /projects/` - Создать проект
  - Body: `ProjectCreate`
  
- `PUT /projects/{project_id}` - Обновить проект
  - Body: `ProjectUpdate` (все поля опциональны)
  
- `DELETE /projects/{project_id}` - Удалить проект
  - **Важно:** Автоматически удаляет связанные AI анализы перед удалением проекта

### Statistics (`/statistics`)

- `GET /statistics/` - Получить статистику
  - Возвращает:
    - `total_clients` - Общее количество клиентов
    - `total_projects` - Общее количество проектов
    - `projects_by_status` - Проекты по статусам (dict)
    - `projects_by_type` - Проекты по типам (dict)
    - `recent_projects_count` - Проекты за последние 7 дней
    - `total_ai_analyses` - Общее количество AI анализов
    - `average_realism_score` - Средний балл реалистичности
    - `top_clients` - Топ-10 клиентов по количеству проектов

---

## 🤖 AI АНАЛИЗ

### Сервис (app/services/ai_client.py)

**API:** OpenRouter API (`https://openrouter.ai/api/v1/chat/completions`)

**Модели (в порядке приоритета):**
1. `anthropic/claude-3.5-sonnet:free` - Основная
2. `google/gemini-2.0-flash-exp:free` - Резервная
3. `x-ai/grok-4.1-fast:free` - Резервная
4. `meta-llama/llama-3.3-70b-instruct:free` - Финальная резервная

**Логика:** Пробует модели по порядку, если одна не работает - переходит к следующей. Если все не работают - возвращает fallback анализ.

**Формат ответа AI:**
```json
{
  "realism_score": 6,  // 1-10
  "budget_adequacy": "низкий/средний/высокий",
  "price_recommendations": {
    "min_price": 5000,
    "recommended_price": 25000,
    "max_price": 40000
  },
  "identified_risks": ["риск1", "риск2"],
  "service_recommendations": ["услуга1", "услуга2"],
  "time_estimate_hours": 40,
  "priority_level": "низкий/средний/высокий",
  "summary": "Краткое резюме"
}
```

**Fallback анализ:** Если AI не работает, возвращается анализ с базовыми значениями (realism_score=5, recommended_price=15000, и т.д.)

---

## 🔔 УВЕДОМЛЕНИЯ

### Сервис (app/services/notification.py)

**Функция:** `notify_admin(project_data, user_data, project_id=None)`

**Логика:**
1. Создает сообщение с полной информацией о заявке
2. Добавляет AI анализ (если есть и не fallback)
3. Отправляет сообщение администратору (ID из `config.bot.admin_id`)
4. **Важно:** Администратор должен сначала написать боту `/start`, иначе будет ошибка "chat not found"

**Формат уведомления:**
- Основная информация о заявке
- AI анализ (если доступен)
- Ссылки на исходники, примеры стиля, пожелания

---

## ⚙️ КОНФИГУРАЦИЯ

### Файл: `app/config.py`

**Структура:**
```python
@dataclass
class BotConfig:
    token: str  # BOT_TOKEN из .env
    admin_id: int  # BOT_ADMIN_ID из .env (по умолчанию: 7229606042)

@dataclass
class DatabaseConfig:
    user: str  # DB_USER (по умолчанию: "video_user")
    password: str  # DB_PASSWORD (по умолчанию: "ascezis_pass")
    host: str  # DB_HOST (по умолчанию: "localhost")
    port: str  # DB_PORT (по умолчанию: "5432")
    name: str  # DB_NAME (по умолчанию: "video_editor_bot")

@dataclass
class AIConfig:
    api_key: str  # OPENROUTER_API_KEY из .env
    base_url: str  # OPENROUTER_BASE_URL

@dataclass
class Config:
    bot: BotConfig = field(default_factory=BotConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    ai: AIConfig = field(default_factory=AIConfig)
```

**Важно:** Используется `field(default_factory=...)` для dataclass, так как изменяемые объекты нельзя использовать как значения по умолчанию.

**Переменные окружения (.env):**
- `BOT_TOKEN` - Токен Telegram бота
- `BOT_ADMIN_ID` - Telegram ID администратора (7229606042)
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` - Настройки БД
- `OPENROUTER_API_KEY` - Ключ для AI анализа

---

## 🚀 ЗАПУСК ПРОЕКТА

### Менеджер процессов (run.py)

Запускает три компонента одновременно:
1. **Backend** - `uvicorn admin.backend.main:app --reload --port 8000`
2. **Frontend** - `npm run dev` (в `admin/frontend/`)
3. **Bot** - `python -m app.main`

**Команда запуска:** `python run.py`

### Инициализация БД

БД инициализируется автоматически при старте backend через `@app.on_event("startup")` в `admin/backend/main.py`.

---

## 🔧 ВАЖНЫЕ ДЕТАЛИ РЕАЛИЗАЦИИ

### 1. Удаление проектов
При удалении проекта сначала удаляются все связанные AI анализы, затем сам проект (избегает нарушения внешнего ключа).

### 2. Создание клиентов
При сохранении заявки проверяется существование клиента по `telegram_id`. Если не существует - создается новый.

### 3. Обработка ошибок AI
Если AI анализ не работает, заявка все равно сохраняется в БД, но без AI анализа. Администратор получает уведомление без AI анализа.

### 4. Кодировка в Windows
В Windows консоли не используются эмодзи в print-выводах (используется `[OK]`, `[ERROR]` вместо ✅, ⚠️).

### 5. CORS
Backend разрешает запросы с фронтенда на портах 5173, 5174, 3000.

### 6. Порт Backend
Backend всегда запускается на порту **8000** (не 8001!).

### 7. FSM Storage
Используется `MemoryStorage` вместо Redis (для простоты).

### 8. Валидация данных
Валидация длительности и URL выполняется через `app/services/validation.py`.

---

## 📊 СТАТУСЫ ПРОЕКТОВ

- `new` - Новая заявка (по умолчанию)
- `in_progress` - В работе
- `completed` - Завершен
- `rejected` - Отклонен

---

## 🔗 ЗАВИСИМОСТИ

### Python (requirements.txt)
- `aiogram==3.10.0` - Telegram Bot Framework
- `sqlalchemy==2.0.23` - ORM
- `asyncpg==0.29.0` - Асинхронный PostgreSQL драйвер
- `fastapi` - REST API
- `uvicorn[standard]` - ASGI сервер
- `aiohttp==3.9.1` - Асинхронный HTTP клиент
- `python-dotenv==1.0.0` - Загрузка .env

### Frontend (admin/frontend/package.json)
- `react@^18.3.1`
- `@chakra-ui/react@^2.10.9`
- `axios@^1.13.2`
- `framer-motion@^12.23.24`
- `vite@^6.4.1`

---

## 🐛 ИЗВЕСТНЫЕ ПРОБЛЕМЫ И РЕШЕНИЯ

### 1. Ошибка "chat not found" при уведомлениях
**Причина:** Администратор не написал боту `/start`
**Решение:** Администратор должен сначала написать боту команду `/start`

### 2. Ошибка "message is not modified" при выборе услуг
**Причина:** Пользователь нажимает на уже выбранную услугу
**Решение:** Обработано через try-except, ошибка игнорируется

### 3. Ошибка кодировки в Windows
**Причина:** Windows консоль не поддерживает эмодзи
**Решение:** Используется обычный текст вместо эмодзи

### 4. Ошибка mutable default в dataclass
**Причина:** Использование объектов как значений по умолчанию
**Решение:** Используется `field(default_factory=...)`

---

## 📝 ФОРМАТЫ ДАННЫХ

### ProjectCreate/ProjectUpdate
```python
{
  "client_id": int,
  "project_type": str,
  "duration_raw": str,
  "duration_final": str,
  "services": List[str],
  "deadline": str,
  "budget": str,
  "source_links": Optional[str],
  "style_examples": Optional[str],
  "additional_notes": Optional[str],
  "status": Optional[str]  # "new" по умолчанию
}
```

### ClientCreate/ClientUpdate
```python
{
  "telegram_id": int,
  "username": Optional[str],
  "full_name": Optional[str]
}
```

---

## 🎯 ТОЧКИ ВХОДА

1. **Бот:** `app/main.py` - `asyncio.run(main())`
2. **Backend:** `admin/backend/main.py` - FastAPI app
3. **Frontend:** `admin/frontend/src/main.jsx` - React app
4. **Запуск всех:** `run.py` - ProcessManager

---

## 🔐 БЕЗОПАСНОСТЬ

- `app/config.py` в `.gitignore` (секретные данные)
- `.env` в `.gitignore`
- Токены и ключи загружаются из переменных окружения
- Нет аутентификации в API (для разработки)

---

## 📈 РАСШИРЕНИЕ ПРОЕКТА

### Добавление нового обработчика бота:
1. Создать файл в `app/bot/handlers/`
2. Создать Router
3. Зарегистрировать в `app/main.py`

### Добавление нового API endpoint:
1. Создать роутер в `admin/backend/routers/`
2. Подключить в `admin/backend/main.py`

### Добавление нового поля в модель:
1. Изменить модель в `app/database/models.py`
2. Обновить Pydantic схемы в роутерах
3. БД обновится автоматически при следующем запуске

---

## ✅ ТЕКУЩИЙ СТАТУС

**Все компоненты работают:**
- ✅ Telegram бот принимает заявки
- ✅ AI анализ работает (с fallback)
- ✅ Данные сохраняются в БД
- ✅ Уведомления отправляются администратору
- ✅ API работает на порту 8000
- ✅ Frontend загружает данные из API
- ✅ Удаление проектов работает корректно

---

**Последнее обновление:** 2025-11-30
**Версия:** 1.0.0

