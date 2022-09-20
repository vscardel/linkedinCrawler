from typing import Any
from bs4 import BeautifulSoup
from settings import Settings

def remove_whitespaces(string:str) -> str:
    string.remove('\n')
    
def extract_company_name_and_url(soup:Any) -> tuple[str,str]:
    #only one tag with this class name
    tag_unified_job_title = soup.find("span", class_="jobs-unified-top-card__company-name")
    #there is only one tag within the parent tag, and it is a link with company href and name
    #the first and last elements are '\n'
    company_info_tag = tag_unified_job_title.contents[1]
    company_name = str(company_info_tag.string).strip()
    company_link = Settings.URLS['LINKEDIN_DOMAIN'] +  company_info_tag['href']
    return (company_name,company_link)
    
