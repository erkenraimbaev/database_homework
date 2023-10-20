import json

import requests


class HHSearchClass:
    """Класс для поиска данных о компаниях HeadHunter.ru и их вакансиях"""

    def __init__(self, employer_id):
        self.employer_id = employer_id

    def __str__(self):
        pass

    def get_employer_data(self):
        """
        Функция для получения данных о работодателе
        """
        data_employers = []
        url = "https://api.hh.ru/employers/"
        response = json.loads(requests.get(url + str(self.employer_id)).content.decode())
        employer_name = response.get("name")
        description = response.get("description")
        employer_area = response.get("area").get("name")
        vacancy_count = response.get("open_vacancies")
        site_url = response.get("site_url")
        filtered_employer = {'name': employer_name,
                             'description': description,
                             'area': employer_area,
                             'vacancy_count': vacancy_count,
                             'url_company': site_url
                             }
        data_employers.append(filtered_employer)
        return data_employers

    def get_vacancies_from_employer(self):
        """Функция для получения вакансий компании"""
        params = {'per_page': 30}
        data_vacancies = json.loads(requests.get('https://api.hh.ru/vacancies?employer_id=' + str(self.employer_id),
                                                 params).content.decode())['items']
        data_vacancies_filtered = []
        for vacancy in data_vacancies:
            employer = vacancy.get('employer').get('name')
            name_vacancy = vacancy.get('name')
            url_vacancy = vacancy.get('alternate_url')
            salary_vacancy = vacancy.get("salary")
            experience_vacancy = vacancy.get('experience').get('name')
            filtered_vacancy = {'employer': employer,
                                'name': name_vacancy,
                                'url': url_vacancy,
                                'salary': salary_vacancy,
                                'experience': experience_vacancy,
                                }
            data_vacancies_filtered.append(filtered_vacancy)
        return data_vacancies_filtered
