import streamlit as st
from page import intro
from page import page_visual_metacritic as pv1
from page import page_visual_total_review as pv2
from page import page_visual_tag_genres_count as pv3
from page import page_recommendation_by_tags_top30 as pr4
from page import page_recommendation_by_tags_select as pr5

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
        pv1.app()
    elif side_select == '시각화2':
        pv2.app()
    elif side_select == '시각화3':
        pv3.app()
   
elif item == 'item2':
    sub_item = st.sidebar.selectbox('추천 서비스 예시', ['추천1', '추천2'])
    if sub_item == '추천1':
        pr4.app()
    elif sub_item == '추천2':
        pr5.app()
