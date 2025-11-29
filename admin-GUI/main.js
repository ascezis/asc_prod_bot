const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let win;
let pythonProcess;

function createWindow() {
  win = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

app.whenReady().then(createWindow);

ipcMain.on('start-python', () => {
  if (pythonProcess) return;

  const scriptPath = path.join(__dirname, '..', 'run.py');

  // 🔹 Запуск Python с -u для unbuffered
  pythonProcess = spawn('python', ['-u', scriptPath]);

  pythonProcess.stdout.on('data', (data) => {
    win.webContents.send('python-log', data.toString());
  });

  pythonProcess.stderr.on('data', (data) => {
    win.webContents.send('python-log', data.toString());
  });

  pythonProcess.on('close', (code) => {
    win.webContents.send('python-log', `Python process exited with code ${code}`);
    pythonProcess = null;
  });
});

ipcMain.on('stop-python', () => {
  if (pythonProcess) {
    pythonProcess.kill();
    pythonProcess = null;
  }
});
