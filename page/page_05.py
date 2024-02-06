# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 21:45:49 2024

@author: goldg
"""

import streamlit as st
from utils import utils_05 as ut5

games_df = ut5.games_df
tfidf_matrix = ut5.process_data(games_df)
indices = ut5.get_indices(games_df)
cosine_similarities = ut5.compute_similarity(tfidf_matrix)

def get_recommendations(game_name, games_df, cosine_similarities, indices):
    idx = indices[game_name]
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # 상위 10개 추천
    game_indices = [i[0] for i in sim_scores]
    recommendations_df = games_df.iloc[game_indices][['Name', 'AppID', 'Price']]
    return recommendations_df

def app():
    st.title("게임 추천 시스템")

    # 사용자가 선택할 수 있는 게임명 목록 생성
    game_names = games_df['Name'].tolist()
    selected_game_name = st.selectbox("추천을 받고 싶은 게임명을 선택하세요:", game_names)

    if selected_game_name:
        recommendations = get_recommendations(selected_game_name, games_df, cosine_similarities, indices)
        st.write(f"게임 '{selected_game_name}'에 대한 추천 게임:")
        st.dataframe(recommendations)

if __name__ == "__main__":
    app()