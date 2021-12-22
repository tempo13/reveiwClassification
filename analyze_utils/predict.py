from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from analyze_utils import config as c
from konlpy.tag import Mecab
import re


class GenderPredict:

    def __init__(self, model_file, tokenizer, max_len):
        self.loaded_model = load_model(model_file)
        self.mecab = Mecab(c.MECAB_PATH)
        self.stopwords = c.STOP_WORDS
        self.tokenizer = tokenizer
        self.max_len = max_len

    def gender_predict(self, new_sentence):
        new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', new_sentence)
        new_sentence = self.mecab.morphs(new_sentence)  # 토큰화
        new_sentence = [word for word in new_sentence if not word in self.stopwords]  # 불용어 제거
        encoded = self.tokenizer.texts_to_sequences([new_sentence])  # 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen=self.max_len)  # 패딩

        score = float(self.loaded_model.predict(pad_new))  # 예측
        if (score > 0.5):
            print("{:.2f}% 확률로 여성 리뷰입니다.".format(score * 100))
        else:
            print("{:.2f}% 확률로 남성 리뷰입니다.".format((1 - score) * 100))