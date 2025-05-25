// Main entry point for the JavaScript application

import { calculateBMR, calculateTDEE, calculateMacronutrients } from './core/calculator.js';
import { optimizeDiet, filterProducts } from './core/optimizer.js';
import { validateInput } from './core/validator.js';
import { renderCharts } from './ui/charts.js';
import { handleFormSubmission } from './ui/formHandler.js';
import { renderResults } from './ui/resultsRenderer.js';
import { PRODUCTS_DATABASE } from './data/products.js';

document.addEventListener('DOMContentLoaded', () => {
    const calculateBtn = document.getElementById('calculateBtn');
    const clearBtn = document.getElementById('clearBtn');

    calculateBtn.addEventListener('click', handleFormSubmission);
    clearBtn.addEventListener('click', () => {
        document.getElementById('resultsContainer').style.display = 'none';
        // Clear input fields and results
    });

    // Initialize charts
    renderCharts();
});