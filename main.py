from crawl_utils import m_review_crawl
import pandas as pd
import time, random
import pickle

def save_file(data, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def m_product_review():
    gender = 'M'
    pickle_file_name = f'product_review_{gender}.pickle'
    crawl = m_review_crawl.MsProductReview(gender)
    review_list = []
    goods_list = crawl.crawl_list()
    print("=" * 30 + str(len(goods_list)) + "=" * 30)  # Start print
    for g in goods_list:
        try:
            r = crawl.crawl_item(g, 100)
            print(str(g) + "=" * 30 + str(len(r)) + "=" * 30)  # Print Process
            review_list.extend(r)
            save_file(review_list, pickle_file_name)
        except Exception as e:
            print(str(e))
            continue
        time.sleep(random.uniform(2, 3))

    df = pd.DataFrame.from_records(review_list)
    df.to_csv(f'product_review_{gender}.csv', encoding='utf-8-sig', index=False)

def m_product_review_all(prd_id, page:int=100):
    result_list = []
    pickle_file_name = f'product_review_{prd_id}.pickle'
    crawl = m_review_crawl.MsProductReview()
    r = crawl.crawl_item(prd_id, page)
    result_list.extend(r)
    save_file(result_list, pickle_file_name)
    df = pd.DataFrame.from_records(result_list)
    df.to_csv(f'product_review_{prd_id}.csv', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    # prd_id = '544003'
    # prd_id = '867282'
    # prd_id = '1324127'
    # prd_id = '623695'
    # prd_id = '1540380'
    # prd_id = '1139338'
    # prd_id = '1773782'
    # prd_id = '1145380'
    prd_id = '1628385'
    m_product_review_all(prd_id, 3000)