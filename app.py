import streamlit as st
from page import intro
from page import page_visual_metacritic as p1
from page import page_visual_developers as p2
from page import page_visual_tags as p3
from page import page_recommendation_by_tags_ver as p4
from page import page_recommendation_by_tags_ver02 as p5
from page import page_recommendation_by_mbti as p6

st.title('Side_Project')

item_list = ['item0','item1','item2']

item_labels = {'item0':'메인', 'item1':'시각화', 'item2':'추천시스템'}

FIL = lambda x : item_labels[x]
item = st.sidebar.selectbox('Select a page',  item_list, format_func = FIL )

if item == 'item0':
	intro.app()
elif item == 'item1':
    side_select = st.sidebar.selectbox('시각화를 선택하세요.', ['시각화1', '시각화2', '시각화3'])
    if side_select == '시각화1':
        p1.app()
    elif side_select == '시각화2':
        p2.app()
    elif side_select == '시각화3':
        p3.app()
   
elif item == 'item2':
    sub_item = st.sidebar.selectbox('추천 서비스 예시', ['추천1', '추천2', '추천3'])
    if sub_item == '추천1':
        p4.app()
    elif sub_item == '추천2':
        p5.app()
    elif sub_item == '추천3':
        p6.app()
