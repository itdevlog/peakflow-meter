"""
Скрипт для запуска тестов системы Пикфлоуметр
"""
import subprocess
import sys
import os
from pathlib import Path

def run_tests():
    """Запуск всех тестов системы"""
    print("Запуск тестов системы Пикфлоуметр...")
    
    # Получаем путь к директории с тестами
    test_dir = Path(__file__).parent / "tests"
    
    if not test_dir.exists():
        print(f"Директория с тестами не найдена: {test_dir}")
        return False
    
    print(f"Поиск тестов в директории: {test_dir}")
    
    # Проверяем наличие pytest
    try:
        import pytest
    except ImportError:
        print("pytest не установлен. Установка...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
            import pytest
        except Exception as e:
            print(f"Не удалось установить pytest: {e}")
            return False
    
    # Запускаем тесты
    try:
        # Путь к тестам
        test_path = str(test_dir)
        
        print("Запуск тестов с использованием pytest...")
        print("-" * 50)
        
        # Запускаем pytest с дополнительными флагами для подробного вывода
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            test_path, 
            "-v",  # подробный вывод
            "--tb=short"  # краткий трейсбек
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)
        
        print("-" * 50)
        print(f"Результат выполнения тестов: {'УСПЕШНО' if result.returncode == 0 else 'С ОШИБКАМИ'}")
        print(f"Код возврата: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Ошибка при запуске тестов: {e}")
        return False


def run_specific_test(test_file: str):
    """Запуск конкретного теста"""
    test_path = Path(__file__).parent / "tests" / test_file
    
    if not test_path.exists():
        print(f"Файл теста не найден: {test_path}")
        return False
    
    try:
        import pytest
        
        print(f"Запуск теста: {test_file}")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            str(test_path), 
            "-v"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Ошибка при запуске теста {test_file}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Запуск конкретного теста
        test_file = sys.argv[1]
        print(f"Запуск конкретного теста: {test_file}")
        success = run_specific_test(test_file)
    else:
        # Запуск всех тестов
        success = run_tests()
    
    # Возвращаем код возврата для CI/CD
    sys.exit(0 if success else 1)