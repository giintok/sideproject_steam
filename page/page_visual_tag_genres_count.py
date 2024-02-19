# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 20:59:52 2024

@author: goldg
"""

import streamlit as st
from utils import utils_visual_tag_genres_count as uv_top10

def app():
    
    df = uv_top10.df
    top_genres, top_tags = uv_top10.data_EDA(df)
    
    plot_top10 = uv_top10.plot_top10(top_genres, top_tags)
    st.pyplot(plot_top10)
    
    st.markdown("---")
    
    word_crowd = uv_top10.generate_and_display_wordcloud(df)
    st.pyplot(word_crowd)