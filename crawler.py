from pydoc import describe
import selenium.webdriver
import requests
import os
import login
import time
from typing import Any
from selenium.webdriver.chrome.options import Options
from settings import Settings
from bs4 import BeautifulSoup
from extraction_rules import *
from dotenv import load_dotenv

load_dotenv()

# 12 is the number of new jobs loaded after scrolling down


def calculate_number_of_scroll_downs(number_of_jobs: int) -> int:
    num_jobs = 0
    num_scroll_downs = 0
    while num_jobs <= number_of_jobs:
        num_jobs += 12
        num_scroll_downs += 1
    return num_scroll_downs


class Crawler:

    def __init__(self, headless=True) -> None:
        # initialize DRIVER and requests
        self.username: str = None
        self.password: str = None
        chrome_options = Options()
        self.request_session = requests.Session()
        chrome_options.add_argument(
            f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-crash-reporter")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-in-process-stack-traces")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--output=/dev/null")

        self.DRIVER = selenium.webdriver.Chrome(
            executable_path=os.getenv('EXECUTABLE_PATH'), options=chrome_options)

    # set the cookies in the requests session
    def login(self, username: str, password: str, DRIVER: Any) -> bool:
        cookie_list: cookies = login.login(username, password, DRIVER)
        if cookie_list:
            login.transfer_cookies_to_request(
                self.request_session, cookie_list)
            return True
        else:
            False

    # scroll down the page the necessary number of times
    # to reveal all jobs urls
    def load_all_jobs(self, num_jobs: int) -> None:
        self.DRIVER.get(Settings.URLS['URL_JOBS'])
        # wait screen to load
        time.sleep(2)
        # each screen loading load 12 new jobs, so
        # i can calculate the number of screen downs
        # i need to take
        num_scroll_downs = calculate_number_of_scroll_downs(num_jobs)
        for count in range(0, num_scroll_downs):
            # 20000 is a big enough number to scroll all the way down
            self.DRIVER.execute_script('window.scrollTo(0, 20000)')
            time.sleep(1)

    # extract all the urls from the scrolled down page
    def get_all_jobs_urls(self) -> list[str]:
        page_html = self.DRIVER.page_source
        soup = BeautifulSoup(page_html, 'html.parser')
        all_html_links = soup.find_all('a')
        href_list = []
        for link in all_html_links:
            link_href = link.get('href')
            if 'JobId' in link_href:
                # take garbage out of the url splitting on '&' and taking the first part
                clean_url = link_href.split('&')[0]
                complete_url = Settings.URLS['LINKEDIN_DOMAIN'] + clean_url
                if complete_url not in href_list:
                    href_list.append(complete_url)
        return href_list

    def extract_html_from_jobs_urls(self, job_urls: list[str]) -> list[str]:
        html_content_list = []
        for url in job_urls:
            try:
                self.DRIVER.get(url)
                # wait for the page to load
                time.sleep(3)
                html_content_list.append(self.DRIVER.page_source)
            except Exception as e:
                print(e)
        return html_content_list

    def build_content_dict(self,content_key: str, content_dict: dict, extraction_function: Any, soup_object: Any = None, jobTitle: str = None, jobDescription:str = None):
        try:
            content_dict[content_key] = extraction_function(soup_object,jobTitle,jobDescription)
        except Exception as e:
            print(f'There was an error on the extraction of key {content_key}')
            print('>>>>>>>>>>>>')
            print(e)
            content_dict[content_key] = ''

    def extract_content_from_html(self, html_content: str) -> dict:
        content_dict = {}
        soup = BeautifulSoup(html_content, 'html.parser')
        self.build_content_dict('CompanyName',content_dict,extract_company_name,soup,None,None)
        self.build_content_dict('CompanyLink',content_dict,extract_company_url,soup,None,None)
        self.build_content_dict('JobTitle',content_dict,extract_job_title,soup,None,None)
    
        jobTitle = content_dict.get('JobTitle','')
    
        self.build_content_dict('Description',content_dict,extract_job_description,soup,None,None)
        
        Description = content_dict.get('Description','')
            
        self.build_content_dict('ApplicantExperience',content_dict,extract_applicant_experience,soup,jobTitle,None)
        self.build_content_dict('Domain',content_dict,extract_domain,jobTitle,None)
        self.build_content_dict('CompanyService',content_dict,extrac_company_service,soup,None,None)
        self.build_content_dict('Location',content_dict,extract_job_location,soup,None,None)
        self.build_content_dict('Modality',content_dict,extract_modality,None,jobTitle,Description)
        self.build_content_dict('ProgrammingLanguage',content_dict,extract_programming_language,None,jobTitle,Description)
        
        frameworks, v_tech, d_tech = extract_description_content(soup,jobTitle,Description)
        
        #the only ones that are different for performance reasons 
        content_dict['Framework'] = frameworks
        content_dict['VirtualizationTech'] = v_tech
        content_dict['DataBaseTech'] = d_tech
            
        self.build_content_dict('CreationDate',content_dict,extract_date,soup,None,None)
        self.build_content_dict('Salary',content_dict,extract_salary,soup,None,None)
        return content_dict

    def __exit__(self):
        self.DRIVER.quit()