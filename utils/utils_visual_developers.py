# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 17:13:37 2024

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
df = pd.read_csv(file_paths)

def calculate_playtime_stats(df):
    dev_avg_playtime = df.groupby('Developers')['Average playtime forever'].mean()
    dev_med_playtime = df.groupby('Developers')['Median playtime forever'].mean()
    pub_avg_playtime = df.groupby('Publishers')['Average playtime forever'].mean()
    pub_med_playtime = df.groupby('Publishers')['Median playtime forever'].mean()
    return dev_avg_playtime, dev_med_playtime, pub_avg_playtime, pub_med_playtime

def plot_playtime_stats(dev_avg_playtime, dev_med_playtime, pub_avg_playtime, pub_med_playtime):
    fig, ax = plt.subplots(2, 2, figsize=(20, 10))

    ax[0, 0].bar(dev_avg_playtime[:10].index, dev_avg_playtime[:10])
    ax[0, 0].set_title('Developers Average playtime')
    ax[0, 0].set_xlabel('Developers')
    ax[0, 0].set_ylabel('Average playtime')
    ax[0, 0].tick_params(axis='x', rotation=90)

    ax[0, 1].bar(dev_med_playtime[:10].index, dev_med_playtime[:10])
    ax[0, 1].set_title('Developers Median playtime')
    ax[0, 1].set_xlabel('Developers')
    ax[0, 1].set_ylabel('Median playtime')
    ax[0, 1].tick_params(axis='x', rotation=90)

    ax[1, 0].bar(pub_avg_playtime[:10].index, pub_avg_playtime[:10])
    ax[1, 0].set_title('Publishers Average playtime')
    ax[1, 0].set_xlabel('Publishers')
    ax[1, 0].set_ylabel('Average playtime')
    ax[1, 0].tick_params(axis='x', rotation=90)

    ax[1, 1].bar(pub_med_playtime[:10].index, pub_med_playtime[:10])
    ax[1, 1].set_title('Publishers Median playtime')
    ax[1, 1].set_xlabel('Publishers')
    ax[1, 1].set_ylabel('Median playtime')
    ax[1, 1].tick_params(axis='x', rotation=90)

    plt.tight_layout()
    
    return fig

def top_developers_by_playtime(df, n=10):
    dev_playtime = df.groupby('Developers').agg({'Average playtime forever': 'mean', 'Name': 'first'}).reset_index()
    top_devs = dev_playtime.nlargest(n, 'Average playtime forever')
    return top_devs

def find_games_by_developer(df, developer):
    games = df[df['Developers'] == developer]['Name']
    return games