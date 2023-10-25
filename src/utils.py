import json

import requests


def get_vacancies_from_employer(employer_id: int):
    """Функция для получения вакансий с сайта НеadHunter"""
    url = 'https://api.hh.ru/vacancies?employer_id='
    data_vacancies_filtered = []

    params = {"per_page": 30}
    response = json.loads(requests.get(url + str(employer_id), params).content.decode())['items']
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
    return data_vacancies_filtered
