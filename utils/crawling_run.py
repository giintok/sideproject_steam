# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 09:38:49 2023

@author: rnjsd
"""

import crawling_model as cm
import pickle
import pandas as pd
from selenium.webdriver import Chrome   
    
#selenium 크롤링
url='https://korean.visitkorea.or.kr/list/travelinfo.do?service=ms#ms^0^1^All^All^1^^3^#%EC%84%9C%EC%9A%B8'

name_link_dict = cm.get_name_link(url)

#name_link_dict 저장하기
with open('name_link_dict.pkl', 'wb') as file:
    pickle.dump(name_link_dict, file)


#name_link_dict 불러오기
with open('name_link_dict.pkl', 'rb') as file:
    name_link_dict = pickle.load(file)
df = pd.DataFrame(columns=['name', 'sub_head', 'view_count', 'tel', 'tag', 'info', 'address'])


#크롤링
browser = Chrome() # 새로운창 안생기고 창 하나에서 작업하기위함
for name, link in name_link_dict.items():
    try:
        if name not in list(df['name']):
            df = pd.concat([df, cm.get_information(name, link, browser)], ignore_index=True)
    except KeyboardInterrupt:
        print("수동으로 실행이 중지되었습니다. 루프를 중단합니다.")
        break
    except Exception as e:
        print(f"{name} 처리 중 오류 발생: {e}")
        continue


#데이터 프레임 저장하기
with open('tag_data.pkl', 'wb') as file:
    pickle.dump(df, file)
    
#데이터 프레임 불러오기
with open('tag_data.pkl', 'rb') as file:
    df = pickle.load(file)

