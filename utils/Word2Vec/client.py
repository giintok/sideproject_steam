from utils.Word2Vec.module import tokenization, sort_by_similarity, find_near_place
from gensim.models import Word2Vec
import os
import pickle
import pandas as pd
#from googletrans import Translator
#from utils import naver_translate_module



path = os.path.dirname(__file__)
parent_path = os.path.dirname(path)

# 모델 불러오기
model = Word2Vec.load(parent_path + '\\data\\word2vec_model.model')

# 데이터 불러오기
place_df = pd.read_csv(parent_path + '\\data\\place.csv')
hotel_df = pd.read_csv(parent_path + '\\data\\hotel.csv')
food_df = pd.read_csv(parent_path + '\\data\\food.csv')

# 장소 , 링크 데이터 불러오기
with open(parent_path + '\\data\\name_link_dict.pkl', 'rb') as file:
    name_link_dict = pickle.load(file)

# 링크 붙이기
place_df['link'] = [name_link_dict[name] for name in place_df.name]
hotel_df['link'] = [name_link_dict[name] for name in hotel_df.name]
food_df['link'] = [name_link_dict[name] for name in food_df.name]

#토큰 가져오기
with open(parent_path + '\\data\\tokenized_data.pkl', 'rb') as file:
    tokenized_data = pickle.load(file)

def app0(user_data):
    new_df = sort_by_similarity(model, place_df, tokenized_data, user_data)
    return new_df

def app1(target_series):
    near_hotel_df = find_near_place(hotel_df, target_series)
    near_food_df = find_near_place(food_df, target_series)
    return near_hotel_df, near_food_df