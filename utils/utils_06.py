# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 10:17:06 2024

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
games_df['Genres'] = games_df['Genres'].apply(lambda x: eval(x))

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

def get_top_similar_games(selected_genres, games_df, cosine_similarities, indices):
    games_subset = games_df.copy()
    if selected_genres:
        for genre in selected_genres:
            games_subset = games_subset[games_subset['Genres'].apply(lambda x: genre in x)]
    
    game_names = games_subset['Name'].tolist() if selected_genres else games_df['Name'].tolist()
    
    top_similar_games = []
    for game_name in game_names:
        idx = indices[game_name]
        sim_scores = list(enumerate(cosine_similarities[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # 가장 유사한 게임 상위 10개 선택
        top_similar_games.extend(sim_scores)
    
    top_similar_games = sorted(top_similar_games, key=lambda x: x[1], reverse=True)[:10]  # 상위 10개 추천
    game_indices = [i[0] for i in top_similar_games]
    recommendations_df = games_df.iloc[game_indices][['AppID', 'Name', 'Price', 'Developers', 'Publishers', 'Genres', 'Age_Category']]
    return recommendations_df