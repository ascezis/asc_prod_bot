"""
Быстрый тест для проверки работы /auth/login
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("ТЕСТИРОВАНИЕ /auth/login")
print("=" * 60)

# Проверка доступности backend
print("\n1. Проверка доступности backend...")
try:
    response = requests.get(f"{BASE_URL}/docs", timeout=2)
    if response.status_code == 200:
        print("✅ Backend доступен")
    else:
        print(f"⚠️ Backend отвечает, но статус: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("❌ Backend не запущен!")
    print("   Запустите: python run.py")
    exit(1)
except Exception as e:
    print(f"❌ Ошибка: {e}")
    exit(1)

# Тест входа
print("\n2. Тестирование входа...")
username = input("Username: ").strip()
password = input("Password: ").strip()

if not username or not password:
    print("❌ Username и Password обязательны!")
    exit(1)

try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": username,
            "password": password
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    print(f"\nСтатус ответа: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ ВХОД УСПЕШЕН!")
        print(f"\nТокен (первые 50 символов): {data['access_token'][:50]}...")
        print(f"\nИнформация о пользователе:")
        print(json.dumps(data['user'], indent=2, ensure_ascii=False))
        
        # Сохраняем токен для дальнейших тестов
        token = data['access_token']
        
        # Тест защищенного endpoint
        print("\n3. Тестирование защищенного endpoint /auth/me...")
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ /auth/me работает!")
            print(f"   Пользователь: {user_data['username']} ({user_data['role']})")
        else:
            print(f"❌ Ошибка /auth/me: {response.status_code}")
            print(f"   Ответ: {response.text}")
            
    elif response.status_code == 401:
        print("\n❌ ОШИБКА ВХОДА: Неверный username или password")
        print(f"   Ответ: {response.text}")
    else:
        print(f"\n❌ Неожиданный статус: {response.status_code}")
        print(f"   Ответ: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ Ошибка запроса: {e}")
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

