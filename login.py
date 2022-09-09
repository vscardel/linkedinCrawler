import time
import requests
import logging
from typing import List, Dict, Any
from settings import Settings

# type definitions
cookie = Dict[str, str]
cookies = List[cookie]

# this function logs into linkedin with the credentials passed and return
# the session cookies to further use


def login(username: str, password: str, DRIVER: Any) -> cookies:
    url_login = Settings.URLS['URL_LOGIN']
    print("get on linkedin")
    DRIVER.get(url_login)
    time.sleep(1)
    print("executing js for login")
    DRIVER.execute_script(
        f'document.querySelector("#username").value = "{username}"')
    DRIVER.execute_script(
        f'document.querySelector("#password").value = "{password}"')
    DRIVER.execute_script(
        'document.querySelector("#organic-div > form > div.login__form_action_container > button").click()')
    current_url = DRIVER.current_url
    if 'manage-account' in current_url:
        print("entered on special manage-account case")
        DRIVER.execute_script(
            'document.querySelector("#ember20 > button.primary-action-new").click()')
        current_url = DRIVER.current_url
    if 'feed' in current_url:
        return DRIVER.get_cookies()
    return []


def transfer_cookies_to_request(request_session: Any, cookie_list: cookies) -> None:
    for cookie in cookie_list:
        if 'httpOnly' in cookie:
            del cookie['httpOnly']
        if 'sameSite' in cookie:
            del cookie['sameSite']
        if 'expiry' in cookie:
            del cookie['expiry']
        current_cookie = requests.cookies.create_cookie(**cookie)
        request_session.cookies.set_cookie(current_cookie)
