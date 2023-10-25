import psycopg2


class DBManager:
    """Класс для создания базы данных, таблиц. и их заполнения"""

    def __init__(self):
        """Инициализация класса менеджера DataBase, подключение к учетной записи PosgreSQL"""
        self.conn = psycopg2.connect(dbname="headhunter_database",
                                     user="postgres",
                                     password="Timur3370",
                                     port="5432",
                                     host='Localhost'
                                     )
        self.cur = self.conn.cursor()

    def connect_to_database(self) -> None:
        """Метод для коннекта"""
        self.conn = psycopg2.connect(dbname="headhunter_database",
                                     user="postgres",
                                     password="Timur3370",
                                     port="5432",
                                     host='Localhost'
                                     )
        self.cur = self.conn.cursor()

    def create_database(self, database_name: str) -> None:
        try:
            self.cur.execute(f"CREATE DATABASE {database_name}")
        except psycopg2.errors.DuplicateDatabase:
            print(f"ОШИБКА: база данных {database_name} уже существует")
        self.conn.close()

    def create_tables(self) -> None:
        """Функция для создания таблиц"""
        # self.connect_to_db()
        self.conn.autocommit = True
        # self.cur.execute(f"DROP DATABASE employers")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS employers (
                                        employer_id INTEGER,
                                        employer VARCHAR(255) PRIMARY KEY NOT NULL,
                                        description TEXT,
                                        employer_area VARCHAR(255),
                                        vacancy_count INTEGER,
                                        site_url VARCHAR(255)
                                        )
                                        """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS vacancies
                                         (vacancy_id INTEGER PRIMARY KEY,
                                         employer VARCHAR(255) NOT NULL,
                                         name_vacancy VARCHAR(255),
                                         url_vacancy VARCHAR(255),
                                         salary INTEGER,
                                         experience TEXT,
                                          
                                         CONSTRAINT fk_vacancies_employer FOREIGN KEY(employer) 
                                         REFERENCES employers(employer)  
                                         )
                                        """)

        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def add_data_employers_to_database(self, employer: dict) -> None:
        """Функция для записи данных в таблицы"""
        self.connect_to_database()
        self.conn.autocommit = True
        self.cur.execute("""INSERT INTO employers (employer_id, employer, description, employer_area, vacancy_count, site_url)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                             (employer.get('employer_id'),
                              employer.get('name'),
                              employer.get('description'),
                              employer.get('area'),
                              employer.get('vacancy_count'),
                              employer.get('url_company')
                              ))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def add_data_vacancies_to_database(self, vacancy: dict) -> None:
        """Метод для добавления вакансиий компаний в таблицу"""
        self.connect_to_database()
        self.conn.autocommit = True
        self.cur.execute("""INSERT INTO vacancies (vacancy_id, employer, name_vacancy, url_vacancy, salary, experience)
                             VALUES (%s, %s, %s, %s, %s, %s)""",
                             (vacancy.get('id'),
                              vacancy.get('employer'),
                              vacancy.get('name'),
                              vacancy.get('url'),
                              vacancy.get('salary'),
                              vacancy.get('experience')
                              ))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return:
        """
        self.connect_to_database()
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute(f"""
                            SELECT employer, COUNT(*)
                            FROM vacancies
                            GROUP BY employer
                            ORDER BY COUNT(*) DESC
                            """)
            data = cur.fetchall()

        self.conn.close()
        return data

    def get_all_vacancies(self):
        """
        Получает список всех вакансий
        :return:
        """
        self.connect_to_database()
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute(f"""
                        SELECT * FROM vacancies
                            """)
            data = cur.fetchall()

        self.conn.close()
        return data

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        :return:
        """
        self.connect_to_database()
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute(f"""
                            SELECT AVG(salary) FROM vacancies
                            """)
            data = cur.fetchone()

        self.conn.close()
        return round(data[0])

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        self.connect_to_database()
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute(f"""
                            SELECT * FROM vacancies
                            WHERE salary > (SELECT AVG(salary) FROM vacancies)
                            """)
            data = cur.fetchall()

        self.conn.close()
        return data

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Получает список всех вакансий в названии которых содержатся переданные в метод слова
        :return:
        """
        self.connect_to_database()
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute(f"""
                            SELECT * FROM vacancies
                            WHERE name_vacancy LIKE '%{keyword}%'
                                    """)
            data = cur.fetchall()

        self.conn.close()
        return data
