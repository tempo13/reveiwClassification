from crawl_util import *
import time
import json


class NProductReview:

    def __init__(self, gender):
        self.prd_list = None
        self.body_info = None
        self.crawl = Fetch()
        self.gender = gender if gender else None
        return

    def item_parser(self, json_data):
        review_list = json_data.get('reviews')
        result = []
        for r in review_list:
            uid = r.get('uniqueKey')
            title = r.get('title')
            content_elm = r.get('content', '')
            content = BeautifulSoup(content_elm, 'html.parser').get_text()
            item = {'id': uid, 'title': title, 'content': content, 'gender': self.gender}
            result.append(item)
        return result

    def crawl_item(self, prd_id, last_page=2):
        # prd_id = '17448180303'
        params = {'nvMid': prd_id, 'reviewType': 'ALL', 'sort': 'RECENT', 'isNeedAggregation': 'N',
                  'isApplyFilter': 'N', 'pageSize': 20}
        raw, result = [], []
        for i in range(1, last_page):
            params.update({'page': i})
            res = self.crawl.fetch_get(u.N_REVIEW, params=params)
            try:
                json_data = res.json()
                raw.append(json_data)
                item_result = self.item_parser(json_data)
                result.extend(item_result)
            except Exception as e:
                print(str(e))
                continue
            time.sleep(random.uniform(1, 3))
        return raw, result

if __name__ == '__main__':
    import pickle
    prd_id, g = '17448180303', "여성"
    crawl = NProductReview(g)
    item_raw, item_result = crawl.crawl_item(prd_id, 500)
    with open(f'n_review_raw_{prd_id}.pickle', 'wb') as f:
        pickle.dump(item_raw, f, pickle.HIGHEST_PROTOCOL)

    with open(f'n_review_result_{prd_id}.pickle', 'wb') as f:
        pickle.dump(item_result, f, pickle.HIGHEST_PROTOCOL)