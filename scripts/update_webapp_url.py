"""
Скрипт для обновления URL Web App в коде
Использование: python scripts/update_webapp_url.py <ngrok_url>
Пример: python scripts/update_webapp_url.py https://abc123.ngrok.io
"""
import sys
import re
import os

def update_url_in_file(file_path, old_pattern, new_url):
    """Обновляет URL в файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем все вхождения
        new_content = re.sub(old_pattern, new_url, content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Обновлен: {file_path}")
            return True
        else:
            print(f"⚠️  Не найдено совпадений в: {file_path}")
            return False
    except Exception as e:
        print(f"❌ Ошибка в {file_path}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Использование: python scripts/update_webapp_url.py <ngrok_url>")
        print("Пример: python scripts/update_webapp_url.py https://abc123.ngrok.io")
        sys.exit(1)
    
    new_url = sys.argv[1].rstrip('/')
    webapp_url = f"{new_url}/index.html"
    
    # Убираем протокол для API URL (если нужен тот же домен)
    api_url = new_url
    
    print(f"🔄 Обновление URL Web App на: {webapp_url}")
    print(f"🔄 API URL: {api_url}")
    print()
    
    # Файлы для обновления
    files_to_update = [
        {
            'path': 'app/bot/handlers/start.py',
            'pattern': r'https://your-domain\.com/webapp/index\.html|https://[a-zA-Z0-9-]+\.ngrok\.io/index\.html'
        },
        {
            'path': 'app/bot/handlers/webapp.py',
            'pattern': r'https://your-domain\.com/webapp/index\.html|https://[a-zA-Z0-9-]+\.ngrok\.io/index\.html'
        }
    ]
    
    updated = 0
    for file_info in files_to_update:
        if update_url_in_file(file_info['path'], file_info['pattern'], webapp_url):
            updated += 1
    
    print()
    print(f"✅ Обновлено файлов: {updated}/{len(files_to_update)}")
    print()
    print("📝 Также проверьте app/webapp/app.js - возможно нужно обновить API_URL вручную")

if __name__ == "__main__":
    main()

