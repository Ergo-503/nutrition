// This file contains functions for optimizing dietary plans based on user input and nutritional goals.

function filterProducts(products, isVegan = false, isDiabetic = false) {
    return products.filter(product => {
        if (isVegan && !product.Vegan) {
            return false;
        }
        if (isDiabetic && product.Diabet > 55 && product.Diabet !== 0) {
            return false;
        }
        return true;
    });
}

function optimizeDiet(targetCalories, targetProtein, targetFat, targetCarbs, products, isVegan = false, isDiabetic = false) {
    const filteredProducts = filterProducts(products, isVegan, isDiabetic);
    let selectedProducts = [];
    let currentCalories = 0;
    let currentProtein = 0;
    let currentFat = 0;
    let currentCarbs = 0;
    let totalCost = 0;

    // Sort products by protein efficiency
    const proteinSources = filteredProducts
        .filter(p => p.Protein > 15)
        .sort((a, b) => (b.Protein / b.Calories) - (a.Protein / a.Calories));

    for (let product of proteinSources) {
        const amount = Math.min(200, (targetProtein * 0.4) / product.Protein * 100);
        if (amount > 20) {
            const calories = (product.Calories * amount) / 100;
            const protein = (product.Protein * amount) / 100;
            const fat = (product.Fat * amount) / 100;
            const carbs = (product.Carbs * amount) / 100;
            const cost = (product.Cost * amount) / 100;

            selectedProducts.push({
                ...product,
                amount: Math.round(amount),
                actualCalories: Math.round(calories),
                actualProtein: Math.round(protein),
                actualFat: Math.round(fat),
                actualCarbs: Math.round(carbs),
                actualCost: Math.round(cost * 100) / 100
            });

            currentCalories += calories;
            currentProtein += protein;
            currentFat += fat;
            currentCarbs += carbs;
            totalCost += cost;
        }
    }

    // Add carbohydrate sources
    const carbSources = filteredProducts
        .filter(p => p.Carbs > 50 && !selectedProducts.some(s => s.Name === p.Name))
        .sort((a, b) => (b.Carbs / b.Cost) - (a.Carbs / a.Cost));

    for (let product of carbSources) {
        const neededCarbs = Math.max(0, targetCarbs - currentCarbs);
        const amount = Math.min(150, (neededCarbs * 0.6) / product.Carbs * 100);
        if (amount > 20) {
            const calories = (product.Calories * amount) / 100;
            const protein = (product.Protein * amount) / 100;
            const fat = (product.Fat * amount) / 100;
            const carbs = (product.Carbs * amount) / 100;
            const cost = (product.Cost * amount) / 100;

            selectedProducts.push({
                ...product,
                amount: Math.round(amount),
                actualCalories: Math.round(calories),
                actualProtein: Math.round(protein),
                actualFat: Math.round(fat),
                actualCarbs: Math.round(carbs),
                actualCost: Math.round(cost * 100) / 100
            });

            currentCalories += calories;
            currentProtein += protein;
            currentFat += fat;
            currentCarbs += carbs;
            totalCost += cost;
        }
    }

    // Add fat sources if needed
    if (currentFat < targetFat * 0.8) {
        const fatSources = filteredProducts
            .filter(p => p.Fat > 20 && !selectedProducts.some(s => s.Name === p.Name))
            .sort((a, b) => (b.Fat / b.Cost) - (a.Fat / a.Cost));

        if (fatSources.length > 0) {
            const product = fatSources[0];
            const neededFat = targetFat - currentFat;
            const amount = Math.min(50, (neededFat * 0.8) / product.Fat * 100);
            if (amount > 5) {
                const calories = (product.Calories * amount) / 100;
                const protein = (product.Protein * amount) / 100;
                const fat = (product.Fat * amount) / 100;
                const carbs = (product.Carbs * amount) / 100;
                const cost = (product.Cost * amount) / 100;

                selectedProducts.push({
                    ...product,
                    amount: Math.round(amount),
                    actualCalories: Math.round(calories),
                    actualProtein: Math.round(protein),
                    actualFat: Math.round(fat),
                    actualCarbs: Math.round(carbs),
                    actualCost: Math.round(cost * 100) / 100
                });

                currentCalories += calories;
                currentProtein += protein;
                currentFat += fat;
                currentCarbs += carbs;
                totalCost += cost;
            }
        }
    }

    return {
        selectedProducts,
        totalCost,
        actualNutrition: {
            calories: Math.round(currentCalories),
            protein: Math.round(currentProtein),
            fat: Math.round(currentFat),
            carbs: Math.round(currentCarbs)
        }
    };
}

export { optimizeDiet };