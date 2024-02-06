# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:32:23 2024

@author: goldg
"""

import streamlit as st
from utils import utils_01 as ut1

data = ut1.read_data(ut1.file_paths)
top_games_data = ut1.select_top_games(data)
plot01 = ut1.visualize_top_games(top_games_data)

positive_rate_fig, negative_rate_fig = ut1.visualize_review_rates(data)

avg_score_and_info = ut1.analyze_developers(data)


def app():
    st.subheader('Top Games Visualization')
    st.pyplot(plot01)
    st.plotly_chart(positive_rate_fig)
    st.plotly_chart(negative_rate_fig)
    st.write(avg_score_and_info)
    st.write('''
             가나다라마바사
             ''')