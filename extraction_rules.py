from typing import Any
from bs4 import BeautifulSoup
from settings import Settings

def extract_company_name_and_url(soup:Any) -> tuple[str,str]:
    #only one tag with this class name
    tag_unified_job_title = soup.find("span", class_="jobs-unified-top-card__company-name")
    #there is only one tag within the parent tag, and it is a link with company href and name
    #the first and last elements are '\n'
    company_info_tag = tag_unified_job_title.contents[1]
    company_name = str(company_info_tag.string).strip()
    company_link = Settings.URLS['LINKEDIN_DOMAIN'] +  company_info_tag['href']
    return (company_name,company_link)

def extract_job_title(soup:Any) -> str:
    tag_company_title = soup.find("h2","t-24 t-bold jobs-unified-top-card__job-title")
    company_title = str(tag_company_title.string.strip())
    return company_title

def extract_applicant_experience(soup:Any,jobTitle) -> str:
    
    keywords = ['júnior','junior','pleno','sênior','senior']
    lowerCaseJobTitle = jobTitle.lower()
    
    tag_unified_top_card = soup.find("li", class_="jobs-unified-top-card__job-insight")
    tag_span = tag_unified_top_card.contents[0]
    text_tag_span = tag_span.string.strip()
    
    for keyword in keywords:
        if keyword in lowerCaseJobTitle or keyword in text_tag_span:
            if keyword == 'pleno': 
                return 'Pleno'
            elif keyword in ['junior','júnior']:
                return 'Júnior'
            else:
                return 'Sênior'
                        
    return "Pleno/Sênior"

def extractDomain(soup:Any,jobTitle:str) -> str:
    pass