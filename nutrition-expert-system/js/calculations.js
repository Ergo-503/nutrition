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