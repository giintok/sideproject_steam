# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 00:07:00 2024

@author: goldg
"""

import pandas as pd
import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer

basic_path = os.path.dirname(__file__)
basic_file_path = os.path.join(basic_path, 'data')

# 게임 파일 경로
file_path = os.path.join(basic_file_path, 'final_dataset.csv')
games_df = pd.read_csv(file_path)

# 환경 변수에서 스팀 API 키 가져오기
STEAM_API_KEY = os.environ.get('9AB34E09020B2C9AD9CC6A31408AFC65')

def get_steam_game_image(app_id):
    base_url = "https://store.steampowered.com/api/appdetails"
    params = {
        "appids": app_id,
        "cc": "kr",  # 국가 코드 (예: 한국은 "kr")
        "key": STEAM_API_KEY  # 스팀 API 키 추가
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # 게임 이미지 URL 가져오기
    try:
        image_url = data[str(app_id)]["data"]["header_image"]
        return image_url
    except KeyError:
        return None
    
def calculate_tag_frequencies():
    all_tags = []
    for tags_list in games_df['Tags'].apply(lambda x: x.split(',')):
        all_tags.extend(tags_list)
    
    # 태그 빈도 계산
    tag_counts = {}
    for tag in all_tags:
        if tag.strip('[]') in tag_counts:  # 대괄호를 제거하고 태그를 저장
            tag_counts[tag.strip('[]')] += 1
        else:
            tag_counts[tag.strip('[]')] = 1
    
    # 태그 빈도를 내림차순으로 정렬하여 반환
    sorted_tag_counts = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_tag_counts

# TF-IDF 벡터화
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(games_df['Tags'])

def recommend_games(selected_tags, page_number=1, games_per_page=5):
    # 선택된 태그가 포함된 게임을 찾습니다.
    games_with_selected_tags = games_df[games_df['Tags'].apply(lambda x: any(tag in x for tag in selected_tags))]

    # 선택된 태그의 개수를 계산합니다.
    games_with_selected_tags['tag_count'] = games_with_selected_tags['Tags'].apply(lambda x: sum(tag in x for tag in selected_tags))

    # 태그의 개수가 많은 게임부터 추천하도록 수정
    sorted_games = games_with_selected_tags.sort_values(by='tag_count', ascending=False)

    # 페이지에 해당하는 게임들을 선택하여 반환
    start_idx = (page_number - 1) * games_per_page
    end_idx = start_idx + games_per_page
    page_games = sorted_games.iloc[start_idx:end_idx]
    
    return page_games
