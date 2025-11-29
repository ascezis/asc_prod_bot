import os
import sys
import subprocess
import signal
import threading
import time
import io


# --- корректный вывод UTF-8 + немедленный вывод ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

# Корень проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------
# МОДУЛИ ПРОЦЕССОВ
# ------------------------------------------------------------------

class ManagedProcess:
    def __init__(self, name: str, cmd, cwd: str):
        self.name = name
        self.cmd = cmd
        self.cwd = cwd
        self.proc: subprocess.Popen | None = None
        self.thread: threading.Thread | None = None
        self.running = False

    def start(self):
        if self.running:
            print(f"⚠️ {self.name} уже запущен")
            return

        print(f"\n🚀 Запуск {self.name} в {self.cwd}")
        self.proc = subprocess.Popen(
            self.cmd,
            cwd=self.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True if isinstance(self.cmd, str) else False
        )

        self.running = True

        # поток чтения логов
        self.thread = threading.Thread(
            target=self.stream_output,
            name=f"{self.name}-logger",
            daemon=True
        )
        self.thread.start()

    def stream_output(self):
        """Читает stdout в реальном времени"""
        if not self.proc or not self.proc.stdout:
            return

        for line in self.proc.stdout:
            print(f"[{self.name}] {line}", end="")

        print(f"[{self.name}] 🔚 Поток завершён")

    def stop(self):
        if not self.running or not self.proc:
            print(f"⚠️ {self.name} не запущен")
            return

        print(f"🛑 Остановка {self.name}")

        try:
            self.proc.terminate()
        except Exception:
            pass

        self.running = False


# ------------------------------------------------------------------
# МЕНЕДЖЕР ПРОЦЕССОВ
# ------------------------------------------------------------------

class ProcessManager:
    def __init__(self):
        self.processes: dict[str, ManagedProcess] = {}

    def register(self, name: str, cmd, cwd: str):
        self.processes[name] = ManagedProcess(name, cmd, cwd)

    def start(self, name: str):
        if name in self.processes:
            self.processes[name].start()

    def stop(self, name: str):
        if name in self.processes:
            self.processes[name].stop()

    def stop_all(self):
        print("\n🔻 Остановка всех процессов...")
        for p in self.processes.values():
            p.stop()

    def all_alive(self):
        return any(
            p.proc and p.proc.poll() is None
            for p in self.processes.values()
        )


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------

def main():
    manager = ProcessManager()

    # --- регистрация модулей ---
    manager.register(
        "Backend",
        [sys.executable, "-m", "uvicorn", "admin.backend.main:app", "--reload", "--port", "8000"],
        PROJECT_ROOT
    )

    manager.register(
        "Frontend",
        "npm run dev",
        os.path.join(PROJECT_ROOT, "admin", "frontend")
    )

    manager.register(
        "Bot",
        [sys.executable, "-m", "app.main"],
        PROJECT_ROOT
    )

    # обработчик Ctrl+C
    signal.signal(signal.SIGINT, lambda sig, frame: manager.stop_all() or sys.exit(0))

    # --- запуск всех по умолчанию ---
    manager.start("Backend")
    manager.start("Frontend")
    manager.start("Bot")

    # Главный цикл: кроссплатформенная версия
    try:
        while True:
            if not manager.all_alive():
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        manager.stop_all()


if __name__ == "__main__":
    main()
