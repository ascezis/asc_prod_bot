const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  startPython: () => ipcRenderer.send('start-python'),
  stopPython: () => ipcRenderer.send('stop-python'),
  onPythonLog: (callback) => ipcRenderer.on('python-log', (_, data) => callback(data)),
});
