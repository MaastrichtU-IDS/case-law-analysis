
# coding: utf-8
import pandas as pd
import matplotlib.pyplot as plt
# ### Merging judgements and orders

df_o = pd.read_csv('../data/order_metadata.csv', encoding='Latin-1') 
df_j = pd.read_csv('../data/judgement_metadata.csv', encoding='Latin-1') #utf8 expected characters
df_j = df_j[list(df_o.columns.values)] #order the columns
df_j['case_type'] = 'Judgement'
df_o['case_type'] = 'Order'
raw = df_j.append(df_o, ignore_index=True)

def get_grouped_df (df, identifier, groupedby):
    subjects = df.groupby(identifier).count()[groupedby]
    df.index = df[identifier]
    df = df.loc[:, df.columns != groupedby]
    df = df[~df.index.duplicated(keep='first')]
    assert len(subjects) == len(df)
    df = df.join(subjects, how='left').reset_index(drop=True)
    return df

df = get_grouped_df(raw, 'source', 'main_subject')

def convert_nan(df, columns):
    for column in columns:
        df[str(column)] = ['not_specified' if str(i) == 'nan' else i for i in df[str(column)]]
    return df

df = convert_nan(df, ['judge','advocate','chamber','country'])

def to_str(df):
    columns = [i for i in df.columns.values]
    for column in columns:
        df[str(column)] = df[str(column)].apply(lambda x: str(x))
    return df

df = to_str(df)

df['lodge_date'] = pd.to_datetime(df['lodge_date'],format= '%d/%m/%Y')
df['document_date'] = pd.to_datetime(df['document_date'],format= '%d/%m/%Y')
df['year_document'] = pd.DatetimeIndex(df['document_date']).year
df['month_document'] = pd.DatetimeIndex(df['document_date']).month
df['year_lodge'] = pd.DatetimeIndex(df['lodge_date']).year
df['month_lodge'] = pd.DatetimeIndex(df['lodge_date']).month

#data correction
df.loc[df['source'] == '62014CJ0049','lodge_date'] = pd.to_datetime('23/01/2014',format= '%d/%m/%Y')
df.loc[df['source'] == '61969CJ0074','lodge_date'] = pd.to_datetime('04/12/1969',format= '%d/%m/%Y')

#add features
df['case_time'] = df['document_date'] - df['lodge_date']
df['n_countries'] = df['country'].apply(lambda x: len(x.split(';')) if x != 'nan' else 0)

#data correction
df.loc[df['country']=='La Pergola','judge'] = 'La Pergola'
df.loc[df['country']=='La Pergola','advocate'] = 'Jacobs'

#Incorrect countries
cases ={
('Provisional data','not_specified'),
('NLD','Netherlands'),
('La Pergola','not_specified'),
('GBR','United Kingdom'),
('FRA','France'),
('FIN','Finland'),
('DEU','Germany'),
('BEL','Belgium'),
('XX','not_specified'),
('USA','United States')
}

def find_replace(l, cases):
    for a, b in cases:
        l = [row.replace(a, b) for row in l]
    return l

#reparing features
df['country'] = find_replace(df['country'], cases)
df['joined_cases'] = [1 if i.find('oin')!=-1 else 0 for i in df['case_label']]
df['ecli'] = [i[22:] for i in df['ecli']]

#Incorrect chambers
cases2 ={
('512032','Sixth Chamber'),
('512031','Sixth Chamber'),
('sixième chambre','Sixth chamber'),
('sixiÃ¨me chambre','Sixth chamber'),
('as amended by Order of 10 July 1975','First chamber')
}

#reparing chambers
df['chamber'] = find_replace(df['chamber'], cases2)
df['country-chamber'] = df['country']+'-'+df['chamber']


# ## Validation of columns in rulings

df_or = pd.read_csv('../data/orders_ruling.csv', encoding='Latin-1') 
df_jr = pd.read_csv('../data/judgements_ruling.csv', encoding='Latin-1') #utf8 expected characters
df_jr = df_jr[list(df_or.columns.values)] #order the columns
raw_r = df_jr.append(df_or, ignore_index=True)

df_r = get_grouped_df(raw_r, 'c1', 'c2')
df_r = df_r[['c1','c3','c4','c5','c6','c7']]
df_r.columns = ['source','ruling_name','ruling_type','ruling_content','case_label','extra']

df_r = convert_nan(df_r, ['ruling_type','ruling_content','case_label','extra'])

#correction 62011CJ0363
df_r.loc[df_r['source'] == '62011CJ0363', 'ruling_name'] = list(df.loc[df['source'] == '62011CJ0363', 'ruling_name'])[0]
df_r.loc[df_r['source'] == '62011CJ0363', 'ruling_type'] = list(df.loc[df['source'] == '62011CJ0363', 'ruling_type'])[0]
df_r.loc[df_r['source'] == '62011CJ0363', 'ruling_content'] = list(df.loc[df['source'] == '62011CJ0363', 'ruling_content'])[0]

#correction 62011CJ0363
df_r.loc[df_r['source'] == '62015CO0462', 'ruling_name'] = list(df.loc[df['source'] == '62015CO0462', 'ruling_name'])[0]
df_r.loc[df_r['source'] == '62015CO0462', 'ruling_type'] = list(df.loc[df['source'] == '62015CO0462', 'ruling_type'])[0]
df_r.loc[df_r['source'] == '62015CO0462', 'ruling_content'] = list(df.loc[df['source'] == '62015CO0462', 'ruling_content'])[0]

df_r = df_r.drop(['extra'],axis=1)

_slice = df_r[df_r['case_label']=='not_specified']
_slice = _slice.reset_index(drop=True)
_slice['case_label'] = list(_slice.loc[:,('ruling_content')])
_slice['ruling_content'] = list(_slice.loc[:,('ruling_type')])
_slice['ruling_type'] = list(_slice.loc[:,('ruling_name')])

df_r = df_r.drop(df_r[df_r['source'].isin(list(_slice['source']))].index)
df_r = df_r.append(_slice).reset_index(drop=True)

_slice2 = df_r[df_r['case_label']=='not_specified']
_slice2 = _slice2.reset_index(drop=True)
_slice2['case_label'] = list(_slice2.loc[:,('ruling_content')])
_slice2['ruling_content'] = list(_slice2.loc[:,('ruling_type')])

df_r = df_r.drop(df_r[df_r['source'].isin(list(_slice2['source']))].index)
df_r = df_r.append(_slice2).reset_index(drop=True)

#data correction
df_r.loc[df_r['source'] == '62008CJ0202', 'ruling_name'] = list(df.loc[df['source'] == '62008CJ0202', 'ruling_name'])[0]
df_r.loc[df_r['source'] == '62008CO0561', 'ruling_name'] = list(df.loc[df['source'] == '62008CO0561', 'ruling_name'])[0]

df_r = df_r.drop(['case_label'],axis=1)

#label creation
df_r['v_in_ruling_name'] = [1 if i.find(' v ')!=-1 else 0 for i in df_r['ruling_name']]
df_r['reference_in_ruling_name'] = [1 if i.find('eference')!=-1 else 0 for i in df_r['ruling_name']]
df_r['request_in_ruling_name'] = [1 if i.find('equest')!=-1 else 0 for i in df_r['ruling_name']]
df_r['Criminal_in_ruling_name'] = [1 if i.find('Criminal')!=-1 else 0 for i in df_r['ruling_name']]

_cases = df_r[df_r['v_in_ruling_name']==0]
_cases = _cases[(_cases['reference_in_ruling_name']==1) | (_cases['request_in_ruling_name']==1)]

df_r['dashes_in_ruling_name'] = [len(i) for i in df_r['ruling_name'].str.findall(' - ')]
df_r['case_in_ruling_name'] = [1 if i.find('C-')!=-1 else 0 for i in df_r['ruling_name']]

_cases = df_r[(df_r['case_in_ruling_name'] == 1) & (df_r['v_in_ruling_name'] ==0) & (df_r['Criminal_in_ruling_name'] == 0)]

df_r['v_in_ruling_type'] = [1 if i.find(' v ')!=-1 else 0 for i in df_r['ruling_type']]
df_r['reference_in_ruling_type'] = [1 if i.find('eference')!=-1 else 0 for i in df_r['ruling_type']]
df_r['request_in_ruling_type'] = [1 if i.find('equest')!=-1 else 0 for i in df_r['ruling_type']]

_cases = df_r[df_r['v_in_ruling_type']==1] 
_cases = _cases[(_cases['reference_in_ruling_type']==0) & (_cases['request_in_ruling_type']==0)]

df_r = df_r.merge(pd.DataFrame({'source':list(_cases['source']),'type_not_specified':[1]*len(_cases)}), how='left', on='source')

df_r['ruling_type'] = ['not_specified' if j ==1 else i for i,j in zip(df_r['ruling_type'],df_r['type_not_specified']) ]
df_r['dashes_in_ruling_type'] = [len(i) for i in df_r['ruling_type'].str.findall(' - ')]

_cases = df_r[df_r['dashes_in_ruling_type'] > 1]
_cases = _cases[(_cases['reference_in_ruling_type']==0) & (_cases['request_in_ruling_type']==0)]

value1 = list(df_r.loc[df_r['source'] == '61997CJ0254', 'ruling_type'])[0]
value2 = list(df_r.loc[df_r['source'] == '61997CJ0254', 'ruling_content'])[0]
df_r.loc[df_r['source'] == '61997CJ0254', 'ruling_type'] = value2
df_r.loc[df_r['source'] == '61997CJ0254', 'ruling_content'] = value1

# ## Final Merge
columns = ['source', 'case_label', 'ecli', 'case_type', 'judge', 'advocate', 'country', 'country-chamber','chamber', 'main_subject',
 'lodge_date', 'document_date','year_document', 'month_document', 'year_lodge', 'month_lodge', 'case_time', 'n_countries', 'joined_cases']
df = df[columns]
df_r = df_r[['source','ruling_name','ruling_type','ruling_content']]
df = df.merge(df_r, on='source')

#write to file
df.to_csv('../data/cases.csv', header=True, index=False, encoding='utf8')

