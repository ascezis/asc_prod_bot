"""
Простой HTTP сервер для тестирования Web App локально
Использование: python app/webapp/server.py
"""
import http.server
import socketserver
import os
import sys

# Добавляем путь к корню проекта
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Добавляем CORS заголовки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🌐 Web App сервер запущен на http://localhost:{PORT}")
        print(f"📁 Директория: {DIRECTORY}")
        print(f"\n📱 Для Telegram Web App используйте ngrok:")
        print(f"   ngrok http {PORT}")
        print(f"\n🔗 После запуска ngrok обновите URL в:")
        print(f"   - app/bot/handlers/start.py")
        print(f"   - app/bot/handlers/webapp.py")
        print(f"\n⏹️  Для остановки нажмите Ctrl+C")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")

if __name__ == "__main__":
    main()

