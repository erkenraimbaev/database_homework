import json

import requests


class HHSearchClass:
    """Класс для поиска данных о компаниях HeadHunter.ru и их вакансиях"""

    def __init__(self, employer_id):
        self.employer_id = employer_id

    def __str__(self):
        pass

    def get_employer_data(self) -> list:
        """
        Функция для получения данных о работодателе
        """
        data_employers = []
        url = "https://api.hh.ru/employers/"
        response = json.loads(requests.get(url + str(self.employer_id)).content.decode())
        emp_id = response.get('id'),
        employer_name = response.get("name")
        description = response.get("description")
        employer_area = response.get("area").get("name")
        vacancy_count = response.get("open_vacancies")
        site_url = response.get("site_url")
        filtered_employer = {'employer_id': emp_id,
                             'name': employer_name,
                             'description': description,
                             'area': employer_area,
                             'vacancy_count': vacancy_count,
                             'url_company': site_url
                             }
        data_employers.append(filtered_employer)
        return data_employers

    def get_vacancies_from_employer(self) -> list:
        """Функция для получения вакансий компании"""
        data_vacancies_filtered = []
        url = 'https://api.hh.ru/vacancies?employer_id='
        params = {"per_page": 30}
        response = json.loads(requests.get(url + str(self.employer_id), params).content.decode())['items']
        for res in response:
            vacancy_id = res.get('id')
            employer_name = res.get('employer').get('name')
            name_vacancy = res.get('name')
            url_vacancy = res.get('alternate_url')
            salary_vacancy = res.get("salary")
            if salary_vacancy is None:
                salary_vacancy = 0
            else:
                salary_vacancy = res.get("salary").get("from")
                if salary_vacancy is None:
                    salary_vacancy = 0
            experience_vacancy = res.get('experience').get('name')
            filtered_vacancy = {'id': vacancy_id,
                                'employer': employer_name,
                                'name': name_vacancy,
                                'url': url_vacancy,
                                'salary': salary_vacancy,
                                'experience': experience_vacancy,
                                }
            data_vacancies_filtered.append(filtered_vacancy)
        print(data_vacancies_filtered)
