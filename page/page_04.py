# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:08:35 2024

@author: goldg
"""

import streamlit as st
from utils import utils_04 as ut4

games_teg_df = ut4.games_teg_df

plot01, genres_count, tags_count = ut4.plot_top_genres_and_tags(games_teg_df, top_n=10)
df_result = ut4.find_top_games_with_details_by_genre(games_teg_df, genres_count, top_n=10)
plot02 = ut4.plot_top_genre_games(genres_count, games_teg_df)

def app():
    st.pyplot(plot01)
    st.dataframe(df_result)
    st.pyplot(plot02)
