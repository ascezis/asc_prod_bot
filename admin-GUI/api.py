from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import subprocess
import threading

app = FastAPI()

# Разрешаем запросы с Electron
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

processes: Dict[str, subprocess.Popen] = {}

@app.get("/status")
def status():
    result = {}
    for name, proc in processes.items():
        result[name] = "running" if proc.poll() is None else "stopped"
    return result

@app.post("/bot/start")
def start_bot():
    if "bot" in processes and processes["bot"].poll() is None:
        return {"status": "already running"}

    cmd = ["python", "-m", "app.main"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    processes["bot"] = proc

    # Поток для вывода логов
    def stream_output(p):
        for line in p.stdout:
            print(f"[Bot] {line}", end="")

    threading.Thread(target=stream_output, args=(proc,), daemon=True).start()
    return {"status": "started"}

@app.post("/bot/stop")
def stop_bot():
    proc = processes.get("bot")
    if not proc or proc.poll() is not None:
        return {"status": "not running"}
    proc.terminate()
    return {"status": "stopped"}

# TODO: /logs, /config, /cache
