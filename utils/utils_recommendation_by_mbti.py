# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 17:02:09 2024

@author: goldg
"""

import pandas as pd
import os

basic_path = os.path.dirname(__file__)
basic_file_path = os.path.join(basic_path, 'data')

# 게임 파일 경로
file_path = os.path.join(basic_file_path, 'final_dataset.csv')
games_df = pd.read_csv(file_path)

# 장르를 리스트로 변환하고 쉼표로 구분하는 전처리
games_df['Tags'] = games_df['Tags'].apply(lambda x: eval(x))

# MBTI 유형과 게임 장르 매핑 정보
mbti_genre_mapping = {
    'ISTJ': ['Strategy', 'Realistic', 'Economy', 'Simulation'],
    'ISFJ': ['Immersive Sim', 'Romance', 'Family Friendly', 'Puzzle-Platformer'],
    'INFJ': ['Thriller', 'Horror', 'Abstract', 'Mystery', 'Choices Matter'],
    'INTJ': ['Realistic', 'Strategy RPG', 'Tactical RPG', 'Futuristic', 'Cyberpunk', 'Crafting'],
    'ISTP': ['Action', 'Adventure', 'Open World'],
    'ISFP': ['Cute', 'Card Game', 'Character Customization', 'Cartoon', 'Comic Book'],
    'INFP': ['Emotional', 'Mystery', 'Story Rich', 'Design & Illustration'],
    'INTP': ['Puzzle', 'Strategy', 'Exploration', 'Choices Matter'],
    'ESTP': ['Sports', 'Action-Adventure', 'Economy', 'Racing'],
    'ESFP': ['Action', 'Party Game', 'Music', 'Rhythm'],
    'ENFP': ['Adventure', 'Fantasy', 'Colorful', 'Emotional'],
    'ENTP': ['Open World', 'Strategy RPG', 'Tactical RPG', 'Puzzle', 'Experimental'],
    'ESTJ': ['War', 'Wargame', 'Tactical', 'Strategy'],
    'ESFJ': ['Immersive Sim', 'Romance', 'Family Friendly', 'Puzzle-Platformer'],
    'ENFJ': ['MMORPG', 'Cooperative', 'PvP', 'Multiplayer'],
    'ENTJ': ['Strategy', 'Strategy', 'Management', 'Simulation']
}

def recommend_games_by_mbti(mbti_type, games_df, columns=None, max_games=20):
    # MBTI 유형에 해당하는 게임 장르 리스트 가져오기
    genres_for_mbti = mbti_genre_mapping.get(mbti_type, [])
    
    # 사용자가 선택한 MBTI 유형에 대응하는 게임 추출
    matched_games = games_df[games_df['Tags'].apply(lambda x: any(tag in genres_for_mbti for tag in x))]
    
    '''
    # 사용자가 지정한 컬럼만 선택
    if columns:
        matched_games = matched_games[columns]
    '''
    
    # 최대 max_games 수만큼 게임 추천
    matched_games = matched_games.head(max_games)
    
    return matched_games
