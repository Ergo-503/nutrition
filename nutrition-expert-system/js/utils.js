// Файл utils.js содержит вспомогательные функции для валидации ввода и работы с localStorage

// Відображення помилки
function showError(message) {
    // Видаляємо попередні помилки
    const existingErrors = document.querySelectorAll('.error');
    existingErrors.forEach(error => error.remove());
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        font-weight: bold;
    `;
    
    const container = document.querySelector('.main-content');
    container.insertBefore(errorDiv, container.firstChild);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Валідація введених даних
function validateInput(input) {
    const value = parseFloat(input.value);
    let isValid = true;
    let message = '';
    
    switch(input.id) {
        case 'age':
            isValid = value >= 16 && value <= 80;
            message = 'Вік має бути від 16 до 80 років';
            break;
        case 'weight':
            isValid = value >= 40 && value <= 200;
            message = 'Вага має бути від 40 до 200 кг';
            break;
        case 'height':
            isValid = value >= 140 && value <= 220;
            message = 'Зріст має бути від 140 до 220 см';
            break;
    }
    
    if (!isValid && value) {
        input.style.borderColor = '#dc3545';
        input.style.backgroundColor = '#fff5f5';
        input.title = message;
    } else {
        input.style.borderColor = '#e9ecef';
        input.style.backgroundColor = 'white';
        input.title = '';
    }
}

// Функція експорту результатів
function exportResults() {
    const results = document.getElementById('results');
    if (results.style.display === 'none') {
        alert('Спочатку виконайте розрахунок!');
        return;
    }
    
    // Збираємо всі результати в текстовому форматі
    const date = new Date().toLocaleDateString('uk-UA');
    const needs = document.getElementById('nutritional-needs').textContent;
    const products = document.getElementById('products-list').textContent;
    const explanation = document.getElementById('explanation').textContent;
    
    const exportText = `
ЕКСПЕРТНА СИСТЕМА ХАРЧУВАННЯ ДЛЯ СПОРТСМЕНІВ
============================================
Дата: ${date}

РОЗРАХОВАНІ ПОТРЕБИ:
${needs}

РЕКОМЕНДОВАНІ ПРОДУКТИ:
${products}

ПОЯСНЕННЯ:
${explanation}

============================================
Цей звіт створено експертною системою.
Рекомендується консультація з дієтологом.
    `;
    
    // Створюємо і завантажуємо файл
    const blob = new Blob([exportText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `nutrition_plan_${date.replace(/\./g, '_')}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Додаємо кнопку експорту після розрахунку
function addExportButton() {
    const resultsSection = document.getElementById('results');
    if (!document.getElementById('export-btn')) {
        const exportBtn = document.createElement('button');
        exportBtn.id = 'export-btn';
        exportBtn.className = 'calculate-btn';
        exportBtn.textContent = '💾 Зберегти результати';
        exportBtn.onclick = exportResults;
        exportBtn.style.marginTop = '20px';
        
        resultsSection.appendChild(exportBtn);
    }
}

// Функція очищення всіх даних
function clearAllData() {
    if (confirm('Ви впевнені, що хочете очистити всі дані?')) {
        // Скидаємо значення форми
        document.getElementById('age').value = '25';
        document.getElementById('weight').value = '70';
        document.getElementById('height').value = '175';
        document.getElementById('gender').value = 'male';
        document.getElementById('activity').value = '1.55';
        document.getElementById('goal').value = 'maintain';
        document.getElementById('vegan').checked = false;
        document.getElementById('diabetes').checked = false;
        
        // Скриваємо результати
        document.getElementById('results').style.display = 'none';
        
        // Очищуємо помилки
        const errors = document.querySelectorAll('.error');
        errors.forEach(error => error.remove());
        
        // Скидаємо валідацію полів
        const inputs = document.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            input.style.borderColor = '#e9ecef';
            input.style.backgroundColor = 'white';
            input.title = '';
        });
    }
}