// Файл utils.js содержит вспомогательные функции для валидации ввода и работы с localStorage

// Функция для валидации пользовательского ввода
function validateInput(input) {
    // Проверка на пустое значение
    if (!input || input.trim() === '') {
        showError('Введіть коректне значення.');
        return false;
    }
    return true;
}

// Функция для отображения сообщения об ошибке
function showError(message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'error';
    errorElement.textContent = message;
    document.body.appendChild(errorElement);
    setTimeout(() => {
        errorElement.remove();
    }, 3000);
}

// Функция для экспорта результатов в localStorage
function exportResults(data) {
    localStorage.setItem('nutritionResults', JSON.stringify(data));
}

// Функция для очистки всех данных
function clearAllData() {
    localStorage.removeItem('nutritionResults');
}

// Функция для добавления кнопки экспорта
function addExportButton() {
    const button = document.createElement('button');
    button.textContent = 'Експортувати результати';
    button.onclick = () => {
        const results = localStorage.getItem('nutritionResults');
        if (results) {
            const blob = new Blob([results], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'results.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } else {
            showError('Немає результатів для експорту.');
        }
    };
    document.body.appendChild(button);
}