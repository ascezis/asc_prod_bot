# 📋 SQL скрипты

## Доступные скрипты

- **[create_users_table.sql](./create_users_table.sql)** - Создание таблицы users вручную

## Использование

### Создание таблицы users вручную

Если у пользователя БД нет прав на автоматическое создание таблиц:

```bash
psql -U postgres -d video_editor_bot -f sql/create_users_table.sql
```

Или выполните SQL вручную через pgAdmin или psql.

---

**Примечание:** Обычно таблицы создаются автоматически при запуске backend через `init_db()`.

