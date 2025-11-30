# API Документация - ASC Prod Bot

## Базовый URL
```
http://localhost:8000
```

## Клиенты (`/clients`)

### GET `/clients/` - Список клиентов
**Параметры запроса:**
- `search` (string, optional) - Поиск по username или full_name
- `telegram_id` (int, optional) - Фильтр по telegram_id
- `limit` (int, default: 100) - Лимит записей (1-1000)
- `offset` (int, default: 0) - Смещение для пагинации

**Пример:**
```bash
GET /clients/?search=john&limit=50&offset=0
```

**Ответ:**
```json
[
  {
    "id": 1,
    "telegram_id": 123456789,
    "username": "john_doe",
    "full_name": "John Doe",
    "created_at": "2024-01-01T00:00:00",
    "projects_count": 5
  }
]
```

### GET `/clients/{client_id}` - Получить клиента по ID
**Ответ:**
```json
{
  "id": 1,
  "telegram_id": 123456789,
  "username": "john_doe",
  "full_name": "John Doe",
  "created_at": "2024-01-01T00:00:00",
  "projects_count": 5
}
```

### POST `/clients/` - Создать клиента
**Тело запроса:**
```json
{
  "telegram_id": 123456789,
  "username": "john_doe",
  "full_name": "John Doe"
}
```

### PUT `/clients/{client_id}` - Обновить клиента
**Тело запроса:**
```json
{
  "username": "john_updated",
  "full_name": "John Updated"
}
```

### DELETE `/clients/{client_id}` - Удалить клиента
**Примечание:** Нельзя удалить клиента, у которого есть проекты.

---

## Проекты (`/projects`)

### GET `/projects/` - Список проектов
**Параметры запроса:**
- `client_id` (int, optional) - Фильтр по ID клиента
- `status` (string, optional) - Фильтр по статусу (new, in_progress, completed, rejected)
- `search` (string, optional) - Поиск по project_type, budget, deadline, additional_notes
- `limit` (int, default: 100) - Лимит записей (1-1000)
- `offset` (int, default: 0) - Смещение для пагинации

**Пример:**
```bash
GET /projects/?status=new&search=лонгрид&limit=50
```

**Ответ:**
```json
[
  {
    "id": 1,
    "client_id": 1,
    "project_type": "Лонгрид для YouTube",
    "duration_raw": "2 часа",
    "duration_final": "10-12 минут",
    "services": ["Монтаж", "Обработка звука"],
    "deadline": "Стандартно (7-10 дней)",
    "budget": "20-30К",
    "source_links": "https://...",
    "style_examples": "https://...",
    "additional_notes": "Особые пожелания",
    "status": "new",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": null,
    "client_name": "John Doe"
  }
]
```

### GET `/projects/{project_id}` - Получить проект по ID
**Ответ:** Аналогично элементу из списка проектов

### POST `/projects/` - Создать проект
**Тело запроса:**
```json
{
  "client_id": 1,
  "project_type": "Лонгрид для YouTube",
  "duration_raw": "2 часа",
  "duration_final": "10-12 минут",
  "services": ["Монтаж", "Обработка звука"],
  "deadline": "Стандартно (7-10 дней)",
  "budget": "20-30К",
  "source_links": "https://...",
  "style_examples": "https://...",
  "additional_notes": "Особые пожелания",
  "status": "new"
}
```

### PUT `/projects/{project_id}` - Обновить проект
**Тело запроса:** Все поля опциональны
```json
{
  "status": "in_progress",
  "budget": "25-35К"
}
```

### DELETE `/projects/{project_id}` - Удалить проект
**Ответ:**
```json
{
  "detail": "Project deleted successfully"
}
```

---

## Статистика (`/statistics`)

### GET `/statistics/` - Получить статистику
**Ответ:**
```json
{
  "total_clients": 50,
  "total_projects": 120,
  "projects_by_status": {
    "new": 30,
    "in_progress": 15,
    "completed": 70,
    "rejected": 5
  },
  "projects_by_type": {
    "Лонгрид для YouTube": 80,
    "Подкаст/интервью": 30,
    "Образовательный контент": 10
  },
  "recent_projects_count": 12,
  "total_ai_analyses": 100,
  "average_realism_score": 7.5,
  "top_clients": [
    {
      "id": 1,
      "telegram_id": 123456789,
      "username": "john_doe",
      "full_name": "John Doe",
      "projects_count": 10
    }
  ]
}
```

---

## Коды ошибок

- `200` - Успешно
- `400` - Ошибка валидации или бизнес-логики
- `404` - Ресурс не найден
- `500` - Внутренняя ошибка сервера

## Примеры использования

### Поиск клиентов
```bash
curl "http://localhost:8000/clients/?search=john"
```

### Фильтрация проектов по статусу
```bash
curl "http://localhost:8000/projects/?status=new"
```

### Создание проекта
```bash
curl -X POST "http://localhost:8000/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 1,
    "project_type": "Лонгрид для YouTube",
    "duration_raw": "2 часа",
    "duration_final": "10-12 минут",
    "services": ["Монтаж"],
    "deadline": "Стандартно (7-10 дней)",
    "budget": "20-30К"
  }'
```

### Получение статистики
```bash
curl "http://localhost:8000/statistics/"
```

