# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 20:40:33 2024

@author: goldg
"""

import pandas as pd
import ast
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud
from matplotlib import font_manager, rc
from collections import Counter

basic_path = os.path.dirname(__file__)
basic_file_path = os.path.join(basic_path, 'data')

# 한글 폰트 설정
font_path = basic_file_path + '\\NanumGothic.ttf'  # 폰트 파일의 경로
fontprop = font_manager.FontProperties(fname=font_path)
rc('font', family=fontprop.get_name())

# 게임 파일 경로
file_paths = os.path.join(basic_file_path, 'final_dataset.csv')
df = pd.read_csv(file_paths)


def data_EDA(df):
    genres_list = df['Genres'].apply(ast.literal_eval).sum()
    tags_list = df['Tags'].apply(ast.literal_eval).sum()
    top_genres = Counter(genres_list).most_common(10)
    top_tags = Counter(tags_list).most_common(10)
    
    return top_genres, top_tags

def plot_top10(top_genres, top_tags):
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    
    genres, counts = zip(*top_genres)
    ax[0].bar(genres, counts)
    ax[0].set_ylabel('Frequency')
    ax[0].set_xlabel('Genres')
    ax[0].set_title('Top 10 Genres')
    ax[0].tick_params(axis='x', rotation=45)

    tags, counts = zip(*top_tags)
    ax[1].bar(tags, counts)
    ax[1].set_ylabel('Frequency')
    ax[1].set_xlabel('Tags')
    ax[1].set_title('Top 10 Tags')
    ax[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    
    return fig

def generate_and_display_wordcloud(df):
    # 'Tags' 열을 파이썬 리스트로 변환
    df['Tags'] = df['Tags'].apply(ast.literal_eval)

    # 모든 태그를 하나의 리스트로 결합
    all_tags = [tag for tags in df['Tags'] for tag in tags]

    # 태그들을 하나의 텍스트로 결합
    tags_text = ' '.join(all_tags)

    # 워드 클라우드 생성
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(tags_text)

    # 워드 클라우드 시각화
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    return fig
