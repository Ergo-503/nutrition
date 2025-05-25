// src/js/core/calculator.js

export function calculateBMR(weight, height, age, gender) {
    if (gender === 'Чоловіча') {
        return 10 * weight + 6.25 * height - 5 * age + 5;
    } else {
        return 10 * weight + 6.25 * height - 5 * age - 161;
    }
}

export function calculateTDEE(bmr, activityLevel, goal) {
    const activityCoefficients = {
        'Дуже низька': 1.2,
        'Низька': 1.375,
        'Середня': 1.55,
        'Висока': 1.725,
        'Дуже висока': 1.9
    };

    const goalAdjustments = {
        'Підтримання форми': 0.0,
        'Набір маси': 0.15,
        'Скидання ваги/Сушка': -0.15
    };

    const activityCoefficient = activityCoefficients[activityLevel];
    const goalAdjustment = goalAdjustments[goal];

    return bmr * activityCoefficient * (1 + goalAdjustment);
}

export function calculateMacronutrients(tdee, weight, goal) {
    const macroRatios = {
        'Підтримання форми': { protein_per_kg: 1.8, fat_percent: 0.25 },
        'Набір маси': { protein_per_kg: 2.2, fat_percent: 0.20 },
        'Скидання ваги/Сушка': { protein_per_kg: 2.5, fat_percent: 0.30 }
    };

    const ratios = macroRatios[goal];

    const proteinGrams = weight * ratios.protein_per_kg;
    const fatCalories = tdee * ratios.fat_percent;
    const fatGrams = fatCalories / 9; // 9 kcal per gram of fat
    const remainingCalories = tdee - (proteinGrams * 4) - (fatGrams * 9);
    const carbsGrams = remainingCalories / 4; // 4 kcal per gram of carbohydrates

    return {
        protein: Math.round(proteinGrams),
        fat: Math.round(fatGrams),
        carbs: Math.round(carbsGrams)
    };
}