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
file_paths = os.path.join(basic_file_path, 'games_final_final.csv')
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


# 상위 N개의 장르를 가장 많이 포함하는 게임 찾기
def find_top_games_with_details_by_genre(games_teg_df, genres_count, top_n=10):
    top_genres_games = {}
    for genre in genres_count.head(top_n).index:
        genre_mask = games_teg_df['Genres'].apply(lambda x: genre in x if isinstance(x, list) else False)
        top_genres_games[genre] = games_teg_df[genre_mask].head(5)

    df_result = pd.DataFrame()

    for genre, games_df in top_genres_games.items():
        df_result[f'{genre}_Positive'] = games_df['Positive'].astype(str) + ' (' + games_df['Name'] + ')'
        df_result[f'{genre}_Negative'] = games_df['Negative'].astype(str) + ' (' + games_df['Name'] + ')'
        df_result[f'{genre}_Avg_Playtime'] = games_df['Average playtime forever'].astype(str) + ' (' + games_df['Name'] + ')'
        df_result[f'{genre}_Median_Playtime'] = games_df['Median playtime forever'].astype(str) + ' (' + games_df['Name'] + ')'

    return df_result

#상위 N개의 장르를 가장 많이 포함하는 게임 찾기
def plot_top_genre_games(genres_count, games_teg_df, top_n=5):
    top_genres_games = {}
    for genre in genres_count.head(top_n).index:
        genre_mask = games_teg_df['Genres'].apply(lambda x: genre in x if isinstance(x, list) else False)
        top_genres_games[genre] = games_teg_df[genre_mask].head(5)

    fig, axes = plt.subplots(nrows=top_n, ncols=4, figsize=(20, 10), sharex=True)

    for i, (genre, games_df) in enumerate(top_genres_games.items()):
        axes[i, 0].barh(games_df['Name'], games_df['Positive'])
        axes[i, 0].set_title(f'{genre} - Positive')

        axes[i, 1].barh(games_df['Name'], games_df['Negative'])
        axes[i, 1].set_title(f'{genre} - Negative')

        axes[i, 2].barh(games_df['Name'], games_df['Average playtime forever'])
        axes[i, 2].set_title(f'{genre} - Avg Playtime')

        axes[i, 3].barh(games_df['Name'], games_df['Median playtime forever'])
        axes[i, 3].set_title(f'{genre} - Median Playtime')

    plt.tight_layout()
    return fig
