"""
해당 파일을 import 하여 predict를 진행합니다.
"""
from analyze_utils import predict as p
import os
import pickle

pickle_file = os.path.join(os.path.dirname(__file__),'model_config.pickle')
with open(pickle_file, 'rb') as f:
    params = pickle.load(f)

model_file = os.path.join(os.path.dirname(__file__), params['model'])
predict = p.GenderPredict(model_file=model_file, tokenizer=params['tokenizer'], max_len=params['max_len'])