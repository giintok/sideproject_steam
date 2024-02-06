from gensim.models import Word2Vec
from module import tokenization
import os
import pandas as pd
import pickle

file_path = os.path.dirname(__file__)
parent_path = os.path.dirname(file_path)

#데이터 불러오기
place_df = pd.read_csv(parent_path + '\\data\\place.csv')

# 토큰화
tokenized_data = tokenization(place_df.data)

with open(parent_path + '\\data\\tokenized_data.pkl', 'wb') as file:
    pickle.dump(tokenized_data, file)

# 모델 생성 및 저장
## 오류시 pip install --upgrade gensim
model = Word2Vec(tokenized_data, vector_size=150, window=5, min_count=5, workers=4, epochs=35)
model.save(parent_path + '\\data\\word2vec_model.model')


