// Функция для расчета базального метаболизма (BMR) по формуле Міффліна-Сан-Джеор
function calculateBMR(weight, height, age, gender) {
    if (gender === 'male') {
        return 10 * weight + 6.25 * height - 5 * age + 5;
    } else if (gender === 'female') {
        return 10 * weight + 6.25 * height - 5 * age - 161;
    } else {
        throw new Error('Неверный пол');
    }
}

// Функция для расчета потребностей в макронутриентах
function calculateMacronutrients(calories, weight, goal) {
    let protein, fat, carbs;

    if (goal === 'gain') {
        protein = weight * 2.2; // 2.2 г белка на кг массы
        fat = (calories * 0.25) / 9; // 25% калорий из жиров
        carbs = (calories - (protein * 4 + fat * 9)) / 4; // Остальные калории из углеводов
    } else if (goal === 'lose') {
        protein = weight * 2.0; // 2.0 г белка на кг массы
        fat = (calories * 0.20) / 9; // 20% калорий из жиров
        carbs = (calories - (protein * 4 + fat * 9)) / 4; // Остальные калории из углеводов
    } else {
        throw new Error('Неверная цель');
    }

    return { protein, fat, carbs };
}

// Функция для оптимизации выбора продуктов на основе макронутриентов
function optimizeProducts(products, targetMacros) {
    // Логика для оптимизации выбора продуктов
    // Возвращает список продуктов, которые соответствуют целевым макронутриентам
    return products.filter(product => {
        return product.protein >= targetMacros.protein &&
               product.fat <= targetMacros.fat &&
               product.carbs <= targetMacros.carbs;
    });
}