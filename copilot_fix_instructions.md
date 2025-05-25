# GitHub Copilot: Инструкции по исправлению ошибок в проекте nutrition-expert-system

## ПРОБЛЕМА
Созданная структура проекта не работает корректно. Программа должна работать ИДЕНТИЧНО исходному файлу `nutrition_expert_system_js.html`.

## КРИТИЧЕСКИЕ ОШИБКИ, КОТОРЫЕ НУЖНО ИСПРАВИТЬ

### 1. ИСПРАВИТЬ index.html - ВОССТАНОВИТЬ ВСЮ HTML-РАЗМЕТКУ

**ПРОБЛЕМА:** В `index.html` отсутствует большая часть HTML-разметки форм и элементов.

**ИСПРАВЛЕНИЕ:** Полностью заменить содержимое `index.html` на:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Експертна система раціонального харчування для спортсменів</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏃‍♂️ Експертна система харчування</h1>
            <p>Персоналізовані рекомендації для спортсменів</p>
        </div>

        <div class="main-content">
            <div class="input-section">
                <h2 class="section-title">Введіть ваші параметри</h2>
                
                <div class="form-grid">
                    <div class="form-group">
                        <h3>👤 Особисті дані</h3>
                        
                        <div class="input-field">
                            <label for="gender">Стать:</label>
                            <select id="gender">
                                <option value="male">Чоловіча</option>
                                <option value="female">Жіноча</option>
                            </select>
                        </div>

                        <div class="input-field">
                            <label for="age">Вік (років):</label>
                            <input type="number" id="age" min="16" max="80" value="25">
                        </div>

                        <div class="input-field">
                            <label for="weight">Вага (кг):</label>
                            <input type="number" id="weight" min="40" max="200" step="0.1" value="70">
                        </div>

                        <div class="input-field">
                            <label for="height">Зріст (см):</label>
                            <input type="number" id="height" min="140" max="220" value="175">
                        </div>
                    </div>

                    <div class="form-group">
                        <h3>🏋️ Спортивна діяльність</h3>
                        
                        <div class="input-field">
                            <label for="activity">Рівень активності:</label>
                            <select id="activity">
                                <option value="1.2">Дуже низька (сидячий спосіб життя)</option>
                                <option value="1.375">Низька (1-3 тренування/тиждень)</option>
                                <option value="1.55" selected>Середня (3-5 тренувань/тиждень)</option>
                                <option value="1.725">Висока (6-7 тренувань/тиждень)</option>
                                <option value="1.9">Дуже висока (щоденні тренування)</option>
                            </select>
                        </div>

                        <div class="input-field">
                            <label for="goal">Мета:</label>
                            <select id="goal">
                                <option value="maintain" selected>Підтримання форми</option>
                                <option value="gain">Набір маси</option>
                                <option value="lose">Схуднення/Сушка</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <h3>🥗 Дієтичні обмеження</h3>
                        
                        <div class="checkbox-group">
                            <div class="checkbox-item">
                                <input type="checkbox" id="vegan">
                                <label for="vegan">Веганська дієта</label>
                            </div>
                            
                            <div class="checkbox-item">
                                <input type="checkbox" id="diabetes">
                                <label for="diabetes">Діабет (низький ГІ)</label>
                            </div>
                        </div>
                    </div>
                </div>

                <button class="calculate-btn" onclick="calculateNutrition()">
                    🔍 Розрахувати раціон
                </button>
            </div>

            <div id="results" class="results-section">
                <h2 class="section-title">Результати розрахунку</h2>
                
                <div class="results-grid">
                    <div class="result-card">
                        <h3>📊 Ваші потреби</h3>
                        <div id="nutritional-needs" class="needs-display"></div>
                    </div>

                    <div class="result-card">
                        <h3>🛒 Рекомендовані продукти</h3>
                        <div id="products-list" class="products-list"></div>
                        <div id="total-cost" style="margin-top: 15px; font-weight: bold; color: #28a745;"></div>
                    </div>
                </div>

                <div class="explanation-card">
                    <h3>💡 Пояснення рекомендацій</h3>
                    <div id="explanation" class="explanation-text"></div>
                </div>

                <div class="charts-container">
                    <div class="chart-card">
                        <div class="chart-title">Розподіл макронутрієнтів</div>
                        <canvas id="macroChart" class="pie-chart"></canvas>
                    </div>
                    
                    <div class="chart-card">
                        <div class="chart-title">Прогноз зміни ваги</div>
                        <canvas id="weightChart" width="300" height="200"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="js/products.js"></script>
    <script src="js/calculations.js"></script>
    <script src="js/charts.js"></script>
    <script src="js/utils.js"></script>
    <script src="js/main.js"></script>
</body>
</html>
```

### 2. ИСПРАВИТЬ js/products.js - ДОБАВИТЬ ВСЕ ПРОДУКТЫ

**ПРОБЛЕМА:** В базе данных не хватает продуктов.

**ИСПРАВЛЕНИЕ:** Заменить содержимое `js/products.js` на:

```javascript
// База продуктів харчування
const PRODUCTS_DATABASE = [
    {name: "Куряча грудка", protein: 23.0, fat: 1.2, carbs: 0.0, calories: 113, cost: 0.8, vegan: false, gi: 0},
    {name: "Рис круглозернистий", protein: 2.7, fat: 0.3, carbs: 77.0, calories: 344, cost: 0.25, vegan: true, gi: 64},
    {name: "Вівсянка", protein: 12.0, fat: 6.2, carbs: 61.0, calories: 342, cost: 0.3, vegan: true, gi: 42},
    {name: "Банани", protein: 1.1, fat: 0.2, carbs: 21.0, calories: 89, cost: 0.6, vegan: true, gi: 62},
    {name: "Молоко 2.5%", protein: 2.8, fat: 2.5, carbs: 4.7, calories: 52, cost: 0.6, vegan: false, gi: 27},
    {name: "Яйця курячі", protein: 12.7, fat: 11.5, carbs: 0.7, calories: 157, cost: 0.6, vegan: false, gi: 0},
    {name: "Олія соняшникова", protein: 0.0, fat: 99.9, carbs: 0.0, calories: 899, cost: 0.5, vegan: true, gi: 0},
    {name: "Гречка", protein: 12.6, fat: 2.6, carbs: 68.0, calories: 343, cost: 0.45, vegan: true, gi: 54},
    {name: "Творог 5%", protein: 17.2, fat: 5.0, carbs: 1.8, calories: 121, cost: 0.9, vegan: false, gi: 27},
    {name: "Картопля", protein: 2.0, fat: 0.1, carbs: 16.0, calories: 77, cost: 0.2, vegan: true, gi: 85},
    {name: "Риба морська", protein: 20.0, fat: 8.0, carbs: 0.0, calories: 150, cost: 3.0, vegan: false, gi: 0},
    {name: "Квасоля червона", protein: 8.4, fat: 0.3, carbs: 13.7, calories: 93, cost: 0.6, vegan: true, gi: 29},
    {name: "Чечевиця", protein: 9.0, fat: 0.4, carbs: 20.0, calories: 116, cost: 0.8, vegan: true, gi: 29},
    {name: "Горіхи волоські", protein: 16.2, fat: 60.8, carbs: 11.1, calories: 656, cost: 4.0, vegan: true, gi: 15},
    {name: "Хліб житній", protein: 6.6, fat: 1.2, carbs: 34.2, calories: 174, cost: 0.6, vegan: true, gi: 58}
];
```

### 3. ПОЛНОСТЬЮ ПЕРЕПИСАТЬ js/calculations.js

**ПРОБЛЕМА:** Функции расчетов неполные и неправильные.

**ИСПРАВЛЕНИЕ:** Заменить содержимое `js/calculations.js` на:

```javascript
// Розрахунок BMR за формулою Міффліна-Сан-Джеор
function calculateBMR(weight, height, age, gender) {
    if (gender === 'male') {
        return 10 * weight + 6.25 * height - 5 * age + 5;
    } else {
        return 10 * weight + 6.25 * height - 5 * age - 161;
    }
}

// Розрахунок потреб у макронутрієнтах
function calculateMacronutrients(calories, weight, goal) {
    let proteinRatio, fatRatio;
    
    switch(goal) {
        case 'gain':
            proteinRatio = 2.2; // г на кг ваги
            fatRatio = 0.20; // 20% від калорій
            break;
        case 'lose':
            proteinRatio = 2.5;
            fatRatio = 0.30; // 30% від калорій
            break;
        default: // maintain
            proteinRatio = 1.8;
            fatRatio = 0.25; // 25% від калорій
    }
    
    const protein = weight * proteinRatio;
    const fat = (calories * fatRatio) / 9; // 9 ккал на грам жиру
    const carbsCalories = calories - (protein * 4) - (fat * 9);
    const carbs = carbsCalories / 4; // 4 ккал на грам вуглеводів
    
    return {
        protein: Math.round(protein),
        fat: Math.round(fat),
        carbs: Math.round(carbs)
    };
}

// Простий алгоритм оптимізації (жадібний підхід)
function optimizeProducts(targetCalories, targetProtein, targetFat, targetCarbs, isVegan, isDiabetic) {
    let availableProducts = PRODUCTS_DATABASE.filter(product => {
        if (isVegan && !product.vegan) return false;
        if (isDiabetic && product.gi > 55 && product.gi !== 0) return false;
        return true;
    });

    if (availableProducts.length === 0) {
        throw new Error('Недостатньо продуктів для вибраних обмежень');
    }

    let selectedProducts = [];
    let currentCalories = 0;
    let currentProtein = 0;
    let currentFat = 0;
    let currentCarbs = 0;
    let totalCost = 0;
    
    // Сортуємо продукти за ефективністю (калорії/ціна)
    availableProducts.sort((a, b) => (b.calories / b.cost) - (a.calories / a.cost));
    
    // Спочатку додаємо основні джерела білка
    const proteinSources = availableProducts.filter(p => p.protein > 15);
    if (proteinSources.length > 0) {
        for (let product of proteinSources.slice(0, 2)) {
            const amount = Math.min(200, (targetProtein * 0.4) / product.protein * 100);
            if (amount > 20) {
                selectedProducts.push({
                    ...product,
                    amount: Math.round(amount)
                });
                
                currentCalories += (product.calories * amount) / 100;
                currentProtein += (product.protein * amount) / 100;
                currentFat += (product.fat * amount) / 100;
                currentCarbs += (product.carbs * amount) / 100;
                totalCost += (product.cost * amount) / 100;
            }
        }
    }
    
    // Додаємо вуглеводні продукти
    const carbSources = availableProducts.filter(p => p.carbs > 50 && !selectedProducts.some(s => s.name === p.name));
    for (let product of carbSources.slice(0, 2)) {
        const neededCarbs = Math.max(0, targetCarbs - currentCarbs);
        const amount = Math.min(150, (neededCarbs * 0.6) / product.carbs * 100);
        if (amount > 20) {
            selectedProducts.push({
                ...product,
                amount: Math.round(amount)
            });
            
            currentCalories += (product.calories * amount) / 100;
            currentProtein += (product.protein * amount) / 100;
            currentFat += (product.fat * amount) / 100;
            currentCarbs += (product.carbs * amount) / 100;
            totalCost += (product.cost * amount) / 100;
        }
    }
    
    // Додаємо жири
    const fatSources = availableProducts.filter(p => p.fat > 20 && !selectedProducts.some(s => s.name === p.name));
    if (fatSources.length > 0 && currentFat < targetFat * 0.8) {
        const product = fatSources[0];
        const neededFat = targetFat - currentFat;
        const amount = Math.min(50, (neededFat * 0.8) / product.fat * 100);
        if (amount > 5) {
            selectedProducts.push({
                ...product,
                amount: Math.round(amount)
            });
            
            currentCalories += (product.calories * amount) / 100;
            currentProtein += (product.protein * amount) / 100;
            currentFat += (product.fat * amount) / 100;
            currentCarbs += (product.carbs * amount) / 100;
            totalCost += (product.cost * amount) / 100;
        }
    }
    
    // Додаємо додаткові продукти для досягнення цільової калорійності
    while (currentCalories < targetCalories * 0.95 && selectedProducts.length < 8) {
        const remainingProducts = availableProducts.filter(p => 
            !selectedProducts.some(s => s.name === p.name) && p.calories > 50
        );
        
        if (remainingProducts.length === 0) break;
        
        const product = remainingProducts[0];
        const neededCalories = targetCalories - currentCalories;
        const amount = Math.min(100, (neededCalories * 0.3) / product.calories * 100);
        
        if (amount > 10) {
            selectedProducts.push({
                ...product,
                amount: Math.round(amount)
            });
            
            currentCalories += (product.calories * amount) / 100;
            currentProtein += (product.protein * amount) / 100;
            currentFat += (product.fat * amount) / 100;
            currentCarbs += (product.carbs * amount) / 100;
            totalCost += (product.cost * amount) / 100;
        } else {
            break;
        }
    }
    
    return {
        products: selectedProducts,
        totalCost: Math.round(totalCost * 100) / 100,
        actualNutrition: {
            calories: Math.round(currentCalories),
            protein: Math.round(currentProtein),
            fat: Math.round(currentFat),
            carbs: Math.round(currentCarbs)
        }
    };
}
```

### 4. ПОЛНОСТЬЮ ПЕРЕПИСАТЬ js/charts.js - УБРАТЬ Chart.js

**ПРОБЛЕМА:** Использует несуществующую библиотеку Chart.js.

**ИСПРАВЛЕНИЕ:** Заменить содержимое `js/charts.js` на Canvas-код из оригинала:

```javascript
// Створення кругової діаграми макронутрієнтів
function createMacroChart(macros) {
    const canvas = document.getElementById('macroChart');
    const ctx = canvas.getContext('2d');
    
    // Очищуємо canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Розрахунок калорій від кожного макронутрієнта
    const proteinCal = macros.protein * 4;
    const fatCal = macros.fat * 9;
    const carbsCal = macros.carbs * 4;
    const total = proteinCal + fatCal + carbsCal;
    
    // Кольори
    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1'];
    const labels = ['Білки', 'Жири', 'Вуглеводи'];
    const values = [proteinCal, fatCal, carbsCal];
    
    // Центр та радіус
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 10;
    
    let currentAngle = -Math.PI / 2; // Починаємо зверху
    
    // Малюємо сектори
    values.forEach((value, index) => {
        const sliceAngle = (value / total) * 2 * Math.PI;
        
        // Сектор
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.closePath();
        ctx.fillStyle = colors[index];
        ctx.fill();
        
        // Обводка
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Підписи
        const labelAngle = currentAngle + sliceAngle / 2;
        const labelX = centerX + Math.cos(labelAngle) * (radius * 0.7);
        const labelY = centerY + Math.sin(labelAngle) * (radius * 0.7);
        
        ctx.fillStyle = 'white';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(labels[index], labelX, labelY - 5);
        ctx.fillText(`${Math.round((value / total) * 100)}%`, labelX, labelY + 10);
        
        currentAngle += sliceAngle;
    });
}

// Створення графіка прогнозу ваги
function createWeightChart(currentWeight, goal) {
    const canvas = document.getElementById('weightChart');
    const ctx = canvas.getContext('2d');
    
    // Очищуємо canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Параметри графіка
    const padding = 40;
    const chartWidth = canvas.width - 2 * padding;
    const chartHeight = canvas.height - 2 * padding;
    
    // Дані для 24 тижнів (6 місяців)
    const weeks = [];
    const weights = [];
    
    for (let week = 0; week <= 24; week++) {
        weeks.push(week);
        
        if (goal === 'gain') {
            weights.push(currentWeight + (week * 0.3)); // +0.3 кг/тиждень
        } else if (goal === 'lose') {
            weights.push(Math.max(currentWeight - (week * 0.4), currentWeight * 0.85)); // -0.4 кг/тиждень
        } else {
            weights.push(currentWeight + (Math.sin(week * 0.2) * 0.5)); // коливання ±0.5 кг
        }
    }
    
    // Знаходимо мін/макс для масштабування
    const minWeight = Math.min(...weights) - 2;
    const maxWeight = Math.max(...weights) + 2;
    const weightRange = maxWeight - minWeight;
    
    // Функція для перетворення координат
    const getX = (week) => padding + (week / 24) * chartWidth;
    const getY = (weight) => padding + ((maxWeight - weight) / weightRange) * chartHeight;
    
    // Сітка
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 1;
    
    // Вертикальні лінії (тижні)
    for (let week = 0; week <= 24; week += 4) {
        const x = getX(week);
        ctx.beginPath();
        ctx.moveTo(x, padding);
        ctx.lineTo(x, padding + chartHeight);
        ctx.stroke();
    }
    
    // Горизонтальні лінії (вага)
    for (let weight = Math.ceil(minWeight); weight <= Math.floor(maxWeight); weight += 2) {
        const y = getY(weight);
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(padding + chartWidth, y);
        ctx.stroke();
    }
    
    // Лінія графіка
    ctx.strokeStyle = goal === 'gain' ? '#28a745' : goal === 'lose' ? '#dc3545' : '#007bff';
    ctx.lineWidth = 3;
    ctx.beginPath();
    
    weights.forEach((weight, index) => {
        const x = getX(weeks[index]);
        const y = getY(weight);
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();
    
    // Точки
    ctx.fillStyle = ctx.strokeStyle;
    weights.forEach((weight, index) => {
        if (index % 4 === 0) { // Показуємо точки кожні 4 тижні
            const x = getX(weeks[index]);
            const y = getY(weight);
            
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, 2 * Math.PI);
            ctx.fill();
        }
    });
    
    // Підписи осей
    ctx.fillStyle = '#495057';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    
    // Підписи тижнів
    for (let week = 0; week <= 24; week += 8) {
        const x = getX(week);
        ctx.fillText(`${week}т`, x, canvas.height - 10);
    }
    
    // Підписи ваги
    ctx.textAlign = 'right';
    for (let weight = Math.ceil(minWeight); weight <= Math.floor(maxWeight); weight += 2) {
        const y = getY(weight);
        ctx.fillText(`${weight}кг`, padding - 10, y + 4);
    }
    
    // Заголовки осей
    ctx.textAlign = 'center';
    ctx.font = 'bold 14px Arial';
    ctx.fillText('Тижні', canvas.width / 2, canvas.height - 5);
    
    ctx.save();
    ctx.translate(15, canvas.height / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Вага (кг)', 0, 0);
    ctx.restore();
    
    // Анотації
    const startWeight = weights[0];
    const endWeight = weights[weights.length - 1];
    
    ctx.font = '10px Arial';
    ctx.fillStyle = '#6c757d';
    ctx.textAlign = 'left';
    ctx.fillText(`Старт: ${startWeight.toFixed(1)}кг`, padding + 5, padding + 15);
    ctx.textAlign = 'right';
    ctx.fillText(`Прогноз: ${endWeight.toFixed(1)}кг`, padding + chartWidth - 5, padding + 15);
}
```

### 5. ПОЛНОСТЬЮ ПЕРЕПИСАТЬ js/utils.js

**ИСПРАВЛЕНИЕ:** Заменить содержимое на:

```javascript
// Відображення помилки
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    
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
    if (confirm('Ви впевнені, що