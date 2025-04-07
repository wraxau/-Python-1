import os
import json
from datetime import datetime

FILENAME = "phonebook.json"


# Загрузка телефонного справочника из файла
def load_phonebook():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


# Сохранение телефонного справочника в файл
def save_phonebook(phonebook):
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(phonebook, file, indent=4, ensure_ascii=False)


# Проверка валидности имени или фамилии
def validate_name(name):
    return name.istitle() and name.replace(" ", "").isalnum()


# Проверка валидности номера телефона
def validate_phone_number(phone):
    if phone.startswith("+7"):
        phone = "8" + phone[2:]
    return phone.isdigit() and len(phone) == 11, phone


# Проверка валидности даты рождения
def validate_date(date):
    try:
        if date:
            datetime.strptime(date, "%d.%m.%Y")
        return True
    except ValueError:
        return False


# Добавление новой записи
def add_record(phonebook):
    first_name = input("Введите имя: ").strip().title()
    last_name = input("Введите фамилию: ").strip().title()

    if not validate_name(first_name) or not validate_name(last_name):
        print(
            "Ошибка: Имя и фамилия должны содержать только латинские буквы, цифры и пробелы, первая буква - заглавная")
        return

    identifier = f"{first_name} {last_name}"
    if identifier in phonebook:
        print("Ошибка: Такая запись уже существует")
        return

    phone = input("Введите номер телефона (11 цифр): ").strip()
    valid, phone = validate_phone_number(phone)
    if not valid:
        print("Ошибка: Некорректный номер телефона")
        return

    birth_date = input("Введите дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
    if not validate_date(birth_date):
        print("Ошибка: Некорректная дата рождения")
        return

    phonebook[identifier] = {"phone": phone, "birth_date": birth_date}
    print(f"Запись для {identifier} добавлена")


# Удаление записи
def delete_record(phonebook):
    identifier = input("Введите Имя и Фамилию для удаления: ").strip().title()
    if identifier in phonebook:
        del phonebook[identifier]
        print(f"Запись {identifier} удалена")
    else:
        print("Ошибка: Запись не найдена")


# Изменение записи
def update_record(phonebook):
    identifier = input("Введите Имя и Фамилию для изменения: ").strip().title()
    if identifier not in phonebook:
        print("Ошибка: Запись не найдена")
        return

    print("Введите новые значения или оставьте поле пустым для сохранения текущего значения")
    phone = input(f"Текущий телефон: {phonebook[identifier]['phone']}\nНовый телефон: ").strip()
    if phone:
        valid, phone = validate_phone_number(phone)
        if not valid:
            print("Ошибка: Некорректный номер телефона")
            return
        phonebook[identifier]['phone'] = phone

    birth_date = input(f"Текущая дата рождения: {phonebook[identifier]['birth_date']}\nНовая дата рождения: ").strip()
    if birth_date:
        if not validate_date(birth_date):
            print("Ошибка: Некорректная дата рождения")
            return
        phonebook[identifier]['birth_date'] = birth_date

    print(f"Запись {identifier} обновлена")


# Поиск записей
def search_records(phonebook):
    query = input("Введите имя, фамилию, телефон или дату рождения для поиска: ").strip().title()
    results = {k: v for k, v in phonebook.items() if query in k or query in v.values()}
    if results:
        for k, v in results.items():
            print(f"{k}: Телефон: {v['phone']}, Дата рождения: {v['birth_date']}")
    else:
        print("Записей не найдено.")


# Просмотр всех записей
def display_all(phonebook):
    if phonebook:
        for k, v in phonebook.items():
            print(f"{k}: Телефон: {v['phone']}, Дата рождения: {v['birth_date']}")
    else:
        print("Справочник пуст")


# Вычисление возраста
def calculate_age(phonebook):
    identifier = input("Введите Имя и Фамилию: ").strip().title()
    if identifier not in phonebook or not phonebook[identifier]['birth_date']:
        print("Ошибка: Запись не найдена или дата рождения отсутствует")
        return

    birth_date = datetime.strptime(phonebook[identifier]['birth_date'], "%d.%m.%Y")
    age = (datetime.now() - birth_date).days // 365
    print(f"Возраст {identifier}: {age} лет")


# Основная программа
def main():
    phonebook = load_phonebook()
    commands = {
        "1": ("Добавить запись", add_record),
        "2": ("Удалить запись", delete_record),
        "3": ("Изменить запись", update_record),
        "4": ("Поиск записей", search_records),
        "5": ("Просмотр всех записей", display_all),
        "6": ("Вычислить возраст", calculate_age),
        "7": ("Выход", lambda x: print("Выход из программы"))
    }

    while True:
        print("\nВыберите команду:")
        for key, (desc, _) in commands.items():
            print(f"{key} - {desc}")
        command = input("Введите номер команды: ").strip()

        if command == "7":
            save_phonebook(phonebook)
            break
        elif command in commands:
            commands[command][1](phonebook)
            save_phonebook(phonebook)
        else:
            print("Ошибка: Некорректная команда")


if __name__ == "__main__":
    main()
