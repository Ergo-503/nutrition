// resultsRenderer.js

export function displayNutritionalNeeds(nutritionalNeeds) {
    const needsText = `
🔥 Калорії: ${Math.round(nutritionalNeeds.tdee)} ккал/день
🥩 Білки: ${nutritionalNeeds.macros.protein} г (${(nutritionalNeeds.macros.protein * 4 / nutritionalNeeds.tdee * 100).toFixed(1)}%)
🥑 Жири: ${nutritionalNeeds.macros.fat} г (${(nutritionalNeeds.macros.fat * 9 / nutritionalNeeds.tdee * 100).toFixed(1)}%)
🍞 Вуглеводи: ${nutritionalNeeds.macros.carbs} г (${(nutritionalNeeds.macros.carbs * 4 / nutritionalNeeds.tdee * 100).toFixed(1)}%)

📈 BMR: ${Math.round(nutritionalNeeds.bmr)} ккал
⚡ TDEE: ${Math.round(nutritionalNeeds.tdee)} ккал
🎯 Мета: ${nutritionalNeeds.userData.goal}`;

    document.getElementById('nutritionalNeeds').textContent = needsText;
}

export function displayProducts(products) {
    let productsText = "📋 СПИСОК ПРОДУКТІВ:\n";
    products.forEach(product => {
        productsText += `${product.amount} г ${product.Name} (Калорії: ${product.actualCalories}, Білки: ${product.actualProtein}, Жири: ${product.actualFat}, Вуглеводи: ${product.actualCarbs})\n`;
    });
    document.getElementById('productsList').textContent = productsText;
}

export function displayExplanation(explanation) {
    document.getElementById('explanation').textContent = explanation;
}

export function displayCharts(macroData, weightData) {
    const macroChartCtx = document.getElementById('macroChart').getContext('2d');
    const weightChartCtx = document.getElementById('weightChart').getContext('2d');

    new Chart(macroChartCtx, {
        type: 'pie',
        data: {
            labels: ['Білки', 'Жири', 'Вуглеводи'],
            datasets: [{
                data: [macroData.protein, macroData.fat, macroData.carbs],
                backgroundColor: ['#3498db', '#e74c3c', '#27ae60']
            }]
        }
    });

    new Chart(weightChartCtx, {
        type: 'line',
        data: {
            labels: weightData.labels,
            datasets: [{
                label: 'Прогноз зміни ваги',
                data: weightData.values,
                borderColor: '#3498db',
                fill: false
            }]
        }
    });
}