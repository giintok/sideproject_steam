# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 21:45:31 2024

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

def process_data(games_df):
    games_df = games_df.fillna('')
    features = ['Genres', 'Tags', 'About the game']
    games_df['combined_features'] = games_df[features].apply(lambda x: ' '.join(x), axis=1)
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(games_df['combined_features'])
    return tfidf_matrix

def get_indices(games_df):
    indices = pd.Series(games_df.index, index=games_df['Name']).drop_duplicates()
    return indices

def compute_similarity(tfidf_matrix):
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_similarities
