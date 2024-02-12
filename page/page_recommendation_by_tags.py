# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:57:49 2024

@author: goldg
"""

import streamlit as st
from utils import utils_recommendation_by_tags as ut7

games_df = ut7.games_df

def app():
    st.title("게임 추천 시스템")

    # 사용자가 선택할 수 있는 장르 목록 생성
    tags = games_df['Tags'].explode().unique()
    
    # 각각의 장르에 대한 셀렉트 박스 생성
    selected_genre1 = st.selectbox("1번째 테그를 선택하세요:", tags)
    selected_genre2 = st.selectbox("2번째 테그를 선택하세요:", tags)
    selected_genre3 = st.selectbox("3번째 테그를 선택하세요:", tags)

    selected_genres = [selected_genre1, selected_genre2, selected_genre3]
    selected_genres = [genre for genre in selected_genres if genre]  # None 값을 필터링

    if selected_genres:
        tfidf_matrix = ut7.process_data_by_tags(games_df, top_n=30)
        indices = ut7.get_indices(games_df)
        cosine_similarities = ut7.compute_similarity(tfidf_matrix)
        recommendations = ut7.get_top_similar_games_by_tags(selected_genres, games_df, cosine_similarities, indices)
        st.write("추천하는 게임:")
        
        st.dataframe(recommendations)
    else:
        st.write("테그를 선택하세요.")

if __name__ == "__main__":
    app()