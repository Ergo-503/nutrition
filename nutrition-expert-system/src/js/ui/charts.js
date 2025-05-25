// This file exports functions for rendering charts using Chart.js, visualizing nutritional data and progress.

export function renderMacroChart(ctx, macroData) {
    const macroChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Білки', 'Жири', 'Вуглеводи'],
            datasets: [{
                data: [macroData.protein, macroData.fat, macroData.carbs],
                backgroundColor: ['#3498db', '#e74c3c', '#27ae60'],
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return `${tooltipItem.label}: ${tooltipItem.raw} г`;
                        }
                    }
                }
            }
        }
    });
    return macroChart;
}

export function renderWeightChart(ctx, weightData) {
    const weightChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: weightData.labels,
            datasets: [{
                label: 'Зміна ваги',
                data: weightData.values,
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.2)',
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return `Вага: ${tooltipItem.raw} кг`;
                        }
                    }
                }
            }
        }
    });
    return weightChart;
}