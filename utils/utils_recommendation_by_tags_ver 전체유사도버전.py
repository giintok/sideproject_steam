# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 00:07:00 2024

@author: goldg
"""

import pandas as pd
import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
        if tag in tag_counts:
            tag_counts[tag] += 1
        else:
            tag_counts[tag] = 1
    
    # 태그 빈도를 내림차순으로 정렬하여 반환
    sorted_tag_counts = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_tag_counts

# TF-IDF 벡터화
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(games_df['Tags'])

def recommend_games(selected_tags, num_recommendations=50, page_number=1):
    # 선택된 태그들을 공백으로 연결하여 새로운 문서를 만듭니다.
    selected_tags_text = ' '.join(selected_tags)
    # 선택된 태그들에 대한 TF-IDF 벡터를 구합니다.
    selected_tags_tfidf = tfidf_vectorizer.transform([selected_tags_text])
    # 선택된 태그들과 유사한 게임을 찾습니다.
    similarities = cosine_similarity(selected_tags_tfidf, tfidf_matrix)
    # 유사도를 기준으로 상위 n개의 게임을 추천합니다.
    start_index = (page_number - 1) * num_recommendations
    end_index = start_index + num_recommendations
    similar_indices = similarities.argsort()[0][start_index:end_index][::-1]
    recommended_games = games_df.iloc[similar_indices]
    return recommended_games


