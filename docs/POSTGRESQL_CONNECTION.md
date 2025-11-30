# Подключение к PostgreSQL

## Способ 1: Через psql (командная строка)

### Подключение от имени администратора (postgres):
```bash
psql -U postgres -d video_editor_bot
```

### Подключение от имени пользователя приложения:
```bash
psql -U video_user -d video_editor_bot
```

При запросе введите пароль: `ascezis_pass`

---

## Способ 2: Через psql с указанием пароля в команде

```bash
psql -U postgres -d video_editor_bot -W
```

Или с переменной окружения:
```bash
set PGPASSWORD=ascezis_pass
psql -U video_user -d video_editor_bot
```

---

## Способ 3: Полная команда с хостом и портом

```bash
psql -h localhost -p 5432 -U postgres -d video_editor_bot
```

---

## Способ 4: Через pgAdmin (графический интерфейс)

1. Откройте pgAdmin
2. Создайте новое подключение:
   - Host: `localhost`
   - Port: `5432`
   - Database: `video_editor_bot`
   - Username: `postgres` (или `video_user`)
   - Password: ваш пароль

---

## Полезные команды после подключения

```sql
-- Показать все таблицы
\dt

-- Показать структуру таблицы
\d users

-- Выполнить SQL скрипт
\i sql/create_users_table.sql

-- Выйти
\q
```

---

## Если psql не найден

Убедитесь, что PostgreSQL установлен и добавлен в PATH, или используйте полный путь:

```bash
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -d video_editor_bot
```

(Замените `15` на вашу версию PostgreSQL)

