from crawl_utils import m_review_crawl
import pandas as pd
import pickle

def m_product_review():
    gender = 'F'
    crawl = m_review_crawl.MsProductReview(gender)
    result = crawl.main()
    with open(f'product_review_{gender}.pickle', 'wb') as f:
        pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)
    df = pd.DataFrame.from_records(result)
    df.to_csv(f'product_review_{gender}.csv', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    m_product_review()