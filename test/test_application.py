import logging
import pytest
import requests
from db import Mysql
from crawler import Crawler
from dotenv import dotenv_values
from settings import Settings
from typing import Any

class Testclass:
    
    session: Any = None
    
    def test_login(self):
        config = dotenv_values(".env")
        print("Executando o teste de login")
        username = config['USERNAME']
        password = config['PASSWORD']
        crawler = Crawler()
        is_logged = crawler.login(username, password, crawler.DRIVER)    
        request_session = crawler.request_session
        self.session = request_session
        logging.warning(self.session)
        response = request_session.get(Settings.URLS['URL_LOGIN'])
        assert is_logged and 'feed' in response.url
    
    def test_db_connection(self):
        mySql = Mysql()
        jobId = mySql.generate_random_id()
        mock_job = {
            "ID": jobId,
            "CompanyName": "Amazon",
            "CompanyLink": "https://www.uol.com.br",
            "JobTitle":"Software Engineer",
            "ApplicantExperience":"Senior",
            "Domain": "Web Development",
            "Location":"Brasil",
            "Description":"bla bla bla",
            "CompanyService": "Sales",
            "Modality": "In Person",
            "ProgrammingLanguage": "Python, C# and Javascript",
            "Framework":"React",
            "VirtualizationTech": "Docker",
            "DataBaseTech": "Relational Databases",
            "CreationDate": "2022-09-08",
            "Salary": '5000.37'
        }
        mySql.insert_job_into_database(mock_job)
        job = mySql.retrieve_job_from_database(jobId = jobId)
        mySql.delete_job_from_database(jobId = jobId)
        assert job