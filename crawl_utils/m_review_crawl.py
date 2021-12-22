from tqdm import tqdm
from .crawl_util import *
import time
import json

class MsProductReview:

    def __init__(self, gender=None):
        self.prd_list = None
        self.body_info = None
        self.load_parser()
        self.crawl = Fetch()
        if gender and gender not in ['M', 'F']:
            raise KeyError
        self.gender = gender
        return

    def load_parser(self):
        f = open('crawl_utils/elementSelectorDict.json')
        selector_meta = json.load(f)
        m = selector_meta.get('MSA')
        self.prd_list = m.get('item_list')
        self.body_info = m.get('body_info')
        self.item_list = m.get('list_item')
        self.list_attr = m.get('list_attr')
        self.prd_url = m.get('list_attr')
        self.review_cnt = m.get('review_cnt')
        self.review_id = m.get('review_id')

    def parse_item(self, html_txt):
        html = BeautifulSoup(html_txt, 'html.parser')
        review_list = html.select(self.prd_list)
        result = []
        for x in review_list:
            txt_list = [t.get_text() for t in x.find_all('div') if len(t.find_all()) == 0]
            review_txt = max(txt_list, key=len)
            body_info_list = [x.get_text() for x in html.select(self.body_info) if len(x.find_all()) == 0]
            body_info = body_info_list[0] if body_info_list else ""
            gender = body_info.split(",")[0]
            review_elm = x.select(f"div[{self.review_id}]")
            review_id = review_elm[0][self.review_id] if review_elm else None
            item = {'review': review_txt, 'gender': gender, 'review_id': review_id}
            result.append(item)
        return result

    def parse_list(self, html_text):
        html = BeautifulSoup(html_text, 'html.parser')
        item_list = html.select(self.item_list)
        goods_list = [x.attrs.get(self.list_attr, None) for x in item_list if self.list_attr in x.attrs.keys()]
        return goods_list

    def crawl_list(self):
        target_url = u.MSA_BEST
        self.crawl = Fetch()
        if self.gender is not None:
            self.crawl.sess.headers.update({'cookie': f'_gf={self.gender}'})
        res = self.crawl.fetch_get(target_url)
        if not res:
            raise ValueError

        goods_list = self.parse_list(res.text)
        return goods_list

    def crawl_category_list(self):
        target_url = u.MSA_CATEGORY
        self.crawl = Fetch()
        if self.gender is not None:
            self.crawl.sess.headers.update({'cookie': f'_gf={self.gender}'})

    def crawl_item(self, goods_no, last_page=10):
        result = []
        target_url = u.MSA
        params = {'sort': 'new', 'selectedSimilarNo': 0, 'goodsNo': goods_no, 'page': 1}
        # page 1 crawl total count.
        res = self.crawl.fetch_get(target_url, params)
        html_text = str(res.text).replace('<br>', '')
        total_page = self.get_review_cnt(html_text)
        if total_page < 1:
            return result
        last_page = last_page if last_page < total_page else total_page
        item = self.parse_item(html_text)
        result.extend(item)

        print('URL: %s' % u.MSA_PRD + goods_no, 'last page: %s' % last_page)
        try:
            for i in tqdm(range(2, last_page)):
                params.update({'page': i})
                res = self.crawl.fetch_get(target_url, params)
                if not res:
                    raise ValueError
                html_text = str(res.text).replace('<br>', '')
                item = self.parse_item(html_text)
                result.extend(item)
                time.sleep(random.uniform(1, 1.5))
        except Exception as e:
            print(e)
            return result
        return result

    def get_review_cnt(self, html_text: str):
        html = BeautifulSoup(html_text, 'html.parser')
        rv_elm = html.select(self.review_cnt)
        parse_num = parse_number(rv_elm[0].get_text()) if rv_elm else []
        review_cnt = parse_num[0] if parse_num else "0"
        review_cnt = int(float(review_cnt))
        return review_cnt

    def main(self):
        stop_stack = 0
        goods_list = self.crawl_list()
        review_list = []
        print("=" * 30 + str(len(goods_list)) + "=" * 30)       # Start print
        for g in goods_list:
            if stop_stack > len(goods_list) // 2:
                break
            try:
                r = self.crawl_item(g, 100)
                print(str(g)+"=" * 30 + str(len(r)) + "=" * 30)     # Print Process
                review_list.extend(r)
            except Exception as e:
                stop_stack += 1
                print(str(e))
                continue
            time.sleep(random.uniform(1, 3))
        return review_list


if __name__ == '__main__':
    # 2081554, NP Padding
    crawl = MsProductReview()
    import pickle
    review_list = crawl.main()
    with open('review_list.pickle', 'wb') as f:
        pickle.dump(review_list, f, pickle.HIGHEST_PROTOCOL)