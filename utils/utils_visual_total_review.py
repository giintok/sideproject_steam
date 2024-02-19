# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 20:21:28 2024

@author: goldg
"""
# 총 리뷰 수(긍정+부정) 과 긍정 비율, 가격 / 긍정 비율 vs 가격 시각화

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
df = pd.read_csv(file_paths)

def data_EDA(df):
    df['Total_Reviews'] = df['Positive'] + df['Negative']
    df['Log_Total_Reviews'] = np.log1p(df['Total_Reviews'])
    df['Positive_ratio'] = df['Positive'] / (df['Positive'] + df['Negative'])
    
    return df

# Total reviews vs Positive Ratio 시각화
def plot_metacritic_vs_positive(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='Log_Total_Reviews', y='Positive_ratio', alpha=0.5, ax=ax)
    ax.set_title('Total reviews count vs Positive ratio')
    ax.set_xlabel('Total reviews count')
    ax.set_ylabel('Positive Ratio')
    ax.grid(True)
    
    return fig

# Total reviews vs Price 시각화
def plot_metacritic_vs_Price(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='Log_Total_Reviews', y='Price', alpha=0.5, ax=ax)
    ax.set_title('Total reviews count vs Price')
    ax.set_xlabel('Total reviews count')
    ax.set_ylabel('Price')
    ax.grid(True)
    
    return fig

# Positive Ratio vs Price 시각화
def plot_positive_vs_Price(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='Positive_ratio', y='Price', alpha=0.5, ax=ax)
    ax.set_title('Positive ratio vs Price')
    ax.set_xlabel('Positive Rati')
    ax.set_ylabel('Price')
    ax.grid(True)
    
    return fig
