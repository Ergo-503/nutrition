// Главная функция для расчета питания
function calculateNutrition() {
    // Получение данных из формы
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);
    const age = parseInt(document.getElementById('age').value);
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const activityLevel = document.getElementById('activity-level').value;

    // Проверка валидности введенных данных
    if (validateInput(weight, height, age)) {
        // Расчет BMR
        const bmr = calculateBMR(weight, height, age, gender);
        
        // Расчет макронутриентов
        const macronutrients = calculateMacronutrients(bmr, weight, activityLevel);
        
        // Отображение результатов
        displayResults(macronutrients);
    } else {
        showError("Будь ласка, введіть правильні дані.");
    }
}

// Функция для отображения результатов
function displayResults(macronutrients) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = ''; // Очистка предыдущих результатов

    // Создание и отображение элементов с результатами
    for (const [key, value] of Object.entries(macronutrients)) {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';
        resultItem.innerHTML = `<strong>${key}:</strong> ${value}`;
        resultsContainer.appendChild(resultItem);
    }

    resultsContainer.style.display = 'block'; // Показать результаты
}

// Установка обработчиков событий
document.getElementById('calculate-btn').addEventListener('click', calculateNutrition);