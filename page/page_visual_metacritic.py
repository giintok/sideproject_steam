import streamlit as st
from utils import utils_visual_metacritic as uv_meta

def app():
    
    df = uv_meta.df
    df = uv_meta.data_EDA(df)
    
    # 선택 상자 생성
    choice = st.selectbox("Choose a graph", ["Metacritic vs. Positive", "Metacritic vs. Price", "Total Reviews vs. Metacritic"])
    
    if choice == "Metacritic vs. Positive":
        st.header("Metacritic vs. Positive")
        plot_MvsPos = uv_meta.plot_metacritic_vs_positive(df)
        st.pyplot(plot_MvsPos)
    
    elif choice == "Metacritic vs. Price":
        st.header("Metacritic vs. Price")
        plot_MvsPri = uv_meta.plot_metacritic_vs_price(df)
        st.pyplot(plot_MvsPri)
    
    elif choice == "Total Reviews vs. Metacritic":
        st.header("Total Reviews vs. Metacritic")
        plot_MvsR = uv_meta.plot_totalreviews_vs_metacritic(df)
        st.pyplot(plot_MvsR)
