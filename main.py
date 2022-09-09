import logging
import time
from crawler import Crawler
from dotenv import dotenv_values

if __name__ == '__main__':
    config = dotenv_values(".env")
    username = config['USERNAME']
    password = config['PASSWORD']
    crawler = Crawler()
    is_logged = crawler.login(username, password, crawler.DRIVER)
    batch_size = 100
    crawler.load_all_jobs(batch_size)
    time.sleep(2)
    job_urls = crawler.get_all_jobs_urls()
    if job_urls:
        pass