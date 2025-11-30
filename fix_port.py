"""
Скрипт для исправления порта в run.py
"""
import re
from pathlib import Path

def fix_port():
    """Исправляет порт с 8001 на 8000 в run.py"""
    run_py = Path("run.py")
    
    if not run_py.exists():
        print("❌ Файл run.py не найден!")
        return False
    
    # Читаем файл
    content = run_py.read_text(encoding="utf-8")
    
    # Заменяем порт 8001 на 8000
    new_content = content.replace('"--port", "8001"', '"--port", "8000"')
    new_content = new_content.replace("--port", "8001", "--port", "8000")
    
    # Если ничего не изменилось, пробуем через regex
    if new_content == content:
        new_content = re.sub(r'--port["\s,]+8001', '--port", "8000', content)
    
    # Проверяем, что замена произошла
    if '"--port", "8000"' in new_content or '--port", "8000' in new_content:
        run_py.write_text(new_content, encoding="utf-8")
        print("✅ Порт исправлен с 8001 на 8000 в run.py")
        return True
    else:
        print("⚠️ Порт 8001 не найден в файле. Возможно, уже исправлен.")
        return False

if __name__ == "__main__":
    fix_port()

