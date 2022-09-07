import logging
import time
from typing import Tuple,Any
from numpy import random
from settings import Settings

Interval = Tuple[int,int]

def pick_random_number(interval:Interval):
    MIN = interval[0]
    MAX = interval[1]
    #picks a random job (and prays to have some content in it)
    job_id = random.randint(MIN,MAX+1)
    return job_id

def extract_html_from_job(job_id:int,request_session:Any) -> str:
    search_url = Settings.URLS['URL_JOB']
    complete_search_url = search_url + f'currentJobId={job_id}'
    job_content = request_session.get(complete_search_url)
    #wait to load the content of the page
    time.sleep(2)
    logging.warning(job_content.content)
    return str(job_content.content)