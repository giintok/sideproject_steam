import streamlit as st
from page import intro
from page import page_01 as p1
from page import page_02 as p2
from page import page_03 as p3
from page import page_04 as p4
from page import page_05 as p5

st.title('Side_Project')

item_list = ['item0','item1','item2']

item_labels = {'item0':'메인', 'item1':'추천시스템', 'item2':'시각화'}

FIL = lambda x : item_labels[x]
item = st.sidebar.selectbox('Select a page',  item_list, format_func = FIL )

if item == 'item0':
	intro.app()
elif item == 'item1':
	p5.app()
elif item == 'item2':
    side_select = st.sidebar.selectbox('시각화를 선택하세요.', ['시각화1', '시각화2', '시각화3', '시각화4'])
    if side_select == '시각화1':
        p1.app()
    elif side_select == '시각화2':
        p2.app()
    elif side_select == '시각화3':
        p3.app()
    elif side_select == '시각화4':
        p4.app()