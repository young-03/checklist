import re
import time
import pandas as pd
import numpy as np
import urllib.request
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib import rc

# 웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# 정보입력
# api 신청 url : https://developers.naver.com/products/service-api/datalab/datalab.md
api_id = "______________"  # "_"를 지운 후 발급받은 id key를 입력해주세요
api_secret = "______________"  # "_"를 지운 후 발급받은 secret key를 입력해주세요

quote = input("검색어를 입력해주세요: ")  # 검색어 입력받기
print(quote, "구매 체크리스트로 검색합니다.", "\n")
Text = urllib.parse.quote(quote + " 구매 체크리스트")

print("크롤링 진행중... 잠시만 기다려주세요.", "\n")
url = "https://openapi.naver.com/v1/search/blog?query=" + Text + "&display=" + str(100)

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", api_id)
request.add_header("X-Naver-Client-Secret", api_secret)

response = urllib.request.urlopen(request)
rescode = response.getcode()

if rescode == 200:
    response_body = response.read()
else:
    print("Error Code:" + rescode)

body = response_body.decode('utf-8')
body = body.replace('"', '')

list1 = body.split('\n\t\t{\n\t\t\t')
list1 = [i for i in list1 if 'naver' in i]

titles = []
links = []

for item in list1:
    title_match = re.search(r'title:(.*?),\n', item)
    link_match = re.search(r'link:(.*?),\n', item)

    if title_match and link_match:
        title = title_match.group(1).replace('<\\/b>', '').replace('<b>', '')  # 태그 제거
        link = link_match.group(1).replace('\\/', '/')

        # 제목에 검색어(quote)가 포함된 경우에만 리스트에 추가
        if quote in title:
            titles.append(title)
            links.append(link)

# 블로그 본문 크롤링
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)

contents = []
for i in links:
    driver.get(i)
    time.sleep(1)
    driver.switch_to.frame("mainFrame")

    try:
        a = driver.find_element(By.CSS_SELECTOR, 'div.se-main-container').text
        contents.append(a)
    except NoSuchElementException:
        a = driver.find_element(By.CSS_SELECTOR, 'div#content-area').text
        contents.append(a)
    # print('본문: \n', a)

driver.quit()

num_titles = len(titles)
print("크롤링 완료!")
print(f"결과 갯수 : {num_titles}개")

if num_titles <= 5:
    print("분석에 사용되는 데이터의 수가 적습니다. 구매에 있어 추가적 정보수집을 권합니다.※")

df = pd.DataFrame({'제목': titles, '내용': contents, '출처': links})
# df 저장
df.to_csv('네이버 제품 블로그데이터_({}).csv'.format(quote), encoding='utf-8-sig', index=False)