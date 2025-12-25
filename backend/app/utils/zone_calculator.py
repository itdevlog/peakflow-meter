"""
Модуль для расчета зон пикфлоу
"""
from typing import Dict
from datetime import date
from ..models.user import ChildProfile


def calculate_predicted_pef(child_profile: ChildProfile) -> float:
    """
    Рассчитывает предсказуемое значение ПСВ (пиковая скорость выдоха) по возрасту, росту и полу.
    Использует медицинские стандарты для детей.
    """
    # Определяем возраст ребенка
    today = date.today()
    birth_date = child_profile.birth_date
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    # Используем медицинские формулы для расчета предсказуемой ПСВ
    # Эти формулы основаны на исследованиях для детей европеоидной расы
    if child_profile.gender == "male":
        # Формула для мальчиков: ПСВ = 54.55 * рост(см) - 3.37 * возраст(лет) - 367.5
        predicted_pef = 54.55 * child_profile.height - 3.37 * age - 367.5
    else:
        # Формула для девочек: ПСВ = 44.8 * рост(см) - 2.86 * возраст(лет) - 278.9
        predicted_pef = 44.8 * child_profile.height - 2.86 * age - 278.9
    
    # Убедимся, что значение не отрицательное
    predicted_pef = max(predicted_pef, 50.0) # Минимальное значение для ребенка
    
    return predicted_pef


def calculate_zone_boundaries(child_profile: ChildProfile) -> Dict[str, int]:
    """
    Рассчитывает границы зон на основе профиля ребенка.
    Использует медицинские стандарты для расчета нормативных значений ПСВ (пиковая скорость выдоха).
    """
    # Рассчитываем предсказуемое значение ПСВ
    predicted_value = calculate_predicted_pef(child_profile)
    
    # Если у нас есть лучший результат, можем использовать его для персонализации
    # Согласно медицинским рекомендациям, используем лучший результат как 100% значение
    if child_profile.best_result and child_profile.best_result > predicted_value:
        # Используем лучший результат как основу для расчета зон
        baseline_value = child_profile.best_result
    else:
        # Используем предсказуемое значение как основу
        baseline_value = int(predicted_value)
    
    # Определяем границы зон по медицинским стандартам:
    # Зеленая зона: > 80% от норматива (хороший контроль)
    # Желтая зона: 60-80% от норматива (умеренный контроль, требует наблюдения)
    # Красная зона: < 60% от норматива (плохой контроль, требует медицинского вмешательства)
    
    green_min = int(baseline_value * 0.8)
    yellow_min = int(baseline_value * 0.6)
    red_min = 0  # Устанавливаем минимальный порог
    
    return {
        "green_min": green_min,
        "yellow_min": yellow_min,
        "red_min": red_min,
        "predicted_value": int(predicted_value),
        "baseline_value": baseline_value,
        "personalized": child_profile.best_result and child_profile.best_result > predicted_value
    }


def determine_zone(value: int, boundaries: Dict[str, int]) -> str:
    """
    Определяет, в какую зону попадает значение
    """
    if value >= boundaries["green_min"]:
        return "green"
    elif value >= boundaries["yellow_min"]:
        return "yellow"
    else:
        return "red"