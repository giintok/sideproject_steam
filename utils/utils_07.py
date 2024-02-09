# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:56:21 2024

@author: goldg
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os

basic_path = os.path.dirname(__file__)
basic_file_path = os.path.join(basic_path, 'data')

# 게임 파일 경로
file_path = os.path.join(basic_file_path, 'games_final_final.csv')
games_df = pd.read_csv(file_path)

# 장르를 리스트로 변환하고 쉼표로 구분하는 전처리 함수
games_df['Tags'] = games_df['Tags'].apply(lambda x: eval(x))

def process_data(games_df):
    games_df = games_df.fillna('')
    features = ['Genres', 'Tags', 'About the game']
    games_df['combined_features'] = games_df[features].apply(lambda x: ' '.join(map(str, x)), axis=1)
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(games_df['combined_features'])
    return tfidf_matrix

def get_indices(games_df):
    indices = pd.Series(games_df.index, index=games_df['Name']).drop_duplicates()
    return indices

def compute_similarity(tfidf_matrix):
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_similarities

def process_data_by_tags(games_df, top_n=30):
    games_df = games_df.fillna('')
    # 태그 카운트 계산
    tag_counts = {}
    for tags_list in games_df['Tags']:
        for tag in tags_list:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # 상위 N개의 태그 선택
    top_tags = [tag for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]]
    
    features = ['Tags', 'About the game']
    games_df['combined_features'] = games_df[features].apply(lambda x: ' '.join(map(str, x)), axis=1)
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', vocabulary=top_tags)
    tfidf_matrix = tfidf_vectorizer.fit_transform(games_df['combined_features'])
    return tfidf_matrix

def get_top_similar_games_by_tags(selected_tags, games_df, cosine_similarities, indices):
    games_subset = games_df.copy()
    selected_games = []
    if selected_tags:
        for tag in selected_tags:
            # 태그 비교 시 대소문자 구분 없이 비교하고, 공백 제거
            tag = tag.strip().lower()
            selected_games.extend(games_subset[games_subset['Tags'].apply(lambda x: tag in map(str.lower, x))].index.tolist())
        if not selected_games:  # 선택한 태그에 해당하는 게임이 없는 경우
            return pd.DataFrame(columns=['AppID', 'Name', 'Price', 'Developers', 'Publishers', 'Genres', 'Age_Category'])
        else:
            games_subset = games_subset.loc[selected_games]
    
    game_names = games_subset['Name'].tolist() if selected_tags else games_df['Name'].tolist()
    
    top_similar_games = []
    for game_name in game_names:
        idx = indices[game_name]
        sim_scores = list(enumerate(cosine_similarities[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # 가장 유사한 게임 상위 10개 선택
        top_similar_games.extend(sim_scores)
    
    top_similar_games = sorted(top_similar_games, key=lambda x: x[1], reverse=True)[:10]  # 상위 10개 추천
    game_indices = [i[0] for i in top_similar_games]
    recommendations_df = games_df.iloc[game_indices][['AppID', 'Name', 'Price', 'Developers', 'Publishers', 'Tags', 'Age_Category']]
    return recommendations_df