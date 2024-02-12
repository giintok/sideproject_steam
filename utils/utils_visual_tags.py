# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:07:45 2024

@author: goldg
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib import font_manager, rc

basic_path = os.path.dirname(__file__)
basic_file_path = os.path.join(basic_path, 'data')

# 한글 폰트 설정
font_path = basic_file_path + '\\NanumGothic.ttf'  # 폰트 파일의 경로
fontprop = font_manager.FontProperties(fname=font_path)
rc('font', family=fontprop.get_name())

# 게임 파일 경로
file_paths = os.path.join(basic_file_path, 'final_dataset.csv')
games_teg_df = pd.read_csv(file_paths)

def plot_top_genres_and_tags(games_teg_df, top_n=10):
    # 각 장르와 태그의 빈도수 계산
    games_teg_df['Genres'] = games_teg_df['Genres'].apply(lambda x: x.strip('[]').split(','))
    games_teg_df['Tags'] = games_teg_df['Tags'].apply(lambda x: x.strip('[]').split(','))
   
    all_genres = [item for sublist in games_teg_df['Genres'] for item in sublist]
    all_tags = [item for sublist in games_teg_df['Tags'] for item in sublist]
    genres_count = pd.Series(all_genres).value_counts()
    tags_count = pd.Series(all_tags).value_counts()
    
    # 상위 N개의 장르와 태그를 그래프로 표시
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # 상위 N개의 장르를 그래프로 표시
    genres_count.head(top_n).plot(kind='barh', color='skyblue', ax=ax[0])
    ax[0].set_title('Top Genres')
    ax[0].set_xlabel('Count')

    # 상위 N개의 태그를 그래프로 표시
    tags_count.head(top_n).plot(kind='barh', color='lightcoral', ax=ax[1])
    ax[1].set_title('Top Tags')
    ax[1].set_xlabel('Count')

    plt.tight_layout()
    
    return fig, genres_count, tags_count

def plot_top_tags_games(games_teg_df, top_n=5):
    # 태그별 게임 수집
    tag_games_count = {}

    for index, row in games_teg_df.iterrows():
        tags = row['Tags']
        for tag in tags:
            if tag in tag_games_count:
                tag_games_count[tag].append(row['Name'])
            else:
                tag_games_count[tag] = [row['Name']]

    # 가장 많이 포함된 태그 순으로 정렬
    sorted_tags = sorted(tag_games_count.items(), key=lambda x: len(x[1]), reverse=True)

    # 상위 N개의 태그를 가장 많이 포함하는 게임 출력
    top_tags_games = {}
    for i in range(top_n):
        tag, games = sorted_tags[i]
        top_tags_games[tag] = games

    return top_tags_games

def top_games_for_selected_tag(games_teg_df, selected_tag, top_n=50):
    # 선택된 테그가 포함된 게임 필터링
    filtered_games = games_teg_df[games_teg_df['Tags'].apply(lambda x: selected_tag in x)]

    # 선택된 테그를 가장 많이 포함하는 상위 N개의 게임 반환
    top_games = filtered_games.head(top_n)

    return top_games