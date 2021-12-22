import pandas as pd


def classify_woman(txt):
    ko_woman_list = ['엄마', '누나', '여자친구', '여동생', '이모', '고모', '어머니']
    # label 0: Man, 1: Woman
    label = 1
    t = txt.replace(" ", "")
    for k in ko_woman_list:
        if k in t:
            label = 0
    return label

def gender_tag(txt):
    if txt is None:
        return None
    gender = 1 if txt == "여성" else 0
    return gender

def data_cleaner(file_name):
    df = pd.read_csv(f'../data/{file_name}.csv')
    df['gender'] = df['review'].apply(classify_woman)
    df = df[df['gender'] == 1]
    return df

def gender_label(df: pd.DataFrame):
    df['label'] = df['gender'].apply(gender_tag)
    res = df[['review', 'label', 'review_id']]
    res = res.rename(columns={'label': 'gender'})
    return res


if __name__ == '__main__':
    # # Woman Product Review cleaner
    # result_df = pd.DataFrame()
    # file_list = ['product_review_1829767', 'product_review_803037', 'product_review_1867509']
    # for f in file_list:
    #     result_df = result_df.append(data_cleaner(f))
    # result_df.to_csv('../data/product_underware_beauty_review.csv', index=False, encoding='utf-8-sig')

    # # review Merge
    # result_df = pd.DataFrame()
    # file_list = ['product_review_2037167', 'product_review_2058188', 'product_review_1848166',
    #              'product_review_1611891', 'product_review_1417691', 'product_review_F']
    # for f in file_list:
    #     result_df = result_df.append(gender_label(pd.read_csv(f'../data/{f}.csv')))
    #
    # result_df.to_csv('../data/product_review_merge.csv', index=False, encoding='utf-8-sig')

    # # review Merge
    result_df = pd.DataFrame()
    file_list = ['comment_refine_result', 'product_review_merge', 'product_underware_beauty_review']
    for f in file_list:
        result_df = result_df.append(pd.read_csv(f'../data/{f}.csv'))

    result_df.to_csv('../data/comment_merge.csv', index=False, encoding='utf-8-sig')
