from bs4 import BeautifulSoup
from selenium import webdriver
import time

jobs = []
img_link = "https://static.rocketpunch.com/images/rocketpunch_logo.svg" # 플랫폼 로고 이미지 URL
base_url = "https://www.rocketpunch.com"
page_num = 1

driver = webdriver.Chrome(executable_path=r"C:\Users\User\Desktop\chromedriver-win64\chromedriver.exe")

while True:
    url = f"https://www.rocketpunch.com/jobs?page={page_num}&keywords=%EB%8D%B0%EC%9D%B4%ED%84%B0"
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    job_titles = soup.find_all('a', class_='nowrap job-title')
    if not job_titles:
        break
    
    for job in job_titles:
        
        # "데이터"와 무관한 공고가 검색이 많이 되서 필터링
        title = job.get_text().strip()
        if (not "데이터" in title) and (not "data" in title.lower()): 
            continue
        
        job_info = {'title': title}
        
        job_url = base_url + job['href']
        driver.get(job_url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 공고제목 - title, 회사이름 - company_name, 공고주소 - detail_url, 이미지주소 - img_link, 
        # 등록일 - pub_date, 마감일 - end_date, 카테고리 - category_name, 기술스택 - stack
        # 지역 - region, 신입/경력 - career
        job_info['company_name'] = soup.find_all('a', class_="nowrap company-name")[0].get_text().strip()
        job_info['detail_url'] = job_url
        
        end_date = soup.find('i', class_="ic-calendar_new icon").next_sibling.get_text().strip()
        job_info['end_date'] = end_date.split()[0]
        job_info['platform_name'] = "RocketPunch"
        
        job_info['category_name'] = None # 카테고리는 따로 없어서 추출하지 않음
        stacks = soup.select_one("#wrap > div.eight.wide.job-content.column > section:nth-child(5) > div").find_all('a')
        job_info['stack'] = [stack.get_text().strip() for stack in stacks]
        job_info['career'] = soup.select_one("body > div.pusher.dimmable > div.ui.vertical.center.aligned.detail.job-header.header.segment > div > div > div.job-stat-info").get_text().strip()

        # 지역의 경우 생략된 공고가 있어 예외처리
        region = soup.find(name='span', class_="address")
        if not region:
            job_info['region'] = None
        else:
            region = region.get_text().strip()
            job_info['region'] = " ".join(region.split()[:2]) # 주소 텍스트에서 서울특별시 **구, 경기도 **시 까지만 저장
        
        jobs.append(job_info)
        
    page_num += 1

driver.quit()

for job in jobs: # 결과 출력
    print(job)

