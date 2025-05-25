// formHandler.js
export function collectUserInput() {
    const age = parseInt(document.getElementById('age').value);
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);
    const gender = document.getElementById('gender').value;
    const activityLevel = document.getElementById('activity').value;
    const goal = document.getElementById('goal').value;
    const isVegan = document.getElementById('vegan').checked;
    const isDiabetic = document.getElementById('diabetes').checked;

    return {
        age,
        weight,
        height,
        gender,
        activityLevel,
        goal,
        isVegan,
        isDiabetic
    };
}

export function clearForm() {
    document.getElementById('age').value = '';
    document.getElementById('weight').value = '';
    document.getElementById('height').value = '';
    document.getElementById('gender').selectedIndex = 0;
    document.getElementById('activity').selectedIndex = 2; // Default to 'Середня'
    document.getElementById('goal').selectedIndex = 0; // Default to 'Підтримання форми'
    document.getElementById('vegan').checked = false;
    document.getElementById('diabetes').checked = false;
}

export function setupFormHandlers(calculateCallback, clearCallback) {
    document.getElementById('calculateBtn').addEventListener('click', (event) => {
        event.preventDefault();
        const userInput = collectUserInput();
        calculateCallback(userInput);
    });

    document.getElementById('clearBtn').addEventListener('click', (event) => {
        event.preventDefault();
        clearForm();
        clearCallback();
    });
}