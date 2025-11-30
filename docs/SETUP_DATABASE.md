# Настройка базы данных для системы уровней доступа

## Проблема

При попытке создать таблицу `users` возникает ошибка:
```
нет доступа к схеме public
```

Это означает, что пользователь БД не имеет прав на создание таблиц.

## Решение

### Вариант 1: Дать права пользователю БД (рекомендуется)

Подключитесь к PostgreSQL от имени администратора (например, `postgres`) и выполните:

```sql
-- Дать права на создание таблиц в схеме public
GRANT CREATE ON SCHEMA public TO video_user;

-- Или дать все права на схему public
GRANT ALL ON SCHEMA public TO video_user;

-- Дать права на использование схемы
GRANT USAGE ON SCHEMA public TO video_user;
```

### Вариант 2: Создать таблицу вручную

1. Подключитесь к PostgreSQL от имени администратора:
```bash
psql -U postgres -d video_editor_bot
```

2. Выполните SQL скрипт:
```bash
psql -U postgres -d video_editor_bot -f sql/create_users_table.sql
```

Или скопируйте содержимое `create_users_table.sql` и выполните в psql.

### Вариант 3: Использовать пользователя с правами администратора

Временно измените `app/config.py` или `.env`:
```python
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

Запустите backend, который автоматически создаст таблицу при старте.

## После создания таблицы

1. Запустите скрипт создания Owner:
```bash
python create_owner_simple.py
```

2. Или запустите backend - таблица будет создана автоматически при старте.

## Проверка

Проверьте, что таблица создана:
```sql
SELECT * FROM users;
```

Если таблица пустая, создайте первого пользователя через `create_owner_simple.py`.

