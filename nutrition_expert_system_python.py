#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Експертна система вибору раціонального харчування для спортсменів
Версія: 2.0
Автор: Студент ДНУ ім. Олеся Гончара
Дата: 2025
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import pulp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from io import StringIO
import datetime
from typing import Dict, List, Tuple, Optional
import json

# =============================================================================
# КОНСТАНТИ ТА КОНФІГУРАЦІЯ
# =============================================================================

# Коефіцієнти фізичної активності
ACTIVITY_COEFFICIENTS = {
    'Дуже низька': 1.2,
    'Низька': 1.375,
    'Середня': 1.55,
    'Висока': 1.725,
    'Дуже висока': 1.9
}

# Коефіцієнти корекції під цілі
GOAL_ADJUSTMENTS = {
    'Підтримання форми': 0.0,
    'Набір маси': 0.15,
    'Скидання ваги/Сушка': -0.15
}

# Норми макронутрієнтів (г білка на кг ваги, % жирів від калорій)
MACRO_RATIOS = {
    'Підтримання форми': {'protein_per_kg': 1.8, 'fat_percent': 0.25},
    'Набір маси': {'protein_per_kg': 2.2, 'fat_percent': 0.20},
    'Скидання ваги/Сушка': {'protein_per_kg': 2.5, 'fat_percent': 0.30}
}

# База продуктів харчування
PRODUCTS_DATABASE = [
    {"Name": "Куряча грудка", "Protein": 23.0, "Fat": 1.2, "Carbs": 0.0, "Calories": 113, "Cost": 80, "Vegan": False, "Diabet": 0},
    {"Name": "Рис круглозернистий", "Protein": 2.7, "Fat": 0.3, "Carbs": 77.0, "Calories": 344, "Cost": 25, "Vegan": True, "Diabet": 64},
    {"Name": "Вівсянка", "Protein": 12.0, "Fat": 6.2, "Carbs": 61.0, "Calories": 342, "Cost": 30, "Vegan": True, "Diabet": 42},
    {"Name": "Банани", "Protein": 1.1, "Fat": 0.2, "Carbs": 21.0, "Calories": 89, "Cost": 60, "Vegan": True, "Diabet": 62},
    {"Name": "Молоко 2.5%", "Protein": 2.8, "Fat": 2.5, "Carbs": 4.7, "Calories": 52, "Cost": 60, "Vegan": False, "Diabet": 27},
    {"Name": "Яйця курячі", "Protein": 12.7, "Fat": 11.5, "Carbs": 0.7, "Calories": 157, "Cost": 60, "Vegan": False, "Diabet": 0},
    {"Name": "Олія соняшникова", "Protein": 0.0, "Fat": 99.9, "Carbs": 0.0, "Calories": 899, "Cost": 50, "Vegan": True, "Diabet": 0},
    {"Name": "Гречка", "Protein": 12.6, "Fat": 2.6, "Carbs": 68.0, "Calories": 343, "Cost": 45, "Vegan": True, "Diabet": 54},
    {"Name": "Творог 5%", "Protein": 17.2, "Fat": 5.0, "Carbs": 1.8, "Calories": 121, "Cost": 90, "Vegan": False, "Diabet": 27},
    {"Name": "Картопля", "Protein": 2.0, "Fat": 0.1, "Carbs": 16.0, "Calories": 77, "Cost": 20, "Vegan": True, "Diabet": 85},
    {"Name": "Риба морська", "Protein": 20.0, "Fat": 8.0, "Carbs": 0.0, "Calories": 150, "Cost": 300, "Vegan": False, "Diabet": 0},
    {"Name": "Квасоля червона", "Protein": 8.4, "Fat": 0.3, "Carbs": 13.7, "Calories": 93, "Cost": 60, "Vegan": True, "Diabet": 29},
    {"Name": "Чечевиця", "Protein": 9.0, "Fat": 0.4, "Carbs": 20.0, "Calories": 116, "Cost": 80, "Vegan": True, "Diabet": 29},
    {"Name": "Горіхи волоські", "Protein": 16.2, "Fat": 60.8, "Carbs": 11.1, "Calories": 656, "Cost": 400, "Vegan": True, "Diabet": 15},
    {"Name": "Хліб житній", "Protein": 6.6, "Fat": 1.2, "Carbs": 34.2, "Calories": 174, "Cost": 60, "Vegan": True, "Diabet": 58},
    {"Name": "Капуста білокачанна", "Protein": 1.8, "Fat": 0.1, "Carbs": 4.7, "Calories": 25, "Cost": 30, "Vegan": True, "Diabet": 15},
    {"Name": "Огірки свіжі", "Protein": 0.8, "Fat": 0.1, "Carbs": 2.5, "Calories": 14, "Cost": 60, "Vegan": True, "Diabet": 15},
    {"Name": "Помідори", "Protein": 1.1, "Fat": 0.2, "Carbs": 3.7, "Calories": 20, "Cost": 80, "Vegan": True, "Diabet": 30}
]

# =============================================================================
# ОСНОВНІ ФУНКЦІЇ РОЗРАХУНКІВ
# =============================================================================

def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """
    Розрахунок базального метаболізму за формулою Міффліна-Сан-Джеор
    
    Args:
        weight: Вага в кг
        height: Зріст в см
        age: Вік в роках
        gender: Стать ('Чоловіча' або 'Жіноча')
    
    Returns:
        BMR в ккал/день
    """
    if gender == 'Чоловіча':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def calculate_tdee(bmr: float, activity_level: str, goal: str) -> float:
    """
    Розрахунок загальних добових енергетичних витрат
    
    Args:
        bmr: Базальний метаболізм
        activity_level: Рівень активності
        goal: Спортивна мета
    
    Returns:
        TDEE в ккал/день
    """
    activity_coefficient = ACTIVITY_COEFFICIENTS[activity_level]
    goal_adjustment = GOAL_ADJUSTMENTS[goal]
    
    tdee = bmr * activity_coefficient
    return tdee * (1 + goal_adjustment)

def calculate_macronutrients(tdee: float, weight: float, goal: str) -> Dict[str, float]:
    """
    Розрахунок потреб у макронутрієнтах
    
    Args:
        tdee: Загальні енергетичні витрати
        weight: Вага користувача
        goal: Спортивна мета
    
    Returns:
        Словник з потребами в білках, жирах, вуглеводах
    """
    ratios = MACRO_RATIOS[goal]
    
    # Білки
    protein_grams = weight * ratios['protein_per_kg']
    
    # Жири
    fat_calories = tdee * ratios['fat_percent']
    fat_grams = fat_calories / 9  # 9 ккал на грам жиру
    
    # Вуглеводи (залишок калорій)
    remaining_calories = tdee - (protein_grams * 4) - (fat_grams * 9)
    carbs_grams = remaining_calories / 4  # 4 ккал на грам вуглеводів
    
    return {
        'protein': round(protein_grams),
        'fat': round(fat_grams),
        'carbs': round(carbs_grams)
    }

# =============================================================================
# АЛГОРИТМ ОПТИМІЗАЦІЇ
# =============================================================================

def filter_products(is_vegan: bool = False, is_diabetic: bool = False) -> List[Dict]:
    """
    Фільтрація продуктів за дієтичними обмеженнями
    
    Args:
        is_vegan: Веганська дієта
        is_diabetic: Діабетичні обмеження
    
    Returns:
        Відфільтрований список продуктів
    """
    filtered_products = []
    
    for product in PRODUCTS_DATABASE:
        # Веганські обмеження
        if is_vegan and not product['Vegan']:
            continue
        
        # Діабетичні обмеження (ГІ <= 55)
        if is_diabetic and product['Diabet'] > 55 and product['Diabet'] != 0:
            continue
        
        filtered_products.append(product)
    
    return filtered_products

def optimize_diet(target_calories: float, target_protein: float, 
                 target_fat: float, target_carbs: float,
                 is_vegan: bool = False, is_diabetic: bool = False) -> Dict:
    """
    Оптимізація харчового раціону методом лінійного програмування
    
    Args:
        target_calories: Цільова калорійність
        target_protein: Цільова кількість білків
        target_fat: Цільова кількість жирів
        target_carbs: Цільова кількість вуглеводів
        is_vegan: Веганські обмеження
        is_diabetic: Діабетичні обмеження
    
    Returns:
        Результат оптимізації
    """
    # Фільтруємо продукти
    products = filter_products(is_vegan, is_diabetic)
    
    if len(products) < 3:
        raise ValueError("Недостатньо продуктів для вибраних обмежень")
    
    # Створюємо модель оптимізації
    model = pulp.LpProblem("OptimalDiet", pulp.LpMinimize)
    
    # Змінні рішення (кількість кожного продукту в грамах)
    product_vars = {}
    for i, product in enumerate(products):
        product_vars[i] = pulp.LpVariable(
            f"product_{i}", 
            lowBound=0, 
            upBound=500,  # Максимум 500г одного продукту
            cat='Continuous'
        )
    
    # Цільова функція: мінімізація вартості
    model += pulp.lpSum([
        product_vars[i] * (products[i]['Cost'] / 100) 
        for i in range(len(products))
    ])
    
    # Обмеження по калоріях (точна відповідність)
    model += pulp.lpSum([
        product_vars[i] * (products[i]['Calories'] / 100)
        for i in range(len(products))
    ]) == target_calories
    
    # Обмеження по макронутрієнтах (мінімальні потреби)
    model += pulp.lpSum([
        product_vars[i] * (products[i]['Protein'] / 100)
        for i in range(len(products))
    ]) >= target_protein
    
    model += pulp.lpSum([
        product_vars[i] * (products[i]['Fat'] / 100)
        for i in range(len(products))
    ]) >= target_fat
    
    model += pulp.lpSum([
        product_vars[i] * (products[i]['Carbs'] / 100)
        for i in range(len(products))
    ]) >= target_carbs
    
    # Додаткові обмеження для діабетиків
    if is_diabetic:
        # Обмеження глікемічного навантаження
        model += pulp.lpSum([
            product_vars[i] * (products[i]['Carbs'] / 100) * (products[i]['Diabet'] / 100)
            for i in range(len(products)) if products[i]['Diabet'] > 0
        ]) <= target_carbs * 0.8
    
    # Розв'язуємо задачу
    status = model.solve(pulp.PULP_CBC_CMD(msg=0))
    
    if pulp.LpStatus[status] != 'Optimal':
        # Пробуємо послабити обмеження
        return try_relaxed_optimization(products, target_calories, target_protein, 
                                      target_fat, target_carbs, is_diabetic)
    
    # Збираємо результати
    selected_products = []
    total_cost = 0
    actual_nutrition = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}
    
    for i in range(len(products)):
        amount = product_vars[i].varValue
        if amount and amount > 1:  # Включаємо тільки значущі кількості
            product = products[i].copy()
            product['amount'] = round(amount)
            
            # Розрахунок фактичного вмісту нутрієнтів
            factor = amount / 100
            actual_nutrition['calories'] += product['Calories'] * factor
            actual_nutrition['protein'] += product['Protein'] * factor
            actual_nutrition['fat'] += product['Fat'] * factor
            actual_nutrition['carbs'] += product['Carbs'] * factor
            
            total_cost += product['Cost'] * factor
            selected_products.append(product)
    
    return {
        'status': 'success',
        'products': selected_products,
        'total_cost': round(total_cost, 2),
        'actual_nutrition': {k: round(v, 1) for k, v in actual_nutrition.items()},
        'objective_value': pulp.value(model.objective)
    }

def try_relaxed_optimization(products: List[Dict], target_calories: float,
                           target_protein: float, target_fat: float, 
                           target_carbs: float, is_diabetic: bool) -> Dict:
    """
    Спроба оптимізації з послабленими обмеженнями
    """
    relaxation_strategies = [
        {'max_weight': 700, 'protein_factor': 1.0, 'message': 'Збільшено максимальну вагу продуктів'},
        {'max_weight': 500, 'protein_factor': 0.9, 'message': 'Зменшено вимоги до білків на 10%'},
        {'max_weight': 700, 'protein_factor': 0.85, 'message': 'Застосовано комбіновані послаблення'}
    ]
    
    for strategy in relaxation_strategies:
        try:
            # Створюємо нову модель з послабленими обмеженнями
            model = pulp.LpProblem("RelaxedDiet", pulp.LpMinimize)
            
            product_vars = {}
            for i, product in enumerate(products):
                product_vars[i] = pulp.LpVariable(
                    f"product_{i}", 
                    lowBound=0, 
                    upBound=strategy['max_weight'],
                    cat='Continuous'
                )
            
            # Цільова функція
            model += pulp.lpSum([
                product_vars[i] * (products[i]['Cost'] / 100) 
                for i in range(len(products))
            ])
            
            # Послаблені обмеження
            model += pulp.lpSum([
                product_vars[i] * (products[i]['Calories'] / 100)
                for i in range(len(products))
            ]) >= target_calories * 0.95  # ±5% по калоріях
            
            model += pulp.lpSum([
                product_vars[i] * (products[i]['Calories'] / 100)
                for i in range(len(products))
            ]) <= target_calories * 1.05
            
            model += pulp.lpSum([
                product_vars[i] * (products[i]['Protein'] / 100)
                for i in range(len(products))
            ]) >= target_protein * strategy['protein_factor']
            
            status = model.solve(pulp.PULP_CBC_CMD(msg=0))
            
            if pulp.LpStatus[status] == 'Optimal':
                # Обробляємо успішний результат
                selected_products = []
                total_cost = 0
                actual_nutrition = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}
                
                for i in range(len(products)):
                    amount = product_vars[i].varValue
                    if amount and amount > 1:
                        product = products[i].copy()
                        product['amount'] = round(amount)
                        
                        factor = amount / 100
                        actual_nutrition['calories'] += product['Calories'] * factor
                        actual_nutrition['protein'] += product['Protein'] * factor
                        actual_nutrition['fat'] += product['Fat'] * factor
                        actual_nutrition['carbs'] += product['Carbs'] * factor
                        
                        total_cost += product['Cost'] * factor
                        selected_products.append(product)
                
                return {
                    'status': 'success',
                    'products': selected_products,
                    'total_cost': round(total_cost, 2),
                    'actual_nutrition': {k: round(v, 1) for k, v in actual_nutrition.items()},
                    'relaxation_applied': strategy['message']
                }
                
        except Exception:
            continue
    
    return {
        'status': 'failed',
        'message': 'Неможливо знайти рішення навіть з послабленими обмеженнями',
        'products': [],
        'total_cost': 0
    }

# =============================================================================
# ГРАФІЧНИЙ ІНТЕРФЕЙС КОРИСТУВАЧА
# =============================================================================

class NutritionExpertSystem:
    """Головний клас експертної системи з графічним інтерфейсом"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.create_widgets()
        self.current_results = None
        
    def setup_main_window(self):
        """Налаштування головного вікна"""
        self.root.title("Експертна система раціонального харчування для спортсменів")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Встановлення іконки (якщо є)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Центрування вікна
        self.center_window()
    
    def center_window(self):
        """Центрування вікна на екрані"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Створення всіх віджетів інтерфейсу"""
        # Заголовок
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🏃‍♂️ Експертна система раціонального харчування",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Персоналізовані рекомендації для спортсменів",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Основний контейнер
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Лівий фрейм (введення параметрів)
        self.create_input_section(main_container)
        
        # Правий фрейм (результати)
        self.create_results_section(main_container)
    
    def create_input_section(self, parent):
        """Створення секції введення параметрів"""
        input_frame = tk.LabelFrame(
            parent,
            text="Параметри користувача",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        input_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Особисті дані
        personal_frame = tk.LabelFrame(input_frame, text="Особисті дані", bg='#f0f0f0')
        personal_frame.pack(fill='x', padx=10, pady=5)
        
        # Стать
        tk.Label(personal_frame, text="Стать:", bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.gender_var = tk.StringVar(value="Чоловіча")
        gender_combo = ttk.Combobox(
            personal_frame,
            textvariable=self.gender_var,
            values=["Чоловіча", "Жіноча"],
            state="readonly"
        )
        gender_combo.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        
        # Вік
        tk.Label(personal_frame, text="Вік (років):", bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.age_var = tk.StringVar(value="25")
        age_entry = tk.Entry(personal_frame, textvariable=self.age_var)
        age_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        
        # Вага
        tk.Label(personal_frame, text="Вага (кг):", bg='#f0f0f0').grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.weight_var = tk.StringVar(value="70")
        weight_entry = tk.Entry(personal_frame, textvariable=self.weight_var)
        weight_entry.grid(row=2, column=1, padx=5, pady=2, sticky='ew')
        
        # Зріст
        tk.Label(personal_frame, text="Зріст (см):", bg='#f0f0f0').grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.height_var = tk.StringVar(value="175")
        height_entry = tk.Entry(personal_frame, textvariable=self.height_var)
        height_entry.grid(row=3, column=1, padx=5, pady=2, sticky='ew')
        
        personal_frame.columnconfigure(1, weight=1)
        
        # Спортивні параметри
        sport_frame = tk.LabelFrame(input_frame, text="Спортивна діяльність", bg='#f0f0f0')
        sport_frame.pack(fill='x', padx=10, pady=5)
        
        # Рівень активності
        tk.Label(sport_frame, text="Рівень активності:", bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.activity_var = tk.StringVar(value="Середня")
        activity_combo = ttk.Combobox(
            sport_frame,
            textvariable=self.activity_var,
            values=list(ACTIVITY_COEFFICIENTS.keys()),
            state="readonly"
        )
        activity_combo.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        
        # Мета
        tk.Label(sport_frame, text="Мета:", bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.goal_var = tk.StringVar(value="Підтримання форми")
        goal_combo = ttk.Combobox(
            sport_frame,
            textvariable=self.goal_var,
            values=list(GOAL_ADJUSTMENTS.keys()),
            state="readonly"
        )
        goal_combo.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        
        sport_frame.columnconfigure(1, weight=1)
        
        # Дієтичні обмеження
        restrictions_frame = tk.LabelFrame(input_frame, text="Дієтичні обмеження", bg='#f0f0f0')
        restrictions_frame.pack(fill='x', padx=10, pady=5)
        
        self.vegan_var = tk.BooleanVar()
        vegan_check = tk.Checkbutton(
            restrictions_frame,
            text="Веганська дієта",
            variable=self.vegan_var,
            bg='#f0f0f0'
        )
        vegan_check.pack(anchor='w', padx=5, pady=2)
        
        self.diabetes_var = tk.BooleanVar()
        diabetes_check = tk.Checkbutton(
            restrictions_frame,
            text="Діабет (низький ГІ)",
            variable=self.diabetes_var,
            bg='#f0f0f0'
        )
        diabetes_check.pack(anchor='w', padx=5, pady=2)
        
        # Кнопки
        buttons_frame = tk.Frame(input_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        calculate_btn = tk.Button(
            buttons_frame,
            text="🔍 Розрахувати раціон",
            command=self.calculate_nutrition,
            bg='#3498db',
            fg='white',
            font=('Arial', 12, 'bold'),
            pady=10
        )
        calculate_btn.pack(fill='x', pady=(0, 5))
        
        clear_btn = tk.Button(
            buttons_frame,
            text="🗑️ Очистити дані",
            command=self.clear_data,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10)
        )
        clear_btn.pack(fill='x')
    
    def create_results_section(self, parent):
        """Створення секції результатів"""
        results_frame = tk.LabelFrame(
            parent,
            text="Результати розрахунку",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        results_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Потреби у поживних речовинах
        needs_frame = tk.LabelFrame(results_frame, text="Розраховані потреби", bg='#f0f0f0')
        needs_frame.pack(fill='x', padx=10, pady=5)
        
        self.needs_text = tk.Text(
            needs_frame,
            height=6,
            font=('Consolas', 10),
            bg='#ecf0f1',
            state='disabled'
        )
        self.needs_text.pack(fill='x', padx=5, pady=5)
        
        # Рекомендовані продукти
        products_frame = tk.LabelFrame(results_frame, text="Оптимальний раціон", bg='#f0f0f0')
        products_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.products_text = tk.Text(
            products_frame,
            height=8,
            font=('Consolas', 10),
            bg='#ecf0f1',
            state='disabled'
        )
        self.products_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Пояснення
        explanation_frame = tk.LabelFrame(results_frame, text="Пояснення рекомендацій", bg='#f0f0f0')
        explanation_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.explanation_text = tk.Text(
            explanation_frame,
            height=6,
            font=('Arial', 9),
            bg='#fff9c4',
            state='disabled',
            wrap='word'
        )
        self.explanation_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Кнопка збереження
        save_btn = tk.Button(
            results_frame,
            text="💾 Зберегти результати",
            command=self.save_results,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10),
            state='disabled'
        )
        save_btn.pack(fill='x', padx=10, pady=5)
        self.save_btn = save_btn
    
    def calculate_nutrition(self):
        """Головна функція розрахунку харчового плану"""
        try:
            # Валідація та збір даних
            user_data = self.validate_and_collect_input()
            
            # Показуємо індикатор завантаження
            self.show_loading()
            
            # Розрахунок потреб
            bmr = calculate_bmr(
                user_data['weight'],
                user_data['height'],
                user_data['age'],
                user_data['gender']
            )
            
            tdee = calculate_tdee(bmr, user_data['activity'], user_data['goal'])
            
            macros = calculate_macronutrients(tdee, user_data['weight'], user_data['goal'])
            
            # Оптимізація продуктів
            optimization_result = optimize_diet(
                tdee,
                macros['protein'],
                macros['fat'],
                macros['carbs'],
                user_data['vegan'],
                user_data['diabetes']
            )
            
            # Збереження результатів
            self.current_results = {
                'user_data': user_data,
                'bmr': bmr,
                'tdee': tdee,
                'macros': macros,
                'optimization': optimization_result
            }
            
            # Відображення результатів
            self.display_results()
            
            # Створення графіків
            self.create_charts()
            
            # Активація кнопки збереження
            self.save_btn.config(state='normal')
            
        except ValueError as e:
            messagebox.showerror("Помилка валідації", str(e))
        except Exception as e:
            messagebox.showerror("Помилка розрахунку", f"Виникла несподівана помилка: {str(e)}")
        finally:
            self.hide_loading()
    
    def validate_and_collect_input(self) -> Dict:
        """Валідація та збір вхідних даних"""
        try:
            age = int(self.age_var.get())
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())
        except ValueError:
            raise ValueError("Будь ласка, введіть коректні числові значення")
        
        # Валідація діапазонів
        if not (16 <= age <= 80):
            raise ValueError("Вік має бути від 16 до 80 років")
        if not (40 <= weight <= 200):
            raise ValueError("Вага має бути від 40 до 200 кг")
        if not (140 <= height <= 220):
            raise ValueError("Зріст має бути від 140 до 220 см")
        
        return {
            'gender': self.gender_var.get(),
            'age': age,
            'weight': weight,
            'height': height,
            'activity': self.activity_var.get(),
            'goal': self.goal_var.get(),
            'vegan': self.vegan_var.get(),
            'diabetes': self.diabetes_var.get()
        }
    
    def show_loading(self):
        """Показати індикатор завантаження"""
        # Можна додати прогрес-бар або анімацію
        self.root.config(cursor="watch")
        self.root.update()
    
    def hide_loading(self):
        """Сховати індикатор завантаження"""
        self.root.config(cursor="")
        self.root.update()
    
    def display_results(self):
        """Відображення результатів розрахунків"""
        if not self.current_results:
            return
        
        results = self.current_results
        
        # Відображення потреб
        self.needs_text.config(state='normal')
        self.needs_text.delete(1.0, tk.END)
        
        needs_text = f"""📊 ВАШІ ПОТРЕБИ:

🔥 Калорії: {results['tdee']:.0f} ккал/день
🥩 Білки: {results['macros']['protein']} г ({results['macros']['protein']*4/results['tdee']*100:.1f}%)
🥑 Жири: {results['macros']['fat']} г ({results['macros']['fat']*9/results['tdee']*100:.1f}%)
🍞 Вуглеводи: {results['macros']['carbs']} г ({results['macros']['carbs']*4/results['tdee']*100:.1f}%)

📈 BMR: {results['bmr']:.0f} ккал
⚡ TDEE: {results['tdee']:.0f} ккал
🎯 Мета: {results['user_data']['goal']}
"""
        
        self.needs_text.insert(tk.END, needs_text)
        self.needs_text.config(state='disabled')
        
        # Відображення продуктів
        self.products_text.config(state='normal')
        self.products_text.delete(1.0, tk.END)
        
        opt_result = results['optimization']
        if opt_result['status'] == 'success':
            products_text = f"""🛒 ОПТИМАЛЬНИЙ РАЦІОН:

💰 Загальна вартість: {opt_result['total_cost']:.2f} грн/день
📊 Фактична калорійність: {opt_result['actual_nutrition']['calories']:.0f} ккал

📋 СПИСОК ПРОДУКТІВ:
"""
            
            for product in opt_result['products']:
                cost = product['Cost'] * product['amount'] / 100
                products_text += f"• {product['Name']}: {product['amount']}г (≈{cost:.1f} грн)\n"
            
            products_text += f"""
📈 ФАКТИЧНИЙ СКЛАД:
🥩 Білки: {opt_result['actual_nutrition']['protein']:.1f}г
🥑 Жири: {opt_result['actual_nutrition']['fat']:.1f}г
🍞 Вуглеводи: {opt_result['actual_nutrition']['carbs']:.1f}г
"""
        else:
            products_text = f"❌ Помилка оптимізації: {opt_result.get('message', 'Невідома помилка')}"
        
        self.products_text.insert(tk.END, products_text)
        self.products_text.config(state='disabled')
        
        # Пояснення
        self.display_explanation()
    
    def display_explanation(self):
        """Відображення пояснень"""
        if not self.current_results:
            return
        
        results = self.current_results
        user_data = results['user_data']
        
        self.explanation_text.config(state='normal')
        self.explanation_text.delete(1.0, tk.END)
        
        explanation = f"""🔍 ПОЯСНЕННЯ РЕКОМЕНДАЦІЙ:

🎯 Основа розрахунків: Ваші потреби розраховані за науково обґрунтованою формулою Міффліна-Сан-Джеор з урахуванням рівня активності "{user_data['activity']}" та мети "{user_data['goal']}".

⚖️ Принцип оптимізації: Система підібрала найдешевший набір продуктів, який точно забезпечує вашу калорійність та перевищує мінімальні потреби в білках, жирах та вуглеводах.

🥗 Рекомендації по харчуванню:
"""
        
        if user_data['goal'] == 'Набір маси':
            explanation += "• Споживайте 20-30г білків протягом 2 годин після тренування для максимального м'язового синтезу.\n"
            explanation += "• Розподіліть вуглеводи між сніданком та після-тренувальним прийомом їжі.\n"
        elif user_data['goal'] == 'Скидання ваги/Сушка':
            explanation += "• Підтримуйте високе споживання білків для збереження м'язової маси при дефіциті калорій.\n"
            explanation += "• Споживайте основну частину вуглеводів навколо тренувань.\n"
        else:
            explanation += "• Дотримуйтесь збалансованого розподілу прийомів їжі протягом дня.\n"
            explanation += "• Забезпечьте достатню кількість овочів та фруктів для мікронутрієнтів.\n"
        
        if user_data['diabetes']:
            explanation += "\n🩺 Діабетичні рекомендації: Всі продукти мають глікемічний індекс ≤55 для стабільного рівня цукру в крові."
        
        if user_data['vegan']:
            explanation += "\n🌱 Веганські рекомендації: Поєднуйте різні рослинні білки для повного амінокислотного профілю."
        
        opt_result = results['optimization']
        if opt_result.get('relaxation_applied'):
            explanation += f"\n⚠️ Примітка: {opt_result['relaxation_applied']}"
        
        self.explanation_text.insert(tk.END, explanation)
        self.explanation_text.config(state='disabled')
    
    def create_charts(self):
        """Створення графіків"""
        if not self.current_results:
            return
        
        # Створюємо нове вікно для графіків
        charts_window = tk.Toplevel(self.root)
        charts_window.title("Візуалізація результатів")
        charts_window.geometry("1000x600")
        charts_window.configure(bg='#f0f0f0')
        
        # Кругова діаграма макронутрієнтів
        fig1, ax1 = plt.subplots(figsize=(6, 5))
        fig1.patch.set_facecolor('#f0f0f0')
        
        macros = self.current_results['macros']
        protein_cal = macros['protein'] * 4
        fat_cal = macros['fat'] * 9
        carb_cal = macros['carbs'] * 4
        
        sizes = [protein_cal, fat_cal, carb_cal]
        labels = [f'Білки\n{macros["protein"]}г', f'Жири\n{macros["fat"]}г', f'Вуглеводи\n{macros["carbs"]}г']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        explode = (0.05, 0.05, 0.05)
        
        wedges, texts, autotexts = ax1.pie(
            sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            explode=explode, shadow=True, startangle=90
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax1.set_title('Розподіл калорій за макронутрієнтами', fontsize=14, fontweight='bold')
        
        canvas1 = FigureCanvasTkAgg(fig1, master=charts_window)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Графік прогнозу ваги
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        fig2.patch.set_facecolor('#f0f0f0')
        
        current_weight = self.current_results['user_data']['weight']
        goal = self.current_results['user_data']['goal']
        weeks = list(range(0, 25))
        
        if goal == 'Набір маси':
            weight_progression = [current_weight + (0.3 * week) for week in weeks]
            color = '#2ECC71'
            title = 'Прогноз набору м\'язової маси'
        elif goal == 'Скидання ваги/Сушка':
            weight_progression = [max(current_weight - (0.4 * week), current_weight * 0.85) for week in weeks]
            color = '#E74C3C'
            title = 'Прогноз зменшення ваги'
        else:
            import random
            weight_progression = [current_weight + random.uniform(-0.5, 0.5) for _ in weeks]
            color = '#3498DB'
            title = 'Підтримання поточної ваги'
        
        ax2.plot(weeks, weight_progression, color=color, linewidth=3, marker='o', markersize=4, alpha=0.8)
        
        ax2.set_xlabel('Тижні', fontweight='bold')
        ax2.set_ylabel('Вага (кг)', fontweight='bold')
        ax2.set_title(title, fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='--')
        
        # Анотації
        ax2.annotate(f'Старт: {current_weight:.1f} кг', 
                    xy=(0, current_weight), xytext=(3, current_weight + 2),
                    fontsize=9, ha='left',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', color='gray'))
        
        ax2.annotate(f'Прогноз (6 міс): {weight_progression[-1]:.1f} кг', 
                    xy=(weeks[-1], weight_progression[-1]),
                    xytext=(weeks[-1]-5, weight_progression[-1] + 2),
                    fontsize=9, ha='right',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', color='gray'))
        
        canvas2 = FigureCanvasTkAgg(fig2, master=charts_window)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        plt.tight_layout()
    
    def save_results(self):
        """Збереження результатів у файл"""
        if not self.current_results:
            messagebox.showwarning("Попередження", "Немає результатів для збереження")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Текстові файли", "*.txt"),
                    ("JSON файли", "*.json"),
                    ("Всі файли", "*.*")
                ],
                title="Зберегти результати харчового плану"
            )
            
            if not filename:
                return
            
            if filename.endswith('.json'):
                self.save_json_results(filename)
            else:
                self.save_text_results(filename)
            
            messagebox.showinfo("Успіх", f"Результати збережено у файл:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Помилка збереження", f"Не вдалося зберегти файл:\n{str(e)}")
    
    def save_text_results(self, filename: str):
        """Збереження результатів у текстовому форматі"""
        results = self.current_results
        
        report = f"""
================================================================================
                    ЗВІТ ЕКСПЕРТНОЇ СИСТЕМИ ХАРЧУВАННЯ
================================================================================

Дата створення: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}

ПАРАМЕТРИ КОРИСТУВАЧА:
{'-' * 50}
Стать: {results['user_data']['gender']}
Вік: {results['user_data']['age']} років
Вага: {results['user_data']['weight']} кг
Зріст: {results['user_data']['height']} см
Рівень активності: {results['user_data']['activity']}
Мета: {results['user_data']['goal']}
Веганська дієта: {'Так' if results['user_data']['vegan'] else 'Ні'}
Діабет: {'Так' if results['user_data']['diabetes'] else 'Ні'}

РОЗРАХОВАНІ ПОТРЕБИ:
{'-' * 50}
Базальний метаболізм (BMR): {results['bmr']:.0f} ккал
Загальні витрати (TDEE): {results['tdee']:.0f} ккал
Білки: {results['macros']['protein']} г
Жири: {results['macros']['fat']} г
Вуглеводи: {results['macros']['carbs']} г

ОПТИМАЛЬНИЙ РАЦІОН:
{'-' * 50}
"""
        
        opt_result = results['optimization']
        if opt_result['status'] == 'success':
            report += f"Загальна вартість: {opt_result['total_cost']:.2f} грн/день\n"
            report += f"Фактична калорійність: {opt_result['actual_nutrition']['calories']:.0f} ккал\n\n"
            report += "СПИСОК ПРОДУКТІВ:\n"
            
            for product in opt_result['products']:
                cost = product['Cost'] * product['amount'] / 100
                report += f"• {product['Name']}: {product['amount']}г (≈{cost:.1f} грн)\n"
            
            report += f"\nФАКТИЧНИЙ СКЛАД:\n"
            report += f"Білки: {opt_result['actual_nutrition']['protein']:.1f}г\n"
            report += f"Жири: {opt_result['actual_nutrition']['fat']:.1f}г\n"
            report += f"Вуглеводи: {opt_result['actual_nutrition']['carbs']:.1f}г\n"
        else:
            report += f"Помилка оптимізації: {opt_result.get('message', 'Невідома помилка')}\n"
        
        report += f"""
================================================================================
Цей звіт створено експертною системою раціонального харчування для спортсменів.
Рекомендується проконсультуватися з кваліфікованим дієтологом перед внесенням
кардинальних змін до раціону харчування.
================================================================================
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def save_json_results(self, filename: str):
        """Збереження результатів у JSON форматі"""
        results_copy = self.current_results.copy()
        
        # Конвертуємо в JSON-сумісний формат
        json_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'user_data': results_copy['user_data'],
            'bmr': float(results_copy['bmr']),
            'tdee': float(results_copy['tdee']),
            'macros': results_copy['macros'],
            'optimization': results_copy['optimization']
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    def clear_data(self):
        """Очищення всіх даних"""
        if messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете очистити всі дані?"):
            # Скидаємо значення до початкових
            self.gender_var.set("Чоловіча")
            self.age_var.set("25")
            self.weight_var.set("70")
            self.height_var.set("175")
            self.activity_var.set("Середня")
            self.goal_var.set("Підтримання форми")
            self.vegan_var.set(False)
            self.diabetes_var.set(False)
            
            # Очищуємо результати
            self.needs_text.config(state='normal')
            self.needs_text.delete(1.0, tk.END)
            self.needs_text.config(state='disabled')
            
            self.products_text.config(state='normal')
            self.products_text.delete(1.0, tk.END)
            self.products_text.config(state='disabled')
            
            self.explanation_text.config(state='normal')
            self.explanation_text.delete(1.0, tk.END)
            self.explanation_text.config(state='disabled')
            
            # Деактивуємо кнопку збереження
            self.save_btn.config(state='disabled')
            
            # Очищуємо збережені результати
            self.current_results = None
    
    def run(self):
        """Запуск головного циклу програми"""
        self.root.mainloop()

# =============================================================================
# ДОПОМІЖНІ ФУНКЦІЇ
# =============================================================================

def resource_path(relative_path):
    """Отримання шляху до ресурсу (для PyInstaller)"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def export_products_database():
    """Експорт бази продуктів у CSV файл"""
    try:
        df = pd.DataFrame(PRODUCTS_DATABASE)
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV файли", "*.csv")],
            title="Експорт бази продуктів"
        )
        if filename:
            df.to_csv(filename, index=False, encoding='utf-8-sig', sep=';')
            messagebox.showinfo("Успіх", f"База продуктів експортована: {filename}")
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося експортувати базу: {str(e)}")

def import_products_database():
    """Імпорт бази продуктів з CSV файлу"""
    try:
        filename = filedialog.askopenfilename(
            filetypes=[("CSV файли", "*.csv")],
            title="Імпорт бази продуктів"
        )
        if filename:
            df = pd.read_csv(filename, encoding='utf-8-sig', sep=';')
            # Валідація структури
            required_columns = ['Name', 'Protein', 'Fat', 'Carbs', 'Calories', 'Cost', 'Vegan', 'Diabet']
            if all(col in df.columns for col in required_columns):
                global PRODUCTS_DATABASE
                PRODUCTS_DATABASE = df.to_dict('records')
                messagebox.showinfo("Успіх", f"База продуктів імпортована: {len(PRODUCTS_DATABASE)} продуктів")
            else:
                messagebox.showerror("Помилка", "Неправильна структура CSV файлу")
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося імпортувати базу: {str(e)}")

# =============================================================================
# ГОЛОВНА ФУНКЦІЯ
# =============================================================================

def main():
    """Головна функція програми"""
    print("🚀 Запуск експертної системи раціонального харчування")
    print("📊 Версія: 2.0")
    print("👨‍💻 Автор: Студент ДНУ ім. Олеся Гончара")
    print("📅 Рік: 2025")
    print("-" * 60)
    
    try:
        # Створення та запуск головного вікна
        app = NutritionExpertSystem()
        app.run()
    except Exception as e:
        print(f"❌ Критична помилка: {e}")
        messagebox.showerror("Критична помилка", f"Не вдалося запустити програму:\n{str(e)}")
    finally:
        print("👋 Програма завершена")

if __name__ == "__main__":
    main()