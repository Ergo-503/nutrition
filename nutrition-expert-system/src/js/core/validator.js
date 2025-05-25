function validateAge(age) {
    if (age < 16 || age > 80) {
        return { valid: false, message: "Вік повинен бути між 16 і 80 роками." };
    }
    return { valid: true };
}

function validateWeight(weight) {
    if (weight < 40 || weight > 200) {
        return { valid: false, message: "Вага повинна бути між 40 і 200 кг." };
    }
    return { valid: true };
}

function validateHeight(height) {
    if (height < 140 || height > 220) {
        return { valid: false, message: "Зріст повинен бути між 140 і 220 см." };
    }
    return { valid: true };
}

function validateInput(age, weight, height) {
    const ageValidation = validateAge(age);
    const weightValidation = validateWeight(weight);
    const heightValidation = validateHeight(height);

    if (!ageValidation.valid) {
        return ageValidation;
    }
    if (!weightValidation.valid) {
        return weightValidation;
    }
    if (!heightValidation.valid) {
        return heightValidation;
    }
    return { valid: true };
}

export { validateInput };