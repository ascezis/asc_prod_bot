@echo off
chcp 65001
cd /d "C:\Users\azis\Desktop\asc_prod_bot"
call venv\Scripts\activate.bat

echo Установка зависимостей...
pip install -r requirements.txt

echo Запуск бота...
python -m app.main
pause