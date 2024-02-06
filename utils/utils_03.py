# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:17:06 2024

@author: goldg
"""

import pandas as pd
import matplotlib.pyplot as plt
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
games_age_df = pd.read_csv(file_paths)

def plot_age_metrics(games_age_df):

    age_playtime = games_age_df.groupby('Age_Category')['Average playtime forever'].mean()
    age_ccu = games_age_df.groupby('Age_Category')['Peak CCU'].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(age_playtime.index, age_playtime.values, label='average playtime')
    ax.plot(age_ccu.index, age_ccu.values, marker='o', color='red', label='peak ccu')
    ax.set_xlabel('age')
    ax.set_ylabel('mean value')
    ax.set_title('Age Metrics')
    ax.legend()

    return fig

def plot_expensive_games(games_age_df):
    games_age_df['Positive_Rate'] = games_age_df['Positive'] / (games_age_df['Positive'] + games_age_df['Negative'])
    games_age_df['Total Reviews'] = games_age_df['Positive'] + games_age_df['Negative']
    top_expensive_games = games_age_df.sort_values(by='Total Reviews', ascending=False).head(100)
    fig = px.scatter(top_expensive_games, x='Price', y='Positive_Rate', size='Total Reviews', hover_data=['Name'])
    return fig
