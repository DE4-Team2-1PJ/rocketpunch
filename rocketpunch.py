import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from bs4 import BeautifulSoup
import time

jobs = []
img_link = "https://static.rocketpunch.com/images/rocketpunch_logo.svg" # 플랫폼 로고 이미지 URL

driver = webdriver.Chrome(executable_path=r"C:\Users\User\Desktop\chromedriver-win64\chromedriver.exe")
url = "https://www.rocketpunch.com/jobs?keywords=%EB%8D%B0%EC%9D%B4%ED%84%B0"
driver.get(url)
time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

job_titles = soup.find_all('a', class_='nowrap job-title')
base_url = "https://www.rocketpunch.com"

for job in job_titles:
    job_info = {'title': job.get_text().strip()} # 공고 제목
    
    job_url = base_url + job['href']
    driver.get(job_url)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # 공고제목 - title, 회사이름 - company_name, 공고주소 - detail_url, 이미지주소 - img_link, 등록일 - pub_date, 마감일 - end_date
    
    job_info['company_name'] = soup.find_all('a', class_="nowrap company-name")[0].get_text().strip()
    job_info['detail_url'] = job_url
    #job_info['pub_date'] = soup.select_one("#wrap > div.four.wide.job-infoset.column > div.ui.celled.grid > div:nth-child(3) > div > div:nth-child(7) > div.content").get_text().strip()
    job_info['end_date'] = soup.select_one("#wrap > div.four.wide.job-infoset.column > div.ui.celled.grid > div:nth-child(3) > div > div:nth-child(6) > div.content").get_text().strip()
    job_info['platform_name'] = "RocketPunch"
    jobs.append(job_info)

driver.quit()

for job in jobs:
    print(job)

