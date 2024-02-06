# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 17:13:38 2024

@author: goldg
"""

import streamlit as st
from utils import utils_02 as ut2

df = ut2.df
dev_avg_playtime, dev_med_playtime, pub_avg_playtime, pub_med_playtime = ut2.calculate_playtime_stats(df)
plot01 = ut2.plot_playtime_stats(dev_avg_playtime, dev_med_playtime, pub_avg_playtime, pub_med_playtime)
top_devs = ut2.top_developers_by_playtime(df)


def app():
    st.pyplot(plot01)
    # 플레이 타임별 상위 개발사
    st.subheader("Top Developers by Playtime")
    st.write(top_devs)

    # 상위 개발사의 게임 목록
    st.subheader("Games by Top Developers")
    selected_dev = st.selectbox("Select a developer", top_devs)
    games = ut2.find_games_by_developer(df, selected_dev)
    st.write(games)