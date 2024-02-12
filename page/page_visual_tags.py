# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:08:35 2024

@author: goldg
"""

import streamlit as st
import pandas as pd
from utils import utils_visual_tags as ut4

games_teg_df = ut4.games_teg_df

plot01, genres_count, tags_count = ut4.plot_top_genres_and_tags(games_teg_df, top_n=10)
top_tags_games = ut4.plot_top_tags_games(games_teg_df, top_n=5)

def app():
    st.pyplot(plot01)
    st.write(top_tags_games)
    selected_tag = st.selectbox("Select a tag", pd.Series([tag for tags in games_teg_df['Tags'] for tag in tags]).unique())
    top_games_df = ut4.top_games_for_selected_tag(games_teg_df, selected_tag)
    st.write(top_games_df)