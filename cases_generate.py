
# coding: utf-8

import pandas as pd

metadata = pd.read_csv('data/cases_metadata.csv')
countries = pd.read_csv('data/countries.csv')
subjects = pd.read_csv('data/subjects.csv')
citations = pd.read_csv('data/citations.csv')
citations['paragraph'] = citations['target'] + '-' + citations['paragraph']

merge_1 = countries.merge(metadata.drop('country', axis=1), on='source', how='left')
merge_2 = subjects.merge(merge_1, on='source', how='inner')
merge_3 = citations.merge(merge_2, on='source', how='inner')

def convert_nan(df, columns):
    for column in columns:
        df[str(column)] = ['not_specified' if str(i) == 'nan' else i for i in df[str(column)]]
    return df

df = convert_nan(merge_3, list(merge_3.columns))

df.to_csv('data/cases.csv', header=True, index=False, encoding='utf8')

