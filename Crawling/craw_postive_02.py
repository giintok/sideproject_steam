# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 18:51:31 2024

@author: goldg
"""
#크롤링으로 방식 바꿔봄

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# app_ids.csv 파일에서 app_id 불러오기
appids = pd.read_csv('app_ids.csv')['AppID']

# 결과를 저장할 리스트 생성
results = []

# 각 app_id에 대해 반복
for appid in appids[1852:]:
    # 게임 페이지 URL 생성
    url = f'https://store.steampowered.com/app/{appid}/'

    # GET 요청을 보내고 응답 받기
    response = requests.get(url)

    # 딜레이 추가
    time.sleep(3)

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 리뷰 타입 (positive/negative) 및 해당 리뷰 수를 추출합니다.
    positive_reviews = soup.find('input', {'id': 'review_type_positive'}).find_next('span', {'class': 'user_reviews_count'}).text
    negative_reviews = soup.find('input', {'id': 'review_type_negative'}).find_next('span', {'class': 'user_reviews_count'}).text

    # 숫자만 추출하여 정수로 변환합니다.
    positive_count = int(''.join(filter(str.isdigit, positive_reviews)))
    negative_count = int(''.join(filter(str.isdigit, negative_reviews)))

    # 결과를 딕셔너리로 저장
    result = {'app_id': appid, 'positive_reviews': positive_count, 'negative_reviews': negative_count}
    results.append(result)

    # 결과 출력
    print(result)

# 결과를 데이터프레임으로 변환
df = pd.DataFrame(results)

# 결과를 파일로 저장
df.to_csv('review_counts_2200.csv', index=False)
