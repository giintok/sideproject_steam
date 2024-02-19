# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 20:29:04 2024

@author: goldg
"""

import streamlit as st
from utils import utils_visual_total_review as uv_review

def app():
    
    df = uv_review.df
    df = uv_review.data_EDA(df)
    
    # 선택 상자 생성
    choice = st.selectbox("Choose a graph", ["Metacritic vs. Positive", "Metacritic vs. Price", "Positive vs. Price"])
    
    if choice == "Metacritic vs. Positive":
        st.header("Metacritic vs. Positive")
        plot_RvsPo = uv_review.plot_metacritic_vs_positive(df)
        st.pyplot(plot_RvsPo)
    
    elif choice == "Metacritic vs. Price":
        st.header("Metacritic vs. Price")
        plot_RvsPri = uv_review.plot_metacritic_vs_Price(df)
        st.pyplot(plot_RvsPri)
    
    elif choice == "Positive vs. Price":
        st.header("Positive vs. Price")
        plot_PovsPri = uv_review.plot_positive_vs_Price(df)
        st.pyplot(plot_PovsPri) 
