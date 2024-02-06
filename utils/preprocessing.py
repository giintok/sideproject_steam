import pandas as pd
import numpy as np
import pickle
import os

file_path = os.path.dirname(__file__)
print(file_path)
# 데이터 불러오기
with open(file_path + '\\data\\tag_data.pkl', 'rb') as file:
    df = pickle.load(file)

# 조회수 1사분위수 이하 잘라내기
Q1 = np.quantile(df.view_count, 0.25)
df = df[df.view_count > Q1]

#외국인 방문 횟수 top.5 인  강남구, 송파구, 서초구, 중구, 종로구 추출
idx_list = []
for idx, adr in enumerate(df.address):
    if '강남구' in adr:
        idx_list.append(idx)
    elif '송파구' in adr:
        idx_list.append(idx)
    elif '서초구' in adr:
        idx_list.append(idx)
    elif '중구' in adr:
        idx_list.append(idx)
    elif '종로구' in adr:
        idx_list.append(idx)
df = df.iloc[idx_list].sort_values(by='view_count', ascending=False, ignore_index=True)

# 숙박, 숙소, 음식 태그를 가진 장소들은 잘라내고 (숙박, 숙소) , (음식) 이렇게 새로운 데이터 생성
hotel_idx_list = []
food_idx_list = []
place_idx_list = []
for idx, tag in enumerate(df.tag):
    if '숙박' in tag:
        hotel_idx_list.append(idx)
    elif '숙소' in tag:
        hotel_idx_list.append(idx)
    elif '음식' in tag:
        food_idx_list.append(idx)
    else:
        place_idx_list.append(idx)

hotel_df = df.iloc[hotel_idx_list].sort_values(by='view_count', ascending=False, ignore_index=True)
food_df = df.iloc[food_idx_list].sort_values(by='view_count', ascending=False, ignore_index=True)
place_df = df.iloc[place_idx_list].sort_values(by='view_count', ascending=False, ignore_index=True)

place_df['data'] = place_df.tag + ', '+ place_df.sub_head + ', ' + place_df['info']

def to_csv():
    place_df.to_csv(file_path + '\\data\\place_df.csv', index=False)
    hotel_df.to_csv(file_path + '\\data\\hotel_df.csv', index=False)
    food_df.to_csv(file_path + '\\data\\food_df.csv', index=False)
    
