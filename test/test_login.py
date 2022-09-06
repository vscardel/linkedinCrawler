from crawler import Crawler
import logging
from dotenv import dotenv_values

def test_login():
    logging.info("Executando o teste de login")
    config = dotenv_values(".env")
    username = config['USERNAME']
    password = config['PASSWORD']
    crawler = Crawler()
    is_logged = crawler.login(username, password, crawler.DRIVER)
    # check if is logged and the cookies were generated
    assert is_logged and crawler.request_session.cookies
