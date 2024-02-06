# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:21:21 2024

@author: goldg
"""
#메타스코어를 이용한 그래프 & 랭킹

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
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

#메타스코어 0인건 삭제
def read_data(file_path):
    data = pd.read_csv(file_path)
    data = data[data['Metacritic score'] != 0]
    
    return data

#최고 동시 접속자 수와 가격을 기준으로 상위 게임을 선택하는 함수
def select_top_games(data, min_concurrent_players=0.25, min_price=50, top_n=10):
    median_concurrent_players = np.median(data['Peak CCU'])
    min_concurrent_players = median_concurrent_players * min_concurrent_players
    filtered_games = data[(data['Peak CCU'] >= min_concurrent_players) | (data['Price'] >= min_price)]
    
    return filtered_games.nlargest(top_n, 'Peak CCU')

#최상위 게임을 시각화
def visualize_top_games(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Name', y='Peak CCU', data=data, palette='viridis', ax=ax)
    ax.set_title('Top Games by Peak Concurrent Users')
    ax.set_xlabel('Game Name')
    ax.set_ylabel('Peak Concurrent Users')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')
    
    return fig

def visualize_review_rates(data):
    # 긍정 리뷰 비율 계산
    data['Positive_Rate'] = data['Positive'] / (data['Positive'] + data['Negative'])
    fig1 = px.scatter(data, x='Metacritic score', y='Positive_Rate', hover_data=['Name'], title='Metacritic Score vs Positive Rate')
    fig1.update_traces(marker=dict(color='green'), selector=dict(mode='markers'))
    fig1.update_xaxes(title_text='Metacritic Score')
    fig1.update_yaxes(title_text='Positive Rate')

    # 부정 리뷰 비율 계산
    data['Negative_Rate'] = data['Negative'] / (data['Positive'] + data['Negative'])
    fig2 = px.scatter(data, x='Metacritic score', y='Negative_Rate', hover_data=['Name'], title='Metacritic Score vs Negative Rate')
    fig2.update_traces(marker=dict(color='red'), selector=dict(mode='markers'))
    fig2.update_xaxes(title_text='Metacritic Score')
    fig2.update_yaxes(title_text='Negative Rate')

    return fig1, fig2

#개발사별 메타스코어 점수와 평균 플레이타임 랭킹
def analyze_developers(data):
    avg_score_and_info = data.groupby('Developers').agg(
        Mean_Metacritic_Score=('Metacritic score', 'mean'),
        Games=('Name', lambda x: ', '.join(x)),
        Prices=('Price', lambda x: ', '.join(x.astype(str)))
    ).sort_values(by='Mean_Metacritic_Score', ascending=False)
    
    # 인덱스명 수정
    avg_score_and_info.index.names = ['Developers']
    
    return avg_score_and_info
