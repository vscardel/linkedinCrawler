import os
from login import login
from crawler import Crawler

def test_login():
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    crawler = Crawler()
    is_logged = crawler.login(username, password, crawler.DRIVER)
    # check if is logged and the cookies were generated
    assert is_logged and crawler.request_session.cookies
