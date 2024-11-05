'''
Создать программу на в которой будет организован список словарей с ключами соответствующие пункту "атрибуты". Программа должна:
1. выбрать файл для работы 
2. Инициализировать базу данных 
3. Добавлять записи 
4. Выводить на экран все записи в виде таблицы 
5. Удалять записи по номеру 
6. Добавлять запись в базу данных 
7. Поиск по одному пол. 
8. Поиск по двум полям. 
9. Осуществлять поиск в соответствии с запросами указанными в пункте "Основные функции". 
Результаты поиска выводить на экран в виде таблицы. 
Атрибуты: ФИО, Название места работы, Должность, Даты мед. осмотров, Название специалиста проводившего осмотр, результаты мед. осмотра. 
Основные функции: Удалить все записи по заданному месту работы, заменить должность для заданного работника, 
вывести все сведения о работниках прошедших мед. осмотр в определенную дату.
'''
import json
from prettytable import PrettyTable  

FILE_NAME = "employees.json"

def load_data():
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_record(data):
    fio = input("Введите ФИО: ")
    workplace = input("Введите место работы: ")
    position = input("Введите должность: ")
    med_exam_dates = input("Введите даты мед. осмотров (через запятую): ").split(", ")
    specialist = input("Введите специалиста: ")
    exam_results = input("Введите результаты мед. осмотра: ")
    
    record = {
        "ФИО": fio,
        "Место работы": workplace,
        "Должность": position,
        "Даты мед. осмотров": med_exam_dates,
        "Специалист": specialist,
        "Результаты мед. осмотра": exam_results
    }
    data.append(record)
    save_data(data)
    print("Запись добавлена.")

def display_search_results(results):
    if results:
        table = PrettyTable()
        table.field_names = ["ФИО", "Место работы", "Должность", "Даты мед. осмотров", "Специалист", "Результаты мед. осмотра"]
        for record in results:
            table.add_row([
                record["ФИО"],
                record["Место работы"],
                record["Должность"],
                ", ".join(record["Даты мед. осмотров"]) if isinstance(record["Даты мед. осмотров"], list) else record["Даты мед. осмотров"],
                record["Специалист"],
                record["Результаты мед. осмотра"]
            ])
        print(table)
    else:
        print("По запросу записи не найдены.")

def initialize_database():
    return []

data = load_data()
while True:
    print("\nМеню:")
    print("1. Инициализировать базу данных")
    print("2. Добавить запись")
    print("3. Показать все записи")
    print("4. Удалить запись по номеру")
    print("5. Поиск по одному полю")
    print("6. Поиск по двум полям")
    print("7. Удалить все записи по месту работы")
    print("8. Заменить должность для заданного работника")
    print("9. Показать всех работников, прошедших мед. осмотр в определенную дату")
    print("0. Выход")

    choice = input("Выберите пункт меню: ")
    match choice:
        case "1":
            data = initialize_database()
            save_data(data)
            print("База данных инициализирована (очищена).")
        case "2":
            add_record(data)
        case "3":
            if data:
                table = PrettyTable()
                table.field_names = ["№", "ФИО", "Место работы", "Должность", "Даты мед. осмотров", "Специалист", "Результаты мед. осмотра"]
                for idx, record in enumerate(data, start=1):
                    table.add_row([
                        idx,
                        record["ФИО"],
                        record["Место работы"],
                        record["Должность"],
                        ", ".join(record["Даты мед. осмотров"]) if isinstance(record["Даты мед. осмотров"], list) else record["Даты мед. осмотров"],
                        record["Специалист"],
                        record["Результаты мед. осмотра"]
                    ])
                print(table)
            else:
                print("База данных пуста.")
        case "4":
            try:
                index = int(input("Введите номер записи для удаления: ")) - 1
                if 0 <= index < len(data):
                    removed = data.pop(index)
                    save_data(data)
                    print(f"Запись под номером {index + 1} удалена.")
                else:
                    print("Неверный номер записи.")
            except ValueError:
                print("Пожалуйста, введите корректный номер записи.")
        case "5":
            field = input("Введите поле для поиска (ФИО, Место работы, Должность, Даты мед. осмотров, Специалист, Результаты мед. осмотра): ")
            value = input("Введите значение для поиска: ")
            if field == "Даты мед. осмотров":
                results = [record for record in data if value in record.get(field, [])]
            else:
                results = [record for record in data if record.get(field) == value]
            display_search_results(results)
        case "6":
            field1 = input("Введите первое поле для поиска: ")
            value1 = input("Введите значение для первого поля: ")
            field2 = input("Введите второе поле для поиска: ")
            value2 = input("Введите значение для второго поля: ")
            results = [record for record in data if record.get(field1) == value1 and record.get(field2) == value2]
            display_search_results(results)
        case "7":
            workplace = input("Введите место работы для удаления записей: ")
            new_data = [record for record in data if record.get("Место работы") != workplace]
            if len(new_data) < len(data):
                data = new_data
                save_data(data)
                print(f"Все записи для места работы '{workplace}' удалены.")
            else:
                print(f"Записей с местом работы '{workplace}' не найдено.")
        case "8":
            fio = input("Введите ФИО сотрудника для изменения должности: ")
            new_position = input("Введите новую должность: ")
            updated = False
            for record in data:
                if record.get("ФИО") == fio:
                    record["Должность"] = new_position
                    updated = True
            if updated:
                save_data(data)
                print(f"Должность для '{fio}' обновлена.")
            else:
                print(f"Сотрудник с ФИО '{fio}' не найден.")
        case "9":
            exam_date = input("Введите дату мед. осмотра для поиска (в формате ГГГГ-ММ-ДД): ")
            results = [record for record in data if exam_date in record.get("Даты мед. осмотров", [])]
            display_search_results(results)
        case "0":
            break
        case _:
            print("Неверный ввод. Попробуйте снова.")
