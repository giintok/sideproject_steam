import streamlit as st
from page import project1 as p1
from page import project2 as p2
from page import intro

st.title('Project')

item_list = ['item0','item1', 'item2']

item_labels = {'item0':'ChatBot', 'item1':'page1', 'item2':'page2'}

FIL = lambda x : item_labels[x]
item = st.sidebar.selectbox('Select a page',  item_list, format_func = FIL )
#item = st.sidebar.selectbox('항목을 골라요.',  item_list)

if item == 'item1':
	p1.app()
elif item == 'item2':
	p2.app()
elif item == 'item0':
	intro.app()
