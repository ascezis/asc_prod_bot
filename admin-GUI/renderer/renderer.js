const startBtn = document.getElementById('start');
const stopBtn = document.getElementById('stop');
const log = document.getElementById('log');

startBtn.addEventListener('click', () => {
  window.electronAPI.startPython();
});

stopBtn.addEventListener('click', () => {
  window.electronAPI.stopPython();
});

window.electronAPI.onPythonLog((data) => {
  const text = data.toString();
  typeLine(text);
});

function typeLine(line) {
  const log = document.getElementById("log");

  const div = document.createElement("div");
  div.className = "typed-line";
  log.appendChild(div);

  let i = 0;
  function type() {
    if (i < line.length) {
      div.textContent += line[i];
      i++;
      log.scrollTop = log.scrollHeight; // прокрутка вниз
      requestAnimationFrame(type);       // плавная печать
    } else {
      div.classList.remove("typed-line"); // убрать курсор после завершения
    }
  }
  type();
}
