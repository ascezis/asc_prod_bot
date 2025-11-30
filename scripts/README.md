# 🔧 Скрипты проекта

## Создание пользователей

- **[create_owner_simple.py](./create_owner_simple.py)** - Создание первого пользователя-владельца (упрощенная версия, рекомендуется)
- **[create_owner.py](./create_owner.py)** - Создание первого пользователя-владельца (полная версия)
- **[create_user.py](./create_user.py)** - Создание пользователей с любой ролью (user, admin, owner)

### Использование:
```bash
# Создать первого владельца
python scripts/create_owner_simple.py

# Создать пользователя с любой ролью
python scripts/create_user.py
```

## Тестирование

- **[test_login.py](./test_login.py)** - Полное тестирование системы аутентификации
- **[test_login_simple.py](./test_login_simple.py)** - Простой тест входа без FastAPI
- **[test_password.py](./test_password.py)** - Тест проверки пароля пользователя
- **[test_config.py](./test_config.py)** - Проверка конфигурации проекта

### Использование:
```bash
python scripts/test_login_simple.py
```

## Утилиты

- **[check_config.py](./check_config.py)** - Проверка конфигурации проекта
- **[fix_port.py](./fix_port.py)** - Исправление проблем с портами
- **[cache_cleaner.py](./cache_cleaner.py)** - Очистка кэша

---

**Примечание:** Все скрипты должны запускаться из корня проекта.
