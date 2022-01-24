from crawl_utils import m_review_crawl
import pandas as pd
import time, random
import pickle


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
            m_review_crawl.save_file(review_list, pickle_file_name)
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
    m_review_crawl.save_file(result_list, pickle_file_name)
    df = pd.DataFrame.from_records(result_list)
    df.to_csv(f'product_review_{prd_id}.csv', encoding='utf-8-sig', index=False)
    prd_info = crawl.get_prd_info(prd_id)
    return prd_info


if __name__ == '__main__':
    prd_id_list = []
    prd_id_list = list(set(prd_id_list))
    info_list = []
    for prd_id in prd_id_list:
        prd_i = m_product_review_all(prd_id, 2000)
        info_list.append(prd_i)
        time.sleep(random.uniform(2, 3))

    df = pd.DataFrame.from_records(info_list)
    try:
        info_file = pd.read_csv('prd_info.csv')
        df = info_file.append(df)
    except:
        pass
    df.to_csv('prd_info.csv', index=False, encoding='utf-8-sig')
