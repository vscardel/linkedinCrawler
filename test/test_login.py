import logging
import pytest
import requests
from crawler import Crawler
from dotenv import dotenv_values
from settings import Settings
from extraction import *

class Testclass:
    
    session:Any = None
    
    def test_login(self):
        config = dotenv_values(".env")
        logging.info("Executando o teste de login")
        username = config['USERNAME']
        password = config['PASSWORD']
        crawler = Crawler()
        is_logged = crawler.login(username, password, crawler.DRIVER)    
        request_session = crawler.request_session
        self.session = request_session
        logging.warning(self.session)
        response = request_session.get(Settings.URLS['URL_LOGIN'])
        assert is_logged and 'feed' in response.url
        
    #will not be logged, just test if it returns
    #something
    def test_extract_html_from_job(self):
        session = requests.Session()
        interval = Settings.SEARCH_INTERVAL
        job_id = pick_random_number(interval)
        html_content = extract_html_from_job(job_id,session)
        assert html_content