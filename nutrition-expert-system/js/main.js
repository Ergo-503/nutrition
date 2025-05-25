// Головна функція розрахунку харчування
function calculateNutrition() {
    try {
        // Збираємо дані з форми
        const age = parseInt(document.getElementById('age').value);
        const weight = parseFloat(document.getElementById('weight').value);
        const height = parseFloat(document.getElementById('height').value);
        const gender = document.getElementById('gender').value;
        const activityLevel = parseFloat(document.getElementById('activity').value);
        const goal = document.getElementById('goal').value;
        const isVegan = document.getElementById('vegan').checked;
        const isDiabetic = document.getElementById('diabetes').checked;
        
        // Валідація даних
        if (isNaN(age) || isNaN(weight) || isNaN(height)) {
            throw new Error('Будь ласка, введіть коректні числові значення');
        }
        
        if (age < 16 || age > 80) {
            throw new Error('Вік має бути від 16 до 80 років');
        }
        
        if (weight < 40 || weight > 200) {
            throw new Error('Вага має бути від 40 до 200 кг');
        }
        
        if (height < 140 || height > 220) {
            throw new Error('Зріст має бути від 140 до 220 см');
        }
        
        // Розрахунки
        const bmr = calculateBMR(weight, height, age, gender);
        let tdee = bmr * activityLevel;
        
        // Корекція калорійності залежно від мети
        if (goal === 'gain') {
            tdee *= 1.15; // +15% для набору маси
        } else if (goal === 'lose') {
            tdee *= 0.85; // -15% для схуднення
        }
        
        const macros = calculateMacronutrients(tdee, weight, goal);
        
        // Оптимізація продуктів
        const optimization = optimizeProducts(
            tdee, 
            macros.protein, 
            macros.fat, 
            macros.carbs, 
            isVegan, 
            isDiabetic
        );
        
        // Відображення результатів
        displayResults(bmr, tdee, macros, optimization, goal, weight, isVegan, isDiabetic);
        
    } catch (error) {
        showError(error.message);
    }
}

// Функція відображення результатів
function displayResults(bmr, tdee, macros, optimization, goal, weight, isVegan, isDiabetic) {
    // Показуємо секцію результатів
    document.getElementById('results').style.display = 'block';
    
    // Відображаємо потреби в харчуванні
    const needsText = `
🔥 Калорії: ${Math.round(tdee)} ккал/день
🥩 Білки: ${macros.protein}г (${Math.round(macros.protein * 4 / tdee * 100)}%)
🥑 Жири: ${macros.fat}г (${Math.round(macros.fat * 9 / tdee * 100)}%)
🍞 Вуглеводи: ${macros.carbs}г (${Math.round(macros.carbs * 4 / tdee * 100)}%)

📊 BMR (базальний метаболізм): ${Math.round(bmr)} ккал
⚡ TDEE (загальні витрати): ${Math.round(tdee)} ккал
🎯 Мета: ${getGoalText(goal)}
    `;
    
    document.getElementById('nutritional-needs').textContent = needsText.trim();
    
    // Відображаємо список продуктів
    let productsText = '📋 ОПТИМАЛЬНИЙ СПИСОК ПРОДУКТІВ:\n\n';
    optimization.products.forEach((product, index) => {
        productsText += `${index + 1}. ${product.name}: ${product.amount}г\n`;
    });
    
    productsText += `\n📊 ФАКТИЧНИЙ СКЛАД РАЦІОНУ:\n`;
    productsText += `Калорії: ${optimization.actualNutrition.calories} ккал\n`;
    productsText += `Білки: ${optimization.actualNutrition.protein}г\n`;
    productsText += `Жири: ${optimization.actualNutrition.fat}г\n`;
    productsText += `Вуглеводи: ${optimization.actualNutrition.carbs}г`;
    
    document.getElementById('products-list').textContent = productsText;
    document.getElementById('total-cost').textContent = `💰 Загальна вартість: ${optimization.totalCost.toFixed(2)} грн/день`;
    
    // Пояснення рекомендацій
    const explanationText = generateExplanation(goal, isVegan, isDiabetic, macros, weight);
    document.getElementById('explanation').innerHTML = explanationText;
    
    // Створюємо графіки
    createMacroChart(macros);
    createWeightChart(weight, goal);
    
    // Додаємо кнопку експорту
    addExportButton();
    
    // Скролимо до результатів
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

// Допоміжна функція для отримання тексту мети
function getGoalText(goal) {
    switch(goal) {
        case 'gain': return 'Набір маси';
        case 'lose': return 'Схуднення/Сушка';
        default: return 'Підтримання форми';
    }
}

// Генерація пояснень
function generateExplanation(goal, isVegan, isDiabetic, macros, weight) {
    let explanation = '<h4>🎯 Основи розрахунку:</h4>';
    explanation += '<p>Ваші потреби розраховані за науково обґрунтованою формулою Міффліна-Сан-Джеор ';
    explanation += 'з урахуванням рівня фізичної активності та поставленої мети.</p>';
    
    explanation += '<h4>💡 Рекомендації по харчуванню:</h4><ul>';
    
    if (goal === 'gain') {
        explanation += '<li>Споживайте 20-30г білків протягом 2 годин після тренування</li>';
        explanation += '<li>Розподіліть прийоми їжі на 5-6 разів на день</li>';
        explanation += '<li>Не забувайте про достатню кількість води (35-40мл на кг ваги)</li>';
    } else if (goal === 'lose') {
        explanation += '<li>Створіть помірний дефіцит калорій (не більше 500 ккал на день)</li>';
        explanation += '<li>Підтримуйте високе споживання білків для збереження м\'язової маси</li>';
        explanation += '<li>Додайте кардіо-тренування 3-4 рази на тиждень</li>';
    } else {
        explanation += '<li>Дотримуйтесь збалансованого харчування</li>';
        explanation += '<li>Споживайте різноманітні продукти для отримання всіх мікронутрієнтів</li>';
        explanation += '<li>Регулярно контролюйте вагу та самопочуття</li>';
    }
    
    if (isVegan) {
        explanation += '<li><strong>Веганська дієта:</strong> Поєднуйте різні рослинні білки, ';
        explanation += 'додайте вітамін B12, омега-3 та залізо</li>';
    }
    
    if (isDiabetic) {
        explanation += '<li><strong>Діабетичні обмеження:</strong> Всі продукти мають низький ';
        explanation += 'глікемічний індекс для стабільного рівня цукру</li>';
    }
    
    explanation += '</ul>';
    
    explanation += '<h4>⚠️ Важливі застереження:</h4>';
    explanation += '<p><small>Ці рекомендації носять загальний характер. Перед кардинальними змінами ';
    explanation += 'в харчуванні обов\'язково проконсультуйтесь з лікарем або дієтологом, особливо ';
    explanation += 'при наявності хронічних захворювань.</small></p>';
    
    return explanation;
}

// Ініціалізація при завантаженні сторінки
document.addEventListener('DOMContentLoaded', function() {
    // Додаємо обробники подій для валідації
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateInput(this);
        });
    });
    
    // Скриваємо результати на початку
    document.getElementById('results').style.display = 'none';
});