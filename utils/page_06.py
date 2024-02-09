# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 10:17:12 2024

@author: goldg
"""

import streamlit as st
from utils import utils_06 as ut6

games_df = ut6.games_df

def app():
    st.title("게임 추천 시스템")

    # 사용자가 선택할 수 있는 장르 목록 생성
    genres = games_df['Genres'].explode().unique()
    
    # 각각의 장르에 대한 셀렉트 박스 생성
    selected_genre1 = st.selectbox("1번째 장르를 선택하세요:", genres)
    selected_genre2 = st.selectbox("2번째 장르를 선택하세요:", genres)
    selected_genre3 = st.selectbox("3번째 장르를 선택하세요:", genres)

    selected_genres = [selected_genre1, selected_genre2, selected_genre3]
    selected_genres = [genre for genre in selected_genres if genre]  # None 값을 필터링

    if selected_genres:
        tfidf_matrix = ut6.process_data(games_df)
        indices = ut6.get_indices(games_df)
        cosine_similarities = ut6.compute_similarity(tfidf_matrix)
        recommendations = ut6.get_top_similar_games(selected_genres, games_df, cosine_similarities, indices)
        st.write("추천하는 게임:")
        
        st.dataframe(recommendations)
    else:
        st.write("장르를 선택하세요.")


if __name__ == "__main__":
    app()
