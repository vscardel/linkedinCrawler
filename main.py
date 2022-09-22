import logging
import time
from crawler import Crawler
from db import Mysql
from dotenv import dotenv_values

if __name__ == '__main__':
    
    config = dotenv_values(".env")
    username = config['USERNAME']
    password = config['PASSWORD']
    crawler = Crawler()
    is_logged = crawler.login(username, password, crawler.DRIVER)
    batch_size = 10
    crawler.load_all_jobs(batch_size)
    time.sleep(2)
    job_urls = crawler.get_all_jobs_urls()
    if job_urls:
        html_list = crawler.extract_html_from_jobs_urls(job_urls)
        for html in html_list:
            info_dict = crawler.extract_content_from_html(html)
            print(info_dict)
    else:
        print("couldn't find any jobs")