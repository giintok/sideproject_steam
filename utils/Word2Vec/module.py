from konlpy.tag import Okt
import pandas as pd
import os
import pickle
#from googletrans import Translator
from haversine import haversine
from utils import naver_translate_module

path = os.path.dirname(__file__)
parent_path = os.path.dirname(path)

#사용자에게 보여줄 태그 불러오기
def show_tag(country_code):
    with open(parent_path + '\\data\\user_choice.txt', 'r', encoding='utf-8') as file:
        choice_list=[]
        lines = file.readlines()
        for line in lines:
            choice_list.extend(line.replace("'", '').replace(' ', '').split(','))
        choice_list = list(set(choice_list))
    if country_code != 'ko':
        korean_to_target_list = [naver_translate_module.translate(text, 'ko', country_code)['message']['result']['translatedText'] for text in choice_list]
        target_to_korean_dict = {target:base for base, target in zip(choice_list, korean_to_target_list)}
        return korean_to_target_list, target_to_korean_dict
    else:
        return choice_list, None
#불용어
def call_stopwords():
    with open(parent_path + '\\data\\stopwords.txt', 'r', encoding='utf-8') as file:
        word_list=[]
        lines = file.readlines()
        for line in lines:
            word_list.extend(line.replace("'", '').replace(' ', '').split(','))
    word_list = list(set(word_list))
    word_list.remove('')
    return word_list

# 토큰화
def tokenization(data):
    stopwords = call_stopwords()
    okt = Okt()
    if isinstance(data, pd.Series):
        data = data.str.replace(r'[^A-Za-zㄱ-ㅎㅏ-ㅣ가-힣 ]', '', regex=True)
        tokenized_data = []
        for sentence in data:
            tokens = okt.morphs(sentence, stem=True)
            stopwords_remove_tokens = [token for token in tokens if not token in stopwords]
            tokenized_data.append(stopwords_remove_tokens)
    return tokenized_data

# 유사도 가장 높은 장소 3곳
def sort_by_similarity(model, df, tokenized_data, user_data):
    sim_list = []
    for data in tokenized_data:
        sim_list.append(model.wv.n_similarity(data, user_data))
    df['similarity'] = sim_list
    return df.sort_values(by='similarity', ascending=False, ignore_index=True).loc[:, ['name', 'Latitude', 'Longitude', 'link']]

# 거리가 가까운곳 3곳 찾기
def find_near_place(base, target):
    # base is pd.DataFrame
    # target is pd.Series
    distance_list = []
    for lat, long in zip(base.Latitude, base.Longitude):
        distance_list.append(round(haversine((lat, long), (target.Latitude, target.Longitude)), 2))
    base['distance_by_target'] = distance_list
    sort_by_distance_df = base.sort_values(by='distance_by_target').reset_index(drop=True)
    return sort_by_distance_df.iloc[:3]