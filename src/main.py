from src.DBManager import DBManager
from src.HHSearchClass import HHSearchClass
from src.utils import get_vacancies_from_employer

employer_names = ['vk', 'АвтоВаз', 'Тинькофф', 'НорНикель', 'Альфа-Банк',
                  'БиоВитрум', 'ТНМК', 'Метало-Промышленная Компания',
                  'ОЗОН-Производство', 'ПАО Ростелеком']
employers_ids = [15478, 193400, 78638, 740, 80, 620417, 3009803, 1120099, 2180, 2748]


def main():
    # Создание экземпляра класса DBManager
    db = DBManager()
    # Создание таблиц
    db.create_tables()
    # Создание экземпляра класса HeadHunter
    for employer in employers_ids:
        hh = HHSearchClass(employer)

    # Получение инфо компании
        data_emp = hh.get_employer_data()

    # Добавление данных в таблицу
        for emp in data_emp:
            db.add_data_employers_to_database(emp)

    # Получение вакансий
        vacancies = get_vacancies_from_employer(employer)

    # Добавление данных в таблицу
        for vac in vacancies:
            db.add_data_vacancies_to_database(vac)

    # Взаимодействие с пользователем - выбор вывода данных из БД
    while True:
        user_input = input(
            "1 - Вывести список всех компаний и количество вакансий у каждой компании; \n"
            "2 - Вывести список всех вакансий; \n"
            "3 - Вывести среднюю зарплату по вакансиям; \n"
            "4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям; \n"
            "5 - Вывести список всех вакансий в названии которых содержатся переданные в метод слова; \n"
            "0 - для выхода. \n"
        )
        if user_input.lower() == "0":
            break

        elif user_input not in ['1', '2', '3', '4', '5', '0']:
            print(f'Такой команды нет, попробуйте еще раз!')
            continue

        elif user_input == "1":
            companies_and_vacancies_count = db.get_companies_and_vacancies_count()
            for company_count in companies_and_vacancies_count:
                print(company_count)

        elif user_input == "2":
            all_vacancies = db.get_all_vacancies()
            for companies_vacancy in all_vacancies:
                print(companies_vacancy)

        elif user_input == "3":
            avg_salary = db.get_avg_salary()
            print(avg_salary)

        elif user_input == "4":
            higher_salary = db.get_vacancies_with_higher_salary()
            for higher_vacancy in higher_salary:
                print(higher_vacancy)

        elif user_input == "5":
            input_keyword = input(f"Введите слово для поиска")
            keyword_data = db.get_vacancies_with_keyword(input_keyword)
            for keyword_vacancy in keyword_data:
                print(keyword_vacancy)


if __name__ == '__main__':
    main()
