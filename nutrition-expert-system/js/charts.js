// Файл js/charts.js

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