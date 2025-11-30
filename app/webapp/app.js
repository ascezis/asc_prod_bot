// Telegram Web App API
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// API URL - для ngrok используем тот же домен, но backend должен быть доступен
// Если backend на localhost:8000, нужно запустить отдельный ngrok для него
// Или настроить прокси в ngrok для порта 8000
// const API_URL = window.location.hostname.includes('ngrok') 
//     ? 'http://localhost:8000'  // Если backend на localhost, используем напрямую (только для теста)
//     : 'http://localhost:8000';

// Если запустите отдельный ngrok для backend (порт 8000), раскомментируйте и укажите URL:
const API_URL = 'https://overfemininely-subministrant-jenell.ngrok-free.dev';

// Получаем данные пользователя из Telegram
const user = tg.initDataUnsafe?.user;
const userId = user?.id;

// Навигация
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const page = btn.dataset.page;
        switchPage(page);
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

function switchPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(`${page}-page`).classList.add('active');
    
    if (page === 'track') {
        loadProjects();
    }
}

// Загрузка заявок пользователя
async function loadProjects() {
    const listEl = document.getElementById('projects-list');
    listEl.innerHTML = '<div class="loading">Загрузка...</div>';
    
    if (!userId) {
        listEl.innerHTML = '<div class="error-message">Не удалось определить пользователя</div>';
        return;
    }
    
    try {
        // Используем endpoint для Web App (без авторизации, только telegram_id)
        const response = await fetch(`${API_URL}/projects/webapp?telegram_id=${userId}`);
        
        if (!response.ok) {
            throw new Error('Ошибка загрузки заявок');
        }
        
        const projects = await response.json();
        
        if (projects.length === 0) {
            listEl.innerHTML = '<div class="empty-state">У вас пока нет заявок</div>';
            return;
        }
        
        listEl.innerHTML = projects.map(project => createProjectCard(project)).join('');
        
        // Добавляем обработчики клика
        document.querySelectorAll('.project-card').forEach(card => {
            card.addEventListener('click', () => showProjectDetails(card.dataset.projectId));
        });
        
    } catch (error) {
        console.error('Ошибка загрузки заявок:', error);
        listEl.innerHTML = '<div class="error-message">Ошибка загрузки заявок. Попробуйте позже.</div>';
    }
}

// Создание карточки заявки
function createProjectCard(project) {
    const statusLabels = {
        'new': { text: 'Новая', class: 'status-new' },
        'in_progress': { text: 'В работе', class: 'status-in_progress' },
        'completed': { text: 'Завершена', class: 'status-completed' },
        'rejected': { text: 'Отклонена', class: 'status-rejected' }
    };
    
    const status = statusLabels[project.status] || statusLabels['new'];
    const date = new Date(project.created_at).toLocaleDateString('ru-RU');
    
    return `
        <div class="project-card" data-project-id="${project.id}">
            <div class="project-header">
                <span class="project-id">#${project.id}</span>
                <span class="status-badge ${status.class}">${status.text}</span>
            </div>
            <div class="project-type">${project.project_type || 'Не указано'}</div>
            <div class="project-info">Бюджет: ${project.budget || 'Не указан'}</div>
            <div class="project-info">Срок: ${project.deadline || 'Не указан'}</div>
            <div class="project-date">Создана: ${date}</div>
        </div>
    `;
}

// Показ деталей заявки
async function showProjectDetails(projectId) {
    // TODO: Реализовать модальное окно с деталями
    tg.showAlert(`Детали заявки #${projectId}`);
}

// Показ деталей заявки (улучшенная версия)
async function showProjectDetails(projectId) {
    if (!userId) return;
    
    try {
        const response = await fetch(`${API_URL}/projects/webapp?telegram_id=${userId}`);
        const projects = await response.json();
        const project = projects.find(p => p.id === parseInt(projectId));
        
        if (!project) {
            tg.showAlert('Заявка не найдена');
            return;
        }
        
        const statusLabels = {
            'new': 'Новая',
            'in_progress': 'В работе',
            'completed': 'Завершена',
            'rejected': 'Отклонена'
        };
        
        const details = `
📋 Заявка #${project.id}

Тип: ${project.project_type || 'Не указано'}
Статус: ${statusLabels[project.status] || project.status}
Бюджет: ${project.budget || 'Не указан'}
Срок: ${project.deadline || 'Не указан'}

Исходный материал: ${project.duration_raw || 'Не указано'}
Готовое видео: ${project.duration_final || 'Не указано'}
Услуги: ${(project.services || []).join(', ') || 'Не указано'}

${project.additional_notes ? `Заметки: ${project.additional_notes}` : ''}
        `.trim();
        
        tg.showAlert(details);
        
    } catch (error) {
        console.error('Ошибка загрузки деталей:', error);
        tg.showAlert('Ошибка загрузки деталей заявки');
    }
}

// Обработка формы создания заявки
document.getElementById('project-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        project_type: document.getElementById('project_type').value,
        duration_raw: document.getElementById('duration_raw').value,
        duration_final: document.getElementById('duration_final').value,
        services: Array.from(document.querySelectorAll('input[name="services"]:checked')).map(cb => cb.value),
        deadline: document.getElementById('deadline').value,
        budget: document.getElementById('budget').value,
        source_links: document.getElementById('source_links').value,
        style_examples: document.getElementById('style_examples').value,
        additional_notes: document.getElementById('additional_notes').value,
    };
    
    // Валидация
    if (!formData.project_type || !formData.duration_raw || !formData.duration_final || 
        formData.services.length === 0 || !formData.deadline || !formData.budget) {
        tg.showAlert('Заполните все обязательные поля');
        return;
    }
    
    // Отправляем данные боту через Web App API
    tg.sendData(JSON.stringify({
        action: 'create_project',
        data: formData
    }));
    
    // Показываем уведомление
    tg.showAlert('Заявка отправлена! Мы свяжемся с вами в ближайшее время.');
    
    // Очищаем форму
    document.getElementById('project-form').reset();
    
    // Переключаемся на страницу отслеживания
    switchPage('track');
    document.querySelectorAll('.nav-btn').forEach(b => {
        b.classList.remove('active');
        if (b.dataset.page === 'track') b.classList.add('active');
    });
});

// Обработка данных от бота
tg.onEvent('viewportChanged', () => {
    tg.expand();
});

// Инициализация
if (userId) {
    console.log('User ID:', userId);
} else {
    console.error('Не удалось получить ID пользователя');
}

