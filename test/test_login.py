from crawler import Crawler
import logging
from dotenv import dotenv_values
from settings import Settings


def test_login():
    config = dotenv_values(".env")
    logging.info("Executando o teste de login")
    username = config['USERNAME']
    password = config['PASSWORD']
    crawler = Crawler()
    is_logged = crawler.login(username, password, crawler.DRIVER)    
    request_session = crawler.request_session
    response = request_session.get(Settings.URLS['URL_LOGIN'])
    assert is_logged and 'feed' in response.url