class Settings:
    URLS = {
        'URL_LOGIN': "https://www.linkedin.com/checkpoint/lg/sign-in-another-account",
        "URL_JOB":"https://www.linkedin.com/jobs/collections/?"
    }
    # those numbers are based on my linkedin recomended jobs
    # if another person were to use this crawler it would be
    # advised to look at the pattern in the url
    # https://www.linkedin.com/jobs/collections/?currentJobId=NUM
    # were NUM is a number between MIN and MAX. Choose a interval that
    # fits what appears on the url when you search for jobs on there
    MIN = 360641128
    MAX = 570000000
    SEARCH_INTERVAL = (MIN,MAX)
    
    
