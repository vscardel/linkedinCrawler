from this import s
from typing import Any,Tuple
from bs4 import BeautifulSoup,NavigableString
from settings import Settings


def extract_company_name_and_url(soup: Any) -> tuple[str, str]:
    # only one tag with this class name
    tag_unified_job_title = soup.find(
        "span", class_="jobs-unified-top-card__company-name")
    # there is only one tag within the parent tag, and it is a link with company href and name
    # the first and last elements are '\n'
    company_info_tag = tag_unified_job_title.contents[1]
    company_name = str(company_info_tag.string).strip()
    company_link = Settings.URLS['LINKEDIN_DOMAIN'] + company_info_tag['href']
    return (company_name, company_link)


def extract_job_title(soup: Any) -> str:
    tag_company_title = soup.find(
        "h2", "t-24 t-bold jobs-unified-top-card__job-title")
    company_title = str(tag_company_title.string.strip())
    return company_title


def extract_applicant_experience(soup: Any, jobTitle) -> str:

    keywords = ['júnior', 'junior', 'pleno', 'sênior', 'senior']

    tag_unified_top_card = soup.find(
        "li", class_="jobs-unified-top-card__job-insight")
    tag_span = tag_unified_top_card.contents[0]
    text_tag_span = tag_span.string.strip()

    for keyword in keywords:
        if keyword in jobTitle or keyword in text_tag_span:
            if keyword == 'pleno':
                return 'Pleno'
            elif keyword in ['junior', 'júnior']:
                return 'Júnior'
            else:
                return 'Sênior'

    return "Pleno/Sênior"


def extract_domain(soup: Any, jobTitle: str) -> str:
    # this list can and will get more complete
    keywords = ['backend', 'back-end', 'frontend', 'front-end']
    for keyword in keywords:
        if keyword in jobTitle:
            if keyword in ['backend', 'back-end']:
                return 'Web Back-End'
            else:
                return 'Web Front-End'
    # default return
    return "Software Engineering"


# two options, make an NLP approach or have a table
# for companies with their services, for now i will
# let this incomplete
def extrac_company_service(soup: Any) -> None:
    return None


def extract_job_location(soup: Any) -> str:
    tag_location = soup.find(
        "span", class_="jobs-unified-top-card__bullet")
    return str(tag_location.string).strip()


def extract_job_description(soup: Any) -> str:
    print('extraindo conteudo')
    tag_job_details = soup.find(
        "div", class_="jobs-box__html-content jobs-description-content__text t-14 t-normal jobs-description-content__text--stretch")
    # bad trick to not raise a "x has no attribute exception"
    span_tag = None
    for content in tag_job_details.contents:
        try:
            if content.name == 'span' and content.contents:
                span_tag = content
        except:
            pass
    if span_tag:
        description = ''
        for content in span_tag.contents:
            content_text = content.string
            if (content.name == 'p' or isinstance(content_text,NavigableString)) and content_text:
                description += content_text
            elif content.name == 'ul':
                for li in content.contents:
                    description += f"{li.string}"
        
    return description


#the programming languages are going to be stored as a string
#where each programming language is separated by a comma
def extract_modality(soup: Any, jobTitle: str, jobDescription: str) -> str:
    # some jobs have a tag indicating its modality, but not all
    tag_modality = soup.find(
        "span", class_="jobs-unified-top-card__workplace-type")
    if tag_modality:
        return str(tag_modality.string.strip())
    else:
        if 'remoto' in jobTitle.lower() or 'remoto' in jobDescription.lower():
            return 'Remoto'
        else:
            return 'Presencial'

#programming languages are stored as a string with the PL separated by
#a comma
def extract_programming_language(jobTitle:str, jobDescription:str) -> str:
    programming_languages_string = ''
    for programming_language in Settings.PROGRAMMING_LANGUAGES:
        if programming_language in jobTitle.lower() or programming_language in jobDescription.lower():
            programming_languages_string += f'{programming_language},'
    #take out the last comma
    programming_languages_string = programming_languages_string[:-1]
    return programming_languages_string

def extract_description_content(jobDescription:str) -> Tuple[str,str,str]:
    framework_string = ''
    virtualization_tech_string = ''
    database_tech_string = ''
    normalized_job_description = jobDescription.lower()
    for framework in Settings.FRAMEWORKS:
        if framework in normalized_job_description:
            framework_string += f'{framework},'
    for v_tech in Settings.VIRTUALIZATION:
        if v_tech in normalized_job_description:
            virtualization_tech_string += f'{v_tech},'
    for d_tech in Settings.DATABASES:
        if d_tech in normalized_job_description:
            database_tech_string += f'{d_tech},'
    #take last comma out of the string
    framework_string = framework_string[:-1]
    virtualization_tech_string = virtualization_tech_string[:-1]
    database_tech_string = database_tech_string[:-1]
    return framework_string,virtualization_tech_string,database_tech_string
