from crawl_util import *
import json

class MsProductReview:

    def __init__(self):
        self.prd_list = None
        self.body_info = None
        self.load_parser()
        return

    def load_parser(self):
        f = open('elementSelectorDict.json')
        selector_meta = json.load(f)
        m = selector_meta.get('Musinsa')
        self.prd_list = m.get('item_list')
        self.body_info = m.get('body_info')

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
            item = {'review': review_txt, 'gender': gender}
            result.append(item)
        return result

    def crawl_main(self, goods_no, last_page=1):
        result = []
        crawl = Fetch()
        target_url = u.MSA
        params = {'sort': 'new', 'selectedSimilarNo': 0, 'goodsNo': goods_no}
        for i in range(1, last_page):
            params.update({'page': i})
            res = crawl.fetch_get(target_url, params)
            if not res:
                raise ValueError
            html_text = str(res.text).replace('<br>', '')
            item = self.parse_item(html_text)
            result.append(item)
        return result


if __name__ == '__main__':
    # 2081554, NP Padding
    crawl = MsProductReview()
    import pprint
    pprint.pprint(crawl.crawl_main('2081554'))