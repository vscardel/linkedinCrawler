import mysql.connector
from typing import Any, List, Dict
from dotenv import dotenv_values


class Mysql:

    # returns a instance of a database
    def __init__(self) -> None:

        config = dotenv_values(".env")

        self.conn = mysql.connector.connect(
            host=config['MYSQL_CONFIG_HOST'],
            user=config['MYSQL_CONFIG_USER'],
            password=config['MYSQL_CONFIG_PASSWORD'],
        )

        # why buffered=True
        self.cursor = self.conn.cursor(buffered=True)
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS LinkedinCrawler;')
        self.cursor.execute('USE LinkedinCrawler;')

        self.cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS Jobs(
            ID BIGINT UNSIGNED NOT NULL,
            JobTitle varchar(255),
            CompanyName varchar(255),
            CompanyLink varchar(255),
            ApplicantExperience varchar(255),
            Domain varchar(255),
            CompanyService varchar(255),
            Location varchar(255),
            Description varchar(10000),
            Modality varchar(255),
            ProgrammingLanguage varchar(255),
            Framework varchar(255),
            VirtualizationTech varchar(255),
            DataBaseTech varchar(255),
            CreationDate DATE,
            Salary FLOAT(8,2),
            PRIMARY KEY (ID)
            );
        '''
        )

    def insert_job_into_database(self, job: dict) -> None:
        insert_query = '''
        INSERT INTO Jobs (
            ID, 
            JobTitle, 
            CompanyName, 
            CompanyLink, 
            ApplicantExperience, 
            Domain, 
            CompanyService, 
            Location,
            Description,
            Modality, 
            ProgrammingLanguage, 
            Framework,
            VirtualizationTech,
            DataBaseTech,
            CreationDate,
            Salary
        )
        VALUES(
            {ID},
            '{JobTitle}',
            '{CompanyName}',
            '{CompanyLink}',
            '{ApplicantExperience}',
            '{Domain}',
            '{CompanyService}',
            '{Location}',
            '{Description}',
            '{Modality}',
            '{ProgrammingLanguage}',
            '{Framework}',
            '{VirtualizationTech}',
            '{DataBaseTech}',
            STR_TO_DATE('{CreationDate}', '%Y-%m-%d'),
            {Salary}
        );
        '''.format(
            ID=job['ID'],
            JobTitle=job['JobTitle'],
            CompanyName=job['CompanyName'],
            CompanyLink=job['CompanyLink'],
            ApplicantExperience=job['ApplicantExperience'],
            Domain=job['Domain'],
            CompanyService=job['CompanyService'],
            Location=job['Location'],
            Description = job['Description'],
            Modality=job['Modality'],
            ProgrammingLanguage=job['ProgrammingLanguage'],
            Framework=job['Framework'],
            VirtualizationTech=job['VirtualizationTech'],
            DataBaseTech=job['DataBaseTech'],
            CreationDate=job['CreationDate'],
            Salary=job['Salary']
        )
        print(insert_query)
        self.cursor.execute(insert_query)
        self.conn.commit()

    def retrieve_job_from_database(self, jobId: int) -> dict:
        retrieve_query = f"SELECT * FROM Jobs WHERE ID = {jobId};"
        self.cursor.execute(retrieve_query)
        query_data = self.cursor.fetchone()
        return query_data

    def delete_job_from_database(self, jobId) -> None:
        delete_query = f"DELETE FROM Jobs WHERE ID = {jobId};"
        self.cursor.execute(delete_query)
        self.conn.commit()

    def generate_random_id(self) -> int:
        # generate random 64 bit integer
        generate_random_number_statement = '''SELECT UUID_SHORT();'''
        self.cursor.execute(generate_random_number_statement)
        # returns a tuple
        random_number = self.cursor.fetchone()
        # the tuple first position in the integer number
        return random_number[0]

    def __exit__(self):
        self.conn.close()
        self.cursor.close()
