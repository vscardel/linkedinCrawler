
import selenium.webdriver
import requests
import login
import os
from login import cookies, transfer_cookies_to_request
from typing import Any
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

class Crawler:

    def __init__(self) -> None:
        # initialize DRIVER and requests
        self.username: str = None
        self.password: str = None
        chrome_options = Options()
        self.request_session = requests.Session()
        chrome_options.add_argument(
            f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
        self.DRIVER = selenium.webdriver.Chrome(
            executable_path=os.getenv('EXECUTABLE_PATH'), options=chrome_options)

    # set the cookies in the requests session
    def login(self, username: str, password: str, DRIVER: Any) -> bool:
        cookie_list: cookies = login.login(username, password, DRIVER)
        if cookie_list:
            transfer_cookies_to_request(self.request_session, cookie_list)
            return True
        else:
            False
    
    def __exit__(self):
        self.DRIVER.quit()
