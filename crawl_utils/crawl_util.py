from bs4 import BeautifulSoup
import requests
import pickle
import random
from crawl_utils import url_list as u
import re

class Fetch:

    def __init__(self):
        self.sess = requests.session()
        self.ua_list = None
        self.load_ua_list()

    def load_ua_list(self):
        try:
            with open('crawl_utils/ua_list.pickle', 'rb') as f:
                self.ua_list = pickle.load(f)
        except:
            self.get_ua()

        self.sess.headers = {
            'user-agent': random.choice(self.ua_list)
        }

    def get_ua(self):
        url = u.UA_URL
        try:
            res = requests.get(url)
            html = BeautifulSoup(res.text, 'html.parser')
            self.ua_list = [x.get_text() for x in html.select('td > a.code')]
            pickle.dump(self.ua_list, open('ua_list.pickle', 'wb'), pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            self.ua_list = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            ]

    def fetch_get(self, target_url, params=None):
        result = None
        try:
            res = self.sess.get(target_url, params=params)
            res.raise_for_status()
            result = res
        except Exception as e:
            print("raise Error cause: %e" %e)
        return result


def parse_number(txt):
    """
    숫자가 포함된 텍스트를 받아 숫자를 찾아줌
    :param txt: 텍스트
    :return: 만약 숫자가 있으면 숫자 텍스트만, 없으면 빈 리스트
    """
    result = re.findall(r'\d+', txt)
    return result

def clear_txt(txt):
    txt = txt.replace('\n', '').replace('\r', '').replace('\t', '')
    return txt

def save_file(data, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def load_pickle_file(file_name):
    with open(file_name, 'rb') as f:
        result = pickle.load(f)
    return result