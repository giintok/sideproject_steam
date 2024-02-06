# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:17:28 2024

@author: goldg
"""

import streamlit as st
from utils import utils_03 as ut3

games_age_df = ut3.games_age_df

plot01 = ut3.plot_age_metrics(games_age_df)
plot02 = ut3.plot_expensive_games(games_age_df)

def app():
    st.pyplot(plot01)
    st.plotly_chart(plot02)