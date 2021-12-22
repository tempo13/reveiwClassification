"""
https://wikidocs.net/94600 를 참고하여 만들었습니다.
"""
import os
import re
import pandas as pd
import numpy as np
from konlpy.tag import Mecab
import sklearn
from crawl_utils.crawl_util import save_file

from analyze_utils import config as c
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, GRU
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint



class GenderTraining:

    def __init__(self):
        self.mecab = Mecab(c.MECAB_PATH)
        self.stopwords = c.STOP_WORDS

    @staticmethod
    def below_threshold_len(max_len, nested_list):
        count = 0
        for sentence in nested_list:
            if (len(sentence) <= max_len):
                count = count + 1
        max_length, rate = max_len, (count / len(nested_list)) * 100
        print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s' % (max_len, (count / len(nested_list)) * 100))
        if rate >= 99.9:
            return True
        else:
            return False


    def create_model(self, df, content_col, label_col):
        data = sklearn.utils.shuffle(df)
        mecab = self.mecab
        data[content_col] = data[content_col].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
        data[content_col].replace('', np.nan, inplace=True)
        print(data.isnull().sum())


        train_data = data.dropna()
        train_data['tokenized'] = train_data[content_col].apply(mecab.morphs)
        train_data['tokenized'] = train_data['tokenized'].apply(
            lambda x: [item for item in x if item not in self.stopwords]
        )


        X_train = train_data['tokenized'].values
        y_train = train_data[label_col].values

        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(X_train)

        threshold = 2
        total_cnt = len(tokenizer.word_index)  # 단어의 수
        rare_cnt = 0  # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
        total_freq = 0  # 훈련 데이터의 전체 단어 빈도수 총 합
        rare_freq = 0  # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

        # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
        for key, value in tokenizer.word_counts.items():
            total_freq = total_freq + value

            # 단어의 등장 빈도수가 threshold보다 작으면
            if (value < threshold):
                rare_cnt = rare_cnt + 1
                rare_freq = rare_freq + value

        print('단어 집합(vocabulary)의 크기 :', total_cnt)
        print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s' % (threshold - 1, rare_cnt))
        print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt) * 100)
        print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq) * 100)

        # 전체 단어 개수 중 빈도수 2이하인 단어 개수는 제거.
        # 0번 패딩 토큰과 1번 OOV 토큰을 고려하여 +2
        vocab_size = total_cnt - rare_cnt + 2
        print('단어 집합의 크기 :', vocab_size)

        tokenizer = Tokenizer(vocab_size, oov_token='OOV')
        tokenizer.fit_on_texts(X_train)
        X_train = tokenizer.texts_to_sequences(X_train)

        max_len = 80
        is_next = True
        while is_next:
            is_max = self.below_threshold_len(max_len, X_train)
            is_next = False if is_max else True
            max_len += 10

        X_train = pad_sequences(X_train, maxlen=max_len)

        embedding_dim = 100
        hidden_units = 128

        model = Sequential()
        model.add(Embedding(vocab_size, embedding_dim))
        model.add(GRU(hidden_units))
        model.add(Dense(1, activation='sigmoid'))

        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
        mc = ModelCheckpoint(os.path.join(os.path.dirname(__file__), 'best_model.h5'), monitor='val_acc', mode='max',
                             verbose=1, save_best_only=True)

        model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
        history = model.fit(X_train, y_train, epochs=15, callbacks=[es, mc], batch_size=64, validation_split=0.2)
        save_params = {
            'tokenizer': tokenizer, 'max_len': max_len, 'model': 'best_model.h5'
        }
        save_file(save_params, os.path.join(os.path.dirname(__file__),'model_config.pickle'))


if __name__ == '__main__':
    """
    train data 는 'review', 'gender(Label)' , 'review_id' 로 구성되어 있습니다. 
    """
    train_data = pd.read_csv('../data/train_data.csv')
    t = GenderTraining()
    t.create_model(train_data, 'review', 'gender')