import mysql.connector
from typing import Any, List, Dict
from dotenv import dotenv_values


class Mysql:

    db_handler = None

    # returns a instance of a database
    def __init__(self) -> None:

        config = dotenv_values(".env")

        self.db_handler = mysql.connector.connect(
            host=config['MYSQL_CONFIG_HOST'],
            user=config['MYSQL_CONFIG_USER'],
            password=config['MYSQL_CONFIG_PASSWORD'],
            database=config['MYSQL_CONFIG_DATABASE']
        )

        #why buffered=True
        self.cursor = self.db_handler.cursor(buffered=True)

    def insert_job_into_database(self, job: dict) -> None:
        insert_query = '''
        INSERT INTO Jobs
        VALUES(
            {ID},
            '{CompanyName}',
            '{ApplicantExperience}',
            '{Domain}',
            '{CompanyService}',
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
            CompanyName=job['CompanyName'],
            ApplicantExperience=job['ApplicantExperience'],
            Domain=job['Domain'],
            CompanyService=job['CompanyService'],
            Modality=job['Modality'],
            ProgrammingLanguage=job['ProgrammingLanguage'],
            Framework=job['Framework'],
            VirtualizationTech=job['VirtualizationTech'],
            DataBaseTech=job['DataBaseTech'],
            CreationDate=job['CreationDate'],
            Salary=job['Salary']
        )
        self.cursor.execute(insert_query)
        self.db_handler.commit()

    def retrieve_job_from_database(self, jobId: int) -> dict:
        retrieve_query = f"SELECT * FROM Jobs WHERE ID = {jobId};"
        self.cursor.execute(retrieve_query)
        query_data = self.cursor.fetchone();
        return query_data
   
    def delete_job_from_database(self,jobId) -> None:
        delete_query = f"DELETE FROM Jobs WHERE ID = {jobId};"
        self.cursor.execute(delete_query)
        self.db_handler.commit()

    def insert_job_batch(self, job_batch: List[Dict]) -> None:
        for job in job_batch:
            self.insert_job_into_database(job)

    def __exit__(self):
        self.db_handler.close()
        self.cursor.close()